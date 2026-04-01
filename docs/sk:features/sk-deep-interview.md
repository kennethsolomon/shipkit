# sk:deep-interview — Feature Spec

**Version:** v3.23.0
**Last updated:** 2026-04-01

## Purpose

Crystallize vague requirements into a decision-complete spec before any exploration or planning. Uses mathematical ambiguity scoring across 4 dimensions — stops asking only when clarity reaches ≥80% (ambiguity ≤20%).

## Trigger Conditions

Auto-invoked by `/sk:start` and `/sk:autopilot` when input has no concrete anchors (no file paths, function names, error messages, or bounded scope). Also invokable manually.

## What It Reads

- `tasks/spec.md` — if exists, asks extend/revise/start fresh
- `tasks/findings.md` — prior context (if any)
- Codebase structure (brownfield detection via Explore agent)

## What It Produces

`tasks/spec.md`:
- Goal statement
- Constraints
- Non-goals (explicitly excluded scope)
- Acceptance criteria (testable)
- Assumptions exposed and resolved
- Technical context (brownfield findings)

## Core Mechanics

### Ambiguity Scoring

| Dimension | Weight |
|-----------|--------|
| Goal Clarity | 35% |
| Constraint Clarity | 25% |
| Success Criteria | 25% |
| Context Clarity | 15% |

Ambiguity = 1 − weighted sum. Gate: ≤ 20% required to proceed.

### Question Strategy

- One question per round targeting the weakest dimension
- Round header: `Round {n} | Targeting: {dimension} | Why now: {rationale} | Ambiguity: {score}%`
- Never asks what the codebase already answers (brownfield Explore agent runs first)
- Ontology tracking: flags when core entity shifts names across rounds

### Exit Conditions

| Condition | Action |
|-----------|--------|
| Ambiguity ≤ 20% | Proceed to spec generation |
| Round 3+, user says "enough/let's go/build it" | Early exit |
| Round 10 | Soft warning |
| Round 20 | Hard cap, proceed with current clarity |

## Integration Points

- `/sk:brainstorm` reads `tasks/spec.md` if present — skips re-asking covered questions
- `/sk:write-plan` reads `tasks/spec.md` acceptance criteria as requirements
- `/sk:autopilot` step 0 — invokes for Check B (vague feature)
- `/sk:start` step 1/3 — invokes for vague-feature flagged tasks

## Hard Rules

- No code, no planning — requirements only
- One question per round — never batch
- Never asks about existing code (use Explore agent instead)
