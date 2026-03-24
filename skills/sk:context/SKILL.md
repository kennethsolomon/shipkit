---
name: sk:context
description: "Session initializer — loads all project context files and outputs a formatted session brief. Run this at the start of every conversation to orient the AI and yourself."
---

# /sk:context — Session Brief + Context Loader

Load all project context files into the conversation and output a formatted session brief. Designed to be run at the **start of every session** for instant orientation.

## What It Does

1. **Reads** all context files (listed below) to load project state into the conversation
2. **Outputs** a formatted SESSION BRIEF the user can read at a glance
3. **Applies** all active lessons from `tasks/lessons.md` as standing constraints for the session

## Hard Rules

- **Read-only.** This skill does not modify any files.
- **Graceful fallback.** Missing files are noted in the brief, not treated as errors.
- **No questions.** This skill runs silently — it does not ask the user anything.

---

## Files to Read (in order)

| # | File | What to Extract |
|---|------|-----------------|
| 1 | `tasks/todo.md` | Task name (from `# TODO —` heading), milestone progress, count of `- [x]` (done) vs `- [ ]` (pending) checkboxes |
| 2 | `tasks/progress.md` | Last 5 entries only (most recent work). If file is large, read only the last 50 lines. |
| 3 | `tasks/findings.md` | Current decisions, chosen approach, open questions |
| 4 | `tasks/lessons.md` | All active lessons — read in full, apply as constraints for this session |
| 5 | `docs/decisions.md` | If exists: last 3 ADR entries. If missing: note "no decisions log yet" |
| 6 | `docs/vision.md` | If exists: product name + value proposition. If missing: note "no vision.md found" |
| 7 | `tasks/tech-debt.md` | If exists: count entries with no `Resolved:` line (unresolved), highest severity among unresolved |

### Reading Strategy

- Read files 1-4 first (these are the core context).
- Files 5-6 are optional — check if they exist before reading.
- For `tasks/progress.md`: only read the last 50 lines to avoid loading a huge file.
- If `tasks/todo.md` is missing: the project has no active task.

---

## Output Format

After reading all files, output this session brief:

```
╔══════════════════════════════════════════╗
║            SESSION BRIEF                 ║
╚══════════════════════════════════════════╝
Branch:     [current git branch]
Task:       [task name from todo.md, or "No active task"]
Progress:   [N done] / [M total] checkboxes in todo.md
Last done:  [last progress.md entry summary, 1 line]
Lessons:    [count] active — [most critical 1-liner from lessons.md]
Open Qs:    [open questions from findings.md, or "none"]
Tech Debt:  [N] unresolved — highest: [severity] ([file:line])
Product:    [value prop from vision.md, or "no vision.md found"]
════════════════════════════════════════════
```

### Field Rules

- **Branch:** Run `git branch --show-current` to get the current branch name.
- **Task:** Extract from the first `# TODO —` line in `tasks/todo.md`. If the file doesn't exist or all checkboxes are done, show "No active task — ready to start fresh".
- **Progress:** Count `- [x]` (done) and `- [ ]` (pending) lines in `tasks/todo.md`. Stop counting at the first `## Verification`, `## Acceptance Criteria`, or `## Risks` heading (these are meta-sections, not tasks). Show `N done / M total`.
- **Last done:** The most recent entry from `tasks/progress.md`. Summarize in one line.
- **Lessons:** Count `### [` headings in `tasks/lessons.md` (each lesson starts with `### [YYYY-MM-DD]`). Show the count + the **Prevention:** line from the most recent lesson.
- **Open Qs:** Check for an "## Open Questions" section in `tasks/findings.md`. List them or say "none".
- **Tech Debt:** Read `tasks/tech-debt.md` if it exists. Count entries that have no `Resolved:` line — each entry starts with `### [`. For unresolved entries, find the highest severity. Show `N unresolved — highest: [severity] ([file])`. If file missing or 0 unresolved, show `none`.
- **Product:** From `docs/vision.md`, extract the value proposition. If file doesn't exist, say "no vision.md found".

---

## After the Brief

After outputting the session brief:

1. **State the active lessons** that apply as constraints. List each prevention rule as a bullet.
2. **State what's next** — tell the user the next step and the command to run.
3. If the user has a specific request, proceed with it (the context is now loaded).

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No `tasks/todo.md` | Show "No active task — ready to start fresh" |
| All checkboxes done in todo.md | Show "Task complete — 0 pending" for Progress field |
| No `tasks/progress.md` | Show "No progress logged yet" for Last done |
| No `tasks/findings.md` | Show "none" for Open Qs |
| No `tasks/lessons.md` | Show "0 active" for Lessons |
| No `docs/decisions.md` | Show "no decisions log yet" — do not error |
| No `docs/vision.md` | Show "no vision.md found" — do not error |
| No `tasks/tech-debt.md` | Show "none" for Tech Debt field — do not error |
| All checkboxes done in todo.md | Show "Task complete — 0 pending" |

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:context"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> This skill is lightweight (read-only file operations + brief output). Sonnet is sufficient for all quality profiles. Haiku for budget.
