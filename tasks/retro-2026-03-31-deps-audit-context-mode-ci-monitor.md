# Retrospective — 2026-03-31 — deps-audit Gate, context-mode Integration, CI Monitor Loop

## Metrics

| Metric | Value |
|--------|-------|
| Planned tasks | ~0 formal (conversation-driven, no todo.md) |
| Completed | All deliverables shipped |
| Commits | 4 (feat + release + docs + fix) |
| Time span | ~24 hours (2026-03-30 13:01 → 2026-03-31 13:34) |
| Files changed | 25 (+870 / -41 lines) |
| Gate attempts | None (ShipKit meta-change — no app to lint/test) |
| Blockers | 1 (maintenance guide not read first → ~9 files missed, second-pass required) |
| Rework rate | ~14% (1 fix commit / 7 total commits) |
| Patterns captured | 4 (via /sk:learn) |

## What Went Well

- **Research-before-adapt classification worked cleanly** — applied steal/install/skip buckets upfront before touching files. Correctly routed context-mode → plugin (hooks + SQLite + MCP = infrastructure) and deps-audit → skill (prompt pattern). Zero misclassifications.
- **4 reusable patterns saved to ~/.claude/skills/learned/** — `maintenance-guide-first`, `research-before-adapt`, `plugin-vs-skill-decision`, `community-plugin-4-touchpoints`. These are now loadable in future sessions.
- **Phase 6 (Skill Improvement) in /sk:learn worked on first run** — the new phase correctly identified the maintenance-guide miss as a skill improvement candidate, and the fix was applied to `sk:skill-creator` before the retro.
- **Template sync test finally added** — `ccc8aaa` (from the previous session rollover) addressed the #1 recurring issue from 3 consecutive retros. `verify-workflow.sh` now has Laravel Boost MCP template sync guards.
- **Community plugin 4-touchpoint pattern documented** — future plugin additions have a clear checklist: setup-claude + setup-optimizer + README + maintenance-guide.

## What Didn't Go Well

- **Maintenance guide read AFTER implementation, not before** — ~9 files were missed on the first pass (help.md, autopilot, setup-optimizer, docs/FEATURES.md, arch changelog, feature spec, maintenance guide itself). Only caught after explicitly referencing the guide. This is the exact scenario the `maintenance-guide-first` pattern was written to prevent — and it happened before the pattern existed.
- **No formal todo.md created** — fourth consecutive retro noting this. Conversation-driven work without a written plan makes scope-check impossible and retrospective data thin.
- **Code-reviewer not run on cross-cutting changes** — action item from the 2026-03-30 retro. 17 files changed in a single feat commit with no structured review pass before committing.

## Patterns

- **Maintenance guide miss is a process smell, not a knowledge gap** — the file was known; reading it was skipped under session pressure. The fix (adding the reminder to `sk:skill-creator`) addresses the trigger point, but the root cause is workflow habit. Worth watching whether the Phase 6 fix actually changes behavior in the next structural change session.
- **Research → classify → implement order reduces rework** — spending the first phase classifying steal/install/skip (with no code written) meant zero backtracking on implementation choices. A pattern worth codifying as a default for any external-repo evaluation task.
- **Template sync is now guarded** — after 3 retros of noting the same issue, the test now exists. Watch whether the failure rate drops to zero over the next 2 sessions.

## Action Items

1. **Create todo.md before any session that touches ≥3 files** — write 3-5 checkboxes before starting implementation. Enables scope-check and produces a retro anchor. This is now a 4-retro recurring action item — escalate to a CLAUDE.md rule if it recurs again. Apply: at session start when scope becomes clear.

2. **Read maintenance-guide.md as the literal first step for ShipKit structural changes** — not after implementation, not when prompted by the user. The `sk:skill-creator` reminder was added, but the habit needs to form before the reminder is needed. Apply: any session touching skills, gates, agents, or community plugins.

3. **Run code-reviewer after changes touching ≥3 SKILL.md files** — carried over from 2026-03-30 retro. Still not done. If it recurs in the next retro, add it as a mandatory step in `sk:gates` or `sk:finish-feature`. Apply: every cross-cutting ShipKit session.

## Previous Action Item Follow-Up

- **Add template-sync lint check** (from 2026-03-29, escalated in 2026-03-30) — ✅ Done. `ccc8aaa` added Laravel Boost MCP template sync guards to `verify-workflow.sh`. 15 new assertions.
- **Run code-reviewer after cross-cutting changes** (from 2026-03-30) — ❌ Not done this session. Escalated.
- **Create todo.md for conversation-driven features** (from 2026-03-30) — ❌ Not done this session. 4th occurrence — escalate to CLAUDE.md rule if recurs.
- **Never use background agents for permission-gated work** (from 2026-03-29) — ✅ Not violated.
