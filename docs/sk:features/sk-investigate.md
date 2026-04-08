# /sk:investigate

> **Status:** Shipped
> **Type:** Skill
> **Workflow Position:** Step 0.5 (auto-skip — runs before brainstorm for unfamiliar brownfield areas)
> **Command:** `/sk:investigate`
> **Skill file:** `skills/sk:investigate/SKILL.md`

---

## Overview

Read-only feature-area exploration that maps an unfamiliar brownfield subsystem before `/sk:brainstorm` runs. Dispatches 3 parallel Explore agents across three lanes (entry points, data model, tests + config), reads 3-5 load-bearing files max, and writes a structured `tasks/investigation.md` report. Output includes **god nodes** (top 3-5 most-referenced files in the area) and **suggested questions** (4-5 questions the terrain map is uniquely positioned to answer).

**Hard gate:** no code changes. The only file investigate writes is `tasks/investigation.md`.

Adapted from [gstack](https://github.com/garrytan/gstack)'s sprint-start review pattern — the insight that a dedicated read-only mapping phase produces deeper plans than starting brainstorm cold.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Task description | User prompt or `tasks/spec.md` | Yes |
| `tasks/findings.md` | Project memory — prior discoveries | No (read if present) |
| `tasks/lessons.md` | Project memory — accumulated lessons | No (read if present) |
| `docs/decisions.md` | Architectural decision records | No (read if present) |

---

## Outputs

| Output | Destination | Notes |
|--------|-------------|-------|
| `tasks/investigation.md` | Project root | Structured report with 7 sections (entry points, data model, tests, config, god nodes, unknowns, suggested questions) |
| Terminal summary | stdout | Lists files read, lanes completed, next action |

---

## Business Logic

### Parallel Lane Dispatch

Three Explore agents run simultaneously with bounded file budgets:

| Lane | Focus | File budget |
|------|-------|-------------|
| **A: Entry points** | Routes, controllers, CLI commands, event listeners — how the subsystem is invoked | 2 files |
| **B: Data model** | Models, migrations, schemas, DTOs — what the subsystem owns or touches | 2 files |
| **C: Tests + config** | Existing tests, config/env keys, feature flags | 1-2 files |

Total hard cap: 5 load-bearing files. This keeps token cost predictable regardless of subsystem size.

### Cross-Reference Pass

After the lane reports come back, investigate checks `tasks/findings.md`, `tasks/lessons.md`, and `docs/decisions.md` for prior context:

- **Findings** — past discoveries about this area (e.g., "the billing module uses Stripe webhooks, not polling")
- **Lessons** — mistakes to avoid ("don't mock Stripe SDK in tests")
- **Decisions** — architectural commitments ("we chose Sanctum over Passport")

Anything found is quoted in the Prior Decisions section of the report.

### Report Structure

`tasks/investigation.md` is written with 5 tables:

1. **Entry Points** — file:line + one-line description per invocation path
2. **Data Model** — models/tables with key fields and relationships
3. **Tests** — existing test coverage and gaps
4. **Config** — env keys, feature flags, external dependencies
5. **Prior Decisions** — quotes from findings/lessons/decisions

---

## Hard Rules

1. **Read-only.** Never edit source code. Never run migrations. Never modify config.
2. **File budget is non-negotiable.** If a lane wants to read a 6th file, it reports "file budget exhausted" instead.
3. **No speculation.** The report only contains things grounded in files actually read. No "probably" or "should be".
4. **Brainstorm reads the output.** `/sk:brainstorm` auto-loads `tasks/investigation.md` if present — investigate is the upstream feeder, not a standalone command.

---

## Auto-Skip Rules

Investigate is auto-skipped by `/sk:start` and `/sk:autopilot` when ANY of these conditions match:

- Task description has concrete anchors (file paths like `app/Models/User.php`, function names, line numbers)
- Repo is greenfield (no `package.json`/`composer.json`/`go.mod`/`Cargo.toml` detected)
- Task is a bug flow (`/sk:deep-dive` owns its own investigation)
- User passed `--skip-investigate` flag
- `tasks/investigation.md` already exists and was written within the last 4 hours

---

## Unfamiliar-Area Signals (when to run)

`/sk:start` triggers investigate when the task matches all of these:

| Signal | Example |
|--------|---------|
| Subsystem reference | "the billing module", "our auth flow", "the webhook system" |
| Exploration verb | "add to", "extend", "modify", "touch", "work on", "how does", "explore", "figure out", "map out" |
| Brownfield | Repo has a manifest + src directory |
| No concrete anchors | No file paths, function names, or line numbers in the task |

Override with `/sk:start --investigate <task>` to force-run or `--skip-investigate` to bypass.

---

## Edge Cases

| Case | Behavior |
|------|----------|
| Subsystem doesn't exist (hallucinated area name) | Report "no matching files found" and return without writing investigation.md — let brainstorm flag it |
| Subsystem is too large (>20 matching files) | Each lane picks the most load-bearing file and notes "partial coverage — N files not read" |
| Conflicting findings between lanes | Report both, let brainstorm resolve |
| `tasks/` directory missing | Create it before writing investigation.md |

---

## UI Behavior

- **Intensity:** `lite` in autopilot (factual mapping, not essays). Full mode available via config override.
- **Output format:** Tables, not prose
- **Auto-advance:** Yes — autopilot continues to brainstorm after investigate completes. No user prompt.
- **Manual mode (`/sk:start`):** Shows a one-line summary ("Mapped 5 files across 3 lanes") and continues to brainstorm.

---

## Model Routing

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

Investigate is factual work — sonnet handles it well at balanced profile. Budget drops to haiku since table generation from file reads is mechanical.

---

## Related Files

- `skills/sk:investigate/SKILL.md` — implementation contract
- `commands/sk/investigate.md` — thin command wrapper
- `skills/sk:start/SKILL.md` — unfamiliar-area detection + routing
- `skills/sk:autopilot/SKILL.md` — Step 0.5 block
- `skills/sk:brainstorm/SKILL.md` — reads `tasks/investigation.md` if present
- `CLAUDE.md` — Step 0.5 row in workflow table
