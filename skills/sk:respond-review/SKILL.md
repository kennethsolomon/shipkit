---
name: sk:respond-review
description: "Triage /sk:review findings into fix-now / defer / dispute buckets, apply fixes, and prepare the review gate for re-run. Wired into /sk:gates Fix & Retest loop; also usable standalone after a manual /sk:review."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

# Respond to Review

Structured protocol for responding to `/sk:review` findings. Classifies each finding, applies fixes for the `fix-now` bucket, logs deferred items to tech debt, and produces a one-line summary for the gates orchestrator.

## When to Use

- **Auto-invoked by `/sk:gates`** when the review gate (Batch 3) produces any Critical or Warning finding
- **Manual entry** after a standalone `/sk:review` run when you want a structured triage instead of fixing ad-hoc
- **Fix & Retest Protocol** — the "Logic change" row of the protocol routes through this skill before re-running the gate

## When NOT to Use

- Review had 0 findings → skip; proceed to next gate
- You are still writing code (review hasn't run yet) — use `/sk:review` first
- Lint/format/style fixes — those are handled in-line by `/sk:gates` Batch 1 without this skill

---

## Inputs

This skill reads review findings from:

1. **Last `/sk:review` output** in the conversation, OR
2. `tasks/progress.md` entries tagged `[review]` from the current session, OR
3. A findings file path passed as argument: `/sk:respond-review <path>`

If no findings source is found, ask the user to point to one and stop.

## Severity Taxonomy

`/sk:review` emits findings at these severities (documented in `skills/sk:review/SKILL.md`):

| Severity | Meaning | Default action |
|----------|---------|----------------|
| **Critical** | Breaks correctness, security, or production safety | `fix-now` — mandatory |
| **Warning** | Reliability/design smell that will cause pain | `fix-now` by default; `defer` only with written rationale |
| **Nit** | Style, naming, minor clarity | `defer` or `dispute` by default; never blocks |

`Critical` and `Warning` findings block the review gate. `Nit` findings are informational only.

---

## Steps

### 1. Collect findings into a triage table

Scan the review output. Build a table with one row per distinct finding:

```markdown
| # | Severity | Dimension | File:Line | Finding | Recommended fix | Bucket |
|---|----------|-----------|-----------|---------|-----------------|--------|
| 1 | Critical | Security | app/Auth.php:42 | Unsanitized input in SQL query | Use prepared statement | fix-now |
| 2 | Warning | Performance | app/Feed.php:18 | N+1 in loop | Eager-load `comments` | fix-now |
| 3 | Nit | Design | app/Util.php:7 | Rename `foo` to `normalizeInput` | Rename | defer |
```

**Deduplication:** If the same finding appears in multiple dimensions (e.g., "missing error handling" flagged by both reliability and design), merge into one row and list both dimensions.

### 2. Classify each finding — three buckets

Apply the bucket-assignment rules in this exact order. First rule that matches wins.

#### Bucket A — `fix-now`

Apply if ANY is true:
- Severity is `Critical`
- Severity is `Warning` AND the finding touches: security, correctness, data integrity, auth, payments, or a production path
- Severity is `Warning` AND the fix is <10 lines and localized (no cross-file refactor)

These fixes happen in this session, before the gate re-runs.

#### Bucket B — `defer`

Apply if ALL are true:
- Severity is `Warning` or `Nit`
- Fix requires a cross-file refactor or a separate design discussion
- Not in security/correctness/data-integrity path
- The user's current task would become significantly larger to address it now

Deferred findings are appended to `tasks/tech-debt.md` with full context. They do NOT block the gate.

#### Bucket C — `dispute`

Apply if ANY is true:
- The finding is based on a misreading of the code (reviewer missed context)
- The finding contradicts an explicit decision in `docs/decisions.md` or `tasks/lessons.md`
- The "fix" would introduce a worse problem than the finding describes

Disputed findings are documented with a written rebuttal. They do NOT block the gate.

**Conservative default:** When torn between `fix-now` and `defer`, choose `fix-now`. When torn between `defer` and `dispute`, choose `defer`. Disputing a finding requires a clear, defensible reason — not just disagreement.

### 3. Apply `fix-now` fixes

For each row in the `fix-now` bucket, in order of severity (Critical before Warning):

1. Read the referenced file(s) fully — do not patch blindly from the review's snippet
2. Check `tasks/lessons.md` for any lesson that applies to this fix pattern
3. Apply the fix with `Edit`
4. If the fix touches logic (new branch, condition, data path, algorithm):
   - Write or update a failing test first (per Fix & Retest Protocol in `CLAUDE.md`)
   - Then apply the fix so the test passes
5. Run the relevant test file locally to confirm the fix works
6. Log the fix to `tasks/progress.md` as `[respond-review] Fixed #N: <short description>`

**Same-finding detection:** If the review has flagged the *same* file:line in two consecutive runs with the same finding, stop fixing and escalate:
- Spawn the `architect` agent with: "Finding X on file:line has survived 2 fix attempts. Diagnose root cause and recommend an alternate approach. Read-only."
- Apply the architect's recommendation as the next fix attempt
- If still present on the 3rd run, trigger 3-strike protocol (stop, report, ask user)

### 4. Log `defer` findings to tech debt

For each row in the `defer` bucket, append one entry to `tasks/tech-debt.md`:

```markdown
### [YYYY-MM-DD] [Finding title]
**Severity:** Warning | Nit
**Location:** `path/to/file.ext:line`
**Finding:** [the finding as stated by the reviewer]
**Why deferred:** [1-2 sentences — why this is not fixed now]
**Suggested fix:** [the reviewer's recommended fix]
**Source:** `/sk:respond-review` from `/sk:review` on branch `[branch name]`
```

If `tasks/tech-debt.md` does not exist, create it with a header first:

```markdown
# Tech Debt Log

Deferred findings and known issues. Append-only. Entries with a `Resolved:` line are closed.
```

### 5. Document `dispute` findings

For each row in the `dispute` bucket, append an entry to `tasks/review-disputes.md`:

```markdown
### [YYYY-MM-DD] [Finding title]
**Severity:** Critical | Warning | Nit
**Location:** `path/to/file.ext:line`
**Finding:** [reviewer's statement]
**Rebuttal:** [why this finding is invalid — cite evidence: code, decision record, lesson]
**Referenced:** [docs/decisions.md entry, tasks/lessons.md entry, or specific line of code that supports the rebuttal]
**Reviewer should re-check:** [what context the next review run should consider]
```

If `tasks/review-disputes.md` does not exist, create it with a header:

```markdown
# Review Disputes

Findings rejected with rebuttals. Append-only. Informs future review runs.
```

### 6. Commit the triage batch

If any `fix-now` fix was applied:

```bash
git add <modified files> tasks/progress.md tasks/tech-debt.md tasks/review-disputes.md
git commit -m "fix(review): apply respond-review triage — <N> fixed, <M> deferred, <K> disputed"
```

One commit for the whole triage batch — do not commit per fix. This is consistent with the squash-gate-commits rule in `CLAUDE.md`.

If no fixes were applied (everything was defer or dispute), still commit the `tasks/` updates:

```bash
git add tasks/progress.md tasks/tech-debt.md tasks/review-disputes.md
git commit -m "chore(review): respond-review triage — 0 fixed, <M> deferred, <K> disputed"
```

### 7. Summary to the caller

Output a single compact block:

```
=== Respond-Review Summary ===
Total findings: N
Fixed now:      X  (Critical: a, Warning: b)
Deferred:       Y  → tasks/tech-debt.md
Disputed:       Z  → tasks/review-disputes.md

Gate status: [READY_TO_RERUN | BLOCKED — see below]
```

If status is `READY_TO_RERUN`, return control to `/sk:gates` (or the user) and recommend re-running the review gate.

If status is `BLOCKED` (3-strike triggered, or architect escalation unresolved), stop and report to the user. Do not auto-rerun.

---

## Integration with `/sk:gates`

`/sk:gates` wires this skill into Batch 3 (review) as follows:

1. Review agent produces findings
2. If findings > 0 → `/sk:gates` invokes `Skill("sk:respond-review")`
3. `/sk:respond-review` runs steps 1–7 above
4. On `READY_TO_RERUN` → `/sk:gates` re-runs the review gate from scratch
5. On `BLOCKED` → `/sk:gates` triggers its own 3-strike protocol

`/sk:respond-review` does not re-invoke `/sk:review` itself — that is always the gate orchestrator's job.

## Anti-Patterns

- **Skipping disputes because they feel confrontational.** A disputed finding documented with evidence is a gift to the next review run. An accepted-and-ignored finding is a bug waiting to happen.
- **Deferring Critical findings.** Never. Critical = `fix-now`, period.
- **Fixing Nits to "clean up" during respond-review.** Nits are `defer` by default. If the reviewer wanted them fixed, they would have flagged them Warning. Don't scope-creep the triage.
- **Fixing without reading the full file.** The review snippet is not the whole picture. Always read the file before editing.
- **Committing per fix.** One triage = one commit. Squash per the gate rule in CLAUDE.md.
- **Running `/sk:review` from inside this skill.** That's the gate's job. This skill triages, fixes, and returns.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:respond-review"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> Bucket classification and fix application both benefit from the main context model. Cheaper models miss dispute-vs-defer nuance.
