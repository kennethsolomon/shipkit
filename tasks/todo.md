# tasks/todo.md — Codex Target (v4.0.0)

Branch: `feat/codex-target`
Plan: `tasks/codex-migration-plan.md`
Inventory: `tasks/codex-migration-inventory.md`
Research: `tasks/codex-migration-research.md`

## Phase 1 — Extract core + claude adapter (no behavior change)

Goal: refactor in-place. Claude Code emit must be byte-identical to v3.30.0.

> Approach revised from initial plan: since current install is pure file-copy and current `SKILL.md` format already matches Claude's expectations, Architecture B (runtime emit via adapter modules) replaces the planned build-step extraction. Frontmatter/template extraction deferred to Phase 2 where it's actually needed for Codex transformation.

- [x] **1.1** Scaffold `core/` and `adapters/claude/` and `adapters/codex/` directories with READMEs
- [x] **1.2** ~~Define `core/tool-map.yaml`~~ — DEFERRED to Phase 2 (only needed when Codex adapter does real transformation)
- [x] **1.3** `git mv skills core/skills` + `git mv commands core/commands` (preserves history)
- [x] **1.4** Build `adapters/claude/emit.js` — passthrough copy from `core/` to `~/.claude/`
- [x] **1.5** Build `adapters/codex/emit.js` — stub that errors with Phase 2 pointer
- [x] **1.6** Rewrite `bin/shipkit.js` to dispatch to adapters via `--target=claude|codex|both`
- [x] **1.7** Update `install.sh` paths to `core/skills/`, `core/commands/sk/`
- [x] **1.8** Update `tests/verify-workflow.sh` paths (168 references)
- [x] **1.9** Update `.gitignore` paths
- [x] **1.10** Bump `package.json` to `4.0.0-alpha.1`; update `files` whitelist (`bin`, `core`, `adapters`)
- [x] **1.11** Run `tests/verify-workflow.sh` — 361 pass / 1 fail (failure is pre-existing on main, unrelated)
- [x] **1.12** Sandbox-test byte-identical Claude install — `diff -r core/ ~/.claude/` reports zero differences
- [x] **1.13** Update `CLAUDE.md` to describe new repo layout
- [ ] **1.14** Commit Phase 1 (awaiting user OK)
- [ ] **1.15** Push + PR Phase 1 (awaiting user OK)

## Phase 2 — Codex pilot (3 commands E2E)

(populated after Phase 1 lands)

## Phase 3 — Full Codex port

(populated after Phase 2 validates)

## Phase 4 — Hard translations (parallel agents, worktrees)

(populated after Phase 3)

## Phase 5 — Cloud degradation

(populated after Phase 4)

## Phase 6 — Distribution + Phase 7 — Validation

(populated after Phase 5)

## Phase 2 — Codex pilot (3 commands E2E)

(populated after Phase 1 lands)

## Phase 3 — Full Codex port

(populated after Phase 2 validates)

## Phase 4 — Hard translations (parallel agents, worktrees)

(populated after Phase 3)

## Phase 5 — Cloud degradation

(populated after Phase 4)

## Phase 6 — Distribution + Phase 7 — Validation

(populated after Phase 5)
