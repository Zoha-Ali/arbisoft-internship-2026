"""
Multi-Agent Orchestrator — Supervisor + Worker Pattern
=======================================================
This file demonstrates how to coordinate multiple specialised AI agents
under a single supervisor, building on the single-agent pattern in agent.py.

--------------------------------------------------------------------
HOW THIS DIFFERS FROM agent.py
--------------------------------------------------------------------
agent.py:  ONE agent, ONE agentic loop, ONE tool registry.
           The agent does everything itself — searches, reads files,
           reasons, and responds.

orchestrator.py:  ONE supervisor + MULTIPLE worker agents.

  Supervisor  – does NOT do the actual work.  Its only job is to read
                the user's request and decide WHICH worker to hand it
                to.  It outputs a routing decision, not a final answer.

  Workers     – each has its own speciality, its own system prompt,
                and its own tool registry.  The supervisor's choice
                determines which worker's agentic loop runs.

Why bother?  Each worker can be independently prompted, tuned, and
extended without touching the others.  The supervisor stays small and
its routing logic is easy to inspect and test.

--------------------------------------------------------------------
TRACING
--------------------------------------------------------------------
Every Claude call and every tool call is recorded in a shared TRACE
list with a timestamp and the name of the agent that made it.
After a run you can print the full trace to see the exact path a
request took through the agent graph.

--------------------------------------------------------------------
"""

import os
import re
import sys
import json
from datetime import datetime
from functools import wraps, partial

import requests
from dotenv import load_dotenv

# Force UTF-8 on Windows terminals (same fix as agent.py).
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
TAVILY_API_KEY    = os.environ["TAVILY_API_KEY"]
MODEL             = "claude-sonnet-5"

# ── SHARED TRACE ──────────────────────────────────────────────────────────────
# A single list that records every significant event across the whole agent
# graph — supervisor routing decisions AND worker tool calls — so you can
# reconstruct the full execution path after the run.
#
# Each entry is a dict:
#   { "ts": "HH:MM:SS", "agent": "<name>", "event": "<description>" }
TRACE: list[dict] = []


def trace(agent: str, event: str) -> None:
    """Append a timestamped event to the global trace log."""
    entry = {
        "ts":    datetime.now().strftime("%H:%M:%S"),
        "agent": agent,
        "event": event,
    }
    TRACE.append(entry)
    # Print immediately so you can watch the trace build up in real time.
    print(f"  [TRACE {entry['ts']}] [{agent}] {event}")


def print_trace() -> None:
    """Pretty-print the full trace after a run."""
    print("\n" + "=" * 60)
    print("FULL EXECUTION TRACE")
    print("=" * 60)
    for e in TRACE:
        print(f"  {e['ts']}  {e['agent']:<20} {e['event']}")
    print("=" * 60)


# ── AGENT-AWARE TOOL HOOK ─────────────────────────────────────────────────────
# Extended version of @log_tool_call from agent.py.
# In agent.py the hook always says "TOOL CALL" with no agent context.
# Here every tool call is attributed to the agent that invoked it, which
# is essential for understanding multi-agent traces.
def make_tool_hook(agent_name: str):
    """
    Returns a decorator that logs tool calls attributed to `agent_name`.

    Usage:
        tool_hook = make_tool_hook("research_worker")

        @tool_hook
        def web_search(query): ...
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            arg_parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
            call_str  = f"{fn.__name__}({', '.join(arg_parts)})"
            trace(agent_name, f"TOOL CALL -> {call_str}")
            result = fn(*args, **kwargs)
            # Log a short preview of the result so the trace stays readable.
            preview = str(result)[:120].replace("\n", " ")
            trace(agent_name, f"TOOL RESULT <- {preview}{'...' if len(str(result)) > 120 else ''}")
            return result
        return wrapper
    return decorator


# ── CORE CLAUDE CALLER ────────────────────────────────────────────────────────
# Reused from agent.py — sends a message list to Claude with a given system
# prompt and returns the assistant's text.
def call_claude(system: str, messages: list[dict], max_tokens: int = 1024) -> str:
    """Call the Anthropic API and return the assistant's text reply."""
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key":         ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        },
        json={
            "model":      MODEL,
            "max_tokens": max_tokens,
            "system":     system,
            "messages":   messages,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    text_parts = [b["text"] for b in data["content"] if b.get("type") == "text"]
    return "\n".join(text_parts)


# ── TOOL CALL PARSER ──────────────────────────────────────────────────────────
# Same regex as agent.py — matches  TOOL: name("argument")
TOOL_PATTERN = re.compile(r'^TOOL:\s*(\w+)\("([^"]*)"\)', re.MULTILINE)


def parse_tool_call(text: str):
    """Return (tool_name, argument) if the text contains a tool call, else None."""
    m = TOOL_PATTERN.search(text)
    return (m.group(1), m.group(2)) if m else None


# ── GENERIC WORKER LOOP ───────────────────────────────────────────────────────
# Both workers use the same loop structure — only their system prompt and
# tool registry differ.  This avoids copy-pasting the loop twice.
def run_worker_loop(
    agent_name: str,
    system_prompt: str,
    tools: dict,
    task: str,
    max_turns: int = 6,
) -> str:
    """
    Agentic loop for a single worker.

    Sends `task` to Claude, handles TOOL: calls using the provided `tools`
    registry, and returns Claude's first tool-call-free reply as the answer.
    Every step is traced via `trace(agent_name, ...)`.
    """
    trace(agent_name, f"Starting task: {task[:80]}")
    messages = [{"role": "user", "content": task}]

    for turn in range(1, max_turns + 1):
        trace(agent_name, f"Calling Claude (turn {turn})")
        reply = call_claude(system_prompt, messages)

        tool_call = parse_tool_call(reply)
        if tool_call is None:
            # No tool call — this is the worker's final answer.
            trace(agent_name, "Final answer produced.")
            return reply

        tool_name, argument = tool_call
        if tool_name not in tools:
            tool_result = f"Error: unknown tool '{tool_name}'"
            trace(agent_name, f"Unknown tool requested: {tool_name}")
        else:
            tool_result = tools[tool_name](argument)   # hook fires inside here

        messages.append({"role": "assistant", "content": reply})
        messages.append({
            "role":    "user",
            "content": f"Tool result for {tool_name}({argument!r}):\n{tool_result}",
        })

    return "Worker reached max turns without a final answer."


# ═══════════════════════════════════════════════════════════════════════════════
# WORKER 1 — RESEARCH WORKER
# Specialty: answering questions that require live web information.
# Tool:      web_search  (same Tavily call as agent.py, now with agent-name trace)
# ═══════════════════════════════════════════════════════════════════════════════

_research_hook = make_tool_hook("research_worker")


@_research_hook
def web_search(query: str) -> str:
    """Search the web via Tavily and return a summary."""
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key":        TAVILY_API_KEY,
            "query":          query,
            "max_results":    3,
            "include_answer": True,
        },
        timeout=15,
    )
    data = response.json()
    if data.get("answer"):
        return data["answer"]
    results = data.get("results", [])
    if not results:
        return "No results found."
    return "\n\n".join(
        f"[{r.get('title','')}] {r.get('content','')[:300]}"
        for r in results[:3]
    )


RESEARCH_SYSTEM = """\
You are a focused research assistant.  Your only job is to answer the
user's question using web search results.

To search, respond with EXACTLY this format on its own line:
TOOL: web_search("your search query")

Rules:
1. Use web_search whenever you need information.
2. After receiving the result, answer concisely in plain text.
3. Never invent facts — only use what the search returns.
4. When you have enough information, give your final answer with NO TOOL: prefix.
"""

RESEARCH_TOOLS = {"web_search": web_search}


def research_worker(task: str) -> str:
    """Worker that answers research questions using web search."""
    return run_worker_loop("research_worker", RESEARCH_SYSTEM, RESEARCH_TOOLS, task)


# ═══════════════════════════════════════════════════════════════════════════════
# WORKER 2 — TODO WORKER
# Specialty: managing todos in the SQLite database.
# Tool:      db_create_todo  (direct DB write, same logic as the MCP tool)
# ═══════════════════════════════════════════════════════════════════════════════

_todo_hook = make_tool_hook("todo_worker")

# Import the database layer from the existing project.
sys.path.insert(0, os.path.dirname(__file__))
from database import SessionLocal, engine
import models
models.Base.metadata.create_all(bind=engine)


@_todo_hook
def db_create_todo(title: str, owner_id: int | None = None) -> str:
    """Create a new todo in the SQLite database and return a confirmation."""
    if not title.strip():
        return "Error: title cannot be empty."
    db = SessionLocal()
    try:
        todo = models.Todo(title=title.strip(), completed=False, owner_id=owner_id)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return f"Created todo #{todo.id}: \"{todo.title}\""
    except Exception as e:
        db.rollback()
        return f"Error: {e}"
    finally:
        db.close()


@_todo_hook
def db_list_todos(_: str = "") -> str:
    """Return all todos in the database as a JSON string."""
    db = SessionLocal()
    try:
        todos = db.query(models.Todo).all()
        result = [{"id": t.id, "title": t.title, "completed": t.completed} for t in todos]
        return json.dumps(result, indent=2) if result else "No todos found."
    finally:
        db.close()


TODO_SYSTEM = """\
You are a todo-management assistant with direct access to a SQLite database.

To use a tool, respond with EXACTLY this format on its own line:
TOOL: tool_name("argument")

Available tools:
- db_create_todo("title")   – create a new todo with the given title
- db_list_todos("")         – list all existing todos (pass an empty string)

Rules:
1. Use a tool for every database action — never pretend to create a todo.
2. After the tool result, confirm what you did in plain text with NO TOOL: prefix.
3. If the user asks you to create multiple todos, call db_create_todo once per item.
"""

def todo_worker(task: str, owner_id: int | None = None) -> str:
    """Worker that manages todos in the database."""
    tools = {
        # Bind owner_id so the tool loop can call it with a single string arg.
        "db_create_todo": partial(db_create_todo, owner_id=owner_id),
        "db_list_todos":  db_list_todos,
    }
    return run_worker_loop("todo_worker", TODO_SYSTEM, tools, task)


# ═══════════════════════════════════════════════════════════════════════════════
# SUPERVISOR
# The supervisor does NOT answer the user's question itself.
# It reads the request and decides which worker to delegate to.
# This keeps the routing logic simple, auditable, and separate from task logic.
# ═══════════════════════════════════════════════════════════════════════════════

SUPERVISOR_SYSTEM = """\
You are a routing supervisor.  You do NOT answer questions yourself.
Your only job is to read the user's request and decide which worker
should handle it.

Available workers:
- research_worker  : handles questions that require web search or factual
                     lookups (e.g. "what is X?", "find information about Y")
- todo_worker      : handles todo-management tasks (e.g. "add a todo",
                     "create a task", "list my todos")

Respond with EXACTLY one line — the worker name and nothing else:
research_worker
  or
todo_worker
"""


def supervisor_route(user_request: str) -> str:
    """
    Ask the supervisor Claude to pick a worker for this request.

    Returns "research_worker" or "todo_worker".
    Falls back to "research_worker" if the response is unrecognised.
    """
    trace("supervisor", f"Routing request: {user_request[:80]}")
    messages = [{"role": "user", "content": user_request}]
    decision = call_claude(SUPERVISOR_SYSTEM, messages, max_tokens=20).strip().lower()

    if "todo" in decision:
        chosen = "todo_worker"
    else:
        chosen = "research_worker"

    trace("supervisor", f"Routing decision -> {chosen}")
    return chosen


# ── TOP-LEVEL ORCHESTRATOR ────────────────────────────────────────────────────
def orchestrate(user_request: str, owner_id: int | None = None) -> dict:
    """
    Entry point for the multi-agent system.

    1. Supervisor reads the request and picks a worker.
    2. The chosen worker runs its own agentic loop.
    3. Returns {"answer": str, "trace": list[dict]} so callers get both the
       final answer and the full execution trace without relying on globals.

    owner_id is forwarded to todo_worker so todos are created under the
    correct user rather than left with a null owner.
    """
    TRACE.clear()

    print(f"\n{'='*60}")
    print(f"REQUEST: {user_request}")
    print(f"{'='*60}")

    chosen_worker = supervisor_route(user_request)

    print(f"\n  Supervisor routed to: {chosen_worker}\n")

    if chosen_worker == "todo_worker":
        answer = todo_worker(user_request, owner_id=owner_id)
    else:
        answer = research_worker(user_request)

    print(f"\n  ANSWER:\n  {answer}\n")
    print_trace()

    return {"answer": answer, "trace": list(TRACE)}


# ── DEMO ──────────────────────────────────────────────────────────────────────
# Two requests sent through the orchestrator:
#   1. A research question  -> should route to research_worker (uses web_search)
#   2. A todo action        -> should route to todo_worker (writes to DB)
#
# Watch the TRACE output to see the supervisor's routing decision and each
# worker's tool calls, all with timestamps and agent names.
if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("# DEMO 1 — Research request")
    print("#" * 60)
    result1 = orchestrate("What is the latest version of Python and what are its main new features?")
    print(f"\nTrace entries: {len(result1['trace'])}")

    print("\n" + "#" * 60)
    print("# DEMO 2 — Todo request")
    print("#" * 60)
    result2 = orchestrate("Add a todo called 'Review multi-agent orchestration notes'")
    print(f"\nTrace entries: {len(result2['trace'])}")
