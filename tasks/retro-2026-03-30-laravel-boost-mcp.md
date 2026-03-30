# Retrospective — 2026-03-30 — Laravel Boost MCP + Stack-Conditional MCP Management

## Metrics

| Metric | Value |
|--------|-------|
| Planned tasks | ~12 (informal — no todo.md task, driven by conversation) |
| Completed | 12 / 12 (100%) |
| Commits | 3 (docs, Release v3.21.0, docs) |
| Time span | ~14 hours (2026-03-29 23:19 → 2026-03-30 13:01) |
| Files changed | 15 (+562 / -27 lines) |
| Gate attempts | tests: 1 run (15/15 pass, 1 fix needed for language detection priority) |
| Blockers | 1 (language detection bug — Laravel+package.json → JavaScript was detected instead of PHP) |
| Rework rate | ~8% (1 test failure → 1 targeted fix) |

## What Went Well

- **Code reviewer caught architectural issues before shipping** — running the `code-reviewer` agent after implementation surfaced 3 critical issues: dual step ownership of `.mcp.json`, buried `boost:install` warning, and missing Sail migration path. All fixed before the release commit.
- **Test-first on the Python script** — adding 10 tests before/alongside the implementation caught the language detection priority bug immediately (Laravel + package.json → returned JavaScript instead of PHP). The test suite is now 15 tests and caught a real regression.
- **Full documentation sweep was done systematically** — templates, README, DOCUMENTATION.md, CHANGELOG, skill-profiles.md, and 4 SKILL.md files all updated in a single pass. No doc was missed after the audit.
- **Clean add/remove/update lifecycle from the start** — `_deploy_project_mcp()` was designed with all three operations (add/remove/update for Sail migration) rather than additive-only, avoiding the pattern that caused the previous retro's "template divergence" issue.

## What Didn't Go Well

- **Template audit was reactive, not proactive** — `laravel.md.template` was only updated after an explicit "does all templates now fix?" question. Should have been part of the initial implementation pass. This is the *third retro in a row* noting this issue.
- **No formal todo.md task created** — the entire feature was driven by conversation without a written plan. This made it harder to track progress and would have made `/sk:scope-check` impossible to run.
- **Previous retro action item not addressed** — "Add template-sync lint check" from the 2026-03-29 retro was not actioned. The template divergence issue recurred as a result.

## Patterns

- **Template divergence is now the #1 systemic process failure** — this is the third consecutive retro noting the same issue. The learned pattern `audit-templates-after-skill-changes` was just created (0.3 confidence) but an automated guard is the real fix. Human checklists aren't working.
- **Code reviewer prevents expensive rework** — two retros now confirm that proactively running the code-reviewer after cross-cutting changes catches architectural issues (dual ownership, missing edge cases) that are much cheaper to fix before commit than after.
- **Single source of truth works** — `skill-profiles.md` as the authoritative mapping for skills/agents/rules/MCP. Adding MCP to the same file rather than a new one kept the system coherent.

## Action Items

1. **Add template-sync test to `verify-workflow.sh`** — diff `laravel.md.template` against `sk:setup-claude/SKILL.md` key sections. Fail if `laravel.md.template` lacks a section that SKILL.md documents. Apply: next improvement task. *(Carried over from 2026-03-29 retro — now high priority given 3 occurrences.)*

2. **Run code-reviewer after every cross-cutting change** — add to personal workflow: after any change touching ≥3 SKILL.md files or introducing new lifecycle logic, run code-reviewer before committing. Apply: every session.

3. **Create todo.md task even for conversation-driven features** — before starting implementation work that spans multiple files, write at least 3-5 checkboxes to `tasks/todo.md`. Enables scope-check and produces a retrospective anchor. Apply: at session start when task scope becomes clear.

## Previous Action Item Follow-Up

- **Add template-sync lint check** (from 2026-03-29) — ❌ Still open. Template divergence recurred. Escalated to high priority.
- **Never use background agents for permission-gated work** (from 2026-03-29) — ✅ Not violated this session. All agents ran foreground.
