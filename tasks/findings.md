# Findings — 2026-03-16 — Workflow Enhancement: E2E, Fix & Retest, sk:features, Simplify, Dep Audit, sk:change

## Problem Statement

The 24-step workflow has 6 gaps:
1. No E2E testing step — behavioral regressions pass all quality gates
2. `sk:features` exists but is not wired into the workflow
3. `/simplify` (built-in Claude Code skill) is not wired into the workflow
4. No dependency audit — vulnerable 3rd-party packages pass all quality gates
5. `sk:change` is buried with no dedicated documentation section
6. No protocol for logic changes made during quality gates — tests become stale silently

## Chosen Approach: Approach B (Smart Absorption) — 27 steps

### What changes

| Item | How integrated |
|------|---------------|
| Dep audit | Folded into `/lint` step (runs `npm audit --audit-level=high` / `composer audit` alongside analyzers) |
| E2E Tests | New hard gate step **after Review** (step 22) — tests final, fully-reviewed code |
| Simplify | Folded into `/review` step (review calls simplify first, then full review) |
| sk:features | New step **after Finalize** (step 26) — syncs specs with what was actually shipped |
| sk:change | Dedicated "Requirement Change Flow" section in CLAUDE.md (no new numbered step) |
| agent-browser | Mandatory prereq added to `install.sh` |
| Fix & Retest Protocol | New named protocol covering steps 12, 14, 16, 18, 20, 22 |

### New 27-step workflow table

| # | Step | Command | Type | Loop? |
|---|------|---------|------|-------|
| 1 | Read Todo | read `tasks/todo.md` | required | no |
| 2 | Read Lessons | read `tasks/lessons.md` | required | no |
| 3 | Explore | `/brainstorm` | required | no |
| 4 | Design | `/frontend-design` or `/api-design` | optional | no |
| 5 | Accessibility | `/accessibility` | optional | no |
| 6 | Plan | `/write-plan` | required | no |
| 7 | Branch | `/branch` | required | no |
| 8 | Migrate | `/schema-migrate` | optional | no |
| 9 | Write Tests | `/write-tests` | required | no |
| 10 | Implement | `/execute-plan` | required | no |
| 11 | Commit | `/smart-commit` | required | no |
| 12 | Lint + Dep Audit | `/lint` | HARD GATE | yes |
| 13 | Commit | `/smart-commit` | conditional | no |
| 14 | Verify Tests | `/test` | HARD GATE | yes |
| 15 | Commit | `/smart-commit` | conditional | no |
| 16 | Security | `/security-check` | HARD GATE | yes |
| 17 | Commit | `/smart-commit` | conditional | no |
| 18 | Performance | `/perf` | optional gate | yes |
| 19 | Commit | `/smart-commit` | conditional | no |
| 20 | Review + Simplify | `/review` | HARD GATE | yes |
| 21 | Commit | `/smart-commit` | conditional | no |
| 22 | E2E Tests | `/e2e` | HARD GATE | yes |
| 23 | Commit | `/smart-commit` | conditional | no |
| 24 | Update Task | `/update-task` | required | no |
| 25 | Finalize | `/finish-feature` | required | no |
| 26 | Sync Features | `/features` | required | no |
| 27 | Release | `/release` | optional | no |

### New flow line

`Read → Explore → Design → Accessibility → Plan → Branch → Migrate → Write Tests → Implement → Lint → Verify Tests → Security → Performance → Review → E2E Tests → Finish → Sync Features`

### Hard gates (5 total, up from 4)
- Step 12: Lint + Dep Audit
- Step 14: Verify Tests (100% coverage)
- Step 16: Security (0 issues)
- Step 20: Review + Simplify (0 issues)
- Step 22: E2E Tests (all scenarios pass)

### Fix & Retest Protocol

Applies to steps 12, 14, 16, 18, 20, 22 — any step that can produce code changes.

```
When any step requires a fix:

1. Classify the fix:
   a. Format/style/config/wording change → commit and re-run the gate (no test update needed)
   b. Logic change (new branch, modified condition, new data path,
      query change, new function, API change) → trigger protocol:

      i.  Update or add failing unit tests for the new behavior
      ii. Re-run /test → must pass at 100% coverage
      iii.Commit (tests + fix together in one commit)
      iv. Re-run the current gate from scratch

Applies to: Lint (12), Verify Tests (14), Security (16),
            Performance (18), Review (20), E2E (22)
```

Exception: Lint formatter auto-fixes (Prettier, Pint, gofmt) are never logic changes — bypass protocol automatically.

## Files to Update (from lessons.md — all in one commit)

1. `CLAUDE.md` — live workflow reference
2. `skills/sk:setup-claude/templates/CLAUDE.md.template` — template for new projects
3. `skills/sk:setup-claude/templates/tasks/workflow-status.md.template` — tracker template
4. `README.md` — workflow table in docs
5. `skills/sk:setup-optimizer/SKILL.md` — embeds step count, flow line, hard gate numbers
6. `CHANGELOG.md` — document what changed
7. `install.sh` — add agent-browser install + new `/e2e` command to echo block
8. `skills/sk:setup-claude/templates/commands/brainstorm.md.template` — Workflow breadcrumb
9. `skills/sk:setup-claude/templates/commands/write-plan.md.template` — Workflow breadcrumb
10. `skills/sk:setup-claude/templates/commands/execute-plan.md.template` — Workflow breadcrumb
11. `skills/sk:setup-claude/templates/commands/security-check.md.template` — Workflow breadcrumb
12. `skills/sk:setup-claude/templates/commands/finish-feature.md.template` — Workflow breadcrumb
13. `skills/sk:setup-claude/templates/commands/release.md.template` — Workflow breadcrumb
14. `.claude/docs/DOCUMENTATION.md` — full workflow diagram, step tables, skills list

### Additional skill files to update
- `skills/sk:lint/SKILL.md` — add dep audit step + Fix & Retest Protocol classification
- `skills/sk:test/SKILL.md` — add Fix & Retest Protocol classification
- `skills/sk:security-check/SKILL.md` — add Fix & Retest Protocol classification
- `skills/sk:perf/SKILL.md` — add Fix & Retest Protocol classification
- `skills/sk:review/SKILL.md` — add simplify pre-step + Fix & Retest Protocol classification

### New files to create
- `skills/sk:e2e/SKILL.md` — new E2E skill using agent-browser (hard gate, all scenarios must pass)

## New Skill: sk:e2e

### Purpose
Run E2E behavioral verification using agent-browser as the final quality gate before finalize. Tests the complete, reviewed, secure implementation from a user's perspective.

### Key behaviors
- Uses agent-browser (`agent-browser` CLI) for browser automation
- Reads `tasks/todo.md` and `tasks/findings.md` to understand acceptance criteria
- Runs existing E2E test files (written in step 9 `/write-tests`)
- Hard gate: all scenarios must pass
- Fix & Retest Protocol: logic fixes require unit test updates + /test re-run before re-running E2E
- Token-efficient: uses agent-browser's ref-based snapshot system

### agent-browser integration
- Install: `npm install -g agent-browser && agent-browser install` (added to `install.sh`)
- Core flow: `open → snapshot -i → interact via @refs → assert`
- Semantic locators: `find role button`, `find text "Sign In"` (not CSS selectors)

## sk:change Section

Add as dedicated section in CLAUDE.md alongside Bug Fix Flow and Hotfix Flow:

```
### Requirement Change Flow
When requirements change mid-workflow, run `/sk:change` to:
1. Assess the scope of the change
2. Determine which completed steps are invalidated
3. Re-enter the workflow at the correct step
4. Reset workflow-status.md to reflect the new entry point
```

## Command Naming Convention

All user-facing commands from this plugin must use the `/sk:` prefix so the origin is unambiguous. CLAUDE.md currently documents commands without the prefix (`/brainstorm`, `/lint`, `/test` etc.) — this must be corrected across all files.

When updating CLAUDE.md and all template files, replace all command references:
- `/brainstorm` → `/sk:brainstorm`
- `/frontend-design` → `/sk:frontend-design`
- `/api-design` → `/sk:api-design`
- `/accessibility` → `/sk:accessibility`
- `/write-plan` → `/sk:write-plan`
- `/branch` → `/sk:branch`
- `/schema-migrate` → `/sk:schema-migrate`
- `/write-tests` → `/sk:write-tests`
- `/execute-plan` → `/sk:execute-plan`
- `/smart-commit` → `/sk:smart-commit`
- `/lint` → `/sk:lint`
- `/test` → `/sk:test`
- `/security-check` → `/sk:security-check`
- `/perf` → `/sk:perf`
- `/review` → `/sk:review`
- `/debug` → `/sk:debug`
- `/hotfix` → `/sk:hotfix`
- `/update-task` → `/sk:update-task`
- `/finish-feature` → `/sk:finish-feature`
- `/features` → `/sk:features`
- `/e2e` → `/sk:e2e`
- `/change` → `/sk:change`
- `/release` → `/sk:release`
- `/status` → `/sk:status`
- `/setup-optimizer` → `/sk:setup-optimizer`

This applies to: CLAUDE.md, all template files, README.md, DOCUMENTATION.md, all SKILL.md files, workflow-status.md.template.

## Open Questions
- None — design is locked
