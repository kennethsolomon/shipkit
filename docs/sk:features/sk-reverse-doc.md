# /sk:reverse-doc

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Standalone
> **Command:** `/sk:reverse-doc <type> <path>`
> **Skill file:** `skills/sk:reverse-doc/SKILL.md`

---

## Overview

Generate architecture, design, or API documentation from existing code by analyzing patterns, tracing data flow, and asking clarifying questions. Works backwards from implementation to create missing docs — distinguishes between what the code does and what the developer intended.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| `<type>` argument | `architecture`, `design`, or `api` | No (inferred from path) |
| `<path>` argument | Target directory or file to document | Yes |
| User answers | Clarifying questions about intent | Yes (interactive) |
| `.shipkit/config.json` | Model routing profile | No |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| Architecture Decision Record | `docs/architecture/` | When type is `architecture` |
| Design document (GDD-style) | `docs/design/` | When type is `design` |
| API specification | `docs/api/` | When type is `api` |
| Follow-up work list | Terminal (stdout) | Suggested next steps, not auto-executed |

---

## Business Logic

1. **Infer type** (if not provided) — map path to doc type:
   - `src/core/`, `src/lib/`, `app/Services/` -> architecture
   - `src/components/`, `resources/views/` -> design
   - `routes/`, `app/Http/Controllers/` -> api

2. **Phase 1: Analyze** — launch 3 parallel Explore agents:
   - Structure agent: map file tree, identify entry points, trace dependency chains
   - Patterns agent: identify design patterns, abstractions, conventions
   - Data flow agent: trace inputs through transformations to outputs
   - Synthesize into: what it does, how it's built, what's unclear

3. **Phase 2: Clarify** — ask user 3-5 clarifying questions to distinguish intentional design from accidental implementation. Example questions:
   - "Is [pattern X] intentional, or would you change it in a refactor?"
   - "What was the motivation for [architectural decision Y]?"
   - "Are [components A and B] coupled by design, or is that tech debt?"

4. **Phase 3: Draft** — generate the document based on analysis + user answers:
   - Architecture: system overview, component diagram, data flow, design decisions with rationale, dependencies, trade-offs
   - Design: feature overview, component breakdown, state management, interaction patterns, edge cases
   - API: endpoint inventory, request/response schemas, auth requirements, error codes, rate limits

5. **Phase 4: Approve** — present draft to user, highlight sections marked as "inferred" (not confirmed), ask for corrections or additions.

6. **Phase 5: Write** — save approved document. Flag follow-up work: related areas needing docs, inconsistencies found, suggested refactoring.

---

## Hard Rules

- Never assume intent — always ask before documenting "why"
- Do not write the file until the user approves the draft
- Do not auto-execute follow-up work — present as a list for the user to decide
- Sections based on inference (not user-confirmed) must be marked as "inferred"
- Clarify phase (Phase 2) cannot be skipped — it is the core value of the skill

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Path does not exist | Error with: "Path not found: [path]" |
| Path is a single file | Analyze that file only; adjust scope of analysis agents |
| Type cannot be inferred from path | Ask user: "What type of doc? (architecture / design / api)" |
| Empty directory | Error with: "No code found at [path]" |
| User rejects draft | Ask for specific corrections; revise and re-present |

---

## Error States

| Condition | Error message / behavior |
|-----------|--------------------------|
| Path not found | Stop with: "Path not found: [path]" |
| No code files in path | Stop with: "No code found at [path] — nothing to document" |
| User provides no answers to clarifying questions | Proceed with all "why" sections marked as "inferred — not confirmed" |
| Write permission denied | Stop with filesystem error context |

---

## UI/UX Behavior

### CLI Output
Interactive multi-phase flow: analysis summary, clarifying questions, draft presentation, approval prompt, then file write.

### When Done
```
Document saved to docs/[type]/[name].md
Follow-up suggestions:
- [related area needing docs]
- [inconsistency found]
- [suggested refactoring]
```

---

## Platform Notes

N/A — CLI tool only.

---

## Related Docs

- `skills/sk:reverse-doc/SKILL.md` — full implementation spec
- `/sk:brainstorm` — for forward documentation (design before code)
- `/sk:api-design` — for designing new APIs (vs. documenting existing ones)
- `/sk:frontend-design` — for designing new UI (vs. documenting existing ones)
