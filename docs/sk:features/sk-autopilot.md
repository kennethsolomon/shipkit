# /sk:autopilot

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone (wraps entire 8-step workflow)
> **Command:** `/sk:autopilot`
> **Skill file:** `skills/sk:autopilot/SKILL.md`

---

## Overview

Hands-free workflow mode that executes all 8 steps with auto-skip, auto-advance, and auto-commit. Same quality gates as manual mode. Stops only for direction approval (after brainstorm), 3-strike failures, and PR push confirmation.

Includes automatic task classification (Step 0) — autopilot silently routes to `/sk:deep-dive` for unknown-cause bugs or `/sk:deep-interview` for vague feature requests before entering the main workflow.

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
| Gate results | Terminal | All gates enforced |
| PR | GitHub | Created after user confirms push |

---

## Business Logic

### Step 0 — Task Classification (auto, silent)

Before loading context, autopilot classifies the input:

| Check | Signals | Action |
|-------|---------|--------|
| **A — Unknown-cause bug** | bug/error/broken/crash/failing + no file:line, no "the issue is X" | Invoke `/sk:deep-dive` → produces `tasks/spec.md` → continue as bug fix |
| **B — Vague feature** | No concrete anchors (no file paths, functions, error messages), open-ended verbs | Invoke `/sk:deep-interview` → produces `tasks/spec.md` → continue to Step 1 |
| **C — Clear input** | Has concrete anchors or bounded scope | Skip Step 0, proceed directly to Step 1 |

Logs are surfaced when routing occurs:
- `[Autopilot] Bug with unknown root cause — running /sk:deep-dive to investigate.`
- `[Autopilot] Input is open-ended — running /sk:deep-interview to crystallize requirements.`

### Steps 1–8

1. Load context files (auto, no prompt)
2. Run brainstorm — present direction summary with **explicit acceptance criteria** — **STOP for user approval**

   Direction approval format:
   ```
   Direction: [summary]
   Scope: [what changes]
   Acceptance Criteria:
     - [ ] [criterion 1 — testable, specific]
     - [ ] [criterion 2]
   Auto-skipping: [list]
   Proceed? (y/n)
   ```

3. On approval: auto-plan, auto-branch, auto-skip detection
4. Write tests (TDD red) → implement (TDD green) → auto-commit
5. Run all quality gates (auto-advance on clean pass)
6. **Step 7.5 — Verify acceptance criteria** before PR push:
   - Each criterion marked ✓ or ✗
   - All must be ✓ before continuing to Step 8
   - If any ✗: fix → re-run gates → re-verify
7. **STOP for PR push confirmation**
8. Create PR, sync features, ask about release

---

## Hard Rules

- ALL 8 steps execute in order (same as manual)
- ALL quality gates enforced (lint, test, security, perf, review, e2e)
- 100% test coverage required on new code
- 0 security issues required
- 3-strike protocol: 3 failures on any step = immediate stop
- PR push ALWAYS requires confirmation (visible to others)
- Acceptance criteria verification (step 7.5) must pass before PR push

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Unknown-cause bug input | Step 0 Check A → routes to `/sk:deep-dive` automatically |
| Vague/open-ended feature input | Step 0 Check B → routes to `/sk:deep-interview` automatically |
| Brainstorm produces unclear direction | Stops at direction approval — user can steer |
| Gate fails on first attempt | Auto-fix and re-run (same as manual); ultraqa cycling on repeated failures |
| Gate fails 3 times | Stop immediately, report to user |
| No changes needed (e.g., task already done) | Report "no changes" and stop |
| Acceptance criteria not all passing | Fix and re-gate before PR |

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
[Autopilot] Input is open-ended — running /sk:deep-interview to crystallize requirements.
...
[1/8] Loading context...
[2/8] Brainstorming...
Direction: Add user profile page with avatar upload
Scope: 3 new files, 2 modified
Acceptance Criteria:
  - [ ] User can upload avatar image (PNG/JPG, max 5MB)
  - [ ] Avatar displayed on profile page
  - [ ] Avatar persists across sessions
Auto-skipping: Migration (no schema changes), Performance (no frontend)
Proceed? (y/n)
```

### When Done
```
Verifying acceptance criteria...
  ✓ User can upload avatar image
  ✓ Avatar displayed on profile page
  ✓ Avatar persists across sessions
All criteria passing. Ready to create PR.
Title: feat(profile): add user profile page with avatar upload
Confirm push + PR? (y/n)
```

---

## Intensity Routing

Autopilot auto-selects output intensity per phase. Resolution: `intensity_overrides["sk:<phase>"]` → phase auto-select → global `intensity` → `full`.

| Phase | Auto-selected | Why |
|-------|--------------|-----|
| brainstorm | full | Need substance for direction approval |
| design | full | Design decisions need clarity |
| write-plan | full | Plans must be decision-complete |
| write-tests | lite | Tests are code — minimal prose |
| execute-plan | lite | Implementation — minimal prose |
| scope-check | lite | Pass/fail comparison |
| gates | lite | Pass/fail, not essays |
| review | deep | Security/perf findings need full detail |
| finalize | full | PR descriptions need clarity |
| learn | lite | Pattern extraction — concise |
| retro | lite | Bullets, not paragraphs |

Config: `.shipkit/config.json` — `intensity` (global default) and `intensity_overrides` (per-skill).

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:autopilot/SKILL.md` — full implementation spec
- `commands/sk/autopilot.md` — command shortcut
- `docs/sk:features/sk-auto-skip.md` — auto-skip intelligence (used by autopilot)
- `docs/sk:features/sk-deep-interview.md` — requirements gathering (auto-routed by Step 0)
- `docs/sk:features/sk-deep-dive.md` — bug investigation (auto-routed by Step 0)
