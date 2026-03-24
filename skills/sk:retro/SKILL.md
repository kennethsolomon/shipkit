---
name: sk:retro
description: Post-ship retrospective analyzing velocity, blockers, and patterns to generate actionable improvements
user_invocable: true
allowed_tools: Read, Glob, Grep, Bash, Write
---

# Retrospective

Analyze completed work after shipping a feature to generate actionable insights for the next iteration.

## When to Use

Run `/sk:retro` after `/sk:finish-feature` or `/sk:release` to reflect on what went well, what didn't, and what to improve. Best run while context is fresh.

## Steps

### 1. Gather Data

Read these files to build the retrospective:

| File | What to Extract |
|------|----------------|
| `tasks/todo.md` | Planned tasks — count total, completed, dropped |
| `tasks/progress.md` | Work log — errors, resolutions, session timestamps |
| `tasks/findings.md` | Design decisions — were they validated? |
| `tasks/lessons.md` | New lessons added during this task |
| `tasks/tech-debt.md` | Tech debt logged during gates |

### 2. Analyze Git History

```bash
# Commits on this branch
git log main..HEAD --oneline --format="%h %s"

# Time span
git log main..HEAD --format="%ai" | tail -1  # first commit
git log main..HEAD --format="%ai" | head -1  # last commit

# Files changed
git diff main..HEAD --stat

# Commit count
git rev-list main..HEAD --count
```

### 3. Calculate Metrics

| Metric | How |
|--------|-----|
| **Completion rate** | Completed tasks / Planned tasks * 100 |
| **Velocity** | Commits per day, files changed per day |
| **Gate performance** | Count fix commits per gate from git log (e.g., `fix(lint):`, `fix(test):`) |
| **Blocker count** | Count "FAIL", "error", "blocked", "3-Strike" entries in tasks/progress.md |
| **Rework rate** | Count fix commits (fix(lint):, fix(test):, etc.) vs feature commits |

### 4. Identify Patterns

- **Recurring blocker**: Same type of issue across multiple gates?
- **Estimation accuracy**: Did planned scope match actual scope? (cross-ref with `/sk:scope-check` if available)
- **Gate friction**: Which gates required the most fix cycles?
- **Previous retro follow-up**: Read previous `tasks/retro-*.md` files — were action items addressed?

### 5. Generate Action Items

Produce 3-5 concrete, actionable improvements:
- Each action item must have: **what** to do, **why** it matters, **when** to apply it
- Prioritize systemic fixes over one-off patches
- Flag recurring unaddressed items from previous retros as process concerns

### 6. Write Report

Save to `tasks/retro-YYYY-MM-DD.md`:

```markdown
# Retrospective — [date] — [task name]

## Metrics
| Metric | Value |
|--------|-------|
| Planned tasks | N |
| Completed | X / N (Y%) |
| Commits | Z |
| Time span | A days |
| Files changed | B (+C/-D) |
| Gate attempts | lint: 1, test: 2, security: 1, ... |
| Blockers | K |
| Rework rate | R% |

## What Went Well
- [data-backed observation]

## What Didn't Go Well
- [data-backed observation, with blocker/error references]

## Patterns
- [recurring theme from this or previous retros]

## Action Items
1. **[What]** — [Why] — Apply during: [When]
2. ...

## Previous Action Item Follow-Up
- [Action from last retro] — [Addressed / Still open]
```

### 7. Summary

Output to user:
```
Retrospective saved to tasks/retro-YYYY-MM-DD.md
Completion: X/N tasks (Y%)  |  Velocity: Z commits/day  |  Blockers: K
Top action: [most important action item]
```

## Model Routing

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |
