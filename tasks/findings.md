# Findings — 2026-03-19 — Vibe Coding Inspiration: sk:context + sk:mvp docs + decisions log

## Problem Statement

ShipKit lacks session continuity tooling. When returning to a project after a break, context must be manually reconstructed by reading 5+ files. sk:mvp also produces no project documentation — the product idea lives only in the conversation. And architectural decisions made during brainstorm are lost (overwritten per task in `tasks/findings.md`).

Inspiration source: `/Users/kennethsolomon/Herd/vibe-coding-starter-kit` — specifically its `03-logs/` memory system and `04-process/llm-prompts.md` session initialization patterns.

## Key Decisions Made

- **All 3 approaches** will be implemented (A, B, C)
- **No new workflow steps** — these are enhancements to existing skills + one new standalone command
- **sk:context** outputs a readable session brief AND auto-loads all files into context in the same run

## Chosen Approaches

### Approach A — Enhance sk:mvp with project context docs

At the end of sk:mvp (after app generation + Playwright validation), auto-generate 3 docs from info already collected during the idea-gathering phase. Zero extra user input.

**Files to generate:**
- `docs/vision.md` — product name, value prop, target audience, core features, north star
- `docs/prd.md` — feature list + acceptance criteria derived from the idea prompt
- `docs/tech-design.md` — tech stack chosen, data models, component map (landing page + app structure)

**Where in sk:mvp:** New Phase 9 (after quality loop, before output summary). Add to SKILL.md as a mandatory step.

---

### Approach B — New `sk:context` command (session initializer)

A new standalone skill `/sk:context` designed to be run at the **start of any session**.

**What it does (two things simultaneously):**
1. **Auto-loads** all context files into the conversation (reads them, extracts key info)
2. **Outputs a formatted session brief** the user can read immediately

**Files it reads:**
- `tasks/todo.md` — current task name + pending checkboxes
- `tasks/workflow-status.md` — current step + `>> next <<`
- `tasks/progress.md` — last 5-10 entries (most recent work)
- `tasks/findings.md` — current task decisions and open questions
- `tasks/lessons.md` — all active lessons (applied as constraints)
- `docs/decisions.md` — if exists, recent ADR entries
- `docs/vision.md` — if exists, product context

**Output format (session brief):**
```
=== SESSION BRIEF ===
Branch:      feature/xxx
Task:        [task name from todo.md]
Step:        [current step] → [next step command]
Last done:   [last progress.md entry summary]
Pending:     N checkboxes remaining
Lessons:     [count] active — [1-liner summary of most critical]
Open Qs:     [any from findings.md]
====================
```

**New skill file:** `skills/sk:context/SKILL.md`
**Trigger:** 14+ file updates per lessons.md (new command added)

---

### Approach C — Persistent decisions log in sk:brainstorm

sk:brainstorm currently writes to `tasks/findings.md` (overwritten each task). Add a **cumulative** write to `docs/decisions.md` in ADR format.

**What changes in sk:brainstorm (Step 6 — Record findings):**
- Still writes to `tasks/findings.md` (unchanged)
- Additionally **appends** a new ADR entry to `docs/decisions.md`

**ADR entry format:**
```markdown
## [YYYY-MM-DD] [Feature/Task Name]

**Context:** [problem being solved]
**Decision:** [chosen approach]
**Rationale:** [why this approach over alternatives]
**Consequences:** [trade-offs accepted]
**Status:** accepted
```

**File location:** `docs/decisions.md` (created on first brainstorm if not exists)
**Rule:** Never overwritten — append only.

---

## Scope Summary

| Item | Type | Complexity | Files Changed |
|------|------|------------|---------------|
| Approach A: sk:mvp docs generation | Enhance existing skill | Small | 1 (sk:mvp/SKILL.md) |
| Approach B: sk:context command | New skill | Small-Medium | 14+ (per lessons.md) |
| Approach C: decisions.md in sk:brainstorm | Enhance existing skill | Small | 2 (sk:brainstorming/SKILL.md + docs/decisions.md template) |

## Open Questions

- None — direction locked
