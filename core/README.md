# core/

Provider-agnostic ShipKit content. Adapters in `adapters/<target>/` consume this directory and emit per-provider files.

| Directory | Purpose |
|---|---|
| `core/skills/` | Skill definitions (currently in Claude `SKILL.md` format; adapter transforms for other targets) |
| `core/commands/sk/` | Lightweight slash commands without a full skill backing |

> **Note**: Today's content uses the Claude Code `SKILL.md` format as the canonical source. The Codex adapter (Phase 2) parses this format, strips Claude-specific frontmatter fields, and re-emits in Codex's required shape. Future migration phases may split the body and frontmatter further for cleaner multi-target support.
