# /sk:team

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Steps 9-10 (Write Tests + Implement) — parallel replacement
> **Command:** `/sk:team`
> **Skill file:** `skills/sk:team/SKILL.md`

---

## Overview

Splits implementation across 3 specialized parallel agents for full-stack tasks: Backend Agent, Frontend Agent, and QA Agent. Each works in an isolated git worktree. Requires an API contract in the plan as the shared boundary. Falls back to single-agent mode when prerequisites aren't met.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Plan with API contract section | Yes |
| `tasks/lessons.md` | Active lessons as constraints | Yes |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Backend tests + code | Feature branch (merged from worktree) | Via Backend Agent |
| Frontend tests + code | Feature branch (merged from worktree) | Via Frontend Agent |
| E2E test scenarios | Test files or `tasks/e2e-scenarios.md` | Via QA Agent |
| Merge result | Feature branch | Auto-merged from worktrees |

---

## Business Logic

1. Validate prerequisites — scan plan for API contract section
2. If no API contract: warn and fall back to single-agent mode
3. Spawn 3 agents simultaneously:
   - Backend Agent (isolated worktree): backend tests + implementation
   - Frontend Agent (isolated worktree): frontend tests + implementation with mocked API
   - QA Agent (background): E2E test scenarios
4. Wait for Backend + Frontend agents to complete
5. Merge worktree branches back to feature branch
6. Collect QA Agent's E2E scenarios
7. Report results (files changed, tests passing, merge status)

---

## Hard Rules

- API contract in plan is mandatory — no contract = no team mode
- Agents ONLY touch their domain (backend files or frontend files, never both)
- Agents do NOT modify the API contract
- Backend and Frontend agents each run their own test suite before reporting done
- Merge conflicts escalate to user if ambiguous

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No API contract in plan | Warn, fall back to single-agent |
| Backend-only or frontend-only task | Fall back to single-agent (team adds overhead) |
| Worktree creation fails | Fall back to single-agent sequential mode |
| Merge conflict in shared files | Auto-resolve if possible, escalate to user if ambiguous |
| One agent fails, other succeeds | Report partial success, merge successful agent's work |

---

## Error States

| Condition | Behavior |
|-----------|----------|
| Agent hits 3-strike failure | Stop that agent, report to orchestrator |
| Both agents fail | Stop team mode, report all failures to user |
| Merge fails completely | Leave worktrees intact, ask user to merge manually |

---

## UI/UX Behavior

### CLI Output
```
Team mode activated — spawning 3 agents:
  Backend Agent (worktree): writing backend tests + implementation
  Frontend Agent (worktree): writing frontend tests + implementation
  QA Agent (background): writing E2E scenarios

[Backend Agent] Complete: 5 files changed, 12 tests passing
[Frontend Agent] Complete: 7 files changed, 8 tests passing
[QA Agent] Complete: 4 E2E scenarios written

Merging worktrees... clean merge.
Team implementation complete.
```

### When Done
```
Team implementation complete:
  Backend Agent: 5 files changed, 12 tests passing
  Frontend Agent: 7 files changed, 8 tests passing
  QA Agent: 4 E2E scenarios written
  Merge: clean

Ready for commit and quality gates.
```

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:team/SKILL.md` — full implementation spec
- `commands/sk/team.md` — command shortcut
- `skills/sk:setup-claude/templates/.claude/agents/backend-dev.md` — Backend Agent template
- `skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md` — Frontend Agent template
- `skills/sk:setup-claude/templates/.claude/agents/qa-engineer.md` — QA Agent template
