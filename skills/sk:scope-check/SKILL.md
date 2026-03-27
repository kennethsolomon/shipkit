---
name: sk:scope-check
description: Compare current implementation against the plan to detect scope creep
allowed_tools: Read, Glob, Grep, Bash
---

# Scope Check

Compare the current implementation against `tasks/todo.md` to detect scope creep and unplanned additions.

## When to Use

Run `/sk:scope-check` mid-implementation (during or after step 10) to verify you're building what was planned — no more, no less. Useful when implementation feels like it's growing beyond the original plan.

## Steps

### 1. Read the Plan

- Read `tasks/todo.md` — extract all planned tasks (checkboxes)
- Count total planned tasks, completed tasks, and remaining tasks
- List planned files/areas from task descriptions

### 2. Analyze Actual Changes

- Run `git diff main..HEAD --stat` to get files changed, insertions, deletions
- Run `git diff main..HEAD --name-only` to list all changed files
- Count new files created vs. files modified
- Identify files changed that are NOT mentioned in any todo.md task

### 3. Compare Planned vs. Actual

For each changed file, trace it back to a planned task:
- **Planned**: File change is directly described in a todo.md checkbox
- **Supporting**: File change is a reasonable dependency of a planned task (e.g., updating imports after moving a function)
- **Unplanned**: File change has no clear connection to any planned task — this is scope creep

### 4. Calculate Scope Bloat

```
Planned tasks:    N checkboxes in todo.md
Actual changes:   M files changed
Unplanned items:  U files with no matching task
Scope bloat:      (U / M) * 100 = X%
```

### 5. Classify

| Classification | Bloat % | Recommendation |
|---------------|---------|----------------|
| **On Track** | 0-10% | Proceeding as planned. Minor supporting changes are normal. |
| **Minor Creep** | 10-25% | Some unplanned additions detected. Review if they're necessary. |
| **Significant Creep** | 25-50% | Scope has grown substantially. Consider splitting into separate tasks. |
| **Out of Control** | >50% | More unplanned work than planned. Stop and reassess with `/sk:change`. |

### 6. Output Report

```markdown
## Scope Check Report — [date]

**Plan**: [N] tasks in tasks/todo.md
**Completed**: [X] / [N] tasks
**Files changed**: [M] files (+[insertions] / -[deletions])
**Unplanned changes**: [U] files

### Classification: [On Track | Minor Creep | Significant Creep | Out of Control] ([X]%)

### Planned Changes
- [file] — task: [matching checkbox text]
- ...

### Supporting Changes
- [file] — supports: [which planned task]
- ...

### Unplanned Changes
- [file] — no matching task found
- ...

### Recommendation
[Actionable advice based on classification]
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | haiku |
| `budget` | haiku |
