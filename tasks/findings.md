# Findings — 2026-03-23 — ShipKit Workflow Improvements from Game Studios

## Problem Statement

ShipKit's workflow relies entirely on manual skill invocations and a large CLAUDE.md for all rules. Three key mechanisms are missing that would improve automation, contextual rule enforcement, and developer experience:
1. No lifecycle hooks — user must manually run `/sk:context` every session, context compression can lose workflow state
2. No path-scoped rules — all conventions live in one massive CLAUDE.md regardless of what files are being touched
3. No persistent status display, scope tracking, retrospective analysis, or reverse documentation

## Source

Analyzed [claude-code-game-studios](https://github.com/kennethsolomon/claude-code-game-studios) — a 48-agent game dev studio template with 8 hooks, 11 path-scoped rules, 37 skills, and a persistent statusline.

## Key Decisions Made

- **All 6 proposed improvements approved**, in priority order
- This is a ShipKit infrastructure improvement, not a project-specific feature

## Chosen Approach — 6 Features in Priority Order

### Feature 1: Lifecycle Hooks (Highest ROI)
Add Claude Code hooks to `settings.json` via `/sk:setup-claude`:
- **SessionStart** — auto-load branch, recent commits, workflow-status.md, tech-debt.md, TODO/FIXME counts. Replaces manual `/sk:context`.
- **PreCompact** — preserve workflow-status.md state + uncommitted changes before context compression. Prevents losing track of current step.
- **PreToolUse (commit)** — validate staged files: enforce conventional commit format, detect hardcoded secrets, check for debug statements, validate JSON files.
- **PreToolUse (push)** — warn when pushing to protected branches (main, master, production).
- **SubagentStart** — log agent invocations with timestamp to `tasks/agent-audit.log`.
- **Stop** — log session accomplishments to `tasks/progress.md`.

### Feature 2: Path-Scoped Rules
Add `.claude/rules/` directory support to `/sk:setup-claude` template:
- Rules auto-activate based on file path patterns
- Generated per detected stack (Laravel, React, Vue, etc.)
- Examples: `laravel.md` for `app/`, `frontend.md` for `resources/`, `tests.md` for `tests/`
- Reduces CLAUDE.md size by moving contextual rules out

### Feature 3: Statusline
Add `.claude/statusline.sh` to `/sk:setup-claude` template:
- Shows: context window %, active model, current workflow step, branch name, active task
- Always visible in CLI — no need to run `/sk:status`

### Feature 4: Scope Check Skill (`/sk:scope-check`)
New skill that compares implementation against `tasks/todo.md`:
- Lists planned vs. actual scope
- Identifies unplanned additions
- Quantifies scope bloat %
- Classifies: On Track (<=10%), Minor Creep (10-25%), Significant Creep (25-50%), Out of Control (>50%)
- Useful mid-implementation to catch drift

### Feature 5: Retrospective Skill (`/sk:retro`)
New skill that analyzes completed work after shipping:
- Planned vs. actual task completion
- Velocity trends from git history
- Blocker analysis from `tasks/progress.md`
- Estimation accuracy
- Recurring pattern detection across retros
- 3-5 action items with owners
- Output to `tasks/retro-YYYY-MM-DD.md`

### Feature 6: Reverse Document Skill (`/sk:reverse-doc`)
New skill that generates documentation from existing code:
- Analyzes code to extract patterns, architecture, conventions
- Asks clarifying questions to distinguish intent from accident
- Drafts architecture/design docs
- Useful for onboarding to existing codebases

## Open Questions

- None — direction locked, all 6 features approved in priority order
