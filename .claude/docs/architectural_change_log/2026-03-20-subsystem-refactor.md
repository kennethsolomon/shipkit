# Gate Auto-Commit + Tech Debt Logging (March 20, 2026)

## Summary

Gate skills (lint, test, security, perf, review, e2e) now own their fix-commit-rerun loops internally. Pre-existing issues found during gates are logged to `tasks/tech-debt.md` instead of being fixed inline or silently skipped. Workflow shrinks from 27 → 21 steps by removing 6 conditional commit steps.

## Type of Architectural Change

**Workflow Behavioral Change + New Persistent Context File**

## What Changed

**Gate Behavior (6 skills):**
- `skills/sk:lint/SKILL.md`, `skills/sk:test/SKILL.md`, `commands/sk/security-check.md`, `skills/sk:perf/SKILL.md`, `skills/sk:review/SKILL.md`, `skills/sk:e2e/SKILL.md`
- Fix loop is now fully internal: fix → auto-commit (`fix(<gate>): ...`) → re-run → repeat until clean. No user confirmation for commits.
- Pre-existing issues (files outside `git diff main..HEAD`) logged to `tasks/tech-debt.md`, never fixed inline

**New Persistent Context File (`tasks/tech-debt.md`):**
- Append-only log of pre-existing issues found by gates
- Entry format: `### [YYYY-MM-DD] Found during: sk:<gate>` / `File:` / `Issue:` / `Severity:` / `Resolved:` (added by sk:update-task)
- Integrated into sk:context (session brief), sk:write-plan (includes in plan?), sk:update-task (marks resolved)

**Workflow Step Reduction (27 → 21):**
- Removed 6 conditional commit steps (old 13, 15, 17, 19, 21, 23)
- Gates renumbered: 12–17; Update=18, Finalize=19, Sync=20, Release=21
- Updated in CLAUDE.md, README, templates, DOCUMENTATION.md, sk:setup-optimizer

**sk:schema-migrate Phase 0:**
- Auto-detects migration files in branch diff before any ORM detection
- If no migration files found: exits cleanly without asking user

**sk:frontend-design Pencil Persistence:**
- Now reads `tasks/todo.md` to derive task-name slug for `.pen` filename
- Always calls `open_document('docs/design/[task-name].pen')` — file persisted to disk from creation

**Statistics:**
- Lines added: 979
- Lines removed: 476
- Files modified: 32

## Impact

- Gate behavior change affects all 6 quality gate skills
- New `tasks/tech-debt.md` file is read at every session start (sk:context) and plan creation (sk:write-plan)
- Workflow step references in all 14 workflow-definition files updated

## Before & After

**Before:** Gate finds issue → fixes → asks user "commit? (y/n)" → user confirms → commits → gate re-runs
**After:** Gate finds issue → fixes → auto-commits internally → re-runs → no user prompt

**Before:** Pre-existing issues either fixed inline (scope creep) or ignored
**After:** Pre-existing issues logged to `tasks/tech-debt.md` with a `Resolved:` lifecycle

## Affected Components

- All 6 hard gate skills
- sk:context, sk:write-plan, sk:update-task (tech-debt.md integration)
- sk:schema-migrate (auto-detect Phase 0)
- sk:frontend-design (Pencil disk persistence)
- CLAUDE.md, README, DOCUMENTATION.md, all 6 command templates (step renumbering)

## Migration/Compatibility

No breaking changes for end users — workflow still follows the same logical sequence. Gate commit behavior is now automatic (was interactive). Users upgrading from v3.6.0:
- Existing projects: no changes needed; `tasks/tech-debt.md` is created on first gate run that finds pre-existing issues
- Workflow step numbers in existing `tasks/workflow-status.md` files are shifted — run `/sk:setup-optimizer` to update

## Verification

- [x] All affected code paths tested (143/143 assertions in tests/verify-workflow.sh)
- [x] Related documentation updated (CLAUDE.md, README, DOCUMENTATION.md, CHANGELOG, lessons.md)
- [x] No breaking changes (backward compatible — gates just no longer prompt for commits)
- [x] Dependent systems verified (sk:context, sk:write-plan, sk:update-task all updated)
