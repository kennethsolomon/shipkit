---
name: sk:save-session
description: "Save current session state for cross-session continuity."
---

# /sk:save-session — Persist Session State

Saves the current session state to `.claude/sessions/` so you can resume work in a future conversation. Essential for EPIC-scope tasks that span multiple sessions.

## Usage

```
/sk:save-session                    # save with auto-generated name
/sk:save-session --name "auth-flow" # save with custom name
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Serialization is lightweight — haiku is sufficient.

## What Gets Saved

The session file captures:

```markdown
---
saved: [YYYY-MM-DDTHH:MM:SSZ]
branch: [current git branch]
task: [current task title from tasks/todo.md]
step: [current workflow step number]
---

## Active Task
[Current task description from tasks/todo.md — first unchecked item]

## Branch State
- Branch: [name]
- Commits since main: [count]
- Uncommitted changes: [list of modified files]

## Progress Summary
[Last 10 lines from tasks/progress.md]

## Key Findings This Session
[Any entries added to tasks/findings.md during this session]

## Open Questions
[Questions that were raised but not resolved]

## Next Steps
[What should be done when resuming — derived from todo.md + progress]

## Context Notes
[Any important context that would be lost on session end]
```

## Storage

- **Path**: `.claude/sessions/[YYYY-MM-DD]-[branch]-[name].md`
- **Example**: `.claude/sessions/2026-03-25-feat-auth-flow-auth-flow.md`
- **Gitignore**: Add `.claude/sessions/` to `.gitignore` (session state is personal, not shared)

## Steps

1. Read current git state (branch, uncommitted changes, recent commits)
2. Read `tasks/todo.md` — extract current task and step
3. Read `tasks/progress.md` — extract recent entries
4. Read `tasks/findings.md` — extract entries from today
5. Ask user: "Any open questions or context to preserve?" (optional)
6. Write session file to `.claude/sessions/`
7. Confirm save with file path

## Auto-Save via Hook

The `session-stop.sh` hook automatically saves a minimal session snapshot on every session end. The `/sk:save-session` command creates a richer, more detailed snapshot with user input.
