# Retrospective — 2026-04-02 — claude-mem Adaptations (v3.24.0 / v3.24.1)

## Metrics

| Metric | Value |
|--------|-------|
| Planned tasks | 2 features (progressive disclosure + auto-progress hook) |
| Completed | 2/2 + full docs + maintenance-guide expansion — 100% |
| Commits | 5 (feat, Release v3.24.0, docs fix, Release v3.24.1, chore: progress) |
| Time span | ~1 hour (single session, April 2) |
| Files changed | 13 (+439 / -107 lines) |
| Gate attempts | None (ShipKit meta-change — skill/prompt files only) |
| Blockers | 1 (.claude/hooks/ gitignored — git add failed on auto-progress.sh) |
| Rework rate | 1 fix commit (974750b — stale hook counts in setup-optimizer, maintenance-guide gaps) |
| Patterns captured | 3 new + 1 confidence bump (research-before-adapt 0.7 → 0.9) |

---

## What Went Well

- **research-before-adapt applied cleanly.** Fetched thedotmack/claude-mem, classified items (steal/install/skip) before writing any code. Two adaptations selected correctly — progressive reading (flat file compatible) and passive git logging (hook-compatible). Zero backtracking.
- **Hook deployment auto-wired via setup-optimizer.** New auto-progress.sh can reach existing project users without any manual steps — setup-optimizer Step 1.5 detects missing `.sh` files and merges `settings.json` entries additively. No user friction.
- **maintenance-guide.md gap caught and fixed mid-session.** Missing sections (skill behavior changes, hook propagation table, hook change checklist) were identified and added. Next contributor has a complete guide.
- **Non-obvious gitignore convention surfaced and captured.** `.claude/hooks/` being gitignored is easy to forget. The failed `git add` was caught immediately, root cause understood, and the pattern saved to learned/shipit/ before the session ended.
- **Version bump cadence appropriate.** Two separate releases (v3.24.0 for the feature, v3.24.1 for the docs fix) kept the changelog granular without ceremony.

---

## What Didn't Go Well

- **No tasks/todo.md — 6th consecutive retro noting this.** Plan lived in context + plan mode; `tasks/todo.md` never created. Makes `/sk:scope-check` impossible and retro task metrics thin. This is a process failure, not a one-off.
- **`npm publish` still not run — 2nd consecutive session.** `git push --tags` completes, but `npm publish` does not follow. The npm registry is now 2 minor versions behind. Action item carries from 2026-04-01.
- **`/sk:review` still not run — 4th consecutive retro.** This session touched 4 SKILL.md files and expanded maintenance-guide.md. No structured review pass. The pattern is clear: meta-changes to ShipKit skip review entirely.
- **Stale hook counts required a second commit.** `974750b` existed only to fix counts in setup-optimizer that should have been caught before the first release. A pre-release checklist would have caught this.

---

## Patterns

- **Progressive-read-over-full-dump is reusable beyond sk:context.** The pattern (read only what the output needs, defer full content on-demand via trigger words) applies to any skill that loads potentially large files before generating a summary. Confidence: 0.5 — first confirmed application.
- **Hook templates are the commitment unit, not live hooks.** Live `.claude/hooks/` files are gitignored by design — templates in `skills/sk:setup-claude/templates/hooks/` are the canonical artifact. A new developer on the project would not know this without the maintenance-guide.
- **research-before-adapt is now near-certain (0.9).** Third confirmed application: wshobson/commands (deps-audit), oh-my-claudecode (7 adaptations), claude-mem (2 adaptations). In all three cases, upfront classification prevented wasted implementation work.

---

## Action Items

1. **Add `npm publish` to `/sk:release` SKILL.md** — After `git push --tags`, add `npm publish` as the final sub-step. This is the 2nd retro noting the package registry is behind the tag. Apply: immediately in the next session that touches `skills/sk:release/SKILL.md`.

2. **Add a pre-release checklist to `/sk:release`** — Scan setup-optimizer for report string counts that reference the just-released feature (hook counts, agent counts, command counts). Catches stale counts before they reach users. Apply: add as Step 0 in `skills/sk:release/SKILL.md`.

3. **Run `/sk:review` after any session touching ≥3 SKILL.md files** — This is the 4th retro noting this. Escalate from "should" to a hard checkpoint in `/sk:finish-feature`: if git diff shows ≥3 SKILL.md files changed, block finalize until review is confirmed. Apply: add to `skills/sk:finish-feature/SKILL.md`.

4. **Create tasks/todo.md before any session touching ≥3 files** — This is the 6th retro noting the same failure. Escalate from action item to CLAUDE.md Workflow Rules: "Before any session touching ≥3 files, create tasks/todo.md." Apply: add rule to `CLAUDE.md` and `skills/sk:setup-claude/templates/CLAUDE.md.template`.

---

## Previous Action Item Follow-Up

- **Escalate todo.md to CLAUDE.md rule** (from 2026-04-01, 5th occurrence) — ❌ Not done. 6th occurrence. Still an action item.
- **Run `/sk:review` after ≥3 SKILL.md changes** (from 2026-04-01, 3rd occurrence) — ❌ Not done. 4th occurrence.
- **Run `npm publish` as part of `/sk:release`** (from 2026-04-01) — ❌ Not done. 2nd occurrence. Package is 2 versions behind.
- **Read maintenance-guide.md first for structural changes** (ongoing) — ✅ Done. Expanded the guide with missing sections during this session.
