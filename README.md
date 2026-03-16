<div align="center">

# SHIPKIT

**A structured, quality-gated workflow system for Claude Code.**

Stop winging it. Ship features with TDD, auto-detecting linters, security audits,<br>
and AI-powered code review — all wired into a single repeatable workflow.

**Every gate must pass. Quality isn't optional — it's structural.**

[![npm](https://img.shields.io/npm/v/@kennethsolomon%2Fshipkit)](https://www.npmjs.com/package/@kennethsolomon/shipkit)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Mac%20%2F%20Linux%20%2F%20Windows-lightgrey)](#)

```bash
npm install -g @kennethsolomon/shipkit && shipkit
```

Works on Mac, Linux, and Windows.

</div>

<div align="center">

![ShipKit terminal demo](assets/shipkit-terminal.png)

</div>

---

<div align="center">

*"Ran `/sk:review` on what I thought was done. It found 3 things I would have caught in production. Now it's in every merge."*

*"Every other Claude workflow I tried was either too rigid or too vague. ShipKit is the first one that actually ships."*

*"The gates feel annoying until the day they catch something real. Now I don't merge without them."*

</div>

---

## Quick Start

```bash
# 1. Install ShipKit globally
npm install -g @kennethsolomon/shipkit && shipkit

# 2. Bootstrap your project (run inside your project directory)
/sk:setup-claude

# 3. Start your first feature
/sk:brainstorm
```

`/sk:setup-claude` creates `tasks/todo.md`, `tasks/lessons.md`, and a project-specific `CLAUDE.md` with the full workflow baked in. Run it once per project.

---

## How It Works

ShipKit installs slash commands and skills into `~/.claude/`. Each command is a focused instruction set that Claude follows — no magic, just structured prompts that enforce quality gates.

The workflow is linear: **Read → Explore → Design → Accessibility → Plan → Branch → Migrate → Write Tests → Implement → Lint → Verify Tests → Security → Performance → Review → E2E Tests → Finish → Sync Features**

Every gate must pass before the next step. If lint fails, fix it. If tests don't cover new code, write them. Security issues block the PR. This isn't optional — it's the whole point.

**Requirements change mid-workflow?** Run `/sk:change`. It assesses the scope and tells you exactly where to re-enter — no guessing, no skipping steps.

---

## Workflow

### Feature Flow

```
Brainstorm → Plan → Branch → [Schema] → Write Tests → Implement → Commit
  → Lint ✓ → Test ✓ → Security ✓ → Review ✓ → E2E ✓ → Update Task → Finish → Sync Features
```

| # | Command | Purpose |
|---|---------|---------|
| 1 | read `tasks/todo.md` | Pick the next task |
| 2 | read `tasks/lessons.md` | Review past corrections |
| 3 | `/sk:brainstorm` | Clarify requirements — no code |
| 4 | `/sk:frontend-design` | UI design spec *(skip if backend-only)*. Add `--pencil` to also generate a Pencil visual mockup |
| 5 | `/sk:api-design` | API contracts *(skip if no new endpoints)* |
| 6 | `/sk:accessibility` | WCAG 2.1 AA audit on design *(skip if no frontend)* |
| 7 | `/sk:write-plan` | Write plan to `tasks/todo.md` |
| 8 | `/sk:branch` | Create branch from current task |
| 9 | `/sk:schema-migrate` | Schema change analysis *(skip if no DB changes)* |
| 10 | `/sk:write-tests` | TDD red: write failing tests first |
| 11 | `/sk:execute-plan` | TDD green: make tests pass |
| 12 | `/sk:smart-commit` | Conventional commit |
| 13 | **`/sk:lint`** | **GATE** — Lint + Dep Audit — all linters must pass |
| 14 | `/sk:smart-commit` | Auto-skip if already clean |
| 15 | **`/sk:test`** | **GATE** — 100% coverage on new code |
| 16 | `/sk:smart-commit` | Auto-skip if already clean |
| 17 | **`/sk:security-check`** | **GATE** — 0 issues |
| 18 | `/sk:smart-commit` | Auto-skip if already clean |
| 19 | **`/sk:perf`** | **GATE** *(optional)* — critical/high findings = 0 |
| 20 | `/sk:smart-commit` | Auto-skip if already clean |
| 21 | **`/sk:review`** | **GATE** — Review + Simplify — 0 issues including nitpicks |
| 22 | `/sk:smart-commit` | Auto-skip if already clean |
| 23 | **`/sk:e2e`** | **GATE** — E2E Tests — all end-to-end tests must pass |
| 24 | `/sk:smart-commit` | Auto-skip if already clean |
| 25 | `/sk:update-task` | Mark done, log completion |
| 26 | `/sk:finish-feature` | Changelog + PR |
| 27 | `/sk:features` | Sync Features — update docs/features/ specs *(required)* |
| 28 | `/sk:release` | Version bump + tag *(optional)* |

> **Fix & Retest Protocol:** All code-producing gates (Lint, Test, Security, Performance, Review, E2E) apply the Fix & Retest Protocol: logic changes require updating unit tests before committing the fix. Fix immediately, then re-run — never ask the user to re-run.

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
| 6–10 | `/sk:lint` → `/sk:test` → `/sk:security-check` → `/sk:review` → `/sk:e2e` | Quality gates |
| 11 | `/sk:finish-feature` | Changelog + PR |

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

### Requirement Change Flow

Requirements change mid-workflow all the time. Run `/sk:change` whenever something shifts — it classifies the scope and routes you back to the right step automatically.

```
Requirement changes → /sk:change → re-enter at correct step
```

| Tier | What changed | Re-entry point |
|------|-------------|----------------|
| **Tier 1** — Behavior Tweak | Logic changes, scope stays the same *(e.g. delete all → delete users only)* | `/sk:write-tests` |
| **Tier 2** — New Requirements | New scope, new constraints, new acceptance criteria | `/sk:write-plan` |
| **Tier 3** — Scope Shift | Fundamental rethinking of approach or architecture | `/sk:brainstorm` |

`/sk:change` logs the change to `tasks/todo.md` and `tasks/progress.md`, marks invalidated tasks, and tells you exactly what to carry forward.

---

## Commands

### Planning & Design

| Command | Description |
|---------|-------------|
| `/sk:brainstorm` | Explore requirements and design before writing any code |
| `/sk:frontend-design` | Create UI design specs and mockups. After the design summary, it asks if you want a Pencil visual mockup. Use `--pencil` flag to jump directly to the Pencil phase *(requires Pencil app + MCP)* |
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
| `/sk:change` | Handle a mid-workflow requirement change — assess scope and re-enter at the right step |
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

ShipKit routes each skill to the right model automatically. Set it once per project:

```bash
/sk:set-profile balanced   # default
/sk:set-profile quality    # most projects
/sk:set-profile full-sail  # high-stakes / client work
/sk:set-profile budget     # side projects / exploration
```

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
| change | opus | sonnet | sonnet | sonnet |
| perf, schema-migrate, accessibility | opus | sonnet | sonnet | haiku |
| lint, test | sonnet | sonnet | haiku | haiku |
| smart-commit, branch, update-task | haiku | haiku | haiku | haiku |

`opus` = inherit (uses your current session model). Config lives in `.shipkit/config.json` — per project, gitignored by default.

### Config Reference

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

## Security

ShipKit instructs Claude to audit your code — but Claude also has access to your filesystem. Protect sensitive files by adding a deny list to `.claude/settings.json` in your project:

```json
{
  "permissions": {
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Read(**/*.p12)",
      "Read(**/credentials*)"
    ]
  }
}
```

This prevents Claude from reading secrets even if a prompt tries to access them. Pair this with your `.gitignore` — never commit `.env` files.

If you discover a security issue in ShipKit itself, please open a [GitHub issue](https://github.com/kennethsolomon/shipkit/issues) or email directly rather than posting publicly.

---

## License

MIT — see [LICENSE](LICENSE) for details.

Built by [Kenneth Solomon](https://github.com/kennethsolomon).

---

<div align="center">

**Claude Code is powerful. ShipKit makes it reliable.**

</div>
