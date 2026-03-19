# Findings — 2026-03-19 — sk:dashboard: Read-Only Kanban Board

## Problem Statement

When working on multiple features in parallel (especially with git worktrees), there's no way to visualize the workflow status across all active branches. The `tasks/workflow-status.md` file only shows one task's progress, and you have to manually read each worktree's file to understand overall state. A read-only Kanban board served on localhost would provide at-a-glance visibility into all active workflows.

## Key Decisions Made

- **Type:** Standalone optional command (`/sk:dashboard`) — not a numbered workflow step. Invokable at any time.
- **Architecture:** Zero-dependency Node.js server using built-in `http` + `fs` modules. No Express, no framework.
- **Frontend:** Single self-contained HTML file with embedded CSS/JS. Vanilla — no React/Vue/Svelte.
- **Data source:** Reads `tasks/workflow-status.md` and `tasks/todo.md` from main repo + all git worktrees. Markdown is the source of truth.
- **Interaction:** Read-only. No editing, no drag-and-drop. Claude updates the markdown; the UI just displays it.
- **Live updates:** Auto-refresh via polling (every 3-5 seconds).
- **Worktree support:** Uses `git worktree list` to discover all worktrees, reads `tasks/` from each.
- **Precedent:** Follows the pattern set by `skills/sk:skill-creator/eval-viewer/viewer.html` — embedded HTML viewer in a skill directory.

## Chosen Approach: Approach A — Zero-Dep Node Server + Single HTML File

### What it does

**Server (Node.js built-in `http` + `fs`):**
- Runs `git worktree list` to discover all active worktrees
- For each worktree, reads and parses:
  - `tasks/workflow-status.md` — 27-step table → step statuses
  - `tasks/todo.md` — task name, milestones, checkbox completion
- Exposes a JSON API endpoint (`/api/status`) returning parsed data for all worktrees
- Serves the single HTML dashboard file
- Listens on a configurable port (default: 3333)

**Dashboard (single HTML file, embedded CSS/JS):**
- Kanban board layout with columns: **Not Started** | **In Progress** | **Done** | **Skipped**
- Each worktree/branch is a **swimlane** (horizontal row across columns)
- Swimlane header shows: branch name, task name (from todo.md Goal), overall progress (e.g., "18/27 steps")
- Each workflow step is a **card** in the appropriate column
- Cards show: step number, step name, command, notes
- Hard gate steps (12, 14, 16, 20, 22) visually distinguished (border/badge)
- `>> next <<` step highlighted prominently
- Auto-polls `/api/status` every 3-5 seconds for live updates
- No page reload needed — DOM updates in place

### Data model

```
Worktree {
  path: string           // filesystem path
  branch: string         // git branch name
  taskName: string       // from todo.md ## Goal
  currentStep: number    // step with >> next <<
  totalDone: number      // count of "done" steps
  totalSkipped: number   // count of "skipped" steps
  steps: Step[]          // all 27 steps
  todoItems: TodoItem[]  // individual checklist items from todo.md [NEW]
}

TodoItem {
  text: string           // item text (backtick-stripped)
  done: boolean          // true = [x], false = [ ]
  section: string        // nearest ## Milestone N: header above this item
}

Step {
  number: number         // 1-27
  name: string           // "Lint + Dep Audit"
  command: string        // "/sk:lint"
  status: string         // "not yet" | ">> next <<" | "done" | "skipped" | "partial"
  notes: string          // free text
  isHardGate: boolean    // steps 12, 14, 16, 20, 22
  isOptional: boolean    // steps 4, 5, 8, 18, 27
}
```

### Markdown parsing rules

**workflow-status.md:**
- Skip lines until `| # |` header row
- Skip separator row (`|---|`)
- Each subsequent `|`-delimited row → split into 4 columns
- Strip whitespace, bold markers (`**`), backtick markers
- Extract command from parentheses in Step column

**todo.md:**
- Task name: first `# TODO —` line, take everything after the last `—`
- Checkboxes: count `- [x]` (done) vs `- [ ]` (pending)
- Milestones: `## Milestone N:` headers

### File structure

```
skills/sk:dashboard/
├── SKILL.md          # Skill definition (instructions for Claude)
├── server.js         # Node.js HTTP server (~100-150 lines)
└── dashboard.html    # Single-file UI (HTML + embedded CSS + JS)
```

### Visual design direction

- Dark theme (developer-friendly, matches terminal aesthetic)
- Compact cards — step number + name + status icon
- Color coding: green (done), blue (in progress/next), gray (not yet), yellow (skipped), red border (hard gate)
- Progress bar per swimlane
- Responsive — works in a half-screen browser window beside the terminal

## Scope

- **In scope:** Server, HTML dashboard, SKILL.md, install.sh update, docs updates
- **Out of scope:** Authentication, persistent storage, WebSocket (polling is sufficient), editing/interaction, mobile layout

## Files to Create/Update

### New files
- `skills/sk:dashboard/SKILL.md` — skill definition
- `skills/sk:dashboard/server.js` — Node.js HTTP server
- `skills/sk:dashboard/dashboard.html` — single-file Kanban UI

### Files to update
- `CLAUDE.md` — add `/sk:dashboard` to commands table
- `README.md` — add to commands section
- `.claude/docs/DOCUMENTATION.md` — add to skills section
- `install.sh` — add `sk:dashboard` to workflow commands echo block
- `tasks/lessons.md` — append: update "update ALL files" list to include dashboard docs

## Open Questions

- None — design is locked
