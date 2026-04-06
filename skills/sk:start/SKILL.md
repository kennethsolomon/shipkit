---
name: sk:start
description: Smart entry point — classifies your task, detects scope, and routes to the optimal flow (feature/debug/hotfix/fast-track), mode (manual/autopilot), and agent strategy (solo/team).
allowed-tools: Read, Write, Bash, Glob, Grep, Agent, Skill
---

# Smart Start

Single entry point that classifies your task and recommends the optimal workflow configuration. Replaces the need to know which command to run first.

## Usage

```
/sk:start <task description>
/sk:start --manual add user profile page
/sk:start --team add profile page with API
/sk:start --debug fix login redirect loop
/sk:start --hotfix prod payments failing
/sk:start --fast-track bump lodash dependency
```

## Steps

### Step 1 — Classify (automatic, no prompt)

Read the task description from arguments. Scan for signal keywords to determine flow and scope:

**Flow detection:**

Check in this order — first match wins:

| Signal Keywords | Additional condition | Detected Flow |
|----------------|---------------------|---------------|
| urgent, prod down, hotfix, emergency, critical, production, incident | — | `hotfix` (6 steps) |
| config, bump, typo, copy, rename, dependency, upgrade, version, docs | — | `fast-track` (5 steps) |
| bug, fix, broken, error, regression, failing, crash, wrong, issue, unexpected | Has known-cause anchor (file:line, "the issue is", specific function + symptom) | `debug` (7 steps) |
| bug, fix, broken, error, regression, failing, crash, wrong, issue, unexpected | No known-cause anchor | `deep-dive` (trace → interview → fix) |
| *(default — no special signals)* | — | `feature` (8 phases + scope check, learn, retro) |

**Known-cause anchors:** specific file path (`app/Models/User.php`), line number reference, function/method name + symptom, explicit "the issue is X", specific HTTP status pointing to code location.

**Vague feature detection** (runs for `feature` flow only):
After flow detection, check if the feature request has no concrete anchors (no file paths, no function names, no bounded scope) AND uses open-ended verbs (improve, enhance, make better, add features, build something, clean up, refactor). If yes, flag as `vague-feature`.

**Scope detection:**

| Signal Keywords | Detected Scope |
|----------------|----------------|
| Frontend: component, page, view, CSS, UI, form, modal, button, sidebar, navbar, layout, style, tailwind, animation | `frontend` |
| Backend: API, endpoint, controller, model, migration, service, queue, job, middleware, database, schema, route | `backend` |
| Both frontend AND backend keywords present | `full-stack` |
| Neither | `unknown` (ask user) |

**Agent recommendation:**

| Scope | Agents |
|-------|--------|
| `full-stack` | `team` (backend + frontend + QA agents) |
| `frontend` only | `solo` |
| `backend` only | `solo` |
| `unknown` | `solo` (default) |

### Step 1.5 — Missing Context Detection (automatic, no prompt)

After classification, scan the task description for gaps. This is informational only — does NOT block.

**Critical context checks:**

| Check | How to detect | Auto-resolve |
|-------|--------------|--------------|
| Tech stack specified? | Look for framework/language keywords | Auto-detect from package.json, composer.json, go.mod, Cargo.toml |
| Acceptance criteria present? | Look for "should", "must", "when", "given" | Cannot auto-resolve — flag for user |
| Scope boundaries stated? | Look for "only", "not", "exclude", "just" | Cannot auto-resolve — flag for user |
| Security requirements? | Check if task involves auth, user data, payments, tokens | Flag: "This touches auth/user data — consider security requirements" |
| Testing expectations? | Look for "test", "coverage", "spec" | Default: 100% coverage on new code (per workflow) |

**If 3+ critical items are missing**, include in the recommendation output:

```
Missing Context (3 items — consider clarifying):
  - No acceptance criteria detected
  - No scope boundaries stated (what should NOT change?)
  - Task involves user data but no security requirements mentioned
```

This check runs silently. If <3 items missing, no output.

### Step 2 — Recommend (one prompt, user confirms or overrides)

Present the classification and recommendation:

```
# Standard feature:
Detected: [Full-stack feature / Backend feature / Frontend feature / etc.]
Recommended:
  Flow:   feature (8 phases)
  Mode:   autopilot
  Agents: [team / solo]
Proceed? (y) or override: manual / no-team / --debug / --hotfix / --fast-track

# Vague feature:
Detected: Open-ended feature request — requirements need clarification
Recommended:
  Flow:   feature (with deep-interview pre-step)
  Mode:   autopilot
  Agents: [scope-based]
Proceed? (y) or override: manual / skip-interview

# Unknown-cause bug:
Detected: Bug investigation (root cause unknown)
Recommended:
  Flow:   deep-dive (trace → interview → fix)
  Mode:   autopilot
  Agents: solo
Proceed? (y) or override: manual / --debug (if cause is known)

# Known-cause bug:
Detected: Bug fix (cause identified)
Recommended:
  Flow:   debug (7 steps)
  Mode:   autopilot
  Agents: solo
```

Default mode recommendation:
- `feature`, `debug`, `deep-dive`, `hotfix`, `fast-track` flow → recommend `autopilot`

Wait for user response:
- `y` or `yes` → proceed with recommendation
- `manual` → use recommended flow but in manual mode (step-by-step)
- `no-team` → use autopilot but single-agent (no team)
- `--debug` → force debug flow
- `--hotfix` → force hotfix flow
- `--fast-track` → force fast-track flow
- Any other override → apply it

### Step 3 — Route (enters the chosen flow)

1. Log the routing decision to terminal:
   ```
   Mode: [autopilot/manual] | Agents: [team/solo] | Flow: [feature/debug/hotfix/fast-track]
   ```

2. Dispatch to the chosen flow:

   **If autopilot mode:**
   - Invoke `/sk:autopilot` with the task description
   - Autopilot handles everything from here

   **If manual mode + team:**
   - Start the normal step-by-step workflow (`/sk:brainstorm`)
   - Note in tracker: "Team mode active — activate `/sk:team` at step 9"
   - User drives each step manually; team mode activates at write-tests/implement

   **If manual mode + solo:**
   - Start the normal step-by-step workflow (`/sk:brainstorm`)
   - Standard manual behavior — no changes from current flow

   **If deep-dive flow:**
   - Invoke `Skill("sk:deep-dive")` with the task description
   - Deep-dive produces `tasks/spec.md` with root cause + fix scope
   - After spec is written, continue bug fix flow: branch → write-tests → execute-plan → commit → gates → finalize

   **If feature flow + autopilot + vague-feature flagged:**
   - Invoke `/sk:autopilot` — autopilot step 0 handles deep-interview automatically

   **If feature flow + manual mode + vague-feature flagged:**
   - Log: `[Start] Open-ended request — running /sk:deep-interview before brainstorm.`
   - Invoke `Skill("sk:deep-interview")`
   - After spec.md is written, invoke `/sk:brainstorm` (reads spec.md automatically)

   **If debug flow:**
   - Invoke `/sk:debug` with the task description

   **If hotfix flow:**
   - Invoke `/sk:hotfix` with the task description

   **If fast-track flow:**
   - Invoke `/sk:fast-track` with the task description

### Step 3.5 — Task Onboarding Record (automatic, no prompt)

After routing, write a lightweight task context snapshot to `tasks/onboarding/[task-slug].md`. This enables `/sk:resume-session` to pick up exactly where the task left off.

Generate `[task-slug]` from the task description: lowercase, spaces → hyphens, max 40 chars. Example: `add-user-authentication`.

```markdown
# Task: [task description]
Date: [YYYY-MM-DD HH:MM]
Branch: [current branch or "not yet created"]
Flow: [feature/debug/hotfix/fast-track]
Mode: [autopilot/manual]
Agents: [team/solo]

## Codebase State
- Recent commits: [last 3 from git log --oneline -3]
- Modified files: [git status --short, if any]

## Detected Context
- Stack: [detected from package.json / composer.json / etc.]
- Scope: [frontend/backend/full-stack/unknown]
- Missing context flagged: [list if any, else "none"]

## Entry Point
Routed to: [/sk:autopilot / /sk:brainstorm / /sk:debug / /sk:hotfix / /sk:fast-track]
```

This file is ephemeral — it is for session continuity only. Do not log to `tasks/findings.md`.

## Override Flags

| Flag | Effect |
|------|--------|
| `--manual` | Force manual mode (step-by-step, no auto-advance) |
| `--no-team` | Force single-agent even if full-stack detected |
| `--team` | Force team mode even if single-domain detected |
| `--debug` | Force debug flow (known-cause bug fix) |
| `--deep-dive` | Force deep-dive flow (unknown-cause investigation) |
| `--interview` | Force deep-interview pre-step even on clear requests |
| `--hotfix` | Force hotfix flow (production emergency) |
| `--fast-track` | Force fast-track flow (small change) |
| `--intensity lite\|full\|deep` | Override intensity for this session |

Flags can be combined: `/sk:start --manual --team --intensity deep add profile page`

## Relationship to Existing Commands

- `/sk:start` is the **recommended** entry point for all new work
- Old commands still work as direct entry points:
  - `/sk:brainstorm` → manual feature workflow
  - `/sk:debug` → bug fix flow
  - `/sk:hotfix` → hotfix flow
  - `/sk:fast-track` → fast-track flow
  - `/sk:autopilot` → autopilot mode directly
- `/sk:start` calls those same flows internally — it's a router, not a replacement

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:start"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Start is a lightweight classifier — haiku is sufficient for keyword matching and routing.
