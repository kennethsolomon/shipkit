# Progress Log

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

## Error Log
| Timestamp | Error | Attempt | Resolution |
|-----------|-------|---------|------------|
|           |       | 1       |            |
