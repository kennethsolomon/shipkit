# Retrospective — 2026-03-29 — Token Optimization (Stack Filtering + CLAUDE.md Compression + Skill Compression)

## Metrics

| Metric | Value |
|--------|-------|
| Planned tasks | 14 (5 waves × tasks) |
| Completed | 14 / 14 (100%) |
| Commits | 0 (uncommitted — all on main) |
| Time span | 1 session (spanned 2 context windows) |
| Files changed | 30 (+1,387 / -2,055 lines, net -668) |
| Gate attempts | tests: 3 runs (9 fail → 7 fail → 0 fail) |
| Blockers | 3 (background agent permissions, worktree cleanup, template staleness) |
| Rework rate | ~15% (7 test fixes after main work) |

## What Went Well

- **Massive token reduction achieved without quality loss** — 13 skills compressed (12-58% each), CLAUDE.md compressed 22%, total net -668 lines across 30 files. Quality bar held: all instructions preserved, only prose→tables/lists conversion.
- **Stack filtering architecture is clean** — `skill-profiles.md` as a single source of truth with 2-axis (stack × capability) mapping. Config schema extensible. Backwards compatible (no config = auto-detect stack, install all).
- **Parallel compression via worktree agents** — 13 skill compressions ran in parallel using isolated worktrees. Throughput was high despite 3 worktrees failing to persist changes (brainstorming, ci, frontend-design).
- **Test suite caught every regression** — 343 assertions caught breadcrumb format changes, casing mismatches, missing headings, stale file paths. No regressions shipped.

## What Didn't Go Well

- **Templates not updated with source documents** — CLAUDE.md was compressed but CLAUDE.md.template was not updated initially. User had to explicitly correct this. Same issue with 5 command template breadcrumbs. This is a *recurring* pattern (see previous retro).
- **Background agents denied permissions** — 3 agents launched in background mode couldn't get Read tool approval (no user to approve). Left 3 orphaned worktrees. Fixed by switching to foreground agents.
- **Context window exhaustion** — session required 2 context windows. The compression work itself consumed significant context, ironically demonstrating the problem it was solving.
- **No branch created** — all work done directly on main. Should have branched per workflow rules.

## Patterns

- **Template divergence is the #1 recurring issue** — this is the third retro noting template/source drift. The `setup-claude-template-syncs-new-projects` learned pattern exists (0.7 confidence) but the lesson was still violated. Human memory isn't sufficient; needs automated enforcement.
- **Background agents are unreliable for permission-gated work** — any operation requiring user approval cannot run in background. This was learned as a pattern (`cleanup-stale-agent-worktrees`).
- **Test-driven refactoring works** — making format changes, running tests, fixing assertions is a reliable loop. The 343-test suite is a safety net that justifies its maintenance cost.

## Action Items

1. **Add template-sync lint check** — a test in `verify-workflow.sh` that diffs key sections of CLAUDE.md against CLAUDE.md.template and fails if they diverge beyond placeholder substitutions. Apply: next CI/test improvement task.

2. **Never use background agents for operations requiring tool approval** — use foreground agents or ensure all file reads are pre-approved. Apply: every session using parallel agents.

3. **Branch before starting work** — even infrastructure/docs work should branch per workflow rules. The `main` branch should only receive merges. Apply: every task.

4. **Commit incrementally per wave** — this session had 30 files of uncommitted changes. Should have committed after each wave (compression, filtering, templates, tests). Apply: every multi-wave task.

## Previous Action Item Follow-Up

- *Move DESIGN NOTE comments into agent templates* — Not addressed (out of scope for this task)
- *Never combine release script + git push in one command* — N/A (no release in this session)
- *Add template-sync check to /sk:setup-optimizer* — Partially addressed: setup-optimizer now has Step 0.5 for re-detection, but no automated lint check for template/source divergence yet
