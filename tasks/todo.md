# TODO — 2026-03-28 — ShipKit Infrastructure Upgrade (Audit Fixes + New Capabilities)

## Goal

Apply all 9 improvements identified in the Claude Code capability audit: fix 2 bugs, upgrade all skill frontmatter, create formal agent definitions, add path-scoped rules, and ship 2 new skills (sk:ci, sk:plugin).

## Constraints (from lessons.md)
- When new skills are added → update CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, lessons.md
- When gate skills change → update tech-debt.md gate skills list (lessons.md §2026-03-20)
- All commands must use /sk: prefix
- When hook/settings.json format changes → update setup-claude templates

---

## Wave 1 — Bug Fixes + Frontmatter (parallel, no dependencies)

- [ ] Fix `allowed_tools` → `allowed-tools` in `skills/sk:gates/SKILL.md`
- [ ] Fix `allowed_tools` → `allowed-tools` in `skills/sk:team/SKILL.md`
- [ ] Move `commands/sk/security-check.md` → `skills/sk:security-check/SKILL.md` (create dir, copy content, keep command as thin wrapper or remove)
- [ ] Add `disable-model-invocation: true` to side-effect skills: sk:smart-commit, sk:release, sk:branch, sk:finish-feature, sk:hotfix, sk:safety-guard
- [ ] Add `model: haiku` to low-complexity skills: sk:lint, sk:context, sk:health, sk:seo-audit
- [ ] Add `model: sonnet` to analysis-heavy skills: sk:review, sk:security-check, sk:perf, sk:e2e
- [ ] Add `argument-hint` to skills with arguments: sk:website (`[--revise] [URL or brief]`), sk:release (`[android|ios]`), sk:security-check (`[--all]`), sk:batch-if-exists
- [ ] Add `${CLAUDE_SKILL_DIR}` references in sk:website and sk:setup-claude for supporting file paths

## Wave 2 — context:fork on Gate Skills (depends on Wave 1 security-check migration)

- [ ] Add `context: fork` + `agent: general-purpose` to `sk:lint/SKILL.md`
- [ ] Add `context: fork` + `agent: general-purpose` to `sk:test/SKILL.md`
- [ ] Add `context: fork` + `agent: general-purpose` to `sk:security-check/SKILL.md`
- [ ] Add `context: fork` + `agent: general-purpose` to `sk:perf/SKILL.md`
- [ ] Add `context: fork` + `agent: general-purpose` to `sk:e2e/SKILL.md`
- [ ] Add `context: fork` + `agent: general-purpose` to `sk:seo-audit/SKILL.md`
- [ ] Add `context: fork` + `agent: general-purpose` to `sk:reverse-doc/SKILL.md`

## Wave 3 — Custom Agents (parallel, no dependencies)

- [ ] Create `.claude/agents/` directory
- [ ] Create `.claude/agents/backend-dev.md` — full-stack backend agent (model: sonnet, memory: project, tools: all, isolation: worktree)
- [ ] Create `.claude/agents/frontend-dev.md` — frontend agent (model: sonnet, memory: project, tools: all, isolation: worktree)
- [ ] Create `.claude/agents/qa-engineer.md` — QA/E2E agent (model: sonnet, memory: project, background: true)
- [ ] Create `.claude/agents/security-reviewer.md` — OWASP security agent (model: sonnet, tools: Read/Grep/Glob/Bash, permissionMode: dontAsk, memory: user)
- [ ] Create `.claude/agents/code-reviewer.md` — 7-dimension code review agent (model: sonnet, tools: Read/Grep/Glob/Bash, permissionMode: dontAsk)
- [ ] Create `.claude/agents/debugger.md` — structured debug specialist (model: sonnet, tools: Read/Edit/Bash/Grep/Glob)
- [ ] Update `skills/sk:team/SKILL.md` to reference the formal `.claude/agents/` definitions instead of inline agent descriptions
- [ ] Update `skills/sk:setup-claude/` templates to copy `.claude/agents/` on project setup

## Wave 4 — Path-Scoped Rules (parallel, no dependencies)

- [ ] Create `.claude/rules/laravel.md` — paths: `app/**/*.php`, `routes/**`, `config/**`
- [ ] Create `.claude/rules/react.md` — paths: `**/*.{tsx,jsx}`, `resources/js/**`
- [ ] Create `.claude/rules/vue.md` — paths: `**/*.vue`, `resources/js/**`
- [ ] Create `.claude/rules/tests.md` — paths: `tests/**`, `**/*.test.*`, `**/*.spec.*`
- [ ] Create `.claude/rules/api.md` — paths: `routes/api.php`, `app/Http/Controllers/**`, `**/controllers/**`
- [ ] Create `.claude/rules/migrations.md` — paths: `database/migrations/**`, `**/*.migration.ts`, `prisma/**`
- [ ] Update `skills/sk:setup-claude/` templates to generate `.claude/rules/` from detected stack

## Wave 5 — New Skills (parallel, no dependencies)

- [ ] Create `skills/sk:ci/SKILL.md` — GitHub Actions + GitLab CI integration skill
  - Wraps `/install-github-app` built-in
  - Provides workflow templates: PR review, issue triage, nightly audit, release automation
  - Supports AWS Bedrock + GCP Vertex AI enterprise setups
  - Generates `.github/workflows/claude.yml` or `.gitlab-ci.yml`
- [ ] Create `skills/sk:plugin/SKILL.md` — package project skills/hooks as distributable Claude Code plugin
  - Creates `.claude-plugin/plugin.json` manifest
  - Moves skills from `.claude/skills/` → `plugin-name/skills/`
  - Converts hooks from `settings.json` → `hooks/hooks.json`
  - Moves agents from `.claude/agents/` → `plugin-name/agents/`
  - Validates plugin structure
  - Generates README.md with install instructions

## Wave 6 — Documentation + Lessons (depends on all above)

- [ ] Update `CLAUDE.md` commands table — add sk:ci, sk:plugin
- [ ] Update `README.md` commands section — add sk:ci, sk:plugin
- [ ] Update `.claude/docs/DOCUMENTATION.md` — add sk:ci, sk:plugin to skills section
- [ ] Update `install.sh` — add sk:ci, sk:plugin to commands echo block
- [ ] Update `tasks/lessons.md` — add lesson entries for sk:ci, sk:plugin, new agents
- [ ] Update `tasks/lessons.md` — update tech-debt.md gate skills list to include `skills/sk:security-check/SKILL.md` (replaces `commands/sk/security-check.md`)
- [ ] Update `CHANGELOG.md` — document all changes in this task

---

## Verification

```bash
# 1. No allowed_tools (underscore) in any SKILL.md
grep -r "allowed_tools" skills/
# Expected: 0 results

# 2. security-check is now a skill
ls skills/sk:security-check/SKILL.md
# Expected: file exists

# 3. disable-model-invocation on side-effect skills
grep -l "disable-model-invocation" skills/sk:smart-commit/SKILL.md skills/sk:release/SKILL.md skills/sk:branch/SKILL.md
# Expected: all 3 listed

# 4. model routing present
grep "model:" skills/sk:lint/SKILL.md skills/sk:review/SKILL.md
# Expected: haiku and sonnet respectively

# 5. agents exist
ls .claude/agents/
# Expected: 6 .md files

# 6. rules exist
ls .claude/rules/
# Expected: 6 .md rules files

# 7. context: fork on gate skills
grep "context: fork" skills/sk:lint/SKILL.md skills/sk:test/SKILL.md skills/sk:security-check/SKILL.md
# Expected: match in all 3

# 8. new skills exist
ls skills/sk:ci/SKILL.md skills/sk:plugin/SKILL.md
# Expected: both exist

# 9. workflow tests still pass
bash tests/verify-workflow.sh
# Expected: all tests pass
```

## Acceptance Criteria

- [ ] Zero `allowed_tools` (underscore) references in skills/
- [ ] `sk:security-check` lives in `skills/sk:security-check/SKILL.md`
- [ ] All 6 side-effect skills have `disable-model-invocation: true`
- [ ] Gate skills (lint, test, security, perf, e2e) have `model` + `context: fork`
- [ ] `.claude/agents/` has 6 agent definitions with memory, model, tools specified
- [ ] `.claude/rules/` has 6 path-scoped rule files
- [ ] `sk:ci` and `sk:plugin` skills exist and are documented
- [ ] All 267 existing tests still pass
- [ ] CLAUDE.md, README.md, DOCUMENTATION.md, install.sh updated with new skills

## Risks / Unknowns

- `context: fork` on gate skills changes invocation behavior — when run standalone, they'll execute in a subagent context. Need to verify this doesn't break sk:gates (which already forks them via Agent tool). May need to remove `context: fork` from gate skills if sk:gates already handles forking.
- `.claude/agents/` agent definitions for backend-dev/frontend-dev/qa-engineer must be compatible with the approach in `skills/sk:team/SKILL.md` — need to read sk:team current implementation before writing agents.
- `sk:security-check` migration: thin wrapper in `commands/sk/security-check.md` should remain for backwards compat — users may have it in muscle memory.
