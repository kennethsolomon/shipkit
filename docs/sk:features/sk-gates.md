# /sk:gates

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Step 7 (replaces individual gate commands)
> **Command:** `/sk:gates`
> **Skill file:** `skills/sk:gates/SKILL.md`

---

## Overview

Run all quality gates (lint, test, security, perf, review, e2e) in optimized parallel batches. Replaces manually invoking 6 separate commands by orchestrating them in 4 dependency-aware batches with automatic fix-commit-rerun loops.

Each batch completion posts a one-line `[Checkpoint]` status line (`[Checkpoint] Batch N complete: <gates>. Next: Batch N+1 — <gates>.`) for progress visibility during long-running gate runs.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Committed implementation code | Working tree (post-commit, step 11) | Yes |
| `tasks/todo.md` | Task progress tracking | No |
| `tasks/progress.md` | Failure logging | Yes |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Gate results summary | Terminal (stdout) | Pass/fail status with attempt counts |
| `tasks/progress.md` entries | Failure logs on 3-strike | Appended on failure |
| Auto-fix commits | Git history | One squash commit per gate pass |

---

## Business Logic

1. **Batch 1 — Parallel** (lint + security + perf): Launch 3 agents simultaneously:
   - Linter agent: formatters, analyzers, dependency audits
   - Security auditor agent: OWASP audit on changed files
   - Performance auditor agent: bundle, N+1, Core Web Vitals, memory
   - Wait for all 3 to complete. Collect results.

2. **Batch 2 — Sequential** (tests): After Batch 1 completes (lint may have auto-formatted):
   - Test runner agent: all test suites, 100% coverage on new code

3. **Batch 3 — Main context** (review): After Batch 2 completes:
   - Review runs in the main context (not as an agent) for full conversation history access
   - Includes simplify pre-pass + multi-dimensional review

4. **Batch 4 — Sequential** (E2E): After Batch 3 completes:
   - E2E tester agent: full end-to-end verification

5. **Summary** — output pass/fail status for all 6 gates with attempt counts.

---

## Hard Rules

- Each agent handles its own fix -> re-run loop internally
- Squash gate commits: one `fix(<gate>): ...` commit per gate pass, not per individual fix
- Do NOT proceed to the next batch if the current batch has unresolved failures
- 3-Strike Protocol: if any single gate fails 3 times, stop the entire gates process
- Review (Batch 3) must run in main context, not as an agent
- Performance gate follows the optional gate rules — can be skipped with user confirmation
- All other gates are hard gates that cannot be skipped

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No changes to lint/test | Gates still run — confirm clean state |
| Lint auto-formats code | Batch 2 (tests) picks up formatted code automatically |
| Performance gate skipped | Log "Auto-skipped: Performance"; proceed to Batch 3 |
| One Batch 1 agent fails while others pass | Wait for all Batch 1 agents to finish, then handle failures before Batch 2 |

---

## Error States

| Condition | Error message / behavior |
|-----------|--------------------------|
| Gate fails 3 times | Stop all gates. Log to `tasks/progress.md`. Report to user with failure details. Do NOT mark step as done. |
| No committed code on branch | Error: "No commits found — run `/sk:smart-commit` first" |
| Agent crashes | Treat as a gate failure. Log and retry up to 3 times. |

---

## UI/UX Behavior

### CLI Output
Progress updates as each batch starts and completes. Final summary table.

### When Done
```
=== Gate Results ===
Lint:     clean (attempt N)
Security: 0 findings (attempt N)
Perf:     0 critical/high (attempt N)
Tests:    X passed, 0 failed (attempt N)
Review:   0 issues (attempt N)
E2E:      Y scenarios passed (attempt N)

All gates passed. Run /sk:update-task
```

---

## Intensity

Gates default to **lite** — pass/fail results, not essays. The review gate (Batch 3) uses its own intensity setting.

| Level | Behavior |
|-------|----------|
| **lite** | One-line per gate result. Compact summary. Default for gates. |
| **full** | Include fix details and agent recommendations. |
| **deep** | Full agent output for each gate. Verbose logging. |

Config: `.shipkit/config.json` — `intensity_overrides["sk:gates"]` → global `intensity` → `lite`.

---

## Platform Notes

N/A — CLI tool only. Agent model routing per gate:
- Linter: haiku (mechanical)
- Test runner: sonnet
- Security auditor: sonnet
- Perf auditor: sonnet
- E2E tester: sonnet
- Review: main context model (opus or sonnet depending on profile)

---

## Related Docs

- `skills/sk:gates/SKILL.md` — full implementation spec
- `/sk:lint` — individual lint gate (step 12)
- `/sk:test` — individual test gate (step 13)
- `/sk:security-check` — individual security gate (step 14)
- `/sk:perf` — individual perf gate (step 15)
- `/sk:review` — individual review gate (step 16)
- `/sk:e2e` — individual E2E gate (step 17)
- `/sk:fast-track` — uses `/sk:gates` as its quality gate step
