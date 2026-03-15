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

### [2026-03-15] Update ALL 6 files when the workflow changes
**Bug:** Workflow expanded from 21 → 24 steps. `CLAUDE.md` and `README.md` were updated first, but `CLAUDE.md.template`, `workflow-status.md.template`, and `setup-optimizer/SKILL.md` were left stale — discovered only in a follow-up audit.
**Root cause:** Workflow definition is duplicated across 6 files. Changing one does not propagate to the others.
**Prevention:** Any time the workflow changes (step count, step numbers, flow line, tracker rules, commands list) — update ALL 6 files in the same commit:
1. `CLAUDE.md` — live workflow reference
2. `skills/setup-claude/templates/CLAUDE.md.template` — template for new projects
3. `skills/setup-claude/templates/tasks/workflow-status.md.template` — tracker template for new projects
4. `README.md` — workflow table in docs
5. `skills/setup-optimizer/SKILL.md` — embeds step count, flow line, and hard gate numbers
6. `CHANGELOG.md` — document what changed

**Additionally, if new commands are added:**
7. `install.sh` — the "Workflow commands:" echo block lists every available command

**Additionally, if the flow line or step names change:**
8. `skills/setup-claude/templates/commands/brainstorm.md.template` — has a `**Workflow:**` breadcrumb line
9. `skills/setup-claude/templates/commands/write-plan.md.template` — has a `**Workflow:**` breadcrumb line
10. `skills/setup-claude/templates/commands/execute-plan.md.template` — has a `**Workflow:**` breadcrumb line
11. `skills/setup-claude/templates/commands/security-check.md.template` — has a `**Workflow:**` breadcrumb line
12. `skills/setup-claude/templates/commands/finish-feature.md.template` — has a `**Workflow:**` breadcrumb line
13. `skills/setup-claude/templates/commands/release.md.template` — has a `**Workflow:**` breadcrumb line

