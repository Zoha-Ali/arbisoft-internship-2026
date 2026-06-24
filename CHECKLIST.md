# Program Checklist

Tracks every ✅ deliverable from the roadmap. Tick off as you complete them, and update
`prompts.md` alongside.

## Phase 1 — Fundamentals (Web)

### Week 1 — Frontend Fundamentals
- [ ] Cursor/Claude Code set up + frontend framework chosen
- [ ] SPA with ≥3 routes and a shared layout
- [ ] ≥1 form with client-side validation
- [ ] ESLint + Prettier configured, clean lint pass committed
- [ ] 3+ unit tests (Jest/Vitest) for a component
- [ ] prompts.md updated

### Week 2 — Backend, REST, CRUD & ORM
- [ ] CRUD REST API for one resource
- [ ] ORM model with ≥1 relationship
- [ ] Input validation + correct HTTP status codes
- [ ] Backend linter configured, clean pass committed
- [ ] AI-generated unit tests reviewed and verified
- [ ] prompts.md updated

### Week 3 — Auth, Authorization, API Tests & Integration
- [ ] JWT auth added to Week 2 API
- [ ] ≥1 role-based authorization rule
- [ ] Frontend connected to backend (full E2E CRUD with login)
- [ ] ≥5 API tests (auth + CRUD + error paths)
- [ ] ≥1 integration test covering the happy path E2E
- [ ] prompts.md updated

## Phase 2 — Agentic AI

### Week 4 — Skills, Hooks, Memory & Plugins
- [ ] Research agent with a web-search skill
- [ ] Memory: agent recalls earlier session facts
- [ ] Hook logging every tool call with timestamps
- [ ] File-read plugin (.txt / .pdf)
- [ ] Demo: multi-hop question using all of the above
- [ ] prompts.md updated

### Week 5 (first half) — MCP, Multi-Agent Orchestration & Tool Design
- [ ] Custom MCP server (≥1 resource, ≥1 tool)
- [ ] MCP server connected to a client
- [ ] Supervisor + worker agent routing to ≥2 sub-agents
- [ ] Tracing layer logging tool calls across the agent graph
- [ ] **Phase 3 proposal submitted for mentor approval (gate)**

## Phase 3 — Self-Directed Build

### Week 5 (second half) — Scaffold & Architecture
- [ ] GitHub repo with scaffold (PR reviewed by mentor)
- [ ] README: architecture diagram, tech choices, model rationale
- [ ] prompts.md: scaffold-generation prompts logged
- [ ] Stubbed entrypoint(s) run E2E on mock data
- [ ] Async written check-in with mentor

### Week 6 — Core Feature Development
- [ ] End-to-end happy path working demo
- [ ] AI feature demo: agent completes ≥1 real task
- [ ] Test suite passing (≥70% coverage target on core logic)
- [ ] prompts.md updated
- [ ] 30-min live mentor demo + feedback

### Week 7 — Advanced AI Features & Polish
- [ ] Secondary AI feature added (RAG / summarization / NL search / planning)
- [ ] Multi-model routing live (≥2 providers)
- [ ] Output validation: schema guards, retries, fallback
- [ ] UX polish / clear CLI messaging
- [ ] OpenAPI spec or usage guide/runbook
- [ ] Draft presentation slides

### Week 8 — Finalization, Documentation & Final Presentation
- [ ] Code freeze (no new features after Day 3)
- [ ] Complete README (setup, architecture, AI feature docs)
- [ ] prompts.md finalized (all phases)
- [ ] Final presentation prepared (20 min + Q&A)
- [ ] 5-min demo video uploaded to Drive
- [ ] Reflection doc (what AI did well / where it failed / lessons)
