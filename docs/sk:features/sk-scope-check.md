# /sk:scope-check

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone (recommended during or after step 10)
> **Command:** `/sk:scope-check`
> **Skill file:** `skills/sk:scope-check/SKILL.md`

---

## Overview

Compare the current implementation against `tasks/todo.md` to detect scope creep and unplanned additions. Produces a scope check report that classifies each changed file as planned, supporting, or unplanned, and calculates a scope bloat percentage with actionable recommendations.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Planned tasks and checkboxes | Yes |
| Git diff (`main..HEAD`) | Changed files, insertions, deletions | Yes |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Scope check report | Terminal (stdout) | Markdown-formatted report with classification |

---

## Business Logic

1. **Read the plan** — parse `tasks/todo.md`, extract all checkboxes, count total/completed/remaining tasks, list planned files and areas.
2. **Analyze actual changes** — run `git diff main..HEAD --stat` and `git diff main..HEAD --name-only` to get files changed, insertions, deletions, new vs. modified file counts.
3. **Compare planned vs. actual** — for each changed file, trace it back to a planned task and classify:
   - **Planned**: directly described in a todo.md checkbox.
   - **Supporting**: reasonable dependency of a planned task (e.g., import updates).
   - **Unplanned**: no clear connection to any planned task (scope creep).
4. **Calculate scope bloat** — `(Unplanned files / Total changed files) * 100`.
5. **Classify** — map bloat percentage to a severity level:
   - 0-10%: On Track
   - 10-25%: Minor Creep
   - 25-50%: Significant Creep
   - >50%: Out of Control
6. **Output report** — render markdown report with planned/supporting/unplanned file lists and recommendation.

---

## Hard Rules

- Never modifies any files — read-only analysis
- Classification must be data-driven: every changed file must be traced to a task or marked unplanned
- Bloat percentage is always calculated as `(unplanned / total changed) * 100`
- "Out of Control" classification recommends stopping and reassessing with `/sk:change`

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No changes on branch | Report "no changes detected" — nothing to check |
| `tasks/todo.md` missing | Error — cannot compare without a plan |
| All changes are supporting | Report 0% bloat, classify as On Track |
| Branch has no commits ahead of main | Report "branch is up to date with main" |

---

## Error States

| Condition | Error message / behavior |
|-----------|--------------------------|
| Not on a feature branch | Warn that comparison is against `main` — may be inaccurate |
| `tasks/todo.md` not found | Stop with: "No plan found in tasks/todo.md — cannot run scope check" |
| Git not available | Stop with git error context |

---

## UI/UX Behavior

### CLI Output
Renders a markdown-formatted scope check report to the terminal including: plan summary, file classification table, bloat percentage, severity classification, and recommendation.

### When Done
```
Scope Check: [Classification] ([X]% bloat)
Planned: N | Supporting: S | Unplanned: U | Total: M files
```

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:scope-check/SKILL.md` — full implementation spec
- `/sk:change` — recommended follow-up when scope is "Out of Control"
- `/sk:execute-plan` — step 10, where scope check is most useful
