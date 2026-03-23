# Component Architecture Update (March 23, 2026)

## Summary

Added Claude Code infrastructure layer to ShipKit: lifecycle hooks, path-scoped rules, gate agents, statusline, and 5 new workflow skills. This extends the setup-claude deployment pipeline to generate hooks, agents, rules, and settings.json alongside existing template files.

## Type of Architectural Change

**Pattern + Subsystem + Integration**

## What Changed

**New infrastructure templates (22 files):**
- 6 lifecycle hook scripts (`templates/hooks/`)
- 5 gate agent definitions (`templates/.claude/agents/`)
- 5 path-scoped rule templates (`templates/.claude/rules/`)
- 1 settings.json template (`templates/.claude/settings.json.template`)
- 1 statusline script (`templates/.claude/statusline.sh`)

**New skills (5 directories):**
- `skills/sk:scope-check/` — scope creep detection
- `skills/sk:retro/` — post-ship retrospective
- `skills/sk:reverse-doc/` — reverse documentation
- `skills/sk:gates/` — parallel gate orchestrator
- `skills/sk:fast-track/` — abbreviated workflow

**Modified deployment engine:**
- `apply_setup_claude.py` — new `_collect_results()`, `_deploy_directory()`, `_deploy_rendered_file()`, `_rules_filter()`, cached detection with `--force-detect`

**Statistics:**
- Lines added: 2360
- Lines removed: 94
- Files modified: 34

## Impact

- `sk:setup-claude` now deploys hooks, agents, rules, settings.json, and statusline to target projects
- Gate skills can now run as isolated sub-agents with parallel execution via `/sk:gates`
- Stack detection results are cached in `.shipkit/config.json` (7-day TTL)

## Before & After

**Before:**
`sk:setup-claude` deployed: CLAUDE.md, commands/, tasks/, docs/

**After:**
`sk:setup-claude` deploys: CLAUDE.md, commands/, tasks/, docs/, hooks/, agents/, rules/, settings.json, statusline.sh

## Affected Components

- `skills/sk:setup-claude/` — deployment pipeline expanded
- `CLAUDE.md` — 5 new commands in table
- `README.md`, `DOCUMENTATION.md` — updated command references

## Migration/Compatibility

Backward compatibility confirmed. Existing projects running `sk:setup-claude` will gain new files on next run but no existing files are modified or removed. New files use `created` mode (create-if-missing).

## Verification

- [x] All affected code paths tested (215/215 assertions pass)
- [x] Related documentation updated (CLAUDE.md, README.md, DOCUMENTATION.md, CHANGELOG.md)
- [x] No breaking changes — additive only
- [x] Dependent systems verified (apply_setup_claude.py tested with --dry-run)
