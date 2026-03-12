# Findings — 2026-03-12 — Fix Plugin Setup & Script Paths

## Problem Statement

`install.sh` creates a symlink at `~/.claude/plugins/claude-skills`, but all script references in the codebase point to `$HOME/.agents/skills/...` — a legacy path that doesn't exist. This means `/setup-claude`, `/re-setup`, and `/finish-feature` cannot run their Python scripts. Additionally, the repo lacks a `.claude-plugin/plugin.json` manifest required for proper plugin structure.

## Scope

7 files reference the broken `$HOME/.agents/skills/` path:

| File | Reference |
|------|-----------|
| `skills/setup-claude/SKILL.md` | `apply_setup_claude.py` path (4 occurrences) |
| `skills/setup-claude/templates/commands/re-setup.md.template` | `apply_setup_claude.py` path (3 occurrences) |
| `skills/setup-claude/templates/commands/finish-feature.md.template` | `detect_arch_changes.py` path (2 occurrences) |
| `commands/re-setup.md` | `apply_setup_claude.py` path (3 occurrences) |
| `commands/finish-feature.md` | `detect_arch_changes.py` path (2 occurrences) |
| `.claude/docs/arch-changelog-guide.md` | `detect_arch_changes.py` path (1 occurrence) |
| `.claude/docs/DOCUMENTATION.md` | `apply_setup_claude.py` path (4 occurrences) |

## Decisions

| Decision | Rationale |
|----------|-----------|
| Approach C: Fix paths + add plugin manifest | Correct paths with minimal change, plus proper plugin structure for future marketplace compatibility |
| Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` | Matches the actual symlink location created by `install.sh` |
| Add `.claude-plugin/plugin.json` | Follows official plugin structure (matches `frontend-design`, `playwright` plugins) |

## Changes Needed

| File | Change |
|------|--------|
| `.claude-plugin/plugin.json` | **Create** — plugin manifest with name, description, author |
| `skills/setup-claude/SKILL.md` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |
| `skills/setup-claude/templates/commands/re-setup.md.template` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |
| `skills/setup-claude/templates/commands/finish-feature.md.template` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |
| `commands/re-setup.md` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |
| `commands/finish-feature.md` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |
| `.claude/docs/arch-changelog-guide.md` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |
| `.claude/docs/DOCUMENTATION.md` | Replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` |

## Open Questions
- None
