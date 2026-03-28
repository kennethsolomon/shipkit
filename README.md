<div align="center">

<img src="assets/shipkit-logo.png" alt="ShipKit" width="260" />

# SHIPKIT

**A structured, quality-gated workflow system for Claude Code.**

Ship features with TDD, security audits, and AI-powered code review —<br>
all wired into a single repeatable workflow.

[![npm](https://img.shields.io/npm/v/@kennethsolomon%2Fshipkit)](https://www.npmjs.com/package/@kennethsolomon/shipkit)
[![license](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Mac%20%2F%20Linux%20%2F%20Windows-lightgrey)](#)

```bash
npm install -g @kennethsolomon/shipkit && shipkit
```

</div>

---

## What's New (v3.16.0 — March 2026)

**Formal Agent Definitions, Path-Scoped Rules, and 2 new skills:**

- **`.claude/agents/`** — 6 formal agent definitions (backend-dev, frontend-dev, qa-engineer, security-reviewer, code-reviewer, debugger) with `memory: project`, `isolation: worktree`, and `background: true` where appropriate. `/sk:setup-claude` deploys these to every new project.
- **`.claude/rules/`** — 6 path-scoped rule files that auto-activate in Claude Code when you edit matching files: `laravel.md`, `react.md`, `vue.md`, `tests.md`, `api.md`, `migrations.md`. Stack-relevant rules are deployed by `/sk:setup-claude` automatically.
- **`/sk:ci`** — Set up GitHub Actions or GitLab CI with Claude Code workflows: auto PR review, issue triage, nightly security audit, release automation. Supports enterprise setups (AWS Bedrock OIDC, Google Vertex AI Workload Identity).
- **`/sk:plugin`** — Package your project-level customizations (skills, agents, hooks) into a distributable Claude Code plugin with a `.claude-plugin/plugin.json` manifest.
- **Skill frontmatter upgrades** — model routing (`haiku` for lightweight skills, `sonnet` for analysis), `disable-model-invocation: true` on side-effect skills (commit, release, branch), `context: fork` on expensive standalone skills (seo-audit, accessibility, reverse-doc).
- **Bug fix** — `allowed_tools` → `allowed-tools` (underscore typo silently ignored by Claude Code) fixed in 7 skills + all agent templates.

---

## What is ShipKit?

ShipKit turns Claude Code into a disciplined development partner. Instead of "write some code," every feature goes through:

**Plan** → **Build (TDD)** → **Quality Gates** → **Ship**

Each gate must pass before the next step. Lint fails? Fix it. Tests don't cover new code? Write them. Security issues? They block the PR. Quality is structural, not optional.

ShipKit auto-detects your stack — linters, test runners, frameworks, package managers. No configuration needed.

---

## Quick Start

```bash
# 1. Install
npm install -g @kennethsolomon/shipkit && shipkit

# 2. Bootstrap your project (run once)
/sk:setup-claude

# 3. Start building
/sk:start
```

That's it. `/sk:setup-claude` creates your project scaffolding: planning files, lifecycle hooks, path-scoped coding rules, and a persistent statusline — all auto-configured for your stack.

`/sk:start` is the recommended entry point — it classifies your task and routes you to the optimal flow automatically. You can also jump directly to `/sk:brainstorm`, `/sk:debug`, or any other flow entry point.

### Updating ShipKit

```bash
# Update the package
npm install -g @kennethsolomon/shipkit && shipkit

# Then in each project, update CLAUDE.md + deploy new hooks:
/sk:setup-optimizer
```

`shipkit` re-installs all skills and commands globally. `/sk:setup-optimizer` updates each project's CLAUDE.md with new commands and deploys any missing hooks.

---

## Lifecycle Hooks

`/sk:setup-claude` installs lifecycle hooks that automate common tasks. Core hooks are always installed; enhanced hooks are opt-in.

**Core hooks (always installed):**
| Hook | Event | What it does |
|------|-------|-------------|
| `session-start` | SessionStart | Loads branch, recent commits, tech debt, code health |
| `session-stop` | Stop | Logs session accomplishments to `tasks/progress.md` |
| `pre-compact` | PreCompact | Saves git state before context compression |
| `validate-commit` | PreToolUse (git commit) | Validates conventional commit format, detects secrets |
| `validate-push` | PreToolUse (git push) | Warns before pushing to protected branches |
| `log-agent` | SubagentStart | Logs sub-agent invocations to `tasks/agent-audit.log` |

**Enhanced hooks (opt-in via `/sk:setup-claude` or `/sk:setup-optimizer`):**
| Hook | Event | What it does |
|------|-------|-------------|
| `config-protection` | PreToolUse (Edit/Write) | Blocks modifications to linter/formatter configs |
| `post-edit-format` | PostToolUse (Edit) | Auto-formats with Biome/Prettier/Pint/gofmt after edits |
| `console-log-warning` | Stop | Warns about `console.log`, `dd()`, `var_dump()` in modified files |
| `suggest-compact` | PreToolUse (Edit/Write) | Suggests `/compact` after 50+ tool calls |
| `cost-tracker` | Stop | Logs session metadata to `.claude/sessions/cost-log.jsonl` |
| `safety-guard` | PreToolUse (Bash/Edit/Write) | Enforces `/sk:safety-guard` freeze/careful mode |

---

## Formal Agent Definitions

`/sk:setup-claude` deploys 6 agent definitions to `.claude/agents/` — specialized sub-agents with `memory`, `model`, `tools`, and `isolation` pre-configured.

| Agent | Model | Memory | Isolation | What it does |
|-------|-------|--------|-----------|-------------|
| `backend-dev` | sonnet | project | worktree | Backend implementation — API, data layer, migrations |
| `frontend-dev` | sonnet | project | worktree | Frontend implementation — components, routing, state |
| `qa-engineer` | sonnet | project | background | QA and E2E test writing |
| `code-reviewer` | sonnet | project | — | 7-dimension code review (read-only) |
| `debugger` | sonnet | project | — | Root-cause analysis and structured investigation |
| `security-reviewer` | sonnet | user | — | OWASP security audit (read-only, memory: user) |

`memory: project` means agents accumulate knowledge across sessions for that project. `isolation: worktree` means the agent works in a separate git worktree — no risk of clobbering your working tree. `background: true` on qa-engineer means it runs without blocking the main conversation.

---

## Path-Scoped Rules

`/sk:setup-claude` installs coding rule files in `.claude/rules/` that Claude Code auto-activates when you open or edit matching files — no manual context loading needed.

| Rule file | Activates when editing | What it enforces |
|-----------|----------------------|-----------------|
| `laravel.md` | `app/**/*.php`, `routes/**`, `config/**` | Laravel conventions, service containers, Eloquent patterns |
| `react.md` | `**/*.tsx`, `**/*.jsx`, `src/**/*.ts` | Hooks rules, component patterns, TypeScript strictness |
| `vue.md` | `**/*.vue`, `resources/js/**/*.ts` | Composition API only, `<script setup>`, Pinia patterns |
| `tests.md` | `tests/**`, `**/*.test.*`, `**/*.spec.*` | TDD standards, assertion quality, test isolation |
| `api.md` | `routes/api.php`, `app/Http/Controllers/**` | RESTful conventions, auth patterns, error response shapes |
| `migrations.md` | `database/migrations/**`, `prisma/**` | Migration safety rules, reversibility, index naming |

Stack-relevant rules are detected and deployed automatically during `/sk:setup-claude` and `/sk:setup-optimizer`.

---

## Pick Your Flow

| I want to... | Run this | What happens |
|--------------|----------|-------------|
| **Not sure — let ShipKit decide** | `/sk:start` | Classifies your task, routes to optimal flow/mode/agents |
| **Build a new feature** | `/sk:brainstorm` | Full workflow: plan → TDD → quality gates → PR |
| **Build hands-free** | `/sk:autopilot` | All 8 steps, auto-skip, auto-advance, auto-commit |
| **Full-stack feature (parallel)** | `/sk:team` | Parallel domain agents (backend + frontend + QA) |
| **Make a small change** | `/sk:fast-track` | Skip planning, keep all quality gates |
| **Fix a bug** | `/sk:debug` | Investigate → regression test → fix → gates → PR |
| **Fix a production emergency** | `/sk:hotfix` | Skip TDD, but quality gates still enforced |
| **Handle a requirement change** | `/sk:change` | Assess scope, re-enter workflow at the right step |

---

## Workflows

### Feature Flow — full planning + TDD + all gates

> Start with: `/sk:brainstorm`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:brainstorm` | Explore requirements, propose approaches | Think |
| 2 | `/sk:frontend-design` or `/sk:api-design` | *Optional* — UI mockup or API contracts (includes accessibility) | Think |
| 3 | `/sk:write-plan` | Write decision-complete plan | Think |
| 4 | `/sk:branch` | Create feature branch | Build |
| 5 | `/sk:write-tests` + `/sk:execute-plan` | TDD: write failing tests, then implement | Build |
| 6 | `/sk:smart-commit` | Conventional commit | Build |
| 7 | `/sk:gates` | All 6 quality gates (parallel batches) | Verify |
| 8 | `/sk:finish-feature` | Update task, changelog, PR, feature sync, release | Ship |

---

### Fast-Track Flow — skip planning, keep all gates

> Start with: `/sk:fast-track`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:branch` | Create feature branch | Build |
| 2 | implement directly | No TDD — write code | Build |
| 3 | `/sk:smart-commit` | Conventional commit | Build |
| 4 | `/sk:gates` | All quality gates (parallel batches) | Verify |
| 5 | `/sk:finish-feature` | Changelog + PR | Ship |

Guard rails: warns if diff > 300 lines or > 5 new files.

---

### Bug Fix Flow — investigate first, then fix

> Start with: `/sk:debug`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:debug` | Reproduce, isolate, hypothesize, verify | Think |
| 2 | `/sk:branch` | Create fix branch | Build |
| 3 | `/sk:write-tests` | Regression test that reproduces the bug | Build |
| 4 | implement the fix | Make regression test pass | Build |
| 5 | `/sk:smart-commit` | Commit fix + test | Build |
| 6 | `/sk:gates` | All quality gates (parallel batches) | Verify |
| 7 | `/sk:finish-feature` | Changelog + PR | Ship |

---

### Hotfix Flow — production emergency

> Start with: `/sk:hotfix`

| Step | Command | What it does | Phase |
|------|---------|-------------|-------|
| 1 | `/sk:debug` | Root-cause analysis | Think |
| 2 | `/sk:branch` | Create hotfix branch | Build |
| 3 | implement directly | Fix the issue | Build |
| 4 | `/sk:smart-commit` | Commit the fix | Build |
| 5 | `/sk:gates` | All quality gates (parallel batches) | Verify |
| 6 | `/sk:finish-feature` | Changelog + PR (marked as hotfix) | Ship |

After merging: add regression test + lesson to `tasks/lessons.md`.

---

### Requirement Change — mid-workflow pivot

> Run: `/sk:change` — it classifies scope and re-enters at the right step

| Tier | What changed | Example | Re-entry point |
|------|-------------|---------|----------------|
| **Tier 1** | Behavior tweak (same scope) | "Delete all" → "Delete users only" | `/sk:write-tests` |
| **Tier 2** | New requirements (new scope) | "Also add export to CSV" | `/sk:write-plan` |
| **Tier 3** | Scope shift (rethink) | "Different approach entirely" | `/sk:brainstorm` |

---

## Quality Gates (`/sk:gates`)

One command runs all 6 gates in parallel batches:

| Batch | Gates | Why this order |
|-------|-------|---------------|
| **1** (parallel) | lint + security + perf | Independent — run simultaneously |
| **2** | tests | Needs lint fixes first |
| **3** | code review | Needs deep understanding |
| **4** | E2E Tests | Needs review fixes |

Each gate auto-fixes and re-runs until clean. Fixes are squashed into one commit per gate pass. If a gate fails 3 times, it stops and asks for help.

Pre-existing issues are logged to `tasks/tech-debt.md` — not fixed inline.

---

## On-Demand Tools

Use these anytime — they're not part of any workflow.

### Intelligence

| Command | Usage | What it does |
|---------|-------|-------------|
| `/sk:learn` | `/sk:learn` | Extract reusable patterns from the session with confidence scoring (0.3-0.9) |
| `/sk:learn` | `/sk:learn --list` | Show all learned patterns |
| `/sk:context-budget` | `/sk:context-budget` | Audit token consumption across skills, agents, MCP tools, CLAUDE.md |
| `/sk:context-budget` | `/sk:context-budget --verbose` | Per-file token breakdown |
| `/sk:health` | `/sk:health` | Scorecard across 7 categories (0-70): tools, context, gates, memory, evals, security, cost |
| `/sk:eval` | `/sk:eval define auth` | Define eval criteria before coding |
| `/sk:eval` | `/sk:eval check auth` | Run evals during implementation |
| `/sk:eval` | `/sk:eval report` | Summary of all eval results with pass@k metrics |

### Session Management

| Command | Usage | What it does |
|---------|-------|-------------|
| `/sk:save-session` | `/sk:save-session` | Save branch, task, progress, open questions to `.claude/sessions/` |
| `/sk:save-session` | `/sk:save-session --name "auth-flow"` | Save with a custom name |
| `/sk:resume-session` | `/sk:resume-session` | List saved sessions and pick one to restore |
| `/sk:resume-session` | `/sk:resume-session --latest` | Auto-pick most recent session |
| `/sk:context` | `/sk:context` | Load all project context (automatic via hooks on session start) |

### Safety

| Command | Usage | What it does |
|---------|-------|-------------|
| `/sk:safety-guard` | `/sk:safety-guard careful` | Block destructive commands (rm -rf, force push, etc.) |
| `/sk:safety-guard` | `/sk:safety-guard freeze --dir src/` | Lock edits to `src/` only |
| `/sk:safety-guard` | `/sk:safety-guard guard --dir src/` | Both careful + freeze combined |
| `/sk:safety-guard` | `/sk:safety-guard off` | Disable all guards |
| `/sk:safety-guard` | `/sk:safety-guard status` | Show current mode + blocked action count |

### Code Quality

| Command | When to use |
|---------|------------|
| `/sk:scope-check` | Mid-implementation — detect scope creep (On Track / Minor / Significant / Out of Control) |
| `/sk:retro` | After shipping — analyze velocity, blockers, patterns, generate action items |
| `/sk:seo-audit` | Web projects — SEO audit with source + dev server scanning |

### Documentation & Setup

| Command | When to use |
|---------|------------|
| `/sk:reverse-doc` | Inherited codebase — generate architecture/design docs from existing code |
| `/sk:setup-optimizer` | Maintenance — diagnose, update workflow, deploy hooks, enrich CLAUDE.md |
| `/sk:ci` | Team — set up GitHub Actions / GitLab CI with PR review, issue triage, nightly audits |
| `/sk:plugin` | Distribution — package custom skills/agents/hooks as a shareable Claude Code plugin |
| `/sk:mvp` | New idea — generate a complete MVP app from a single prompt |
| `/sk:status` | Quick view of workflow and task status |
| `/sk:dashboard` | Visual Kanban board across all git worktrees |

---

## Stack Support

| Area | Supported |
|------|-----------|
| **Frameworks** | Laravel, Next.js, Nuxt, React, Vue, Node.js |
| **Linters** | Pint, ESLint, PHPStan, Rector, Prettier, Biome |
| **Test runners** | Pest, PHPUnit, Jest, Vitest, Playwright |
| **Schema / ORM** | Prisma, Drizzle, Eloquent, SQLAlchemy, ActiveRecord |
| **Release** | npm, Composer, iOS (App Store), Android (Play Store) |

---

## Code Navigation (LSP)

ShipKit configures LSP (Language Server Protocol) automatically — giving Claude Code go-to-definition, find-references, hover, and diagnostics instead of plain text search.

**`/sk:setup-claude`** and **`/sk:setup-optimizer`** both run an LSP Integration step that:
- Sets `ENABLE_LSP_TOOL=1` in `~/.claude/settings.json`
- Detects your stack and installs the appropriate language server

| Stack | Language Server |
|-------|----------------|
| TypeScript / JavaScript | `typescript-language-server` |
| PHP | `intelephense` |
| Python | `pylsp` |
| Go | `gopls` |
| Rust | `rust-analyzer` |
| Swift | `sourcekit-lsp` |

**Rule:** Prefer LSP over `rg`/Grep for code navigation. Use `rg` only when LSP is unavailable or for arbitrary text/pattern matching.

---

## MCP Servers & Plugins

Both `/sk:setup-claude` and `/sk:setup-optimizer` offer to install three tools that enhance Claude Code's reasoning, knowledge, and session visibility. All are opt-in and idempotent.

### Sequential Thinking MCP

**Why it exists:** Complex problems — architecture decisions, multi-step debugging, tasks with many constraints — benefit from structured reasoning. Without it, Claude works through hard problems in a single pass, which can miss steps or lose track of constraints.

**What it does:** Gives Claude a dedicated reasoning scratchpad. It thinks through steps sequentially before responding, without cluttering your conversation with the intermediate work.

**Benefit:** More coherent, thorough responses on hard problems. Especially useful during `/sk:brainstorm`, `/sk:debug`, and `/sk:review`.

**How it's installed:** Adds `@modelcontextprotocol/server-sequential-thinking` to `~/.mcp.json` (global, applies to all projects).

### Context7

**Why it exists:** Claude's training has a knowledge cutoff. When you're working with libraries that release frequently — React, Next.js, Tailwind, shadcn/ui — Claude's suggestions can reference outdated APIs, deprecated methods, or patterns that no longer apply.

**What it does:** Fetches current, version-accurate documentation for libraries you're using and injects it into Claude's context at the moment it's needed.

**Benefit:** Accurate code suggestions for the actual version you're running. No more `useEffect` patterns from React 17 when you're on React 19.

**How it's installed:** Enables `context7@claude-plugins-official` in `~/.claude/settings.json`.

### ccstatusline

**Why it exists:** Knowing your context window %, active model, and current branch at a glance matters. Without it, you have to run `/sk:status` or guess when to `/compact`.

**What it does:** Adds a persistent statusline to the Claude Code CLI showing context window usage, active model, git branch, and current task.

**Benefit:** Always-visible session state. Know when you're approaching context limits before it becomes a problem.

**How it's installed:** Runs `npx ccstatusline@latest` which writes the statusline config to `~/.claude/settings.json`.

---

## All Commands

<details>
<summary><strong>54 commands</strong> — click to expand</summary>

| Command | Purpose |
|---------|---------|
| `/sk:accessibility` | WCAG 2.1 AA audit |
| `/sk:api-design` | Design API contracts before implementation |
| `/sk:autopilot` | Hands-free workflow — auto-skip, auto-advance, auto-commit |
| `/sk:brainstorm` | Explore requirements and design; extracts requirements checklist |
| `/sk:branch` | Create feature branch from current task |
| `/sk:change` | Handle mid-workflow requirement changes |
| `/sk:config` | View/edit project config |
| `/sk:context` | Load project context (automatic via hooks) |
| `/sk:context-budget` | Audit context window token consumption |
| `/sk:dashboard` | Live Kanban board — sk:dashboard across worktrees |
| `/sk:debug` | Structured bug investigation |
| `/sk:e2e` | E2E Tests — behavioral verification |
| `/sk:eval` | Define, run, and report evals for agent reliability |
| `/sk:execute-plan` | Execute plan checkboxes in batches with status checkpoints |
| `/sk:fast-track` | Small changes — skip planning, keep gates |
| `/sk:features` | Sync feature specs with codebase |
| `/sk:finish-feature` | Changelog + PR |
| `/sk:frontend-design` | UI mockup + optional Pencil visual design |
| `/sk:gates` | All quality gates in parallel batches with batch checkpoints |
| `/sk:health` | Harness self-audit scorecard |
| `/sk:help` | Show all commands |
| `/sk:hotfix` | Emergency fix workflow |
| `/sk:laravel-init` | Configure existing Laravel project |
| `/sk:laravel-new` | Scaffold fresh Laravel app |
| `/sk:learn` | Extract reusable patterns from sessions |
| `/sk:lint` | Auto-detect and run all linters |
| `/sk:mvp` | Generate MVP app from a prompt |
| `/sk:perf` | Performance audit |
| `/sk:plan` | Create/refresh planning files |
| `/sk:release` | Version bump + tag (`--android` / `--ios` for store audit) |
| `/sk:resume-session` | Resume a previously saved session |
| `/sk:retro` | Post-ship retrospective |
| `/sk:reverse-doc` | Generate docs from existing code |
| `/sk:review` | 7-dimension code review with `<think>` reasoning and exhaustiveness |
| `/sk:safety-guard` | Protect against destructive ops |
| `/sk:save-session` | Save session state for continuity |
| `/sk:schema-migrate` | Database schema change analysis |
| `/sk:scope-check` | Detect scope creep mid-implementation |
| `/sk:security-check` | OWASP security audit with content isolation and CVSS scoring |
| `/sk:ci` | Set up Claude Code GitHub Actions or GitLab CI — PR review, issue triage, nightly audits, release automation |
| `/sk:plugin` | Package custom skills, agents, and hooks as a distributable Claude Code plugin |
| `/sk:seo-audit` | SEO audit for web projects |
| `/sk:set-profile` | Switch model routing profile |
| `/sk:website` | Build a complete, client-deliverable multi-page marketing website from a brief or URL. Supports `--stack nuxt`, `--stack laravel`, `--deploy`, `--revise`. Full guide: `docs/guides/sk-website-guide.md` |
| `/sk:setup-claude` | Bootstrap project scaffolding |
| `/sk:setup-optimizer` | Diagnose + update workflow + deploy hooks + enrich CLAUDE.md |
| `/sk:skill-creator` | Create or improve skills |
| `/sk:smart-commit` | Conventional commit with approval |
| `/sk:start` | Smart entry point — classifies task, routes to optimal flow |
| `/sk:status` | Show workflow + task status |
| `/sk:team` | Parallel domain agents for full-stack tasks |
| `/sk:test` | Run all test suites |
| `/sk:update-task` | Mark task done |
| `/sk:write-plan` | Write plan to `tasks/todo.md`; auto-generates `tasks/contracts.md` for API tasks |
| `/sk:write-tests` | TDD: write failing tests first |

</details>

---

## Learn More

| Topic | Where |
|-------|-------|
| Detailed workflow steps (8-step flow) | [DOCUMENTATION.md](.claude/docs/DOCUMENTATION.md) |
| Feature specifications | [docs/FEATURES.md](docs/FEATURES.md) |
| Model routing profiles & config | [DOCUMENTATION.md — Config](.claude/docs/DOCUMENTATION.md#config-reference) |
| Infrastructure (hooks, agents, rules) | [DOCUMENTATION.md — Setup](.claude/docs/DOCUMENTATION.md#what-gets-created) |
| Security & permissions | [DOCUMENTATION.md — Security](.claude/docs/DOCUMENTATION.md#security) |

---

<div align="center">

MIT License — Built by [Kenneth Solomon](https://github.com/kennethsolomon)

**Claude Code is powerful. ShipKit makes it reliable.**

</div>
