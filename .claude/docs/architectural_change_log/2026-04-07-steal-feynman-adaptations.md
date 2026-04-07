---
date: 2026-04-07
source: https://github.com/getcompanion-ai/feynman
type: steal-adaptation
---

# Feynman Steal Adaptations

Five patterns adapted from the Feynman open-source AI research agent.

## Changes

### 1. Honest Status Labels (CLAUDE.md + sk:review)

**What:** Added `verified` / `unverified` / `inferred` / `blocked` status labels to `tasks/progress.md` protocol (CLAUDE.md) and per-finding tags in `sk:review` report format.

**Why:** Prevents vague language ("may need testing", "possibly affected") from hiding real gaps. Forces honest accounting of what was actually confirmed vs. assumed.

**Files:** `CLAUDE.md` (Project Memory section), `skills/sk:review/SKILL.md` (Step 11 report format + rules)

### 2. Progress.md as Lab Notebook (CLAUDE.md)

**What:** Strengthened `tasks/progress.md` rules — now requires reading it before resuming substantial work, and each entry must end with a `Next:` line.

**Why:** Prior rule said "write continuously" but didn't mandate pre-read on resume or require entries to include next-step intent. Sessions resumed cold without context.

**Files:** `CLAUDE.md` (Project Memory section)

### 3. Slug-Based Artifact Naming (sk:deep-dive)

**What:** Added slug derivation at the start of Stage 1. Intermediate trace artifacts written to `tasks/.drafts/<slug>-trace.md` instead of in-memory only.

**Why:** Multiple concurrent bug investigations would produce colliding intermediate artifacts. Slug prevents this and makes trace artifacts resumable across sessions.

**Files:** `skills/sk:deep-dive/SKILL.md`

### 4. Multi-Agent Decomposition is Internal Tactic (sk:autopilot + sk:team)

**What:** Added explicit "Agent Orchestration Principle" / "Orchestration Principle" sections stating that multi-agent decomposition is an internal tactic, not primary UX. Users see synthesized results, not coordination internals.

**Why:** Without this rule, autopilot and team mode risk exposing chain-shaped orchestration steps in user-facing output, creating noise and confusion.

**Files:** `skills/sk:autopilot/SKILL.md`, `skills/sk:team/SKILL.md`

### 5. Per-Artifact Provenance Sidecar (sk:review)

**What:** Added Step 11.5 to `sk:review` — after generating the report, writes `tasks/review-provenance.md` recording which files were read in full vs. grep-only, blast-radius verification status per symbol, and which dimensions were checked vs. skipped.

**Why:** The review report states findings but not what was actually checked. The provenance sidecar makes the audit trail explicit — especially useful for distinguishing `verified` from `inferred` blast-radius findings.

**Files:** `skills/sk:review/SKILL.md` (new Step 11.5)
