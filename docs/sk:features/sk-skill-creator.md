# /sk:skill-creator

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone
> **Command:** `/sk:skill-creator`
> **Skill file:** `skills/sk:skill-creator/SKILL.md`

---

## Overview

Create and iteratively improve skills via: draft, test, evaluate, improve, repeat. Includes description optimization for triggering accuracy, eval-based benchmarking, and guided SKILL.md writing patterns.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Skill intent | User conversation | Yes |
| Existing skill path | Filesystem | No (for improvement mode) |
| Eval set | `evals/evals.json` | No (generated during testing) |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| `SKILL.md` | `skills/<name>/SKILL.md` | Full skill with frontmatter |
| Eval results | `<name>-workspace/` | Per-iteration benchmark data |
| `.skill` package | Filesystem | Optional, for distribution |

---

## Business Logic

1. **Capture intent** — what, when, output format, test cases needed?
2. **Interview + research** — edge cases, I/O formats, dependencies
3. **Write SKILL.md** — name, description, body following writing guide
4. **Test** — spawn with/without-skill agents, grade, aggregate
5. **Improve** — apply feedback, rerun, iterate until satisfied
6. **Description optimization** — 20 trigger/no-trigger queries, 60/40 train/test split

### Writing Guide Patterns

| Pattern | Purpose |
|---------|---------|
| **Anti-Patterns section** | Define 3-5 explicit failure modes the skill must NEVER produce. Prevents subtle failures where the skill technically follows instructions but produces wrong results. |
| **Auto-Clarity escape hatch** | For style-modifying skills: define when to temporarily disable the style (security warnings, destructive ops, confused users). Safety valve for output modification. |
| **Progressive disclosure** | 3-level loading: metadata (always), SKILL.md body (on trigger), bundled resources (on demand) |
| **Example-driven specs** | Before/after pairs baked into the SKILL.md for self-documenting behavior |

---

## Hard Rules

- Description is the primary triggering mechanism — must be specific and slightly "pushy"
- SKILL.md should stay under 500 lines
- Never create skills for malware, exploits, or unauthorized access
- Anti-patterns section recommended for all skills
- Auto-clarity section required for any skill that modifies output style

---

## Related Docs

- `skills/sk:skill-creator/SKILL.md` — full implementation spec
- `skills/sk:skill-creator/references/schemas.md` — JSON schemas for evals
- `skills/sk:skill-creator/agents/grader.md` — eval grading agent
