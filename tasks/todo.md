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

## Phase 4 — Sub-agent translation — DONE

- [x] Translated all 18 ShipKit sub-agent definitions (architect, backend-dev, code-reviewer, etc.)
- [x] Each agent emits both `.codex/agents/<name>.toml` (config) + `.codex/agents/<name>.md` (developer_instructions body, with path transforms applied)
- [x] Model mapping: Claude `haiku`/`sonnet`/`opus` → Codex `gpt-5-haiku`/`gpt-5` + reasoning_effort low/medium/high
- [x] Sandbox mode inference: `Edit`/`Write`/`NotebookEdit` in allowed-tools → `workspace-write`, otherwise → `read-only`. Bash alone doesn't force write-mode (code-reviewer + architect use it for git diff)
- [x] `.codex/config.toml` lists all 18 agents in comment block
- [x] Wrote `tasks/codex-quality-deltas.md` documenting:
  - Per-skill parallel-to-sequential perf deltas (`/sk:gates`, `/sk:team`, `/sk:deep-dive`, `/sk:review`)
  - Cloud-only constraints (Phase 5)
  - Pencil + context-mode incompatibilities
  - Tool naming compatibility matrix
  - Open quality bets to validate
- [x] Sandbox-tested: `shipkit --target=codex` emits 18 agents (36 files); spot-check confirms correct sandbox modes
- [x] Deferred to Phase 5: sequential rewrite of `/sk:gates` body (current skill body still describes parallel batches; agent will adapt or the AGENTS.md header explains the constraint)
- [ ] Commit Phase 4 (next)

## Phase 5 — Cloud-mode environment detection — DONE

- [x] `core/lib/env-detect.sh` — sets SHIPKIT_TARGET/ENV/HOOKS_OK/MCP_OK; priority: runtime env vars → local cwd → user-home
- [x] Emit env-detect.sh to `.codex/lib/` during codex install
- [x] AGENTS.md expanded with comprehensive cloud-constraints section + cloud-affected-skills table
- [x] Documentation in `tasks/codex-quality-deltas.md` (covers all 6 phases)
- [ ] **Deferred to Phase 7** — manual Codex Cloud E2E verification (requires user's Codex environment)

## Phase 6 — Distribution — DONE

- [x] README.md updated with three-way install matrix + targets badge + Quick Start for both Claude and Codex
- [x] CHANGELOG.md v4.0.0-beta.1 entry covering all 6 phases + deltas
- [x] `.claude/docs/architectural_change_log/2026-05-13-codex-dual-target.md` written (full architecture write-up)
- [x] `npm pack --dry-run` inspected: 246 files, 510 KB tarball, includes bin/, core/, adapters/, CLAUDE.md, README.md
- [x] `package.json` version bumped: 4.0.0-alpha.1 → 4.0.0-beta.1
- [x] CLAUDE.md version banner updated
- [x] Defer Codex plugin marketplace per locked decision
- [ ] Commit Phase 5+6 (next)

## Phase 7 — Validation

- [ ] **7.1** Run `/sk:autopilot` equivalent on a sample feature in Claude Code
- [ ] **7.2** Run same flow in Codex CLI (`codex --cd`)
- [ ] **7.3** Run same flow in Codex Cloud (push, kick off task)
- [ ] **7.4** Compare outputs; capture deltas in `tasks/codex-quality-deltas.md`
- [ ] **7.5** Cut `4.0.0` final once parity is documented
- [ ] **7.6** Phase 7 retrospective in `tasks/retro-2026-XX-XX-codex-port.md`
