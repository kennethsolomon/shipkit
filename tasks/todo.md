# TODO — 2026-03-08 — Workflow Tracker Enhancement

## Goal
Add a persistent workflow tracker (`tasks/workflow-status.md`) with strict step ordering, status dashboard after every command, and zero-tolerance loops for security-check and review.

## Plan

### 1. Create workflow-status.md template
- [x] Create `setup-claude/templates/tasks/workflow-status.md.template` with the 14-step table (columns: #, Step, Status, Notes)
- [x] All steps start as `not yet`, step 1 marked `>> next <<`
- [x] Include header explaining the file's purpose and reset behavior

### 2. Register template in apply script
- [x] Add `workflow-status.md.template` → `tasks/workflow-status.md` mapping in `apply_setup_claude.py` (mode: `"missing"`)

### 3. Update CLAUDE.md template with strict workflow rules
- [x] Replace the "Recommended Workflow" section in `setup-claude/templates/CLAUDE.md.template` with:
  - New 14-step flow diagram
  - New step table with Type column (required/optional/conditional) and Loop column
  - **Workflow Tracker Rules** subsection:
    - Every slash command MUST read `tasks/workflow-status.md` at start
    - Every slash command MUST update the tracker and print the dashboard at end
    - Dashboard format: table with `>> next <<` indicator
    - Optional steps (frontend-design, debug, release): ask to skip, record reason
    - Conditional commits (7, 10, 12): auto-skip with reason if no changes
    - `/security-check` loop: must reach 0 issues (all severities) — fix → commit → re-run
    - `/review` loop: must reach 0 issues (including nitpicks) — fix → commit → re-run
    - Attempt counting for looped steps
    - Steps cannot run out of order without explicit skip confirmation
  - **Tracker Reset Rules** subsection:
    - `/brainstorm` checks if tracker has any `done`/`skipped` steps — if yes, asks "New feature? Reset tracker?"
    - User can manually request a reset at any time

### 4. Update brainstorm template with reset detection
- [x] Add step 0 to `setup-claude/templates/commands/brainstorm.md.template`:
  - Read `tasks/workflow-status.md`
  - If any steps are `done` or `skipped`, ask user: "Existing workflow detected. Start fresh? (reset tracker)"
  - If yes, reset all steps to `not yet`, mark step 1 as `>> next <<`
  - If tracker doesn't exist, create it from the template format

### 5. Create the local workflow-status.md for this repo
- [x] Create `tasks/workflow-status.md` for the current project (so we can use it immediately)

## Verification
- `grep "workflow-status" setup-claude/scripts/apply_setup_claude.py` → shows the mapping line
- `cat setup-claude/templates/tasks/workflow-status.md.template` → shows 14-step table
- `grep "Workflow Tracker" setup-claude/templates/CLAUDE.md.template` → shows new rules section
- `grep "workflow-status" setup-claude/templates/commands/brainstorm.md.template` → shows reset detection

## Acceptance Criteria
- [ ] `tasks/workflow-status.md` template exists with all 14 steps
- [ ] Template registered in apply script as "missing" mode
- [ ] CLAUDE.md template has strict tracker rules (read/update/print dashboard)
- [ ] CLAUDE.md template specifies zero-tolerance for security-check and review loops
- [ ] Brainstorm template includes reset detection as step 0
- [ ] Local `tasks/workflow-status.md` created for this repo
- [ ] Running `/re-setup` on a new project would create the tracker file

## Risks / Unknowns
- None — all changes are to templates and one script mapping line

## Results
- (fill after execution)

## Errors
| Error | Attempt | Resolution |
|-------|---------|------------|
|       | 1       |            |
