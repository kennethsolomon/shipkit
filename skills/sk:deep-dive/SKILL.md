---
name: sk:deep-dive
description: "Two-stage pipeline: parallel trace → deep-interview. For bugs where root cause is unknown. Outputs tasks/spec.md with root cause + fix requirements."
allowed-tools: Read, Write, Bash, Glob, Grep, Agent, Skill
---

# Deep Dive

Investigate bugs with unknown root causes before writing a single line of fix code. Stage 1 runs 3 parallel investigation lanes and synthesizes findings. Stage 2 runs a pre-seeded deep interview to crystallize what exactly to fix. Output is a spec that drives the standard bug fix flow.

<HARD-GATE>
Do NOT write fix code before Stage 2 produces tasks/spec.md. Random fixes before root cause confirmation waste time and mask real issues.
</HARD-GATE>

## When to Use

- Bug with no known root cause: "something is broken with auth", "payments failing intermittently", "the dashboard is slow"
- Auto-invoked by `/sk:start` and `/sk:autopilot` when bug signals detected + no known cause
- You want to understand WHY before deciding WHAT to fix

## When NOT to Use

- Root cause is already known (specific file:line, stack trace, "the issue is X") → use `/sk:debug` directly
- User says "just fix it" with a specific location → skip to bug fix flow
- No reproducible symptom yet → gather reproduction steps first

---

## Stage 1 — Parallel Trace

Run 3 investigation lanes **simultaneously** via Agent tool:

### Lane 1 — Recent Changes (Bash)
```bash
git log --oneline -20
git diff HEAD~5 --stat
git log --oneline --since="7 days ago" -- [affected-area-if-known]
```
Goal: correlate the bug's appearance with recent commits. Output: list of suspect commits with dates and file counts.

### Lane 2 — Code Structure (Explore agent)
```
Explore agent prompt:
"Map the code structure relevant to [symptom/area]. Find:
1. Entry points (routes, controllers, handlers) for the affected feature
2. Core data flow — what calls what
3. External dependencies (DB queries, API calls, queues, caches)
4. Any TODO/FIXME/HACK comments in the affected area
Read-only. Return file paths and a brief call chain."
```

### Lane 3 — Runtime Behavior (Bash)
```bash
# Run failing tests/commands — capture full output
[detected test command] 2>&1 | head -100

# Check error logs if accessible
tail -100 storage/logs/laravel.log 2>/dev/null || \
  tail -100 logs/app.log 2>/dev/null || \
  echo "No log file found"
```
Goal: reproduce the failure and capture exact error output, stack traces, and timing.

**Wait for all 3 lanes to complete.**

### Trace Synthesis

After all lanes return, synthesize into a trace report:

```
## Trace Report

### Suspect Commits (Lane 1)
- {commit hash} {date}: {message} — {files changed}
- Most likely: {top suspect if any}

### Affected Code Area (Lane 2)
- Entry point: {file:line}
- Call chain: {A → B → C → D}
- External deps: {DB/API/queue/cache calls}

### Runtime Failure (Lane 3)
- Error: {exact message}
- Stack trace: {top 5 frames}
- Reproducible: {yes/no/intermittent}

### Unknowns (what the trace couldn't resolve)
- {unknown 1}
- {unknown 2}
```

---

## Stage 2 — Pre-Seeded Deep Interview

Run the deep-interview logic with trace context injected — same ambiguity scoring, but starting from a much higher baseline.

**Threshold:** 25% (trace already reduced uncertainty — lower bar to proceed)

**3-Point Injection:**

1. **Enriched starting point** — pre-score dimensions based on trace:
   - If root cause is strongly suspected: Goal Clarity starts at 0.6
   - If stack trace is clear: Context Clarity starts at 0.8
   - Unknowns from trace become the first questions

2. **System context** — inject Lane 2's code map as background so questions skip "what does this code do"

3. **Seed questions** — convert trace unknowns into first interview questions:
   > `Round 1 | Targeting: Goal Clarity | Why now: trace found suspect commit but needs confirmation | Ambiguity: 45%`
   > "The trace shows {commit} changed {file} 3 days ago, right when this started. Was this change intentional? What was it supposed to do?"

Follow the same interview loop mechanics as `/sk:deep-interview` (one question per round, round headers, dimension scoring).

**Output:** `tasks/spec.md` — same format as deep-interview but with an added section:

```markdown
## Root Cause
- Suspect: {commit / code path / config / race condition}
- Evidence: {Lane 1/2/3 findings that support this}
- Confidence: {high / medium / low}

## Fix Scope
- Minimal fix: {what to change}
- Regression risk: {what else might break}
- Test to write first: {the failing test that proves the bug exists}
```

---

## Stage 3 — Bug Fix Handoff

After `tasks/spec.md` is written:

1. Log: `[Deep-dive] Root cause identified (ambiguity: {score}%). Proceeding to fix flow.`
2. Continue with bug fix flow:
   - `/sk:branch` — create branch from spec title
   - `/sk:write-tests` — write regression test that fails (proves bug exists)
   - `/sk:execute-plan` — implement fix
   - `/sk:smart-commit`
   - `/sk:gates`
   - `/sk:finish-feature`

If invoked by autopilot/start: return to caller after writing spec — the caller drives the fix flow.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:deep-dive"]` is set, use that model.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit. When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
