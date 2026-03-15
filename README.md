# claude-skills

Custom [Claude Code](https://claude.ai/code) skills for bootstrapping and maintaining projects with an enforced TDD workflow.

## Installation

```bash
git clone git@github.com:kennethsolomon/claude-skills.git
cd claude-skills
./install.sh
```

### Updating

```bash
cd claude-skills
git pull
./install.sh
```

Re-run install after pulling to pick up new skills/commands. It's idempotent.

### Uninstalling

```bash
cd claude-skills
./uninstall.sh
```

## Workflow

Every step has a slash command. Follow the flow top to bottom — quality gates block forward progress until they pass.

```
Flow: Read → Explore → Design → Plan → Branch → Write Tests → Implement → Lint → Verify Tests → Security → Review → Finish
```

| # | Step | Command | Notes |
|---|------|---------|-------|
| 1 | Read Todo | read `tasks/todo.md` | Pick the next task |
| 2 | Read Lessons | read `tasks/lessons.md` | Review past corrections |
| 3 | Explore | `/brainstorm` | Clarify requirements, no code |
| 4 | Design | `/frontend-design` | UI mockup, skip if backend-only |
| 5 | Plan | `/write-plan` | Write plan to `tasks/todo.md`, no code |
| 6 | Branch | `/branch` | Auto-named from current task |
| 7 | Write Tests | `/write-tests` | TDD red: write failing tests first |
| 8 | Implement | `/execute-plan` | TDD green: make tests pass |
| 9 | Commit | `/smart-commit` | Commit tests + implementation |
| 10 | **Lint** | run project linter | **GATE** — all lint tools must pass |
| 11 | Commit | `/smart-commit` | Auto-skip if lint was clean |
| 12 | **Verify Tests** | run project test suite | **GATE** — 100% coverage required |
| 13 | Commit | `/smart-commit` | Auto-skip if tests passed first try |
| 14 | **Security** | `/security-check` | **GATE** — 0 issues across all severities |
| 15 | Commit | `/smart-commit` | Auto-skip if security was clean |
| 16 | **Review** | `/review` | **GATE** — 0 issues including nitpicks |
| 17 | Commit | `/smart-commit` | Auto-skip if review was clean |
| 18 | Update | `/update-task` | Mark done, log completion |
| 19 | Finalize | `/finish-feature` | Changelog + PR |
| 20 | Release | `/release` | Version bump + tag, optional |

### Quality Gates (Steps 10, 12, 14, 16)

These steps **block all forward progress** until they pass clean. Claude fixes issues and re-runs automatically until clean. Gates cannot be skipped.

### Step Completion Summary

After every step, Claude outputs:

```
--- Step [#] [Name]: [done/skipped/partial] ---
Summary: [what was done]
Next step: [#] [Name] — run `[command]`
```

Run `/status` at any time to check where you are.

## Skills

| Skill | Command | What it does |
|-------|---------|--------------|
| `setup-claude` | `/setup-claude` | Bootstrap scaffolding (CLAUDE.md, tasks/, commands/) |
| `brainstorming` | `/brainstorm` | Explore design before writing code |
| `frontend-design` | `/frontend-design` | Design direction + specs for UI work |
| `write-tests` | `/write-tests` | TDD: Write failing tests before implementation |
| `review` | `/review` | Self-review across 7 dimensions |
| `smart-commit` | `/smart-commit` | Auto-generate conventional commit messages |
| `schema-migrate` | `/schema-migrate` | Multi-ORM schema change analysis |
| `release` | `/release` | Version bump, changelog, tag. `--ios`/`--android` for store audits |
| `features` | `/features` | Sync `docs/features/` specs with codebase |
| `skill-creator` | `/skill-creator` | Create or improve skills |
| `setup-optimizer` | `/setup-optimizer` | Enrich CLAUDE.md with project context |
| `starter-setup` | `/starter-setup` | Create optimized CLAUDE.md via auto-detection |
| `claude-doctor` | `/claude-doctor` | Diagnose and improve your CLAUDE.md |

## Commands

| Command | Purpose |
|---------|---------|
| `/brainstorm` | Explore requirements and design |
| `/frontend-design` | UI mockup before implementation |
| `/write-plan` | Write decision-complete plan |
| `/branch` | Create feature branch from current task |
| `/execute-plan` | Execute plan checkboxes in batches |
| `/smart-commit` | Conventional commit with approval |
| `/security-check` | OWASP security audit |
| `/review` | Self-review of branch changes |
| `/update-task` | Mark task done, log completion |
| `/finish-feature` | Changelog + PR creation |
| `/release` | Version bump + changelog + tag |
| `/status` | Show workflow + task status |

## Laravel Plugin

For Laravel projects, install the [laravel-setup](https://github.com/kennethsolomon/claude-skills-laravel) plugin which extends this workflow with:
- `/laravel-init` — configure existing Laravel project
- `/laravel-lint` — Pint + PHPStan + Rector
- `/laravel-write-tests` — Pest + Vitest (Laravel-specific TDD)
- `/laravel-test` — verify tests pass with 100% coverage

## Full Documentation

See [DOCUMENTATION.md](.claude/docs/DOCUMENTATION.md) for detailed usage, tutorials, and per-skill reference.
