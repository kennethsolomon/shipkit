# 2026-04-02 — Progressive Disclosure + Auto-Progress Hook

## Summary

2 improvements adapted from claude-mem (thedotmack/claude-mem). No workflow step order changed — both are internal mechanic upgrades to existing systems.

---

## Changes

### 1. Progressive Disclosure in `/sk:context`

**File:** `skills/sk:context/SKILL.md`, `docs/sk:features/sk-context.md`

**Change:** `/sk:context` now uses a progressive reading strategy instead of loading all files in full upfront.

**Before:** All 7 context files read in full at session start. On a mature project with large `tasks/findings.md` (500+ lines) and `tasks/lessons.md` (20+ lessons), this could consume 3,000+ tokens before any work began.

**After:**
- `tasks/findings.md` → first 50 lines only (sufficient for open questions extraction)
- `tasks/lessons.md` → grep count + last 30 lines only (last 2–3 lessons for brief)
- `tasks/tech-debt.md` → grep headers only (count + severity)
- All other files unchanged (already lean: todo.md, progress.md capped at 50 lines, vision.md small)

A **Context Index** section is appended after the SESSION BRIEF:
```
── On demand ──────────────────────────────────────────
  findings  [~180 lines]  2 open questions   → "load findings"
  lessons   [7 active]    last: 2026-04-01   → "load lessons"
  tech-debt [3 unresolved, HIGH]             → "load debt"
───────────────────────────────────────────────────────
```

**On-demand triggers:** `load findings`, `load lessons`, `load debt`, `load all` (or `/sk:context --load <name>`) → reads full file on request.

**Estimated savings:** 60–80% reduction in cold-start context on mature projects with large task files.

---

### 2. Auto-Progress Hook (`auto-progress.sh`)

**Files:** `.claude/hooks/auto-progress.sh`, `.claude/settings.json`, `skills/sk:setup-claude/templates/hooks/auto-progress.sh`, `skills/sk:setup-claude/templates/.claude/settings.json.template`, `skills/sk:setup-optimizer/SKILL.md`

**Change:** New `PostToolUse` hook that auto-logs significant git events to `tasks/progress.md`.

**Why:** Manual progress logging is the most-skipped step in the workflow (noted in 5 consecutive retros). The hook provides a passive safety net — `tasks/progress.md` now always captures the key moments even when the AI forgets to log them manually.

**What it captures:**
| Event | Log entry |
|-------|-----------|
| `git commit` | `- [HH:MM] Auto: git commit — "feat: add auth"` |
| `git push` | `- [HH:MM] Auto: git push — origin main` |
| `git tag` | `- [HH:MM] Auto: git tag — v3.24.0` |

**Hard constraints:**
- Only fires on `Bash` tool calls — filtered internally
- Only writes if `tasks/progress.md` already exists (never creates it)
- Exit 0 always — never blocks tool execution
- Classified as an **enhanced hook** (opt-in) — not installed by default, available via `/sk:setup-optimizer`

---

## Files Updated

- `skills/sk:context/SKILL.md` — progressive reading strategy, Context Index, on-demand loading
- `docs/sk:features/sk-context.md` — updated spec
- `.claude/hooks/auto-progress.sh` — new hook
- `.claude/settings.json` — PostToolUse entry for auto-progress.sh
- `skills/sk:setup-optimizer/SKILL.md` — auto-progress.sh added to enhanced hooks list
- `skills/sk:setup-claude/templates/hooks/auto-progress.sh` — new template
- `skills/sk:setup-claude/templates/.claude/settings.json.template` — PostToolUse hook wiring
- `docs/FEATURES.md` — sk-context.md spec date updated
- `README.md` — keyword-router added to always-installed hooks; auto-progress added to opt-in hooks

---

## Design Decisions

**Why progressive disclosure and not full removal of upfront reading?**
The SESSION BRIEF still needs certain data (task name, progress counts, open questions, lesson count). The index pass reads only what the brief extracts. Full content is preserved and accessible — it's deferred, not discarded.

**Why only git events in auto-progress, not all Bash commands?**
All Bash commands would be extremely noisy (hundreds of entries per session for grep, git status, etc.). Git commit/push/tag are the high-signal moments — they represent completed units of work worth logging. This matches the intent of `tasks/progress.md` as a milestone log, not a command transcript.

**Why enhanced (opt-in) rather than core for auto-progress?**
It writes to a project file (`tasks/progress.md`) that may not exist in all projects. Core hooks should be safe to run in any project. The hook already guards against this (`[ -f "tasks/progress.md" ] || exit 0`) but the opt-in classification communicates the intent correctly.
