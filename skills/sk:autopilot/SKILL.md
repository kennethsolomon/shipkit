---
name: sk:autopilot
description: Hands-free workflow — runs all 8 steps with auto-skip, auto-advance, auto-commit. Stops only for direction approval, 3-strike failures, and PR push.
allowed-tools: Read, Write, Bash, Glob, Grep, Agent, Skill
---

# Autopilot Mode

Hands-free workflow that executes all 8 steps of the ShipIt workflow with minimal interruptions. Same quality gates, same fix loops, same 100% coverage — just fewer stops.

## When to Use

- You know roughly what you want built and trust the workflow to handle details
- You want to minimize context switches and manual step advancement
- The task is well-defined enough for a single direction-approval checkpoint

## When NOT to Use

- Exploratory work where you want to steer each step
- Tasks requiring frequent design decisions mid-implementation
- When you want to review intermediate outputs before proceeding

## Quality Guarantee

Autopilot runs the EXACT same 8 steps as manual mode:
- ALL quality gates enforced (lint, test, security, perf, review, e2e)
- ALL fix-rerun loops active
- 100% test coverage required on new code
- 0 security issues required
- The ONLY difference: auto-advance between steps instead of stopping

## Steps

### 1. Load Context + Brainstorm + Direction Approval (STOP — requires user input)

- Read `tasks/todo.md`, `tasks/lessons.md`, `tasks/findings.md`, `tasks/tech-debt.md`
- Run brainstorm internally (3 parallel Explore agents)
- Propose 2-3 approaches with trade-offs

**Present ONE direction summary and ask:**
> "Direction: [1-2 sentence summary of chosen approach]
> Scope: [what will be built/changed]
> Auto-skipping: [list of steps that will be auto-skipped and why]
> Proceed? (y/n)"

Wait for explicit `y` before continuing. This is the ONLY planning stop.

### 2. Design (auto-skip if no frontend/API keywords)

Run `/sk:frontend-design` or `/sk:api-design` if applicable. Auto-skip if no frontend/API keywords detected. Log: `Auto-skipped: Design ([reason])`

### 3. Plan (auto-advance)

Write the implementation plan to `tasks/todo.md`. Do NOT ask for plan approval — the direction approval in step 1 covers this.

### 4. Branch (auto-advance)

Create feature branch auto-named from the task. Do NOT ask for confirmation.

### 5. Write Tests + Implement (auto-advance)

- Run `/sk:write-tests` (TDD red phase)
- Run `/sk:schema-migrate` if database keywords detected
- Run `/sk:execute-plan` (TDD green phase)
- Auto-advance when done

### 5.5. Scope Check (auto-advance)

Run `/sk:scope-check` to compare the implementation against `tasks/todo.md`.

- If scope creep detected: log findings, trim the excess, re-commit
- If on-scope: auto-advance silently

### 6. Commit (auto-commit)

Auto-commit with conventional commit format. Do NOT ask for commit message approval.
Format: `type(scope): description`

### 7. Gates (auto-advance on clean pass)

Run all quality gates via `/sk:gates`:
1. Lint + dep audit
2. Test (100% coverage)
3. Security (0 issues)
4. Performance (if not auto-skipped)
5. Review + simplify
6. E2E

Each gate auto-fixes and re-runs internally. Squash gate commits — one commit per gate pass.

### 8. PR Push (STOP — requires user confirmation)

**This is the second mandatory stop.** Present:
> "All gates passed. Ready to create PR.
> Title: [conventional format]
> Changes: [file count] files, [line count] lines
> Confirm push + PR? (y/n)"

Wait for explicit confirmation — pushing is visible to others.

After confirmation:
- Create PR
- Sync features (`/sk:features`)
- Ask about release (never auto-skipped)

### 8.5. Learn (auto-advance)

Run `/sk:learn` to extract reusable patterns from this session.

- Patterns are saved to `~/.claude/skills/learned/` automatically
- Auto-advance after saving — no confirmation needed in autopilot

### 8.6. Retro (auto-advance)

Run `/sk:retro` to capture velocity, blockers, and action items for this feature.

- Output is brief — 3-5 bullets covering what went well, what slowed down, and next actions
- Appended to `tasks/progress.md`

## 3-Strike Protocol

If any step fails 3 times:
- **STOP immediately**
- Report: what failed, what was tried, error details
- Ask user for guidance before continuing
- This overrides auto-advance — 3 strikes always stops

## Stops Summary

| Stop | When | Why |
|------|------|-----|
| Direction approval | After brainstorm (step 1) | User must approve the approach |
| 3-strike failure | Any step fails 3x | Needs human judgment |
| PR push | Before creating PR (step 8) | Visible to others — always confirm |
| Release | After step 8.6 | Never auto-skipped — always ask |

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
