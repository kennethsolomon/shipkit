# /sk:gates

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Steps 12-17 (replaces individual gate commands)
> **Command:** `/sk:gates`
> **Skill file:** `skills/sk:gates/SKILL.md`

---

## Overview

Run all quality gates (lint, test, security, perf, review, e2e) in optimized parallel batches. Replaces manually invoking 6 separate commands by orchestrating them in 4 dependency-aware batches with automatic fix-commit-rerun loops.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Committed implementation code | Working tree (post-commit, step 11) | Yes |
| `tasks/workflow-status.md` | Gate step tracking | Yes |
| `tasks/progress.md` | Failure logging | Yes |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Gate results summary | Terminal (stdout) | Pass/fail status with attempt counts |
| `tasks/workflow-status.md` updates | Steps 12-17 marked done with attempt counts | Updated per gate |
| `tasks/progress.md` entries | Failure logs on 3-strike | Appended on failure |
| Auto-fix commits | Git history | Each gate handles its own fix-commit loop |

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

- Each agent handles its own fix -> auto-commit -> re-run loop internally
- Do NOT proceed to the next batch if the current batch has unresolved failures
- 3-Strike Protocol: if any single gate fails 3 times, stop the entire gates process
- Update `tasks/workflow-status.md` for each gate as it completes (steps 12-17)
- Review (Batch 3) must run in main context, not as an agent
- Performance gate follows the optional gate rules — can be skipped with user confirmation
- All other gates are hard gates that cannot be skipped

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No changes to lint/test | Gates still run — confirm clean state |
| Lint auto-formats code | Batch 2 (tests) picks up formatted code automatically |
| Performance gate skipped | Mark step 15 as "skipped" in workflow-status.md; proceed to Batch 3 |
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
