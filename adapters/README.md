# adapters/

Per-target emit logic. Each adapter takes the provider-agnostic content in `core/` and writes provider-specific files to the install destination.

| Adapter | Status | Destination | Format |
|---|---|---|---|
| `claude/` | ✅ shipped | `~/.claude/skills/` + `~/.claude/commands/sk/` | `SKILL.md` w/ Claude frontmatter (`name`, `description`, `model`) |
| `codex/` | 🚧 Phase 2 | `<cwd>/.agents/skills/` + `<cwd>/.codex/` + `<cwd>/AGENTS.md` | Codex-spec `SKILL.md` (`name`, `description`) + `config.toml` + `hooks.json` |

Each adapter exports:

```js
module.exports = {
  emit({ coreDir, destDir }) { /* returns stats */ },
  uninstall({ destDir })     { /* returns stats */ },
};
```

`bin/shipkit.js` selects the adapter via `--target=claude|codex|both` (default: `claude`).

See `tasks/codex-migration-plan.md` for the full migration plan and `tasks/codex-migration-research.md` for the Codex platform capability map.
