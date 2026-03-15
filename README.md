# SHIPKIT

A structured, quality-gated workflow system for Claude Code.

Ship features with TDD, auto-detecting linters, security audits, and AI-powered code review — all wired into a single repeatable workflow.

[![npm](https://img.shields.io/npm/v/@kennethsolomon%2Fshipkit)](https://www.npmjs.com/package/@kennethsolomon/shipkit)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Mac%20%2F%20Linux%20%2F%20Windows-lightgrey)](#)

```bash
npm install -g @kennethsolomon/shipkit && shipkit
```

Works on Mac, Linux, and Windows.

```
~ $ shipkit

           ⚑
           |
          /|\
         / | \
        /  |  \
       /   |   \
      / ☠  |  ☠ \
     /     |     \
    /______|______\
  ▄████████████████▄
  █  ◉          ◉  █
   ▀██████████████▀
     ≋  ≋  ≋  ≋  ≋

  ShipKit v3.0.1
  A structured workflow toolkit for Claude Code.
  by Kenneth Solomon

  ✓ Installed commands/sk (15 commands)
  ✓ Installed skills (19 skills)

  Done! Run /sk:help to get started.

~ $
```

---

> "Stop winging it. Ship with a system."

---

## How It Works

ShipKit installs a set of slash commands and skills into your Claude Code config (`~/.claude/`). Each command is a focused instruction set that Claude follows — no magic, just structured prompts that enforce quality gates.

The workflow is linear: **Explore → Design → Plan → Branch → Test → Implement → Lint → Verify → Security → Review → Ship.**

Every gate must pass before the next step. If lint fails, you fix it. If tests don't cover new code, you write them. Security issues block the PR. This isn't optional — it's the whole point.

---

## Installation

```bash
npm install -g @kennethsolomon/shipkit && shipkit
```

Or clone and install locally (symlinks — changes reflect immediately):

```bash
git clone https://github.com/kennethsolomon/shipkit.git
cd shipkit
./install.sh
```

### Update

```bash
npm install -g @kennethsolomon/shipkit && shipkit
```

Re-running always installs the latest version.

### Uninstall

```bash
shipkit --uninstall
```

---

## Workflow

### Feature Flow

```
Brainstorm → Plan → Branch → [Schema] → Write Tests → Implement → Commit
  → Lint ✓ → Test ✓ → Security ✓ → Review ✓ → Update Task → Finish
```

| # | Command | Purpose |
|---|---------|---------|
| 1 | read `tasks/todo.md` | Pick the next task |
| 2 | read `tasks/lessons.md` | Review past corrections |
| 3 | `/sk:brainstorm` | Clarify requirements — no code |
| 4 | `/sk:frontend-design` | UI design spec *(skip if backend-only)* |
| 5 | `/sk:api-design` | API contracts *(skip if no new endpoints)* |
| 6 | `/sk:accessibility` | WCAG 2.1 AA audit on design *(skip if no frontend)* |
| 7 | `/sk:write-plan` | Write plan to `tasks/todo.md` |
| 8 | `/sk:branch` | Create branch from current task |
| 9 | `/sk:schema-migrate` | Schema change analysis *(skip if no DB changes)* |
| 10 | `/sk:write-tests` | TDD red: write failing tests first |
| 11 | `/sk:execute-plan` | TDD green: make tests pass |
| 12 | `/sk:smart-commit` | Conventional commit |
| 13 | **`/sk:lint`** | **GATE** — all linters must pass |
| 14 | `/sk:smart-commit` | Auto-skip if already clean |
| 15 | **`/sk:test`** | **GATE** — 100% coverage on new code |
| 16 | `/sk:smart-commit` | Auto-skip if already clean |
| 17 | **`/sk:security-check`** | **GATE** — 0 issues |
| 18 | `/sk:smart-commit` | Auto-skip if already clean |
| 19 | **`/sk:review`** | **GATE** — 0 issues including nitpicks |
| 20 | `/sk:smart-commit` | Auto-skip if already clean |
| 21 | `/sk:update-task` | Mark done, log completion |
| 22 | `/sk:finish-feature` | Changelog + PR |
| 23 | `/sk:release` | Version bump + tag *(optional)* |

### Bug Fix Flow

```
Debug → Plan → Branch → Write Tests → Implement → Lint ✓ → Test ✓ → Security ✓ → Review ✓ → Finish
```

| # | Command | Purpose |
|---|---------|---------|
| 1 | `/sk:debug` | Root-cause analysis |
| 2 | `/sk:write-plan` | Fix plan |
| 3 | `/sk:branch` | Create branch |
| 4 | `/sk:write-tests` | Reproduce the bug in a test |
| 5 | `/sk:execute-plan` | Fix — make the test pass |
| 6–9 | lint → test → security → review | Quality gates |
| 10 | `/sk:finish-feature` | Changelog + PR |

### Hotfix Flow

For production issues that need to ship immediately. Skips brainstorm, design, and TDD. **Quality gates are non-negotiable even in a hotfix.**

```
Debug → Branch → Fix → Smoke Test → Lint ✓ → Test ✓ → Security ✓ → Review ✓ → Finish
```

| # | Command | Purpose |
|---|---------|---------|
| 1 | `/sk:debug` | Root-cause analysis — understand before touching code |
| 2 | `/sk:branch` | Auto-named from the bug description |
| 3 | implement directly | No write-tests phase — go straight to the fix |
| 4 | run existing tests | Existing tests MUST still pass |
| 5 | `/sk:smart-commit` | Commit the fix |
| 6 | **`/sk:lint`** | **GATE** |
| 7 | **`/sk:test`** | **GATE** |
| 8 | **`/sk:security-check`** | **GATE** |
| 9 | **`/sk:review`** | **GATE** |
| 10 | `/sk:update-task` | Mark done |
| 11 | `/sk:finish-feature` | Changelog + PR — mark as hotfix |

After merging: add a regression test and a lesson to `tasks/lessons.md`.

---

## Commands

### Planning & Design

| Command | Description |
|---------|-------------|
| `/sk:brainstorm` | Explore requirements and design before writing any code |
| `/sk:frontend-design` | Create UI design specs and mockups |
| `/sk:api-design` | Design REST or GraphQL API contracts |
| `/sk:accessibility` | WCAG 2.1 AA audit on design or existing frontend |
| `/sk:write-plan` | Write a decision-complete plan to `tasks/todo.md` |
| `/sk:plan` | Create or refresh task planning files |
| `/sk:setup-claude` | Bootstrap project scaffolding (CLAUDE.md + tasks/) |
| `/sk:setup-optimizer` | Enrich CLAUDE.md by scanning the codebase |

### Development

| Command | Description |
|---------|-------------|
| `/sk:branch` | Create a feature branch from the current task |
| `/sk:schema-migrate` | Analyze pending schema changes (Prisma, Drizzle, Eloquent, SQLAlchemy, ActiveRecord) |
| `/sk:write-tests` | TDD: write failing tests before implementation |
| `/sk:execute-plan` | Implement the plan in small batches |
| `/sk:debug` | Structured bug investigation: reproduce → isolate → fix |
| `/sk:hotfix` | Emergency fix workflow — skips design and TDD |

### Quality Gates

| Command | Description |
|---------|-------------|
| `/sk:lint` | Auto-detect and run all linters (Pint, ESLint, PHPStan, Prettier…) |
| `/sk:test` | Auto-detect and run all test suites, verify 100% coverage on new code |
| `/sk:security-check` | OWASP security audit across changed code |
| `/sk:perf` | Performance audit: bundle size, N+1 queries, Core Web Vitals |
| `/sk:review` | Rigorous self-review across 7 dimensions |

### Shipping

| Command | Description |
|---------|-------------|
| `/sk:smart-commit` | Generate conventional commit messages with approval |
| `/sk:update-task` | Mark current task done, log completion |
| `/sk:finish-feature` | Write changelog entry + create PR |
| `/sk:release` | Version bump + CHANGELOG + git tag + push |
| `/sk:features` | Sync docs/features/ specs with the codebase |

### Laravel

| Command | Description |
|---------|-------------|
| `/sk:laravel-new` | Scaffold a fresh Laravel app with production-ready conventions |
| `/sk:laravel-init` | Configure an existing Laravel project |

### Configuration

| Command | Description |
|---------|-------------|
| `/sk:config` | View and edit project config (`.shipkit/config.json`) |
| `/sk:set-profile` | Switch model routing profile for this project |

### Meta

| Command | Description |
|---------|-------------|
| `/sk:help` | Show all commands and workflow overview |
| `/sk:status` | Show workflow and task status at a glance |
| `/sk:skill-creator` | Create or improve ShipKit skills |

---

## Model Routing Profiles

ShipKit routes each skill to the right model automatically based on your project profile.
Set it once with `/sk:set-profile <name>` — config is saved to `.shipkit/config.json`.

| Profile | Philosophy | Best for |
|---------|-----------|---------|
| `full-sail` | Opus on everything that matters | High-stakes work, client projects |
| `quality` | Opus for planning + review, Sonnet for implementation | Most professional projects |
| `balanced` | Sonnet across the board *(default)* | Day-to-day development |
| `budget` | Haiku where possible, Sonnet for gates | Side projects, prototyping |

| Skill group | full-sail | quality | balanced | budget |
|-------------|-----------|---------|----------|--------|
| brainstorm, write-plan, debug, execute-plan, review | opus | opus | sonnet | sonnet |
| write-tests, frontend-design, api-design, security-check | opus | sonnet | sonnet | sonnet |
| perf, schema-migrate, accessibility | opus | sonnet | sonnet | haiku |
| lint, test | sonnet | sonnet | haiku | haiku |
| smart-commit, branch, update-task | haiku | haiku | haiku | haiku |

`opus` = inherit (uses your current session model).

### Other config settings

```json
{
  "profile": "balanced",
  "auto_commit": true,
  "skip_gates": [],
  "coverage_threshold": 100,
  "branch_pattern": "feature/{slug}",
  "model_overrides": { "sk:review": "opus" }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `profile` | `balanced` | Model routing profile |
| `auto_commit` | `true` | Auto-commit after each gate passes |
| `skip_gates` | `[]` | Gates to skip — e.g. `["perf","accessibility"]` for backend-only projects |
| `coverage_threshold` | `100` | Minimum test coverage % on new code |
| `branch_pattern` | `feature/{slug}` | Branch naming convention |
| `model_overrides` | `{}` | Per-skill model overrides that take precedence over profile |

---

## Stack Support

ShipKit auto-detects your stack — no configuration needed.

| Area | Supported |
|------|-----------|
| **Linters** | Pint, ESLint, PHPStan, Rector, Prettier, Biome, Stylelint |
| **Test runners** | Pest, PHPUnit, Jest, Vitest, Playwright |
| **Schema / ORM** | Prisma, Drizzle, Eloquent, SQLAlchemy + Alembic, ActiveRecord |
| **Frameworks** | Laravel, Next.js, Nuxt, React, Vue, Node.js |
| **Release** | npm, Composer, iOS (App Store), Android (Play Store) |

---

## Project Setup

To wire ShipKit into a new project:

```
/sk:setup-claude
```

This creates `tasks/todo.md`, `tasks/lessons.md`, and a project-specific `CLAUDE.md` with the full workflow baked in.

---

## Why ShipKit

Claude Code is powerful but context degrades as the window fills. Unstructured sessions lead to skipped tests, no lint, missing security review, and PRs that broke things in ways nobody caught.

ShipKit fixes that with a repeatable system: every feature goes through the same gates in the same order. Quality isn't optional — it's structural.

---

## License

MIT — by [Kenneth Solomon](https://github.com/kennethsolomon)
