# Retrospective — 2026-04-02 — agent-browser + Retro Action Item Fixes (v3.25.0)

## Metrics

| Metric | Value |
|--------|-------|
| Planned tasks | None (no tasks/todo.md — session started from user question + retro action items) |
| Completed | 5 items: 3 retro fixes + agent-browser integration + maintenance-guide update |
| Commits | 6 (fix, feat, docs, chore: docs, chore: Release v3.25.0, chore: docs) |
| Time span | ~1.5 hours (09:10 → 10:35, April 2) |
| Files changed | 9 across 3 substantive commits (+76 / -19 lines) |
| Gate attempts | None (ShipKit meta-change — skill/prompt files only) |
| Blockers | 0 |
| Rework rate | 0% |
| Patterns captured | 2 new (retro-action-to-rule-escalation, community-plugin-two-subtypes) |

---

## What Went Well

- **All 3 retro action items closed in the same session they were escalated.** todo.md rule, /sk:review gate, npm publish — each converted from repeated retro note to enforced mechanism. The `retro-action-to-rule-escalation` pattern worked exactly as described: ≥3x recurrence = fix the system, not the habit.
- **research-before-adapt applied cleanly to agent-browser.** Fetched the repo, classified (CLI tool, not Claude plugin), found it was already partially integrated in sk:e2e before touching anything. Read first prevented duplication.
- **maintenance-guide gap caught mid-integration.** The existing "community plugin" pattern assumed Claude plugins — agent-browser exposed the gap. Extended the guide with a CLI tool sub-type rather than bodging the existing section. Future contributors now have both patterns documented.
- **Correct priority order in sk:e2e.** The priority flip (Playwright CLI when specs exist → agent-browser for interactive) is architecturally sound: existing test infrastructure is preserved, new projects get the token-efficient path by default.
- **tasks/todo.md rule now enforced in CLAUDE.md AND CLAUDE.md.template.** Previous sessions updated CLAUDE.md but forgot the template. This session updated both, consistent with the "always update templates" memory.

---

## What Didn't Go Well

- **No tasks/todo.md again** — the very rule we added in this session wasn't applied to this session. The rule is now in CLAUDE.md but won't retroactively fix an already-started session. First session it will take effect is the next one.
- **`/sk:review` still not run** — 5 SKILL.md files changed this session (sk:release, sk:e2e, sk:setup-claude, sk:setup-optimizer, sk:finish-feature). The new gate in /sk:finish-feature would have caught this — but we didn't run /sk:finish-feature either. Meta-change sessions skip the standard workflow entirely.
- **arch change log entry not created.** The maintenance-guide quick checklist includes "Create entry in `.claude/docs/architectural_change_log/`" after any workflow change. Two workflow changes happened this session (agent-browser integration, retro enforcement rules) — no arch log entry was created for either.

---

## Patterns

- **Rules take effect from the next session, not the current one.** Adding a rule mid-session doesn't retroactively apply it. The todo.md rule, the /sk:review gate, and the npm publish step were all added this session but couldn't be applied to this session. This is expected — just worth noting so the next session starts correctly.
- **Meta-change sessions need a lightweight checklist.** Sessions that only change ShipKit internals (no app code, no gates to run) consistently skip: arch log, /sk:review, tasks/todo.md. A "meta-change checklist" in CLAUDE.md or /sk:finish-feature would catch these without requiring the full gate suite.
- **retro-action-to-rule-escalation validated immediately.** The pattern was identified in the retro, acted on in the same session, and worked. Confidence should bump from 0.5 → 0.7 on next occurrence.

---

## Action Items

1. **Create arch change log entries for this session's changes** — Two workflow changes were made (agent-browser integration, retro enforcement rules) without arch log entries. Apply: immediately at the start of the next session before any new work.

2. **Add a "meta-change checklist" to /sk:finish-feature or CLAUDE.md** — Sessions touching only ShipKit internals consistently skip arch log, /sk:review, and tasks/todo.md. A dedicated checklist for meta-change sessions (≥3 SKILL.md or ≥3 commands/ files changed) would catch these gaps without the overhead of the full workflow. Apply: next meta-change session.

3. **Run /sk:review on the 5 SKILL.md files changed this session** — sk:release, sk:e2e, sk:setup-claude, sk:setup-optimizer, sk:finish-feature. Apply: start of next session.

---

## Previous Action Item Follow-Up

- **Add `npm publish` to `/sk:release`** (from 2026-04-02 morning, 2nd occurrence) — ✅ Done. Added as Step 7 in sk:release SKILL.md.
- **Run `/sk:review` after ≥3 SKILL.md changes** (from 2026-04-02 morning, 4th occurrence) — ✅ Enforced in /sk:finish-feature "Before You Start". Gate added. Still not run this session (meta-change — no /sk:finish-feature invoked).
- **Create tasks/todo.md before ≥3 file sessions** (from 2026-04-02 morning, 6th occurrence) — ✅ Added as CLAUDE.md rule 8 + mirrored to template. Not applied this session (rule added mid-session).
- **Add pre-release checklist to /sk:release** (from 2026-04-02 morning) — ❌ Not done. Deprioritized in favor of the 3 higher-urgency fixes.
