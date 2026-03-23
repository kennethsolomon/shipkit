---
description: "Parallel domain agents — spawns Backend, Frontend, and QA agents for full-stack implementation."
---

# /sk:team

Split implementation across parallel domain agents.

Usage: `/sk:team`

Spawns 3 specialized agents in parallel:
- **Backend Agent** (worktree) — backend tests + implementation
- **Frontend Agent** (worktree) — frontend tests + implementation
- **QA Agent** (background) — E2E test scenarios

**Prerequisite:** Plan must contain an explicit API contract section.

Falls back to single-agent mode if:
- No API contract in plan
- Backend-only or frontend-only task
- Worktree creation fails

See `skills/sk:team/SKILL.md` for full details.
