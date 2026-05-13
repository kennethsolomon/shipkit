# adapters/codex/

Emits a Codex-native ShipKit installation from `core/`. Target: OpenAI Codex CLI + Codex Cloud.

## Output layout (per `destDir`, which is the user's project root)

| Path | Purpose |
|---|---|
| `AGENTS.md` | Codex instruction file. Generated from ShipKit's `CLAUDE.md` with a Codex-specific header (tool naming, cloud constraints, invocation guide). Hard-capped at 32 KiB per file by Codex. |
| `.agents/skills/sk-<name>/SKILL.md` | Codex skill. Auto-triggered by description; loaded progressively. Frontmatter: `name`, `description` only. |
| `.agents/skills/sk-<name>/...` | Asset files (Python scripts, HTML, references/, etc.) copied verbatim alongside `SKILL.md`. |
| `.codex/config.toml` | MCP servers, named profiles, sub-agent stubs. |
| `.codex/hooks.json` | CLI-only lifecycle hooks (`SessionStart`, `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`). |
| `.codex/hooks/*.sh` | ShipKit hook scripts copied so `hooks.json` `command` paths resolve. |

## Naming convention

`sk:foo` (Claude folder/skill name) becomes **`sk-foo`** on Codex. The colon is unsafe in directory names on Windows + many CI runners; the dash is universally safe. Both the folder name and the frontmatter `name:` follow this convention.

Slash-command invocation differs across targets:

| Target | Invocation |
|---|---|
| Claude Code | `/sk:foo` |
| Codex CLI / Cloud | Auto-trigger from description, OR ask "use the sk-foo skill" |

## Body transforms (applied at emit time)

Skill bodies in `core/` are the canonical Claude-Code format. The Codex adapter rewrites a small, safe set of references so the same body works on both targets without source-level forks:

| Pattern | Replacement |
|---|---|
| `~/.claude/skills/sk:` | `~/.agents/skills/sk-` |
| `~/.claude/skills/` | `~/.agents/skills/` |
| `~/.claude/agents/` | `~/.codex/agents/` |
| `~/.claude/settings.json` | `~/.codex/config.toml` |
| `~/.claude/sessions/` | `~/.codex/sessions/` |
| `~/.claude/` (rest) | `~/.codex/` |
| `.claude/agents/` | `.codex/agents/` |
| `.claude/hooks/` | `.codex/hooks/` |
| `.claude/skills/sk:` | `.agents/skills/sk-` |
| `.claude/skills/` | `.agents/skills/` |
| `.claude/commands/sk:` | `.agents/skills/sk-` |
| `.claude/commands/sk/` | `.agents/skills/` |
| `.claude/commands/` | `.agents/skills/` |
| `.claude/docs/` | `docs/` |
| `.claude/evals/` | `.codex/evals/` |
| `.claude/rules/` | `.codex/rules/` |
| `.claude/safety-guard` | `.codex/safety-guard` |
| `.claude/settings.json` | `.codex/config.toml` |
| `.claude/sessions/` | `~/.codex/sessions/` |
| `.claude/mcp.json` | `~/.codex/config.toml` |

### NOT transformed (deliberate)

- **Tool names** — `Read`/`Edit`/`Write`/`Grep`/`Glob`/`Bash`/`Agent` references in skill bodies are *actions*, not literal tool API calls. Codex agents read the same English text and use their own tool surface (`apply_patch`, shell `rg`, etc.). Blind tool-name replacement risks turning factual references nonsensical.
- **"Claude Code" / "CLAUDE.md" prose** — agents read `AGENTS.md`, which contains a header documenting the mapping. Preserving the original prose keeps factual references intact ("Claude Code's plan mode", etc.).
- **`/sk:foo` slash-command invocations** — Codex auto-triggers on description; agents figure out the correct skill name from context. No literal-typing equivalent on Codex.
- **`.claude/statusline.sh`** — Codex has no statusline equivalent. The 3 residual refs in `sk-setup-claude` are intentionally untouched (that skill is target-specific by design).

## Known Codex-incompatible skills

These skills exist in `core/skills/` but emit a degraded or marker-only Codex version. Future phases address each:

| Skill | Issue | Status |
|---|---|---|
| `sk-setup-claude` | Setup target is `.claude/`; entire purpose is Claude-only | Phase 5 — add `sk-setup-codex` companion + cloud gate |
| `sk-frontend-design` `--pencil` | Uses Pencil MCP (visual editor); MCP available in Codex CLI but not Cloud | Phase 5 — env-detect; degrade `--pencil` flag |
| `sk-mvp` Pencil usage | Same as above | Phase 5 |
| Anything using `ctx_batch_execute` / `ctx_*` | context-mode plugin is a Claude-Code-specific harness optimization | Phase 5 — degrade gracefully; document |
| `/sk:gates` parallel sub-agent batches | Codex sub-agents are explicit + token-expensive; parallel batches need redesign | Phase 4 — emit `.codex/agents/*.toml` + sequential rewrite |
| `/sk:team` parallel domain agents | Same as above | Phase 4 |

## Sub-agent translation (Phase 4)

Currently `.codex/config.toml` has commented `[agents.*]` placeholders. Phase 4 will:

1. Inventory every `Agent` tool / `subagent_type` call across `core/skills/`
2. Emit a `.codex/agents/<name>.toml` per ShipKit sub-agent (architect, code-reviewer, debugger, frontend-dev, backend-dev, etc.)
3. Rewrite parallel-batch skill bodies (`/sk:gates`, `/sk:team`, `/sk:deep-dive`) to use sequential `codex exec` invocations or in-process iteration, with documented perf delta.

## Testing

The repo's `tests/verify-workflow.sh` checks Claude-emit semantics. Codex-emit currently has no test suite — verify manually:

```bash
SB=$(mktemp -d) && cd "$SB"
node /path/to/shipkit/bin/shipkit.js --target=codex
# Inspect:
ls .agents/skills/ | head
cat AGENTS.md | head -30
cat .codex/config.toml
jq . .codex/hooks.json
```

For Codex CLI E2E validation, launch `codex --cd "$SB"` and confirm AGENTS.md is honored.
