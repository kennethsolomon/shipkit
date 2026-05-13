---
name: sk:deep-interview
description: "Socratic requirements-gathering with mathematical ambiguity scoring. Runs before brainstorm on vague tasks. Outputs tasks/spec.md."
allowed-tools: Read, Write, Glob, Grep, Bash, Agent, AskUserQuestion
---

# Deep Interview

Crystallize vague requirements into a decision-complete spec before any exploration or planning begins. Uses mathematical ambiguity scoring to know when to stop asking — not time-based, not vibes-based.

<HARD-GATE>
Do NOT write code, create a plan, or invoke any implementation skill. This skill only asks questions and writes tasks/spec.md.
</HARD-GATE>

## When to Use

- User has a vague idea: "improve the dashboard", "build something for auth", "make it faster"
- User says "deep interview", "ask me everything", "don't assume", "interview me"
- Auto-invoked by `/sk:autopilot` and `/sk:start` when input has no concrete anchors

## When NOT to Use

- Task has specific file paths, function names, or error messages — execute directly
- Task is a bounded bug fix with a known cause — use `/sk:debug` or `/sk:deep-dive`
- User says "just do it" or "skip the questions"
- `tasks/spec.md` already exists and is current

---

## Ambiguity Scoring

Track 4 weighted dimensions throughout the interview:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Goal Clarity | 35% | Does the user know exactly what outcome they want? |
| Constraint Clarity | 25% | Are boundaries, limits, and non-goals clear? |
| Success Criteria | 25% | Can we write a failing test for this? |
| Context Clarity | 15% | Is the brownfield/technical context understood? |

**Ambiguity score** = 1 − (weighted sum of dimension scores)

**Gate threshold:** Ambiguity must reach ≤ 20% before proceeding. Default is 20% — do not proceed above this.

Score each dimension 0.0–1.0 after each round based on the conversation so far.

---

## Ontology Tracking

Maintain a list of "core entities" mentioned across rounds (the main nouns: the thing being built/fixed).

- Track entity names across rounds
- If the same concept appears under 3+ different names (e.g., "workflow", "inbox", "planner"), ask: "Across our conversation you've called this a workflow, an inbox, and a planner. Which one is the core thing this IS?"
- Stability ratio = stable entities / total entities. Report when ≥ 75% stable.

---

## Steps

### Phase 1 — Initialize

1. **Check for existing spec:** If `tasks/spec.md` exists, read it. Ask: "A spec already exists — extend, revise, or start fresh?"

2. **Brownfield detection:** If this is an existing codebase (check for `package.json`, `composer.json`, `go.mod`, etc.), spawn an Explore agent:
   > "Read CLAUDE.md, tasks/findings.md if present, and explore the top-level directory structure. Return: tech stack, main features, recent activity (git log --oneline -5). Read-only."

   Use findings to pre-fill Context Clarity — don't ask what the code already answers.

3. **Seed from caller context:** If invoked by autopilot/start with a task description, use it as the starting prompt. Set initial dimension scores based on how concrete it is.

### Phase 2 — Interview Loop

Repeat until ambiguity ≤ 20% OR early exit OR hard cap:

#### Step 2a — Identify target dimension

Find the dimension with the lowest clarity score. That is the next question target.

If all dimensions are stuck (score hasn't improved in 2 rounds on the same dimension), switch to ontology-style questioning: "What is the core thing this IS, before we discuss what it does?"

#### Step 2b — Ask one question

Use `AskUserQuestion` with:
- Header prefix: `Round {n} | Targeting: {dimension} | Ambiguity: {score}%`
- One question only — never batch multiple questions
- Question style by dimension:

| Dimension | Style | Example |
|-----------|-------|---------|
| Goal Clarity | "What exactly happens when...?" | "When you say 'improve the dashboard', what specific action does a user take that currently fails or frustrates?" |
| Constraint Clarity | "What are the hard limits?" | "Should this work for all users or only admins?" |
| Success Criteria | "How would you test this?" | "If I built this correctly, what would you check to confirm it's done?" |
| Context Clarity | "What must stay unchanged?" | "Are there existing components this must integrate with?" |

Provide 3–4 contextually relevant options plus free-text. Options should expose assumptions, not gather feature lists.

**Never ask:**
- What the codebase already tells you (check brownfield context first)
- Multiple questions at once
- Generic questions unrelated to the weakest dimension

#### Step 2c — Score the round

After the user answers, update all 4 dimension scores. Recalculate ambiguity.

#### Step 2d — Report progress

After each round:
```
Round {n} complete.

| Dimension        | Score | Weight | Weighted |
|------------------|-------|--------|----------|
| Goal Clarity     | {s}   | 35%    | {s*.35}  |
| Constraint       | {s}   | 25%    | {s*.25}  |
| Success Criteria | {s}   | 25%    | {s*.25}  |
| Context          | {s}   | 15%    | {s*.15}  |
| **Ambiguity**    |       |        | **{score}%** |

Ontology: {n} entities | Stability: {ratio} | New: {n} | Stable: {n}

{score <= 20 ? "Clarity threshold met — ready to proceed." : "Next: targeting " + weakest_dimension}
```

#### Step 2e — Check exit conditions

| Condition | Action |
|-----------|--------|
| Ambiguity ≤ 20% | Exit loop → Phase 3 |
| Round 3+ and user says "enough", "let's go", "build it", "proceed" | Early exit → Phase 3 |
| Round 10 | Warn: "We're at 10 rounds. Ambiguity: {score}%. Continue or proceed?" |
| Round 20 | Hard cap: proceed with current clarity, note in spec |

### Phase 3 — Generate Spec

Write `tasks/spec.md`:

```markdown
# Spec: {title}

## Metadata
- Interview rounds: {n}
- Final ambiguity: {score}%
- Status: {PASSED | EARLY_EXIT | HARD_CAP}
- Generated: {YYYY-MM-DD}

## Goal
{crystal-clear goal statement — 1–3 sentences}

## Constraints
- {constraint 1}
- {constraint 2}

## Non-Goals (explicitly excluded)
- {excluded scope 1}

## Acceptance Criteria
- [ ] {testable criterion 1}
- [ ] {testable criterion 2}
- [ ] {testable criterion 3}

## Assumptions Exposed
| Assumption | How surfaced | Resolution |
|------------|-------------|------------|
| {assumption} | Round {n} | {decision} |

## Technical Context
{brownfield findings or "greenfield — no existing constraints"}

## Ontology
Core entity: {the main thing being built/fixed}
Supporting concepts: {list}
```

### Phase 4 — Handoff

Tell the user:
> "Spec written to `tasks/spec.md` (ambiguity: {score}%). `/sk:brainstorm` will read it automatically — no need to repeat requirements."

If invoked by autopilot or start: return silently — the caller continues automatically.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:deep-interview"]` is set, use that model.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit. When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
