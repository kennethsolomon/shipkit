# TODO — 2026-03-16 — Workflow Enhancement: E2E, Fix & Retest Protocol, sk:features, Simplify, Dep Audit, sk:change, /sk: prefix

## Goal

Expand the 24-step workflow to 27 steps by adding E2E testing (agent-browser), wiring sk:features after finalize, folding dep audit into lint, folding simplify into review, adding the Fix & Retest Protocol across all code-producing gates, adding a dedicated sk:change section, and enforcing /sk: prefix on all command references across all 14+ affected files.

## Constraints (from lessons.md)

- Any workflow change MUST update ALL 14+ files in the same commit — see lessons.md for full list
- Never overwrite tasks/lessons.md or tasks/security-findings.md — append only
- New sk:e2e command must be added to install.sh symlinks echo block

---

## Milestone 1: New Skill + Updated Skill Files

These are all independent — run in parallel.

#### Wave 1 (parallel)

- [ ] Create `skills/sk:e2e/SKILL.md` — new hard gate E2E skill using agent-browser
  - Purpose: behavioral verification of final reviewed+secure code
  - Steps: read context (todo.md + findings.md) → detect local server → run agent-browser E2E tests written in Write Tests step → classify fixes → apply Fix & Retest Protocol for logic changes
  - Hard gate: all scenarios must pass, 0 failures
  - Fix & Retest Protocol section (same as all other gates)
  - agent-browser core flow: `agent-browser open <url>` → `agent-browser snapshot -i` → interact via @refs → assert expected state
  - Semantic locators: `find role button`, `find text "X"` — never CSS selectors
  - Model routing section (balanced = sonnet)

- [ ] Update `skills/sk:lint/SKILL.md` — add dep audit + Fix & Retest Protocol
  - After Step 4 (Run Analyzers), add new Step 5: **Dependency Audit**
    - PHP: run `composer audit` if composer.json exists
    - Node: run `npm audit --audit-level=high` if package.json exists (or `yarn audit` / `pnpm audit` if detected)
    - Python: run `pip-audit` if pyproject.toml/requirements.txt exists
    - Go/Rust: note no standard dep audit CLI, skip
    - Report findings: package name, severity, CVE, fix version
    - Block (fail) on: critical or high severity vulnerabilities with available fix
    - Warn (pass with note) on: medium/low or unfixable critical/high
  - Rename old Step 5 → Step 6 (Fix and Re-run) — add dep audit to re-run if fixed
  - Rename old Step 6 → Step 7 (Report Results) — add dep audit line to report
  - Add Fix & Retest Protocol section after Report Results:
    - Formatter auto-fixes (Pint, Prettier, gofmt, cargo fmt): never logic changes → bypass
    - Analyzer fixes (PHPStan, Rector, ESLint, ruff, golangci-lint, clippy): classify each fix
    - Logic change → trigger protocol (update tests → /sk:test → commit → re-run /sk:lint)

- [ ] Update `skills/sk:test/SKILL.md` — add Fix & Retest Protocol
  - Add section after the existing exit criteria:
  - **Fix & Retest Protocol:** If a test failure requires an implementation fix, classify the fix:
    - Bug fix that doesn't change behavior contract → fix impl, re-run /sk:test
    - Logic change (new behavior, changed contract) → update/add tests first, then fix impl, then re-run /sk:test

- [ ] Update `skills/sk:security-check/SKILL.md` — add Fix & Retest Protocol
  - Add Fix & Retest Protocol section to Next Steps:
  - When presenting a fix, classify it as style/config OR logic change
  - Logic change → must update/add unit tests → run /sk:test → commit → re-run /sk:security-check
  - Update the "loop back" instruction to include test update step for logic changes

- [ ] Update `skills/sk:perf/SKILL.md` — add Fix & Retest Protocol
  - Same as security-check: add classification + Fix & Retest Protocol to next steps
  - N+1 fixes, query changes, algorithm changes are always logic changes → trigger protocol
  - Bundle/config changes are style/config → bypass protocol

- [ ] Update `skills/sk:review/SKILL.md` — add simplify pre-step + Fix & Retest Protocol
  - Add new Step 0 (before "Read Project Context"): **Run Simplify**
    - Invoke the built-in `simplify` skill on changed files: "Review changed code for reuse, quality, and efficiency, then fix any issues found."
    - If simplify makes changes → commit those changes first with /sk:smart-commit before continuing review
    - Note: simplify runs automatically as part of /sk:review — user does not need to run it separately
  - Add Fix & Retest Protocol section to Step 11 (Next Steps):
    - When a fix is logic-level (new branch, changed data path, refactored algorithm) → update tests first
    - Logic change fix flow: update tests → /sk:test clean → commit (tests + fix) → re-run /sk:review

---

## Milestone 2: Workflow Definition Files (14 files)

All files in this milestone are independent and can be updated in parallel. All must be completed in the same commit.

#### Wave 2 (parallel — all workflow definition files)

- [ ] Update `CLAUDE.md` — master workflow reference
  - **Flow line:** `Read → Explore → Design → Accessibility → Plan → Branch → Migrate → Write Tests → Implement → Lint → Verify Tests → Security → Performance → Review → E2E Tests → Finish → Sync Features`
  - **Workflow table:** expand 24 → 27 steps:
    - Steps 1–21: same as current except rename "Lint" → "Lint + Dep Audit" (step 12) and "Review" → "Review + Simplify" (step 20), update all command refs to /sk: prefix
    - Add step 22: `E2E Tests | /sk:e2e | required | yes — all scenarios must pass`
    - Add step 23: `Commit | /sk:smart-commit | conditional (skip if E2E was clean) | no`
    - Renumber old 22 (Update) → 24, old 23 (Finalize) → 25, old 24 (Release) → 27
    - Add step 26: `Sync Features | /sk:features | required | no`
  - **Step Details:** update/add descriptions for steps 12, 20, 22, 24, 25, 26, 27
  - **Tracker Rules:**
    - Rule 3 optional steps: update to `(4, 5, 8, 18, 27)`
    - Rule 4 conditional commits: update to `(13, 15, 17, 19, 21, 23)`
    - Rule 5 hard gates: update to `(12, 14, 16, 20, 22)` — add step 22 (E2E) bullet
    - Rule 6: update hard gate list to include 22
  - **Add Fix & Retest Protocol section** (after Tracker Rules, before Tracker Reset):
    - Full protocol text from findings.md
    - Applies to steps 12, 14, 16, 18, 20, 22
    - Exception: formatter auto-fixes bypass protocol
  - **Bug Fix Flow:** update all commands to /sk: prefix
  - **Hotfix Flow:** update all commands to /sk: prefix
  - **Add Requirement Change Flow section** (after Hotfix Flow):
    - When requirements change mid-workflow, run `/sk:change`
    - Steps: assess scope → determine invalidated steps → re-enter at correct step → reset workflow-status.md
  - **TDD section:** update command refs to /sk: prefix
  - **Commands table:** add /sk: prefix to all entries; add sk:e2e, sk:features, sk:change entries; remove old entries without prefix

- [ ] Update `skills/sk:setup-claude/templates/CLAUDE.md.template` — identical changes to CLAUDE.md above

- [ ] Update `skills/sk:setup-claude/templates/tasks/workflow-status.md.template`
  - Expand from 24 → 27 rows
  - Steps 1–21: update HARD GATE notes — old gates were 12, 14, 16, 20; now add 22
  - Rename row 12: "Lint" → "Lint + Dep Audit" with HARD GATE note
  - Rename row 20: "Review" → "Review + Simplify" with HARD GATE note
  - Add row 22: `/sk:e2e | not yet | HARD GATE — all E2E scenarios must pass`
  - Add row 23: `/sk:smart-commit | not yet | conditional`
  - Renumber 22→24 (Update Task), 23→25 (Finalize), 24→27 (Release)
  - Add row 26: `/sk:features | not yet | required — sync feature specs after ship`

- [ ] Update `README.md` — workflow table section
  - Update step count reference (24 → 27)
  - Update flow line
  - Update workflow table to match new 27 steps with /sk: prefix
  - Update Bug Fix Flow and Hotfix Flow command refs to /sk: prefix
  - Mention Fix & Retest Protocol briefly

- [ ] Update `skills/sk:setup-optimizer/SKILL.md`
  - Update step count: "24 steps" → "27 steps"
  - Update flow line string
  - Update hard gate numbers: `(12, 14, 16, 20)` → `(12, 14, 16, 20, 22)`
  - Update optional steps list: add 27 (Release), ensure 18 still listed
  - Update any command refs to /sk: prefix

- [ ] Update `install.sh`
  - Add agent-browser mandatory install block after the symlink section:
    ```
    echo "Installing agent-browser (E2E testing, ~100MB Chrome download)..."
    npm install -g agent-browser
    agent-browser install
    ```
  - Note: skills/sk:e2e is auto-discovered by the existing `for skill_dir in skills/*/` loop — no manual entry needed

- [ ] Update `skills/sk:setup-claude/templates/commands/brainstorm.md.template`
  - Update `**Workflow:**` breadcrumb to new flow line
  - Update any /command refs to /sk: prefix

- [ ] Update `skills/sk:setup-claude/templates/commands/write-plan.md.template`
  - Update `**Workflow:**` breadcrumb to new flow line
  - Update any /command refs to /sk: prefix

- [ ] Update `skills/sk:setup-claude/templates/commands/execute-plan.md.template`
  - Update `**Workflow:**` breadcrumb to new flow line
  - Update any /command refs to /sk: prefix

- [ ] Update `skills/sk:setup-claude/templates/commands/security-check.md.template`
  - Update `**Workflow:**` breadcrumb to new flow line
  - Update any /command refs to /sk: prefix

- [ ] Update `skills/sk:setup-claude/templates/commands/finish-feature.md.template`
  - Update `**Workflow:**` breadcrumb to new flow line
  - Update any /command refs to /sk: prefix

- [ ] Update `skills/sk:setup-claude/templates/commands/release.md.template`
  - Update `**Workflow:**` breadcrumb to new flow line
  - Update any /command refs to /sk: prefix

- [ ] Update `.claude/docs/DOCUMENTATION.md`
  - Update ASCII flowchart: "27 STEPS" label, add Phase for E2E Tests + Sync Features
  - Update workflow table to 27 steps with /sk: prefix
  - Update skills list: add sk:e2e entry
  - Update commands table: /sk: prefix on all entries, add sk:e2e, sk:features, sk:change
  - Update hard gate list: add step 22 (E2E)
  - Add Fix & Retest Protocol to the workflow rules section

---

## Milestone 3: Changelog + Lessons Update

#### Wave 3 (depends on Wave 2 being complete)

- [ ] Update `CHANGELOG.md` — add v3.1.0 or next patch entry
  - Workflow expanded: 24 → 27 steps
  - New: sk:e2e skill (agent-browser E2E hard gate at step 22)
  - New: Fix & Retest Protocol (steps 12, 14, 16, 18, 20, 22)
  - New: Sync Features step (step 26, after finalize)
  - New: Requirement Change Flow section (sk:change)
  - Enhanced: sk:lint now includes dependency audit
  - Enhanced: sk:review now runs simplify as pre-step
  - Convention: all command references now use /sk: prefix

- [ ] Update `tasks/lessons.md` — append new entry (never overwrite)
  - Entry: "2026-03-16: sk: prefix convention — all commands must use /sk: prefix"
  - Update existing "Update ALL 6 files" entry to reflect the full 14+ file list including sk:e2e

---

## Verification

```bash
# Confirm new skill exists
ls skills/sk:e2e/SKILL.md

# Confirm no bare /command refs remain (without sk: prefix) in workflow files
grep -r "run \`/brainstorm\`\|run \`/lint\`\|run \`/test\`\|run \`/review\`" CLAUDE.md

# Confirm all 27 steps present in workflow table
grep -c "^|" CLAUDE.md  # should include 27 data rows in workflow table

# Confirm Fix & Retest Protocol present in all gate skill files
grep -l "Fix & Retest" skills/sk:lint/SKILL.md skills/sk:test/SKILL.md skills/sk:security-check/SKILL.md skills/sk:perf/SKILL.md skills/sk:review/SKILL.md skills/sk:e2e/SKILL.md

# Confirm dep audit in lint
grep "composer audit\|npm audit" skills/sk:lint/SKILL.md

# Confirm simplify in review
grep -i "simplify" skills/sk:review/SKILL.md

# Confirm agent-browser in install.sh
grep "agent-browser" install.sh

# Confirm CLAUDE.md.template matches CLAUDE.md step count
grep -c "^|" skills/sk:setup-claude/templates/CLAUDE.md.template

# Confirm workflow-status.md.template has 27 rows
grep -c "not yet" skills/sk:setup-claude/templates/tasks/workflow-status.md.template
```

## Acceptance Criteria

- [ ] 27-step workflow table present and consistent across CLAUDE.md, CLAUDE.md.template, README.md, DOCUMENTATION.md
- [ ] workflow-status.md.template has 27 rows with correct HARD GATE annotations (steps 12, 14, 16, 20, 22)
- [ ] skills/sk:e2e/SKILL.md exists and documents agent-browser usage, hard gate behavior, Fix & Retest Protocol
- [ ] Fix & Retest Protocol present in all 6 code-producing gate skills (lint, test, security, perf, review, e2e)
- [ ] Dep audit (composer audit / npm audit) present in sk:lint
- [ ] Simplify pre-step present in sk:review
- [ ] agent-browser install present in install.sh
- [ ] All /command refs use /sk: prefix in CLAUDE.md, templates, README, DOCUMENTATION
- [ ] Requirement Change Flow section present in CLAUDE.md with /sk:change command
- [ ] CHANGELOG.md updated
- [ ] tasks/lessons.md updated with /sk: prefix convention (appended, not overwritten)

## Risks/Unknowns

- agent-browser requires Chrome download (~100MB) — already noted in install.sh task above
- workflow-status.md.template hard gate step numbers must match CLAUDE.md exactly — easy to mismatch during renumbering, verify with grep after
