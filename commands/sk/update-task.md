---
description: "Mark current task done in tasks/todo.md and log completion to tasks/progress.md."
---

# /sk:update-task

Mark the current task as complete and log progress.

## Steps

### 1. Identify Current Task
- Read `tasks/todo.md` and find the task that matches the current branch or the most recently worked-on incomplete task
- Read `tasks/progress.md` to understand what was done

### 2. Mark Task Done
- In `tasks/todo.md`, change the task's checkbox from `[ ]` to `[x]`
- If the task has subtasks, verify all subtasks are also checked

### 3. Log Completion
- Append a completion entry to `tasks/progress.md`:

```markdown
### [YYYY-MM-DD] [Task title] — COMPLETED
- Branch: `<branch-name>`
- Changes: [brief summary of what was implemented]
- Tests: [test count and coverage]
- Files changed: [count]
```

### 4. Check for Remaining Work
- Show how many tasks remain in `tasks/todo.md`
- Show the next incomplete task (if any)

### 5. Confirm
- Show the user what was marked done and logged
