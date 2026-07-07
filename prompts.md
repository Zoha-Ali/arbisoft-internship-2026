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

### 2026-07-08 — Add User update/delete endpoints and fix password hashing

**Tool:** Claude Code
**Prompt:**

> Add PUT /users/{user_id} and DELETE /users/{user_id} endpoints to main.py with proper duplicate email and username validation that excludes the current user being updated. Also fix the bcrypt password hashing by replacing passlib with direct bcrypt library and pre-hashing passwords with SHA-256 to avoid the 72-byte truncation issue.

**Result:** Added update_user and delete_user endpoints with duplicate validation. Fixed password hashing using bcrypt directly with SHA-256 pre-hashing. Full User CRUD now complete.
**Kept in repo at:** backend/main.py, backend/auth.py
