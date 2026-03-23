---
name: sk:team
description: Parallel domain agents for full-stack implementation — spawns Backend, Frontend, and QA agents in isolated worktrees.
user_invocable: true
allowed_tools: Read, Write, Bash, Glob, Grep, Agent
---

# Team Mode

Splits implementation across specialized parallel agents when a task spans multiple domains (frontend + backend). Each agent works in an isolated worktree to avoid conflicts. Works in both manual and autopilot modes.

## When to Use

- Full-stack features with both backend API and frontend UI work
- Tasks where frontend and backend have clear boundaries (separate directories)
- Changes large enough that parallel implementation saves meaningful time

## When NOT to Use

- Backend-only or frontend-only tasks — single agent is faster
- Tasks where frontend and backend share files (e.g., Inertia controllers returning views)
- Small changes (<100 lines estimated) — worktree overhead exceeds time saved
- Tasks without a clear API contract boundary

## Agents

| Agent | Role | Isolation | Model |
|-------|------|-----------|-------|
| **Backend Agent** | Writes backend tests + implements API/services/models | Isolated worktree | sonnet |
| **Frontend Agent** | Writes frontend tests + implements UI/components/pages | Isolated worktree | sonnet |
| **QA Agent** | Writes E2E test scenarios while others implement | Background | sonnet |

## Prerequisites

The plan in `tasks/todo.md` MUST contain an explicit **API contract** section defining:
- Endpoint paths and HTTP methods
- Request payload shapes (with types)
- Response payload shapes (with types)
- Authentication requirements
- Error response formats

If no API contract is found, team mode warns and falls back to single-agent sequential mode.

## Steps

### 0. Validate Prerequisites

1. Read `tasks/todo.md` — scan for API contract section
2. If no API contract found:
   > "No API contract found in plan. Team mode requires explicit endpoint definitions as the shared boundary between agents. Falling back to single-agent mode."
   - Exit team mode, proceed with normal sequential implementation
3. If API contract found, continue

### 1. Prepare Worktrees

1. Get current branch name: `git branch --show-current`
2. Verify working directory is clean: `git status --porcelain`
3. Note: worktree creation is handled by the Agent tool's `isolation: "worktree"` parameter

### 2. Spawn Agents (parallel)

Launch all 3 agents simultaneously using the Agent tool:

**Backend Agent** (`isolation: "worktree"`):
- Task: "Read the API contract in tasks/todo.md. Write backend tests for all endpoints (controller tests, model tests, validation tests). Then implement: migrations, models, services, controllers, routes. Make all tests pass. Commit with `feat(backend): [description]`."
- Receives: full plan from `tasks/todo.md`, `tasks/lessons.md`

**Frontend Agent** (`isolation: "worktree"`):
- Task: "Read the API contract in tasks/todo.md. Write frontend tests for all components/pages (component tests, interaction tests, form tests). Mock API endpoints using contract shapes. Then implement: API client, composables/hooks, components, pages, routes. Make all tests pass. Commit with `feat(frontend): [description]`."
- Receives: full plan from `tasks/todo.md`, `tasks/lessons.md`

**QA Agent** (`run_in_background: true`):
- Task: "Read the plan in tasks/todo.md. Write E2E test scenarios covering all user flows. Do NOT run them — they'll be executed after merge. Report scenario count and coverage summary."
- Receives: full plan from `tasks/todo.md`

### 3. Wait for Completion

Wait for Backend Agent and Frontend Agent to complete. The QA Agent runs in the background and will be collected later.

For each completed agent, check:
- Did it succeed or hit 3-strike failure?
- What files were changed?
- What tests pass?

### 4. Merge Worktrees

If both agents used worktree isolation and made changes:

1. Check if worktree branches exist
2. Merge backend worktree branch into feature branch:
   ```bash
   git merge <backend-worktree-branch> --no-edit
   ```
3. Merge frontend worktree branch into feature branch:
   ```bash
   git merge <frontend-worktree-branch> --no-edit
   ```
4. If merge conflicts occur:
   - Attempt auto-resolution for non-overlapping changes
   - If conflicts are in shared files (routes, config, types), resolve by combining both additions
   - If conflicts are ambiguous, stop and ask user:
     > "Merge conflict in [file]. Backend added [X], Frontend added [Y]. Which to keep, or combine?"

### 5. Collect QA Agent Results

Collect the QA Agent's E2E scenarios. These will be used in the E2E gate (step 17).

### 6. Report Results

```
Team implementation complete:
  Backend Agent: [N] files changed, [M] tests passing
  Frontend Agent: [N] files changed, [M] tests passing
  QA Agent: [N] E2E scenarios written
  Merge: [clean / N conflicts resolved]

Ready for commit and quality gates.
```

## Fallback

If worktree creation fails (git state issues, disk space, etc.):
> "Worktree creation failed: [error]. Falling back to single-agent sequential mode."

Run normal sequential implementation (write-tests → implement) instead.

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:team"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit. When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
