# 2026-04-01 — oh-my-claudecode Adaptations

## Summary

7 improvements adapted from oh-my-claudecode (19k stars). No workflow step order changed — all additions are either new optional pre-steps, internal mechanic upgrades, or config additions.

---

## Changes

### 1. Native Agent Teams
**File:** `.claude/settings.json`, `skills/sk:setup-claude/templates/.claude/settings.json.template`
**Change:** Added `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` to `env` — enables native Claude Code team spawning for `/sk:team`.

### 2. Magic Keyword Hook
**Files:** `.claude/hooks/keyword-router.sh`, `.claude/settings.json`
**Change:** New `UserPromptSubmit` hook. Keywords `autopilot:`, `debug:`, `fast:`, `interview:`, `team:` inject routing context. Claude invokes the corresponding skill automatically.

### 3. New Skill: `/sk:deep-interview`
**Files:** `skills/sk:deep-interview/SKILL.md`, `commands/sk/deep-interview.md`, `docs/sk:features/sk-deep-interview.md`
**Change:** Socratic requirements-gathering with mathematical ambiguity scoring (4 weighted dimensions, ≤20% gate). Outputs `tasks/spec.md`. Auto-invoked by start/autopilot for vague tasks.

### 4. Autopilot + Start Auto-Routing
**Files:** `skills/sk:autopilot/SKILL.md`, `skills/sk:start/SKILL.md`
**Change:**
- Autopilot gains Step 0 (task classification): Check A (unknown bug → deep-dive), Check B (vague feature → deep-interview), Check C (clear → skip)
- Start gains deep-dive flow detection (bug + no known cause), vague-feature flagging, and routing to deep-interview for manual mode
- Autopilot direction approval now includes explicit acceptance criteria
- Autopilot gains Step 7.5: verify all acceptance criteria before PR push

### 5. New Skill: `/sk:deep-dive`
**Files:** `skills/sk:deep-dive/SKILL.md`, `commands/sk/deep-dive.md`, `docs/sk:features/sk-deep-dive.md`
**Change:** Two-stage pipeline for unknown-cause bugs: 3 parallel trace lanes (git history, code structure, runtime behavior) → pre-seeded deep interview → `tasks/spec.md` with root cause. Replaces manual `/sk:debug` for investigation-heavy cases.

### 6. Auto-Consensus in `/sk:write-plan`
**Files:** `commands/sk/write-plan.md`, `skills/sk:setup-claude/templates/commands/write-plan.md.template`
**Change:** write-plan auto-detects high-risk keywords (auth, migration, payment, breaking change, deploy, credentials) and runs Architect + Critic review loop before user approval. `--consensus` forces it; `--no-consensus` skips it.

### 7. ultraqa Cycling in Test + Gates
**Files:** `skills/sk:test/SKILL.md`, `skills/sk:gates/SKILL.md`
**Change:** Replaced blind retry loops with 3-cycle architect-diagnosed cycling. Same-failure detection (first 30 chars): if identical across 2 attempts, triggers architect diagnosis immediately instead of waiting for attempt 3.

---

## Files Updated (Documentation + Templates)

- `CLAUDE.md` — step 0, debug alt-flow, commands table
- `commands/sk/help.md` — workflow table, bug fix table, all commands
- `skills/sk:brainstorming/SKILL.md` — reads tasks/spec.md in step 1
- `skills/sk:setup-claude/templates/CLAUDE.md.template` — step 0
- `skills/sk:setup-claude/templates/.claude/settings.json.template` — env + hook
- `skills/sk:setup-claude/templates/commands/brainstorm.md.template` — spec.md reading
- `skills/sk:setup-claude/templates/hooks/keyword-router.sh` — new template
- `docs/FEATURES.md` — deep-interview + deep-dive entries
- `.claude/docs/maintenance-guide.md` — step count updated

---

## Design Decisions

**Why auto-detect rather than manual flags?**
The user's primary entry point is `/sk:start` (80%) and `/sk:autopilot`. Requiring manual flags creates friction and means the improvements only help when remembered. Detection-at-classification is zero-ceremony.

**Why is deep-interview optional (step 0) rather than replacing brainstorm?**
Brainstorm explores HOW to implement (codebase research, approach proposals). Deep-interview clarifies WHAT the user wants. They're complementary. For clear tasks, brainstorm is sufficient. For vague tasks, deep-interview runs first.

**Why threshold 25% for deep-dive vs 20% for deep-interview?**
The trace stage already reduces uncertainty significantly. The interview starts with more context, so a slightly looser gate is appropriate.
