"""
MCP Server — Todos Demo
=======================
This file implements a standalone MCP (Model Context Protocol) server that
exposes the project's SQLite todos database to any MCP-compatible client
(e.g. Claude Code, Claude Desktop, or a custom agent).

--------------------------------------------------------------------
WHAT IS MCP?
--------------------------------------------------------------------
MCP is an open protocol that lets LLM applications connect to external
data sources and tools in a standardised way.  Think of it like a USB-C
standard for AI: the client (Claude) plugs into any MCP server without
needing custom integration code for each one.

An MCP server exposes two main primitives:

  RESOURCE  — read-only data the model can inspect, like a file or a
              database query result.  The client fetches it by URI.
              Analogy: a webpage you can GET.

  TOOL      — an action the model can invoke, like calling a function.
              The client calls it with arguments and gets a result back.
              Analogy: a POST endpoint.

--------------------------------------------------------------------
HOW TO RUN THIS SERVER
--------------------------------------------------------------------
From inside the backend/ folder:

    python mcp_server.py

The server speaks the MCP stdio transport: it reads JSON-RPC from
stdin and writes responses to stdout.  You never run it manually in
a terminal yourself — an MCP client (like Claude Code) launches it
as a subprocess and wires up stdin/stdout automatically.

--------------------------------------------------------------------
HOW TO CONNECT IT TO CLAUDE CODE
--------------------------------------------------------------------
Add the server to the .mcp.json file in the ROOT of this repo
(or in ~/.claude/mcp.json for a user-level config).  Claude Code
reads that file and launches the server automatically.

See the companion file .mcp.json (created alongside this file) for
the exact config snippet.

--------------------------------------------------------------------
"""

import json
import sys
import os

# The MCP package's high-level "FastMCP" class handles all the JSON-RPC
# plumbing so we can focus on declaring resources and tools.
from mcp.server.fastmcp import FastMCP

# Re-use the existing project's database session and ORM models so this
# server reads/writes the same todos.db that the FastAPI app uses.
sys.path.insert(0, os.path.dirname(__file__))
from database import SessionLocal
import models

# Ensure the database tables exist (idempotent — safe to call every startup).
from database import engine
models.Base.metadata.create_all(bind=engine)

# ── Create the MCP server ─────────────────────────────────────────────────────
# The name "todos-mcp" is what appears in the MCP client's server list.
mcp = FastMCP("todos-mcp")


# ── RESOURCE: todos://all ─────────────────────────────────────────────────────
# A RESOURCE is read-only data exposed at a URI.
# The MCP client (Claude) can fetch this URI to get context without the user
# having to copy-paste the data into the chat.
#
# When Claude Code is connected to this server and the user asks
# "what todos do I have?", Claude can call this resource and read the JSON.
@mcp.resource("todos://all")
def get_all_todos() -> str:
    """
    RESOURCE – returns every todo in the database as a JSON string.

    URI:  todos://all
    Type: text/plain  (JSON encoded as a string — MCP resources return strings)
    """
    db = SessionLocal()
    try:
        todos = db.query(models.Todo).all()
        result = [
            {
                "id":        t.id,
                "title":     t.title,
                "completed": t.completed,
                "owner_id":  t.owner_id,
            }
            for t in todos
        ]
        return json.dumps(result, indent=2)
    finally:
        db.close()


# ── TOOL: create_todo ─────────────────────────────────────────────────────────
# A TOOL is a callable action with typed parameters.
# The MCP client (Claude) can invoke this when the user asks it to create a
# todo, and Claude will decide the right title to pass in.
#
# Unlike the FastAPI endpoint, this demo tool has NO auth/ownership — it is a
# standalone MCP concept demo, not connected to the JWT system.
@mcp.tool()
def create_todo(title: str) -> str:
    """
    TOOL – create a new todo in the database.

    Args:
        title: The text of the todo item to create.

    Returns:
        A confirmation string with the new todo's id and title.

    Note: owner_id is left NULL in this demo — the MCP server is a
    separate concept demo with no auth layer.
    """
    if not title or not title.strip():
        return "Error: title cannot be empty."

    db = SessionLocal()
    try:
        todo = models.Todo(title=title.strip(), completed=False, owner_id=None)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return f"Created todo #{todo.id}: \"{todo.title}\""
    except Exception as e:
        db.rollback()
        return f"Error creating todo: {e}"
    finally:
        db.close()


# ── Entry point ───────────────────────────────────────────────────────────────
# FastMCP.run() starts the stdio transport loop.
# The process blocks here, reading MCP messages from stdin and replying on
# stdout, until the client closes the connection.
if __name__ == "__main__":
    mcp.run(transport="stdio")
