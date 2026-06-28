
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
**Kept in repo at:** frontend/src/components/Todo*.tsx, frontend/src/routes/Todos.tsx

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