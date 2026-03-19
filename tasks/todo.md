# TODO — 2026-03-19 — New Skill: sk:dashboard (Read-Only Kanban Board)

## Change Log
- [2026-03-19] Add individual todo item display to dashboard — re-entered at /sk:write-plan

## Goal

Create `/sk:dashboard` — a zero-dependency Node.js server that serves a read-only Kanban board showing workflow status across all git worktrees. Markdown files are the source of truth; the UI polls and displays.

## Constraints (from lessons.md)

- All commands must use `/sk:` prefix
- Never overwrite `tasks/lessons.md` — append only
- Any new skill added to install.sh echo block
- New skill docs must be added to: CLAUDE.md commands table, README.md, DOCUMENTATION.md
- `tasks/lessons.md` must be updated to include sk:dashboard in the "update ALL files" list

---

## Milestone 1: Tests (write failing tests first — TDD red phase)

#### Wave 1 (first — tests must exist before implementation)

- [x] Update `tests/verify-workflow.sh` — add assertions for sk:dashboard
  - `assert_file_exists` — `skills/sk:dashboard/SKILL.md` exists
  - `assert_file_exists` — `skills/sk:dashboard/server.js` exists
  - `assert_file_exists` — `skills/sk:dashboard/dashboard.html` exists
  - `assert_contains` — `server.js` contains `"http"` (built-in module)
  - `assert_contains` — `server.js` contains `"worktree"` (git worktree discovery)
  - `assert_contains` — `server.js` contains `"workflow-status.md"` (reads status file)
  - `assert_contains` — `server.js` contains `"/api/status"` (JSON API endpoint)
  - `assert_contains` — `dashboard.html` contains `"SHIPKIT"` (header title)
  - `assert_contains` — `dashboard.html` contains `"fetch"` (polling mechanism)
  - `assert_contains` — `dashboard.html` contains `"JetBrains Mono"` or `"Orbitron"` (design fonts)
  - `assert_contains` — `SKILL.md` contains `"sk:dashboard"` (skill name)
  - `assert_contains` — `SKILL.md` contains `"server.js"` (references server)
  - `assert_contains` — `CLAUDE.md` contains `"sk:dashboard"` (commands table)
  - `assert_contains` — `README.md` contains `"sk:dashboard"`
  - `assert_contains` — `.claude/docs/DOCUMENTATION.md` contains `"sk:dashboard"`
  - `assert_contains` — `install.sh` contains `"sk:dashboard"`

---

## Milestone 2: Core Implementation (server + UI + skill definition)

#### Wave 2a (parallel — all three files are independent)

- [x] Create `skills/sk:dashboard/server.js` — Node.js HTTP server
  - Uses only built-in modules: `http`, `fs`, `path`, `child_process`
  - `git worktree list` to discover all worktrees
  - Parse `tasks/workflow-status.md` from each worktree (table → JSON)
  - Parse `tasks/todo.md` from each worktree (goal + checkbox counts)
  - `GET /api/status` — returns JSON array of worktree status objects
  - `GET /` — serves `dashboard.html` from same directory
  - Default port 3333, configurable via `--port` flag or `PORT` env var
  - CORS headers for local development
  - Graceful error handling: missing files → empty/default state, not crash

- [x] Create `skills/sk:dashboard/dashboard.html` — single-file Kanban UI
  - All CSS in `<style>`, all JS in `<script>` — no external files except Google Fonts CDN
  - Mission Control aesthetic per design (dark theme, JetBrains Mono + Orbitron)
  - Color palette: `#080C14` bg, `#111827` surface, `#10B981` done, `#3B82F6` active, `#334155` pending, `#F59E0B` skipped, `#EF4444` hard gate accent
  - Layout: header bar → scrollable content area → footer bar
  - Each worktree = collapsible swimlane section
  - Swimlane header: branch name, task name, progress fraction + percentage
  - Phase timeline: 27 cells, color-coded by status, hard gates with red bottom border, active step with blue glow
  - Active step card: prominent display with blue left border
  - Status columns: Done / Skipped / Not Yet with step lists
  - Progress bar per swimlane (gradient fill)
  - Legend row: done / next / hard gate / skipped / not yet
  - Auto-polls `/api/status` every 3 seconds, DOM updates in place (no reload)
  - Collapsed state: header + progress bar only; expanded shows full timeline + columns
  - Footer: worktree count, last refresh timestamp, port number
  - Responsive at >=768px (half-screen beside terminal)

- [x] Create `skills/sk:dashboard/SKILL.md` — skill definition
  - Frontmatter: `name: sk:dashboard`, description
  - Purpose: Read-only workflow dashboard served on localhost
  - Instructions: how to start (`node server.js`), what it shows, how to stop
  - Notes: does not modify any files, read-only, auto-refreshes
  - Model Routing section (sonnet for all profiles — lightweight skill)

---

## Milestone 3: Documentation Updates (parallel — all independent)

#### Wave 3 (parallel — all documentation files)

- [x] Update `CLAUDE.md` — add `/sk:dashboard` to commands table
  - Add row: `| \`/sk:dashboard\` | Read-only workflow Kanban board — localhost server, multi-worktree |`
  - Place in the commands table near other utility commands

- [x] Update `README.md` — add `sk:dashboard` to commands section
  - Same row as CLAUDE.md in the commands/skills table

- [x] Update `.claude/docs/DOCUMENTATION.md` — add `sk:dashboard` to skills section
  - Add subsection entry: purpose, how to start, what it shows

- [x] Update `install.sh` — add `sk:dashboard` to workflow commands echo block
  - Add `echo "  /sk:dashboard    — Read-only workflow Kanban board (localhost)"` in the commands listing

- [x] Append `tasks/lessons.md` — update "update ALL files" list
  - Append new entry: "[2026-03-19] sk:dashboard — update its docs when the skill changes"
  - Note the 5 files: SKILL.md, CLAUDE.md, README.md, DOCUMENTATION.md, install.sh

---

## Milestone 4: Tests — Todo Item Display (TDD red phase)

#### Wave 4a (parallel — all are independent test additions)

- [x] Update `tests/verify-workflow.sh` — add assertions for todoItems feature
  - `assert_contains` — `server.js` contains `"todoItems"` (new API field)
  - `assert_contains` — `server.js` contains `"section"` (section label per item)
  - `assert_contains` — `dashboard.html` contains `"todoItems"` (reads new field)
  - `assert_contains` — `dashboard.html` contains `"TASKS"` (section heading in UI)
  - `assert_contains` — `dashboard.html` contains `"todo-item"` (CSS class for items)
  - API smoke test: start server, hit `/api/status`, verify `todoItems` is an array in the JSON response

---

## Milestone 5: Implementation — Todo Item Display (TDD green phase)

#### Wave 5a (parallel — server.js and dashboard.html are independent)

- [x] Update `skills/sk:dashboard/server.js` — extend `parseTodo()`
  - New return shape: `{ taskName, todosDone, todosTotal, todoItems }`
  - `todoItems`: array of `{ text: string, done: boolean, section: string }`
  - Parse `## Milestone N:` headers → set current `section` label
  - `- [x] ...` lines → `{ text, done: true, section }`
  - `- [ ] ...` lines → `{ text, done: false, section }`
  - Stop collecting items at `## Verification`, `## Acceptance Criteria`, `## Risks`, `## Change Log` headers
  - Strip backtick formatting from item text
  - Empty `todoItems: []` on ENOENT (same graceful-fallback pattern as existing code)

- [x] Update `skills/sk:dashboard/dashboard.html` — add Tasks panel to each swimlane
  - New "TASKS" section rendered below the step-columns area within each swimlane body
  - Items grouped by `section` label (milestone name as a divider heading)
  - Three item states — use icon prefix:
    - `✓` done: muted green text, no highlight
    - `→` current (first item where `done === false`): blue text, subtle left-border highlight
    - `○` pending: gray text
  - Section divider: small uppercase label between milestone groups
  - If `todoItems` is empty or missing → render nothing (graceful fallback)
  - Change detection already covers this (existing `JSON.stringify` comparison)

---

## Verification

```bash
# Confirm new skill files exist
ls skills/sk:dashboard/SKILL.md
ls skills/sk:dashboard/server.js
ls skills/sk:dashboard/dashboard.html

# Confirm server uses built-in modules only
grep "require('http')" skills/sk:dashboard/server.js
grep "worktree" skills/sk:dashboard/server.js
grep "/api/status" skills/sk:dashboard/server.js

# Confirm todoItems in server + dashboard
grep "todoItems" skills/sk:dashboard/server.js
grep "todoItems" skills/sk:dashboard/dashboard.html
grep "TASKS" skills/sk:dashboard/dashboard.html

# Confirm dashboard has key UI elements
grep "SHIPKIT" skills/sk:dashboard/dashboard.html
grep "fetch" skills/sk:dashboard/dashboard.html

# Confirm sk:dashboard in all documentation files
grep "sk:dashboard" CLAUDE.md
grep "sk:dashboard" README.md
grep "sk:dashboard" .claude/docs/DOCUMENTATION.md
grep "sk:dashboard" install.sh

# Server smoke test — verify todoItems in API response
node skills/sk:dashboard/server.js &
SERVER_PID=$!
sleep 1
curl -s http://localhost:3333/api/status | python3 -c "import sys,json; d=json.load(sys.stdin); print('todoItems ok' if isinstance(d[0]['todoItems'], list) else 'FAIL')"
kill $SERVER_PID

# Run full test suite
bash tests/verify-workflow.sh
```

## Acceptance Criteria

- [x] `skills/sk:dashboard/server.js` exists, uses only Node.js built-in modules
- [x] `skills/sk:dashboard/dashboard.html` exists with Mission Control UI
- [x] `skills/sk:dashboard/SKILL.md` exists with skill definition
- [x] Server starts on port 3333 and responds to `/api/status` with valid JSON
- [x] Server discovers worktrees via `git worktree list`
- [x] Server parses `tasks/workflow-status.md` table into step objects
- [x] Server parses `tasks/todo.md` for task name and checkbox counts
- [x] **[NEW]** `/api/status` response includes `todoItems: [{ text, done, section }]` per worktree
- [x] **[NEW]** `todoItems` grouped by `## Milestone` sections from `todo.md`
- [x] **[NEW]** Dashboard renders a TASKS panel per swimlane showing individual checklist items
- [x] **[NEW]** Current item (first undone) highlighted in blue; done items muted; pending items gray
- [x] Dashboard renders swimlanes per worktree with phase timeline
- [x] Dashboard auto-polls every 3 seconds without page reload
- [x] Hard gate steps (12, 14, 16, 20, 22) visually distinguished
- [x] Active step (`>> next <<`) highlighted with blue glow
- [x] Collapsed/expanded swimlane toggle works
- [x] `sk:dashboard` present in CLAUDE.md, README.md, DOCUMENTATION.md, install.sh
- [x] `tasks/lessons.md` updated (appended, not overwritten)
- [x] All tests in `tests/verify-workflow.sh` pass

## Risks/Unknowns

- Worktree paths may contain spaces — ensure server handles quoted paths from `git worktree list`
- If no `tasks/workflow-status.md` exists in a worktree, server should return empty/default state (not crash)
- Google Fonts CDN requires internet connection — dashboard degrades to system monospace font if offline (acceptable)
