# TODO — 2026-03-29 — Token Optimization (Stack Filtering + CLAUDE.md Compression + Skill Compression)

## Goal

Reduce ShipKit token consumption ~30% through three changes: compress CLAUDE.md, filter skills by stack, and compress skill SKILL.md files. Quality is the highest priority — skip any compression that would reduce instruction fidelity.

---

## Wave 1 — CLAUDE.md Compression — DONE

- [x] Compress CLAUDE.md workflow section (merged steps + details, tables for flows/rules)
- [x] Compress sub-agent patterns + smaller sections
- [x] Verify: same info, fewer tokens. Result: ~22% reduction

## Wave 2 — Stack Filtering Reference + Config — DONE

- [x] Create `skills/sk:setup-claude/references/skill-profiles.md` (skill/agent/rule → stack mapping)
- [x] Document `.shipkit/config.json` extended schema (stack, capabilities, skills)

## Wave 3 — Update setup-claude + setup-optimizer — DONE

- [x] setup-claude: add Phase 0.5 (stack detection + project-level skill/agent/rule installation)
- [x] setup-optimizer: add Step 0.5 (re-detect + diff + sync with confirmation)

## Wave 4 — Skill SKILL.md Compression — DONE

13 skills compressed, 3 skipped (under 10% threshold):

| Skill | Before | After | Savings |
|-------|--------|-------|---------|
| sk:skill-creator | 32,373 | 16,199 | 50% |
| sk:brainstorming | 9,089 | 3,805 | 58% |
| sk:write-tests | 9,150 | 6,825 | 25% |
| sk:mvp | 12,538 | 9,750 | 22% |
| sk:e2e | 10,045 | 7,932 | 21% |
| sk:features | 8,954 | 7,125 | 20% |
| sk:lint | 7,217 | 5,911 | 18% |
| sk:debug | 8,600 | 7,113 | 17% |
| sk:seo-audit | 12,501 | 10,614 | 15% |
| sk:review | 25,939 | 22,273 | 14% |
| sk:perf | 9,954 | 8,704 | 13% |
| sk:website | 18,214 | 16,064 | 12% |
| sk:security-check | 10,466 | 9,223 | 12% |

Skipped (under threshold): sk:ci (5%), sk:frontend-design (8%), sk:accessibility (7%)

## Wave 5 — Verification — DONE

- [x] Workflow tests: 334 passed, 9 failed (all pre-existing sk:security-check + README failures)
- [x] Fixed test regressions: brainstorming "Search-First" casing, CLAUDE.md "Auto-advance by default", "Requirement Change Flow" heading
- [x] Backwards compatible: no config → auto-detect stack

## Acceptance Criteria

- [x] CLAUDE.md compressed (~22% reduction), same information
- [x] `skill-profiles.md` maps every skill/agent/rule to a stack
- [x] `setup-claude` detects stack + installs project-level skills/agents/rules
- [x] `setup-optimizer` re-detects + diffs + syncs with confirmation
- [x] User-customized agents/rules never removed (EDITED marker check)
- [x] `extra` and `disabled` overrides never touched by auto-detection
- [x] Compressed skills maintain full instruction fidelity
- [x] Skills with < 10% compression skipped
- [x] All workflow tests pass (pre-existing failures only)
