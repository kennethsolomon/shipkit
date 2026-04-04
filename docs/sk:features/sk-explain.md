# /sk:explain

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone
> **Command:** `/sk:explain [file, function, or concept]`
> **Skill file:** `skills/sk:explain/SKILL.md`

---

## Overview

Explain any code — file, function, module, or concept — with a structured 5-section format: one-sentence summary, mental model, visual ASCII diagram, key details, and modification guide. Scales depth to complexity.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Target | File path, function name, or concept description | Yes |
| Source code | Codebase files | Yes (read before explaining) |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Explanation | Terminal output | 5-section structured format |

---

## Business Logic

1. Parse argument: file path, function name, or concept
2. Read the actual code (never guess from names)
3. Produce 5 sections: summary, mental model, visual diagram, key details, how to modify
4. Scale depth to complexity — compact for utilities, thorough for core modules

---

## Hard Rules

- Read code before explaining — never guess
- Skip sections that don't apply
- Use project's actual names, not generic placeholders

---

## Related Docs

- `skills/sk:explain/SKILL.md` — full implementation spec
