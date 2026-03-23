# /sk:fast-track

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone (replaces full workflow for small changes)
> **Command:** `/sk:fast-track`
> **Skill file:** `skills/sk:fast-track/SKILL.md`

---

## Overview

Abbreviated workflow for small, well-understood changes. Skips brainstorm, design, accessibility, plan, and write-tests phases but enforces all quality gates via `/sk:gates`. Includes guard rails that warn when changes exceed fast-track thresholds.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Pick task or accept user description | Yes |
| `tasks/lessons.md` | Active lessons applied as constraints | Yes |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Feature branch | Git | Created via `/sk:branch` |
| Implementation code | Working tree | Direct implementation, no TDD |
| Conventional commit | Git history | Via `/sk:smart-commit` |
| Gate results | Terminal + `tasks/workflow-status.md` | Via `/sk:gates` |
| Changelog + PR | Git + remote | Via `/sk:finish-feature` |

---

## Business Logic

1. **Context** (quick) — read `tasks/todo.md` (pick task or accept user description) and `tasks/lessons.md` (apply active lessons as constraints).
2. **Branch** — run `/sk:branch` to create a feature branch.
3. **Implement** — write code directly. No brainstorm, design, plan, or TDD phases. Focus on minimal change needed.
4. **Guard rails check** (post-implementation):
   - Diff size > 300 lines: warn and ask to continue or switch to full workflow
   - New files > 5: warn and suggest `/sk:write-tests` first
   - Migration files detected: warn and suggest `/sk:schema-migrate`
5. **Commit** — run `/sk:smart-commit` for conventional commit.
6. **Gates** — run `/sk:gates` for all quality gates in parallel batches (lint, test, security, perf, review, E2E). Same gate process as full workflow.
7. **Finalize** — run `/sk:finish-feature` for changelog + PR.

---

## Hard Rules

- All quality gates are enforced — no shortcuts on quality, only on ceremony
- Guard rails must trigger warnings at thresholds (300 lines, 5 new files, migration files)
- Guard rail warnings require explicit user confirmation to proceed
- Cannot be used for new features (use full workflow), multi-system changes (use full workflow), design-dependent changes (use `/sk:brainstorm`), or bug fixes (use `/sk:debug` flow)
- Workflow status must be updated: planning steps marked as "skipped (fast-track)"

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Diff exceeds 300 lines | Warn: "This change is [N] lines -- larger than the 300-line fast-track threshold. Consider the full workflow. Continue? (y/n)" |
| More than 5 new files created | Warn: "You've created [N] new files. Consider running `/sk:write-tests` first. Continue? (y/n)" |
| Migration files in changes | Warn: "Migration files detected. Consider running `/sk:schema-migrate` for analysis." |
| User says no to guard rail warning | Exit fast-track; recommend full workflow |
| No `tasks/todo.md` task matches | Accept user's verbal description as the task |

---

## Error States

| Condition | Error message / behavior |
|-----------|--------------------------|
| `tasks/lessons.md` missing | Warn but continue — no lessons to apply |
| `/sk:gates` fails (3-strike) | Stop fast-track; report gate failure details to user |
| Already on main branch | Error: "Cannot fast-track on main — run `/sk:branch` first" |

---

## UI/UX Behavior

### CLI Output
Abbreviated step indicators. Guard rail warnings when thresholds exceeded. Gate results from `/sk:gates`.

### When Done
```
Fast-track complete. PR created.
```

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:fast-track/SKILL.md` — full implementation spec
- `/sk:gates` — quality gate orchestrator used in step 5
- `/sk:branch` — branch creation step
- `/sk:smart-commit` — commit step
- `/sk:finish-feature` — finalization step
- `/sk:debug` — alternative flow for bug fixes
- `/sk:hotfix` — alternative flow for production emergencies
