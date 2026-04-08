# /sk:explain

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone
> **Command:** `/sk:explain [file, function, or concept]`
> **Skill file:** `skills/sk:explain/SKILL.md`

---

## Overview

Explain any code — file, function, module, or concept — with a structured 6-section format: one-sentence summary, mental model, visual ASCII diagram, key details, modification guide, and suggested questions. Scales depth to complexity.

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
| Explanation | Terminal output | 6-section structured format (adds suggested questions) |

---

## Business Logic

1. Parse argument: file path, function name, or concept
2. Read the actual code (never guess from names)
3. Produce 6 sections: summary, mental model, visual diagram, key details, how to modify, suggested questions
4. Scale depth to complexity — compact for utilities, thorough for core modules

---

## Hard Rules

- Read code before explaining — never guess
- Skip sections that don't apply
- Use project's actual names, not generic placeholders

---

## Intensity

| Level | Behavior |
|-------|----------|
| **lite** | One-sentence summary + key details only. Skip diagram and modification guide. |
| **full** | All 5 sections. Scale depth to complexity. Default. |
| **deep** | All 5 sections expanded. Include alternatives, historical context, cross-references. |

Config: `.shipkit/config.json` — `intensity_overrides["sk:explain"]` → global `intensity` → `full`.

---

## Related Docs

- `skills/sk:explain/SKILL.md` — full implementation spec
