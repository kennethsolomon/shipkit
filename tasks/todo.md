# TODO — 2026-03-20 — Gate Auto-Commit + Tech Debt Logging

## Change Log
- [2026-03-20] Added Pencil disk persistence to sk:frontend-design — re-entered at /sk:write-tests

## Goal

Two UX improvements to the ShipKit gate workflow:
1. **Gate loops own their commits** — fix → auto-commit → re-run is fully internal to each gate. No asking the user.
2. **Pre-existing issues → `tasks/tech-debt.md`** — out-of-scope findings are logged, not fixed inline and not silently skipped. Marked `Resolved:` by `sk:update-task` when addressed.

Workflow shrinks from 27 → 21 steps (removes conditional commit steps 13, 15, 17, 19, 21, 23).

## Constraints (from lessons.md)

- When workflow step count/names change: update ALL 14 files (see lessons.md for complete list)
- All commands use `/sk:` prefix
- Never overwrite `tasks/lessons.md` — append only
- Never overwrite `tasks/security-findings.md` — append only
- New file `tasks/tech-debt.md`: also append-only

---

## Milestone 1: Tests (TDD Red Phase)

#### Wave 1 (parallel — all independent)

- [x] Add assertions to `tests/verify-workflow.sh` for gate auto-commit behavior:
  - `assert_contains` — `skills/sk:lint/SKILL.md` contains `"auto-commit"`
  - `assert_contains` — `skills/sk:test/SKILL.md` contains `"auto-commit"`
  - `assert_contains` — `commands/sk/security-check.md` contains `"auto-commit"`
  - `assert_contains` — `skills/sk:perf/SKILL.md` contains `"auto-commit"`
  - `assert_contains` — `skills/sk:review/SKILL.md` contains `"auto-commit"`
  - `assert_contains` — `skills/sk:e2e/SKILL.md` contains `"auto-commit"`

- [x] Add assertions for tech-debt.md integration:
  - `assert_contains` — `skills/sk:review/SKILL.md` contains `"tech-debt.md"`
  - `assert_contains` — `commands/sk/security-check.md` contains `"tech-debt.md"`
  - `assert_contains` — `skills/sk:lint/SKILL.md` contains `"tech-debt.md"`
  - `assert_contains` — `skills/sk:context/SKILL.md` contains `"tech-debt.md"`
  - `assert_contains` — `commands/sk/write-plan.md` contains `"tech-debt.md"`
  - `assert_contains` — `commands/sk/update-task.md` contains `"tech-debt.md"`
  - `assert_contains` — `commands/sk/update-task.md` contains `"Resolved:"`

- [x] Add assertions for workflow step count reduction:
  - `assert_not_contains` — `CLAUDE.md` does not contain `"| 13 | Commit"` (conditional commit removed)
  - `assert_not_contains` — `CLAUDE.md` does not contain `"| 15 | Commit"`
  - `assert_not_contains` — `CLAUDE.md` does not contain `"| 17 | Commit"`
  - `assert_not_contains` — `CLAUDE.md` does not contain `"| 23 | Commit"`
  - `assert_contains` — `CLAUDE.md` contains `"| 21 | Release"` (new final step number)

---

## Milestone 2: Gate SKILL.md Updates

#### Wave 2 (parallel — all gate skills are independent)

- [x] **sk:lint** — Update `skills/sk:lint/SKILL.md`
  - In Step 6 (Fix and Re-run): after all fixes are applied, add:
    - Auto-commit with message `fix(lint): resolve lint and dep audit issues`
    - Re-run all tools to verify clean
    - Loop until clean — no asking the user
  - In Step 6: if a pre-existing issue is found (exists outside `git diff HEAD --name-only`), log it to `tasks/tech-debt.md` using the standard format, do not fix it
  - Remove "ask before committing" language anywhere in the skill

- [x] **sk:test** — Update `skills/sk:test/SKILL.md`
  - In Step 4 (If Tests Fail): after fix is applied:
    - Auto-commit with message `fix(test): resolve failing tests`
    - Re-run the failing suite
    - Loop until all pass — no asking the user
  - Remove "confirm with the user before applying" clause (Step 4, last bullet) — just fix and commit

- [x] **sk:security-check** — Update `commands/sk/security-check.md`
  - Remove "DO NOT fix code" hard rule — replace with:
    - "Fix all in-scope findings (current branch diff) immediately. Auto-commit with `fix(security): resolve [severity] findings`. Re-run until 0 findings."
    - "Pre-existing findings (outside current branch diff): log to `tasks/tech-debt.md`, do not fix inline."
  - Keep `tasks/security-findings.md` report generation — it still tracks history
  - Update "When Done" section: remove "The user decides what to address" → gate is self-resolving

- [x] **sk:perf** — Update `skills/sk:perf/SKILL.md`
  - Remove "DO NOT fix code" hard rule — replace with:
    - "Fix all critical/high in-scope findings immediately. Auto-commit with `fix(perf): resolve [severity] findings`. Re-run until critical/high = 0."
    - "Medium/low findings: log to `tasks/tech-debt.md` if pre-existing, or include in same commit if in scope."
  - Keep `tasks/perf-findings.md` report generation
  - Update "When Done" section to reflect auto-fix behavior

- [x] **sk:review** — Update `skills/sk:review/SKILL.md`
  - Replace Step 11 (Next Steps) entirely:
    - All issues (Critical, Warning, Nitpick): fix all, auto-commit with `fix(review): address review findings`, re-run
    - No "would you like to fix nitpicks?" prompt — fix everything, no asking
    - Pre-existing issues (outside branch diff found during blast-radius analysis): log to `tasks/tech-debt.md`, do not fix
  - Step 0 (Simplify): if simplify makes changes, auto-commit with `fix(review): simplify pre-pass` — do not ask user
  - Update Fix & Retest Protocol: auto-commit after logic fix without asking

- [x] **sk:schema-migrate** — Update `skills/sk:schema-migrate/SKILL.md`
  - Add Phase 0 (before ORM Detection): Auto-detect migration changes
    - Run `git diff main..HEAD --name-only` and check for migration-related files:
      - `migrations/`, `database/migrations/`, `prisma/migrations/`, `alembic/versions/`, `db/migrate/`
      - Schema definition files: `prisma/schema.prisma`, `drizzle.config.*`, `alembic.ini`
      - Any `*.sql` files in migration directories
    - If **no migration files** found in diff → auto-skip: log "No migration changes detected — skipping" and exit cleanly
    - If migration files found → proceed with existing Phase 1 (ORM Detection) as normal
  - No asking the user — detection is automatic

- [x] **sk:e2e** — Update `skills/sk:e2e/SKILL.md`
  - In Fix & Retest Protocol: after fix is applied:
    - Auto-commit with message `fix(e2e): resolve failing E2E scenarios`
    - Re-run `/sk:e2e` from scratch
    - Loop until all pass — no asking
  - Pre-existing issues found during E2E (pre-existing bugs in unrelated features): log to `tasks/tech-debt.md`

---

## Milestone 3: Planning/Utility SKILL.md Updates

#### Wave 3 (parallel — all independent)

- [x] **sk:context** — Update `skills/sk:context/SKILL.md`
  - Add `tasks/tech-debt.md` as file #8 in the Files to Read table:
    - What to extract: count of unresolved entries (no `Resolved:` line), highest severity
  - Add `Tech Debt:` field to SESSION BRIEF output:
    ```
    Tech Debt:  [N] unresolved — highest: [severity] ([file])
    ```
  - Add edge case: "No `tasks/tech-debt.md`" → show "none logged"
  - If 0 unresolved: show "none"

- [x] **sk:write-plan** — Update `commands/sk/write-plan.md`
  - In Step 2 (Read context files): add `tasks/tech-debt.md` to the read list:
    - Filter to unresolved entries only (no `Resolved:` line)
    - If any unresolved items exist, after presenting the plan ask:
      > "There are N unresolved tech debt items in `tasks/tech-debt.md`. Should any be included in this task?"
    - If user says yes: add them as tasks in the plan before approval
    - If no tech-debt.md or 0 unresolved: skip silently

- [x] **sk:update-task** — Update `commands/sk/update-task.md`
  - Add Step 2.5 (between "Mark Task Done" and "Log Completion"):
    - Read `tasks/tech-debt.md` if it exists
    - Find any unresolved entries that match tasks in the current `tasks/todo.md` plan (by file/issue description)
    - For each matched entry: append `Resolved: [YYYY-MM-DD] — [current branch name]` to that entry
    - If no matches: skip silently
    - Never delete entries — only append the `Resolved:` line

---

## Milestone 4: Workflow Definition Files

#### Wave 4 (parallel — all independent)

- [x] **CLAUDE.md** — Update workflow table + rules
  - Remove steps 13, 15, 17, 19, 21, 23 (conditional commit steps) from the workflow table
  - Renumber remaining steps: gates become 12, 13, 14, 15, 16, 17; Update→18, Finalize→19, Sync→20, Release→21
  - Update Step column names for gates to note "internal fix-commit-rerun"
  - Update Hard Gate rules: "Gates own their commits — fix → auto-commit → re-run internally. No manual commit step after a gate."
  - Add tech-debt.md to "Project Memory" section — read at start of every task, append-only
  - Update Workflow Tracker Rules section: remove conditional commit logic (steps 13/15/17/19/21/23 no longer exist)
  - Update Bug Fix Flow and Hotfix Flow tables: remove conditional commit rows, renumber
  - Update Fix & Retest Protocol: auto-commit instead of ask

- [x] **`skills/sk:setup-claude/templates/CLAUDE.md.template`** — Mirror all CLAUDE.md changes
  - Same step removal, renumbering, gate rules, tech-debt.md section, tracker rule updates

- [x] **`skills/sk:setup-claude/templates/tasks/workflow-status.md.template`** — Remove conditional commit rows
  - Remove rows for old steps 13, 15, 17, 19, 21, 23
  - Renumber remaining rows to match new 21-step workflow

- [x] **README.md** — Update workflow table
  - Remove conditional commit rows (13, 15, 17, 19, 21, 23)
  - Renumber remaining steps

- [x] **`skills/sk:setup-optimizer/SKILL.md`** — Update step count + flow
  - Update step count reference (27 → 21)
  - Update the flow line if it mentions step numbers
  - Update hard gate step numbers (now 12, 13, 14, 15, 16, 17)

- [x] **`.claude/docs/DOCUMENTATION.md`** — Update workflow section
  - Update workflow step count and table
  - Remove conditional commit steps
  - Add tech-debt.md to project memory section

- [x] **`CHANGELOG.md`** — Document this change
  - New section: Gate Auto-Commit + Tech Debt Logging (v3.7.0 or next)
  - Bullet: "Gate loops now auto-fix + auto-commit internally — no separate commit step after each gate"
  - Bullet: "Removed conditional commit steps 13, 15, 17, 19, 21, 23 — workflow is now 21 steps"
  - Bullet: "Pre-existing issues found during gates are logged to `tasks/tech-debt.md` instead of fixed inline or skipped"
  - Bullet: "sk:context surfaces unresolved tech debt in session brief"
  - Bullet: "sk:write-plan checks tech-debt.md and asks if items should be included"
  - Bullet: "sk:update-task marks tech-debt entries resolved when related tasks complete"

- [x] **`tasks/lessons.md`** — Append new lesson (append-only)
  - New entry: `[2026-03-20] tech-debt.md — update gate skills when logging format changes`
  - Files: all 6 gate SKILL.md files + sk:context + sk:write-plan + sk:update-task

#### Wave 5 (parallel — command templates with Workflow breadcrumb, depends on Wave 4 CLAUDE.md being finalized)

- [ ] Update `skills/sk:setup-claude/templates/commands/brainstorm.md.template` — update `**Workflow:**` breadcrumb step numbers
- [ ] Update `skills/sk:setup-claude/templates/commands/write-plan.md.template` — update `**Workflow:**` breadcrumb
- [ ] Update `skills/sk:setup-claude/templates/commands/execute-plan.md.template` — update `**Workflow:**` breadcrumb
- [ ] Update `skills/sk:setup-claude/templates/commands/security-check.md.template` — update `**Workflow:**` breadcrumb
- [ ] Update `skills/sk:setup-claude/templates/commands/finish-feature.md.template` — update `**Workflow:**` breadcrumb
- [ ] Update `skills/sk:setup-claude/templates/commands/release.md.template` — update `**Workflow:**` breadcrumb

---

## Verification

```bash
# Gate skills have auto-commit language
grep -n "auto-commit" skills/sk:lint/SKILL.md
grep -n "auto-commit" skills/sk:test/SKILL.md
grep -n "auto-commit" commands/sk/security-check.md
grep -n "auto-commit" skills/sk:perf/SKILL.md
grep -n "auto-commit" skills/sk:review/SKILL.md
grep -n "auto-commit" skills/sk:e2e/SKILL.md

# tech-debt.md integration
grep -n "tech-debt.md" skills/sk:review/SKILL.md
grep -n "tech-debt.md" skills/sk:context/SKILL.md
grep -n "tech-debt.md" commands/sk/write-plan.md
grep -n "Resolved:" commands/sk/update-task.md

# Workflow step reduction
grep -c "Commit" CLAUDE.md  # should be fewer than before
grep "| 21 |" CLAUDE.md     # Release is now step 21

# Run full test suite
bash tests/verify-workflow.sh
```

## Acceptance Criteria

- [ ] `sk:schema-migrate` auto-detects migration changes and skips without asking if none found
- [ ] All 6 gate SKILL.md files contain auto-commit behavior in their fix loops
- [ ] No gate SKILL.md asks the user to approve commits
- [ ] All 6 gate SKILL.md files log pre-existing issues to `tasks/tech-debt.md`
- [ ] `tasks/tech-debt.md` format documented: entry with `Resolved:` lifecycle
- [ ] `sk:context` reads `tasks/tech-debt.md` and shows unresolved count in session brief
- [ ] `sk:write-plan` reads `tasks/tech-debt.md` and asks about unresolved items
- [ ] `sk:update-task` marks matched tech-debt entries as `Resolved:` on task completion
- [ ] CLAUDE.md workflow is 21 steps (no conditional commit rows)
- [ ] All 14 workflow-definition files updated consistently (per lessons.md rule)
- [ ] All 6 command templates updated with new step numbers in `**Workflow:**` breadcrumb
- [ ] `CHANGELOG.md` documents the change
- [ ] `tasks/lessons.md` updated with tech-debt.md tracking entry
- [ ] All tests in `tests/verify-workflow.sh` pass

---

## Milestone 5: Pencil Disk Persistence (added via /sk:change)

#### Wave 6 (single task)

- [x] **sk:frontend-design** — Update `skills/sk:frontend-design/SKILL.md`
  - In the Pencil phase (both `--pencil` flag path and the inline "want a Pencil mockup?" prompt):
    - Before opening any Pencil document, derive a filename from the current task:
      - Read `tasks/todo.md`, extract task name from `# TODO — YYYY-MM-DD — <task-name>`
      - Convert to kebab-case (e.g., "Gate Auto-Commit + Tech Debt" → `gate-auto-commit-tech-debt`)
    - Ensure `docs/design/` directory exists in the project root
    - Call `open_document('docs/design/[task-name].pen')` — this creates the `.pen` file on disk at that path from the start
    - All subsequent Pencil design tool calls operate on that file (it's already persisted)
  - Add a note: "The `.pen` file is created at `docs/design/[task-name].pen` before any design work begins, ensuring the design is saved to disk and committable."

---

## Risks/Unknowns

- `assert_not_contains` may not exist in `tests/verify-workflow.sh` — check if it needs to be added as a new test helper
- sk:perf and sk:security-check are currently "report only" — shifting them to "fix and auto-commit" is a significant behavior change; ensure the report generation (perf-findings.md / security-findings.md) is preserved alongside the new fix behavior
- Command templates (breadcrumb lines): need to read each one to find the exact step numbers referenced before updating
