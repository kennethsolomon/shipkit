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
/sk:brainstorm
```

That's it. `/sk:setup-claude` creates your project scaffolding: planning files, lifecycle hooks, path-scoped coding rules, and a persistent statusline — all auto-configured for your stack.

---

## Pick Your Flow

| I want to... | Run this | What happens |
|--------------|----------|-------------|
| **Build a new feature** | `/sk:brainstorm` | Full workflow: plan → TDD → 6 quality gates → PR |
| **Make a small change** | `/sk:fast-track` | Skip planning, keep all quality gates |
| **Fix a bug** | `/sk:debug` | Investigate → regression test → fix → gates → PR |
| **Fix a production emergency** | `/sk:hotfix` | Skip TDD, but quality gates still enforced |
| **Handle a requirement change** | `/sk:change` | Assess scope, re-enter workflow at the right step |

---

## How a Feature Gets Built

Here's what a typical feature flow looks like:

```
Think:   /sk:brainstorm → /sk:write-plan
Build:   /sk:branch → /sk:write-tests → /sk:execute-plan → /sk:smart-commit
Verify:  /sk:gates          ← runs lint, test, security, perf, review, E2E Tests
Ship:    /sk:finish-feature  ← changelog + PR
```

**The key command is `/sk:gates`** — it runs all 6 quality gates in parallel batches:

| Batch | What runs | Why |
|-------|----------|-----|
| 1 (parallel) | lint + security + perf | Independent — run simultaneously |
| 2 | tests | Need lint fixes first |
| 3 | code review | Needs deep understanding |
| 4 | E2E tests | Needs review fixes |

Each gate auto-fixes issues, auto-commits, and re-runs until clean. You just wait.

---

## After Shipping

| Command | What it does |
|---------|-------------|
| `/sk:retro` | Analyze velocity, blockers, and patterns — generates action items |
| `/sk:scope-check` | Mid-implementation: detect scope creep (On Track → Out of Control) |
| `/sk:reverse-doc` | Generate docs from existing code — useful for inherited codebases |

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
<summary><strong>35 commands</strong> — click to expand</summary>

| Command | Purpose |
|---------|---------|
| `/sk:accessibility` | WCAG 2.1 AA audit |
| `/sk:api-design` | Design API contracts before implementation |
| `/sk:brainstorm` | Explore requirements and design |
| `/sk:branch` | Create feature branch from current task |
| `/sk:change` | Handle mid-workflow requirement changes |
| `/sk:config` | View/edit project config |
| `/sk:context` | Load project context (automatic via hooks) |
| `/sk:dashboard` | Live Kanban board — sk:dashboard across worktrees |
| `/sk:debug` | Structured bug investigation |
| `/sk:e2e` | E2E Tests — behavioral verification |
| `/sk:execute-plan` | Execute plan checkboxes in batches |
| `/sk:fast-track` | Small changes — skip planning, keep gates |
| `/sk:features` | Sync feature specs with codebase |
| `/sk:finish-feature` | Changelog + PR |
| `/sk:frontend-design` | UI mockup + optional Pencil visual design |
| `/sk:gates` | All quality gates in parallel batches |
| `/sk:help` | Show all commands |
| `/sk:hotfix` | Emergency fix workflow |
| `/sk:laravel-init` | Configure existing Laravel project |
| `/sk:laravel-new` | Scaffold fresh Laravel app |
| `/sk:lint` | Auto-detect and run all linters |
| `/sk:mvp` | Generate MVP app from a prompt |
| `/sk:perf` | Performance audit |
| `/sk:plan` | Create/refresh planning files |
| `/sk:release` | Version bump + tag (`--android` / `--ios` for store audit) |
| `/sk:retro` | Post-ship retrospective |
| `/sk:reverse-doc` | Generate docs from existing code |
| `/sk:review` | 7-dimension code review |
| `/sk:schema-migrate` | Database schema change analysis |
| `/sk:scope-check` | Detect scope creep mid-implementation |
| `/sk:security-check` | OWASP security audit |
| `/sk:seo-audit` | sk:seo-audit for web projects |
| `/sk:set-profile` | Switch model routing profile |
| `/sk:setup-claude` | Bootstrap project scaffolding |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:status` | Show workflow + task status |
| `/sk:test` | Run all test suites |
| `/sk:update-task` | Mark task done |
| `/sk:write-plan` | Write plan to `tasks/todo.md` |
| `/sk:write-tests` | TDD: write failing tests first |

</details>

---

## Learn More

| Topic | Where |
|-------|-------|
| Detailed workflow steps (21-step table) | [DOCUMENTATION.md](.claude/docs/DOCUMENTATION.md) |
| Feature specifications | [docs/FEATURES.md](docs/FEATURES.md) |
| Model routing profiles & config | [DOCUMENTATION.md — Config](.claude/docs/DOCUMENTATION.md#config-reference) |
| Infrastructure (hooks, agents, rules) | [DOCUMENTATION.md — Setup](.claude/docs/DOCUMENTATION.md#what-gets-created) |
| Security & permissions | [DOCUMENTATION.md — Security](.claude/docs/DOCUMENTATION.md#security) |

---

<div align="center">

MIT License — Built by [Kenneth Solomon](https://github.com/kennethsolomon)

**Claude Code is powerful. ShipKit makes it reliable.**

</div>
