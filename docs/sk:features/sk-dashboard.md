# /sk:dashboard

> **Status:** Shipped (v3.5.0 — 2026-03-19)
> **Type:** Developer Tool (standalone — not a numbered workflow step)
> **Command:** `/sk:dashboard` (or run directly: `node skills/sk:dashboard/server.js`)
> **Skill file:** `skills/sk:dashboard/SKILL.md`

---

## Overview

Read-only workflow Kanban board served by a zero-dependency Node.js HTTP server. Visualizes workflow progress across all git worktrees in real time. Use it any time you want a visual overview of where each worktree stands — which steps are done, what's next, and what individual tasks the AI is currently working on.

Start: `node skills/sk:dashboard/server.js` → `http://localhost:3333`

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/workflow-status.md` | Each worktree's task directory | No — empty state if missing |
| `tasks/todo.md` | Each worktree's task directory | No — empty state if missing |
| `git worktree list` | Git CLI (child_process) | Yes — falls back to `{path: cwd, branch: 'unknown'}` on error |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Dashboard UI | `http://localhost:PORT/` | Served from `skills/sk:dashboard/dashboard.html` |
| Status JSON | `http://localhost:PORT/api/status` | Array of worktree status objects, auto-refreshed |

### `/api/status` Response Shape

```json
[
  {
    "path": "/absolute/path/to/worktree",
    "branch": "feature/sk-dashboard",
    "taskName": "New Skill: sk:dashboard (Read-Only Kanban Board)",
    "todosDone": 12,
    "todosTotal": 19,
    "todoItems": [
      { "text": "Update tests/verify-workflow.sh", "done": true, "section": "Milestone 1: Tests" },
      { "text": "Create skills/sk:dashboard/server.js", "done": true, "section": "Milestone 2: Core Implementation" }
    ],
    "currentStep": 22,
    "totalDone": 14,
    "totalSkipped": 7,
    "totalSteps": 27,
    "steps": [
      {
        "number": 1,
        "name": "Read Todo",
        "command": "/sk:brainstorm",
        "status": "done",
        "notes": "tasks/findings.md and lessons.md read",
        "isHardGate": false,
        "isOptional": false
      }
    ]
  }
]
```

---

## Business Logic

### Server (`server.js`)

1. **Start HTTP server** on `PORT` (default 3333, override via `--port` arg or `PORT` env var).
2. **`GET /`** — reads and serves `dashboard.html` from `__dirname`. Returns 404 if file missing.
3. **`GET /api/status`** — calls `buildStatus()`, returns JSON array. Returns `{"error": "Internal server error"}` (no stack trace) on failure.
4. **`discoverWorktrees()`** — runs `execSync("git worktree list")`, parses each line:
   - Branched worktree: `^path  hash  [branch]$` → `{path, branch}`
   - Detached HEAD: `^path  hash  (HEAD detached at ...)$` → `{path, branch: "(detached)"}`
   - Falls back to `[{path: cwd, branch: "unknown"}]` on `execSync` error.
5. **`parseWorkflowStatus(worktreePath)`** — reads `tasks/workflow-status.md`, parses markdown table rows into step objects. Returns `[]` on ENOENT.
6. **`parseTodo(worktreePath)`** — reads `tasks/todo.md`:
   - Extracts `taskName` from `# TODO — date — <name>` header (splits on first em dash `—`)
   - Counts `[x]` / `[ ]` checkboxes for `todosDone` / `todosTotal`
   - Collects `todoItems` only from `## Milestone` sections — starts collecting at first `## Milestone` header (`inMilestones = true`), stops at first `STOP_HEADERS` match after milestones (`pastMilestones = true`). STOP_HEADERS: `Verification`, `Acceptance Criteria`, `Risks`, `Change Log`, `Summary`.
   - Item text stripped of `**` and backticks via `stripMd()`.
   - Returns `{taskName: "", todosDone: 0, todosTotal: 0, todoItems: []}` on ENOENT.

### Dashboard (`dashboard.html`)

1. On load, calls `fetchStatus()` immediately, then polls every 3 seconds.
2. **Change detection**: compares `JSON.stringify(data)` against `lastResponseJson` — skips re-render if identical.
3. **`renderWorktree(wt)`** — builds swimlane HTML:
   - Header: branch name + task name + progress bar (done+skipped / total steps, %)
   - Phase timeline: numbered step dots colored by status (done=green, next=blue pulse, skipped=amber, gate=red outline, partial=purple, not-yet=gray)
   - Active step card: highlighted display of current step number + command
   - Kanban columns: Done (14), Next (1), Hard Gate indicator, Skipped, Not Yet
   - **TASKS panel**: rendered by `renderTodoItems(wt.todoItems)` — see below
4. **`renderTodoItems(todoItems)`** — renders TASKS panel:
   - Groups items by `section` with divider labels
   - First `done: false` item = "current" (→ blue, `todo-current` class)
   - All `done: true` items = ✓ muted green (`todo-done`)
   - Remaining `done: false` items = ○ gray (`todo-pending`)
   - Returns `''` (renders nothing) if `todoItems` is empty or missing
5. **`esc(s)`** — HTML escapes all dynamic content via regex (`&`, `<`, `>`, `"`)
6. Swimlane expand/collapse toggle via click on `.swimlane-header`

---

## Hard Rules

- **Read-only** — server never writes to any file
- **No external dependencies** — only Node.js built-in modules (`http`, `fs`, `path`, `child_process`)
- **No stack traces in responses** — errors return generic `"Internal server error"` message
- **All dynamic content escaped** — `esc()` applied to every user-data string rendered in HTML
- **Graceful degradation** — missing files return empty/default state, never crash

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| `tasks/workflow-status.md` missing | Returns `steps: []`, `currentStep: 0`, `totalDone: 0` |
| `tasks/todo.md` missing | Returns `taskName: ""`, `todosDone: 0`, `todosTotal: 0`, `todoItems: []` |
| No `## Milestone` headers in todo.md | `todoItems: []` (empty — TASKS panel renders nothing) |
| `## Change Log` appears before `## Milestone` | Handled correctly — `inMilestones` flag stays `false` until first `## Milestone` |
| Detached HEAD worktree | Shown with branch label `(HEAD detached at abc1234)` |
| Port already in use | Node exits with `EADDRINUSE` error to stderr; no crash loop |
| Google Fonts CDN unavailable | Dashboard degrades to system monospace font (offline-safe) |
| Single worktree (no linked worktrees) | Shows one swimlane — normal behavior |
| `todoItems` is empty | `renderTodoItems()` returns `''` — TASKS section not shown |
| All todo items done | All items show ✓ (done); no current item highlighted (none in → state) |

---

## Error States

| Condition | Response |
|-----------|----------|
| `/api/status` throws | HTTP 500 `{"error": "Internal server error"}` |
| `dashboard.html` file missing | HTTP 404 `"dashboard.html not found"` |
| Any other route | HTTP 404 `"Not found"` |
| `git worktree list` fails | Falls back to `[{path: cwd, branch: "unknown"}]` |
| File read error (not ENOENT) | Logs to stderr, returns empty state |

---

## UI/UX Behavior

### Dashboard Layout

```
┌─ SHIPKIT MISSION CONTROL ──────────── LIVE  ↻ 3s  HH:MM ─┐
│                                                             │
│ ▼ feature/sk-dashboard  •  Task Name              21/27 78%│
│   [phase timeline: 1 2 3 4 5 6 7 8 9 10 11 ...]           │
│   [active step card: 22 E2E /sk:e2e]                       │
│   Done(14) │ Next(1) │ Skipped(7) │ Not Yet(6)             │
│   ─── TASKS ────────────────────────────────────────────── │
│   Milestone 1: Tests                                        │
│   ✓ Update verify-workflow.sh                              │
│   Milestone 2: Core Implementation                         │
│   ✓ Create server.js                                       │
│   → Implement TASKS panel  ← current (blue)                │
│   ○ Update documentation   ← pending (gray)                │
└─────────────────────────────────────────────────────────── ┘
│ 1 worktree · Last refresh: 2s ago · Port 3333              │
```

### Step Status Colors

| Status | Color | Class |
|--------|-------|-------|
| `done` | Green | `step-done` |
| `>> next <<` | Blue pulse | `step-next` |
| `skipped` | Amber | `step-skipped` |
| `partial` | Purple | `step-partial` |
| hard gate + not done | Red outline | `step-gate` |
| `not yet` | Gray | `step-pending` |

### Todo Item States

| State | Icon | Color | Condition |
|-------|------|-------|-----------|
| Done | ✓ | Muted green | `done: true` |
| Current | → | Blue + left border | First item where `done: false` |
| Pending | ○ | Gray | Remaining `done: false` items |

### When Done (CLI)

```
ShipKit Dashboard running at http://localhost:3333
```

---

## Platform Notes

CLI tool — no mobile platform. Developer-only, localhost-only, read-only.

`Access-Control-Allow-Origin: *` is set on all responses. Acceptable because the server has no auth and no mutations; CORS is not an attack surface for a localhost-only dev tool.

---

## Related Docs

- `skills/sk:dashboard/SKILL.md` — skill definition and model routing
- `skills/sk:dashboard/server.js` — HTTP server implementation (~200 lines)
- `skills/sk:dashboard/dashboard.html` — single-file UI (~940 lines)
- `tasks/workflow-status.md` — data source for step statuses
- `tasks/todo.md` — data source for task name, counts, and `todoItems`
- `.claude/docs/architectural_change_log/2026-03-19-subsystem-refactor.md` — architecture decision record
