---
description: "Hands-free workflow — all 8 steps, auto-skip, auto-advance, auto-commit. Stops only for direction approval and PR push."
---

# /sk:autopilot

Run the full ShipIt workflow in hands-free mode.

Usage: `/sk:autopilot <task description>`

Executes all 8 workflow steps with:
- **Auto-skip** — optional steps skipped when clearly not needed
- **Auto-advance** — no manual step transitions
- **Auto-commit** — conventional format, no approval prompt
- **Same quality gates** — all gates enforced, same fix loops

Stops only for:
1. Direction approval (after brainstorm)
2. 3-strike failures
3. PR push confirmation

See `skills/sk:autopilot/SKILL.md` for full details.
