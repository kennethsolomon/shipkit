# /sk:context

> **Status:** Shipped (updated v3.24.0 — 2026-04-02)
> **Type:** Developer Tool (standalone — not a numbered workflow step)
> **Command:** `/sk:context`
> **Skill file:** `skills/sk:context/SKILL.md`

---

## Overview

Session initializer that loads all project context files into the conversation and outputs a formatted SESSION BRIEF. Designed to be run at the **start of every conversation** for instant orientation.

Uses **progressive disclosure**: reads only what the SESSION BRIEF needs upfront (index pass), then makes full file content available on demand. Reduces cold-start context burn by 60–80% on mature projects. Read-only, no modifications, no questions.

---

## Inputs

| Input | How Read | Required |
|-------|----------|----------|
| `tasks/todo.md` | Full | No — shows "No active task" if missing |
| `tasks/progress.md` | Last 50 lines only | No — shows "No progress logged yet" if missing |
| `tasks/findings.md` | First 50 lines only (index pass) | No — shows "none" for Open Qs if missing |
| `tasks/lessons.md` | Count (grep) + last 30 lines (index pass) | No — shows "0 active" if missing |
| `docs/decisions.md` | Last 3 entries | No — shows "no decisions log yet" if missing |
| `docs/vision.md` | First 10 lines | No — shows "no vision.md found" if missing |
| `tasks/tech-debt.md` | Headers grep only (index pass) | No — shows "none logged" if missing |
| `git branch --show-current` | Git CLI | Yes — always available |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| SESSION BRIEF | Terminal (stdout) | Formatted box with branch, task, progress, lessons, open Qs, tech debt, product |
| Context Index | Terminal (stdout) | One-line per heavy file — shows what's available on demand |
| Active lessons | Terminal (stdout) | Prevention rules from last 3 lessons as standing constraints |
| Next step | Terminal (stdout) | Command to run next |

### SESSION BRIEF Format

```
╔══════════════════════════════════════════╗
║            SESSION BRIEF                 ║
╚══════════════════════════════════════════╝
Branch:     feature/add-auth
Task:       Add email/password authentication
Progress:   12/19 checkboxes done
Last done:  Implemented AuthController with JWT signing
Lessons:    7 active — maintenance-guide.md must be read first
Open Qs:    none
Tech Debt:  3 unresolved — highest: HIGH (src/auth.ts:42)
Product:    Ship features with TDD, security audits, and code review
════════════════════════════════════════════

── On demand ──────────────────────────────────────────
  findings  [~180 lines]  2 open questions   → "load findings"
  lessons   [7 active]    last: 2026-04-01   → "load lessons"
  tech-debt [3 unresolved, HIGH]             → "load debt"
───────────────────────────────────────────────────────
```

---

## Business Logic

### Index Pass (always runs)

1. Read `tasks/todo.md` in full → extract task name, checkbox counts
2. Read last 50 lines of `tasks/progress.md` → extract last entry
3. Read first 50 lines of `tasks/findings.md` → extract open questions section
4. Grep `tasks/lessons.md` for `### [` count; read last 30 lines for recent lessons
5. Read last 3 entries of `docs/decisions.md` if it exists
6. Read first 10 lines of `docs/vision.md` if it exists
7. Grep `tasks/tech-debt.md` for entry count and severity keywords

### Context Index

After the SESSION BRIEF, output one-line per file that exists AND has content worth loading:
- Only show files where the index pass found content (skip if missing or empty)
- Include approximate line count, key stat (open Qs / active count / unresolved count)
- Show on-demand trigger phrase

### On-Demand Loading

When user says a trigger phrase, read the full file and output it:

| Trigger | Action |
|---------|--------|
| `load findings` / `show findings` | Read `tasks/findings.md` in full |
| `load lessons` / `show lessons` | Read `tasks/lessons.md` in full; apply ALL lessons as constraints |
| `load debt` / `load tech-debt` | Read `tasks/tech-debt.md` in full |
| `load all` / `full context` | Read all 7 files in full (original behavior) |
| `/sk:context --load <name>` | Same as trigger phrase variants |

---

## Hard Rules

- **Read-only** — this skill never modifies any files
- **Graceful fallback** — missing files are noted in the brief, never treated as errors
- **No questions** — runs silently, does not ask the user anything
- **Progressive by default** — index pass only; full files on demand

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No `tasks/todo.md` | Shows "No active task — ready to start fresh" |
| No `tasks/progress.md` | Shows "No progress logged yet" for Last done |
| No `tasks/findings.md` | Shows "none" for Open Qs; omits findings row from Context Index |
| No `tasks/lessons.md` | Shows "0 active" for Lessons; omits lessons row from Context Index |
| No `docs/decisions.md` | Shows "no decisions log yet" — no error |
| No `docs/vision.md` | Shows "no vision.md found" — no error |
| No `tasks/tech-debt.md` | Shows "none logged"; omits debt row from Context Index |
| All tech-debt resolved | Shows "none"; omits debt row from Context Index |
| All checkboxes done | Shows "Task complete — 0 pending" |
| Context Index has no rows | Omits entire "On demand" section |
| User says "load all" | Reads all 7 files in full — original pre-v3.24.0 behavior |

---

## Error States

| Condition | Behavior |
|-----------|----------|
| Git not available | Branch field shows "unknown" |
| File read error (not ENOENT) | Treat as missing — use fallback value |

---

## Platform Notes

CLI tool — no mobile or web platform. Works in any project that uses ShipKit's `tasks/` file structure.

---

## Related Docs

- `skills/sk:context/SKILL.md` — full implementation spec and model routing
- `tasks/todo.md` — primary data source for task and progress info
- `tasks/lessons.md` — loaded progressively; say "load lessons" for full content
- `docs/decisions.md` — ADR log (created by sk:brainstorm)
- `docs/vision.md` — product context (created by sk:mvp Step 9)
