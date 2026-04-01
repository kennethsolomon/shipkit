# /sk:start

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Entry point (before step 1)
> **Command:** `/sk:start`
> **Skill file:** `skills/sk:start/SKILL.md`

---

## Overview

Smart entry point that classifies a task description and recommends the optimal workflow configuration: flow (feature/debug/deep-dive/hotfix/fast-track), mode (manual/autopilot), and agent strategy (solo/team). Replaces the need to know which command to run first.

Also detects vague feature requests and routes to `/sk:deep-interview` before brainstorm, and detects unknown-cause bugs and routes to `/sk:deep-dive` before the fix flow.

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
| Dispatched flow | Invoked skill | Routes to autopilot, brainstorm, debug, deep-dive, hotfix, or fast-track |

---

## Business Logic

### Step 1 — Flow Detection

| Signal | Detected Flow |
|--------|--------------|
| Bug signals (bug, fix, broken, error, crash, failing, not working, issue, unexpected behavior) AND no known-cause anchors (no file:line, no "the issue is X", no specific function + symptom) | `deep-dive` |
| Bug signals AND known cause present | `debug` |
| urgent, prod down, hotfix, emergency | `hotfix` |
| config, bump, typo, dependency, rename | `fast-track` |
| (default) | `feature` |

**Known-cause anchors:** specific file path, function name, line number, "the issue is", "because", specific error code/message pointing to a cause.

### Step 1.5 — Vague Feature Detection

For `feature` flow tasks, checks for vague-feature signals:

| Check | How to detect | Action |
|-------|--------------|--------|
| Is feature request vague? | No file paths, no function names, no bounded scope, open-ended verbs (improve/enhance/build/add features/make better/clean up) | Flag: `vague-feature` |

### Step 2 — Recommend

| Detected | Recommended output |
|----------|-------------------|
| Unknown-cause bug | `Flow: deep-dive (trace → interview → fix) / Mode: autopilot / Agents: solo` |
| Vague feature | `Flow: feature (with deep-interview pre-step) / Mode: autopilot / Agents: [scope-based]` |
| Full-stack feature | `Flow: feature / Mode: autopilot / Agents: team` |
| Debug (known cause) | `Flow: debug / Mode: manual / Agents: solo` |
| Fast-track | `Flow: fast-track / Mode: autopilot / Agents: solo` |

### Step 3 — Route

| Flow | Action |
|------|--------|
| `deep-dive` | Invoke `/sk:deep-dive` → produces `tasks/spec.md` with root cause → continue: branch → write-tests → execute-plan → commit → gates → finalize |
| `feature` + autopilot + `vague-feature` | Autopilot Step 0 handles deep-interview automatically |
| `feature` + manual + `vague-feature` | Log: `[Start] Vague request — running /sk:deep-interview before brainstorm.` → invoke `/sk:deep-interview` → invoke `/sk:brainstorm` (reads spec.md) |
| `feature` + clear | Invoke autopilot or brainstorm as recommended |
| `debug` | Invoke `/sk:debug` |
| `hotfix` | Invoke `/sk:hotfix` |
| `fast-track` | Invoke `/sk:fast-track` |

---

## Override Flags

| Flag | Effect |
|------|--------|
| `--manual` | Force manual mode (no autopilot) |
| `--team` | Force team agents regardless of scope |
| `--no-team` | Force solo agents |
| `--debug` | Force debug flow |
| `--hotfix` | Force hotfix flow |
| `--fast-track` | Force fast-track flow |
| `--deep-dive` | Force deep-dive flow (trace + interview for bug investigation) |
| `--interview` | Force deep-interview pre-step before brainstorm |

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
| Ambiguous keywords (e.g., "fix the config") | Defaults to most specific match (fix → debug wins over config → fast-track) |
| Bug signals + no known cause | Routes to deep-dive, not debug |
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

### CLI Output — Clear input
```
Detected: Full-stack feature (backend API + frontend page + migration)
Recommended:
  Flow:   feature (8 steps)
  Mode:   autopilot
  Agents: team (backend + frontend + QA)

Proceed? (y) or override: manual / no-team / --debug / --hotfix / --fast-track
```

### CLI Output — Unknown-cause bug
```
Detected: Bug investigation (root cause unknown)
Recommended:
  Flow:   deep-dive (trace → interview → fix)
  Mode:   autopilot
  Agents: solo

Proceed? (y) or override: --debug (if you know the cause)
```

### CLI Output — Vague feature
```
Detected: Open-ended feature request — requirements need clarification
Recommended:
  Flow:   feature (with deep-interview pre-step)
  Mode:   autopilot
  Agents: [scope-based]

Proceed? (y) or override: manual / --interview (run interview only)
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
- `docs/sk:features/sk-deep-dive.md` — unknown-cause bug investigation (dispatched by start)
- `docs/sk:features/sk-deep-interview.md` — vague feature requirements gathering (dispatched by start)
