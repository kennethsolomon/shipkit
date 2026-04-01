---
name: sk:gates
description: Run all quality gates in optimized parallel batches — one command instead of seven
allowed-tools: Agent, Read, Write, Bash, Glob, Grep
---

# Gates Orchestrator

Run all quality gates (lint, test, security, perf, deps-audit, review, e2e) in optimized batches. Replaces manually invoking 7 separate commands.

## When to Use

Run `/sk:gates` after `/sk:smart-commit` completes (step 6). This single command covers all quality gates (step 7 of the workflow).

## Execution Strategy

Gates are organized into 4 batches for maximum parallelism while respecting dependencies:

### Batch 1 — Parallel Agents (lint + security + perf + deps-audit)

Launch 4 agents simultaneously:

1. **Linter agent** — runs all formatters, analyzers
2. **`security-reviewer` agent** — OWASP audit on changed files (read-only; reports findings, does not fix)
3. **`performance-optimizer` agent** — bundle, N+1, Core Web Vitals, memory (worktree isolation — finds AND fixes critical/high issues)
   **Auto-skip:** If NO frontend keywords (component, view, page, CSS, UI, form, modal, button, react, vue, svelte, blade) AND NO database keywords (migration, schema, table, column, model, database, foreign key, index, seed) appear in `tasks/todo.md`, skip this agent and log: `Auto-skipped: Performance (no frontend or database keywords in plan)`.
4. **`/sk:deps-audit` skill** — CVE scan, license compliance, outdated packages across all detected ecosystems (npm, Composer, Cargo, pip, Go, Bundler). Auto-fixes safe patch/minor bumps. Writes findings to `tasks/security-findings.md`.

These 4 have no dependencies on each other. Run them in parallel using the Agent tool.

Wait for all 4 to complete. Collect results. Apply security fixes from `security-reviewer` findings in the main context. `performance-optimizer` commits its own fixes from its worktree — merge them in. `/sk:deps-audit` auto-commits any dependency bumps it applied.
Post checkpoint: `[Checkpoint] Batch 1 complete: lint + security + perf + deps-audit. Next: Batch 2 — test.`

### Batch 2 — Test Agent (sequential, needs lint fixes)

After Batch 1 completes (lint may have auto-formatted code):

4. **Test runner agent** — runs all test suites, ensures 100% coverage on new code
Post checkpoint: `[Checkpoint] Batch 2 complete: test. Next: Batch 3 — review.`

### Batch 3 — Review (main context, needs test confirmation)

After Batch 2 completes:

5. **`code-reviewer` agent** — 7-dimension review (correctness, security, performance, reliability, design, best practices, testing). Read-only — reports findings. Main context applies fixes and re-runs.
Post checkpoint: `[Checkpoint] Batch 3 complete: review. Next: Batch 4 — e2e.`

### Batch 4 — E2E Agent (needs review fixes)

After Batch 3 completes:

6. **E2E tester agent** — runs full E2E verification using scenarios written by `qa-engineer` during implementation
Post checkpoint: `[Checkpoint] Batch 4 complete: e2e. All gates done.`

## Gate Results

After all 4 batches complete, output a summary:

```
=== Gate Results ===
Lint:       clean (attempt N)
Security:   0 findings (attempt N)
Perf:       0 critical/high (attempt N)
Deps Audit: 0 CVEs (attempt N)
Tests:      X passed, 0 failed (attempt N)
Review:     0 issues (attempt N)
E2E:        Y scenarios passed (attempt N)

All gates passed. Run /sk:update-task
```

## Failure Handling

- Each agent handles its own fix → re-run loop internally (up to 2 self-fix attempts)
- **Squash gate commits:** When a gate requires fixes, collect all fixes for that pass, then make ONE commit: `fix(<gate>): resolve <gate> issues`. Do not commit after each individual fix.
- Do NOT proceed to the next batch if the current batch has unresolved failures

**Same-failure detection:** Track the first 30 chars of each gate's error message. If identical across 2 consecutive fix attempts, trigger architect diagnosis immediately — do not wait for a 3rd attempt.

**On 3rd failure of any gate (or 2nd if same-failure detected):**
1. Gates orchestrator spawns `architect` agent:
   ```
   Task(subagent_type="architect", model="sonnet", prompt="Gate [name] failing after 2 fix attempts.
   Error: [error output]
   Diagnose root cause and recommend a specific fix.")
   ```
2. Main context applies the architect's recommendation
3. Re-run the failed gate (this is the final attempt)
4. If still failing → 3-strike protocol below

## 3-Strike Protocol

If any single gate fails after architect-assisted retry:
1. Stop the entire gates process
2. Log the failure to `tasks/progress.md`
3. Report to user: gate name, error, architect diagnosis, what was tried
4. Do NOT mark the step as done

## Model Routing

The orchestrator itself runs in the main context. Agents use their own model routing:
- Linter: haiku (mechanical)
- Deps audit: haiku (mechanical)
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
