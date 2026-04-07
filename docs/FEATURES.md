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
| `/sk:deep-interview` | Socratic requirements-gathering with ambiguity scoring; auto-run for vague tasks | [sk-deep-interview.md](sk:features/sk-deep-interview.md) |
| `/sk:investigate` | Read-only feature-area exploration before brainstorm (Step 0.5) | [sk-investigate.md](sk:features/sk-investigate.md) |
| `/sk:brainstorm` | Explore requirements and design before implementation | — |
| `/sk:frontend-design` | UI mockup + optional Pencil visual design | — |
| `/sk:api-design` | Design API contracts (endpoints, payloads, auth, errors) | — |
| `/sk:accessibility` | WCAG 2.1 AA audit on design spec | — |
| `/sk:write-plan` | Write decision-complete plan into `tasks/todo.md` | — |
| `/sk:branch` | Create feature branch auto-named from current task | — |
| `/sk:schema-migrate` | Database schema change analysis (multi-ORM) | — |
| `/sk:write-tests` | TDD: write failing tests before implementation | — |
| `/sk:execute-plan` | Execute `tasks/todo.md` checkboxes in batches | — |
| `/sk:reverse-doc` | Generate architecture/design/API docs from existing code | [sk-reverse-doc.md](sk:features/sk-reverse-doc.md) |

### Quality Gates

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:deps-audit` | CVE scan, license compliance, outdated packages (npm, Composer, Cargo, pip, Go, Bundler) | — |
| `/sk:lint` | Auto-detect + run all linters | — |
| `/sk:test` | Auto-detect + run all test suites; 100% coverage gate | — |
| `/sk:security-check` | OWASP security audit on changed files | — |
| `/sk:perf` | Performance audit (bundle, N+1, Core Web Vitals, memory) | — |
| `/sk:seo-audit` | Dual-mode SEO audit (source + dev server), ask-before-fix | — |
| `/sk:review` | Multi-dimensional self-review with simplify pre-pass | — |
| `/sk:respond-review` | Triage `/sk:review` findings into fix-now / defer / dispute (auto-invoked by gates Batch 3) | [sk-respond-review.md](sk:features/sk-respond-review.md) |
| `/sk:e2e` | E2E behavioral verification (final quality gate) | — |
| `/sk:scope-check` | Compare implementation against plan to detect scope creep | [sk-scope-check.md](sk:features/sk-scope-check.md) |
| `/sk:gates` | Run all quality gates in optimized parallel batches | [sk-gates.md](sk:features/sk-gates.md) |

### Completion

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:smart-commit` | Conventional commit with approval workflow | — |
| `/sk:update-task` | Mark task done; log completion to `tasks/progress.md` | — |
| `/sk:finish-feature` | Changelog + arch log + PR creation | — |
| `/sk:features` | Sync feature specs with shipped implementation | — |
| `/sk:release` | Version bump + changelog + git tag | — |
| `/sk:retro` | Post-ship retrospective with metrics and action items | [sk-retro.md](sk:features/sk-retro.md) |

### Developer Tools

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:dashboard` | Live Kanban board — workflow status across all worktrees | [sk-dashboard.md](sk:features/sk-dashboard.md) |
| `/sk:context` | Session initializer — load context files + output SESSION BRIEF | [sk-context.md](sk:features/sk-context.md) |
| `/sk:deep-dive` | Trace + interview pipeline for unknown-cause bugs | [sk-deep-dive.md](sk:features/sk-deep-dive.md) |
| `/sk:debug` | Structured bug investigation (known cause): reproduce → isolate → fix | — |
| `/sk:hotfix` | Emergency fix workflow (skip TDD, enforce quality gates) | — |
| `/sk:change` | Handle mid-workflow requirement change; re-enter at correct step | — |
| `/sk:status` | Show workflow + task status at a glance | — |
| `/sk:fast-track` | Abbreviated workflow for small changes; skips ceremony, keeps gates | [sk-fast-track.md](sk:features/sk-fast-track.md) |
| `/sk:start` | Smart entry point — classifies task, routes to optimal flow/mode/agents | [sk-start.md](sk:features/sk-start.md) |
| `/sk:autopilot` | Hands-free workflow — all 8 steps, auto-skip, auto-advance, auto-commit | [sk-autopilot.md](sk:features/sk-autopilot.md) |
| `/sk:team` | Parallel domain agents (backend + frontend + QA) for full-stack tasks | [sk-team.md](sk:features/sk-team.md) |
| `/sk:steal` | Review external source (GitHub, article, screenshot) and adapt ideas | [sk-steal.md](sk:features/sk-steal.md) |
| `/sk:explain` | Explain code with visual diagrams and mental models | [sk-explain.md](sk:features/sk-explain.md) |

### Workflow Enhancements

| Feature | Purpose | Spec |
|---------|---------|------|
| Auto-Skip Intelligence | Auto-detect and skip optional steps when not needed | [sk-auto-skip.md](sk:features/sk-auto-skip.md) |

### Setup & Configuration

| Command | Purpose | Spec |
|---------|---------|------|
| `/sk:setup-claude` | Bootstrap Claude Code project scaffolding | — |
| `/sk:setup-optimizer` | Diagnose + update workflow + enrich CLAUDE.md | — |
| `/sk:skill-creator` | Create or modify skills; run evals; anti-pattern + auto-clarity guidance | [sk-skill-creator.md](sk:features/sk-skill-creator.md) |
| `/sk:eval` | Define, run, report evals, and benchmark skill token/quality impact | [sk-eval.md](sk:features/sk-eval.md) |
| `/sk:laravel-init` | Configure existing Laravel project with opinionated conventions | — |
| `/sk:laravel-new` | Scaffold fresh Laravel app | — |
| `/sk:mvp` | Generate complete MVP validation app from a prompt | — |
| `/sk:config` / `/sk:set-profile` | View/edit ShipKit project config (`.shipkit/config.json`) | — |

---

## Spec Status

| Spec | Last Updated | Version |
|------|-------------|---------|
| [sk-dashboard.md](sk:features/sk-dashboard.md) | 2026-03-19 | v3.5.0 |
| [sk-context.md](sk:features/sk-context.md) | 2026-04-02 | v3.24.0 |
| [sk-scope-check.md](sk:features/sk-scope-check.md) | 2026-03-23 | v3.7.0 |
| [sk-retro.md](sk:features/sk-retro.md) | 2026-03-23 | v3.7.0 |
| [sk-reverse-doc.md](sk:features/sk-reverse-doc.md) | 2026-03-23 | v3.7.0 |
| [sk-gates.md](sk:features/sk-gates.md) | 2026-04-06 | v3.27.0 |
| [sk-fast-track.md](sk:features/sk-fast-track.md) | 2026-03-23 | v3.7.0 |
| [sk-auto-skip.md](sk:features/sk-auto-skip.md) | 2026-03-24 | v3.10.0 |
| [sk-autopilot.md](sk:features/sk-autopilot.md) | 2026-04-06 | v3.27.0 |
| [sk-team.md](sk:features/sk-team.md) | 2026-03-24 | v3.10.0 |
| [sk-start.md](sk:features/sk-start.md) | 2026-04-06 | v3.27.0 |
| [sk-deps-audit.md](sk:features/sk-deps-audit.md) | 2026-03-31 | v3.22.0 |
| [sk-deep-interview.md](sk:features/sk-deep-interview.md) | 2026-04-01 | v3.23.0 |
| [sk-deep-dive.md](sk:features/sk-deep-dive.md) | 2026-04-01 | v3.23.0 |
| [sk-skill-creator.md](sk:features/sk-skill-creator.md) | 2026-04-06 | v3.27.0 |
| [sk-eval.md](sk:features/sk-eval.md) | 2026-04-06 | v3.27.0 |
| [sk-steal.md](sk:features/sk-steal.md) | 2026-04-06 | v3.27.1 |
| [sk-investigate.md](sk:features/sk-investigate.md) | 2026-04-07 | v3.28.0 |
| [sk-respond-review.md](sk:features/sk-respond-review.md) | 2026-04-07 | v3.28.0 |
