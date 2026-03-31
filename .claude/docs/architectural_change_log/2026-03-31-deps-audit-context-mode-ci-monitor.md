# Deps Audit + Context-Mode + CI Monitor (March 31, 2026)

## Summary

Added `/sk:deps-audit` as a new quality gate (now 7 gates in Batch 1), integrated context-mode plugin into setup-claude and setup-optimizer, added CI monitor loop to `/sk:finish-feature`, added task onboarding record to `/sk:start`, and added skill improvement pass to `/sk:learn`.

## Type of Architectural Change

**New Skill + Integration + Workflow Enhancement**

## What Changed

### New skill (1 directory)
- `skills/sk:deps-audit/` — CVE scanning, license compliance, outdated package detection across npm, Composer, Cargo, pip, Go modules, and Bundler. Auto-fixes safe patch/minor bumps.

### Gates expanded (Batch 1: 3 → 4 parallel agents)
- `skills/sk:gates/SKILL.md` — Batch 1 now runs lint + security + perf + deps-audit in parallel. Gate count 6 → 7.

### Workflow enhancements (3 skills modified)
- `commands/sk/finish-feature.md` — Added Step 7.5: mandatory CI monitor loop after PR creation. Polls CI every 60s, addresses all auto-reviewer comments, iterates until CI green + zero unresolved threads.
- `skills/sk:start/SKILL.md` — Added Step 3.5: writes `tasks/onboarding/[task-slug].md` after routing. Captures flow, mode, agents, stack state for session continuity.
- `skills/sk:learn/SKILL.md` — Added Phase 6: skill improvement pass. Scans session for evidence of skill underperformance and proposes targeted SKILL.md diffs.

### Context-mode plugin integration (2 skills modified)
- `skills/sk:setup-claude/SKILL.md` — Added context-mode as 4th recommended plugin in MCP Servers & Plugins section.
- `skills/sk:setup-optimizer/SKILL.md` — Added context-mode to Step 1.7 check: install if missing, run `/context-mode:ctx-upgrade` if update available.

### Documentation updated (9 files)
- `CLAUDE.md` — deps-audit in commands table, gates step note updated
- `commands/sk/help.md` — deps-audit in commands + model routing, step 7 gate list
- `skills/sk:autopilot/SKILL.md` — step 7 gate list
- `skills/sk:setup-optimizer/SKILL.md` — missing commands list
- `skills/sk:setup-claude/templates/CLAUDE.md.template` — commands table, gates note
- `skills/sk:setup-claude/templates/commands/finish-feature.md.template` — CI monitor loop
- `docs/FEATURES.md` — deps-audit entry
- `docs/sk:features/sk-deps-audit.md` — full feature spec (created)
- `README.md` — gates table, Scenario A, commands count, Recommended Community Plugins section

## Impact

- `/sk:gates` Batch 1 now runs 4 agents in parallel instead of 3. Batch 1 wall-clock time increases slightly (deps-audit is haiku-based and fast).
- Every PR created via `/sk:finish-feature` now has a mandatory CI monitor loop — PRs will not be considered done until CI is green and all auto-reviewer comments are addressed.
- `/sk:setup-claude` and `/sk:setup-optimizer` will prompt to install/update context-mode on new and existing projects.
- `/sk:start` now writes `tasks/onboarding/[slug].md` on every invocation — adds one small file per task.

## Before & After

**Gates Batch 1 before:** lint + security-reviewer + performance-optimizer (3 parallel)
**Gates Batch 1 after:** lint + security-reviewer + performance-optimizer + deps-audit (4 parallel)

**finish-feature before:** PR created → learn → retro
**finish-feature after:** PR created → CI monitor loop (mandatory) → learn → retro

**setup-claude before:** Sequential Thinking, Context7, ccstatusline (3 recommended plugins)
**setup-claude after:** Sequential Thinking, Context7, ccstatusline, context-mode (4 recommended plugins)

## Affected Components

- `skills/sk:deps-audit/` — new
- `skills/sk:gates/` — Batch 1 expanded
- `commands/sk/finish-feature.md` — CI monitor added
- `skills/sk:start/` — onboarding record added
- `skills/sk:learn/` — skill improvement pass added
- `skills/sk:setup-claude/` — context-mode plugin added
- `skills/sk:setup-optimizer/` — context-mode check added, deps-audit in commands list

## Migration/Compatibility

Backward compatible. Existing projects:
- Will get deps-audit in gates automatically on next `/sk:gates` run (no config needed).
- Will get the CI monitor loop in `/sk:finish-feature` automatically.
- Will be prompted to install context-mode on next `/sk:setup-optimizer` run.
- No existing files are modified or removed by these changes.

## Verification

- [ ] `/sk:deps-audit` runs standalone and writes to `tasks/security-findings.md`
- [ ] `/sk:gates` Batch 1 shows 4 agents in parallel output
- [ ] `/sk:finish-feature` step 7.5 CI loop runs after PR creation
- [ ] `/sk:setup-claude` prompts for context-mode during MCP setup
- [ ] `/sk:setup-optimizer` step 1.7 shows context-mode status
