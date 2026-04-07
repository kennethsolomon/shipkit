---
name: sk:investigate
description: "Read-only feature-area exploration. Maps the existing terrain before you decide what to build. Runs before /sk:brainstorm when the task touches an unfamiliar area of the codebase. Outputs tasks/investigation.md."
allowed-tools: Read, Glob, Grep, Bash, Agent
---

# Investigate

Read-only feature-area exploration. Map the existing terrain so the brainstorm that follows starts from a base of facts, not assumptions.

<HARD-GATE>
Do NOT write code, modify source files, run migrations, or create plans. This skill only reads the codebase and writes a single findings report to `tasks/investigation.md`.
</HARD-GATE>

## When to Use

- Task touches an unfamiliar area: "add X to the billing module", "modify the notifications flow", "extend the auth middleware"
- Task references a system area without scope: "the dashboard", "our import pipeline", "the webhook system"
- Brownfield entry: you need to understand what exists before designing what to add
- User says "look around first", "explore the code", "investigate", "map out how X works"

## When NOT to Use

- Task has concrete anchors (specific file paths, function names, line numbers) — skip to `/sk:brainstorm` or `/sk:debug`
- Bug fix with a known cause — use `/sk:debug`
- Bug with unknown root cause — use `/sk:deep-dive` (which has its own trace lanes)
- Greenfield feature with no existing code to map — skip to `/sk:brainstorm`

## Difference from Other Skills

| Skill | Answers |
|-------|---------|
| `/sk:investigate` | **What exists?** (read-only terrain map) |
| `/sk:brainstorm` | **What should we build?** (design refinement) |
| `/sk:deep-interview` | **What do we actually want?** (requirements) |
| `/sk:deep-dive` | **Why is this broken?** (root cause for unknown bugs) |
| `/sk:debug` | **How do I fix this known bug?** (fix planning) |

`/sk:investigate` feeds `/sk:brainstorm` — it produces the factual grounding that brainstorm would otherwise have to assume.

---

## Steps

### 1. Parse the investigation target

From the task description, identify the **feature area** to map. Examples:
- "add notifications to billing" → area = `billing` + `notifications`
- "how does our OAuth flow work" → area = `oauth`
- "extend the webhook dispatch system" → area = `webhooks`

If the area is ambiguous, ask one clarifying question (multiple choice) before proceeding. Do not ask about requirements — only about which part of the code to map.

### 2. Dispatch 3 parallel Explore agents

Launch three read-only Explore agents in parallel via the Agent tool. Give each a focused lane so they do not duplicate work.

**Lane A — Entry points & routing:**
> "Read-only. Find the entry points for the [area] feature: routes, controllers, API endpoints, CLI commands, UI pages, background jobs, event listeners. List the file paths, the URL/event/command names, and the handler function that owns each entry point. Do not read implementation details yet. Return a plain markdown list."

**Lane B — Data model & persistence:**
> "Read-only. For the [area] feature, find: database tables/collections involved, ORM models, migrations that created them, key foreign-key relationships, and any in-memory caches or queues. For each table, note the file path of the model and the fields that matter for this feature. Return a plain markdown list."

**Lane C — Tests & existing patterns:**
> "Read-only. For the [area] feature, find: existing tests (unit, integration, E2E), fixtures/factories, and the conventions used (test framework, mocking patterns, setup/teardown). List file paths and describe the test style. Also note any feature flags, config toggles, or environment variables that gate this area. Return a plain markdown list."

Wait for all three lanes to complete. If any agent fails, proceed with what you have — do not retry indefinitely.

### 3. Read the critical files identified

From the three agent reports, select the 3-5 most load-bearing files (entry point + primary model + primary test). Read them in the main context so the brainstorm that follows can reason about real code, not summaries.

Do not read more than 5 files at this stage — the goal is grounding, not exhaustive understanding.

### 4. Check for prior context

Read these files if they exist:
- `tasks/findings.md` — prior decisions in this repo
- `tasks/lessons.md` — known pitfalls (apply as constraints for the brainstorm that follows)
- `tasks/cross-platform.md` — cross-platform impact surfaces
- `docs/decisions.md` — prior ADRs that touch this area

Note any relevant entries. Do not re-derive what the codebase already answers.

### 5. Write `tasks/investigation.md`

Write a single findings report. Structure:

```markdown
# Investigation: [area name]

**Date:** YYYY-MM-DD
**Scope:** [1-line description of what was mapped]
**Status:** complete

## Entry Points

| Type | Name | File | Handler |
|------|------|------|---------|
| Route | `GET /api/billing/invoices` | `app/Http/Controllers/InvoiceController.php:24` | `InvoiceController@index` |
| Job | `SendInvoiceEmail` | `app/Jobs/SendInvoiceEmail.php:12` | — |

## Data Model

| Table/Model | File | Key fields | Relationships |
|-------------|------|-----------|---------------|
| `invoices` | `app/Models/Invoice.php` | `id`, `user_id`, `amount_cents`, `status` | belongsTo User, hasMany LineItems |

## Existing Tests

| Layer | File | Style | Notes |
|-------|------|-------|-------|
| Feature | `tests/Feature/BillingTest.php` | Pest, DB transactions | Covers happy path; no refund test |

## Config & Flags

| Name | File | Purpose |
|------|------|---------|
| `BILLING_ENABLED` | `.env.example` | Gates the whole feature |

## Load-Bearing Files Read

- `app/Http/Controllers/InvoiceController.php` — thin; delegates to BillingService
- `app/Services/BillingService.php` — holds the charge/refund logic (180 lines)
- `tests/Feature/BillingTest.php` — reference for the test style expected

## Prior Decisions Referenced

- `docs/decisions.md` 2026-01-14: decided to use Stripe webhooks over polling
- `tasks/lessons.md` 2026-02-03: never cache invoice amounts — always read from Stripe

## Unknowns / Open Questions

- Is the refund flow covered by existing tests? *(no — gap found)*
- How does the retry policy for failed charges work? *(not obvious from the handler — needs a brainstorm discussion)*

## Entry Points for the Brainstorm

Recommended starting point for `/sk:brainstorm`: [one-line directional hint — e.g., "The refund path is the least-covered and most risky area to extend."]
```

### 6. Transition

Tell the user:
> "Investigation written to `tasks/investigation.md`. `/sk:brainstorm` will read it automatically. Proceeding to brainstorm — run `/sk:brainstorm` or let the workflow advance."

If invoked by `/sk:start` or `/sk:autopilot`: return silently — the caller continues automatically.

---

## Rules

- **Read-only.** Never write, edit, or run migrations. Only file that gets written is `tasks/investigation.md`.
- **Bounded.** Three parallel lanes, up to 5 load-bearing file reads. Investigation is not a code audit — it is grounding.
- **No requirements questions.** Requirements belong to brainstorm/deep-interview. Investigate only asks "which part of the code?" if the area is ambiguous.
- **No design proposals.** Do not propose architectures. The report is factual. The directional hint in step 5 is at most one sentence.
- **Always produce `tasks/investigation.md`.** Even if the three lanes return sparse results — a sparse report is still useful signal ("this area has no tests" is itself a finding).

## Anti-Patterns

- **Reading 30 files to "be thorough."** Stop at 5. Brainstorm and plan will read more as they need to.
- **Writing findings for the whole codebase.** Scope is the feature area, not the repo.
- **Asking requirements questions.** That is the job of deep-interview/brainstorm.
- **Proposing solutions.** The report maps terrain; it does not draw roads.
- **Running in parallel with brainstorm.** Investigate runs **before** brainstorm — the output feeds brainstorm as pre-read context.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:investigate"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit. Parallel Explore agents should use the same resolved model.
