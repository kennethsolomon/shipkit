# /sk:eval

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone (used during and after implementation)
> **Command:** `/sk:eval`
> **Skill file:** `skills/sk:eval/SKILL.md`

---

## Overview

Formal evaluation framework for measuring agent reliability and code quality. Define evals before coding, check during implementation, report after shipping. Includes skill benchmarking for measuring token/quality impact.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Feature name | Command argument | Yes (for define/check) |
| Skill name | Command argument | Yes (for benchmark) |
| `.claude/evals/<feature>.md` | Eval definitions | Yes (for check/report) |
| `.claude/evals/<skill>/prompts.json` | Benchmark prompt set | No (auto-generated if missing) |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Eval definition | `.claude/evals/<feature>.md` | YAML frontmatter + checks |
| Eval results | `.claude/evals/<feature>.log` | Timestamped pass/fail |
| Benchmark results | `.claude/evals/<skill>/results/` | JSON with metadata, token stats |
| Benchmark report | Terminal | Markdown table with savings % |

---

## Subcommands

| Command | Purpose |
|---------|---------|
| `define <feature>` | Create eval definition with checks from task requirements |
| `check <feature>` | Run all checks, report pass/fail |
| `report` | Summary of all eval results |
| `list` | Show all defined evals |
| `benchmark <skill>` | Compare skill output vs baseline across identical prompts |

---

## Skill Benchmarking

Adapted from the [Caveman benchmark harness](https://github.com/JuliusBrussee/caveman).

1. **Load/create prompt set** — 5-10 diverse prompts matching the skill's trigger conditions
2. **Run trials** — parallel with-skill vs baseline agents, `temperature: 0`
3. **Compute stats** — median token delta, savings %, quality score delta
4. **Output report** — markdown table with per-prompt and average results
5. **Optional README update** — auto-patch between `<!-- BENCHMARK-TABLE-START/END -->` markers

---

## Grader Types

| Type | How | Use for |
|------|-----|---------|
| **Code** | Run commands, check exit codes | Deterministic tests |
| **Model** | LLM scores against rubric (1-5) | Subjective quality |
| **Human** | Generate checklist for manual review | UI/UX verification |

---

## Metrics

| Metric | Meaning |
|--------|---------|
| `pass@k` | At least 1 success in k attempts (capability evals) |
| `pass^k` | ALL k attempts succeed (regression evals) |

---

## Hard Rules

- Eval definitions must have testable checks — no vague criteria
- Benchmark uses `temperature: 0` for reproducibility
- Results include metadata (model, date, trials, skill hash) for traceability

---

## Related Docs

- `skills/sk:eval/SKILL.md` — full implementation spec
- `skills/sk:skill-creator/SKILL.md` — uses eval infrastructure for skill testing
