# /sk:start

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Entry point (before step 1)
> **Command:** `/sk:start`
> **Skill file:** `skills/sk:start/SKILL.md`

---

## Overview

Smart entry point that classifies a task description and recommends the optimal workflow configuration: flow (feature/debug/hotfix/fast-track), mode (manual/autopilot), and agent strategy (solo/team). Replaces the need to know which command to run first.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Task description | Command argument | Yes |
| `tasks/todo.md` | Additional context for classification | No |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Classification | Terminal | Flow + scope + agent recommendation |
| Dispatched flow | Invoked skill | Routes to autopilot, brainstorm, debug, hotfix, or fast-track |

---

## Business Logic

1. **Classify** (automatic, no prompt):
   - Scan description for bug signals → debug flow
   - Scan for urgency signals → hotfix flow
   - Scan for small-change signals → fast-track flow
   - Default → feature flow
   - Scan for frontend/backend keywords → detect scope (full-stack/frontend/backend)
   - Full-stack → recommend team mode; single-domain → recommend solo
2. **Recommend** (one prompt):
   - Present: detected type, recommended flow + mode + agents
   - Show override options
   - Wait for user confirmation
3. **Route**:
   - Dispatch to chosen flow (autopilot, brainstorm, debug, hotfix, fast-track)

---

## Hard Rules

- Always waits for user confirmation before routing — never auto-dispatches
- Classification is keyword-based — explicit override flags always take precedence
- All existing entry points still work (sk:brainstorm, sk:debug, etc.) — sk:start is additive

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No task description provided | Ask user to describe the task |
| Ambiguous keywords (e.g., "fix the config") | Defaults to most specific match (fix → debug, config → fast-track; debug wins) |
| Multiple override flags | Apply all (e.g., `--manual --team`) |
| Unknown scope | Default to solo, ask user in recommendation |

---

## Error States

| Condition | Behavior |
|-----------|----------|
| Invoked skill fails | Error propagates from the dispatched skill |
| Invalid override flag | Warn and show valid options |

---

## UI/UX Behavior

### CLI Output
```
Detected: Full-stack feature (backend API + frontend page + migration)
Recommended:
  Flow:   feature (8 steps)
  Mode:   autopilot
  Agents: team (backend + frontend + QA)

Proceed? (y) or override: manual / no-team / --debug / --hotfix / --fast-track
```

### When Done
Routes to chosen flow — no explicit "done" message from sk:start itself.

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:start/SKILL.md` — full implementation spec
- `commands/sk/start.md` — command shortcut
- `docs/sk:features/sk-autopilot.md` — autopilot mode (dispatched by start)
- `docs/sk:features/sk-team.md` — team mode (dispatched by start)
- `docs/sk:features/sk-fast-track.md` — fast-track flow (dispatched by start)
