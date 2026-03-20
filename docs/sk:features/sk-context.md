# /sk:context

> **Status:** Shipped (v3.7.0 — 2026-03-20)
> **Type:** Developer Tool (standalone — not a numbered workflow step)
> **Command:** `/sk:context`
> **Skill file:** `skills/sk:context/SKILL.md`

---

## Overview

Session initializer that loads all project context files into the conversation and outputs a formatted SESSION BRIEF. Designed to be run at the **start of every conversation** for instant orientation — replaces manually reading 5+ files. Read-only, no modifications, no questions.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Project planning file | No — shows "No active task" if missing |
| `tasks/workflow-status.md` | Workflow tracker | No — shows "Workflow not started" if missing |
| `tasks/progress.md` | Work log (last 50 lines only) | No — shows "No progress logged yet" if missing |
| `tasks/findings.md` | Current task decisions | No — shows "none" for Open Qs if missing |
| `tasks/lessons.md` | Past corrections (read in full) | No — shows "0 active" if missing |
| `docs/decisions.md` | ADR log (last 3 entries) | No — shows "no decisions log yet" if missing |
| `docs/vision.md` | Product context (name + value prop) | No — shows "no vision.md found" if missing |
| `tasks/tech-debt.md` | Pre-existing issues from gates | No — shows "none logged" if missing |
| `git branch --show-current` | Git CLI | Yes — always available |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| SESSION BRIEF | Terminal (stdout) | Formatted box with branch, task, step, pending, lessons, open Qs, product |
| Active lessons | Terminal (stdout) | Bulleted list of prevention rules from lessons.md |
| Next step | Terminal (stdout) | Command to run next |

### SESSION BRIEF Format

```
╔══════════════════════════════════════════╗
║            SESSION BRIEF                 ║
╚══════════════════════════════════════════╝
Branch:     feature/xxx
Task:       Task name from todo.md
Step:       10 Implement → run `/sk:execute-plan`
Last done:  Last progress.md entry summary
Pending:    5 checkboxes remaining in todo.md
Lessons:    7 active — most critical 1-liner
Open Qs:    none
Tech Debt:  3 unresolved — highest: high (src/auth.ts:42)
Product:    value prop from vision.md
════════════════════════════════════════════
```

---

## Business Logic

1. **Read core files (1-5)** — always attempted. Missing files produce fallback values, not errors.
2. **Read optional files (6-7)** — check existence before reading. Missing = noted in brief.
3. **Extract fields:**
   - **Branch:** `git branch --show-current`
   - **Task:** First `# TODO —` line, text after last em dash `—`
   - **Step:** Row containing `>> next <<` in workflow-status.md table; extract step #, name, command
   - **Last done:** Most recent entry from progress.md (1-line summary)
   - **Pending:** Count `- [ ]` lines in todo.md; stop at `## Verification`, `## Acceptance Criteria`, or `## Risks` headings
   - **Lessons:** Count `### [` headings in lessons.md; show count + **Prevention:** line from most recent
   - **Open Qs:** `## Open Questions` section in findings.md, or "none"
   - **Tech Debt:** Count entries in tech-debt.md with no `Resolved:` line; report count + highest severity + file. "none logged" if file missing, "none" if 0 unresolved.
   - **Product:** Value proposition from vision.md, or "no vision.md found"
4. **Output SESSION BRIEF** in the box format.
5. **State active lessons** as bulleted prevention rules — these become standing constraints.
6. **State next step** — the command to run.
7. If user has a specific request, proceed with it (context is loaded).

---

## Hard Rules

- **Read-only** — this skill never modifies any files
- **Graceful fallback** — missing files are noted in the brief, never treated as errors
- **No questions** — runs silently, does not ask the user anything
- **Progress.md capped** — only reads last 50 lines to avoid loading a huge file

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No `tasks/todo.md` | Shows "No active task — ready to start fresh" |
| No `tasks/workflow-status.md` | Shows "Workflow not started" for Step field |
| No `tasks/progress.md` | Shows "No progress logged yet" for Last done |
| No `tasks/findings.md` | Shows "none" for Open Qs |
| No `tasks/lessons.md` | Shows "0 active" for Lessons |
| No `docs/decisions.md` | Shows "no decisions log yet" — no error |
| No `docs/vision.md` | Shows "no vision.md found" — no error |
| No `tasks/tech-debt.md` | Shows "none logged" for Tech Debt |
| `tasks/tech-debt.md` exists, 0 unresolved | Shows "none" for Tech Debt |
| All checkboxes done in todo.md | Shows "Task complete — 0 pending" |
| No `>> next <<` in workflow-status.md | Shows "Workflow complete" or "Not started" |

---

## Error States

| Condition | Behavior |
|-----------|----------|
| Git not available | Branch field shows "unknown" |
| File read error (not ENOENT) | Treat as missing — use fallback value |

---

## UI/UX Behavior

### CLI Output

Two-part output:
1. **SESSION BRIEF box** — formatted with Unicode box-drawing characters
2. **Active lessons** — bulleted list of prevention rules
3. **Next step** — one line with the command to run

### When Done

The skill transitions directly to the user's request if they have one, or suggests the next workflow step.

---

## Platform Notes

CLI tool — no mobile or web platform. Works in any project that uses ShipKit's `tasks/` file structure.

---

## Related Docs

- `skills/sk:context/SKILL.md` — full implementation spec and model routing
- `tasks/todo.md` — primary data source for task and progress info
- `tasks/workflow-status.md` — primary data source for workflow step status
- `tasks/lessons.md` — loaded in full and applied as session constraints
- `docs/decisions.md` — ADR log (created by sk:brainstorming)
- `docs/vision.md` — product context (created by sk:mvp Step 9)
