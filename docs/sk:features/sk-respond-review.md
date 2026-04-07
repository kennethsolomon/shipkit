# /sk:respond-review

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Sub-routine — auto-invoked by `/sk:gates` Batch 3; also available standalone
> **Command:** `/sk:respond-review`
> **Skill file:** `skills/sk:respond-review/SKILL.md`

---

## Overview

Triage `/sk:review` findings into three buckets (`fix-now`, `defer`, `dispute`) and apply each bucket's action. Auto-invoked by `/sk:gates` Batch 3 when the code-reviewer returns any Critical or Warning finding. Also available as a standalone command after a bare `/sk:review`.

Without triage, every Critical or Warning blocks gates equally — causing churn on cosmetic or cross-file refactor suggestions. Respond-review classifies findings first, fixes second.

Adapted from [obra/superpowers](https://github.com/obra/superpowers)'s review-loop pattern.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Review findings | stdout of `/sk:review` or `code-reviewer` agent report | Yes |
| Working tree diff | `git diff` against base branch | Yes |
| `tasks/tech-debt.md` | Deferred items log | No (created if absent) |
| `tasks/review-disputes.md` | Disputed findings log | No (created if absent) |
| `tasks/findings.md`, `docs/decisions.md` | For dispute justification | No (read if present) |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Fix-now commit | Git history | One squash commit per triage batch |
| `tasks/tech-debt.md` entries | Project memory | Deferred findings with context |
| `tasks/review-disputes.md` entries | Project memory | Disputed findings with reasoning |
| Return status | stdout | `READY_TO_RERUN` or `BLOCKED` |

---

## Business Logic

### Triage Buckets

| Bucket | Criteria | Action |
|--------|----------|--------|
| **fix-now** | Critical severity, OR Warning in safety path (auth/payments/PII), OR localized <10-line change | Apply fix via Edit, squash-commit |
| **defer** | Cross-file refactor, non-safety, or suggestion without concrete line reference | Log to `tasks/tech-debt.md` with severity, file, reason |
| **dispute** | Reviewer misread the code, contradicts a documented decision, or finding is already addressed | Log to `tasks/review-disputes.md` with evidence + rationale |

### Conservative Default

When a finding is ambiguous, prefer this order: `fix-now > defer > dispute`.

Fixing is always safer than deferring. Deferring is safer than disputing. Disputes should be rare and well-justified — reviewers are usually right even when they seem wrong.

### Fix-Now Protocol

For each fix-now finding:

1. Read the file at the finding's location
2. Confirm the finding still applies (reviewer may reference stale code)
3. Apply the minimal fix via Edit
4. If the fix introduces a logic change (new branch, condition, algorithm), follow Fix & Retest Protocol:
   - Update/add failing tests
   - Run `/sk:test` at 100% coverage
   - Commit tests+fix together
5. After all fix-now findings are addressed, create one squash commit: `fix(review): resolve review findings batch N`

### Defer Logging

Append to `tasks/tech-debt.md` with this format:

```
## [YYYY-MM-DD] [Finding title]
- **Severity:** Critical | Warning
- **File:** path/to/file.php:42
- **Reason deferred:** <why>
- **Effort:** Low | Medium | High
```

### Dispute Logging

Append to `tasks/review-disputes.md` with this format:

```
## [YYYY-MM-DD] [Finding title]
- **Reviewer claim:** <what the reviewer said>
- **Our response:** <rebuttal with evidence>
- **Evidence:** <file:line references or decision doc quote>
```

### Same-Finding Escalation

If the same file:line finding survives two consecutive Batch 3 attempts:

1. Invoke the `architect` agent with the finding + the two attempted fixes
2. Architect proposes a different approach
3. Apply architect's fix, commit, re-run Batch 3

If the same finding survives three consecutive attempts → trigger 3-strike protocol (stop, ask user).

### Return Status

After triage completes:

| Status | Meaning | Gates behavior |
|--------|---------|----------------|
| `READY_TO_RERUN` | All fix-now applied, defers/disputes logged | Re-run Batch 3 from scratch |
| `BLOCKED` | Fix-now failed or exceeded 3-strike | Trigger 3-strike protocol immediately |

---

## Hard Rules

1. **Never silently dismiss a finding.** Every finding must land in exactly one bucket with a visible log entry.
2. **Safety-path warnings are never deferred.** Auth, payments, and PII handling always route to fix-now regardless of scope.
3. **Cross-file refactors always defer.** Fix-now is for localized changes only — if the fix touches 3+ files, defer and create a tech-debt entry.
4. **Disputes require evidence.** A dispute entry with no file:line reference or decision doc quote is rejected — escalate to user.
5. **One squash commit per triage batch.** Don't create micro-commits per finding.

---

## Auto-Invocation Contract (gates Batch 3)

`/sk:gates` Batch 3 runs `code-reviewer`, then:

```
if review.findings.any(critical or warning):
    result = Skill("sk:respond-review")
    if result == READY_TO_RERUN:
        rerun_batch_3()  # max 3 total attempts
    elif result == BLOCKED:
        trigger_3_strike()
```

Respond-review owns the triage + fix loop. Gates owns the rerun + 3-strike loop. This separation keeps gates as the single source of re-run logic.

---

## Edge Cases

| Case | Behavior |
|------|----------|
| Reviewer output is malformed | Return `BLOCKED` with error message — don't guess |
| Finding references a file not in the diff | Check if it's a pre-existing issue; if so, defer with note "pre-existing — not introduced by this branch" |
| No findings at all | Return `READY_TO_RERUN` immediately (nothing to triage) |
| Triage produces zero fix-now items | Still return `READY_TO_RERUN` — defers and disputes don't require rerun, but gates needs the signal to advance |
| Same finding flagged by multiple reviewers (security + general) | Deduplicate by file:line:issue, apply once |

---

## UI Behavior

- **Intensity:** `deep` when auto-invoked by gates (security/perf findings need full detail). Configurable via `intensity_overrides`.
- **Output format:**
  ```
  === Respond Review: Triage Report ===
  Fix-now (3):
    - [Critical] POST /login missing rate limit → app/Http/Controllers/AuthController.php:42
    - [Warning] logout doesn't revoke tokens → app/Services/AuthService.php:108
    - [Critical] XSS in comment render → resources/views/comments.blade.php:15
  Defer (2):
    - [Warning] Extract OrderCalculator into service (cross-file refactor)
    - [Warning] Use dependency injection instead of facades (12 files)
  Dispute (1):
    - [Warning] "N+1 query on User::posts" — already eager-loaded at line 47, reviewer missed it

  Applying 3 fix-now items...
  ✓ AuthController.php:42 — added RateLimiter middleware
  ✓ AuthService.php:108 — added token->delete() in logout flow
  ✓ comments.blade.php:15 — escaped {{ $comment->body }}

  Squash commit: fix(review): resolve review findings batch 1
  Status: READY_TO_RERUN
  ```
- **Auto-advance:** Yes — in gates mode, returns status and lets gates handle the rerun decision.

---

## Model Routing

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

Triage requires judgment (severity classification, dispute evidence) — keeps sonnet minimum.

---

## Related Files

- `skills/sk:respond-review/SKILL.md` — implementation contract
- `commands/sk/respond-review.md` — thin command wrapper
- `skills/sk:gates/SKILL.md` — Batch 3 auto-invoke protocol
- `skills/sk:review/SKILL.md` — upstream (produces findings)
- `CLAUDE.md` — Fix & Retest Protocol row for review findings
- `tasks/tech-debt.md` — deferred findings log
- `tasks/review-disputes.md` — disputed findings log
