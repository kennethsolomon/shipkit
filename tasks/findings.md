# Findings — 2026-03-20 — Gate Auto-Commit + Tech Debt Logging

## Problem Statement

Two UX frustrations with ShipKit's gate workflow:
1. Gates (lint, test, security, perf, review, e2e) ask the user to approve each commit after every fix cycle — unnecessary friction when the gate itself enforces 0 issues
2. Pre-existing issues found during gates are either silently skipped ("out of scope") or fixed inline (scope creep) — neither is correct

## Key Decisions Made

- **Gate loops own their commits** — fix → auto-commit → re-run is internal to each gate. No asking. Commit message: `fix(<gate>): <what was fixed>`
- **Conditional commit steps removed** — steps 13, 15, 17, 19, 21, 23 are eliminated. Workflow shrinks from 27 → 21 steps
- **Pre-existing issues → `tasks/tech-debt.md`** — gates log out-of-scope issues there instead of fixing inline or skipping silently
- **tech-debt.md is append-only** — entries are never deleted; marked `Resolved:` when fixed
- **Resolved by sk:update-task** — when a task that addresses a debt item completes, sk:update-task marks it resolved with the branch name
- **sk:context and sk:write-plan read tech-debt.md** — surface unresolved items in session brief; sk:write-plan asks if any should be included in the current task

## Chosen Approach

Single approach — no alternatives debated; direction agreed in conversation.

### Gate Loop (new internal flow for all 6 gates)
```
gate runs
→ issues found?
  → yes: fix all (any severity, any level) → auto-commit → re-run gate → repeat
  → pre-existing issue (outside branch diff)? → log to tasks/tech-debt.md → do not fix → continue
→ clean: move to next workflow step
```

### tech-debt.md Entry Format
```markdown
### [YYYY-MM-DD] Found during: sk:<gate>
File: path/to/file.ext:line
Issue: description of the problem
Severity: critical | high | medium | low | nitpick
Resolved: YYYY-MM-DD — feature/branch-name  ← added by sk:update-task when fixed
```

### New Workflow (21 steps)
| # | Step |
|---|------|
| 1 | Read Todo |
| 2 | Read Lessons |
| 3 | Explore |
| 4 | Design |
| 5 | Accessibility |
| 6 | Plan |
| 7 | Branch |
| 8 | Migrate |
| 9 | Write Tests |
| 10 | Implement |
| 11 | Commit (post-implement milestone) |
| 12 | Lint + Dep Audit [gate — internal fix-commit-rerun loop] |
| 13 | Verify Tests [gate — internal fix-commit-rerun loop] |
| 14 | Security [gate — internal fix-commit-rerun loop] |
| 15 | Performance [gate — internal fix-commit-rerun loop] |
| 16 | Review + Simplify [gate — internal fix-commit-rerun loop] |
| 17 | E2E Tests [gate — internal fix-commit-rerun loop] |
| 18 | Update |
| 19 | Finalize |
| 20 | Sync Features |
| 21 | Release |

## Files Changed

### Gate SKILL.md files (fix loop + tech-debt logging)
- `skills/sk:lint/SKILL.md`
- `skills/sk:test/SKILL.md`
- `skills/sk:security-check/SKILL.md`
- `skills/sk:perf/SKILL.md`
- `skills/sk:review/SKILL.md`
- `skills/sk:e2e/SKILL.md`

### Planning/utility SKILL.md files (tech-debt integration)
- `skills/sk:context/SKILL.md` — read tech-debt.md, surface unresolved
- `skills/sk:write-plan/SKILL.md` — read tech-debt.md, ask to include items
- `skills/sk:update-task/SKILL.md` — mark resolved items

### Workflow definition files (step renumbering)
- `CLAUDE.md`
- `skills/sk:setup-claude/templates/CLAUDE.md.template`
- `skills/sk:setup-claude/templates/tasks/workflow-status.md.template`
- `README.md`
- `skills/sk:setup-optimizer/SKILL.md`
- `.claude/docs/DOCUMENTATION.md`
- `CHANGELOG.md`
- `tasks/lessons.md` (append only)
- Command templates with **Workflow:** breadcrumbs (6 files)

## Open Questions

- None — direction locked
