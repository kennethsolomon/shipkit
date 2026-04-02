# 2026-04-02 — Retro Action Item Enforcement Rules

## Summary

Three recurring retro action items (noted 2–6× each without resolution) converted from habits to enforced mechanisms. No workflow step order changed — these are internal enforcement upgrades to existing steps.

---

## Changes

### 1. tasks/todo.md — CLAUDE.md Rule 8

**Files:** `CLAUDE.md`, `skills/sk:setup-claude/templates/CLAUDE.md.template`

**Before:** Recurring retro action item — "create tasks/todo.md before any session touching ≥3 files." Noted 6 consecutive times, never acted on.

**After:** Rule 8 added to Workflow Rules:
> "**todo.md required** — before any session touching ≥ 3 files, create `tasks/todo.md` with at least 5 checkboxes. No todo.md = no `/sk:scope-check`, no retro task metrics."

Mirrored to `CLAUDE.md.template` so new projects bootstrapped by `/sk:setup-claude` inherit the rule.

**Why a rule and not a gate:** No automated enforcement is possible without a hook that counts modified files before a session starts. A documented rule + retro accountability is the correct enforcement level for a session-start behavior.

---

### 2. /sk:review gate in /sk:finish-feature

**File:** `commands/sk/finish-feature.md`

**Before:** Recurring retro action item — "run /sk:review after ≥3 SKILL.md changes." Noted 4 consecutive times, never acted on.

**After:** "Before You Start" section now includes:

```bash
git diff main..HEAD --name-only | grep -c 'SKILL\.md' || true
```

If count ≥ 3 and `/sk:review` hasn't been run this session → stop and run it before proceeding. Hard block, not a recommendation.

**Why /sk:finish-feature and not /sk:gates:** Gates run app-level quality checks (lint, test, security). SKILL.md cross-cutting review is a meta-level concern — it belongs at the finalize step where structural completeness is assessed, not alongside code quality gates.

---

### 3. npm publish in /sk:release

**File:** `skills/sk:release/SKILL.md`

**Before:** Recurring retro action item — "npm publish after git push --tags." Noted 2 consecutive times; npm registry was 2 versions behind GitHub.

**After:** Step 7 added to Standard Git Release flow:
- Checks for `package.json` with a `name` field
- Runs `npm publish` (or `npm publish --access public` for scoped packages)
- Skips if `"private": true`

**Why Step 7 (not a separate step):** It's part of the same release action — version bumped, tag pushed, package published. Splitting it out would imply it's optional or separable. It isn't for a public npm package.

---

## Files Updated

- `CLAUDE.md` — rule 8 added to Workflow Rules
- `skills/sk:setup-claude/templates/CLAUDE.md.template` — rule 8 mirrored
- `commands/sk/finish-feature.md` — /sk:review gate added to "Before You Start"
- `skills/sk:release/SKILL.md` — npm publish as Step 7

---

## Pattern

All three fixes followed the `retro-action-to-rule-escalation` pattern: items that recurred ≥3 times without resolution were converted from habits to enforcement mechanisms in the same session the pattern was identified. The pattern itself was then saved to `~/.claude/skills/learned/shipit/retro-action-to-rule-escalation.md`.
