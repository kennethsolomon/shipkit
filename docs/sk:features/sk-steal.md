# /sk:steal

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone
> **Command:** `/sk:steal`
> **Skill file:** `skills/sk:steal/SKILL.md`

---

## Overview

Review an external source (GitHub repo, article URL, screenshot, pasted code) and extract ideas to adapt into ShipKit or the current project. Fetches, indexes, and analyzes the source across 3 parallel lanes: extract ideas, compare with existing, draft adaptations. Outputs a steal report with "Worth Stealing" / "Already Covered" / "Not Worth It" tables.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| External source | GitHub URL, article URL, screenshot path, pasted text | Yes |
| Current codebase | Skills, hooks, rules, agents, CLAUDE.md | Yes (for comparison) |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Steal report | Terminal output | Comparison table with recommendations |
| Adapted files | Working tree | Skills, hooks, rules created/modified per approval |

---

## Business Logic

1. Classify source type (GitHub, URL, screenshot, text)
2. Fetch and index content via context-mode or Read
3. Run 3 parallel analysis lanes: extract ideas, compare with existing, draft adaptations
4. Present steal report with actionable table
5. Implement approved items following ShipKit conventions

---

## Hard Rules

- Always compare before suggesting — don't recommend what we already have
- Never copy code verbatim — adapt to our conventions
- Credit the source in commit messages
- Skip ideas that only work for a tech stack we don't use

---

## Related Docs

- `skills/sk:steal/SKILL.md` — full implementation spec
- `.claude/docs/maintenance-guide.md` — for derived file updates when adapting
