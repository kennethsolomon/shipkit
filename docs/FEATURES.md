# ShipKit Feature Specifications

Platform-agnostic feature specifications for ShipKit skills and commands.

## How to Use

Each spec in `docs/sk:features/` documents a skill or command: what it reads, what it produces, its business logic, hard rules, edge cases, and UI behavior. Specs are the source of truth for understanding *how* a skill works — the SKILL.md files are the *implementation* contract.

Update specs after shipping changes: `/sk:features` auto-detects what changed.

---

## Skills by Domain

### Planning & Exploration

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:brainstorm` | Explore requirements and design before implementation | — |
| `/sk:frontend-design` | UI mockup + optional Pencil visual design | — |
| `/sk:api-design` | Design API contracts (endpoints, payloads, auth, errors) | — |
| `/sk:accessibility` | WCAG 2.1 AA audit on design spec | — |
| `/sk:write-plan` | Write decision-complete plan into `tasks/todo.md` | — |
| `/sk:branch` | Create feature branch auto-named from current task | — |
| `/sk:schema-migrate` | Database schema change analysis (multi-ORM) | — |
| `/sk:write-tests` | TDD: write failing tests before implementation | — |
| `/sk:execute-plan` | Execute `tasks/todo.md` checkboxes in batches | — |

### Quality Gates

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:lint` | Auto-detect + run all linters; dependency vulnerability audit | — |
| `/sk:test` | Auto-detect + run all test suites; 100% coverage gate | — |
| `/sk:security-check` | OWASP security audit on changed files | — |
| `/sk:perf` | Performance audit (bundle, N+1, Core Web Vitals, memory) | — |
| `/sk:seo-audit` | Dual-mode SEO audit (source + dev server), ask-before-fix | — |
| `/sk:review` | Multi-dimensional self-review with simplify pre-pass | — |
| `/sk:e2e` | E2E behavioral verification (final quality gate) | — |

### Completion

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:smart-commit` | Conventional commit with approval workflow | — |
| `/sk:update-task` | Mark task done; log completion to `tasks/progress.md` | — |
| `/sk:finish-feature` | Changelog + arch log + PR creation | — |
| `/sk:features` | Sync feature specs with shipped implementation | — |
| `/sk:release` | Version bump + changelog + git tag | — |

### Developer Tools

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:dashboard` | Live Kanban board — workflow status across all worktrees | [sk-dashboard.md](sk:features/sk-dashboard.md) |
| `/sk:debug` | Structured bug investigation: reproduce → isolate → fix | — |
| `/sk:hotfix` | Emergency fix workflow (skip TDD, enforce quality gates) | — |
| `/sk:change` | Handle mid-workflow requirement change; re-enter at correct step | — |
| `/sk:status` | Show workflow + task status at a glance | — |

### Setup & Configuration

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:setup-claude` | Bootstrap Claude Code project scaffolding | — |
| `/sk:setup-optimizer` | Diagnose + update workflow + enrich CLAUDE.md | — |
| `/sk:skill-creator` | Create or modify skills; run evals | — |
| `/sk:laravel-init` | Configure existing Laravel project with opinionated conventions | — |
| `/sk:laravel-new` | Scaffold fresh Laravel app | — |
| `/sk:mvp` | Generate complete MVP validation app from a prompt | — |
| `/sk:config` / `/sk:set-profile` | View/edit ShipKit project config (`.shipkit/config.json`) | — |

---

## Spec Status

| Spec | Last Updated | Version |
|------|-------------|---------|
| [sk-dashboard.md](sk:features/sk-dashboard.md) | 2026-03-19 | v3.5.0 |
