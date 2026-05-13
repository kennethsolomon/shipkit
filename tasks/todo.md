# tasks/todo.md — Codex Target (v4.0.0)

Branch: `feat/codex-target`
Plan: `tasks/codex-migration-plan.md`
Inventory: `tasks/codex-migration-inventory.md`
Research: `tasks/codex-migration-research.md`

## Phase 1 — Extract core + claude adapter (no behavior change) — DONE

Committed as `af85cde`. Claude Code emit byte-identical to v3.30.0.

- [x] Scaffold `core/`, `adapters/claude/`, `adapters/codex/` directories
- [x] `git mv skills core/skills` + `git mv commands core/commands`
- [x] Claude adapter passthrough emit
- [x] Codex adapter stub
- [x] Rewrite `bin/shipkit.js` with `--target` flag
- [x] Update install.sh, verify-workflow.sh, .gitignore paths
- [x] Bump version to `4.0.0-alpha.1`
- [x] Update CLAUDE.md
- [x] Commit Phase 1

## Phase 2 — Codex adapter MVP — DONE

Real `adapters/codex/emit.js` producing AGENTS.md + `.agents/skills/` + `.codex/` from `core/`. Verified end-to-end via sandbox install.

- [x] Frontmatter parser + Codex name conversion
- [x] `emitSkill` — strips Claude-only fields, copies asset trees
- [x] `emitCommand` — promotes commands-without-skill to Codex skills
- [x] `emitAgentsMd` — wraps CLAUDE.md with Codex-specific header (tool naming, cloud constraints, invocation guide)
- [x] `emitConfigToml` — profiles, MCP stubs, agents stubs
- [x] `emitHooksJson` — 11 ShipKit hooks → 5 Codex events; copies .sh into `.codex/hooks/`
- [x] Wire `bin/shipkit.js`: pass `repoRoot`, format codex install report
- [x] Add `CLAUDE.md` to npm package `files` whitelist
- [x] Sandbox-tested: `--target=codex`, `--target=both`, codex uninstall
- [x] `tests/verify-workflow.sh` regression check (361/1 unchanged)
- [ ] Commit Phase 2 (next)

## Phase 3 — Skill body audit + transform pass — DONE

- [x] Audit Read/Edit/Write refs — minimal; agents handle as actions via apply_patch alias
- [x] Audit Grep/Glob refs — minimal; agents handle as actions
- [x] Audit Agent/sub-agent refs — 20+ files; deferred to Phase 4 as planned
- [x] Audit WebFetch/WebSearch refs — none found
- [x] Flag Pencil-dependent skills (sk-frontend-design --pencil, sk-mvp) — documented in adapters/codex/README.md, env-detect deferred to Phase 5
- [x] Flag context-mode-dependent skills — documented
- [x] Decided architecture: target-agnostic source + body-transform pass at emit time (not per-target overlays)
- [x] 19-rule `BODY_TRANSFORMS` table in `adapters/codex/emit.js` covers .claude/ → .codex/ + .agents/ path mappings
- [x] Spot-checked sk-safety-guard, sk-laravel-new, sk-setup-claude residuals
- [x] Written `adapters/codex/README.md` documenting transforms + NOT-transformed rationale + known-incompatible skills + Phase 4 plan
- [x] Verified test suite (361/1 unchanged)
- [ ] Commit Phase 3 (next)

## Phase 4 — Hard translations (parallel sub-agents, worktrees)

- [ ] **4.1** Inventory all `Agent` tool invocations in skill bodies (from `tasks/codex-migration-inventory.md`)
- [ ] **4.2** For each parallel-batch pattern (e.g., `/sk:gates` Batch 3), define a `.codex/agents/<name>.toml`
- [ ] **4.3** Emit `.codex/agents/` directory from adapter
- [ ] **4.4** Rewrite skill bodies that orchestrate parallel agents to use sequential invocations on Codex (document perf delta in `tasks/codex-quality-deltas.md`)
- [ ] **4.5** Replace `isolation: "worktree"` agent calls with `git worktree add` + `codex --cd <path>` shell helper
- [ ] **4.6** Sandbox test: invoke at least one ported sub-agent via Codex
- [ ] **4.7** Commit Phase 4

## Phase 5 — Cloud-mode environment detection

- [ ] **5.1** Write `core/lib/env-detect.sh` — detects Codex Cloud (no `~/.codex/`, no hooks, no MCP unless pre-wired)
- [ ] **5.2** Inject env-detect calls into skills that rely on CLI-only features (hooks, sub-agents, MCP)
- [ ] **5.3** Each gated skill prints a degraded-mode notice and continues with reduced functionality
- [ ] **5.4** Document the cloud quality delta in `tasks/codex-quality-deltas.md`
- [ ] **5.5** Manually verify in Codex Cloud: push branch, run a representative workflow
- [ ] **5.6** Commit Phase 5

## Phase 6 — Distribution

- [ ] **6.1** Update README.md with three-way install matrix (Claude / Codex CLI / Codex Cloud)
- [ ] **6.2** Add architectural change log entry in `.claude/docs/architectural_change_log/`
- [ ] **6.3** Update CHANGELOG.md with v4.0.0 entry
- [ ] **6.4** Test `npm pack` and inspect tarball contents
- [ ] **6.5** Cut `4.0.0-beta.1` (npm dist-tag `next`) for early adopters
- [ ] **6.6** Defer Codex plugin marketplace until access confirmed (per locked decision)
- [ ] **6.7** Commit Phase 6

## Phase 7 — Validation

- [ ] **7.1** Run `/sk:autopilot` equivalent on a sample feature in Claude Code
- [ ] **7.2** Run same flow in Codex CLI (`codex --cd`)
- [ ] **7.3** Run same flow in Codex Cloud (push, kick off task)
- [ ] **7.4** Compare outputs; capture deltas in `tasks/codex-quality-deltas.md`
- [ ] **7.5** Cut `4.0.0` final once parity is documented
- [ ] **7.6** Phase 7 retrospective in `tasks/retro-2026-XX-XX-codex-port.md`
