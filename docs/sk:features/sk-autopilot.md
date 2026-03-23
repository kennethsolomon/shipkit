# /sk:autopilot

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone (wraps entire 21-step workflow)
> **Command:** `/sk:autopilot`
> **Skill file:** `skills/sk:autopilot/SKILL.md`

---

## Overview

Hands-free workflow mode that executes all 21 steps with auto-skip, auto-advance, and auto-commit. Same quality gates as manual mode. Stops only for direction approval (after brainstorm), 3-strike failures, and PR push confirmation.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Task description | Command argument | Yes |
| `tasks/todo.md` | Existing plan context | No |
| `tasks/lessons.md` | Active lessons as constraints | Yes |
| `tasks/findings.md` | Prior brainstorm findings | No |
| `tasks/tech-debt.md` | Unresolved tech debt | No |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Feature branch | Git | Auto-named from task |
| Tests + implementation | Working tree | TDD red-green |
| Conventional commit | Git history | Auto-committed, no approval |
| Gate results | Terminal + `tasks/workflow-status.md` | All gates enforced |
| PR | GitHub | Created after user confirms push |

---

## Business Logic

1. Auto-reset workflow tracker if stale
2. Load context files (auto, no prompt)
3. Run brainstorm — present direction summary — **STOP for user approval**
4. On approval: auto-plan, auto-branch, auto-skip detection
5. Write tests (TDD red) → implement (TDD green) → auto-commit
6. Run all quality gates (auto-advance on clean pass)
7. **STOP for PR push confirmation**
8. Create PR, sync features, ask about release

---

## Hard Rules

- ALL 21 steps execute in order (same as manual)
- ALL quality gates enforced (lint, test, security, perf, review, e2e)
- 100% test coverage required on new code
- 0 security issues required
- 3-strike protocol: 3 failures on any step = immediate stop
- PR push ALWAYS requires confirmation (visible to others)

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Brainstorm produces unclear direction | Stops at direction approval — user can steer |
| Gate fails on first attempt | Auto-fix and re-run (same as manual) |
| Gate fails 3 times | Stop immediately, report to user |
| No changes needed (e.g., task already done) | Report "no changes" and stop |

---

## Error States

| Condition | Behavior |
|-----------|----------|
| 3-strike failure | Stop, report what failed + what was tried |
| Git branch conflict | Stop, ask user to resolve |
| Missing `tasks/todo.md` | Create one during plan step |

---

## UI/UX Behavior

### CLI Output
Streams step completion as it runs:
```
[1/21] Loading context...
[2/21] Brainstorming...
Direction: Add user profile page with avatar upload
Scope: 3 new files, 2 modified
Auto-skipping: Migration (no schema changes), Performance (no frontend)
Proceed? (y/n)
```

### When Done
```
All gates passed. Ready to create PR.
Title: feat(profile): add user profile page with avatar upload
Changes: 8 files, 342 lines
Confirm push + PR? (y/n)
```

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:autopilot/SKILL.md` — full implementation spec
- `commands/sk/autopilot.md` — command shortcut
- `docs/sk:features/sk-auto-skip.md` — auto-skip intelligence (used by autopilot)
