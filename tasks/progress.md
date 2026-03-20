# Progress Log

### [2026-03-20] Templates — updated to 21-step workflow
- File: skills/sk:setup-claude/templates/CLAUDE.md.template
- File: skills/sk:setup-claude/templates/tasks/workflow-status.md.template
- Removed 6 conditional commit rows, renumbered to 21 steps

### [2026-03-20] README + DOCUMENTATION + CHANGELOG + lessons — updated for 21-step workflow
- README.md: removed 6 conditional commit rows (old steps 13, 15, 17, 19, 21, 23), renumbered to 21 steps
- .claude/docs/DOCUMENTATION.md: updated step count references (27→21), updated gate step numbers, added tech-debt.md to persistent context files
- CHANGELOG.md: added v3.7.0 section
- tasks/lessons.md: appended tech-debt.md tracking lesson

### [2026-03-20] CLAUDE.md — updated to 21-step workflow
- Removed 6 conditional commit steps (old 13,15,17,19,21,23)
- Renumbered steps: gates now 12-17, Release=21
- Added "Gates own their commits" rule (tracker rule 4)
- Updated Step 22→Step 17 in tracker rules; hard gates now listed as 12,13,14,16,17
- Added tech-debt.md to Project Memory (read list + Never overwrite)
- Updated Bug Fix Flow and Hotfix Flow tables (removed conditional commit rows, added gates-own-commits note)
- Updated Fix & Retest Protocol step list to 12,13,14,15,16,17
- Updated optional steps list to (4,5,8,15,21)

### [2026-03-20] sk:perf — changed to fix+auto-commit+tech-debt
- File: skills/sk:perf/SKILL.md
- Removed "DO NOT fix code" rule
- Added fix+auto-commit+tech-debt logging behavior
- Kept perf-findings.md report generation

### [2026-03-20] sk:e2e — added auto-commit + tech-debt logging
- File: skills/sk:e2e/SKILL.md
- Fix & Retest Protocol: changed to auto-commit
- Added pre-existing issues → tech-debt.md section

### [2026-03-20] sk:review — added auto-commit + tech-debt logging
- File: skills/sk:review/SKILL.md
- Step 0: changed /sk:smart-commit to auto-commit with message `fix(review): simplify pre-pass`
- Step 11: replaced "ask to fix nitpicks" with auto-fix-all + tech-debt logging for out-of-scope files
- Fix & Retest Protocol: auto-commit instead of manual commit (`fix(review): [description]`)

### [2026-03-20] sk:security-check — changed to fix+auto-commit+tech-debt
- File: commands/sk/security-check.md
- Removed "DO NOT fix code" rule
- Added fix+auto-commit+tech-debt logging behavior
- Kept security-findings.md report generation

### [2026-03-20] sk:context + sk:mvp docs + decisions log — COMPLETED
- Branch: `feature/context-mvp-docs-decisions`
- Changes: 3 improvements inspired by vibe-coding-starter-kit
  - A) sk:mvp: new Step 9 generates docs/vision.md, docs/prd.md, docs/tech-design.md
  - B) sk:context: new session initializer skill — reads 7 context files, outputs SESSION BRIEF
  - C) sk:brainstorming: appends ADR entries to docs/decisions.md (cumulative, append-only)
- Tests: 118/118 pass (21 new assertions)
- Files changed: 12 (1 new, 11 modified)
- Review: 0 critical, 0 warning, 3 nitpicks fixed

## Session: 2026-03-19 — todoItems implementation
- server.js: extended parseTodo() with todoItems [{text, done, section}]; STOP_HEADERS set; Milestone header tracking
- dashboard.html: added renderTodoItems() + TASKS panel in renderWorktree(); ✓/→/○ state icons; graceful empty fallback
- tests: 96/96 pass (6 new Milestone 6 assertions all green, first try)

## Requirement Change — 2026-03-19
- What changed: Dashboard to show individual todo checklist items (text + done/pending state) instead of just aggregate counts
- Trigger: User feedback after E2E — wants to see which specific phase/task the AI is currently on
- Scope tier: 2 — New Requirements
- Re-entry point: /sk:write-plan
- Invalidated tasks: none (all existing tasks still valid; this adds new scope on top)

## Session: 2026-03-08
- Started: workflow tracker enhancement
- Summary: Implementing 14-step workflow tracker with strict enforcement

## Work Log
- 2026-03-08 — Created workflow-status.md template (files: setup-claude/templates/tasks/workflow-status.md.template)
- 2026-03-08 — Registered template in apply script (files: setup-claude/scripts/apply_setup_claude.py:302)
- 2026-03-08 — Replaced CLAUDE.md workflow section with strict tracker rules (files: setup-claude/templates/CLAUDE.md.template:34-88)
- 2026-03-08 — Added reset detection step 0 to brainstorm template (files: setup-claude/templates/commands/brainstorm.md.template)
- 2026-03-08 — Added dashboard printing to brainstorm "When Done" section
- 2026-03-08 — Created local tasks/workflow-status.md with current session state

## Session: 2026-03-12
- Started: Fix plugin setup & script paths
- Summary: Replace broken $HOME/.agents paths with $HOME/.claude/plugins/claude-skills, add plugin manifest

## Work Log (2026-03-12)
- Created `.claude-plugin/plugin.json` (plugin manifest)
- Fixed paths in `skills/setup-claude/SKILL.md` (4 occurrences)
- Fixed paths in `skills/setup-claude/templates/commands/re-setup.md.template` (3 occurrences)
- Fixed paths in `skills/setup-claude/templates/commands/finish-feature.md.template` (2 occurrences)
- Fixed paths in `commands/re-setup.md` (3 occurrences)
- Fixed paths in `commands/finish-feature.md` (2 occurrences)
- Fixed paths in `.claude/docs/arch-changelog-guide.md` (1 occurrence)
- Fixed paths in `.claude/docs/DOCUMENTATION.md` (4 script paths + 5 legacy install instruction references)

## Test Results
| Command | Expected | Actual | Status |
|---------|----------|--------|--------|
| grep "workflow-status" apply_setup_claude.py | mapping line | found at line 302 | pass |
| grep "Workflow Tracker" CLAUDE.md.template | rules section | found at line 57 | pass |
| cat workflow-status.md.template | 14-step table | all 14 steps present | pass |
| dry-run from new path | success | success | pass |
| grep .agents/skills (non-tasks) | no matches | no matches | pass |
| python3 validate plugin.json | valid | valid | pass |

## Session: 2026-03-16
- Started: Workflow enhancement — E2E, Fix & Retest Protocol, sk:features, simplify, dep audit, sk:change, /sk: prefix
- Branch: feature/workflow-e2e-fix-retest-sk-prefix

## Work Log (2026-03-16)
- Created `skills/sk:e2e/SKILL.md` — new agent-browser E2E hard gate skill
- Updated `skills/sk:lint/SKILL.md` — dep audit (composer audit, npm audit, pip-audit) + Fix & Retest Protocol
- Updated `skills/sk:test/SKILL.md` — Fix & Retest Protocol
- Updated `commands/sk/security-check.md` — Fix & Retest Protocol (note: security-check lives here, not in skills/)
- Updated `skills/sk:perf/SKILL.md` — Fix & Retest Protocol
- Updated `skills/sk:review/SKILL.md` — simplify pre-step (Step 0) + Fix & Retest Protocol
- Updated `CLAUDE.md` — 27-step workflow, Fix & Retest Protocol, Requirement Change Flow, /sk: prefix on all commands
- Updated `skills/sk:setup-claude/templates/CLAUDE.md.template` — identical changes
- Updated `skills/sk:setup-claude/templates/tasks/workflow-status.md.template` — 27 rows, new hard gate step 22
- Updated `README.md` — 27-step workflow, /sk: prefix, Fix & Retest mention
- Updated `skills/sk:setup-optimizer/SKILL.md` — step count 24→27, new flow line, hard gates 12/14/16/20/22
- Updated `install.sh` — agent-browser mandatory install block
- Updated 5 command templates (brainstorm, write-plan, execute-plan, security-check, finish-feature) — new flow breadcrumb
- Updated `.claude/docs/DOCUMENTATION.md` — 27 steps, sk:e2e in skills list, updated flowchart
- Updated `CHANGELOG.md` — v3.1.0 entry
- Appended `tasks/lessons.md` — /sk: prefix convention + expanded 14-file update list
- Created `tests/verify-workflow.sh` — 52 assertions, all passing

## Test Results (2026-03-16)
| Suite | Result |
|-------|--------|
| tests/verify-workflow.sh | 52/52 PASS |

### 2026-03-16 — Workflow Enhancement — COMPLETED
- Branch: `feature/workflow-e2e-fix-retest-sk-prefix`
- Changes: Expanded workflow 24→27 steps; added sk:e2e hard gate, Fix & Retest Protocol across 6 skills, dep audit in sk:lint, simplify pre-step in sk:review, sk:features sync step, sk:change Requirement Change Flow section, /sk: prefix standardized across 14+ files
- Tests: 52/52 assertions passing (tests/verify-workflow.sh)
- Files changed: 22 (2 commits: 4bb3c36 feat, b0a097c fix)

## Session: 2026-03-16 — sk:seo-audit + Checklist Rollout
- Branch: feature/sk-seo-audit-checklist-format

## Work Log (2026-03-16 — sk:seo-audit)
- Fixed test path: security-check lives at `commands/sk/security-check.md`, not `skills/sk:security-check/SKILL.md`
- Created `skills/sk:seo-audit/SKILL.md` — dual-mode audit, ask-before-fix, checklist output
- Updated `skills/sk:perf/SKILL.md` — checkbox format + resolved column in report
- Updated `skills/sk:accessibility/SKILL.md` — checkbox format + resolved column in report
- Updated `commands/sk/security-check.md` — checkbox format + Passed Checks + resolved column
- Updated `CLAUDE.md` — added sk:seo-audit to commands table
- Updated `README.md` — added sk:seo-audit to commands section
- Updated `.claude/docs/DOCUMENTATION.md` — added sk:seo-audit to skills section
- Updated `install.sh` — added sk:seo-audit echo line
- Appended `tasks/lessons.md` — sk:seo-audit update-all-files lesson

## Test Results (2026-03-16 — sk:seo-audit)
| Suite | Result |
|-------|--------|
| tests/verify-workflow.sh | 74/74 PASS |

### 2026-03-16 — sk:seo-audit + Checklist Format Rollout — COMPLETED
- Branch: `feature/sk-seo-audit-checklist-format`
- Commits: f75f608 (feat), e4751e7 (review fixes)
- All acceptance criteria met; 74/74 tests pass

## Session: 2026-03-19 — sk:dashboard + todoItems TASKS Panel

## Work Log (2026-03-19)
- Created `skills/sk:dashboard/server.js` — zero-dep Node.js HTTP server, `git worktree list` discovery, workflow-status + todo parsing, `/api/status` JSON endpoint
- Created `skills/sk:dashboard/dashboard.html` — Mission Control Kanban UI, swimlanes per worktree, phase timeline, 3s polling
- Created `skills/sk:dashboard/SKILL.md` — skill definition
- Updated `CLAUDE.md`, `README.md`, `.claude/docs/DOCUMENTATION.md`, `install.sh` — added sk:dashboard
- Appended `tasks/lessons.md` — sk:dashboard update-all-files lesson
- Extended `parseTodo()` — added `todoItems: [{text, done, section}]` (Milestone 4+5)
- Fixed critical bug in `parseTodo()` — replaced `collecting=true` flag with `inMilestones`/`pastMilestones` (## Change Log appeared before ## Milestone in todo.md)
- Review fixes: detached HEAD in `discoverWorktrees`, `indexOf` for em dash, swimlane `max-height` 1200→4000px, `assert_api_field` retry loop replacing `sleep 1`

## Test Results (2026-03-19 — sk:dashboard)
| Suite | Result |
|-------|--------|
| tests/verify-workflow.sh | 96/96 PASS |
| E2E (Playwright MCP) | 10/10 PASS |

### 2026-03-19 — sk:dashboard (Read-Only Kanban Board + TASKS Panel) — COMPLETED
- Branch: `feature/sk-dashboard`
- Changes: New `sk:dashboard` skill — zero-dep Node server + single-file HTML Kanban; TASKS panel per swimlane showing individual todo checklist items grouped by milestone; parseTodo bug fix; review fixes for detached HEAD, em dash, max-height, test retry
- Tests: 96/96 assertions passing (tests/verify-workflow.sh); 10/10 E2E scenarios (Playwright MCP)
- Files changed: 13 (5 commits: f07db5f, 03c6e24, 1eb13cc, 99f8d7c, d3637fd)

### [2026-03-20] sk:lint — added auto-commit + tech-debt logging
- File: skills/sk:lint/SKILL.md
- Added auto-commit in Step 6 fix loop
- Added tech-debt.md logging for pre-existing issues (files outside `git diff main..HEAD --name-only`)
- Removed manual commit approval language; all commits in gate are now automatic

### [2026-03-20] sk:test — added auto-commit to fix loop
- File: skills/sk:test/SKILL.md
- Added auto-commit in Step 4 fix loop
- Removed "confirm with user" clause

### [2026-03-20] sk:schema-migrate — added Phase 0 auto-detect
- File: skills/sk:schema-migrate/SKILL.md
- Added Phase 0 that auto-skips when no migration files in branch diff
- No user prompt needed for skip decision

### [2026-03-20] sk:write-plan — added tech-debt.md check
- File: commands/sk/write-plan.md
- Added tasks/tech-debt.md to Step 2 read list
- Added ask logic for unresolved debt items before plan approval

### [2026-03-20] sk:update-task — added Resolved: marking for tech-debt
- File: commands/sk/update-task.md
- Added Step 2.5 to mark matched tech-debt entries as Resolved: on task completion

### [2026-03-20] sk:context — added tech-debt.md integration
- File: skills/sk:context/SKILL.md
- Added tasks/tech-debt.md as file #8 in read table
- Added Tech Debt field to session brief output
- Added edge case and field rule for tech-debt.md

### [2026-03-20] sk:setup-optimizer — updated to 21-step workflow
- File: skills/sk:setup-optimizer/SKILL.md
- Changed 27→21 step count references
- Updated hard gate step numbers

### [2026-03-20] Gate Auto-Commit + Tech Debt Logging — COMPLETED
- Branch: `feature/gate-auto-commit-tech-debt`
- Changes: Gate auto-commit (6 skills), tech-debt.md logging lifecycle, 27→21 step workflow, sk:schema-migrate auto-detect, Pencil disk persistence; DOCUMENTATION.md workflow table fix found during sk:review
- Tests: 143/143 pass (tests/verify-workflow.sh)
- Files changed: 33 across 3 commits (feat + 2 fix)
- Gates: lint clean, 143 tests pass, 0 security findings, 0 perf findings, 0 review issues, 143 E2E pass

### [2026-03-20] sk:frontend-design — Pencil disk persistence
- File: skills/sk:frontend-design/SKILL.md
- Step 1 of Pencil phase rewritten: reads tasks/todo.md for task name, converts to kebab-case, always calls open_document('docs/design/[task-name].pen') to persist to disk
- Removed open_document('new') — file is now always written to docs/design/ from the start
- Tests: 2 new assertions in tests/verify-workflow.sh — 143/143 pass

### [2026-03-20] Command templates — updated workflow breadcrumbs to 21 steps
- Updated Workflow: breadcrumb in all 6 command templates
- Note: release.md.template does not exist in skills/sk:setup-claude/templates/commands/ (only in node_modules); 5 local templates updated

## Error Log
| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|
|           |       | 1       |            |
