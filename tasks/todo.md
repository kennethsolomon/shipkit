# TODO — 2026-03-19 — New Skill: sk:dashboard (Read-Only Kanban Board)

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

# Confirm dashboard has key UI elements
grep "SHIPKIT" skills/sk:dashboard/dashboard.html
grep "fetch" skills/sk:dashboard/dashboard.html

# Confirm sk:dashboard in all documentation files
grep "sk:dashboard" CLAUDE.md
grep "sk:dashboard" README.md
grep "sk:dashboard" .claude/docs/DOCUMENTATION.md
grep "sk:dashboard" install.sh

# Confirm /sk: prefix used (no bare /dashboard reference)
grep -r '`/dashboard`' CLAUDE.md README.md .claude/docs/DOCUMENTATION.md

# Server smoke test
node skills/sk:dashboard/server.js &
SERVER_PID=$!
sleep 1
curl -s http://localhost:3333/api/status | head -c 200
curl -s http://localhost:3333/ | head -c 200
kill $SERVER_PID

# Run full test suite
bash tests/verify-workflow.sh
```

## Acceptance Criteria

- [ ] `skills/sk:dashboard/server.js` exists, uses only Node.js built-in modules
- [ ] `skills/sk:dashboard/dashboard.html` exists with Mission Control UI
- [ ] `skills/sk:dashboard/SKILL.md` exists with skill definition
- [ ] Server starts on port 3333 and responds to `/api/status` with valid JSON
- [ ] Server discovers worktrees via `git worktree list`
- [ ] Server parses `tasks/workflow-status.md` table into step objects
- [ ] Server parses `tasks/todo.md` for task name and checkbox counts
- [ ] Dashboard renders swimlanes per worktree with phase timeline
- [ ] Dashboard auto-polls every 3 seconds without page reload
- [ ] Hard gate steps (12, 14, 16, 20, 22) visually distinguished
- [ ] Active step (`>> next <<`) highlighted with blue glow
- [ ] Collapsed/expanded swimlane toggle works
- [ ] `sk:dashboard` present in CLAUDE.md, README.md, DOCUMENTATION.md, install.sh
- [ ] `tasks/lessons.md` updated (appended, not overwritten)
- [ ] All tests in `tests/verify-workflow.sh` pass

## Risks/Unknowns

- Worktree paths may contain spaces — ensure server handles quoted paths from `git worktree list`
- If no `tasks/workflow-status.md` exists in a worktree, server should return empty/default state (not crash)
- Google Fonts CDN requires internet connection — dashboard degrades to system monospace font if offline (acceptable)
