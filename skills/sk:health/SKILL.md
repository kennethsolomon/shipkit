---
name: sk:health
description: "Run harness self-audit and produce a health scorecard."
model: haiku
---

# /sk:health — Harness Self-Audit Scorecard

Deterministic scoring of your ShipKit setup across 7 categories. Produces a reproducible scorecard that identifies gaps and recommends improvements.

## Usage

```
/sk:health              # full scorecard
/sk:health --category <name>  # single category deep-dive
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> File checks + arithmetic — haiku is sufficient.

## Scoring Categories

Each category scores 0-10. Maximum total: 70.

### 1. Tool Coverage (0-10)

Check for presence and completeness of:

| Check | Points |
|-------|--------|
| `.claude/hooks/` exists with 6+ hooks | +2 |
| `.claude/agents/` exists with 4+ agents | +2 |
| `.claude/rules/` exists with 1+ rules | +1 |
| `commands/sk/` or `.claude/commands/sk/` has 10+ commands | +2 |
| MCP servers configured | +1 |
| Statusline configured in settings.json | +1 |
| Permissions deny list has 3+ entries | +1 |

### 2. Context Efficiency (0-10)

| Check | Points |
|-------|--------|
| CLAUDE.md exists and is <250 lines | +2 (>250: +1, >400: 0) |
| No duplicate instructions across CLAUDE.md and skills | +2 |
| MCP tools total <40 | +2 (40-60: +1, >60: 0) |
| Skills total <60 | +2 (>60: +1, >80: 0) |
| Agent descriptions all <200 lines | +2 |

### 3. Quality Gates (0-10)

| Check | Points |
|-------|--------|
| Lint configured (package.json scripts or Makefile) | +2 |
| Test runner configured | +2 |
| Security check available (npm audit, composer audit, etc.) | +2 |
| E2E test config exists (playwright.config, cypress.config) | +2 |
| Code review skill available | +2 |

### 4. Memory Persistence (0-10)

| Check | Points |
|-------|--------|
| `tasks/findings.md` exists and has content | +2 |
| `tasks/lessons.md` exists and has content | +2 |
| `tasks/progress.md` exists | +1 |
| `tasks/tech-debt.md` exists | +1 |
| `tasks/cross-platform.md` exists | +1 |
| Session hooks active (session-start.sh, session-stop.sh) | +2 |
| `.claude/sessions/` directory exists | +1 |

### 5. Eval Coverage (0-10)

| Check | Points |
|-------|--------|
| Test directory exists (`tests/`, `test/`, `spec/`, `__tests__/`) | +2 |
| Test assertions exist (grep for assert/expect/test/it/describe) | +2 |
| Coverage config exists (jest.config coverage, phpunit coverage) | +2 |
| `.claude/evals/` directory exists with eval definitions | +2 |
| CI/CD runs tests (`.github/workflows/` with test step) | +2 |

### 6. Security Guardrails (0-10)

| Check | Points |
|-------|--------|
| validate-commit hook exists | +2 |
| validate-push hook exists | +2 |
| config-protection hook exists | +2 |
| Deny rules in settings.json (3+ patterns) | +2 |
| safety-guard hook exists | +2 |

### 7. Cost Efficiency (0-10)

| Check | Points |
|-------|--------|
| Model routing configured (`.shipkit/config.json` exists) | +3 |
| Compact suggestions active (suggest-compact hook) | +2 |
| Cost tracker active (cost-tracker hook) | +2 |
| Context budget recently audited (`/sk:context-budget` run) | +3 |

## Output Format

```
=== ShipKit Health Scorecard ===

  Tool Coverage:        8/10  ||||||||..
  Context Efficiency:   7/10  |||||||...
  Quality Gates:       10/10  ||||||||||
  Memory Persistence:   6/10  ||||||....
  Eval Coverage:        4/10  ||||......
  Security Guardrails:  8/10  ||||||||..
  Cost Efficiency:      5/10  |||||.....
  ─────────────────────────────────
  Total:               48/70  (69%)

  Rating: GOOD

Findings:
  [MISSING] No .claude/evals/ directory — no formal eval definitions
  [MISSING] No CI/CD test step detected
  [MISSING] Context budget never audited
  [WEAK]    Only 4 hooks installed (recommended: 8+)

Top 3 Actions:
  1. Run /sk:eval define to create eval definitions (+4 points)
  2. Add CI/CD test workflow (+2 points)
  3. Run /sk:context-budget to audit token usage (+3 points)
```

### Rating Scale

| Score | Rating |
|-------|--------|
| 60-70 | EXCELLENT |
| 45-59 | GOOD |
| 30-44 | FAIR |
| 15-29 | NEEDS WORK |
| 0-14 | CRITICAL |
