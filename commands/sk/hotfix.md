---
description: "Emergency fix workflow for production issues. Skips brainstorm, design, and TDD setup. Goes straight to: investigate → branch → fix → gates → ship."
disable-model-invocation: true
---

# /sk:hotfix

Emergency workflow for production issues that need to ship fast. Skips brainstorm, design, and write-tests phases. Quality gates still apply — they cannot be skipped.

## When to Use

- A bug is causing production impact RIGHT NOW
- There is no time for full TDD workflow
- The fix is small and well-understood

**If the bug is complex or the fix is unclear, use the full Bug Fix Flow (`/sk:debug`) instead.**

## Before You Start

1. Read `tasks/lessons.md` — apply any relevant lessons immediately
2. Read `tasks/todo.md` — note the bug being fixed for tracking

## Hotfix Flow

| # | Step | Command | Notes |
|---|------|---------|-------|
| 1 | Investigate | `/sk:debug` | Root-cause analysis only — understand before touching code |
| 2 | Branch | `/sk:branch` | Auto-named from the bug description |
| 3 | Fix | implement directly | No write-tests phase — go straight to the fix |
| 4 | Smoke Test | run existing tests | Existing tests MUST still pass — no new failures allowed |
| 5 | Commit | `/sk:smart-commit` | Commit the fix |
| 6 | **Lint** | `/sk:lint` | **GATE** — all lint tools must pass |
| 7 | Commit | `/sk:smart-commit` | Skip if lint was clean |
| 8 | **Verify Tests** | `/sk:test` | **GATE** — all existing tests must pass |
| 9 | Commit | `/sk:smart-commit` | Skip if tests passed first try |
| 10 | **Security** | `/sk:security-check` | **GATE** — 0 issues across all severities |
| 11 | Commit | `/sk:smart-commit` | Skip if security was clean |
| 12 | **Review** | `/sk:review` | **GATE** — 0 issues including nitpicks |
| 13 | Commit | `/sk:smart-commit` | Skip if review was clean |
| 14 | Update | `/sk:update-task` | Mark done, log completion |
| 15 | Finalize | `/sk:finish-feature` | Changelog + PR — mark PR as hotfix |

## Quality Gates Are Non-Negotiable

Even in a hotfix, **gates 6, 8, 10, and 12 cannot be skipped.** Fix issues immediately and re-run. A broken hotfix is worse than no hotfix.

## After Merging

Consider creating a follow-up task to:
- Write a regression test for the bug that was just fixed
- Add a lesson to `tasks/lessons.md` if this bug reveals a recurring pattern
- Review whether the root cause points to a broader systemic issue

## Step Summary Format

After each step, output:

```
--- Hotfix Step [#] [Name]: [done/skipped] ---
Summary: [what was done]
Next step: [#] [Name] — run `[command]`
```
