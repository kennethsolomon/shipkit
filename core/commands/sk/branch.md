---
description: "Create a feature branch from the current task in tasks/todo.md."
disable-model-invocation: true
---

# /sk:branch

Create a feature branch for the current task.

## Steps

### 1. Read Current Task
- Read `tasks/todo.md` and find the next incomplete task (first unchecked checkbox)
- Extract a short name from the task description

### 2. Check Prerequisites
- Ensure working directory is clean (`git status`). If dirty, warn the user and stop.
- Ensure you're on the main branch. If not, ask the user to confirm branching from the current branch.

### 3. Pull Latest
```bash
git pull origin main
```

### 4. Create Branch
- Generate branch name: `feature/<short-task-name>` (kebab-case, max 50 chars)
  - Example task: "Add server metrics dashboard" → `feature/server-metrics-dashboard`
  - Example task: "Fix duplicate episode notifications" → `fix/duplicate-episode-notifications`
- Use `fix/` prefix for bug fixes, `feature/` for new features, `refactor/` for refactoring
```bash
git checkout -b <branch-name>
```

### 5. Confirm
- Show the user the branch name created
- Show which task this branch is for
