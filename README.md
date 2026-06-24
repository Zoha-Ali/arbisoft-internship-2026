# Arbisoft AI-Focused Internship 2026 — Web Track

Working repo for the 8-week Arbisoft internship (Fundamentals → Agentic AI → Build).

## Structure

```
.
├── frontend/        # Week 1 SPA, grows through Week 3 (connects to backend)
├── backend/         # Added in Week 2 — CRUD API + ORM
├── prompts.md       # Required AI-interaction log (program ground rule)
├── CHECKLIST.md      # Every ✅ deliverable from the roadmap, trackable
└── README.md
```

> Phase 3 (the self-proposed agentic AI project) will live in its own repo once the proposal
> is approved at the mid-Week-5 gate — this repo is for Phase 1 + Phase 2 fundamentals only.

## Setup (Week 1)

```bash
cd frontend
npm install
npm run dev      # Vite dev server
npm run test     # Vitest + React Testing Library
npm run lint      # ESLint
npm run format   # Prettier
```

## Ground rules baked into this repo

- Every significant AI prompt goes in `prompts.md` (template + example entry inside).
- `CHECKLIST.md` mirrors every ✅ from the program doc — tick items off as you go.
- Commit AI-generated diffs with a clean lint pass (`frontend/eslint.config.js` + `.prettierrc`).
