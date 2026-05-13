# Codex Quality Deltas

Known differences in ShipKit behavior between **Claude Code** (primary target) and **OpenAI Codex** (secondary target). Tracked separately from `tasks/tech-debt.md` so the dual-target quality bar stays visible.

Updated: 2026-05-13 (Phase 4 of `tasks/codex-migration-plan.md`)

## Legend

| Severity | Meaning |
|---|---|
| 🔴 **Behavior** | Skill produces a meaningfully different outcome on Codex vs Claude |
| 🟡 **Performance** | Same outcome, but slower or more expensive on Codex |
| 🟢 **Cosmetic** | Output differs in non-substantive ways (logging, message phrasing) |

## Phase 4 — Sub-agent parallelization

| Skill | Severity | Delta | Mitigation |
|---|---|---|---|
| `/sk:gates` | 🟡 Performance | Claude runs the 7 quality gates as parallel sub-agents in 3 batches (≈3-5x faster). Codex sub-agents are explicit + token-expensive; defaults to sequential execution. | Phase 4 ships `.codex/agents/*.toml` so a Codex user can opt into parallel via `codex exec --agent <name>` per gate, but the orchestration is manual. Phase 5 will add sequential rewrite of gate body that reads "decreased throughput on Codex." |
| `/sk:team` | 🟡 Performance | Claude spawns 3 parallel domain agents (backend-dev, frontend-dev, qa-engineer) in worktrees. Codex requires `git worktree add` + sequential `codex exec --cd <path>` per agent. | `.codex/agents/{backend-dev,frontend-dev,qa-engineer}.toml` emitted; orchestration scripting deferred to Phase 5. Expect 2-3x wall-clock slowdown. |
| `/sk:deep-dive` | 🟡 Performance | Parallel trace agents (3 lanes) on Claude; sequential trace on Codex. Same correctness, longer wall-time. | Same as `/sk:team` — agents ship, orchestration deferred. |
| `/sk:review` | 🟡 Performance | Claude runs security + perf + test-coverage as 3 parallel review agents. Codex runs sequentially. | `.codex/agents/{code-reviewer,security-auditor,perf-auditor}.toml` ship; sequential dispatch built into skill body Phase 5. |

## Phase 5 — Cloud constraints (Codex Web only)

These affect Codex Cloud (ChatGPT-hosted) installations only. Codex CLI users get full functionality.

| Skill / Feature | Severity | Delta | Mitigation |
|---|---|---|---|
| All hooks (`.codex/hooks.json`) | 🔴 Behavior | Codex Cloud doesn't honor hooks. SessionStart context loading, pre-commit validation, post-edit formatting, safety-guard etc. are no-ops. | Phase 5 env-detect; skills that depend on hook side-effects print a degraded-mode notice. |
| `/sk:safety-guard` | 🔴 Behavior | Relies on PreToolUse hook to block dangerous shell ops. Cloud has no hooks → guard is decorative only. | Phase 5: skill detects cloud, switches to "advisory" mode (prints warnings only). |
| User-global MCP servers | 🔴 Behavior | `~/.codex/config.toml` doesn't apply in Cloud. Only environment-provided MCP servers work. | Document; recommend using cloud-managed MCP for cross-task continuity. |
| Sub-agent invocation | 🔴 Behavior | Cloud tasks have a `max_threads` cap; `codex exec` from within a task may not spawn additional tasks. | Phase 5: skills that hard-require sub-agents print "manual fallback required on Cloud" notice. |

## Pencil MCP (visual design)

| Skill | Severity | Delta | Mitigation |
|---|---|---|---|
| `/sk:frontend-design --pencil` | 🔴 Behavior | Pencil MCP is Claude-Code-native (via `claude_ai_Pencil` MCP). On Codex CLI it works if user installs the MCP separately; on Codex Cloud it does not. | Phase 5: env-detect; `--pencil` flag becomes a no-op + warning on Cloud. Pure-CSS mockup fallback in skill body. |
| `/sk:mvp` (Pencil step) | 🔴 Behavior | Optional Pencil mockup for MVP landing page. | Same as above. |

## context-mode plugin

| Skill / Feature | Severity | Delta | Mitigation |
|---|---|---|---|
| Skills using `mcp__plugin_context-mode_context-mode__ctx_*` tools | 🔴 Behavior | Context-mode is a Claude-Code-specific harness plugin (SQLite FTS5 output caching). No Codex equivalent. | Phase 5: skill bodies that explicitly reference `ctx_batch_execute` etc. gain a "[Codex: use shell directly]" annotation. Sequential reads work fine on Codex, just without the dedup cache. |

## Setup skill

| Skill | Severity | Delta | Mitigation |
|---|---|---|---|
| `/sk:setup-claude` | 🔴 Behavior | Configures `~/.claude/` paths, `.claude/settings.json`, `.claude/statusline.sh`. Meaningless on Codex. | Phase 5: emit a `sk-setup-codex` companion skill that configures `.codex/config.toml`, MCP, profiles. Codex users skip `sk-setup-claude`. |

## Tool naming

| Tool | Claude Code | Codex | Compatibility status |
|---|---|---|---|
| File read | `Read` | `apply_patch` (atomic; no separate read) | ✅ Auto-resolved by Codex aliases |
| File edit | `Edit` | `apply_patch` | ✅ Auto-resolved |
| File write | `Write` | `apply_patch` | ✅ Auto-resolved |
| Shell | `Bash` | `Bash` (alias for `shell`/`local_shell`) | ✅ Native |
| Search code | `Grep` | shell `rg` | 🟢 Cosmetic — agents adapt |
| Find files | `Glob` | shell `find` / `fd` | 🟢 Cosmetic — agents adapt |
| Web fetch | `WebFetch` | `web_search` (no URL-fetch primitive) | 🟡 Codex can browse via search; URL-specific fetch loses precision |
| Web search | `WebSearch` | `web_search` | ✅ Native |
| Plan mode | `EnterPlanMode` | `/plan` slash + `read-only` sandbox | 🟢 Cosmetic |
| Background tasks | `run_in_background:true` | `codex exec` from wrapper script | 🟡 Codex has no in-process equivalent — must shell out |

## Open quality bets (track here as work progresses)

- [ ] **AGENTS.md token cost vs CLAUDE.md** — measure how often Codex re-reads vs Claude. If Codex reads it every turn, the 16.8 KiB cost compounds.
- [ ] **Skill auto-trigger fidelity** — Claude triggers skills via description match in agent context. Codex uses progressive disclosure (~2% ctx cap). Need empirical comparison on 5+ representative tasks.
- [ ] **Sequential gate wall-clock** — once `/sk:gates` runs end-to-end on Codex CLI, capture the time delta vs Claude in this doc.
- [ ] **Cloud E2E** — full `/sk:autopilot` flow on Codex Cloud is unvalidated. Phase 7.
