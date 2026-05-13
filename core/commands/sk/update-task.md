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

### 2.5. Mark Resolved Tech Debt

- Read `tasks/tech-debt.md` if it exists
- Find any unresolved entries (entries with no `Resolved:` line) whose `File:` or `Issue:` description relates to files or features changed in the current task (cross-reference with `tasks/todo.md` plan and current branch diff via `git diff main..HEAD --name-only`)
- For each matched entry, append this line directly after the entry's `Severity:` line:
  `Resolved: [YYYY-MM-DD] — [current branch name]`
- Never delete entries — only append the `Resolved:` line
- If `tasks/tech-debt.md` doesn't exist or no matches found: skip silently

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
