---
description: "Smart entry point — classifies your task and routes to the optimal flow, mode, and agent strategy."
---

# /sk:start

Smart entry point for all ShipIt work. Classifies your task and recommends the best workflow configuration.

Usage: `/sk:start <task description>`

Examples:
```
/sk:start add user profile page with avatar upload
/sk:start fix login redirect loop
/sk:start urgent: payments failing in production
/sk:start bump lodash to latest version
```

**What it does:**
1. **Classifies** — detects if it's a feature, bug, hotfix, or small change
2. **Detects scope** — full-stack, frontend-only, or backend-only
3. **Recommends** — optimal flow + mode (autopilot/manual) + agents (team/solo)
4. **Routes** — enters the chosen workflow after your confirmation

**Override flags:**
- `--manual` — force step-by-step mode
- `--team` / `--no-team` — force team or solo agents
- `--debug` / `--hotfix` / `--fast-track` — force a specific flow

See `skills/sk:start/SKILL.md` for full details.
