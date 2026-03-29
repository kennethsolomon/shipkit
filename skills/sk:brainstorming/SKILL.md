---
name: sk:brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation."
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
---

# Brainstorming Ideas Into Designs

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, or scaffold until the user approves the design. Every project — no matter how simple — goes through this process. The design can be short, but it MUST be presented and approved.
</HARD-GATE>

## Steps

1. **Explore context** — read `tasks/findings.md` and `tasks/lessons.md` if they exist. Summarize prior decisions; ask extend/revise/fresh? Do not re-explore what is already decided. Apply every active lesson as a design constraint. Check files, docs, recent commits.
2. **Ask clarifying questions** — one per message, prefer multiple choice. Focus on purpose, constraints, success criteria.
3. **Architecture assessment** (complex tasks only) — if task spans multiple systems, requires data modeling/API contracts, 3+ components, or touches auth/billing: invoke the `architect` agent with: "Read tasks/findings.md, tasks/lessons.md, tasks/tech-debt.md, explore relevant code. Propose 2-3 architecturally sound approaches for [task] with trade-offs. Read-only." Incorporate into step 5.
4. **Search-First Research** — before proposing approaches:

   | Check | Action | Decision |
   |-------|--------|----------|
   | Grep codebase | Similar functionality exists? | **Adopt** (90%+) · **Extend** (60-90%) · **Build** (<60%) |
   | Package registries | Well-maintained package? | Include as approach option |
   | Existing skills/MCPs | ShipKit skill handles this? | Include as approach option |

5. **Propose 2-3 approaches** — with trade-offs; lead with recommendation and reasoning.
6. **Present design** — scale each section to complexity. Ask after each section. Cover: architecture, components, data flow, error handling, testing.
7. **Write findings** — save to `tasks/findings.md` (problem statement, decisions, approach + rationale, open questions). Append ADR to `docs/decisions.md` (see below). Optionally: `docs/plans/YYYY-MM-DD-<topic>-design.md`. Commit all.
8. **Transition** — invoke `/sk:write-plan`. Do NOT invoke any other skill.

## Decisions Log

After writing findings, **append** an ADR entry to `docs/decisions.md`. This file is **cumulative and append-only** — never overwrite or remove existing entries.

### If `docs/decisions.md` does not exist

Create it with this header first:

```markdown
# Architecture Decision Records

A cumulative log of key design decisions made across features. Append-only — never overwrite.
```

### ADR Entry Format

```markdown
## [YYYY-MM-DD] [Feature/Task Name]

**Context:** [problem being solved — 1-2 sentences]
**Decision:** [chosen approach — 1 sentence]
**Rationale:** [why this approach over alternatives]
**Consequences:** [trade-offs accepted]
**Status:** accepted
```

### Rules

- **Append-only** — never edit or delete existing entries
- **One entry per brainstorm** — each completed brainstorm adds exactly one ADR entry
- **Absolute dates only** — always `YYYY-MM-DD`

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:brainstorming"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
