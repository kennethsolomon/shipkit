---
name: sk:gates
description: Run all quality gates in optimized parallel batches — one command instead of six
allowed_tools: Agent, Read, Write, Bash, Glob, Grep
---

# Gates Orchestrator

Run all quality gates (lint, test, security, perf, review, e2e) in optimized batches. Replaces manually invoking 6 separate commands.

## When to Use

Run `/sk:gates` after committing implementation code (step 11). This single command handles steps 12-17 of the workflow.

## Execution Strategy

Gates are organized into 4 batches for maximum parallelism while respecting dependencies:

### Batch 1 — Parallel Agents (lint + security + perf)

Launch 3 agents simultaneously:

1. **Linter agent** — runs all formatters, analyzers, dep audits
2. **Security auditor agent** — OWASP audit on changed files
3. **Performance auditor agent** — bundle, N+1, Core Web Vitals, memory

These 3 have no dependencies on each other. Run them in parallel using the Agent tool.

Wait for all 3 to complete. Collect results.

### Batch 2 — Test Agent (sequential, needs lint fixes)

After Batch 1 completes (lint may have auto-formatted code):

4. **Test runner agent** — runs all test suites, ensures 100% coverage on new code

### Batch 3 — Review (main context, needs test confirmation)

After Batch 2 completes:

5. **Review** — runs `/sk:review` in the main context (NOT as an agent) because review needs deep code understanding and access to the full conversation history

### Batch 4 — E2E Agent (needs review fixes)

After Batch 3 completes:

6. **E2E tester agent** — runs full E2E verification

## Gate Results

After all 4 batches complete, output a summary:

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

## Failure Handling

- Each agent handles its own fix → re-run loop internally
- **Squash gate commits:** When a gate requires fixes, collect all fixes for that pass, then make ONE commit: `fix(<gate>): resolve <gate> issues`. Do not commit after each individual fix.
- If any agent fails after 3 attempts → stop all gates and report to user
- Do NOT proceed to the next batch if the current batch has unresolved failures

## 3-Strike Protocol

If any single gate fails 3 times:
1. Stop the entire gates process
2. Log the failure to `tasks/progress.md`
3. Report to user with details of what failed and what was tried
4. Do NOT mark the step as done

## Model Routing

The orchestrator itself runs in the main context. Agents use their own model routing:
- Linter: haiku (mechanical)
- Test runner: sonnet
- Security auditor: sonnet
- Perf auditor: sonnet
- E2E tester: sonnet
- Review: main context model (opus or sonnet depending on profile)

| Profile | Orchestrator Model |
|---------|-------------------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |
