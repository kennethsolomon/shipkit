---
name: sk:context-budget
description: "Audit context window token consumption and find optimization opportunities."
---

# /sk:context-budget — Token Consumption Audit

Audits all components that consume context window tokens — agents, skills, rules, MCP tools, CLAUDE.md — and identifies optimization opportunities.

## Usage

```
/sk:context-budget              # standard audit
/sk:context-budget --verbose    # per-file breakdown
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Counting and classification is lightweight — haiku is sufficient.

## How It Works

### Phase 1: Inventory

Scan and count token estimates for every loaded component:

| Component | Location | Token Estimation |
|-----------|----------|------------------|
| CLAUDE.md | `CLAUDE.md` | `words * 1.3` |
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | `words * 1.3` |
| Skills | `skills/*/SKILL.md` | `words * 1.3` |
| Commands | `commands/**/*.md` | `words * 1.3` |
| Agents | `.claude/agents/*.md` | `words * 1.3` |
| Rules | `.claude/rules/*.md` | `words * 1.3` |
| MCP tool schemas | count tools * ~500 tokens each | `tool_count * 500` |
| Hooks | `.claude/hooks/*.sh` (minimal overhead) | `words * 1.3` |

**Token estimation formula:**
- Prose/markdown: `word_count * 1.3`
- Code blocks: `char_count / 4`
- MCP tool schemas: ~500 tokens per tool definition

### Phase 2: Classify Usage Frequency

For each component, classify how often it's actually needed:

| Classification | Meaning | Action |
|---------------|---------|--------|
| **Always** | Loaded every session, always relevant | Keep as-is |
| **Sometimes** | Relevant to specific task types | Consider conditional loading |
| **Rarely** | Edge case, rarely triggered | Candidate for removal/extraction |

Classification heuristics:
- Skills used in the workflow (brainstorm, write-tests, gates, etc.) → Always
- Skills triggered by keywords (frontend-design, api-design) → Sometimes
- Niche skills (seo-audit, schema-migrate) → Rarely
- MCP tools: if >20 tools on one server → flag as over-subscribed

### Phase 3: Detect Issues

Flag these common problems:

1. **Bloated agents** — agent descriptions >200 lines
2. **Bloated skills** — skill definitions >400 lines
3. **Bloated rules** — rule files >100 lines
4. **MCP over-subscription** — servers with >20 tools (each costs ~500 tokens)
5. **CLI-wrapping MCPs** — MCP servers that just wrap CLI tools (overhead > benefit)
6. **Duplicate content** — same instructions in CLAUDE.md AND skill files
7. **CLAUDE.md bloat** — CLAUDE.md >200 lines (the target)
8. **Unused components** — skills/agents never referenced in workflow

### Phase 4: Report

Output a structured report:

```
=== Context Budget Audit ===

Component Breakdown:
  CLAUDE.md              ~1,200 tokens
  Global CLAUDE.md         ~800 tokens
  Skills (42 files)     ~18,000 tokens
  Commands (35 files)    ~8,000 tokens
  Agents (8 files)       ~3,200 tokens
  Rules (5 files)        ~1,500 tokens
  MCP tools (3 servers)  ~15,000 tokens (30 tools)
  ─────────────────────────────────
  Total overhead:        ~47,700 tokens

Context window:          200,000 tokens
Overhead:                 47,700 tokens (23.8%)
Available for work:      152,300 tokens

Issues Found:
  [HIGH]   MCP server "playwright" has 28 tools (~14,000 tokens)
  [MEDIUM] Skill sk:frontend-design is 380 lines (~500 tokens)
  [LOW]    Agent perf-auditor has 220 lines (~290 tokens)

Top 3 Optimizations:
  1. Remove unused MCP tools from playwright (save ~7,000 tokens)
  2. Consolidate duplicate workflow instructions (save ~1,200 tokens)
  3. Trim agent descriptions to <150 lines (save ~400 tokens)

  Potential savings: ~8,600 tokens (18% reduction)
```

### --verbose Mode

Adds per-file token breakdown:

```
Skills Breakdown:
  sk:autopilot/SKILL.md        ~620 tokens
  sk:brainstorm/SKILL.md       ~480 tokens
  sk:gates/SKILL.md            ~440 tokens
  ...
```
