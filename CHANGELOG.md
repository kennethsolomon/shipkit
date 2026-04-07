# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v3.29.0] - 2026-04-07

### Added
- **`/sk:review` provenance sidecar (Step 11.5)** — after each review pass, writes `tasks/review-provenance.md` recording which files were read in full vs. grep-only, blast-radius verification per symbol, and which dimensions were checked vs. skipped. Adapted from Feynman's `.provenance.md` sidecar pattern.
- **Honest status labels** — `verified` / `unverified` / `inferred` / `blocked` labels now required on every `/sk:review` finding and in `tasks/progress.md` entries. Review report gains a Verification Status summary block. Prevents vague language from masking unconfirmed findings. Adapted from Feynman's `inferred` / `blocked` output convention.
- **Progress.md lab notebook protocol** — `tasks/progress.md` entries now require a `Next:` line stating what the next session should do first. Added explicit "read before resuming substantial work" rule to `CLAUDE.md`. Adapted from Feynman's `CHANGELOG.md` lab notebook pattern.
- **Slug-based artifact naming in `/sk:deep-dive`** — Stage 1 now derives a short slug from the bug description and writes intermediate trace artifacts to `tasks/.drafts/<slug>-trace.md`, preventing collision when multiple bugs are investigated concurrently. Adapted from Feynman's run-scoped file naming convention.
- **Agent orchestration principle in `/sk:autopilot` and `/sk:team`** — explicit design rule: multi-agent decomposition is an internal tactic, not primary UX. Users see synthesized results, not coordination internals. Adapted from Feynman's "Do not force chain-shaped orchestration onto the user" principle.

### Changed
- **`/sk:review` Step 11 report format** — every finding now includes a verification status tag (`[verified]`, `[inferred]`, `[blocked]`). New rule: never tag a finding `[verified]` unless the relevant file was read in full.
- **`CLAUDE.md` Project Memory section** — strengthened with lab notebook protocol, `Next:` line requirement, and honest status labels convention.
- **`.claude/docs/maintenance-guide.md`** — three new sections: "When You Change the Honest Status Label Convention", "When You Change the Progress.md Lab Notebook Protocol", "When You Change the Slug-Based Artifact Naming Convention".

---

## [v3.28.1] - 2026-04-07

### Removed
- **`commands/sk/investigate.md` and `commands/sk/respond-review.md`** — auto-generated command stubs that were skipped at install time because matching skill directories existed. Removing them eliminates drift risk and aligns with the rest of the codebase (49 other skills have no command stub). No user-facing change — `/sk:investigate` and `/sk:respond-review` still work because slash invocation resolves to the skill.

---

## [v3.28.0] - 2026-04-07

### Added
- **`/sk:investigate`** — new read-only feature-area exploration skill (Step 0.5). Dispatches 3 parallel Explore agents (entry points / data model / tests+config) and writes `tasks/investigation.md`. Wired into `/sk:start` and `/sk:autopilot` with auto-skip for concrete anchors, greenfield repos, and bug flows. Adapted from gstack's sprint-start review pattern.
- **`/sk:respond-review`** — new triage skill that classifies `/sk:review` findings into fix-now / defer / dispute buckets. Auto-invoked by `/sk:gates` Batch 3 when findings > 0. Same-finding escalation routes to the architect agent on 2nd survival. Adapted from superpowers' review-loop pattern.
- **`/sk:ci --claude` fast-path** — scaffolds ShipKit-aware claude-code-action workflow with 8-dimension review prompt and `claude` label trigger. Drop-in CI config for on-demand PR review.
- **`<private>...</private>` tag convention** — content wrapped in these tags is never written to persistent memory surfaces (auto-memory, `tasks/*.md`, commits, PRs, changelogs). Documented in `CLAUDE.md` Project Memory section. Adapted from claude-mem's exclusion mechanism.

### Changed
- **`/sk:gates` Batch 3** now auto-invokes `sk:respond-review` when review returns any Critical/Warning findings, keeping gates as the single source of re-run logic.
- **`/sk:start`** classifier detects unfamiliar brownfield areas (subsystem references + exploration verbs) and routes to `/sk:investigate` before brainstorm. New `--investigate` / `--skip-investigate` override flags.
- **`/sk:autopilot`** adds Step 0.5 (Investigate) with intensity auto-select = `lite`.
- **`CLAUDE.md` + template** updated with Step 0.5, Fix & Retest row for review findings, Memory Privacy subsection, and new Commands table entries.

---

## [v3.27.1] - 2026-04-06

### Fixed
- **Session-start hook staleness detection** — displays `(stale — todo.md last modified Xd ago)` when todo.md is older than 7 days, preventing misleading "Current task" display from unrelated projects
- **`/sk:steal` maintenance sync** — added explicit post-implementation step to sync derived files via maintenance guide after ShipKit-internal adaptations

---

## [v3.27.0] - 2026-04-06

### Added
- **Intensity routing** — new `intensity` config (lite/full/deep) with per-phase auto-select in autopilot, `--intensity` flag on `/sk:start`, and intensity sections in sk:review (default: deep), sk:explain, sk:gates (default: lite)
- **Anti-pattern blocks** — skill-creator now guides new skills to include `## Anti-Patterns (NEVER do these)` sections for explicit failure mode documentation
- **Auto-clarity escape hatch** — skill-creator guides style-modifying skills to define when to temporarily disable themselves (security warnings, destructive ops)
- **Skill benchmarking** — new `/sk:eval benchmark <skill>` subcommand to measure token/quality impact with parallel with/without-skill trials
- **Multi-format plugin distribution** — new `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` manifests with CI auto-sync workflow
- Feature specs for sk:skill-creator and sk:eval

### Changed
- `.shipkit/config.json` now supports `intensity` and `intensity_overrides` fields (follows existing profile/model_overrides pattern)
- Enriched `.claude-plugin/plugin.json` with version and skills path

---

## [v3.26.1] - 2026-04-05

### Fixed
- **Installer crash on broken symlinks** — `shipkit` install now detects and removes broken symlinks (from old `shipit` path) before copying skill directories, preventing ENOENT errors on `mkdirSync`
- **Installer resilience** — individual skill install failures no longer crash the entire install; failed skills are reported as warnings

---

## [v3.26.0] - 2026-04-05

### Added
- **`/sk:steal` skill** — review external sources (GitHub repos, articles, screenshots) and adapt useful patterns into your project
- **`/sk:explain` skill** — structured code explainer: one-sentence summary, mental model, ASCII diagram, key details, modification guide
- **`scan-secrets.sh` hook** — PreToolUse hook detects AWS keys, GitHub tokens, API keys, Slack tokens, private keys, and connection strings before writing
- **`warn-large-files.sh` hook** — blocks writes to node_modules, vendor, dist, build, __pycache__, .venv, and binary file extensions
- **`doc-reviewer` agent** — reviews documentation for accuracy, completeness, staleness, and clarity by cross-referencing source code
- **`security.md` rule** — path-scoped security rules (auth, middleware, crypto files)
- **`error-handling.md` rule** — path-scoped error handling patterns (exceptions, services files)
- **`frontend.md` rule** — framework-agnostic design tokens, accessibility checklist, performance rules
- **`CLAUDE.local.md.example`** — personal overrides template for team projects (gitignored)
- **`/sk:frontend-design` design principle table** — 11 principles (glassmorphism, brutalism, minimalism, etc.) with "best for" guidance

### Changed
- **`/sk:review` now 8-dimension** — added Documentation dimension (Step 9), delegates to `doc-reviewer` agent when doc files changed
- **`/sk:gates` Batch 3** — `doc-reviewer` runs in parallel with `code-reviewer` when doc files are in the diff
- **`config-protection.sh` hook** — now also blocks .env, .pem, .key, lock files, generated code, and sensitive directories
- **`safety-guard.sh` hook** — added DELETE without WHERE, TRUNCATE TABLE, curl|sh piping, npm/cargo/gem/twine publish, mkfs/dd/fdisk
- **`post-edit-format.sh` hook** — added Ruff, Black+isort (Python), and Dart formatter support
- **`security-reviewer` agent** — added injection grep checklist (SQL, command, XSS, template, path traversal, SSRF, deserialization)
- **`code-reviewer` agent** — added "Correctness Patterns to Catch" and "What NOT to Flag" sections
- **`migrations.md` rule** — added drizzle, knex, sequelize, typeorm, flyway, liquibase migration paths
- Agent count: 13 → 14 core agents; Hook count: 7/7 → 7/9 (core/enhanced)

---

## [v3.25.1] - 2026-04-02

### Fixed
- **`/sk:release` npm publish guard** — publishable package check now requires `name` + `main`/`bin`/`exports` field (prevents accidentally publishing apps that lack `"private": true`); adds confirmation prompt + OTP note before publishing.
- **`/sk:e2e` spec detection scoped to `e2e/` and `tests/e2e/`** — previous `find` matched unit test specs (Vitest/Jest), causing false Playwright CLI priority match.
- **`/sk:setup-claude` agent-browser labeled as CLI tool** — clarifies check method (PATH, not `claude plugin list`).
- **`/sk:finish-feature` `/sk:review` gate wording** — rephrased to "not certain it was run" (original wording was unenforceable).
- **`/sk:e2e` Step 4b terminus** — added missing "Skip to Step 5".
- **Arch change log entries** — added `2026-04-02-agent-browser-e2e-integration.md` and `2026-04-02-retro-enforcement-rules.md`.

---

## [v3.25.0] - 2026-04-02

### Added
- **agent-browser integration in `/sk:e2e`** — accessibility tree snapshots (text refs like `@e1`, `@e2`) replace screenshot-based verification. 10–20× fewer tokens than Playwright MCP. Priority order: Playwright CLI when spec files already exist → agent-browser for interactive verification → prompt to install one if neither found. Install: `npm install -g agent-browser && agent-browser install`.
- **agent-browser in `/sk:setup-claude` and `/sk:setup-optimizer`** — added as item 5 in the MCP/plugins install prompt. Setup optimizer now reports `X/5 configured` and can install agent-browser automatically.
- **agent-browser in README** — new "Recommended CLI Tools" table under MCP Servers section.

### Changed
- **`/sk:e2e` description updated** — now accurately reflects agent-browser as the preferred interactive verification tool, Playwright CLI as the spec-file runner.
- **`.claude/docs/maintenance-guide.md`** — "When You Add/Remove a Community Plugin" section split into two sub-types: Claude Plugin (installed via `/plugin`) and CLI Tool (installed via `npm install -g`). agent-browser is the first CLI tool sub-type. Different check command, install steps, and README section for each.

### Fixed
- **`tasks/todo.md` now enforced as a workflow rule** — CLAUDE.md rule 8 added: before any session touching ≥ 3 files, create `tasks/todo.md` with at least 5 checkboxes. Mirrored to `CLAUDE.md.template` for new projects. (6th retro noting this issue — escalated from habit to rule.)
- **`/sk:finish-feature` blocks on missing `/sk:review`** — "Before You Start" section now counts SKILL.md files changed on the branch. If ≥ 3 and `/sk:review` hasn't run, finalize is blocked. (4th retro noting this issue — escalated to hard gate.)
- **`/sk:release` now runs `npm publish`** — requires confirmation prompt + OTP note before publishing; publishable package check requires `name` + `main`/`bin`/`exports` field (prevents accidentally publishing apps that lack `"private": true`). For scoped packages runs `npm publish --access public`.
- **`/sk:e2e` spec detection scoped to `e2e/` and `tests/e2e/`** — previous `find` was too broad and matched unit test specs (Vitest/Jest), causing false Playwright CLI priority match. Now only E2E directories count.
- **`/sk:setup-claude` agent-browser item clarified as CLI tool** — labeled `*(CLI tool — check via PATH, not via claude plugin list)*` to prevent wrong install state check.
- **Arch change log entries** — added `2026-04-02-agent-browser-e2e-integration.md` and `2026-04-02-retro-enforcement-rules.md`.

---

## [v3.24.1] - 2026-04-02

### Fixed
- `skills/sk:setup-optimizer/SKILL.md` — hook report string count corrected from `X/6` to `X/7` for both core and enhanced hooks; deployed hooks example now includes `keyword-router.sh` and `auto-progress.sh`.

### Changed
- `.claude/docs/maintenance-guide.md` — added "When You Change a Skill's Behavior" section, "How Updates Reach Existing Projects" propagation table, "Quick Checklist After Any Hook Change", hook count update rule, README as a touchpoint for hook changes, and expanded canonical file roles table.

---

## [v3.24.0] - 2026-04-02

### Added
- **Progressive disclosure in `/sk:context`** — index pass reads only what the SESSION BRIEF needs upfront: `tasks/findings.md` first 50 lines, `tasks/lessons.md` count + last 30 lines, `tasks/tech-debt.md` headers only. Full content available on-demand via `"load findings"` / `"load lessons"` / `"load debt"` / `"load all"`. Cuts cold-start context 60–80% on mature projects with large task files. Adapted from claude-mem (thedotmack/claude-mem).
- **Context Index** in `/sk:context` output — a compact section after the SESSION BRIEF showing which heavy files are available on demand with approximate sizes and trigger phrases.
- **`auto-progress.sh`** (enhanced/opt-in hook, PostToolUse) — auto-logs `git commit`, `git push`, and `git tag` events to `tasks/progress.md`. Passive safety net for the most-skipped manual workflow step. Never blocks, exit 0 always, only writes if `tasks/progress.md` exists. Adapted from claude-mem.

### Changed
- `/sk:context` reading strategy updated: findings.md, lessons.md, and tech-debt.md are now read progressively (index pass only by default). Behavior is identical for the SESSION BRIEF; difference is context efficiency.
- `skills/sk:setup-optimizer/SKILL.md` enhanced hooks list updated to include `auto-progress.sh`.
- README hooks table updated: `keyword-router` added to always-installed table (missing since v3.23.0); `auto-progress` added to opt-in table.

---

## [v3.23.0] - 2026-04-01

### Added
- **`/sk:deep-interview`** — Socratic requirements-gathering skill with mathematical ambiguity scoring (4 weighted dimensions: Goal 35%, Constraint 25%, Success Criteria 25%, Context 15%). Blocks until clarity ≥80%. One question per round. Outputs `tasks/spec.md`. Auto-triggered by `/sk:autopilot` and `/sk:start` for vague/open-ended tasks.
- **`/sk:deep-dive`** — Two-stage pipeline for unknown-cause bugs: 3 parallel trace lanes (git history, code structure, runtime behavior) → pre-seeded deep interview (threshold 25%) → `tasks/spec.md` with root cause + fix scope. Auto-triggered by `/sk:autopilot` and `/sk:start` when bug signals detected with no known cause.
- **Magic keyword hook** (`keyword-router.sh`) — `UserPromptSubmit` hook. Prefixes `autopilot:`, `debug:`, `fast:`, `interview:`, `team:` inject routing context; Claude invokes the corresponding skill automatically.
- **`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`** env var in `.claude/settings.json` — enables native Claude Code agent team spawning for `/sk:team`.
- **Step 0 task classification in `/sk:autopilot`** — silently routes to `/sk:deep-dive` (Check A: unknown-cause bug) or `/sk:deep-interview` (Check B: vague feature) before entering the main workflow. Clear input (Check C) skips Step 0.
- **Acceptance criteria in `/sk:autopilot`** — direction approval now includes explicit testable acceptance criteria. Step 7.5 verifies all criteria pass before PR push.
- **Deep-dive + vague-feature routing in `/sk:start`** — flow detection now includes `deep-dive` (bug signals + no known cause). Vague-feature flag routes to `/sk:deep-interview` in manual mode. New override flags: `--deep-dive`, `--interview`.
- **Auto-consensus in `/sk:write-plan`** — automatically runs Architect + Critic review loop when high-risk keywords detected (auth, migration, payment, breaking change, deploy, credentials). `--consensus` forces it; `--no-consensus` skips.
- **ultraqa cycling in `/sk:test`** — replaces blind retry with 3-cycle architect-diagnosed loop. Same-failure detection (first 30 chars): identical failures across 2 attempts trigger architect diagnosis immediately.
- **ultraqa cycling in `/sk:gates`** — failure handling now spawns `architect` agent for root cause diagnosis on repeated gate failures. Same-failure detection triggers early.
- **Feature specs** `docs/sk:features/sk-deep-interview.md` and `docs/sk:features/sk-deep-dive.md`.
- **Architectural change log** entry for this release.

### Changed
- `/sk:brainstorm` Step 1 reads `tasks/spec.md` if present; treats its acceptance criteria as fixed constraints (skips re-asking).
- `/sk:autopilot` and `/sk:start` feature specs updated to document new routing logic.
- `commands/sk/help.md` Feature Workflow table, Bug Fix Workflow, and All Commands updated.
- `skills/sk:setup-optimizer` now checks for `sk:deep-interview`, `sk:deep-dive`, and `keyword-router.sh`.
- README commands count updated 44 → 46.
- All templates updated: `CLAUDE.md.template`, `settings.json.template`, `write-plan.md.template`, `brainstorm.md.template`, `keyword-router.sh` template.

---

## [v3.22.0] - 2026-03-31

### Added
- **`/sk:deps-audit`** — new quality gate skill: CVE scanning, license compliance, and outdated package detection across npm, Composer, Cargo, pip, Go modules, and Bundler. Auto-fixes safe patch/minor version bumps. Runs automatically in `/sk:gates` Batch 1 as the 4th parallel agent (gate count 6 → 7).
- **context-mode plugin integration** — `/sk:setup-claude` and `/sk:setup-optimizer` now prompt to install/update `mksglu/context-mode` (96% average context savings via SQLite-backed output summarization). Documented in README under "Recommended Community Plugins".
- **CI monitor loop in `/sk:finish-feature`** — mandatory Step 7.5 after PR creation: polls CI every 60s, reads all auto-reviewer comments (Copilot, CodeRabbit, etc.), iterates until CI green + zero unresolved threads before calling the feature done.
- **Task onboarding record in `/sk:start`** — Step 3.5 writes `tasks/onboarding/[task-slug].md` after routing, capturing flow, mode, agents, and codebase state for session continuity.
- **Skill improvement pass in `/sk:learn`** — Phase 6 scans the session for evidence of skill underperformance and proposes targeted SKILL.md diffs via `/sk:skill-creator`.
- **Feature spec** `docs/sk:features/sk-deps-audit.md` — full business logic, edge cases, and hard rules for the new skill.
- **Maintenance guide** updated with "When You Add/Remove a Community Plugin" section.
- **Architectural change log** entry for this release.

### Changed
- `/sk:gates` Batch 1 now runs 4 parallel agents (lint + security + perf + deps-audit) instead of 3.
- `/sk:autopilot` Step 7 gate list updated to match new gate order.
- `/sk:setup-optimizer` Step 1.7 checks 4 global plugins instead of 3; includes context-mode install/update.
- README commands count updated 43 → 44.

---

## [v3.21.0] - 2026-03-30

### Added
- **Laravel Boost MCP** (`laravel/boost`) — project-level MCP server auto-configured in `.mcp.json` for Laravel projects. Provides 9 tools: `DatabaseSchema`, `DatabaseQuery`, `DatabaseConnections`, `SearchDocs`, `ReadLogEntries`, `BrowserLogs`, `LastError`, `GetAbsoluteUrl`, `ApplicationInfo`
- **Stack-conditional MCP management** — `skill-profiles.md` now maps MCP servers to stacks. `sk:setup-claude` creates `.mcp.json`, `sk:setup-optimizer` Step 0.5 adds/removes/updates entries when stack changes (including Sail migration: switches between `php` and `vendor/bin/sail` command)
- **Laravel framework detection in `apply_setup_claude.py`** — reads `composer.json`, detects Inertia+React, Inertia+Vue, Livewire, and API-only flavors, Eloquent ORM, Pest testing, and correct build commands (`php artisan serve`, `vendor/bin/pint`, `vendor/bin/pest`)
- **`.mcp.json` generation in `apply_setup_claude.py`** — deterministic apply now writes `.mcp.json` for Laravel and removes `laravel-boost` for non-Laravel stacks
- **Laravel Boost MCP section in `laravel.md.template`** — documents all 9 MCP tools and when to use each
- **10 new tests** in `test_apply_setup_claude.py` covering Laravel detection flavors, MCP create/remove/update/Sail/user-entry-preservation, and rules filter

### Changed
- `README.md` MCP Servers section split into **Global** (opt-in, `~/.mcp.json`) and **Project-level** (stack-conditional, `.mcp.json`)
- `DOCUMENTATION.md` setup-claude entry now distinguishes global MCP from project-level MCP
- `sk:setup-optimizer` Step 1.7 renamed to "Global MCP" — project MCP is exclusively owned by Step 0.5

---

## [v3.20.0] - 2026-03-29

### Added
- **Stack-aware skill filtering** — `/sk:setup-claude` now auto-detects project stack (14 frameworks supported) and installs only relevant skills, agents, and rules at the project level (`.claude/skills/`, `.claude/agents/`, `.claude/rules/`)
- `skills/sk:setup-claude/references/skill-profiles.md` — source of truth mapping 44 skills, 13 agents, and 6 rules to their applicable stacks
- `.shipkit/config.json` extended schema — new `stack` (detected, detected_at, capabilities) and `skills` (extra, disabled) fields
- Config Reference section in DOCUMENTATION.md — full schema docs, stack detection priority, model routing profiles

### Changed
- `/sk:setup-claude` — new Phase 0.5 adds stack detection + project-level skill/agent/rule installation before CLAUDE.md generation
- `/sk:setup-optimizer` — new Step 0.5 re-detects stack, diffs changes, syncs skills/agents/rules with user confirmation
- CLAUDE.md compressed ~22% — merged step table + details, tables for flows/rules, tighter prose
- 13 skill SKILL.md files compressed 12-58% — prose→tables/lists, removed duplication, all instructions preserved
- README.md — added "Stack-Aware Skill Filtering" section with override examples

---

## [v3.19.0] - 2026-03-29


### Added
- `sk:laravel-deploy` — new skill for deploying Laravel apps to Laravel Cloud via the `cloud` CLI; gates must pass before any deploy
- `sk:laravel-init` now suggests installing official Laravel plugins (`laravel-simplifier` + `laravel-cloud`) after setup with a `[y/n]` prompt
- `sk:setup-claude` Laravel Detection: added "Laravel Official Plugins" subsection prompting plugin install, "Code Refinement" sub-agent pattern referencing `laravel-simplifier` after `/sk:execute-plan`, and "Laravel Commands" section that injects `sk:laravel-deploy`/`sk:laravel-init`/`sk:laravel-new` into generated CLAUDE.md command tables
- `laravel.md.template` — added "Code Refinement" standing rule documenting `laravel-simplifier` usage for all ShipKit-scaffolded Laravel projects


---


## [v3.18.0] - 2026-03-29


### Added
- _Upcoming features and improvements will be listed here_

### Changed
- _Behavioral changes will be listed here_

### Deprecated
- _Features being phased out will be listed here_

### Removed
- _Features being removed will be listed here_

### Fixed
- _Bug fixes will be listed here_

### Security
- _Security fixes will be listed here_


---


## [v3.18.0] - 2026-03-29


### Added
- Steps 5.5 (Scope Check), 8.5 (Learn), 8.6 (Retro) wired into the standard workflow, autopilot, and finish-feature
- `/sk:save-session` session-end hook: session-stop.sh now saves a minimal snapshot to `.claude/sessions/auto-YYYY-MM-DD-branch.md` on every session end
- `.claude/docs/maintenance-guide.md`: permanent map of which files to touch when changing workflow steps, agents, skills, gates, or hooks

### Changed
- `commands/sk/help.md`: Feature Workflow table now matches CLAUDE.md exactly — Step 2 (Design) restored, gates collapsed to single `/sk:gates` row
- `skills/sk:setup-claude/templates/CLAUDE.md.template`: new project bootstraps now include steps 5.5, 8.5, 8.6
- `skills/sk:setup-optimizer/SKILL.md`: diagnostics updated from "8 steps" to "11 steps" — prevents false-positive outdated-workflow flags on correctly updated projects
- `skills/sk:gates/SKILL.md`: perf auto-skip rule now documented in the skill (was only in CLAUDE.md); stale step references updated from old 21-step numbering
- All "8-step workflow" references updated to "8-phase workflow" across autopilot, team, DOCUMENTATION.md

### Fixed
- `.claude/agents/debugger.md`, `qa-engineer.md`, `tech-writer.md`: added DESIGN NOTE comments explaining why isolation is intentionally omitted — prevents false-positive audit flags


---


## [v3.17.1] - 2026-03-29


### Changed
- **README rewrite** — scenario-first structure with 5 tutorial walkthroughs (feature, bug fix, hotfix, small change, requirement change); agents table now shows `Invoked by` column; condensed MCP section; removed What's New and redundant Highest ROI sections

### Security
- _Security fixes will be listed here_


---


## [v3.17.0] - 2026-03-29


### Changed
- **Agent wiring** — 9 workflow skills now explicitly invoke named agents by name instead of generic descriptions: `sk:team` → `backend-dev`, `frontend-dev`, `mobile-dev`, `qa-engineer`; `sk:gates` → `security-reviewer`, `performance-optimizer`, `code-reviewer`; `sk:brainstorming` → `architect` (complex tasks); `sk:debug` → `debugger`; `sk:schema-migrate` → `database-architect`; `sk:perf` → `performance-optimizer`; `sk:security-check` → `security-reviewer`; `sk:ci` → `devops-engineer`; `sk:reverse-doc` → `tech-writer`


---


## [3.16.1] — 2026-03-29 — Fix duplicate slash commands

### Fixed
- **Duplicate slash commands** — `/sk:security-check`, `/sk:start`, and others appeared 2–3× in autocomplete. Root cause: three registration sources (global skill, global command file, project-level command file). Removed 12 stale command files from `~/.claude/commands/sk/` superseded by skills, deleted `commands/sk/security-check.md` from the project, and added a cleanup pass in `bin/shipkit.js install()` that removes stale command files after skills are installed — preventing recurrence on future installs.

## [3.16.0] — 2026-03-29 — Claude Code Infrastructure Upgrade + 13 Formal Agents

### Added
- **13 formal agent definitions** — deployed by `/sk:setup-claude` to every project:
  - *Implementation:* `backend-dev`, `frontend-dev`, `mobile-dev` (React Native/Expo/Flutter)
  - *Quality:* `qa-engineer`, `code-reviewer`, `security-reviewer`, `performance-optimizer`
  - *Design:* `architect` (pre-plan system design), `database-architect` (migration safety)
  - *Operations:* `devops-engineer`, `debugger`, `refactor-specialist`, `tech-writer`
- **`.claude/rules/`** — 6 path-scoped coding rule files that auto-activate per directory:
  `laravel.md`, `react.md`, `vue.md`, `tests.md`, `api.md`, `migrations.md`
- **`/sk:ci`** — GitHub Actions + GitLab CI integration: PR review, issue triage, nightly audit, release automation workflows. Supports AWS Bedrock (OIDC) and Google Vertex AI (Workload Identity)
- **`/sk:plugin`** — Package project-level customizations (skills, agents, hooks) as a distributable Claude Code plugin with `.claude-plugin/plugin.json` manifest
- **`skills/sk:security-check/SKILL.md`** — security-check promoted to a full skill with upgraded frontmatter (`model: sonnet`, `disable-model-invocation: true`)
- **`skills/sk:setup-claude/templates/.claude/rules/`** — added `vue.md.template`, `migrations.md.template`; added proper `paths:` frontmatter to all 5 existing templates
- **README — Highest ROI Workflow** — comprehensive guide showing how every feature works together, with a "which tool for which situation" reference table
- **DOCUMENTATION.md — Formal Agents reference** — full invocation guide for all 13 agents with `when to use` + example invocations
- **DOCUMENTATION.md — sk:ci and sk:reverse-doc** — proper "when and how to use" sections with workflow context

### Changed
- **Skill frontmatter — model routing:** `model: haiku` → sk:lint, sk:context, sk:health, sk:seo-audit, sk:accessibility; `model: sonnet` → sk:review, sk:perf, sk:e2e, sk:security-check
- **Skill frontmatter — side-effect guard:** `disable-model-invocation: true` added to sk:smart-commit, sk:release, sk:safety-guard, sk:branch, sk:finish-feature, sk:hotfix
- **Skill frontmatter — isolated context:** `context: fork` added to sk:seo-audit, sk:accessibility, sk:reverse-doc
- **`/sk:setup-optimizer`** — updated to check for 13 core agents (was 6), 6 rule files, and stale agent frontmatter

### Fixed
- **`allowed_tools` → `allowed-tools`** — fixed underscore typo (silently ignored by Claude Code) in sk:gates, sk:team, sk:scope-check, sk:start, sk:fast-track, sk:retro, sk:autopilot, sk:reverse-doc, and all 8 agent templates in sk:setup-claude
- **`tests/verify-workflow.sh`** — fixed 10 stale assertions checking for removed thin command wrappers; tests now check SKILL.md paths (343/343 passing)

## [3.15.3] — 2026-03-28 — Fix duplicate skill/command registrations

### Fixed
- **`commands/sk/`** — Removed 11 thin command wrappers (`autopilot`, `context-budget`, `eval`, `health`, `learn`, `resume-session`, `safety-guard`, `save-session`, `start`, `team`, `website`) that duplicated corresponding `skills/sk:*/SKILL.md` entries, causing each to appear multiple times in the Claude Code command picker
- **`bin/shipkit.js`** — Added deduplication guard: install now skips any `commands/sk/<name>.md` file when a corresponding `skills/sk:<name>/` directory exists, preventing the issue from recurring when new skills are added

## [3.15.2] — 2026-03-28 — Fix duplicate /sk:website command

### Fixed
- **`commands/sk/website.md`** — Replaced full content with thin wrapper (matches autopilot pattern), eliminating the duplicate `/sk:website` entry in Claude Code command autocomplete

## [3.15.1] — 2026-03-28 — sk:website Extensions (multi-stack + deploy)

### Added
- **`/sk:website --stack nuxt`** — Build client marketing sites with Nuxt 3 + Vue 3 + Tailwind instead of Next.js
- **`/sk:website --stack laravel`** — Build client marketing sites with Laravel 11 + Blade + Tailwind + Alpine.js
- **`/sk:website --deploy`** — Optional deploy step after build: detects Vercel CLI, falls back to Netlify CLI, always confirms before deploying, updates HANDOFF.md with live URL
- **`skills/sk:website/references/stacks/nextjs.md`** — Next.js App Router reference: multi-page file structure, site config pattern, per-page SEO metadata, contact API route, sitemap/robots, WhatsApp React component, dev/build commands
- **`skills/sk:website/references/stacks/nuxt.md`** — Nuxt 3 reference: multi-page file structure, site config, `useSeoMeta` per-page SEO, contact server route, WhatsApp Vue SFC component, dev/build commands
- **`skills/sk:website/references/stacks/laravel.md`** — Laravel 11 + Blade reference: multi-page views, `config/site.php` config, per-page SEO in layouts, contact controller with honeypot, sitemap route, WhatsApp Blade partial, deploy host options

### Changed
- **`skills/sk:website/SKILL.md`** — Added Mode Detection rows for `--stack` and `--deploy` flags; added Stack Detection table (flag → auto-detect → default Next.js priority order); Step 1 now shows detected stack in confirmation block; Step 3a now reads matched stack reference before scaffolding; Step 3d WhatsApp section now stack-aware (React TSX / Vue SFC / Blade partial); added Step 8 Deploy (flag-gated, always confirms before deploying)
- **`commands/sk/website.md`** — Updated description and usage examples with `--stack` and `--deploy` flags; added stack comparison table
- **`docs/guides/sk-website-guide.md`** — Added "Choosing a Stack" section with comparison table and auto-detection rules; added "Using the Deploy Flag" section with requirements, flow, and safety note; updated Quick Start with new flag examples; updated WhatsApp section with stack-specific replacement instructions; updated Related Commands table

## [3.15.0] — 2026-03-28 — sk:website Client Website Builder

### Added
- **`/sk:website`** — New skill for building complete, client-deliverable multi-page marketing websites from a brief, URL, or one sentence. Ports the best of website-studio into shipkit, making shipkit the all-in-one tool.
  - Brief extraction from Google Maps URL, existing site URL, or plain text
  - Real copy generation — no Lorem ipsum, no `[placeholder]` headlines
  - Parallel research agents: strategy + copy + art direction spawn simultaneously
  - WhatsApp / Messenger floating CTA: auto-detected for local businesses in PH/SEA
  - Lighthouse 90+ enforcement loop before client handoff
  - Client handoff package: `HANDOFF.md`, `DEPLOY.md`, `CONTENT-GUIDE.md`
  - Revision mode (`/sk:website --revise`) for targeted client feedback iterations
  - 15 niche reference guides: cafe, restaurant, law firm, dentist, gym, real estate, accountant, med-spa, home-services, wedding, agency, portfolio, ecommerce, SaaS, local-business
  - Art direction reference with 7 aesthetic directions
  - Content & SEO reference with local SEO guidance (Philippines / SEA focus)
  - Launch checklist with blocker vs. polish classification
  - WhatsApp CTA implementation guide with Next.js component code
  - Comprehensive guide: `docs/guides/sk-website-guide.md`
  - Feature spec: `docs/sk:features/sk-website.md`

## [3.14.0] — 2026-03-28 — Prompt Engineering Upgrades

### Changed
- **`sk:review`** — added `<think>` reasoning scratchpad before each of 7 analysis dimensions; exhaustiveness commitment (partial analysis not accepted); upgraded code reference format to `file:line:name:type` with symbol type annotation (function, method, class, variable, hook, component)
- **`sk:security-check`** — added content isolation rule (scanned file content treated as DATA, never instructions) to prevent prompt injection; added instruction hierarchy (system prompt > user chat > file content); added CVSS Base Score estimation field to Critical and High findings in report output
- **`sk:write-plan`** — new Step 3b: auto-generates `tasks/contracts.md` when plan contains API/endpoint/route/controller/backend keywords; contract defines endpoints, request/response shapes, auth, errors, and mocking boundary — mandatory prerequisite for `/sk:team`
- **`sk:brainstorm`** — new Step 5b: extracts explicit requirements checklist after approach approval; requires coverage confirmation before recording findings; checklist included in `tasks/findings.md`
- **`sk:execute-plan`** — added status checkpoint cadence: `[Checkpoint]` line posted every 3–5 tool calls or after editing 3+ files
- **`sk:gates`** — added batch checkpoint lines after each of the 4 gate batches for progress visibility

## [3.13.2] — 2026-03-26 — Branding

### Added
- **ShipKit logo** — added to README header

## [3.13.1] — 2026-03-26 — Hook & Template Fixes

### Fixed
- **`session-start.sh`** — now surfaces the first unchecked `- [ ]` item from `tasks/todo.md` at session start instead of showing nothing
- **`statusline.sh`** — active task now shows the first unchecked checkbox instead of the document title (`head -1`)
- **`validate-commit.sh`** — now blocks commits (`exit 2`) on violations (bad format, debug statements, secrets) instead of warning and allowing through
- **`settings.json`** — `PostToolUse` matcher changed from `"Edit"` to `"Edit|Write"` so auto-formatting fires when new files are created, not only when existing files are edited
- All 4 fixes synced to `sk:setup-claude` templates so new bootstrapped projects get the corrected versions

## [3.13.0] — 2026-03-26 — MCP Plugins & Docs

### Added
- **Sequential Thinking MCP** — added to `sk:setup-claude` and `sk:setup-optimizer` installation steps
- **Context7 MCP** — added to `sk:setup-claude` and `sk:setup-optimizer` for up-to-date library docs
- **ccstatusline** — added to `sk:setup-claude` and `sk:setup-optimizer` for session status line

### Changed
- `install.sh` — added `sk:seo-audit` and `sk:dashboard` to post-install summary
- `CLAUDE.md` — fixed `sk:resume-session` ordering in Commands table (alphabetical)

## [3.12.0] — 2026-03-26 — LSP Integration

### Added
- **LSP integration** — `ENABLE_LSP_TOOL=1` added to global `~/.claude/settings.json`; `typescript-language-server` installed for JS/TS projects
- **`sk:setup-claude`** — new LSP Integration step: detects stack, checks and installs the appropriate language server (TypeScript, PHP, Python, Go, Rust, Swift)
- **`sk:setup-optimizer`** — new Step 1.6 LSP Integration Check: verifies `ENABLE_LSP_TOOL` env, installs missing language server per detected stack
- **Code Navigation section** — added to `CLAUDE.md.template` (both setup-claude and setup-optimizer), `CLAUDE.md` (this project), and `~/.claude/CLAUDE.md` (global); setup-claude and setup-optimizer insert/update this section on every run

### Changed
- `settings.json.template` — includes `ENABLE_LSP_TOOL=1` env block so all bootstrapped projects have LSP enabled

## [3.11.1] — 2026-03-25 — Documentation

### Changed
- Fixed command count in README from 51 to 52
- Expanded on-demand tools section in DOCUMENTATION.md with high-ROI usage guide (before/during/after workflow)

## [3.11.0] — 2026-03-25 — ECC Intelligence Upgrade

### Added
- **`sk:learn`** — extract reusable patterns from sessions into learned instincts with confidence scoring (0.3-0.9), project/global scoping, and export/import for sharing
- **`sk:context-budget`** — audit context window token consumption across agents, skills, rules, MCP tools, and CLAUDE.md; detect bloat; recommend top 3 optimizations with token savings
- **`sk:health`** — harness self-audit scorecard across 7 categories (Tool Coverage, Context Efficiency, Quality Gates, Memory Persistence, Eval Coverage, Security Guardrails, Cost Efficiency), scored 0-70
- **`sk:save-session`** — save current session state (branch, task, progress, findings) to `.claude/sessions/` for cross-session continuity
- **`sk:resume-session`** — list and restore saved sessions with full context injection
- **`sk:safety-guard`** — destructive operation protection with 3 modes: careful (block destructive commands), freeze (lock edits to directory), guard (both combined)
- **`sk:eval`** — eval-driven development with capability/regression evals, code-based/model-based/human graders, pass@k and pass^k metrics
- **Enhanced hooks** — 6 new hook scripts: `config-protection.sh` (block linter config edits), `post-edit-format.sh` (auto-format after edits), `console-log-warning.sh` (warn on debug statements), `cost-tracker.sh` (session metadata logging), `suggest-compact.sh` (suggest /compact at 50+ tool calls), `safety-guard.sh` (freeze/careful mode enforcement)

### Changed
- **`sk:start`** — added Missing Context Detection phase (flags missing acceptance criteria, scope boundaries, security requirements)
- **`sk:brainstorm`** — added search-first research phase (check repo, package registries, existing skills before proposing custom solutions)
- **`sk:setup-claude`** — added Phase 0 Reconnaissance for first-time setup (directory scan, entry point detection, architecture classification, data flow trace); enhanced hooks now prompt for opt-in installation
- **`sk:setup-optimizer`** — added hooks detection and installation prompting; now checks for all 7 new commands in CLAUDE.md
- **`settings.json.template`** — wired 6 new hooks (config-protection, post-edit-format, suggest-compact, safety-guard, console-log-warning, cost-tracker)
- **`set-profile`** — added model routing for 7 new skills

## [3.10.2] — 2026-03-24 — UX/UI Design Intelligence Upgrade

### Changed
- **`sk:frontend-design`** — added UX Quality Constraints section with 99 rules across 10 priority-ordered categories (accessibility, touch, performance, style, layout, typography, animation, forms, navigation, charts); added Professional UI Anti-Patterns section; added Pre-Delivery Checklist to design output template
- **`sk:accessibility`** — added iOS Dynamic Type audit section; added escape routes and keyboard shortcut preservation rules to keyboard navigation checklist

## [3.10.1] — 2026-03-24 — Security & Quality Fixes

### Fixed
- **Command injection** — replaced `shell=True` with `shlex.split()` in `sk:debug` step_runner.py subprocess calls
- **Path traversal** — added symlink check before packaging in `sk:skill-creator` package_skill.py
- **TOCTOU race** — atomic write via tempfile+rename in `sk:setup-claude` apply_setup_claude.py
- **Silent error handling** — replaced bare `except Exception` with specific types (`OSError`, `UnicodeDecodeError`, `json.JSONDecodeError`) across 5 files; added context to error messages
- **Naming mismatch** — replaced all "writing-plans" references with `/sk:write-plan` in `sk:brainstorming` SKILL.md
- **Dead code** — removed unused `_save_progress()` method, `sys` import, and `Tuple` import
- **Python compatibility** — added `from __future__ import annotations` to 6 files using Python 3.10+ union syntax

### Changed
- **Model routing** — upgraded `full-sail` and `quality` profiles from `sonnet` to `opus (inherit)` in `sk:lint` and `sk:test`

## [3.10.0] — 2026-03-23 — Workflow Acceleration

### Added
- **Auto-skip intelligence** — optional steps (design, accessibility, migration, performance) automatically skipped when detection criteria aren't met. Works in both manual and autopilot modes. No confirmation prompt — just a log line.
- **`/sk:autopilot`** — hands-free workflow mode. Runs all 21 steps with auto-skip, auto-advance, and auto-commit. Same quality gates as manual. Stops only for direction approval (1x) and PR push (1x).
- **`/sk:team`** — parallel domain agents for full-stack tasks. Spawns Backend Agent, Frontend Agent, and QA Agent in isolated worktrees. Requires API contract in plan.
- **`/sk:start`** — smart entry point that classifies tasks (feature/bug/hotfix/small change), detects scope (full-stack/frontend/backend), and recommends optimal flow + mode + agents.
- 3 new agent templates: `backend-dev.md`, `frontend-dev.md`, `qa-engineer.md`
- Model routing entries for start (haiku), autopilot (profile-based), and team (profile-based)
- `/sk:setup-optimizer` now detects and upgrades existing projects with auto-skip rules and new commands

## [3.9.0] — 2026-03-23

### Added
- **Cross-platform change tracking** — `tasks/cross-platform.md` logs changes that need replication in a companion codebase (web <-> mobile). Integrated into `/sk:setup-claude` bootstrap, `/sk:setup-optimizer` diagnosis, CLAUDE.md template, and Project Memory reads.

## [3.8.0] — 2026-03-23

### Added
- **Lifecycle hooks** — 6 Claude Code hooks deployed via `/sk:setup-claude`: session-start (auto-context), pre-compact (state preservation), validate-commit (conventional commit + debug statement checks), validate-push (protected branch warnings), log-agent (subagent audit trail), session-stop (session logging)
- **Path-scoped rules** — `.claude/rules/` directory with stack-specific rules: tests.md (always), api.md, frontend.md, laravel.md, react.md (conditional on detection)
- **Statusline** — persistent CLI status showing context %, model, workflow step, branch, and task name
- **Gate agents** — 5 agent definitions for parallel gate execution: linter (haiku), test-runner, security-auditor, perf-auditor, e2e-tester (sonnet)
- `/sk:scope-check` — compare implementation against plan, detect scope creep with 4-tier classification
- `/sk:retro` — post-ship retrospective: velocity, blockers, gate performance, action items
- `/sk:reverse-doc` — generate architecture/design docs from existing code with clarifying questions
- `/sk:gates` — run all quality gates in optimized parallel batches (single command replaces 6)
- `/sk:fast-track` — abbreviated workflow for small changes: skip planning, keep all quality gates
- **Cached stack detection** — `apply_setup_claude.py` caches detection results in `.shipkit/config.json` with 7-day TTL and `--force-detect` override
- `settings.json.template` — Claude Code settings with hooks, statusline, and permission allow/deny lists

## [3.7.0] — 2026-03-20

### Changed
- Gate loops now auto-fix + auto-commit internally — no separate commit step after each gate
- Workflow reduced from 27 → 21 steps (removed conditional commit steps 13, 15, 17, 19, 21, 23)
- Pre-existing issues found during gates are logged to `tasks/tech-debt.md` instead of fixed inline or silently skipped
- `sk:schema-migrate` auto-detects migration changes and skips automatically if none found

### Added
- `tasks/tech-debt.md` — append-only log of pre-existing issues found during gates
- `sk:context` now surfaces unresolved tech debt count in session brief
- `sk:write-plan` checks `tasks/tech-debt.md` and asks if items should be included in the current task
- `sk:update-task` marks tech-debt entries as `Resolved:` when related tasks complete

## [3.6.0] - 2026-03-20

### Added
- `sk:context` — Session initializer that loads all project context files (`tasks/todo.md`, `tasks/workflow-status.md`, `tasks/progress.md`, `tasks/findings.md`, `tasks/lessons.md`, `docs/decisions.md`, `docs/vision.md`) and outputs a formatted SESSION BRIEF. Run at the start of every session for instant orientation.

### Changed
- `sk:mvp` — New Step 9 auto-generates `docs/vision.md`, `docs/prd.md`, and `docs/tech-design.md` from the idea gathered in Steps 1-2. Persists product context for follow-up sessions.
- `sk:brainstorming` — Now appends an Architecture Decision Record (ADR) entry to `docs/decisions.md` after each brainstorm. Cumulative, append-only log of design decisions across features.

## [3.5.0] - 2026-03-19

### Added
- `sk:dashboard` — Read-only workflow Kanban board served by a zero-dependency Node.js server. Shows live workflow status across all git worktrees: phase timeline, step Kanban (Done/Next/Skipped/Not Yet), progress bar, and a **TASKS panel** displaying individual todo checklist items grouped by milestone. Items show current progress state (✓ done, → current, ○ pending). Auto-polls every 3 seconds. Start with `node skills/sk:dashboard/server.js` → `http://localhost:3333`.

## [3.4.0] - 2026-03-19

### Changed
- `sk:review` — Step 2 rewritten with **blast-radius analysis**: extracts changed symbols from git hunk headers (`@@`), classifies them as modified/removed vs. new, finds dependent files via import-chain narrowing with `rg`, and reads only the minimal context set (changed files in full + caller call sites + tests). Replaces the old "read every changed file" approach with focused, dependency-aware context collection.
  - New `[Blast Radius]` review dimension for cross-file findings (broken callers, removed exports, stale tests)
  - Steps 3 (Correctness), 4 (Security), 6 (Reliability), 7 (Design) now include mandatory blast-radius cross-checks against dependent files
  - Security checklist scoped to diff + blast-radius files only; pre-existing issues no longer flagged unless they interact with changed code
  - Noise guard: symbols with >100 matches flagged as too generic; symbols <3 chars filtered out
  - Report format updated with blast-radius scope summary and `[Blast Radius]` tag

## [3.3.0] - 2026-03-18

### Added
- `sk:mvp` — MVP Validation App Generator: generates a complete, polished MVP from a single idea prompt. Outputs a landing page with waitlist email collection + a working app with fake data. Supports 4 preset stacks (Next.js, Nuxt, Laravel, React+Vite), optional Pencil MCP visual design phase, and Playwright MCP visual validation after code generation. All code is generated locally — no deployments, no real databases, no third-party API integrations.

### Changed
- `sk:e2e` — now prefers Playwright CLI when `playwright.config.ts` / `playwright.config.js` is detected; falls back to `agent-browser` only when no config exists. Adds a Playwright setup reference (`headless: true`, `channel: undefined`) to avoid system Chrome conflicts. Includes a minimal `playwright.config.ts` template and `e2e/helpers/` auth helper pattern.

## [3.2.0] - 2026-03-16

### Added
- `sk:seo-audit` — new standalone SEO audit skill: dual-mode (source template scan + optional dev server probe), ask-before-fix mechanical fixes, checklist output to `tasks/seo-findings.md`
  - Phase 1: technical SEO (robots.txt, sitemap, canonical, noindex, lang), on-page SEO (title, description, h1, alt, link text, image filenames), content signals (OG tags, Twitter Card, JSON-LD)
  - Phase 2 (optional): dev server probe via parallel `curl -s -I` HEAD requests with Content-Type: text/html filter to avoid false positives from non-web services
  - Phase 3: ask-before-fix — shows grouped list of auto-fixable issues, applies only on `y`, continues on individual fix failure
  - Checklist output: `- [ ]` (open) / `- [x]` (auto-fixed), append-only with date headers
  - Content Strategy section for advisory-only items (JSON-LD, og:image, Search Console)
  - Fix & Retest Protocol: template/config fixes bypass; logic fixes require test update

### Changed
- Checklist format rolled out to all audit skills for consistency: `sk:perf`, `sk:accessibility`, `sk:security-check` reports now use `- [ ]` / `- [x]` checkbox format with `Open | Resolved this run` summary columns
- `install.sh`: added idempotency guard for `agent-browser` — skips reinstall if already present

## [3.1.0] - 2026-03-16

### Added
- `sk:e2e` — new hard gate E2E skill using agent-browser for behavioral verification after Review
- Fix & Retest Protocol — applies to all code-producing gates (Lint, Test, Security, Performance, Review, E2E): logic changes require updating unit tests before committing the fix
- Sync Features step (step 26) — runs `/sk:features` after Finalize to keep feature specs in sync with shipped code
- Requirement Change Flow section — documents `/sk:change` for mid-workflow requirement changes
- Dependency audit in `/sk:lint` — runs `composer audit` / `npm audit` / `pip-audit` alongside code linters
- agent-browser mandatory install in `install.sh` (~100MB Chrome download on first run)

### Changed
- Workflow expanded from 24 → 27 steps (new steps: 22 E2E Tests, 23 conditional commit, 26 Sync Features)
- Hard gates updated: 4 → 5 (added step 22 E2E Tests)
- Step 12 renamed: "Lint" → "Lint + Dep Audit"
- Step 20 renamed: "Review" → "Review + Simplify" (sk:review now runs simplify pre-pass automatically)
- All command references standardized to `/sk:` prefix across CLAUDE.md, templates, README, and DOCUMENTATION.md
- `/sk:review` now runs built-in `simplify` as a pre-pass before the full multi-dimensional review

## [3.0.7] - 2026-03-16

### Fixed

- **Command palette duplicates**: Removed `commands/sk/release.md` and `commands/sk/features.md` — both duplicated their SKILL.md counterparts, causing `/sk:release` and `/sk:features` to appear multiple times in the palette
- Removed corresponding `release.md.template` and `features.md.template` from `sk:setup-claude` templates to prevent re-generating the conflict

### Added

- **`/sk:frontend-design --pencil`**: New `--pencil` flag to jump directly to the Pencil visual mockup phase without going through the design summary prompt
- Pencil prompt at end of design summary is now a hard-stop (`MUST stop and ask`) so it can no longer be silently skipped

### Changed

- Updated Pencil prompt to clearly state prerequisites: Pencil app must be open and Pencil MCP must be connected
- Updated `README.md`, `CLAUDE.md`, `help.md`, and `sk:setup-claude` CLAUDE.md template to document the `--pencil` flag and clarify it is opt-in

## [3.0.6] - 2026-03-16

### Fixed

- **`sk:test`**: Fix Vitest config import path (`vitest/sk:config` → `vitest/config`) — generated `vitest.config.ts` would fail to compile
- **`sk:security-check`**: Replace hardcoded `Unknown` stack placeholders with dynamic stack detection instructions — stack-specific checks were being skipped entirely
- **`sk:finish-feature`**: Replace hardcoded `Unknown` framework references in verification checklist with stack-detection instructions

### Added

#### New Skills and Commands (P1–P4 workflow enhancements)

**`/api-design` skill (P2)**
- Design REST/GraphQL API contracts before implementation — mirrors `/frontend-design` but for APIs
- Covers endpoint design, request/response shapes, auth flows, error codes, rate limiting, versioning
- Outputs a complete API specification; implementation happens in `/execute-plan`
- Added to workflow Step 4 alongside `/frontend-design`

**`/accessibility` skill (P3)**
- WCAG 2.1 AA audit runs after `/frontend-design` or on existing frontend code
- Checks color contrast, keyboard navigation, ARIA semantics, forms, images, motion, content structure
- Writes findings to `tasks/accessibility-findings.md` (append-only, never overwritten)
- Added as new optional workflow Step 5; skip if backend-only

**`/perf` skill (P3)**
- Performance audit runs before `/review` — auto-detects stack (React, Laravel, Node, Go, Python)
- Frontend: bundle size, render performance, Core Web Vitals (LCP, CLS, INP)
- Backend: N+1 queries, missing indexes, unbounded queries, missing caching
- Writes findings to `tasks/perf-findings.md` (append-only)
- Added as new optional gate Step 18; loops until critical/high findings = 0

**`/hotfix` command (P2)**
- Emergency fix workflow — skips brainstorm, design, and write-tests phases
- 15-step flow: debug → branch → fix → lint → test → security → review → finish
- All 4 quality gates still enforced; cannot be skipped even in emergencies
- After merging: prompts to add regression test and lessons.md entry

**Workflow expanded from 21 → 24 steps**
- Step 5: Accessibility (new optional step after Design)
- Step 18: Performance (new optional gate before Review)
- All existing step numbers shifted accordingly
- Optional steps: 4, 5, 7, 18, 24 — Hard gates: 12, 14, 16, 20

#### Pencil MCP Integration (`/frontend-design`)
- After the text design summary, skill now prompts: "Would you like me to create a Pencil visual mockup? (y/n)"
- If yes: creates a `.pen` file in `docs/design/` using Pencil MCP tools
- Loads design guidelines (`get_guidelines`) and a matching style guide (`get_style_guide`) based on the chosen aesthetic
- Sets the color palette as Pencil variables via `set_variables`
- Builds frames and components with `batch_design`, one screen per batch
- Validates output visually with `get_screenshot` and iterates if needed
- Supports updating existing `.pen` files when iterating on a design
- Pencil MCP config updated: uses Pencil app's own MCP binary (`/Applications/Pencil.app/...`) with `--app desktop` identifier

#### Workflow Tracker (`tasks/workflow-status.md`)
- New persistent tracker file tracks progress through the 14-step development workflow
- Status dashboard printed after every slash command (done/partial/skipped/not yet)
- `>> next <<` indicator shows which step to run next
- Zero-tolerance enforcement loops for `/security-check` (0 issues, all severities) and `/review` (0 issues, including nitpicks)
- Attempt counting for looped steps (e.g., "clean on attempt 3")
- Optional steps (frontend-design, debug, release) require explicit skip confirmation
- Conditional commits (steps 7, 10, 12) auto-skip with reason when no changes exist
- Tracker resets on new feature/bug via `/brainstorm` or manual request
- Created automatically by `/setup-claude` and `/re-setup`

#### Mobile Store Readiness Audit (`/release --android`, `/release --ios`)
- New `--android` flag: runs full Play Store readiness audit after git release
- New `--ios` flag: runs full App Store readiness audit after git release
- Flags can be combined: `/release --android --ios` for both stores
- Auto-detects mobile framework (Expo, React Native, Flutter, native, Capacitor, MAUI)
- Detects first-time vs update submission based on project config
- Per-item PASS/FAIL/WARN/MANUAL CHECK grading across all checklist sections
- Proposes config fixes with user approval before applying
- Framework-specific build and submit commands (EAS, Gradle, xcodebuild)
- New reference files:
  - `release/references/android-checklist.md` — 14-section Play Store checklist
  - `release/references/ios-checklist.md` — 14-section App Store checklist

### Fixed

#### Command Implementations & Quality Gates
- **`/sk:help`** — Improved output with clean "Meta" section at top (displays 3 key commands: `/sk:help`, `/sk:status`, `/sk:skill-creator`)
- **`/sk:help`** — Removed duplicate `/sk:release` entry from all-commands list
- **`/sk:config`** — Added full executable implementation (Python) for viewing and managing `.shipkit/config.json`
  - Displays current config in formatted table with descriptions
  - Shows model assignments for current profile
  - Integrates with `/sk:set-profile` for profile switching
- **`/sk:set-profile`** — Added full executable implementation (Python) for switching model routing profiles
  - Accepts profile argument or displays options interactively
  - Validates profile names (full-sail, quality, balanced, budget)
  - Updates config file and displays new model assignments
  - Creates `.shipkit/` directory and adds to `.gitignore` automatically
- **`/sk:finish-feature`** — Fixed missing YAML frontmatter (was preventing skill registration)
  - All 18 ShipKit commands now have valid frontmatter and descriptions
  - Audit script validates all commands pass validation checks

---

## [2.1.0] - 2026-03-07

### Added

#### Security Audit Skill (`/security-check`)
- New command template: audits changed files (or full project with `--all`) for security vulnerabilities
- OWASP Top 10 (2021) checklist with CWE references
- Stack-specific checks (React/Next.js, Express/Node.js, Python, Go, PHP)
- Production readiness checks (error handling, input validation, secrets management)
- Writes structured findings to `tasks/security-findings.md` (severity-rated, never overwritten)

#### Security Context Threading
- `tasks/security-findings.md` — new persistent audit log read by 4 skills
- `/brainstorm` now reads security-findings.md for recurring security patterns
- `/finish-feature` enforces security gate (blocks on unresolved Critical/High findings)

#### 7-Dimension Code Review (`/review` upgrade)
- Expanded from 4 categories to 7 dimensions: Correctness, Security, Performance, Reliability, Design, Best Practices, Testing
- Performance analysis: N+1 queries, memory leaks, O(n²), unnecessary re-renders
- Reliability checks: error handling quality, graceful degradation, timeout handling
- Every finding tagged with dimension, file:line, and impact explanation
- Max findings increased from 15 to 20 with "What Looks Good" section

### Changed

#### Workflow Restructuring
- `/review` is now report-only — no longer creates PRs
- `/finish-feature` now creates PRs via `gh pr create` (with summary + security status)
- `/finish-feature` auto-commits changelog and arch log entries (no need to loop back to `/commit`)
- New workflow order: `/security-check` → `/review` → `/finish-feature` → `/release`
- Explicit review loop: `/debug` → `/commit` → `/review` until clean
- Review severity tiers: Critical (must fix), Warning (should fix), Nitpick (asks user)

### Fixed

- Heredoc syntax in finish-feature template (EOF delimiter spacing)
- Stale skill counts across documentation (6+ → 8+)
- Missing `/security-check` phase in README flow diagram
- Vague "loop until clean" replaced with explicit `/debug` → `/commit` → `/review` cycle

---

## [2.0.0] - 2026-03-03

### Added

#### Lessons + Findings Context Threading (Complete Feedback Loop)
- **brainstorming/SKILL.md** — Now reads `tasks/findings.md` and `tasks/lessons.md` before exploring; applies lessons as design constraints
- **frontend-design/SKILL.md** — Reads findings.md as design brief; reads lessons.md for constraints
- **finish-feature.md.template** — "Before You Start" block: scans diff against lessons.md Bug patterns
- **plan.md.template** — "Before You Start" block: applies lessons.md as constraints
- Updated 3 additional templates: brainstorm, execute-plan, write-plan with context threading

**Impact:** Every skill that makes decisions now reads lessons.md; every skill accepting handoff reads findings.md.

#### Intelligent Architectural Change Detection
- **New script:** `setup-claude/scripts/detect_arch_changes.py`
  - Analyzes git diff main..HEAD
  - Auto-detects: control flow, data flow, pattern, integration, subsystem changes
  - Generates markdown draft for arch logs (80% complete)
  - Options: `--dry-run`, `--show-analysis`, `--output FILE`

- **Integration in finish-feature step 4:**
  - Runs auto-detector on every branch
  - If changes detected: auto-generates arch log draft
  - User reviews/edits the [TODO] sections
  - User commits the final arch log
  - If no changes: gracefully skips to step 5

**Impact:** No more manual "is this an architectural change?" questions. Script analyzes code and tells you.

#### Comprehensive Documentation Updates
- **FEATURES.md** — Complete feature reference with examples and benefits
- **README.md** — Complete workflow flow diagram, updated tutorials, What's New section
- **CLAUDE.md** — Enhanced workflow table with context column
- **arch-changelog-guide.md** — Updated with auto-detection workflow
- **changelog-guide.md** — Clarified CHANGELOG.md vs arch logs

### Changed

- **.gitignore** — Removed brainstorming/ and frontend-design/ (custom skills)
- **Workflow table in CLAUDE.md** — Added context column (what files each skill reads/writes)
- **finish-feature template** — Enhanced step 4 with intelligent arch detection
- **Multiple command templates** — Added/updated "Before You Start" blocks for context threading

### Fixed

- **Context reset issue** — findings.md and lessons.md now persist across sessions
- **Repeated bugs** — Lessons.md prevents recurring mistakes across features
- **Arch documentation gaps** — Auto-detection catches manual oversights

---

## [1.0.0] - 2026-02-15

(Earlier releases not shown)
