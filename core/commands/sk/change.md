---
description: "Handle a mid-workflow requirement change — assess scope and re-enter at the right step."
---

# /sk:change

Handle a requirement change that was discovered mid-workflow. Assesses the scope of the change and routes you back to the correct step — no over-restarting, no skipping.

## Hard Rules

- **DO NOT modify code or tests until this command completes.** The re-entry point must be determined first.
- **DO NOT guess the scope.** Ask explicitly if unclear.
- **Always update `tasks/todo.md` and `tasks/progress.md`** to record what changed and why before routing forward.

## Steps

### 1. Understand the Change

Ask the user:
- What changed? (describe the old behavior and the new behavior)
- What triggered this change? (review finding, stakeholder feedback, edge case discovered, etc.)
- Is this change isolated to one area, or does it affect multiple parts of the system?

Do not proceed until you have clear answers.

### 2. Assess the Scope

Based on the answers, classify the change into one of three tiers:

---

**Tier 1 — Behavior Tweak**

The logic changes but the scope and plan stay the same. Examples:
- Delete all tables → delete only users table
- Return 404 → return 403 on unauthorized access
- Sort ascending → sort descending

Re-entry point: **`/sk:write-tests`**

Action: Update or replace the affected tests to reflect the new behavior. The existing plan is still valid — only the test assertions and implementation need to change.

---

**Tier 2 — New Requirements**

New scope, new constraints, or new acceptance criteria that the current plan doesn't cover. Examples:
- Simple delete → soft-delete with audit log
- Basic auth → role-based permissions
- Single endpoint → paginated + filterable endpoint

Re-entry point: **`/sk:write-plan`**

Action: Update `tasks/todo.md` with revised tasks. The brainstorm findings are still valid but the plan needs new steps. After plan approval, proceed to `/sk:write-tests`.

---

**Tier 3 — Scope Shift**

Fundamental rethinking of the approach, user flow, or architecture. Examples:
- Rethinking the entire delete flow and who can trigger it
- Changing the data model the feature is built on
- New understanding of the problem that invalidates prior decisions

Re-entry point: **`/sk:brainstorm`**

Action: The existing findings and plan may be partially or fully invalid. Start fresh from brainstorm, record new decisions in `tasks/findings.md`, then proceed through write-plan → write-tests → execute-plan.

---

### 3. Confirm the Tier

Present your classification to the user:

```
Change detected: <1-line summary of what changed>
Scope tier: Tier <1|2|3> — <Behavior Tweak|New Requirements|Scope Shift>
Re-entry point: /sk:<command>

Reason: <1-2 sentences explaining why this tier was chosen>

Proceed? (yes / no / different tier)
```

Wait for explicit confirmation before logging or routing.

### 4. Log the Change

Once confirmed, update the planning files:

**`tasks/todo.md`** — Add a `## Change Log` section at the top (or append to existing):
```
## Change Log
- [<date>] <summary of change> — re-entered at /sk:<command>
```

Mark any tasks that are now invalidated with `~~strikethrough~~` and a note: `(invalidated by requirement change — see change log)`.

**`tasks/progress.md`** — Append:
```
## Requirement Change — <date>
- What changed: <description>
- Trigger: <what caused the change>
- Scope tier: <1|2|3>
- Re-entry point: /sk:<command>
- Invalidated tasks: <list or "none">
```

### 5. Route Forward

Tell the user exactly where to go next:

> "Change logged. Re-enter the workflow at `/sk:<command>`.
> Carry forward: <what's still valid — plan steps, findings, etc.>
> Discard: <what's no longer valid>"

**Do not proceed to the next step yourself.** The user must explicitly invoke it.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:change"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit. When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
