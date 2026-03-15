---
description: "Switch the ShipKit model routing profile for this project."
---

# /sk:set-profile

Quickly switch the model routing profile for this project.

Usage: `/sk:set-profile <profile>`

Valid profiles: `full-sail` · `quality` · `balanced` · `budget`

## Profiles

| Profile | Philosophy | Best for |
|---------|-----------|---------|
| `full-sail` | Opus on everything that matters | High-stakes work, client projects, production features |
| `quality` | Opus for planning + review, Sonnet for implementation | Most professional projects |
| `balanced` | Sonnet across the board *(default)* | Day-to-day development |
| `budget` | Haiku where possible, Sonnet for gates | Side projects, exploration, prototyping |

## Model Table

| Skill | full-sail | quality | balanced | budget |
|-------|-----------|---------|----------|--------|
| brainstorm, write-plan, debug, execute-plan, review | opus | opus | sonnet | sonnet |
| write-tests, frontend-design, api-design, security-check | opus | sonnet | sonnet | sonnet |
| perf, schema-migrate, accessibility | opus | sonnet | sonnet | haiku |
| lint, test | sonnet | sonnet | haiku | haiku |
| smart-commit, branch, update-task | haiku | haiku | haiku | haiku |

Note: `opus` = inherit (uses the current session model). Switch to Opus 4.5 in your session to get the full benefit.

## Steps

### 1 — Validate input

If no profile argument provided, show the profile table above and ask: "Which profile? (full-sail / quality / balanced / budget)"

If an invalid profile name is given, show the valid options.

### 2 — Read current config

Read `.shipkit/sk:config.json` if it exists. Otherwise start with defaults.

### 3 — Update profile

Set `profile` to the chosen value.

### 4 — Write config

1. Create `.shipkit/` directory if it does not exist
2. Write updated config to `.shipkit/sk:config.json`
3. Add `.shipkit/` to `.gitignore` if not already present

### 5 — Confirm

Display:

```
Profile set to: <profile>

Model assignments for this project:
  brainstorm, write-plan, debug, execute-plan, review → <model>
  write-tests, frontend-design, api-design, security-check → <model>
  perf, schema-migrate, accessibility → <model>
  lint, test → <model>
  smart-commit, branch, update-task → haiku

Run /sk:config to see all settings or make further changes.
```
