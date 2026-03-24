---
name: sk:dashboard
description: Read-only workflow Kanban board — localhost server showing workflow status across git worktrees
license: Complete terms in LICENSE.txt
---

# /sk:dashboard

## Purpose

Read-only Kanban board that visualizes workflow progress across all git worktrees in a project. Runs as a standalone localhost server — no workflow integration required. Use it anytime you want a visual overview of where each worktree stands in the workflow.

## How to Start

```bash
node skills/sk:dashboard/server.js
```

Opens on `http://localhost:3333`. Stop with `Ctrl+C`.

Override the port:

```bash
node skills/sk:dashboard/server.js --port 4000
# or
PORT=4000 node skills/sk:dashboard/server.js
```

## What It Shows

- **Swimlanes per worktree** — one row per worktree discovered via `git worktree list`
- **Phase timeline** — workflow steps laid out as columns (Explore, Design, Plan, Branch, Tests+Implement, Commit, Gates, Finalize)
- **Progress bars** — percentage of todo.md checkboxes completed per worktree
- **Current task** — the active task name from `tasks/todo.md`

## Architecture

Zero-dependency Node.js server. Uses only built-in modules (`http`, `fs`, `path`, `child_process`).

- `server.js` serves the dashboard HTML and exposes `/api/status`
- `/api/status` reads `tasks/todo.md` from each worktree, parses checkbox progress, and returns JSON
- `dashboard.html` is a single-file UI (HTML + embedded CSS + JS) that polls `/api/status` every 3 seconds
- Worktree discovery via `git worktree list`

## Key Details

- Read-only — does not modify any files
- Auto-discovers worktrees via `git worktree list`
- Graceful degradation: missing files show empty state, offline falls back to system fonts
- Default port 3333, configurable via `--port` flag or `PORT` env var
- Uses only Node.js built-in modules (http, fs, path, child_process)

## Files

- `server.js` — Node.js HTTP server (~150 lines)
- `dashboard.html` — Single-file Kanban UI (HTML + embedded CSS + JS)

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:dashboard"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |
