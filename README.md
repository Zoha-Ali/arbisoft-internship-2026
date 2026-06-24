# Arbisoft AI-Focused Internship 2026 — Web Track

Working repo for the 8-week Arbisoft internship (Fundamentals → Agentic AI → Build).

## Structure

```
.
├── frontend/        # Week 1 SPA, grows through Week 3 (connects to backend)
├── backend/         # Added in Week 2 — CRUD API + ORM
├── prompts.md       # Required AI-interaction log (program ground rule)
└── README.md
```

> Phase 3 (the self-proposed agentic AI project) will live in its own repo once the proposal
> is approved at the mid-Week-5 gate — this repo is for Phase 1 + Phase 2 fundamentals only.

## Week 1 Status: ✅ Complete

**Deployed site:** https://teal-puppy-ec56f0.netlify.app

A React + TypeScript SPA with:
- 3 routes (Home, About, Todos) with shared layout
- Todo app: add tasks, check them off, delete them
- Form validation with error messages
- 8 passing unit tests (Vitest + React Testing Library)
- Styled UI: cards, buttons, animations, hover states
- ESLint + Prettier (clean pass)
- All prompts logged in `prompts.md`

## Setup

```bash
cd frontend
npm install
npm run dev      # Vite dev server at http://localhost:5173
npm run test     # Vitest + React Testing Library
npm run lint     # ESLint
npm run format   # Prettier
```

## Ground Rules

- Every significant AI prompt goes in `prompts.md`.
- Commit AI-generated code with a clean lint pass.
- All tests passing before pushing.

## Next: Week 2

Backend integration with CRUD API, ORM models, JWT auth, and E2E testing.