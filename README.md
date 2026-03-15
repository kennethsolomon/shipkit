# claude-skills

Custom Claude Code skills with TDD workflow, auto-detecting linters and test runners.

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

### Uninstalling

```bash
./uninstall.sh
```

## Workflow

```
Read → Explore → Design → Plan → Branch → Migrate → Write Tests → Implement → Lint → Verify Tests → Security → Review → Finish
```

| # | Step | Command | Notes |
|---|------|---------|-------|
| 1 | Read Todo | read `tasks/todo.md` | Pick the next task |
| 2 | Read Lessons | read `tasks/lessons.md` | Review past corrections |
| 3 | Explore | `/brainstorm` | Clarify requirements, no code |
| 4 | Design | `/frontend-design` or `/api-design` | UI/API design, optional Pencil mockup, skip if backend-only |
| 5 | Accessibility | `/accessibility` | WCAG 2.1 AA audit on design spec, skip if no frontend |
| 6 | Plan | `/write-plan` | Write plan to `tasks/todo.md`, no code |
| 7 | Branch | `/branch` | Auto-named from current task |
| 8 | Migrate | `/schema-migrate` | Skip if no schema changes |
| 9 | Write Tests | `/write-tests` | TDD red: write failing tests first |
| 10 | Implement | `/execute-plan` | TDD green: make tests pass |
| 11 | Commit | `/smart-commit` | Commit tests + implementation |
| 12 | **Lint** | `/lint` | **GATE** — all lint tools must pass |
| 13 | Commit | `/smart-commit` | Auto-skip if lint was clean |
| 14 | **Verify Tests** | `/test` | **GATE** — 100% coverage required |
| 15 | Commit | `/smart-commit` | Auto-skip if tests passed first try |
| 16 | **Security** | `/security-check` | **GATE** — 0 issues across all severities |
| 17 | Commit | `/smart-commit` | Auto-skip if security was clean |
| 18 | Performance | `/perf` | Optional gate — critical/high must reach 0 |
| 19 | Commit | `/smart-commit` | Auto-skip if perf was clean |
| 20 | **Review** | `/review` | **GATE** — 0 issues including nitpicks |
| 21 | Commit | `/smart-commit` | Auto-skip if review was clean |
| 22 | Update | `/update-task` | Mark done, log completion |
| 23 | Finalize | `/finish-feature` | Changelog + PR |
| 24 | Release | `/release` | Version bump + tag, optional |

### Bug Fix Flow

```
Debug → Plan → Branch → Write Tests → Implement → Lint → Verify Tests → Security → Review → Finish
```

| # | Step | Command | Notes |
|---|------|---------|-------|
| 1 | Read Todo | read `tasks/todo.md` | Pick the bug |
| 2 | Read Lessons | read `tasks/lessons.md` | Review past corrections |
| 3 | Debug | `/debug` | Root-cause analysis |
| 4 | Plan | `/write-plan` | Fix plan to `tasks/todo.md` |
| 5 | Branch | `/branch` | Auto-named from current task |
| 6 | Write Tests | `/write-tests` | Reproduce the bug in a test |
| 7 | Implement | `/execute-plan` | Fix the bug, make tests pass |
| 8 | Commit | `/smart-commit` | Commit fix + tests |
| 9 | **Lint** | `/lint` | **GATE** |
| 10 | Commit | `/smart-commit` | Auto-skip if clean |
| 11 | **Verify Tests** | `/test` | **GATE** |
| 12 | Commit | `/smart-commit` | Auto-skip if clean |
| 13 | **Security** | `/security-check` | **GATE** |
| 14 | **Review** | `/review` | **GATE** |
| 15 | Finalize | `/finish-feature` | Changelog + PR |

### Hotfix Flow

For production emergencies, use `/hotfix` — skips brainstorm, design, and write-tests. Quality gates still apply.

```
Investigate → Branch → Fix → Lint → Verify Tests → Security → Review → Finish
```

### Quality Gates

Steps 12, 14, 16, and 20 are hard gates that block all forward progress until they pass clean. Step 18 (Performance) is an optional gate. Claude fixes issues and re-runs automatically. Hard gates cannot be skipped.

### Step Summary

```
--- Step [#] [Name]: [done/skipped/partial] ---
Summary: [what was done]
Next step: [#] [Name] — run `[command]`
```

## Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| `setup-claude` | `/setup-claude` | Bootstrap scaffolding (CLAUDE.md, tasks/, commands/) |
| `setup-optimizer` | `/setup-optimizer` | Enrich CLAUDE.md with project context |
| `brainstorming` | `/brainstorm` | Explore design before writing code |
| `frontend-design` | `/frontend-design` | Design direction + specs for UI work. Optionally creates a Pencil `.pen` visual mockup via Pencil MCP (saved to `docs/design/`) |
| `api-design` | `/api-design` | Design REST/GraphQL API contracts before implementation |
| `accessibility` | `/accessibility` | WCAG 2.1 AA audit — runs after design, produces `tasks/accessibility-findings.md` |
| `write-tests` | `/write-tests` | TDD: write failing tests before implementation |
| `lint` | `/lint` | Run project linter |
| `test` | `/test` | Run project test suite |
| `review` | `/review` | Self-review across 7 dimensions |
| `debug` | `/debug` | Root-cause analysis for bugs |
| `smart-commit` | `/smart-commit` | Auto-generate conventional commit messages |
| `schema-migrate` | `/schema-migrate` | Multi-ORM schema change analysis |
| `perf` | `/perf` | Performance audit — bundle, N+1, Core Web Vitals, memory. Produces `tasks/perf-findings.md` |
| `release` | `/release` | Version bump, changelog, tag |
| `features` | `/features` | Sync `docs/features/` specs with codebase |
| `skill-creator` | `/skill-creator` | Create or improve skills |
| `laravel-init` | `/laravel-init` | Configure existing Laravel project |
| `laravel-new` | `/laravel-new` | Scaffold a new Laravel project |

## Commands

| Command | Purpose |
|---------|---------|
| `/brainstorm` | Explore requirements and design |
| `/frontend-design` | UI mockup before implementation. Prompts to create Pencil visual mockup |
| `/api-design` | Design API contracts before implementation |
| `/accessibility` | WCAG 2.1 AA audit after design |
| `/write-plan` | Write decision-complete plan |
| `/branch` | Create feature branch from current task |
| `/execute-plan` | Execute plan checkboxes in batches |
| `/smart-commit` | Conventional commit with approval |
| `/lint` | Run project linter |
| `/test` | Run project test suite |
| `/security-check` | OWASP security audit |
| `/perf` | Performance audit |
| `/review` | Self-review of branch changes |
| `/hotfix` | Emergency fix workflow |
| `/update-task` | Mark task done, log completion |
| `/finish-feature` | Changelog + PR creation |
| `/release` | Version bump + changelog + tag |
| `/status` | Show workflow + task status |
| `/setup-optimizer` | Diagnose + update workflow + enrich CLAUDE.md |
| `/plan` | Quick plan without full workflow |

## Laravel Support

Laravel detection is built-in. Run `/laravel-init` on any existing project or `/laravel-new` to scaffold.
