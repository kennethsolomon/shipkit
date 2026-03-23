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

## What is ShipKit?

ShipKit is a collection of slash commands that turn Claude Code into a disciplined development partner. Instead of asking Claude to "write some code," you follow a structured workflow where every feature goes through:

1. **Planning** — brainstorm, design, write a plan
2. **Implementation** — TDD (write tests first, then code)
3. **Quality gates** — lint, test, security audit, performance check, code review, E2E tests
4. **Shipping** — changelog, PR, release

Each gate must pass before the next step. If lint fails, fix it. If tests don't cover new code, write them. Security issues block the PR. This forces quality into the process rather than hoping for it at the end.

**ShipKit auto-detects your stack** — no configuration needed. It finds your linters, test runners, frameworks, and package managers automatically.

---

## Quick Start

```bash
# 1. Install ShipKit globally
npm install -g @kennethsolomon/shipkit && shipkit

# 2. Open your project in Claude Code, then bootstrap it
/sk:setup-claude

# 3. Start your first feature
/sk:brainstorm
```

`/sk:setup-claude` creates `tasks/todo.md`, `tasks/lessons.md`, a project-specific `CLAUDE.md` with the full workflow, lifecycle hooks, path-scoped rules, and a persistent statusline. Run it once per project.

---

## Which Flow Should I Use?

ShipKit has 5 workflows. Pick the one that matches your situation:

| Situation | Flow | Command | Steps |
|-----------|------|---------|-------|
| **Building a new feature** | Full Workflow | `/sk:brainstorm` | 21 steps — full planning + TDD + all gates |
| **Small, obvious change** (config, typo, deps) | Fast-Track | `/sk:fast-track` | 6 steps — skip planning, keep all gates |
| **Fixing a bug** | Bug Fix | `/sk:debug` | 11 steps — investigate first, then fix |
| **Production emergency** | Hotfix | `/sk:hotfix` | 11 steps — skip TDD, gates still enforced |
| **Requirements changed mid-work** | Change | `/sk:change` | Re-enter at the right step |

**Not sure?** Start with `/sk:brainstorm`. If the change turns out to be small, you can always switch to `/sk:fast-track`.

---

## Workflows in Detail

### 1. Full Feature Flow

Use this for any new feature, significant refactor, or change that needs design thinking.

```
/sk:brainstorm → /sk:write-plan → /sk:branch → /sk:write-tests → /sk:execute-plan
  → /sk:smart-commit → /sk:gates → /sk:update-task → /sk:finish-feature
```

**Step by step:**

| Phase | Step | Command | What it does |
|-------|------|---------|-------------|
| **Think** | 1 | read `tasks/todo.md` | Pick the next task |
| | 2 | read `tasks/lessons.md` | Review past mistakes to avoid repeating them |
| | 3 | `/sk:brainstorm` | Explore requirements — ask questions, propose approaches, get alignment. No code. |
| | 4 | `/sk:frontend-design` or `/sk:api-design` | Design mockup or API contract. Skip if not needed. Use `--pencil` for Pencil visual mockups. |
| | 5 | `/sk:accessibility` | WCAG 2.1 AA audit on the design. Skip if backend-only. |
| | 6 | `/sk:write-plan` | Write a decision-complete plan to `tasks/todo.md` with milestones and waves. |
| **Build** | 7 | `/sk:branch` | Create a feature branch auto-named from the task. |
| | 8 | `/sk:schema-migrate` | Analyze database schema changes. Auto-skips if no migrations detected. |
| | 9 | `/sk:write-tests` | TDD red phase — write failing tests that define expected behavior. |
| | 10 | `/sk:execute-plan` | TDD green phase — implement code to make tests pass. Uses sub-agents for parallel work. |
| | 11 | `/sk:smart-commit` | Stage changes and generate a conventional commit message for approval. |
| **Verify** | 12-17 | `/sk:gates` | Run ALL quality gates in one command (see [Quality Gates](#quality-gates) below). |
| **Ship** | 18 | `/sk:update-task` | Mark task done in `tasks/todo.md`, log completion. |
| | 19 | `/sk:finish-feature` | Update CHANGELOG, create architectural changelog if needed, push branch, create PR. |
| | 20 | `/sk:features` | Sync `docs/sk:features/` specs with what was actually shipped. |
| | 21 | `/sk:release` | Bump version, create git tag, push. Optional — skip if not releasing yet. |

**After shipping (recommended):** Run `/sk:retro` to analyze what went well, what didn't, and generate action items for next time.

---

### 2. Fast-Track Flow

Use this for small, obvious changes where the "what" is already clear: config changes, dependency bumps, copy/wording edits, small refactors, adding a missing test.

```bash
/sk:fast-track
```

That's it — one command. It handles:

1. Create branch
2. Implement directly (no brainstorm, no design, no TDD)
3. Commit with conventional message
4. Run ALL quality gates via `/sk:gates`
5. Create PR

**Guard rails:** If your diff exceeds 300 lines or creates more than 5 new files, it warns you to consider the full workflow.

**Still enforces all quality gates.** Fast-track skips the planning ceremony, not the quality checks.

---

### 3. Bug Fix Flow

Use this when something is broken and you need to investigate before fixing.

```
/sk:debug → /sk:branch → /sk:write-tests → fix → /sk:smart-commit → /sk:gates → /sk:finish-feature
```

| Step | Command | What it does |
|------|---------|-------------|
| 1 | `/sk:debug` | Structured investigation: reproduce → isolate → hypothesize → verify. Logs findings. |
| 2 | `/sk:branch` | Create a fix branch. |
| 3 | `/sk:write-tests` | Write a regression test that reproduces the bug (it should fail). |
| 4 | implement the fix | Make the regression test pass. |
| 5 | `/sk:smart-commit` | Commit the fix + test together. |
| 6 | `/sk:gates` | Run all quality gates. |
| 7 | `/sk:finish-feature` | Create PR. |

---

### 4. Hotfix Flow

Use this for production emergencies that need to ship immediately. Skips brainstorm, design, and TDD — but quality gates are still enforced.

```bash
/sk:hotfix
```

| Step | Command | What it does |
|------|---------|-------------|
| 1 | `/sk:debug` | Understand the root cause before touching code. |
| 2 | `/sk:branch` | Create branch. |
| 3 | implement directly | Fix the issue — no write-tests phase. |
| 4 | run existing tests | Existing tests MUST still pass. |
| 5 | `/sk:smart-commit` | Commit the fix. |
| 6 | `/sk:gates` | All quality gates run. |
| 7 | `/sk:finish-feature` | Create PR marked as hotfix. |

**After merging:** Add a regression test and a lesson to `tasks/lessons.md` so it doesn't happen again.

---

### 5. Requirement Change Flow

Requirements change mid-workflow all the time. Don't start over — run `/sk:change`.

```bash
/sk:change
```

It classifies the scope and routes you back to the right step automatically:

| Tier | What changed | Example | Re-entry point |
|------|-------------|---------|----------------|
| **Tier 1** — Behavior Tweak | Logic changes, scope stays the same | "Delete all" → "Delete users only" | `/sk:write-tests` |
| **Tier 2** — New Requirements | New scope, new constraints | "Also add export to CSV" | `/sk:write-plan` |
| **Tier 3** — Scope Shift | Fundamental rethinking | "Actually, let's use a different approach entirely" | `/sk:brainstorm` |

---

## Quality Gates

Quality gates are the core of ShipKit. Every change — whether full workflow, fast-track, bug fix, or hotfix — must pass these gates before merging.

### Running gates individually

You can run each gate separately:

| Command | What it checks | Blocks on |
|---------|---------------|-----------|
| `/sk:lint` | All detected linters + dependency vulnerability audit | Any lint error or high/critical vulnerability |
| `/sk:test` | All detected test suites | Any test failure or <100% coverage on new code |
| `/sk:security-check` | OWASP Top 10 audit on changed files | Any security finding |
| `/sk:perf` | Bundle size, N+1 queries, Core Web Vitals, memory leaks | Critical or high findings |
| `/sk:review` | 7-dimension code review with blast-radius analysis | Any issue including nitpicks |
| `/sk:e2e` | End-to-end behavioral tests (Playwright or agent-browser) | Any failing scenario |

### Running all gates at once

```bash
/sk:gates
```

This single command replaces running 6 gates manually. It runs them in optimized parallel batches:

| Batch | Gates | Why this order |
|-------|-------|---------------|
| **Batch 1** (parallel) | lint + security + perf | Independent — no dependencies on each other |
| **Batch 2** | test | Needs lint fixes applied first |
| **Batch 3** | review | Needs deep code understanding — runs in main context |
| **Batch 4** | e2e | Needs review fixes applied |

Each gate auto-fixes issues, auto-commits fixes, and re-runs until clean. You don't need to do anything — just wait for the results.

### How gates fix issues

When a gate finds a problem:
1. It fixes the issue automatically
2. Commits with a descriptive message (e.g., `fix(lint): resolve lint issues`)
3. Re-runs the gate from scratch
4. Repeats until clean

If a gate fails 3 times, it stops and asks you for help (3-strike protocol).

**Pre-existing issues** (problems that existed before your branch) are logged to `tasks/tech-debt.md` instead of being fixed inline — they're out of scope for your current task.

---

## On-Demand Tools

These commands aren't part of any workflow — use them whenever you need them.

### Scope Check

```bash
/sk:scope-check
```

Run mid-implementation to check if you're building more than planned. Compares your actual changes against `tasks/todo.md` and classifies scope creep:

| Classification | Bloat % | What it means |
|---------------|---------|---------------|
| **On Track** | 0-10% | Normal — minor supporting changes |
| **Minor Creep** | 10-25% | Some unplanned additions — review if necessary |
| **Significant Creep** | 25-50% | Scope has grown substantially — consider splitting |
| **Out of Control** | >50% | More unplanned than planned — stop and reassess with `/sk:change` |

### Retrospective

```bash
/sk:retro
```

Run after shipping a feature to analyze what happened:
- Completion rate (planned vs. actual tasks)
- Velocity (commits/day, files changed/day)
- Blocker analysis (errors from `tasks/progress.md`)
- Gate performance (how many attempts before clean)
- 3-5 action items for next time

Saves to `tasks/retro-YYYY-MM-DD.md`. Reads previous retros to detect recurring patterns.

### Reverse Documentation

```bash
/sk:reverse-doc architecture src/core/
/sk:reverse-doc design src/components/auth/
/sk:reverse-doc api routes/
```

Generate documentation from existing code — works backwards from implementation. Useful when:
- Onboarding to an inherited codebase with no docs
- Formalizing a prototype into documented design
- Capturing the "why" before a major refactor

It analyzes the code, asks you clarifying questions (to distinguish intent from accident), then drafts documentation for your approval.

### Other Tools

| Command | When to use |
|---------|------------|
| `/sk:context` | Load all project context at session start (automatic via hooks, but can run manually) |
| `/sk:status` | Quick view of workflow and task status |
| `/sk:dashboard` | Visual Kanban board showing workflow status across all git worktrees |
| `/sk:mvp` | Generate a complete MVP app from a single idea prompt |
| `/sk:seo-audit` | SEO audit for web projects |

---

## Infrastructure (What `/sk:setup-claude` Creates)

When you run `/sk:setup-claude`, it detects your stack and creates:

### Planning Files (`tasks/`)

| File | Purpose |
|------|---------|
| `tasks/todo.md` | Current task plan with checkboxes |
| `tasks/findings.md` | Discoveries from brainstorming |
| `tasks/progress.md` | Work log — every attempt, error, and resolution |
| `tasks/lessons.md` | Past mistakes and how to avoid them (append-only) |
| `tasks/workflow-status.md` | Tracks which workflow step you're on |
| `tasks/tech-debt.md` | Pre-existing issues found by gates (append-only) |

### Lifecycle Hooks (`.claude/hooks/`)

Hooks fire automatically — no manual invocation needed.

| Hook | When it fires | What it does |
|------|--------------|-------------|
| `session-start.sh` | Every session start | Loads branch, workflow step, tech debt count, code health |
| `pre-compact.sh` | Before context compression | Preserves workflow state so you don't lose track |
| `validate-commit.sh` | Before every commit | Checks conventional commit format, detects debug statements and secrets |
| `validate-push.sh` | Before every push | Warns when pushing to protected branches (main, master, production) |
| `log-agent.sh` | When a sub-agent starts | Logs agent invocations to `tasks/agent-audit.log` |
| `session-stop.sh` | When session ends | Logs session accomplishments to `tasks/progress.md` |

### Gate Agents (`.claude/agents/`)

Specialized agents that run quality gates as isolated sub-processes:

| Agent | Model | Purpose |
|-------|-------|---------|
| `linter` | Haiku | Run linters + dependency audits (mechanical — fast model) |
| `test-runner` | Sonnet | Run test suites, fix failures, verify coverage |
| `security-auditor` | Sonnet | OWASP audit on changed files |
| `perf-auditor` | Sonnet | Performance audit (N+1, bundle, memory) |
| `e2e-tester` | Sonnet | End-to-end behavioral verification |

### Path-Scoped Rules (`.claude/rules/`)

Rules that auto-activate based on which files you're editing:

| Rule | Activates on | What it enforces |
|------|-------------|-----------------|
| `tests.md` | `tests/`, `test/`, `__tests__/` | Naming conventions, arrange/act/assert, coverage requirements |
| `api.md` | `routes/api/`, `src/api/` | Input validation, error responses, auth patterns |
| `frontend.md` | `resources/`, `src/components/` | Component structure, accessibility, state management |
| `laravel.md` | `app/`, `routes/`, `database/` | Eloquent patterns, form requests, service layer (Laravel only) |
| `react.md` | `src/components/`, `src/hooks/` | Hooks rules, component patterns, TypeScript (React only) |

### Other Files

- **`CLAUDE.md`** — Project-specific instructions with the full workflow baked in
- **`.claude/settings.json`** — Hook configuration, permissions, statusline
- **`.claude/statusline.sh`** — Persistent CLI status showing context %, model, workflow step, branch, task

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

## All Commands Reference

| Command | Purpose |
|---------|---------|
| `/sk:accessibility` | WCAG 2.1 AA audit — runs after design, before implementation |
| `/sk:api-design` | Design API contracts (endpoints, payloads, auth, errors) before implementation |
| `/sk:brainstorm` | Explore requirements and design |
| `/sk:branch` | Create feature branch auto-named from current task |
| `/sk:change` | Handle mid-workflow requirement changes — re-enter at correct step |
| `/sk:config` | View and edit project config (`.shipkit/config.json`) |
| `/sk:context` | Load all context files + output session brief for fast session start |
| `/sk:dashboard` | Read-only workflow Kanban board — localhost server, multi-worktree |
| `/sk:debug` | Investigate and debug issues (bug fix entry point) |
| `/sk:e2e` | E2E behavioral verification using agent-browser (final quality gate) |
| `/sk:execute-plan` | Execute `tasks/todo.md` checkboxes in batches |
| `/sk:fast-track` | Abbreviated workflow for small changes — skip planning, keep all gates |
| `/sk:features` | Sync feature specs with shipped implementation |
| `/sk:finish-feature` | Changelog + PR creation |
| `/sk:frontend-design` | UI mockup before implementation. Prompts to create Pencil visual mockup |
| `/sk:gates` | Run all quality gates in optimized parallel batches |
| `/sk:help` | Show all commands and workflow overview |
| `/sk:hotfix` | Emergency fix workflow — skip design/TDD, quality gates enforced |
| `/sk:laravel-init` | Configure existing Laravel project with opinionated conventions |
| `/sk:laravel-new` | Scaffold fresh Laravel app |
| `/sk:lint` | Auto-detect and run all project linters + dependency audits |
| `/sk:mvp` | Generate complete MVP validation app from a prompt |
| `/sk:perf` | Performance audit — bundle, N+1, Core Web Vitals, memory |
| `/sk:plan` | Create or refresh task planning files |
| `/sk:release` | Version bump + changelog + tag. Use `--android` / `--ios` for store audit. |
| `/sk:retro` | Post-ship retrospective: velocity, blockers, action items |
| `/sk:reverse-doc` | Generate architecture/design docs from existing code |
| `/sk:review` | Self-review with simplify pre-pass + multi-dimensional review |
| `/sk:schema-migrate` | Multi-ORM schema change analysis |
| `/sk:scope-check` | Compare implementation against plan, detect scope creep |
| `/sk:security-check` | OWASP security audit on changed files |
| `/sk:seo-audit` | SEO audit — dual-mode (source templates + dev server) |
| `/sk:set-profile` | Switch model routing profile for this project |
| `/sk:setup-claude` | Bootstrap project scaffolding (CLAUDE.md + tasks/ + hooks + rules) |
| `/sk:setup-optimizer` | Diagnose + update workflow + enrich CLAUDE.md |
| `/sk:skill-creator` | Create or improve ShipKit skills |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:status` | Show workflow + task status |
| `/sk:test` | Auto-detect and run all project test suites |
| `/sk:update-task` | Mark task done and log completion |
| `/sk:write-plan` | Write decision-complete plan into `tasks/todo.md` |
| `/sk:write-tests` | TDD: Write failing tests before implementation |

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

ShipKit also deploys a `validate-commit.sh` hook that warns about hardcoded secrets in staged changes before every commit.

If you discover a security issue in ShipKit itself, please open a [GitHub issue](https://github.com/kennethsolomon/shipkit/issues) or email directly rather than posting publicly.

---

## License

MIT — see [LICENSE](LICENSE) for details.

Built by [Kenneth Solomon](https://github.com/kennethsolomon).

---

<div align="center">

**Claude Code is powerful. ShipKit makes it reliable.**

</div>
