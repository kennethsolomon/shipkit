<div align="center">

# SHIPKIT

**A structured, quality-gated workflow system for Claude Code.**

Ship features with TDD, security audits, and AI-powered code review —<br>
all wired into a single repeatable workflow.

[![npm](https://img.shields.io/npm/v/@kennethsolomon%2Fshipkit)](https://www.npmjs.com/package/@kennethsolomon/shipkit)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Mac%20%2F%20Linux%20%2F%20Windows-lightgrey)](#)

```bash
npm install -g @kennethsolomon/shipkit && shipkit
```

</div>

---

## What is ShipKit?

ShipKit turns Claude Code into a disciplined development partner. Instead of "write some code," every feature goes through:

**Plan** → **Build (TDD)** → **Quality Gates** → **Ship**

Each gate must pass before the next step. Lint fails? Fix it. Tests don't cover new code? Write them. Security issues? They block the PR. Quality is structural, not optional.

ShipKit auto-detects your stack — linters, test runners, frameworks, package managers. No configuration needed.

---

## Quick Start

```bash
# 1. Install
npm install -g @kennethsolomon/shipkit && shipkit

# 2. Bootstrap your project (run once)
/sk:setup-claude

# 3. Start building
/sk:start
```

That's it. `/sk:setup-claude` creates your project scaffolding: planning files, lifecycle hooks, path-scoped coding rules, and a persistent statusline — all auto-configured for your stack.

`/sk:start` is the recommended entry point — it classifies your task and routes you to the optimal flow automatically. You can also jump directly to `/sk:brainstorm`, `/sk:debug`, or any other flow entry point.

---

## Pick Your Flow

| I want to... | Run this | What happens |
|--------------|----------|-------------|
| **Not sure — let ShipKit decide** | `/sk:start` | Classifies your task, routes to optimal flow/mode/agents |
| **Build a new feature** | `/sk:brainstorm` | Full workflow: plan → TDD → quality gates → PR |
| **Build hands-free** | `/sk:autopilot` | All 8 steps, auto-skip, auto-advance, auto-commit |
| **Full-stack feature (parallel)** | `/sk:team` | Parallel domain agents (backend + frontend + QA) |
| **Make a small change** | `/sk:fast-track` | Skip planning, keep all quality gates |
| **Fix a bug** | `/sk:debug` | Investigate → regression test → fix → gates → PR |
| **Fix a production emergency** | `/sk:hotfix` | Skip TDD, but quality gates still enforced |
| **Handle a requirement change** | `/sk:change` | Assess scope, re-enter workflow at the right step |

---

## Workflows

### Feature Flow — full planning + TDD + all gates

> Start with: `/sk:brainstorm`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:brainstorm` | Explore requirements, propose approaches | Think |
| 2 | `/sk:frontend-design` or `/sk:api-design` | *Optional* — UI mockup or API contracts (includes accessibility) | Think |
| 3 | `/sk:write-plan` | Write decision-complete plan | Think |
| 4 | `/sk:branch` | Create feature branch | Build |
| 5 | `/sk:write-tests` + `/sk:execute-plan` | TDD: write failing tests, then implement | Build |
| 6 | `/sk:smart-commit` | Conventional commit | Build |
| 7 | `/sk:gates` | All 6 quality gates (parallel batches) | Verify |
| 8 | `/sk:finish-feature` | Update task, changelog, PR, feature sync, release | Ship |

---

### Fast-Track Flow — skip planning, keep all gates

> Start with: `/sk:fast-track`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:branch` | Create feature branch | Build |
| 2 | implement directly | No TDD — write code | Build |
| 3 | `/sk:smart-commit` | Conventional commit | Build |
| 4 | `/sk:gates` | All quality gates (parallel batches) | Verify |
| 5 | `/sk:finish-feature` | Changelog + PR | Ship |

Guard rails: warns if diff > 300 lines or > 5 new files.

---

### Bug Fix Flow — investigate first, then fix

> Start with: `/sk:debug`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:debug` | Reproduce, isolate, hypothesize, verify | Think |
| 2 | `/sk:branch` | Create fix branch | Build |
| 3 | `/sk:write-tests` | Regression test that reproduces the bug | Build |
| 4 | implement the fix | Make regression test pass | Build |
| 5 | `/sk:smart-commit` | Commit fix + test | Build |
| 6 | `/sk:gates` | All quality gates (parallel batches) | Verify |
| 7 | `/sk:finish-feature` | Changelog + PR | Ship |

---

### Hotfix Flow — production emergency

> Start with: `/sk:hotfix`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:debug` | Root-cause analysis | Think |
| 2 | `/sk:branch` | Create hotfix branch | Build |
| 3 | implement directly | Fix the issue | Build |
| 4 | `/sk:smart-commit` | Commit the fix | Build |
| 5 | `/sk:gates` | All quality gates (parallel batches) | Verify |
| 6 | `/sk:finish-feature` | Changelog + PR (marked as hotfix) | Ship |

After merging: add regression test + lesson to `tasks/lessons.md`.

---

### Requirement Change — mid-workflow pivot

> Run: `/sk:change` — it classifies scope and re-enters at the right step

| Tier | What changed | Example | Re-entry point |
|------|-------------|---------|----------------|
| **Tier 1** | Behavior tweak (same scope) | "Delete all" → "Delete users only" | `/sk:write-tests` |
| **Tier 2** | New requirements (new scope) | "Also add export to CSV" | `/sk:write-plan` |
| **Tier 3** | Scope shift (rethink) | "Different approach entirely" | `/sk:brainstorm` |

---

## Quality Gates (`/sk:gates`)

One command runs all 6 gates in parallel batches:

| Batch | Gates | Why this order |
|-------|-------|---------------|
| **1** (parallel) | lint + security + perf | Independent — run simultaneously |
| **2** | tests | Needs lint fixes first |
| **3** | code review | Needs deep understanding |
| **4** | E2E Tests | Needs review fixes |

Each gate auto-fixes and re-runs until clean. Fixes are squashed into one commit per gate pass. If a gate fails 3 times, it stops and asks for help.

Pre-existing issues are logged to `tasks/tech-debt.md` — not fixed inline.

---

## On-Demand Tools

Use these anytime — they're not part of any workflow.

| Command | When to use |
|---------|------------|
| `/sk:scope-check` | Mid-implementation — detect scope creep (On Track / Minor / Significant / Out of Control) |
| `/sk:retro` | After shipping — analyze velocity, blockers, patterns, generate action items |
| `/sk:reverse-doc` | Inherited codebase — generate architecture/design docs from existing code |
| `/sk:status` | Quick view of workflow and task status |
| `/sk:dashboard` | Visual Kanban board across all git worktrees |
| `/sk:mvp` | Generate a complete MVP app from a single idea prompt |
| `/sk:seo-audit` | SEO audit for web projects |
| `/sk:learn` | Extract reusable patterns from sessions into learned instincts |
| `/sk:context-budget` | Audit context window token consumption and find savings |
| `/sk:health` | Harness self-audit scorecard (7 categories, 0-70) |
| `/sk:save-session` | Save current session state for cross-session continuity |
| `/sk:resume-session` | Resume a previously saved session with full context |
| `/sk:safety-guard` | Protect against destructive ops (careful/freeze/guard modes) |
| `/sk:eval` | Define, run, and report on evaluations for agent reliability |

---

## Stack Support

| Area | Supported |
|------|-----------|
| **Frameworks** | Laravel, Next.js, Nuxt, React, Vue, Node.js |
| **Linters** | Pint, ESLint, PHPStan, Rector, Prettier, Biome |
| **Test runners** | Pest, PHPUnit, Jest, Vitest, Playwright |
| **Schema / ORM** | Prisma, Drizzle, Eloquent, SQLAlchemy, ActiveRecord |
| **Release** | npm, Composer, iOS (App Store), Android (Play Store) |

---

## All Commands

<details>
<summary><strong>45 commands</strong> — click to expand</summary>

| Command | Purpose |
|---------|---------|
| `/sk:accessibility` | WCAG 2.1 AA audit |
| `/sk:api-design` | Design API contracts before implementation |
| `/sk:autopilot` | Hands-free workflow — auto-skip, auto-advance, auto-commit |
| `/sk:brainstorm` | Explore requirements and design |
| `/sk:branch` | Create feature branch from current task |
| `/sk:change` | Handle mid-workflow requirement changes |
| `/sk:config` | View/edit project config |
| `/sk:context` | Load project context (automatic via hooks) |
| `/sk:context-budget` | Audit context window token consumption |
| `/sk:dashboard` | Live Kanban board — sk:dashboard across worktrees |
| `/sk:debug` | Structured bug investigation |
| `/sk:e2e` | E2E Tests — behavioral verification |
| `/sk:eval` | Define, run, and report evals for agent reliability |
| `/sk:execute-plan` | Execute plan checkboxes in batches |
| `/sk:fast-track` | Small changes — skip planning, keep gates |
| `/sk:features` | Sync feature specs with codebase |
| `/sk:finish-feature` | Changelog + PR |
| `/sk:frontend-design` | UI mockup + optional Pencil visual design |
| `/sk:gates` | All quality gates in parallel batches |
| `/sk:health` | Harness self-audit scorecard |
| `/sk:help` | Show all commands |
| `/sk:hotfix` | Emergency fix workflow |
| `/sk:laravel-init` | Configure existing Laravel project |
| `/sk:laravel-new` | Scaffold fresh Laravel app |
| `/sk:learn` | Extract reusable patterns from sessions |
| `/sk:lint` | Auto-detect and run all linters |
| `/sk:mvp` | Generate MVP app from a prompt |
| `/sk:perf` | Performance audit |
| `/sk:plan` | Create/refresh planning files |
| `/sk:release` | Version bump + tag (`--android` / `--ios` for store audit) |
| `/sk:resume-session` | Resume a previously saved session |
| `/sk:retro` | Post-ship retrospective |
| `/sk:reverse-doc` | Generate docs from existing code |
| `/sk:review` | 7-dimension code review |
| `/sk:safety-guard` | Protect against destructive ops |
| `/sk:save-session` | Save session state for continuity |
| `/sk:schema-migrate` | Database schema change analysis |
| `/sk:scope-check` | Detect scope creep mid-implementation |
| `/sk:security-check` | OWASP security audit |
| `/sk:seo-audit` | sk:seo-audit for web projects |
| `/sk:set-profile` | Switch model routing profile |
| `/sk:setup-claude` | Bootstrap project scaffolding |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:start` | Smart entry point — classifies task, routes to optimal flow |
| `/sk:status` | Show workflow + task status |
| `/sk:team` | Parallel domain agents for full-stack tasks |
| `/sk:test` | Run all test suites |
| `/sk:update-task` | Mark task done |
| `/sk:write-plan` | Write plan to `tasks/todo.md` |
| `/sk:write-tests` | TDD: write failing tests first |

</details>

---

## Learn More

| Topic | Where |
|-------|-------|
| Detailed workflow steps (8-step flow) | [DOCUMENTATION.md](.claude/docs/DOCUMENTATION.md) |
| Feature specifications | [docs/FEATURES.md](docs/FEATURES.md) |
| Model routing profiles & config | [DOCUMENTATION.md — Config](.claude/docs/DOCUMENTATION.md#config-reference) |
| Infrastructure (hooks, agents, rules) | [DOCUMENTATION.md — Setup](.claude/docs/DOCUMENTATION.md#what-gets-created) |
| Security & permissions | [DOCUMENTATION.md — Security](.claude/docs/DOCUMENTATION.md#security) |

---

<div align="center">

MIT License — Built by [Kenneth Solomon](https://github.com/kennethsolomon)

**Claude Code is powerful. ShipKit makes it reliable.**

</div>
