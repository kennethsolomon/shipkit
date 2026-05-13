---
name: sk:eval
description: "Define, run, and report on evaluations for agent reliability and code quality."
---

# /sk:eval — Eval-Driven Development

A formal evaluation framework for measuring agent reliability and code quality. Define evals before coding, check during implementation, and report after shipping.

## Usage

```
/sk:eval define <feature>    # create eval definition
/sk:eval check <feature>     # run evals against current state
/sk:eval report              # summary of all eval results
/sk:eval list                # show all defined evals
/sk:eval benchmark <skill>   # measure skill token/quality impact
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> Eval analysis needs reasoning for model-based graders — sonnet for balanced+.

## Eval Types

### Capability Evals

Test whether Claude can accomplish something new:

- "Can it generate a valid migration from a schema description?"
- "Can it write a test that covers all edge cases?"
- "Can it refactor without changing behavior?"

### Regression Evals

Ensure changes don't break existing behavior:

- "Does the login flow still work after auth refactor?"
- "Do all API endpoints still return correct status codes?"
- "Are all existing tests still passing?"

## Grader Types

### Code-Based (Deterministic)

Graded by running commands — pass/fail:

```yaml
grader: code
checks:
  - command: "npm test"
    expect: exit_code_0
  - command: "grep -r 'TODO' src/"
    expect: no_output
  - command: "npx tsc --noEmit"
    expect: exit_code_0
```

### Model-Based (LLM-as-Judge)

Graded by an LLM against a rubric — scored 1-5:

```yaml
grader: model
rubric: |
  Score the implementation on:
  1. Correctness — does it solve the stated problem?
  2. Completeness — are all edge cases handled?
  3. Code quality — is it readable and maintainable?
  4. Security — are there any vulnerabilities?
  5. Performance — any obvious inefficiencies?
threshold: 4.0
```

### Human (Manual Review)

Flagged for human review — generates a checklist:

```yaml
grader: human
checklist:
  - "UI renders correctly on mobile"
  - "Error messages are user-friendly"
  - "Animation feels smooth (60fps)"
```

## Metrics

### pass@k

At least 1 success in k attempts. Used for capability evals where some variance is expected.

```
pass@3: Run the eval 3 times. Pass if at least 1 succeeds.
```

### pass^k

ALL k attempts must succeed. Used for regression evals where consistency is required.

```
pass^3: Run the eval 3 times. Pass only if all 3 succeed.
```

## Storage

### Eval Definition

Stored in `.claude/evals/[feature].md`:

```markdown
---
feature: user-authentication
type: capability
grader: code
created: 2026-03-25
pass_metric: pass@1
---

## Description
Verify the OAuth2 login flow works end-to-end.

## Checks
- [ ] `npm test -- --grep "auth"` passes
- [ ] `curl -s localhost:3000/auth/google` returns 302
- [ ] `grep -r "hardcoded.*secret" src/` returns nothing

## History
| Date | Result | Score | Notes |
|------|--------|-------|-------|
```

### Eval Results

Appended to `.claude/evals/[feature].log`:

```
[2026-03-25T10:30:00Z] PASS — pass@1 (1/1 succeeded)
  check_1: npm test (exit 0) ✓
  check_2: curl auth redirect (302) ✓
  check_3: no hardcoded secrets ✓
```

## Skill Benchmarking

Compare a skill's output against a baseline (no skill) across identical prompts. Measures token usage, output quality, and consistency. Adapted from the [Caveman benchmark harness](https://github.com/JuliusBrussee/caveman/blob/main/benchmarks/run.py).

### `/sk:eval benchmark <skill-name>`

**Step 1 — Load or create prompt set:**

Check for `.claude/evals/<skill-name>/prompts.json`:

```json
{
  "version": 1,
  "prompts": [
    {
      "id": "descriptive-slug",
      "category": "debugging|bugfix|setup|explanation|refactor|architecture|code-review|devops|implementation",
      "prompt": "The full user prompt to test with"
    }
  ]
}
```

If no prompt set exists, generate 5–10 diverse prompts that match the skill's trigger conditions. Present to user for confirmation before running.

**Step 2 — Run trials:**

For each prompt, spawn 2 agents in parallel:
- **With-skill:** Load the skill's SKILL.md as system context, run the prompt
- **Baseline:** Run the same prompt with no skill loaded

Use `temperature: 0` for reproducibility. Run N trials per mode (default: 1, configurable with `--trials N`).

Save all outputs to `.claude/evals/<skill-name>/results/`:
```
results/
├── benchmark_YYYYMMDD_HHMMSS.json
└── ...
```

**Step 3 — Compute stats:**

For each prompt, compute:
- **Token delta:** `baseline_output_tokens - skill_output_tokens` (savings %)
- **Quality score:** If model-based grader is defined, run it on both outputs

Aggregate:
- Median token savings across all prompts
- Min/max savings range
- Average quality score delta (if graded)

**Step 4 — Output report:**

```markdown
## Skill Benchmark: <skill-name>

| Prompt | Baseline (tokens) | With Skill (tokens) | Saved |
|--------|------------------:|-------------------:|------:|
| [label] | NNN | NNN | NN% |
| **Average** | **NNN** | **NNN** | **NN%** |

*Range: NN%–NN% savings across prompts.*

Quality: [average score delta if graded, or "not graded"]
```

Save results JSON with metadata (model, date, trials, skill hash).

Also write a `worked/{skill-name}-YYYYMMDD/` folder alongside the results:

```
worked/{skill-name}-YYYYMMDD/
├── prompts.md        # the prompts used (human-readable)
├── outputs/          # raw agent outputs, one file per prompt
│   ├── {slug}-with-skill.md
│   └── {slug}-baseline.md
└── review.md         # honest verdict: what the skill got right, wrong, and missed
```

`review.md` must be honest — note failures, not just wins. This is the source of truth for whether the skill actually improved behavior.

**Step 5 — Update README (optional):**

If `--update-readme` flag is passed and README.md contains `<!-- BENCHMARK-TABLE-START -->` / `<!-- BENCHMARK-TABLE-END -->` markers, replace the content between them with the new table.

## Workflow Integration

### Before Coding (define)

```
/sk:eval define user-authentication
```

Creates the eval definition with checks derived from the task requirements.

### During Implementation (check)

```
/sk:eval check user-authentication
```

Runs all checks and reports pass/fail. Use during step 5 (Write Tests + Implement) to verify progress.

### After Shipping (report)

```
/sk:eval report
```

Summary of all evals:

```
=== Eval Report ===

  user-authentication    PASS  pass@1  (3 checks, 3 passed)
  api-v2-endpoints       PASS  pass^3  (5 checks, 5 passed x3)
  queue-reliability      FAIL  pass@3  (2 checks, 0/3 succeeded)

  Overall: 2/3 passing (67%)

  Action: queue-reliability needs investigation
```
