---
description: "Show all ShipKit commands and workflow overview."
---

# Meta

| Command | Description |
|---------|-------------|
| `/sk:help` | Show all commands and workflow overview |
| `/sk:status` | Show workflow and task status at a glance |
| `/sk:skill-creator` | Create or improve ShipKit skills |

---

# /sk:help — ShipKit

A structured workflow toolkit for Claude Code.
Run these commands in order for a complete, quality-gated feature build.

---

## Feature Workflow

| # | Command | Purpose |
|---|---------|---------|
| 1 | `/sk:brainstorm` | Explore requirements — **no code yet** |
| 2 | `/sk:frontend-design` or `/sk:api-design` | Design UI or API contracts *(auto-skip if no frontend/API keywords)* |
| 3 | `/sk:write-plan` | Write a decision-complete plan to `tasks/todo.md` |
| 4 | `/sk:branch` | Create a feature branch from the current task |
| 5 | `/sk:write-tests` + `/sk:execute-plan` | TDD red + green (includes `/sk:schema-migrate` if DB keywords detected) |
| 5.5 | `/sk:scope-check` | Trim scope creep — compare implementation to plan |
| 6 | `/sk:smart-commit` | Conventional commit with approval |
| 7 | `/sk:gates` | **All quality gates** — lint, test, security, perf, review, e2e *(hard gate)* |
| 8 | `/sk:finish-feature` | Changelog + PR creation |
| 8.5 | `/sk:learn` | Extract reusable patterns from this session |
| 8.6 | `/sk:retro` | Post-ship retrospective — velocity, blockers, next actions |

## Requirement Change Flow

Requirements change mid-workflow? Run `/sk:change` — it classifies the scope and routes you back to the right step.

| Tier | Scope | Re-entry |
|------|-------|---------|
| Tier 1 | Behavior tweak *(logic changes, plan stays)* | `/sk:write-tests` |
| Tier 2 | New requirements *(new scope or constraints)* | `/sk:write-plan` |
| Tier 3 | Scope shift *(rethinking the approach)* | `/sk:brainstorm` |

## Bug Fix Workflow

| Command | Purpose |
|---------|---------|
| `/sk:debug` | Root-cause analysis |
| `/sk:write-plan` | Fix plan |
| `/sk:branch` | Feature branch |
| `/sk:write-tests` | Reproduce the bug in a test |
| `/sk:execute-plan` | Fix the bug |
| `/sk:lint` → `/sk:test` → `/sk:security-check` → `/sk:review` | Quality gates |
| `/sk:finish-feature` | Changelog + PR |

## All Commands

| Command | Description |
|---------|-------------|
| `/sk:accessibility` | WCAG 2.1 AA audit on frontend code |
| `/sk:api-design` | Design REST/GraphQL contracts before implementation |
| `/sk:autopilot` | Hands-free workflow — auto-skip, auto-advance, auto-commit |
| `/sk:brainstorm` | Explore requirements and design (includes search-first research) |
| `/sk:branch` | Create branch from current task |
| `/sk:change` | Handle mid-workflow requirement change |
| `/sk:config` | View and edit project config |
| `/sk:context` | Load project context (automatic via hooks) |
| `/sk:context-budget` | Audit context window token consumption and find savings |
| `/sk:dashboard` | Read-only workflow Kanban board |
| `/sk:debug` | Structured bug investigation |
| `/sk:e2e` | E2E behavioral verification |
| `/sk:eval` | Define, run, and report evals for agent reliability |
| `/sk:execute-plan` | Implement plan in batches |
| `/sk:fast-track` | Small changes — skip planning, keep gates |
| `/sk:features` | Sync docs/sk:features/ specs with codebase |
| `/sk:finish-feature` | Changelog + PR creation |
| `/sk:frontend-design` | UI mockup + optional Pencil visual mockup |
| `/sk:gates` | All quality gates in parallel batches |
| `/sk:health` | Harness self-audit scorecard (7 categories, 0-70) |
| `/sk:hotfix` | Emergency fix workflow (skips design/TDD) |
| `/sk:laravel-init` | Configure existing Laravel project |
| `/sk:laravel-new` | Scaffold new Laravel project |
| `/sk:learn` | Extract reusable patterns from sessions |
| `/sk:lint` | Auto-detect and run all linters |
| `/sk:mvp` | Generate MVP app from a prompt |
| `/sk:perf` | Performance audit |
| `/sk:plan` | Create/refresh task planning files |
| `/sk:release` | Version bump + tag (`--android` / `--ios` for store audit) |
| `/sk:resume-session` | Resume a previously saved session |
| `/sk:retro` | Post-ship retrospective |
| `/sk:reverse-doc` | Generate docs from existing code |
| `/sk:review` | 7-dimension self-review of branch changes |
| `/sk:safety-guard` | Protect against destructive ops (careful/freeze/guard) |
| `/sk:save-session` | Save session state for cross-session continuity |
| `/sk:schema-migrate` | Multi-ORM schema change analysis |
| `/sk:scope-check` | Detect scope creep mid-implementation |
| `/sk:security-check` | OWASP security audit |
| `/sk:seo-audit` | SEO audit for web projects |
| `/sk:set-profile` | Switch model routing profile |
| `/sk:setup-claude` | Bootstrap project scaffolding |
| `/sk:setup-optimizer` | Diagnose + update workflow + enrich CLAUDE.md |
| `/sk:skill-creator` | Create or improve skills |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:start` | Smart entry point — classifies task, routes to optimal flow |
| `/sk:status` | Show workflow and task status |
| `/sk:team` | Parallel domain agents for full-stack tasks |
| `/sk:test` | Auto-detect and verify all tests pass |
| `/sk:update-task` | Mark task done, log completion |
| `/sk:write-plan` | Write plan to `tasks/todo.md` |
| `/sk:write-tests` | TDD: write failing tests first |

---

## Model Routing Profiles

ShipKit routes each skill to the right model automatically. Set once per project:

```
/sk:set-profile balanced   ← default
/sk:set-profile quality    ← most projects
/sk:set-profile full-sail  ← high-stakes / client work
/sk:set-profile budget     ← side projects / exploration
```

| Skill group | full-sail | quality | balanced | budget |
|-------------|-----------|---------|----------|--------|
| brainstorm, write-plan, debug, execute-plan, review | opus | opus | sonnet | sonnet |
| write-tests, frontend-design, api-design, security-check | opus | sonnet | sonnet | sonnet |
| change | opus | sonnet | sonnet | sonnet |
| autopilot, team | opus | opus | sonnet | sonnet |
| perf, schema-migrate, accessibility | opus | sonnet | sonnet | haiku |
| eval | sonnet | sonnet | sonnet | haiku |
| lint, test | sonnet | sonnet | haiku | haiku |
| smart-commit, branch, update-task | haiku | haiku | haiku | haiku |
| start, learn, context-budget, health | haiku | haiku | haiku | haiku |
| save-session, resume-session, safety-guard | haiku | haiku | haiku | haiku |

`opus` = inherit (uses your current session model).
Config lives in `.shipkit/config.json` — per project, gitignored by default.

---

**ShipKit** by Kenneth Solomon · `npx @kennethsolomon/shipkit` to install/update
