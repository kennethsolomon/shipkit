# Lessons Learned

Accumulated patterns from past bugs and corrections. Read this file at the **start of any task** and apply all active lessons before proceeding. Add a new entry whenever a recurrent mistake is identified.

## Entry Format

```markdown
### [YYYY-MM-DD] [Brief title]
**Bug:** What went wrong (symptom)
**Root cause:** Why it happened
**Prevention:** What to do differently next time
```

## Active Lessons

<!-- Add entries here. Remove a lesson only when the root cause is permanently fixed in the codebase. -->

### [2026-03-15] Always update CLAUDE.md.template when workflow changes
**Bug:** Workflow expanded from 21 → 24 steps (added Accessibility step 5, Performance step 18, Hotfix flow, new commands `/api-design` `/accessibility` `/perf` `/hotfix`). Main `CLAUDE.md` and `README.md` were updated and pushed, but `skills/setup-claude/templates/CLAUDE.md.template` was left at the old 21-step version.
**Root cause:** Template file is separate from the live CLAUDE.md — changes to one don't automatically propagate to the other. Easy to overlook when iterating on the workflow.
**Prevention:** Any time the workflow table, step count, step numbers, tracker rules (optional steps, conditional commits, hard gates), flow line, or commands list change in `CLAUDE.md` — immediately update `skills/setup-claude/templates/CLAUDE.md.template` in the same commit. These two files must always be in sync.

