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
14. `.claude/docs/DOCUMENTATION.md` — internal docs with full workflow diagram, recommended workflow table, skills list, and scenario tables



### [2026-03-16] All commands must use /sk: prefix
**Bug:** CLAUDE.md and all workflow templates documented commands without the /sk: prefix (e.g. `/brainstorm`, `/lint`, `/review`) even though the actual skills use `sk:` in their directory names. This caused ambiguity about whether commands come from this plugin or Claude Code builtins.
**Root cause:** The /sk: prefix convention was not established when the workflow was first documented.
**Prevention:** All user-facing commands from this plugin must use the `/sk:` prefix. When adding new commands, always document them as `/sk:<name>`. When updating workflow files, ensure all command references use `/sk:` prefix. This applies to: CLAUDE.md, CLAUDE.md.template, README.md, DOCUMENTATION.md, all SKILL.md files, all command templates.

### [2026-03-16] Update ALL 14+ files when the workflow changes (expanded list)
**Bug:** The previous "Update ALL 6 files" lesson was incomplete — it missed the sk:e2e skill file and the /sk: prefix convention. As of the 27-step workflow, more files are involved.
**Root cause:** The file list in the lesson was not kept up to date as the project grew.
**Prevention:** The complete list of files to update when the workflow changes (step count, flow line, step names, commands list) is now:
1. `CLAUDE.md`
2. `skills/sk:setup-claude/templates/CLAUDE.md.template`
3. `skills/sk:setup-claude/templates/tasks/workflow-status.md.template`
4. `README.md`
5. `skills/sk:setup-optimizer/SKILL.md`
6. `CHANGELOG.md`
7. `install.sh` (if new commands added)
8. `skills/sk:setup-claude/templates/commands/brainstorm.md.template`
9. `skills/sk:setup-claude/templates/commands/write-plan.md.template`
10. `skills/sk:setup-claude/templates/commands/execute-plan.md.template`
11. `skills/sk:setup-claude/templates/commands/security-check.md.template`
12. `skills/sk:setup-claude/templates/commands/finish-feature.md.template`
13. `.claude/docs/DOCUMENTATION.md`
Additionally, if new gate skills are added (like sk:e2e):
14. Add Fix & Retest Protocol to the new skill's SKILL.md
15. Reference the new skill in `tasks/lessons.md` (this file)

### [2026-03-16] sk:seo-audit — update its docs when the skill changes
**Bug:** New standalone skill added (sk:seo-audit) without updating the "update ALL files" lesson to include it.
**Root cause:** The lesson list wasn't updated when the new skill was created.
**Prevention:** When sk:seo-audit changes (skill behavior, output format, phases), update ALL 5 of these files in the same commit:
1. `skills/sk:seo-audit/SKILL.md` — the skill itself
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `install.sh` — commands echo block

### [2026-03-19] sk:context — update its docs when the skill changes
**Bug:** New standalone skill added (sk:context) without tracking which files need updating.
**Root cause:** The lesson list wasn't updated when the new skill was created.
**Prevention:** When sk:context changes (skill behavior, output format, files read), update ALL of these files in the same commit:
1. `skills/sk:context/SKILL.md` — the skill itself
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `install.sh` — commands echo block
6. `skills/sk:setup-claude/templates/CLAUDE.md.template` — template for new projects

### [2026-03-19] sk:dashboard — update its docs when the skill changes
**Bug:** New standalone skill added (sk:dashboard) without updating the "update ALL files" lesson to include it.
**Root cause:** The lesson list wasn't updated when the new skill was created.
**Prevention:** When sk:dashboard changes (skill behavior, server.js, dashboard.html), update ALL 5 of these files in the same commit:
1. `skills/sk:dashboard/SKILL.md` — the skill itself
2. `skills/sk:dashboard/server.js` — the server
3. `skills/sk:dashboard/dashboard.html` — the UI
4. `CLAUDE.md` — commands table
5. `README.md` — commands section
6. `.claude/docs/DOCUMENTATION.md` — skills section
7. `install.sh` — commands echo block

### [2026-03-20] tech-debt.md — update gate skills when logging format changes
**Bug:** New tech-debt.md logging format introduced without a tracking entry.
**Root cause:** No lesson existed to track which files depend on the tech-debt.md format.
**Prevention:** When the tech-debt.md entry format changes, update ALL of these files in the same commit:
1. `skills/sk:lint/SKILL.md`
2. `skills/sk:test/SKILL.md`
3. `commands/sk/security-check.md`
4. `skills/sk:perf/SKILL.md`
5. `skills/sk:review/SKILL.md`
6. `skills/sk:e2e/SKILL.md`
7. `skills/sk:context/SKILL.md`
8. `commands/sk/write-plan.md`
9. `commands/sk/update-task.md`

### [2026-03-23] New skills — update docs when any of these skills change
**Bug:** 5 new skills added without tracking entries for dependent files.
**Root cause:** Lesson list not updated when new skills were created.
**Prevention:** When any of these skills change, update ALL listed files in the same commit:

**sk:scope-check:**
1. `skills/sk:scope-check/SKILL.md`
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `docs/sk:features/sk-scope-check.md` — feature spec

**sk:retro:**
1. `skills/sk:retro/SKILL.md`
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `docs/sk:features/sk-retro.md` — feature spec

**sk:reverse-doc:**
1. `skills/sk:reverse-doc/SKILL.md`
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `docs/sk:features/sk-reverse-doc.md` — feature spec

**sk:gates:**
1. `skills/sk:gates/SKILL.md`
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `docs/sk:features/sk-gates.md` — feature spec
6. All 5 agent definitions in `skills/sk:setup-claude/templates/.claude/agents/`

**sk:fast-track:**
1. `skills/sk:fast-track/SKILL.md`
2. `CLAUDE.md` — commands table
3. `README.md` — commands section
4. `.claude/docs/DOCUMENTATION.md` — skills section
5. `docs/sk:features/sk-fast-track.md` — feature spec

**Hooks & infrastructure:**
When hook behavior or settings.json format changes, update:
1. All 6 hook scripts in `skills/sk:setup-claude/templates/hooks/`
2. `skills/sk:setup-claude/templates/.claude/settings.json.template`
3. `skills/sk:setup-claude/scripts/apply_setup_claude.py`
4. `skills/sk:setup-claude/SKILL.md`
5. `install.sh` — commands echo block

### [2026-03-23] New skills (batch 2) — update docs when any of these skills change
**Bug:** 3 new skills added without tracking entries for dependent files.
**Root cause:** Lesson list not updated when new skills were created.
**Prevention:** When any of these skills change, update ALL listed files in the same commit:

**sk:start:**
1. `skills/sk:start/SKILL.md`
2. `commands/sk/start.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section

**sk:autopilot:**
1. `skills/sk:autopilot/SKILL.md`
2. `commands/sk/autopilot.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section

**sk:team:**
1. `skills/sk:team/SKILL.md`
2. `commands/sk/team.md`
3. 3 agent templates in `skills/sk:setup-claude/templates/.claude/agents/` (backend-dev.md, frontend-dev.md, qa-engineer.md)
4. `CLAUDE.md` — commands table
5. `README.md` — commands section
6. `.claude/docs/DOCUMENTATION.md` — skills section

**Auto-skip intelligence:**
1. `CLAUDE.md` — workflow tracker rules section
2. `skills/sk:setup-claude/templates/CLAUDE.md.template` — same rules
3. `skills/sk:setup-optimizer/SKILL.md` — auto-skip detection reference

### [2026-03-25] New skills (batch 3 — ECC intelligence) — update docs when any of these skills change
**Bug:** 7 new skills added as part of ECC intelligence upgrade.
**Root cause:** New skills need tracking entries for dependent files.
**Prevention:** When any of these skills change, update ALL listed files in the same commit:

**sk:learn:**
1. `skills/sk:learn/SKILL.md`
2. `commands/sk/learn.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section
6. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**sk:context-budget:**
1. `skills/sk:context-budget/SKILL.md`
2. `commands/sk/context-budget.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section
6. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**sk:health:**
1. `skills/sk:health/SKILL.md`
2. `commands/sk/health.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section
6. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**sk:save-session:**
1. `skills/sk:save-session/SKILL.md`
2. `commands/sk/save-session.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section
6. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**sk:resume-session:**
1. `skills/sk:resume-session/SKILL.md`
2. `commands/sk/resume-session.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section
6. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**sk:safety-guard:**
1. `skills/sk:safety-guard/SKILL.md`
2. `commands/sk/safety-guard.md`
3. `skills/sk:setup-claude/templates/hooks/safety-guard.sh`
4. `CLAUDE.md` — commands table
5. `README.md` — commands section
6. `.claude/docs/DOCUMENTATION.md` — skills section
7. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**sk:eval:**
1. `skills/sk:eval/SKILL.md`
2. `commands/sk/eval.md`
3. `CLAUDE.md` — commands table
4. `README.md` — commands section
5. `.claude/docs/DOCUMENTATION.md` — skills section
6. `skills/sk:setup-claude/templates/CLAUDE.md.template`

**Enhanced hooks:**
When enhanced hook behavior changes, update:
1. All 6 enhanced hook scripts in `skills/sk:setup-claude/templates/hooks/`
2. `skills/sk:setup-claude/templates/.claude/settings.json.template`
3. `skills/sk:setup-claude/SKILL.md`
4. `skills/sk:setup-optimizer/SKILL.md`
