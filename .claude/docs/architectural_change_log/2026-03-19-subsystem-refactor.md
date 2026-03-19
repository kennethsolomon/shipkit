# sk:dashboard — New Skill Subsystem (March 19, 2026)

## Summary

Added `sk:dashboard` — a new zero-dependency Node.js skill that introduces a live Kanban board server for monitoring workflow status across all git worktrees. Extends the `parseTodo()` data model with per-item todo tracking.

## Type of Architectural Change

**New Subsystem**

## What Changed

**New Subsystem: `skills/sk:dashboard/`**
- `server.js` — zero-dependency HTTP server (Node.js built-ins only: `http`, `fs`, `path`, `child_process`). Provides two routes: `GET /` (serves dashboard.html) and `GET /api/status` (JSON status for all worktrees).
- `dashboard.html` — single-file self-contained UI. No build step, no npm dependencies. Polls `/api/status` every 3 seconds via `fetch`.
- `SKILL.md` — skill definition for `/sk:dashboard`

**Extended Data Model:**
- `parseTodo()` now returns `todoItems: [{text, done, section}]` in addition to existing `taskName`, `todosDone`, `todosTotal`. Items collected only from `## Milestone` sections; stops at `## Verification` / `## Acceptance Criteria` / `## Risks` headers.

**Statistics:**
- Lines added: 1696
- Lines removed: 287 (tasks/findings.md + tasks/todo.md restructuring)
- Files modified: 13

## Impact

- New optional developer tool — run on demand, no auto-start
- No changes to existing skill behavior or workflow steps
- Extends `/api/status` response shape with `todoItems` array (additive, non-breaking)

## Before & After

**Before:** No live dashboard. Workflow status only visible by reading `tasks/workflow-status.md` directly.

**After:** `node skills/sk:dashboard/server.js` → `http://localhost:3333` shows all worktrees as swimlanes with phase timeline, Kanban columns, progress bar, and TASKS panel with individual todo item states.

## Affected Components

- `skills/sk:dashboard/` — new subsystem (self-contained)
- `CLAUDE.md`, `README.md`, `.claude/docs/DOCUMENTATION.md`, `install.sh` — documentation references added
- `tasks/lessons.md` — sk:dashboard added to "update ALL files" list

## Migration/Compatibility

Backward compatibility confirmed ✓ — additive only. No existing skill behavior changed.

## Verification

- [x] All affected code paths tested (96/96 assertions in tests/verify-workflow.sh)
- [x] Related documentation updated (CLAUDE.md, README.md, DOCUMENTATION.md, install.sh)
- [x] No breaking changes
- [x] Dependent systems verified (10/10 E2E scenarios via Playwright MCP)
