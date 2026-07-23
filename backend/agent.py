"""
Week 4 Research Agent
=====================
Demonstrates: skill (web_search), memory (in-memory list), hook (log_tool_call
decorator), plugin (read_file), and an agentic loop that drives Claude via the
raw Anthropic REST API using `requests`.

Pieces at a glance
------------------
SKILL    – web_search(query)     calls Tavily to retrieve live web results
PLUGIN   – read_file(path)       reads .txt or .pdf files and returns text
HOOK     – @log_tool_call        decorator that logs every tool invocation
MEMORY   – session_memory list   stores facts so the agent can recall them
LOOP     – run_agent(question)   sends messages to Claude, handles tool calls,
                                 feeds results back, repeats until done
"""

import os
import re
import sys
import json
from datetime import datetime
from functools import wraps

import requests
from dotenv import load_dotenv

# Force UTF-8 output on Windows so Claude's Unicode responses print correctly.
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# ── Load environment variables from backend/.env ──────────────────────────────
load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TAVILY_API_KEY    = os.environ["TAVILY_API_KEY"]
MODEL             = "claude-sonnet-5"

# ── MEMORY ────────────────────────────────────────────────────────────────────
# A simple in-memory list that persists for the lifetime of one agent run.
# The agent (and we) can append facts to it and include them in the system
# prompt so Claude can "recall" them on later turns.
session_memory: list[str] = []


def remember(fact: str) -> None:
    """Store a fact in session memory."""
    session_memory.append(fact)


def memory_context() -> str:
    """Return all stored facts as a block to inject into the system prompt."""
    if not session_memory:
        return ""
    lines = "\n".join(f"- {f}" for f in session_memory)
    return f"\n\nThings you already know from this session:\n{lines}"


# ── HOOK ──────────────────────────────────────────────────────────────────────
# A decorator that wraps any tool function and prints a timestamped log line
# before the tool runs.  Apply it with @log_tool_call above a function.
def log_tool_call(fn):
    """Decorator – logs tool name, arguments, and timestamp before execution."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ts   = datetime.now().strftime("%H:%M:%S")
        name = fn.__name__
        # Build a readable argument string
        arg_parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        print(f"[{ts}] TOOL CALL -> {name}({', '.join(arg_parts)})")
        return fn(*args, **kwargs)
    return wrapper


# ── SKILL: web_search ─────────────────────────────────────────────────────────
# Calls the Tavily Search API and returns a short summary of the top results.
# Tavily is purpose-built for LLM agents; it returns clean, pre-extracted text.
@log_tool_call
def web_search(query: str) -> str:
    """SKILL – search the web via Tavily and return a text summary."""
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query":   query,
            "max_results": 3,
            "include_answer": True,
        },
        timeout=15,
    )
    data = response.json()

    # Tavily often provides a direct answer; fall back to individual results.
    if data.get("answer"):
        return data["answer"]

    results = data.get("results", [])
    if not results:
        return "No results found."

    snippets = []
    for r in results[:3]:
        snippets.append(f"[{r.get('title', '')}] {r.get('content', '')[:300]}")
    return "\n\n".join(snippets)


# ── PLUGIN: read_file ─────────────────────────────────────────────────────────
# Reads a .txt or .pdf file from disk and returns its text content.
# Useful for letting the agent consult local documents.
@log_tool_call
def read_file(path: str) -> str:
    """PLUGIN – read a .txt or .pdf file and return its text content."""
    if not os.path.exists(path):
        return f"Error: file not found: {path}"

    if path.lower().endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            pages  = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages).strip() or "PDF contained no extractable text."
        except Exception as e:
            return f"Error reading PDF: {e}"

    if path.lower().endswith(".txt"):
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    return "Error: only .txt and .pdf files are supported."


# ── TOOL REGISTRY ─────────────────────────────────────────────────────────────
# Maps tool name strings (as Claude will emit them) to the actual functions.
TOOLS = {
    "web_search": web_search,
    "read_file":  read_file,
}


# ── SYSTEM PROMPT ─────────────────────────────────────────────────────────────
# Instructs Claude on the text-based tool-call format we parse below.
# We avoid the SDK's native tool-calling because we are using raw requests.
SYSTEM_TEMPLATE = """\
You are a helpful research assistant with access to two tools.

To use a tool, respond with EXACTLY this format on its own line (nothing before or after on that line):
TOOL: tool_name("argument")

Available tools:
- web_search("query")   – search the web for current information
- read_file("path")     – read a local .txt or .pdf file

Rules:
1. Use a tool whenever you need information you don't have.
2. After receiving a tool result, continue reasoning and use more tools if needed.
3. When you have enough information, give your final answer as plain text with no TOOL: prefix.
4. Never fabricate tool results — only use what is returned to you.{memory}
"""


def build_system_prompt() -> str:
    """Inject current session memory into the system prompt."""
    return SYSTEM_TEMPLATE.format(memory=memory_context())


# ── TOOL CALL PARSER ─────────────────────────────────────────────────────────
# Looks for lines like:  TOOL: web_search("some query")
# Returns (tool_name, argument) or None if no tool call is found.
TOOL_PATTERN = re.compile(r'^TOOL:\s*(\w+)\("([^"]*)"\)', re.MULTILINE)


def parse_tool_call(text: str):
    """Extract (tool_name, argument) from Claude's response, or return None."""
    match = TOOL_PATTERN.search(text)
    if match:
        return match.group(1), match.group(2)
    return None


# ── ANTHROPIC API CALL ────────────────────────────────────────────────────────
def call_claude(messages: list[dict]) -> str:
    """Send a message list to Claude and return the assistant's text reply."""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key":          ANTHROPIC_API_KEY,
            "anthropic-version":  "2023-06-01",
            "content-type":       "application/json",
        },
        json={
            "model":      MODEL,
            "max_tokens": 1024,
            "system":     build_system_prompt(),
            "messages":   messages,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    # Collect all text blocks (API may return multiple or non-text blocks)
    text_parts = [block["text"] for block in data["content"] if block.get("type") == "text"]
    return "\n".join(text_parts)


# ── AGENTIC LOOP ──────────────────────────────────────────────────────────────
# 1. Send the user question to Claude.
# 2. If Claude's reply contains a TOOL: call, run the tool (hook logs it).
# 3. Append the tool result as a user message and call Claude again.
# 4. Repeat until Claude gives a reply with no tool call → that is the answer.
def run_agent(question: str, max_turns: int = 8) -> str:
    """Run the agentic loop for a single question and return the final answer."""
    print(f"\n{'='*60}")
    print(f"QUESTION: {question}")
    print(f"{'='*60}\n")

    messages = [{"role": "user", "content": question}]

    for turn in range(1, max_turns + 1):
        print(f"-- Turn {turn} --------------------------------------------")
        reply = call_claude(messages)
        print(f"Claude: {reply}\n")

        tool_call = parse_tool_call(reply)

        if tool_call is None:
            # No tool call → Claude is done; this is the final answer.
            return reply

        tool_name, argument = tool_call
        print(f"  -> Detected tool call: {tool_name}({argument!r})")

        if tool_name not in TOOLS:
            tool_result = f"Error: unknown tool '{tool_name}'"
        else:
            tool_result = TOOLS[tool_name](argument)

        print(f"  -> Tool result: {tool_result[:200]}{'...' if len(tool_result) > 200 else ''}\n")

        # Append the assistant's tool-call message and the tool result so
        # Claude has full context on the next turn.
        messages.append({"role": "assistant", "content": reply})
        messages.append({
            "role":    "user",
            "content": f"Tool result for {tool_name}({argument!r}):\n{tool_result}",
        })

    return "Agent reached the maximum number of turns without a final answer."


# ── DEMO ──────────────────────────────────────────────────────────────────────
# This demo shows all four pieces working together:
#   - MEMORY:  we pre-load a fact the agent will need to recall
#   - HOOK:    logged automatically by @log_tool_call on web_search / read_file
#   - SKILL:   web_search is called during the loop
#   - PLUGIN:  read_file is available (not called in this demo unless needed)
#   - LOOP:    multi-turn until Claude has a complete answer
if __name__ == "__main__":
    # Seed memory with a fact from "earlier in the session"
    remember("The user is a software engineering intern at Arbisoft.")
    remember("The user is particularly interested in how AI agents are used in real products.")

    # Multi-hop question: requires a web search AND recalling the memory fact
    question = (
        "Search the web for one real product that uses an AI agent with tool-calling, "
        "then explain why that kind of product might be especially relevant to the user "
        "based on what you already know about them."
    )

    answer = run_agent(question)

    print(f"\n{'='*60}")
    print("FINAL ANSWER")
    print(f"{'-'*60}")
    print(answer)
