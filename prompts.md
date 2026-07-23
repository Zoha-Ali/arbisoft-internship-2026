## Week 1 — Frontend Fundamentals

### June 24 — Install dependencies and verify setup

**Tool:** Claude Code
**Prompt:**

> Install dependencies in /frontend, then run npm run dev, npm run test, and npm run lint. Fix any errors that come up and tell me what you changed.

**Result:** Installed Node.js, resolved eslint-plugin-react-hooks version conflict, all tests passed, lint clean, dev server running.
**Correction:** None.
**Kept in repo at:** frontend/package.json

---

### June 24 — Build a Todos app (replace Contact route)

**Tool:** Claude Code
**Prompt:**

> Replace the Contact route with a Todos route. Build a TodoForm component with validation, a TodoList that renders TodoItems, and TodoItem with a checkbox and delete button. Lift state up to the Todos page and pass props down. Update the nav link from Contact to Todos.

**Result:** Generated TodoForm.tsx, TodoItem.tsx, TodoList.tsx, Todos.tsx with full state management and working prop drilling.
**Correction:** None.
**Kept in repo at:** frontend/src/components/Todo\*.tsx, frontend/src/routes/Todos.tsx

---

### June 24 — Style the entire UI

**Tool:** Claude Code
**Prompt:**

> Update index.css with a light off-white background, better typography, and generous spacing. Style nav links as buttons with hover states. Add form styling with borders, padding, and focus states for inputs and a teal button. Make todo items look like cards with shadows and spacing. Add strikethrough on completed items. Style error messages in red, add 0.2s transitions to interactive elements, center the "No todos yet" message in light gray, and add breathing room between nav and content.

**Result:** Completely restyled index.css with cohesive color scheme, animations, and polish.
**Correction:** None.
**Kept in repo at:** frontend/src/index.css

---

### June 24 — Write tests for Todo components

**Tool:** Claude Code
**Prompt:**

> Create TodoItem.test.tsx with 3 tests: renders title, checkbox calls toggleTodo with correct ID, delete calls deleteTodo with correct ID. Create TodoList.test.tsx with 2 tests: renders all todos, shows "No todos yet" when empty.

**Result:** Both test files generated with Vitest + React Testing Library. All 8 tests passing (4 new + 4 existing).
**Correction:** None.
**Kept in repo at:** frontend/src/components/TodoItem.test.tsx, TodoList.test.tsx

---

### June 24 — Update Home and About pages

**Tool:** Claude Code
**Prompt:**

> Replace Home.tsx with a "Welcome to my Week 1 SPA" heading and 2–3 sentences explaining it's a React app showing routing, state management, and validation. Replace About.tsx with "About This Project" and explain what the todo app demonstrates.

**Result:** Both routes now have meaningful project descriptions.
**Correction:** None.
**Kept in repo at:** frontend/src/routes/Home.tsx, About.tsx

---

### June 24 — Fix config split (Vitest vs Vite)

**Tool:** Claude Code
**Prompt:**

> Remove the test property from vite.config.ts and move it into a separate vitest.config.ts file so the build doesn't error.

**Result:** Created vitest.config.ts with test settings, cleaned up vite.config.ts. Build succeeded.
**Correction:** None.
**Kept in repo at:** frontend/vite.config.ts, vitest.config.ts

---

## Week 2

### June 29 — FastAPI Backend Setup

**Prompt:** Set up a FastAPI project with main.py, models.py, database.py, and requirements.txt with a /todos GET endpoint returning an empty list.

**Result:** Working FastAPI backend with SQLAlchemy ORM, Pydantic validation, and SQLite database. Tested on localhost:8000/todos.

**Changes:** Created backend/ folder with 4 files and deployed locally.

### July 1 — Add CRUD endpoints to FastAPI backend

**Tool:** Claude Code
**Prompt:**

> I have an existing FastAPI backend in /backend with main.py, models.py, and database.py already set up. The Todo model and GET /todos endpoint already exist and work correctly — do not modify them. Add POST /todos, PUT /todos/{todo_id}, and DELETE /todos/{todo_id} endpoints following the same style as the existing GET endpoint. Use separate Pydantic request schemas for input. Return 404 if todo_id doesn't exist. Do not touch any frontend files or database.py/models.py unless absolutely necessary.

**Result:** All 3 endpoints added cleanly. Tested via FastAPI /docs UI — create, update, delete all working correctly.
**Kept in repo at:** backend/main.py

---

### July 1 — Connect frontend to FastAPI backend

**Tool:** Claude Code
**Prompt:**

> In frontend/src/routes/Todos/Todos.tsx, update this file to connect to the FastAPI backend running at http://localhost:8000. Replace local state management with API calls for GET, POST, PUT, DELETE. Use fetch with async/await and wrap every call in try/catch. Show an error message if any call fails. Use useEffect to load todos on mount. Keep the same component structure and props — don't touch TodoForm.tsx or TodoList.tsx. Use arrow functions throughout. Do not touch any other files.

**Result:** Todos now persist to SQLite database via FastAPI. Error handling working. CORS middleware added to backend.
**Kept in repo at:** frontend/src/routes/Todos/Todos.tsx, backend/main.py

---

### July 1 — Update all import paths to use @ alias

**Tool:** Claude Code
**Prompt:**

> In the frontend/src folder, update all relative imports that use ../ or ./ paths to use the @ alias instead. Update ALL files in src/ including components, routes, and App.tsx. Do not touch any files outside of frontend/src. Do not change anything else — only the import paths.

**Result:** All 8 files updated to use @/ absolute imports. Vite and tsconfig both configured with the alias.
**Kept in repo at:** All files in frontend/src/

---

### July 2 — Add react-hook-form to TodoForm

**Tool:** Claude Code
**Prompt:**

> Replace the manual useState validation in TodoForm.tsx with react-hook-form. Keep the same UI and CSS. Add validation for: required field, no whitespace-only input, and pattern rule blocking special characters to prevent SQL injection. Show error messages below the input.

**Result:** TodoForm now uses react-hook-form with register, handleSubmit, reset, and formState.errors. Special characters like quotes and semicolons are blocked.
**Kept in repo at:** frontend/src/components/TodoForm/TodoForm.tsx

---

### 2026-07-06 — Create pytest unit tests for FastAPI backend

**Tool:** Claude Code
**Prompt:**

> Create a file backend/test_main.py with pytest unit tests for the FastAPI backend. Use TestClient from fastapi.testclient and an in-memory SQLite database for testing (not the real todos.db). Write tests for: GET /todos, POST /todos, PUT /todos/{id}, DELETE /todos/{id}, POST /users, GET /users, POST /todos with invalid owner_id.

**Result:** Created test_main.py with 15 tests covering all endpoints. Uses dependency injection override to swap in an in-memory SQLite DB; autouse fixture drops and recreates schema between each test for isolation.
**Kept in repo at:** backend/test_main.py

---

### 2026-07-06 — Add JWT authentication to FastAPI backend

**Tool:** Claude Code
**Prompt:**

> Add JWT authentication to the FastAPI backend using python-jose[cryptography] and passlib[bcrypt]. Add hashed_password to User model. Create auth.py with hash/verify, create_access_token (2d), create_refresh_token (5d), decode_token. Add POST /auth/signup, POST /auth/login, POST /auth/refresh endpoints and a get_current_user dependency. Protect GET /todos with the dependency.

**Result:** Created auth.py with passlib/jose helpers. Added hashed_password column to User model. Added 4 auth schemas, get_current_user dependency, and 3 auth endpoints to main.py. GET /todos now requires a valid Bearer token.
**Kept in repo at:** backend/auth.py, backend/models.py, backend/main.py

---

### 2026-07-07 — Add User update/delete endpoints and fix password hashing

**Tool:** Claude Code
**Prompt:**

> Add PUT /users/{user_id} and DELETE /users/{user_id} endpoints to main.py with proper duplicate email and username validation that excludes the current user being updated. Also fix the bcrypt password hashing by replacing passlib with direct bcrypt library and pre-hashing passwords with SHA-256 to avoid the 72-byte truncation issue.

**Result:** Added update_user and delete_user endpoints with duplicate validation. Fixed password hashing using bcrypt directly with SHA-256 pre-hashing. Full User CRUD now complete.
**Kept in repo at:** backend/main.py, backend/auth.py

### 2026-07-08 — Create AuthContext with login/logout and wrap app in AuthProvider

**Tool:** Claude Code
**Prompt:**

> Create a new file at src/contexts/AuthContext/AuthContext.tsx. It should export an AuthProvider component and a useAuth hook. The context should hold: accessToken (string | null, stored in React state — NOT localStorage), a login(accessToken, refreshToken) function that sets the access token in state and saves the refresh token to localStorage, and a logout() function that clears the access token from state and removes the refresh token from localStorage. Use TypeScript, arrow functions, and follow the existing absolute import convention (@/ alias) if applicable. Wrap the app with AuthProvider in main.tsx.

**Result:** Created AuthContext.tsx with AuthProvider and useAuth hook. accessToken held in useState, refresh token persisted to localStorage under key "refreshToken". useAuth throws if called outside provider. Wrapped <App /> and <ToastContainer /> in <AuthProvider> in main.tsx.
**Kept in repo at:** frontend/src/contexts/AuthContext/AuthContext.tsx, frontend/src/main.tsx

---

### 2026-07-08 — Return tokens from /auth/signup alongside user data

**Tool:** Claude Code
**Prompt:**

> In backend/main.py, update the /auth/signup endpoint so that after creating the user, it also generates an access token and refresh token. Change the response to include the user data plus access_token and refresh_token. Update the UserResponse model or create a new response model if needed to include these fields.

**Result:** Added SignupResponse model (extends UserResponse with access_token, refresh_token, token_type). Updated /auth/signup to return a SignupResponse instance with both tokens generated via the existing create_access_token/create_refresh_token functions.
**Kept in repo at:** backend/main.py

---

### 2026-07-08 — Create SignUp page with react-hook-form and auth integration

**Tool:** Claude Code
**Prompt:**

> Create a new file at src/routes/SignUp/SignUp.tsx. Build a Sign Up page using react-hook-form with username (min 3), email (valid format), and password (min 8) fields. On submit POST to ${BASE_URL}/auth/signup, call login() from useAuth on success, show success toast and navigate to /todos. On failure show error toast with backend detail. Add /signup route to App.tsx.

**Result:** Created SignUp.tsx with react-hook-form validation, fetch call to /auth/signup, useAuth login(), react-toastify toasts, and useNavigate redirect. Button disabled during submission. Added SignUp import and /signup Route to App.tsx.
**Kept in repo at:** frontend/src/routes/SignUp/SignUp.tsx, frontend/src/App.tsx

---

### 2026-07-08 — Style SignUp.tsx with Tailwind CSS matching TodoForm visual style

**Tool:** Claude Code
**Prompt:**

> Style SignUp.tsx using Tailwind CSS classes to match the visual style of the existing TodoForm component — proper spacing between fields, a styled input box (border, padding, focus ring), a styled submit button matching the app's primary button style, and a clean centered card/container layout for the whole form.

**Result:** Added Tailwind classes to SignUp.tsx for a centered card layout (white card, shadow, max-w-[360px]), inputs with border/padding/focus ring matching TodoForm.css exact colours (#2a9d8f teal), error messages matching .form-error style, and a submit button matching the "Add" button. No new CSS files created.
**Kept in repo at:** frontend/src/routes/SignUp/SignUp.tsx

---

### 2026-07-08 — Fix SignUp page centering and spacing to match app layout pattern

**Tool:** Claude Code
**Prompt:**

> The SignUp page isn't properly centered — it should be horizontally centered on the page, and the layout should fit within the viewport without requiring scrolling. Match how centering/spacing is handled elsewhere in the app.

**Result:** Removed full-viewport centering wrapper (min-h-screen flex) and card div — Layout's .app-shell (max-width: 600px; margin: 0 auto) already handles centering for all routes. Reduced vertical spacing (gap-3, py-2.5) and restored plain <section>/<h1> to match other route pages.
**Kept in repo at:** frontend/src/routes/SignUp/SignUp.tsx

---

### 2026-07-08 — Create SignIn page and add cross-links between SignIn/SignUp

**Tool:** Claude Code
**Prompt:**

> Create src/routes/SignIn/SignIn.tsx matching SignUp.tsx structure and Tailwind styling. Fields: email (required, valid format) and password (required). POST to /auth/login, call login() on success, toast and navigate to /todos. On failure show error toast. Add /signin route to App.tsx. Add cross-links: SignUp -> /signin and SignIn -> /signup.

**Result:** Created SignIn.tsx with email+password fields, fetch to /auth/login, useAuth login(), toasts, and navigate. Added Link import and "Don't have an account?" link to SignIn. Added Link import and "Already have an account?" link to SignUp. Added SignIn import and /signin Route to App.tsx.
**Kept in repo at:** frontend/src/routes/SignIn/SignIn.tsx, frontend/src/routes/SignUp/SignUp.tsx, frontend/src/App.tsx

---

### 2026-07-08 — Add Authorization header to Todos fetch calls and guard TodoList against non-array todos

**Tool:** Claude Code
**Prompt:**

> Update Todos.tsx to include the access token from useAuth() in the Authorization: Bearer header for all requests to /todos. Update TodoList.tsx to safely handle the case where todos is not yet an array (default to empty array) so a failed or pending request doesn't crash the page.

**Result:** Added useAuth() to Todos.tsx, built an authHeaders() helper that injects the Bearer token, applied it to all four fetch calls, and added accessToken to the useEffect dependency array so todos re-fetch on login. Defaulted todos prop to [] in TodoList.tsx destructuring.
**Kept in repo at:** frontend/src/routes/Todos/Todos.tsx, frontend/src/components/TodoList/TodoList.tsx

---

### 2026-07-08 — Guard fetchTodos against non-ok responses in Todos.tsx

**Tool:** Claude Code
**Prompt:**

> In Todos.tsx, update fetchTodos inside useEffect to check res.ok before calling setTodos. If not ok (e.g. 401), don't call setTodos with the error object — show a toast error and redirect to /signin.

**Result:** Added res.ok check in fetchTodos. 401 shows "Session expired" toast and navigates to /signin. Other non-ok statuses show a generic error toast. setTodos is only called on a successful response. Added useNavigate import.
**Kept in repo at:** frontend/src/routes/Todos/Todos.tsx

---

### 2026-07-08 — Add session restore via refresh token on app load in AuthContext

**Tool:** Claude Code
**Prompt:**

> In AuthContext.tsx, add logic that runs once on app load: check localStorage for a refresh token, call POST /auth/refresh if found, set the returned access token in state. If refresh fails, clear localStorage. Expose isLoading boolean so components like Todos can wait before treating the user as unauthenticated.

**Result:** Added isLoading state (starts true) and a restore useEffect in AuthProvider. Calls /auth/refresh with stored token; sets accessToken on success, clears localStorage on failure. Sets isLoading=false in finally block. Updated Todos.tsx to skip fetchTodos and render a loading state while isLoading is true, then proceed normally.
**Kept in repo at:** frontend/src/contexts/AuthContext/AuthContext.tsx, frontend/src/routes/Todos/Todos.tsx

---

### 2026-07-08 — Update test_main.py for JWT-protected /todos and add auth tests

**Tool:** Claude Code
**Prompt:**

> Update backend/test_main.py to fix failing tests now that GET /todos requires JWT. Add auth_token and auth_headers fixtures. Update all /todos tests to include the Bearer token. Add 5+ new tests covering signup success, duplicate signup, login success, wrong password, and accessing /todos without a token (401).

**Result:** Added auth_token fixture (signs up via /auth/signup, returns access token) and auth_headers fixture. Updated all 10 /todos tests to pass headers. Migrated test_create_user and test_get_users_returns_created_user to use /auth/signup instead of /users (which now requires hashed_password). Added 6 new tests: signup success, duplicate email, duplicate username, login success, wrong password, unknown email, and 401 on unauthenticated GET /todos.
**Kept in repo at:** backend/test_main.py

---

### 2026-07-08 — Enforce ownership on PUT/DELETE /todos and add 403 tests

**Tool:** Claude Code
**Prompt:**

> Update PUT /todos/{id} and DELETE /todos/{id} in main.py to check that the todo's owner_id matches the authenticated user's id, returning 403 if not. Update test_main.py to add tests confirming a user cannot update or delete another user's todo.

**Result:** Added get_current_user dependency to both PUT and DELETE /todos endpoints with a 403 check on owner_id mismatch. Refactored auth_user fixture to return full signup response (including user id). Updated all PUT/DELETE todo tests to create todos with owner_id=auth_user["id"]. Added other_auth_headers fixture for a second user. Added test_update_todo_forbidden and test_delete_todo_forbidden (both expect 403).
**Kept in repo at:** backend/main.py, backend/test_main.py

---

### 2026-07-08 — Add auth-aware nav links and Log Out button to Layout

**Tool:** Claude Code
**Prompt:**

> Update the Layout navigation to add Sign Up and Sign In links. If the user is logged in (accessToken exists via useAuth), hide Sign Up/Sign In and show a Log Out button that calls logout() and navigates to /signin.

**Result:** Updated Layout.tsx to use useAuth() and useNavigate(). Renders Sign Up + Sign In links when logged out, and a Log Out button when logged in. Added .nav-logout CSS class to Layout.css so the button matches nav link styling exactly.
**Kept in repo at:** frontend/src/components/Layout/Layout.tsx, frontend/src/components/Layout/Layout.css

---

### 2026-07-08 — Require auth on POST /todos, auto-set owner_id, guard toggleTodo/deleteTodo

**Tool:** Claude Code
**Prompt:**

> Update POST /todos to require authentication via get_current_user and automatically set owner_id to current_user.id, ignoring any owner_id from the client. Remove owner_id from TodoCreate. In Todos.tsx, update toggleTodo and deleteTodo to check res.ok before updating state — on failure show error toast with backend message and don't modify state.

**Result:** Removed owner_id from TodoCreate schema. Added get_current_user dependency to POST /todos; owner_id now always set to current_user.id. Added res.ok checks to toggleTodo and deleteTodo in Todos.tsx with json.detail error toasts. Updated test_main.py: removed owner_id from all POST /todos calls, removed test_create_todo_invalid_owner_id, added test_create_todo_sets_owner, cleaned up auth_user fixture usage.
**Kept in repo at:** backend/main.py, frontend/src/routes/Todos/Todos.tsx, backend/test_main.py

---

### 2026-07-08 — Add test_full_user_journey integration test

**Tool:** Claude Code
**Prompt:**

> Add one integration test called test_full_user_journey that covers the complete happy path: sign up, create a todo, fetch and confirm it appears, mark it completed and confirm the response, delete it and confirm it no longer appears. Add clear comments marking each step.

**Result:** Added test_full_user_journey to test_main.py under a new "# --- Integration ---" section. Five clearly commented steps covering signup → create → list → update → delete, each with targeted assertions.
**Kept in repo at:** backend/test_main.py

---

### 2026-07-08 — Filter GET /todos by authenticated user and add isolation test

**Tool:** Claude Code
**Prompt:**

> Update GET /todos to only return todos belonging to the currently authenticated user (filter by owner_id == current_user.id). Add a test confirming a user only sees their own todos, not another user's.

**Result:** Added .filter(models.Todo.owner_id == current_user.id) to the GET /todos query. Added test_user_only_sees_own_todos: both users create a todo, each list call returns exactly one item belonging only to that user.
**Kept in repo at:** backend/main.py, backend/test_main.py

---

### 2026-07-23 — Create Week 4 research agent with skill, memory, hook, plugin, and agentic loop

**Tool:** Claude Code
**Prompt:**

> Create backend/agent.py: a research agent using raw requests to the Anthropic API (claude-sonnet-5). Add web_search skill (Tavily), read_file plugin (txt/pdf via pypdf), log_tool_call hook decorator, in-memory session_memory list, and a text-based agentic loop. Demo with a multi-hop question requiring web search + memory recall.

**Result:** Created agent.py with all five pieces. Installed pypdf and python-dotenv. Fixed Windows cp1252 encoding by reconfiguring stdout to UTF-8. Agent ran successfully: 2 web_search tool calls + hook logs + memory injection + final answer.
**Kept in repo at:** backend/agent.py

---

### 2026-07-24 — Create MCP server exposing todos resource and create_todo tool

**Tool:** Claude Code
**Prompt:**

> Create backend/mcp_server.py: an MCP server using the mcp Python package. Expose ONE resource (todos://all returning all todos as JSON) and ONE tool (create_todo(title)). Use stdio transport. Add clear comments explaining resource vs tool in MCP terms and how to connect it via .mcp.json. Also create .mcp.json at the repo root.

**Result:** Installed mcp[cli]. Created mcp_server.py using FastMCP high-level API with @mcp.resource and @mcp.tool decorators, reusing existing models.py and database.py. Created .mcp.json at repo root pointing to backend/mcp_server.py. Verified server starts and responds to MCP initialize correctly.
**Kept in repo at:** backend/mcp_server.py, .mcp.json

---

### 2026-07-24 — Create multi-agent orchestrator with supervisor + worker pattern

**Tool:** Claude Code
**Prompt:**

> Create backend/orchestrator.py implementing a supervisor + worker multi-agent pattern, building on agent.py. Requirements: (1) A supervisor agent that routes user requests to the right worker. (2) At least 2 workers: research_worker (web_search via Tavily) and todo_worker (db_create_todo + db_list_todos via SQLAlchemy directly). (3) A tracing layer that logs every tool call across the whole agent graph with timestamp and agent name. (4) A demo sending 2 requests (one routed to research_worker, one to todo_worker) and printing the full trace. (5) Clear comments explaining supervisor/worker vs single agent in agent.py.

**Result:** Created orchestrator.py with: shared TRACE list + trace()/print_trace() helpers; make_tool_hook(agent_name) factory (extends agent.py's @log_tool_call with agent attribution); call_claude() and parse_tool_call() reused from agent.py; generic run_worker_loop() used by both workers; research_worker with web_search; todo_worker with db_create_todo + db_list_todos; supervisor_route() calling Claude with a routing-only system prompt; orchestrate() entry point that clears trace, calls supervisor, delegates to worker, prints trace.
**Kept in repo at:** backend/orchestrator.py

---

### 2026-07-24 — Add POST /agent/ask endpoint to main.py

**Tool:** Claude Code
**Prompt:**

> Add a new endpoint POST /agent/ask to backend/main.py that accepts a JSON body {"question": "..."}, calls the existing run_agent function from agent.py (import it), and returns the agent's final answer as JSON {"answer": "..."}. No authentication needed. Make sure agent.py is structured so run_agent can be imported (refactor if needed).

**Result:** Imported run_agent from agent.py in main.py (no refactor needed — run_agent was already a proper function with demo under if __name__ == "__main__"). Added AgentRequest and AgentResponse Pydantic models and POST /agent/ask route at the bottom of main.py.
**Kept in repo at:** backend/main.py

---


### 2026-07-24 — Create Agent page with question/answer UI

**Tool:** Claude Code
**Prompt:**

> Create src/routes/Agent/Agent.tsx: a page with a textarea for the user's question, a submit button, and an answer display area. On submit, POST to ${BASE_URL}/agent/ask with { question }. Show loading state (button disabled, "Thinking..."). Display returned answer in a styled box. Error toast on failure. Add /agent route to App.tsx and an "Agent" nav link in Layout.tsx.

**Result:** Created Agent.tsx using local useState (no react-hook-form needed — single unvalidated textarea). Textarea disables during loading. Answer renders in a teal-bordered box with whitespace-pre-wrap. Added Agent import and /agent route to App.tsx. Added Agent link to Layout.tsx nav alongside existing links.
**Kept in repo at:** frontend/src/routes/Agent/Agent.tsx, frontend/src/App.tsx, frontend/src/components/Layout/Layout.tsx

---

### 2026-07-24 — Add POST /orchestrator/ask endpoint

**Tool:** Claude Code
**Prompt:**

> Add POST /orchestrator/ask to backend/main.py that accepts {"question": "..."}, calls orchestrate() from orchestrator.py, and returns {"answer": "...", "trace": [...]}. Refactor orchestrate() to return both values instead of only the answer string.

**Result:** Changed orchestrate() return type from str to dict {"answer": str, "trace": list[dict]}. Updated demo call sites to unpack the dict. Added OrchestratorTraceEntry and OrchestratorResponse Pydantic models to main.py. Added POST /orchestrator/ask route reusing AgentRequest. Imported orchestrate in main.py.
**Kept in repo at:** backend/orchestrator.py, backend/main.py

---

### 2026-07-24 — Update Agent page to call /orchestrator/ask and show trace

**Tool:** Claude Code
**Prompt:**

> Update Agent.tsx to call POST /orchestrator/ask instead of /agent/ask. Keep the same textarea/submit/loading pattern. After receiving the response, display the answer as before, and show the trace array in a collapsible section ("Show agent trace") with each entry's timestamp, agent name, and event.

**Result:** Added TraceEntry interface and AGENT_COLORS map (supervisor=orange, research_worker=teal, todo_worker=blue). Added trace and traceOpen state. Fetch now hits /orchestrator/ask and stores json.trace. Collapsible trace panel renders as a monospace list with timestamp, coloured agent name, and event text. Panel resets on each new submission.
**Kept in repo at:** frontend/src/routes/Agent/Agent.tsx

---

### 2026-07-24 — Add auth to /orchestrator/ask and thread owner_id to db_create_todo

**Tool:** Claude Code
**Prompt:**

> Update POST /orchestrator/ask in main.py to require authentication via Depends(get_current_user) and pass current_user.id through to orchestrate(). Update orchestrate() to accept owner_id and pass it to todo_worker. Update db_create_todo to accept and use owner_id instead of leaving it null. Update Agent.tsx to include Authorization header using useAuth(), show a sign-in prompt for unauthenticated users, and redirect to /signin on 401.

**Result:** Added owner_id: int | None = None param to db_create_todo, todo_worker, and orchestrate(). todo_worker now builds its tools dict locally using functools.partial to bind owner_id to db_create_todo, keeping the tool loop's single-string-arg contract intact. Removed now-unused TODO_TOOLS module-level dict and WORKERS dict. orchestrate() dispatches with explicit if/else instead of WORKERS lookup so owner_id can be forwarded selectively. main.py endpoint gains Depends(get_current_user) and passes current_user.id. Agent.tsx imports useAuth and useNavigate; shows loading placeholder during auth restore; shows sign-in prompt when not logged in; includes Authorization header on fetch; redirects to /signin on 401.
**Kept in repo at:** backend/orchestrator.py, backend/main.py, frontend/src/routes/Agent/Agent.tsx

---

### 2026-07-24 — Filter db_list_todos by owner_id in orchestrator.py

**Tool:** Claude Code
**Prompt:**

> db_list_todos in orchestrator.py returns ALL todos regardless of owner. Fix it to accept and filter by owner_id (.filter(models.Todo.owner_id == owner_id)), and bind it with functools.partial in todo_worker's tools dict — same pattern as db_create_todo.

**Result:** Added owner_id param to db_list_todos; query now filters by owner_id when provided (no filter only if owner_id is None, matching the guard pattern used elsewhere). Updated todo_worker's tools dict to bind db_list_todos with partial(db_list_todos, owner_id=owner_id). Confirmed db_create_todo was already correct from the previous fix.
**Kept in repo at:** backend/orchestrator.py

---
