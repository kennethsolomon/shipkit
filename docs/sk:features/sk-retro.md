# /sk:retro

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone (run after step 19 or step 21)
> **Command:** `/sk:retro`
> **Skill file:** `skills/sk:retro/SKILL.md`

---

## Overview

Post-ship retrospective that analyzes completed work to generate actionable improvements. Gathers data from task files and git history, calculates velocity and gate performance metrics, identifies recurring patterns, and writes a structured retro report with 3-5 concrete action items.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `tasks/todo.md` | Planned tasks — total, completed, dropped | Yes |
| `tasks/progress.md` | Work log — errors, resolutions, timestamps | Yes |
| `tasks/workflow-status.md` | Step status — attempt counts, skip reasons | Yes |
| `tasks/findings.md` | Design decisions — validation status | No |
| `tasks/lessons.md` | Lessons added during this task | No |
| `tasks/tech-debt.md` | Tech debt logged during gates | No |
| `tasks/retro-*.md` | Previous retro reports — follow-up tracking | No |
| Git log (`main..HEAD`) | Commits, time span, files changed | Yes |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Retrospective report | `tasks/retro-YYYY-MM-DD.md` | New file per retro, never overwritten |
| Summary line | Terminal (stdout) | Completion rate, velocity, top action item |

---

## Business Logic

1. **Gather data** — read all task files (`todo.md`, `progress.md`, `workflow-status.md`, `findings.md`, `lessons.md`, `tech-debt.md`).
2. **Analyze git history** — extract commits on branch, time span (first to last commit), files changed with insertions/deletions, total commit count.
3. **Calculate metrics**:
   - Completion rate: completed / planned * 100
   - Velocity: commits per day, files changed per day
   - Gate performance: attempt counts from workflow-status.md notes
   - Blocker count: occurrences of "FAIL", "error", "blocked", "3-Strike" in progress.md
   - Rework rate: fix commits vs. feature commits
4. **Identify patterns** — recurring blockers, estimation accuracy, gate friction (which gates needed most fix cycles), previous retro follow-up status.
5. **Generate action items** — produce 3-5 concrete improvements, each with what/why/when. Prioritize systemic fixes over one-off patches. Flag unaddressed items from previous retros.
6. **Write report** — save to `tasks/retro-YYYY-MM-DD.md` with sections: Metrics, What Went Well, What Didn't Go Well, Patterns, Action Items, Previous Action Item Follow-Up.
7. **Output summary** — print completion rate, velocity, blocker count, and top action item.

---

## Hard Rules

- Every observation must be data-backed — no speculation without evidence from task files or git history
- Action items must have all three components: what, why, when
- Previous retro action items must be explicitly followed up — addressed or still open
- Report is always written as a new file; never overwrites previous retros
- Prioritize systemic fixes over one-off patches

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No commits on branch | Report "no work detected on this branch" — metrics are all zero |
| `tasks/progress.md` missing | Skip blocker analysis; note data gap in report |
| No previous retro files | Skip "Previous Action Item Follow-Up" section |
| Single-commit branch | Velocity is N/A (no time span); note in report |
| All gates passed first try | Highlight in "What Went Well" — gate performance is clean |

---

## Error States

| Condition | Error message / behavior |
|-----------|--------------------------|
| `tasks/todo.md` not found | Stop with: "No plan found — cannot generate retrospective without task data" |
| Not on a feature branch | Warn: "Running retro on main — git analysis compares against HEAD~N instead of main..HEAD" |
| Git history unavailable | Stop with git error context |

---

## UI/UX Behavior

### CLI Output
Prints a one-line summary after writing the report.

### When Done
```
Retrospective saved to tasks/retro-YYYY-MM-DD.md
Completion: X/N tasks (Y%)  |  Velocity: Z commits/day  |  Blockers: K
Top action: [most important action item]
```

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:retro/SKILL.md` — full implementation spec
- `/sk:finish-feature` — typically run before retro
- `/sk:release` — alternative trigger point for retro
- `/sk:scope-check` — cross-referenced for estimation accuracy analysis
