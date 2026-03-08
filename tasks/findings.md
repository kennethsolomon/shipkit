# Findings — 2026-03-08 — Workflow Tracker Enhancement

## Requirements
- Strict ordered workflow with 14 steps, tracked in `tasks/workflow-status.md`
- Status dashboard printed after every slash command (done/partial/skipped/not yet/in progress)
- ">> next <<" indicator on the next step to run
- Loop enforcement: `/security-check` and `/review` must reach 0 issues (all severities, including nitpicks)
- Attempt counting for looped steps (security-check, review)
- Conditional commits (steps 7, 10, 12) auto-skip with reason if no changes
- `/debug` is optional — confirm to skip
- `/frontend-design` is optional — confirm to skip
- `/release` is step 14, optional — confirm to skip
- Tracker resets on every new feature/bug/problem
- Reset via: (a) `/brainstorm` auto-detects existing tracker and asks, or (b) manual request
- Tracker file created by `/setup-claude` and `/re-setup`

## Workflow Steps (14)

| # | Step | Type | Loop? |
|---|------|------|-------|
| 1 | /brainstorm | required | no |
| 2 | /frontend-design | optional (confirm to skip) | no |
| 3 | /write-plan | required | no |
| 4 | /execute-plan | required | no |
| 5 | /commit | required | no |
| 6 | /write-tests | required | no |
| 7 | /commit | conditional (auto-skip if no changes) | no |
| 8 | /debug | optional (confirm to skip) | no |
| 9 | /security-check | required, must be fully clean | yes — fix → commit → security-check |
| 10 | /commit | conditional (auto-skip if security was clean) | no |
| 11 | /review | required, must be fully clean (0 issues, 0 nitpicks) | yes — fix → commit → review |
| 12 | /commit | conditional (auto-skip if review was clean) | no |
| 13 | /finish-feature | required | no |
| 14 | /release | optional (confirm to skip) | no |

## Decisions
| Decision | Rationale |
|----------|-----------|
| Approach A: File tracker + CLAUDE.md rules | Simplest solution, no code enforcement needed — CLAUDE.md rules are sufficient |
| Single file `tasks/workflow-status.md` | Persists across conversations, human-readable |
| Reset via brainstorm + manual | Two entry points cover all use cases |
| Auto-skip conditional commits | Reduces friction — no need to confirm when nothing changed |
| Attempt counting on loops | Visibility into how many passes security/review took |

## Changes Needed
| File | Change |
|------|--------|
| `CLAUDE.md` | Replace workflow section with strict tracker-based flow |
| `setup-claude` templates | Add `workflow-status.md` template to bootstrap |
| `tasks/workflow-status.md` | New tracker file |
| Brainstorm skill template | Add reset detection at top |

## Open Questions
- None
