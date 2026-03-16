---
description: "Show all ShipKit commands and workflow overview."
---

# /sk:help — ShipKit

A structured workflow toolkit for Claude Code.
Run these commands in order for a complete, quality-gated feature build.

---

## Feature Workflow

| Command | Purpose |
|---------|---------|
| `/sk:brainstorm` | Explore requirements and design — **no code yet** |
| `/sk:write-plan` | Write a decision-complete plan to `tasks/todo.md` |
| `/sk:branch` | Create a feature branch from the current task |
| `/sk:schema-migrate` | Analyze schema changes *(skip if no DB changes)* |
| `/sk:write-tests` | TDD red: write failing tests first |
| `/sk:execute-plan` | TDD green: implement until tests pass |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:lint` | **GATE** — all linters must pass |
| `/sk:test` | **GATE** — 100% coverage on new code |
| `/sk:security-check` | **GATE** — 0 security issues |
| `/sk:review` | **GATE** — self-review across 7 dimensions |
| `/sk:update-task` | Mark task done, log completion |
| `/sk:finish-feature` | Changelog + PR creation |

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
| `/sk:brainstorm` | Explore requirements, no code |
| `/sk:branch` | Create branch from current task |
| `/sk:change` | Handle mid-workflow requirement change — re-enter at the right step |
| `/sk:debug` | Structured bug investigation |
| `/sk:execute-plan` | Implement plan in batches |
| `/sk:features` | Sync docs/sk:features/ specs with codebase |
| `/sk:finish-feature` | Changelog + PR creation |
| `/sk:frontend-design` | UI mockup + design spec before implementation |
| `/sk:hotfix` | Emergency fix workflow (skips design/TDD) |
| `/sk:laravel-init` | Configure existing Laravel project |
| `/sk:laravel-new` | Scaffold new Laravel project |
| `/sk:lint` | Auto-detect and run all linters |
| `/sk:perf` | Performance audit |
| `/sk:plan` | Create/refresh task planning files |
| `/sk:release` | Version bump + changelog + tag |
| `/sk:review` | Self-review of branch changes |
| `/sk:schema-migrate` | Multi-ORM schema change analysis |
| `/sk:security-check` | OWASP security audit |
| `/sk:setup-claude` | Bootstrap project scaffolding |
| `/sk:setup-optimizer` | Enrich CLAUDE.md by scanning codebase |
| `/sk:skill-creator` | Create or improve skills |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:status` | Show workflow and task status |
| `/sk:test` | Auto-detect and verify all tests pass |
| `/sk:update-task` | Mark task done, log completion |
| `/sk:write-plan` | Write plan to `tasks/todo.md` |
| `/sk:write-tests` | TDD: write failing tests first |
| `/sk:config` | View and edit project config |
| `/sk:set-profile` | Switch model routing profile |

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
| perf, schema-migrate, accessibility | opus | sonnet | sonnet | haiku |
| lint, test | sonnet | sonnet | haiku | haiku |
| smart-commit, branch, update-task | haiku | haiku | haiku | haiku |

`opus` = inherit (uses your current session model).
Config lives in `.shipkit/config.json` — per project, gitignored by default.

---

**ShipKit** by Kenneth Solomon · `npx @kennethsolomon/shipkit` to install/update
