# 2026-05-13 — Dual-target architecture (Claude Code + OpenAI Codex)

## Summary

ShipKit transitioned from a Claude-Code-only package to a **dual-target** system supporting Claude Code (primary) and OpenAI Codex (CLI + Cloud, secondary). The same `core/` content drives both targets via per-target adapters.

Version: `3.30.0` → `4.0.0-beta.1`.

## Motivation

Users adopting Codex CLI / Codex Cloud asked for ShipKit's enforced workflow there. Maintaining two forked packages was untenable; we needed a shared-core architecture that emits target-specific files at install time.

## Architecture change

### Before (v3.x)

```
shipkit/
├── skills/sk:*/SKILL.md          # Claude Code skills
├── commands/sk/*.md              # Claude Code slash commands
└── bin/shipkit.js                # Copy these to ~/.claude/
```

`bin/shipkit.js` was a pure file-copy CLI. The package shipped Claude-Code-shaped files directly.

### After (v4.0)

```
shipkit/
├── core/
│   ├── skills/sk:*/SKILL.md      # provider-agnostic source
│   ├── commands/sk/*.md          # provider-agnostic source
│   └── lib/env-detect.sh         # runtime target/env detection
├── adapters/
│   ├── claude/emit.js            # passthrough (today's format is canonical)
│   └── codex/emit.js             # parse → strip Claude fields → emit Codex SKILL.md
└── bin/shipkit.js                # --target=claude|codex|both dispatches to adapter
```

The Claude `SKILL.md` format remains the canonical source. The Codex adapter transforms at emit time:
- Strips Claude-only frontmatter (`model`, `allowed-tools`)
- Renames folders/skills `sk:foo` → `sk-foo` (filesystem safety)
- Applies 19 path-substitution rules (`.claude/agents/` → `.codex/agents/`, etc.)
- Generates `AGENTS.md` from `CLAUDE.md` with a Codex-specific header
- Emits `.codex/config.toml`, `.codex/hooks.json` + scripts, `.codex/agents/<name>.{toml,md}` for 18 sub-agents, `.codex/lib/env-detect.sh`

### Trade-offs considered and rejected

- **Build-step adapters emitting to `dist/`** — rejected. Adds complexity; the runtime emit is fast enough and avoids `prepack` brittleness.
- **Per-target source forks** — rejected. Two divergent copies guarantee drift; the transform-at-emit pattern keeps one source.
- **Codex plugin marketplace as primary distribution** — deferred. No marketplace access confirmed; npm only for v4.0.

## What works on each target

| Capability | Claude Code | Codex CLI | Codex Cloud |
|---|---|---|---|
| Skills (auto-trigger) | ✅ | ✅ | ✅ |
| Slash commands | ✅ `/sk:foo` | ⚠️ via description match | ⚠️ via description match |
| Hooks | ✅ | ✅ (`.codex/hooks.json`) | ❌ no hooks in Cloud |
| Sub-agents | ✅ parallel | ⚠️ sequential | ⚠️ sequential, no nested |
| MCP servers | ✅ | ✅ (`.codex/config.toml`) | ⚠️ pre-wired only |
| Pencil MCP | ✅ | ⚠️ if user-installed | ❌ unavailable |
| Worktree isolation | ✅ Agent tool | ⚠️ scripted | ⚠️ container-equivalent |
| Background tasks | ✅ `run_in_background` | ⚠️ `codex exec` shell-out | ❌ |

Detailed per-skill comparison in `tasks/codex-quality-deltas.md`.

## Migration notes for existing Claude Code users

- **No behavior change.** `shipkit` (no args) still installs into `~/.claude/` with byte-identical output to v3.30.0 (verified by `diff -r` in sandbox).
- **Repo layout changed.** If you were referencing `shipkit/skills/sk:foo/SKILL.md` from your own scripts, update to `shipkit/core/skills/sk:foo/SKILL.md`. Users of the published npm package are unaffected.

## Six-phase rollout

| Phase | Commit | Deliverable |
|---|---|---|
| 1 | `af85cde` | Core + adapter scaffolding; Claude byte-identical |
| 2 | `626710f` | Real Codex adapter MVP |
| 3 | `075ae91` | Body-transform pass (121 transforms) + audit doc |
| 4 | `b6b83e2` | 18 sub-agents translated |
| 5 | (this commit) | `env-detect.sh` + AGENTS.md cloud expansion |
| 6 | (this commit) | Distribution: README, CHANGELOG, version bump |

Phase 7 (cross-target validation) is user-driven and tracked in `tasks/codex-quality-deltas.md`.

## Tests

`tests/verify-workflow.sh`: 361/362 pass across all 6 phases (the 1 failure is pre-existing and unrelated — references a deleted `commands/sk/brainstorm.md`).

## Files of note

- `tasks/codex-migration-plan.md` — full plan
- `tasks/codex-migration-inventory.md` — Claude-coupling inventory (82+ touchpoints)
- `tasks/codex-migration-research.md` — Codex platform capability map (17 sources)
- `tasks/codex-quality-deltas.md` — per-skill dual-target delta inventory
- `adapters/codex/README.md` — adapter docs (transform table, NOT-transformed rationale)
