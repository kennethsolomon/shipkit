# sk:deep-dive — Feature Spec

**Version:** v3.23.0
**Last updated:** 2026-04-01

## Purpose

Investigate bugs with unknown root causes before any fix code is written. Runs 3 parallel investigation lanes, synthesizes findings, then runs a pre-seeded deep interview to crystallize exactly what to fix. Output drives the standard bug fix flow.

## Trigger Conditions

Auto-invoked by `/sk:start` (deep-dive flow) and `/sk:autopilot` (step 0, Check A) when:
- Bug signals present (`bug`, `error`, `broken`, `crash`, `failing`, `not working`, etc.)
- AND no known-cause anchors (no file:line, no "the issue is X", no specific function + symptom)

## What It Reads

- `git log` and `git diff` — recent commit history
- Affected codebase area (via Explore agent)
- Test output / error logs

## What It Produces

`tasks/spec.md` — standard spec format plus:
- Root cause section (suspect, evidence, confidence level)
- Fix scope (minimal change, regression risk)
- Regression test to write first

## Core Mechanics

### Stage 1 — Parallel Trace (3 lanes)

| Lane | Tool | Goal |
|------|------|------|
| Recent changes | Bash: `git log --oneline -20` + `git diff HEAD~5 --stat` | Correlate bug with commits |
| Code structure | Explore agent | Map entry points, call chain, external deps |
| Runtime behavior | Bash: run failing tests/commands | Reproduce failure, capture error output |

All 3 lanes run simultaneously via Agent tool.

### Stage 2 — Pre-Seeded Deep Interview

Same ambiguity scoring as `/sk:deep-interview` but:
- Threshold: 25% (trace already reduced uncertainty)
- Starts with pre-scored dimensions (Lane 2/3 may fill Context Clarity to 0.8)
- First questions target trace unknowns, not things the trace already answered
- 3-point injection: enriched starting point + system context + seeded questions

## Integration Points

- `/sk:start` — routes here when bug signals detected + no known cause
- `/sk:autopilot` step 0 (Check A) — invokes for unknown-cause bugs
- After spec: hands off to branch → `/sk:write-tests` → `/sk:execute-plan` → commit → gates

## Hard Rules

- No fix code before `tasks/spec.md` is written
- All 3 trace lanes must run before Stage 2
- Regression test must be written before fix implementation
