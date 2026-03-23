---
name: sk:autopilot
description: Hands-free workflow — runs all 21 steps with auto-skip, auto-advance, auto-commit. Stops only for direction approval, 3-strike failures, and PR push.
user_invocable: true
allowed_tools: Read, Write, Bash, Glob, Grep, Agent, Skill
---

# Autopilot Mode

Hands-free workflow that executes all 21 steps of the ShipIt workflow with minimal interruptions. Same quality gates, same fix loops, same 100% coverage — just fewer stops.

## When to Use

- You know roughly what you want built and trust the workflow to handle details
- You want to minimize context switches and manual step advancement
- The task is well-defined enough for a single direction-approval checkpoint

## When NOT to Use

- Exploratory work where you want to steer each step
- Tasks requiring frequent design decisions mid-implementation
- When you want to review intermediate outputs before proceeding

## Quality Guarantee

Autopilot runs the EXACT same 21 steps as manual mode:
- ALL quality gates enforced (lint, test, security, perf, review, e2e)
- ALL fix-commit-rerun loops active
- 100% test coverage required on new code
- 0 security issues required
- The ONLY difference: auto-advance between steps instead of stopping

## Steps

### 0. Reset Tracker

Read `tasks/workflow-status.md`. If it has done/skipped steps from a different task, auto-reset all steps to `not yet`.

### 1. Load Context (auto — no prompt)

- Read `tasks/todo.md`
- Read `tasks/lessons.md` (apply all active lessons as constraints)
- Read `tasks/findings.md` (if exists)
- Read `tasks/tech-debt.md` (if exists)

### 2. Brainstorm + Direction Approval (STOP — requires user input)

Run brainstorm internally:
- Explore the codebase (3 parallel Explore agents)
- Propose 2-3 approaches with trade-offs

**Present ONE direction summary and ask:**
> "Direction: [1-2 sentence summary of chosen approach]
> Scope: [what will be built/changed]
> Auto-skipping: [list of steps that will be auto-skipped and why]
> Proceed? (y/n)"

Wait for explicit `y` before continuing. This is the ONLY planning stop.

### 3. Plan (auto-advance)

Write the implementation plan to `tasks/todo.md`. Do NOT ask for plan approval — the direction approval in step 2 covers this.

### 4. Branch (auto-advance)

Create feature branch auto-named from the task. Do NOT ask for confirmation.

### 5. Auto-Skip Detection

Scan `tasks/todo.md` for frontend/backend/database keywords. For each optional step:
- **Design (step 4)**: auto-skip if no frontend keywords
- **Accessibility (step 5)**: auto-skip if no frontend keywords
- **Migrate (step 8)**: auto-skip if no database keywords
- **Performance (step 15)**: auto-skip if no frontend AND no database keywords

Log each auto-skip: `Auto-skipped: [Step Name] ([reason])`

### 6. Write Tests (auto-advance)

Write failing tests based on the plan (TDD red phase). Auto-advance when done.

### 7. Implement (auto-advance)

Execute the plan — make failing tests pass. Use wave-based sub-agents for parallel work where possible.

### 8. Commit (auto-commit)

Auto-commit with conventional commit format. Do NOT ask for commit message approval.
Format: `type(scope): description`

### 9. Gates (auto-advance on clean pass)

Run all quality gates. Use `/sk:gates` if available, otherwise run sequentially:
1. Lint + dep audit
2. Test (100% coverage)
3. Security (0 issues)
4. Performance (if not auto-skipped)
5. Review + simplify
6. E2E

Each gate auto-fixes and re-runs internally. Auto-advance to next gate on clean pass.

### 10. PR Push (STOP — requires user confirmation)

**This is the second mandatory stop.** Present:
> "All gates passed. Ready to create PR.
> Title: [conventional format]
> Changes: [file count] files, [line count] lines
> Confirm push + PR? (y/n)"

Wait for explicit confirmation — pushing is visible to others.

### 11. Finalize (auto-advance)

- Create PR
- Sync features (`/sk:features`)
- Ask about release (step 21 is never auto-skipped)

## 3-Strike Protocol

If any step fails 3 times:
- **STOP immediately**
- Report: what failed, what was tried, error details
- Ask user for guidance before continuing
- This overrides auto-advance — 3 strikes always stops

## Stops Summary

| Stop | When | Why |
|------|------|-----|
| Direction approval | After brainstorm (step 2) | User must approve the approach |
| 3-strike failure | Any step fails 3x | Needs human judgment |
| PR push | Before creating PR (step 10) | Visible to others — always confirm |

Everything else auto-advances.

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:autopilot"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit. When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
