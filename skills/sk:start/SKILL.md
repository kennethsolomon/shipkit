---
name: sk:start
description: Smart entry point — classifies your task, detects scope, and routes to the optimal flow (feature/debug/hotfix/fast-track), mode (manual/autopilot), and agent strategy (solo/team).
user_invocable: true
allowed_tools: Read, Write, Bash, Glob, Grep, Agent, Skill
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

| Signal Keywords | Detected Flow |
|----------------|---------------|
| bug, fix, broken, error, regression, failing, crash, wrong | `debug` (7 steps) |
| urgent, prod down, hotfix, emergency, critical, production, incident | `hotfix` (6 steps) |
| config, bump, typo, copy, rename, dependency, upgrade, version, docs | `fast-track` (5 steps) |
| *(default — no special signals)* | `feature` (8 steps) |

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
Detected: [Full-stack feature / Backend bug fix / Frontend hotfix / Small config change / etc.]
Recommended:
  Flow:   [feature (8 steps) / debug (7 steps) / hotfix (6 steps) / fast-track (5 steps)]
  Mode:   [autopilot / manual]
  Agents: [team (backend + frontend + QA) / solo]

Proceed? (y) or override: manual / no-team / --debug / --hotfix / --fast-track
```

Default mode recommendation:
- `feature` flow → recommend `autopilot`
- `debug` flow → recommend `autopilot`
- `hotfix` flow → recommend `autopilot`
- `fast-track` flow → recommend `autopilot`

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

   **If debug flow:**
   - Invoke `/sk:debug` with the task description

   **If hotfix flow:**
   - Invoke `/sk:hotfix` with the task description

   **If fast-track flow:**
   - Invoke `/sk:fast-track` with the task description

## Override Flags

| Flag | Effect |
|------|--------|
| `--manual` | Force manual mode (step-by-step, no auto-advance) |
| `--no-team` | Force single-agent even if full-stack detected |
| `--team` | Force team mode even if single-domain detected |
| `--debug` | Force debug flow (bug fix) |
| `--hotfix` | Force hotfix flow (production emergency) |
| `--fast-track` | Force fast-track flow (small change) |

Flags can be combined: `/sk:start --manual --team add profile page`

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
