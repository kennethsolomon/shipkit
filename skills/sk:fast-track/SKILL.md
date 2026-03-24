---
name: sk:fast-track
description: Abbreviated workflow for small, clear changes — skip planning ceremony, keep all quality gates
user_invocable: true
allowed_tools: Read, Write, Bash, Glob, Grep, Agent, Skill
---

# Fast-Track Flow

Abbreviated workflow for small, well-understood changes. Skips brainstorm, design, plan, and write-tests phases but still enforces all quality gates.

## When to Use

- Config changes, dependency bumps, copy/wording changes
- Small refactors with obvious scope
- Adding a missing test for existing code
- Fixing a typo or updating documentation
- Any change where the "what" is already clear and doesn't need design exploration

## When NOT to Use

- New features (use full workflow)
- Changes affecting multiple systems (use full workflow)
- Anything requiring design decisions (use `/sk:brainstorm` first)
- Bug fixes (use `/sk:debug` flow)

## Guard Rails

Before proceeding, check the scope of planned changes:

1. **Diff size check**: After implementation, run `git diff --stat HEAD`. If the diff exceeds **300 lines** changed:
   > "This change is [N] lines — larger than the 300-line fast-track threshold. Consider the full workflow for better test coverage. Continue anyway? (y/n)"

2. **New file count**: If more than **5 new files** are created:
   > "You've created [N] new files. Consider running `/sk:write-tests` first. Continue anyway? (y/n)"

3. **Migration check**: If any migration files are detected in changes, warn:
   > "Migration files detected. Consider running `/sk:schema-migrate` for analysis."

## Steps

### 1. Context (quick)
- Read `tasks/todo.md` — pick the task or accept user's description
- Read `tasks/lessons.md` — apply active lessons as constraints

### 2. Branch
- Run `/sk:branch` to create a feature branch

### 3. Implement
- Write the code directly — no brainstorm, design, plan, or TDD phases
- Focus on the minimal change needed

### 4. Commit
- Run `/sk:smart-commit` to stage and commit with conventional commit message

### 5. Gates
- Run `/sk:gates` — all quality gates in optimized parallel batches
- This is the same gate process as the full workflow — no shortcuts on quality
- Lint, test, security, perf, review, E2E all run

### 6. Finalize
- Run `/sk:finish-feature` for changelog + PR

## Model Routing

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |
