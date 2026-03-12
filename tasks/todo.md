# TODO — 2026-03-12 — Fix Plugin Setup & Script Paths

## Goal

Fix broken script paths (`$HOME/.agents` → `$HOME/.claude/plugins/claude-skills`) across 7 files and add `.claude-plugin/plugin.json` manifest so the plugin works correctly after `./install.sh`.

## Plan

### 1. Create plugin manifest
- [x] Create `.claude-plugin/plugin.json` with name, description, author fields (matching official plugin format)

### 2. Fix script paths in source files (templates + SKILL.md)
- [x] `skills/setup-claude/SKILL.md` — replace `$HOME/.agents` → `$HOME/.claude/plugins/claude-skills` (4 occurrences)
- [x] `skills/setup-claude/templates/commands/re-setup.md.template` — replace path (3 occurrences)
- [x] `skills/setup-claude/templates/commands/finish-feature.md.template` — replace path (2 occurrences)

### 3. Fix script paths in generated/output files
- [x] `commands/re-setup.md` — replace path (3 occurrences)
- [x] `commands/finish-feature.md` — replace path (2 occurrences)
- [x] `.claude/docs/arch-changelog-guide.md` — replace path (1 occurrence)
- [x] `.claude/docs/DOCUMENTATION.md` — replace path (4 occurrences + legacy install instructions)

### 4. Verify
- [x] Run `python3 "$HOME/.claude/plugins/claude-skills/skills/setup-claude/scripts/apply_setup_claude.py" "$(pwd)" --dry-run` — succeeds
- [x] Confirm no remaining references to `$HOME/.agents` in the repo (only in tasks/ docs describing the problem)
- [x] Confirm `.claude-plugin/plugin.json` exists and is valid JSON

## Results
- All 7 source files updated with correct paths
- DOCUMENTATION.md also had legacy install instructions (clone to ~/.agents, link script) — updated to match current install.sh flow
- Plugin manifest created at `.claude-plugin/plugin.json`
- Dry-run script executes successfully from new path
- No functional `.agents/skills` references remain
