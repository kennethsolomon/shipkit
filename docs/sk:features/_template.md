# /sk:feature-name

> **Status:** Shipped | In Progress | Planned
> **Type:** Skill | Command | Workflow Step
> **Workflow Position:** Step N of 27 (or "standalone")
> **Command:** `/sk:feature-name`
> **Skill file:** `skills/sk:feature-name/SKILL.md` (or `commands/sk/feature-name.md`)

---

## Overview

One-paragraph description of what this skill/command does, when to use it, and what it produces.

---

## Inputs

What the skill reads before executing:

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Project planning file | Yes/No |
| `tasks/lessons.md` | Past corrections | Yes/No |
| Git diff / branch | Current branch changes | Yes/No |
| ... | ... | ... |

---

## Outputs

What the skill produces when done:

| Output | Destination | Notes |
|--------|-------------|-------|
| Findings report | `tasks/findings-file.md` | Appended, never overwritten |
| Code changes | Working tree | Description |
| ... | ... | ... |

---

## Business Logic

Step-by-step description of what the skill does internally:

1. Step one
2. Step two
3. Step three

Include decision branches, conditional behavior, hard rules.

---

## Hard Rules

Constraints the skill never violates:

- Rule 1
- Rule 2

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| File missing | Graceful fallback — describe |
| No changes detected | Behavior |
| ... | ... |

---

## Error States

| Condition | Error message / behavior |
|-----------|--------------------------|
| ... | ... |

---

## UI/UX Behavior

### CLI Output
Describe the terminal output format.

### When Done
What the skill says when it completes successfully (exact message if defined in SKILL.md).

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:feature-name/SKILL.md` — full implementation spec
- Other related skills or files
