---
name: sk:resume-session
description: "Resume a previously saved session with full context restoration."
---

# /sk:resume-session — Restore Session Context

Lists available saved sessions and restores the selected one, injecting the saved context into the current conversation.

## Usage

```
/sk:resume-session             # list sessions, pick one
/sk:resume-session --latest    # auto-pick most recent session
/sk:resume-session --name "auth-flow"  # resume specific named session
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Deserialization is lightweight — haiku is sufficient.

## How It Works

### Step 1: List Available Sessions

Read `.claude/sessions/` and display:

```
Available sessions:

  1. [2026-03-25] feat/auth-flow — "auth-flow" (3 hours ago)
     Task: Implement OAuth2 login with Google
     Step: 5 (Write Tests + Implement)

  2. [2026-03-24] feat/api-redesign — "api-v2" (1 day ago)
     Task: Redesign REST API to v2 spec
     Step: 7 (Gates)

  3. [2026-03-23] fix/queue-timeout — auto-save (2 days ago)
     Task: Fix Redis queue timeout in production
     Step: 4 (Branch)

Select session (1-3) or 'q' to cancel:
```

### Step 2: Load Session

Read the selected session file and inject context:

1. **Verify branch** — check if the session's branch still exists
   - If yes: suggest `git checkout [branch]` if not already on it
   - If no: warn that the branch was deleted, proceed with context anyway
2. **Load task state** — read `tasks/todo.md` and cross-reference with saved state
3. **Load progress** — read `tasks/progress.md` for the full history
4. **Restore context** — output the session's findings, open questions, and next steps

### Step 3: Report

```
Resumed session from 2026-03-25 on branch feat/auth-flow

  Task: Implement OAuth2 login with Google
  Step: 5 (Write Tests + Implement)
  Commits since save: 2

  Open Questions:
    - Should we support refresh token rotation?
    - Which scopes are required for profile access?

  Next Steps:
    - Write integration test for token exchange
    - Implement callback controller
```

### Step 4: Continue

The workflow continues from wherever it left off. The session file provides enough context to avoid re-reading the entire codebase.

## Session Cleanup

Sessions older than 30 days are candidates for cleanup. Run manually:
```bash
find .claude/sessions/ -name "*.md" -mtime +30 -delete
```

Future: add `--cleanup` flag to auto-remove old sessions.
