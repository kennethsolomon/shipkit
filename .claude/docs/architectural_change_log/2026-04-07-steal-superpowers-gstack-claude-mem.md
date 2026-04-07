# Steal Adaptations: Respond-Review, Investigate, Private Memory, Claude PR Action

**Date:** 2026-04-07
**Source:** [obra/superpowers](https://github.com/obra/superpowers) + [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) + [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) + [garrytan/gstack](https://github.com/garrytan/gstack)
**Scope:** Cross-cutting (workflow, gates, CLAUDE.md, CI, privacy convention)

---

## Changes

### 1. `/sk:respond-review` — Review Finding Triage (from superpowers)

- **What:** New skill + command that triages `/sk:review` findings into fix-now / defer / dispute buckets.
- **Why:** Without triage, every Critical or Warning finding blocked gates equally, causing churn on cosmetic or cross-file refactor suggestions. Superpowers' review-loop shows triage first, fix second.
- **Impact:**
  - Conservative default: `fix-now > defer > dispute`
  - `fix-now`: Critical findings, Warnings in safety paths (auth/payments/PII), localized (<10 lines) fixes
  - `defer`: Cross-file refactors or non-safety suggestions → logged to `tasks/tech-debt.md`
  - `dispute`: Reviewer misread, or contradicts a prior decision → logged to `tasks/review-disputes.md`
  - One squash commit per triage batch; returns `READY_TO_RERUN` or `BLOCKED`
  - Same-finding escalation: architect agent on 2nd survival, 3-strike on 3rd
  - **Auto-invoked by `/sk:gates` Batch 3** when review returns any Critical/Warning — keeps gates as single source of re-run logic
  - Can also be invoked manually after a standalone `/sk:review`

### 2. `/sk:investigate` — Read-Only Feature-Area Exploration (from gstack)

- **What:** New skill + command that maps an unfamiliar brownfield subsystem before brainstorm. HARD-GATE: no code changes, writes only `tasks/investigation.md`.
- **Why:** `/sk:brainstorm` assumed the user already had enough context. For unfamiliar areas ("the billing module", "our webhook system"), brainstorm started cold and produced shallow plans. gstack's sprint-start review pattern showed the value of a dedicated read-only mapping phase.
- **Impact:**
  - **New workflow Step 0.5** between deep-interview (step 0) and brainstorm (step 1)
  - Dispatches 3 parallel Explore agents (entry points / data model / tests+config)
  - Reads 3-5 load-bearing files max — keeps token cost predictable
  - Cross-references `tasks/findings.md`, `tasks/lessons.md`, `docs/decisions.md`
  - Writes structured `tasks/investigation.md` with Entry Points / Data Model / Tests / Config / Prior Decisions tables
  - Brainstorm now reads `tasks/investigation.md` automatically
  - **Auto-skip rules:** concrete anchors in task, greenfield repo, bug flow (deep-dive owns its own investigation), `--skip-investigate` flag, or recent investigation.md (<4 hours)
  - **Unfamiliar-area detection:** subsystem references + exploration verbs + brownfield + no concrete anchors
  - Wired into `/sk:start` (manual mode) and `/sk:autopilot` (step 0.5)
  - Intensity auto-selected to `lite` in autopilot (factual mapping, not essays)

### 3. `<private>` Tag Convention — Memory Privacy (from claude-mem)

- **What:** Policy rule in CLAUDE.md: content wrapped in `<private>...</private>` tags is never written to any persistent memory surface.
- **Why:** Users need a way to paste credentials, internal URLs, stakeholder names, or debugging snippets into a conversation without leaking them into `tasks/*.md`, auto-memory files, commit messages, or changelogs. claude-mem had a similar exclusion mechanism but only for its own storage — we generalized it to all persistent surfaces.
- **Impact:**
  - **5 rules** documented in `CLAUDE.md` → Project Memory → Memory Privacy subsection
  - Applies to: `tasks/*.md`, `~/.claude/projects/*/memory/`, commit messages, PR descriptions, changelogs, architectural change log
  - Multi-line and single-line tags both supported; case-sensitive
  - Missing closing tag → treat to end-of-message as private
  - If user asks to save `<private>` content: refuse and instruct to unmark first
  - Mirrored in `skills/sk:setup-claude/templates/CLAUDE.md.template` so new projects inherit it

### 4. `/sk:ci --claude` Fast-Path — ShipKit-Aware PR Review (from claude-code-action)

- **What:** New `--claude` flag on `/sk:ci` that scaffolds a ShipKit-aware claude-code-action GitHub workflow.
- **Why:** `anthropics/claude-code-action` ships a generic @claude trigger. We wanted a drop-in config that runs ShipKit's 8-dimension review prompt on every PR and outputs a `=== ShipKit Review Summary ===` block for grep-ability.
- **Impact:**
  - Added to `skills/sk:ci/SKILL.md` as a "Fast Path" section (no separate command — folded into existing `/sk:ci`)
  - Scaffolds two workflows:
    - `[1] @claude Trigger` — `pull_request.types: [labeled]` with `label_trigger: "claude"` for on-demand invocation
    - `[2b] ShipKit Auto PR Review` — runs on every PR open/sync with 8-dimension prompt (correctness, security, performance, reliability, design, best practices, documentation, testing)
  - Users run `/sk:ci --claude` once per repo; no further setup needed

---

## Workflow Integration

Before these changes, the flow was:
```
0 (deep-interview, optional) → 1 (brainstorm) → 2 (design) → 3 (plan) → 4 (branch) →
5 (tests+implement) → 5.5 (scope-check) → 6 (commit) → 7 (gates) → 8 (finalize) →
8.5 (learn) → 8.6 (retro)
```

After:
```
0 (deep-interview, optional) → 0.5 (investigate, auto-skip) → 1 (brainstorm) → 2 → 3 → 4 →
5 → 5.5 → 6 → 7 (gates; Batch 3 now auto-invokes respond-review) → 8 → 8.5 → 8.6
```

Step 0.5 is optional like step 0 — does not change the required step count for `/sk:setup-optimizer`'s 11-step validation.

`/sk:respond-review` has **no new workflow position** — it's a sub-routine inside gates Batch 3 and also available as a standalone command.

---

## Files Changed

| File | Change |
|------|--------|
| `skills/sk:investigate/SKILL.md` | **New** — read-only feature-area exploration skill |
| `commands/sk/investigate.md` | **New** — thin command wrapper |
| `skills/sk:respond-review/SKILL.md` | **New** — review finding triage skill |
| `commands/sk/respond-review.md` | **New** — thin command wrapper |
| `skills/sk:ci/SKILL.md` | Added `--claude` fast-path section + `[2b]` ShipKit auto-review template |
| `skills/sk:gates/SKILL.md` | Batch 3 now auto-invokes `Skill("sk:respond-review")`; references 8-dimension review |
| `skills/sk:start/SKILL.md` | Added unfamiliar-area detection + `--investigate`/`--skip-investigate` flags + routing branch for investigate pre-phase |
| `skills/sk:autopilot/SKILL.md` | Added Step 0.5 (Investigate) block; intensity routing table gets `investigate → lite` row |
| `CLAUDE.md` | Added Step 0.5 row; auto-skip rules; `<private>` privacy subsection; Commands table entries for investigate + respond-review; `/sk:ci --claude` note |
| `skills/sk:setup-claude/templates/CLAUDE.md.template` | Mirrored all CLAUDE.md changes |
| `skills/sk:setup-optimizer/SKILL.md` | Added `sk:investigate` and `sk:respond-review` to missing-commands check |
| `commands/sk/help.md` | Added Step 0.5 row; new entries in All Commands table |
| `docs/FEATURES.md` | Added `/sk:investigate` (Planning & Exploration) + `/sk:respond-review` (Quality Gates) entries |
| `docs/dashboard.html` | `COMMANDS` array: added `/sk:investigate`, `/sk:respond-review`; updated `/sk:ci` desc for `--claude` fast-path |
| `tasks/steal-report-2026-04-07.md` | Full steal report from the 4 sources |

---

## Rationale for Scope Choices

- **Folded `--claude` into `/sk:ci` instead of creating `/sk:ci-claude`:** A new command would duplicate 90% of `/sk:ci`'s existing scaffolding logic. A flag keeps both code paths in one place.
- **Made `/sk:respond-review` both standalone and gates-invoked:** Users running a bare `/sk:review` want triage too. Making it a skill (not just gates-internal logic) gives them both entry points.
- **Investigate as Step 0.5, not Step 1.5:** It must run before brainstorm reads context files, so brainstorm can consume `tasks/investigation.md` as input.
- **`<private>` as a CLAUDE.md policy, not a hook:** A hook would have false positives (what about log files? diffs?). A policy rule tells the assistant to apply it at write time, with the user's trust model clear.
- **No `/sk:investigate` in `/sk:fast-track`:** Fast-track is for small known changes where exploration is overhead. Investigate only triggers in full flow when signals match.
