---
name: sk:context
description: "Session initializer — loads all project context files and outputs a formatted session brief. Run this at the start of every conversation to orient the AI and yourself."
model: haiku
---

# /sk:context — Session Brief + Context Loader

Load all project context files into the conversation and output a formatted session brief. Designed to be run at the **start of every session** for instant orientation.

## What It Does

1. **Reads** context files using a progressive index strategy — reads only what the SESSION BRIEF needs
2. **Outputs** a formatted SESSION BRIEF plus a Context Index showing what's available on demand
3. **Applies** all active lessons from `tasks/lessons.md` as standing constraints for the session
4. **Loads** full file content on demand when requested

## Hard Rules

- **Read-only.** This skill does not modify any files.
- **Graceful fallback.** Missing files are noted in the brief, not treated as errors.
- **No questions.** This skill runs silently — it does not ask the user anything.

---

## Files to Read (Progressive Strategy)

| # | File | How to Read | What to Extract |
|---|------|-------------|-----------------|
| 1 | `tasks/todo.md` | Full | Task name, milestone progress, `[x]`/`[ ]` counts |
| 2 | `tasks/progress.md` | Last 50 lines only | Most recent entry summary |
| 3 | `tasks/findings.md` | First 50 lines only | Open questions section, headings |
| 4 | `tasks/lessons.md` | Last 30 lines only + count | Count `### [` headings (total); read last 30 lines for recent lessons |
| 5 | `docs/decisions.md` | Last 3 entries | ADR summaries |
| 6 | `docs/vision.md` | First 10 lines | Product name + value proposition |
| 7 | `tasks/tech-debt.md` | Headers only (grep) | Count unresolved entries + highest severity |

### Why Progressive Reading

- `tasks/findings.md` can grow to 500+ lines. The first 50 lines contain the section headings and open questions — all the SESSION BRIEF needs.
- `tasks/lessons.md` can accumulate 20+ lessons. The count + last 2–3 lessons are sufficient for the brief; full lessons are loaded on demand when needed for active work.
- `tasks/tech-debt.md` only needs entry counts and severity labels for the brief.

Full content is always available via on-demand loading (see below).

---

## Output Format

### Part 1 — SESSION BRIEF

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

### Part 2 — Context Index

After the SESSION BRIEF, output the context index:

```
── On demand ──────────────────────────────────────────
  findings  [~N lines]  [N open questions]   → "load findings"
  lessons   [N active]  last: YYYY-MM-DD     → "load lessons"
  tech-debt [N unresolved, SEVERITY]         → "load debt"
───────────────────────────────────────────────────────
```

Only show rows for files that exist. If a file is missing, omit its row silently.

### Part 3 — Active Lessons + Next Step

After the context index:
1. **State the active lessons** that apply as constraints. List each **Prevention:** rule as a bullet (from the last 3 lessons read).
2. **State what's next** — tell the user the next step and the command to run.

---

## Field Rules

- **Branch:** Run `git branch --show-current`.
- **Task:** Extract from the first `# TODO —` line in `tasks/todo.md`. If missing or all done: "No active task — ready to start fresh".
- **Progress:** Count `- [x]` (done) and `- [ ]` (pending) in `tasks/todo.md`. Stop at first `## Verification`, `## Acceptance Criteria`, or `## Risks` heading.
- **Last done:** Most recent entry from `tasks/progress.md` (last 50 lines). Summarize in one line.
- **Lessons count:** Count `### [` occurrences in `tasks/lessons.md` (full grep, not full read). Show count + **Prevention:** line from the most recently read lesson.
- **Open Qs:** `## Open Questions` section in first 50 lines of `tasks/findings.md`, or "none".
- **Tech Debt:** Grep `tasks/tech-debt.md` for `### [` entries without `Resolved:`. Count unresolved + find highest severity keyword (CRITICAL > HIGH > MEDIUM > LOW). Show `N unresolved — highest: [severity] ([file])`. "none" if 0 or file missing.
- **Product:** First `value proposition` or description paragraph from `docs/vision.md` first 10 lines.

---

## On-Demand Loading

When the user says any of the following (case-insensitive), read the full file and output it:

| Trigger | Action |
|---------|--------|
| `load findings` / `show findings` | Read `tasks/findings.md` in full and output |
| `load lessons` / `show lessons` | Read `tasks/lessons.md` in full and output, applying ALL lessons as constraints |
| `load debt` / `load tech-debt` / `show debt` | Read `tasks/tech-debt.md` in full and output |
| `load all` / `full context` | Read all 7 files in full (original behavior) |
| `/sk:context --load findings` | Same as "load findings" |
| `/sk:context --load lessons` | Same as "load lessons" |
| `/sk:context --load all` | Same as "load all" |

On-demand loads are additive — they do not re-run the SESSION BRIEF.

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No `tasks/todo.md` | Show "No active task — ready to start fresh" |
| All checkboxes done in todo.md | Show "Task complete — 0 pending" for Progress field |
| No `tasks/progress.md` | Show "No progress logged yet" for Last done |
| No `tasks/findings.md` | Show "none" for Open Qs; omit findings row from Context Index |
| No `tasks/lessons.md` | Show "0 active" for Lessons; omit lessons row from Context Index |
| No `docs/decisions.md` | Show "no decisions log yet" — do not error |
| No `docs/vision.md` | Show "no vision.md found" — do not error |
| No `tasks/tech-debt.md` | Show "none" for Tech Debt; omit debt row from Context Index |
| All tech-debt entries resolved | Show "none" for Tech Debt; omit debt row from Context Index |
| Context Index has no rows | Omit the entire "On demand" section |
| User requests "load all" | Read all 7 files in full — original behavior |

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
