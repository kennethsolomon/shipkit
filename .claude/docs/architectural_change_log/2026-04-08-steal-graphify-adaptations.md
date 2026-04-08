# 2026-04-08 — graphify Steal Adaptations

**Source:** https://github.com/safishamsi/graphify

## Changes

### 1. `ambiguous` status label (CLAUDE.md, sk:review, maintenance-guide)
Added `ambiguous` as a fifth honest status label — distinct from `blocked` (can't check) and `inferred` (blast-radius guess). Use when a finding or claim could mean multiple things and needs disambiguation before acting.

Files updated: `CLAUDE.md`, `skills/sk:review/SKILL.md`, `.claude/docs/maintenance-guide.md`

### 2. God nodes in `/sk:investigate`
Added **God Nodes** section to `tasks/investigation.md` output template — top 3-5 most-referenced files in the feature area. Highest-leverage points: changes here have the widest blast radius.

Files updated: `skills/sk:investigate/SKILL.md`, `docs/sk:features/sk-investigate.md`

### 3. Suggested questions in `/sk:investigate` and `/sk:explain`
Both skills now surface 4-5 questions the analysis is uniquely positioned to answer. In investigate: questions the terrain map raises. In explain: questions the code structure surfaces that aren't obvious from reading linearly.

`/sk:explain` updated from 5-section to 6-section format. Intensity table updated accordingly.

Files updated: `skills/sk:investigate/SKILL.md`, `skills/sk:explain/SKILL.md`, `docs/sk:features/sk-investigate.md`, `docs/sk:features/sk-explain.md`

### 4. Worked examples structure in `/sk:eval benchmark`
After each benchmark run, `/sk:eval benchmark` now writes a `worked/{skill}-YYYYMMDD/` folder with human-readable prompts, raw outputs, and an honest `review.md` verdict. Pattern adapted from graphify's `worked/{slug}/` convention.

Files updated: `skills/sk:eval/SKILL.md`, `docs/sk:features/sk-eval.md`

## Spec status bumps
`docs/FEATURES.md`: sk-investigate, sk-explain, sk-eval → 2026-04-08 / v3.29.1
