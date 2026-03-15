---
description: "View and edit ShipKit project configuration (.shipkit/sk:config.json)."
---

# /sk:config

View and manage ShipKit configuration for this project.

## Config File

ShipKit stores per-project config in `.shipkit/sk:config.json` at the project root.
If the file does not exist, display defaults and offer to create it.

## Steps

### 1 — Read current config

Check if `.shipkit/sk:config.json` exists. If yes, read and parse it.
If not, use defaults:

```json
{
  "profile": "balanced",
  "auto_commit": true,
  "skip_gates": [],
  "coverage_threshold": 100,
  "branch_pattern": "feature/{slug}",
  "model_overrides": {}
}
```

### 2 — Display current config

Show a formatted table explaining every setting and its current value:

| Setting | Value | Description |
|---------|-------|-------------|
| `profile` | `<value>` | Model routing profile (full-sail / quality / balanced / budget) |
| `auto_commit` | `<value>` | Auto-run `/sk:smart-commit` after each gate passes |
| `skip_gates` | `<value>` | Gates to skip (e.g. `["perf","accessibility"]` for backend-only projects) |
| `coverage_threshold` | `<value>` | Minimum test coverage % on new code (default: 100) |
| `branch_pattern` | `<value>` | Branch naming pattern (`feature/{slug}`, `feat/{slug}`, etc.) |
| `model_overrides` | `<value>` | Per-skill model overrides e.g. `{ "sk:review": "opus" }` |

Then show the model table for the **current profile**:

#### Model assignments — `<profile>` profile

| Skill | Model |
|-------|-------|
| brainstorm, write-plan, debug, execute-plan, review | `<model>` |
| write-tests, frontend-design, api-design, security-check | `<model>` |
| perf, schema-migrate, accessibility | `<model>` |
| lint, test | `<model>` |
| smart-commit, branch, update-task | `haiku` |

Use this model table to fill in values:

| Skill | full-sail | quality | balanced | budget |
|-------|-----------|---------|----------|--------|
| brainstorm, write-plan, debug, execute-plan, review | opus | opus | sonnet | sonnet |
| write-tests, frontend-design, api-design, security-check | opus | sonnet | sonnet | sonnet |
| perf, schema-migrate, accessibility | opus | sonnet | sonnet | haiku |
| lint, test | sonnet | sonnet | haiku | haiku |
| smart-commit, branch, update-task | haiku | haiku | haiku | haiku |

Note: `opus` resolves to `inherit` — Claude uses whatever model the current session is running on.

### 3 — Offer to edit

Ask: "Which setting would you like to change? (or press Enter to exit)"

If the user specifies a setting:

- `profile` → show `/sk:set-profile` options and apply
- `auto_commit` → toggle true/false
- `skip_gates` → show available gates (`lint`, `test`, `security-check`, `perf`, `accessibility`, `review`) and let user pick
- `coverage_threshold` → accept a number 0-100
- `branch_pattern` → accept a pattern string (show examples: `feature/{slug}`, `feat/{slug}`, `{slug}`)
- `model_overrides` → accept JSON or guided per-skill input

### 4 — Write config

If any setting was changed:
1. Create `.shipkit/` directory if it does not exist
2. Write updated config to `.shipkit/sk:config.json`
3. Add `.shipkit/sk:config.json` to `.gitignore` if not already present
4. Confirm: "Config saved to `.shipkit/sk:config.json`"

If no changes, exit cleanly.

## Notes

- Config is **per-project** — each repo has its own `.shipkit/sk:config.json`
- `model_overrides` takes precedence over `profile` for individual skills
- Gitignore: `.shipkit/sk:config.json` is personal preference — don't commit it unless the team agrees on a shared profile
