# Steal Adaptations: Intensity Routing, Skill Benchmarks, Plugin Distribution

**Date:** 2026-04-06
**Source:** [socrates-skill](https://github.com/RoundTable02/socrates-skill) + [caveman](https://github.com/JuliusBrussee/caveman)
**Scope:** Cross-cutting (config, autopilot, gates, review, explain, start, eval, skill-creator, CI)

---

## Changes

### 1. Anti-Pattern Blocks (from Socrates)
- **What:** Added "Anti-Patterns Section" guidance to `skills/sk:skill-creator/SKILL.md`
- **Why:** Skills that define only positive behavior miss subtle failure modes. Explicit NEVER-do lists improve reliability.
- **Impact:** All future skills created via `/sk:skill-creator` get prompted to include anti-patterns.

### 2. Auto-Clarity Escape Hatch (from Caveman)
- **What:** Added "Auto-Clarity Escape Hatch" guidance to `skills/sk:skill-creator/SKILL.md`
- **Why:** Style-modifying skills (compression, formatting) may compress security warnings into ambiguous fragments.
- **Impact:** Skills that modify output style are guided to define when to temporarily disable themselves.

### 3. Intensity Levels (config + per-phase auto-select)
- **What:** New `intensity` and `intensity_overrides` fields in `.shipkit/config.json`. Per-phase auto-select in autopilot. `--intensity` flag on `/sk:start`. Intensity sections in sk:review, sk:explain, sk:gates.
- **Why:** Different workflow phases need different verbosity. Gates need one-liners; review needs exhaustive detail.
- **Impact:** Follows existing `profile` + `model_overrides` pattern. Three levels: lite/full/deep.
- **Resolution order:** `intensity_overrides["sk:<phase>"]` > phase auto-select > global `intensity` > `full`

### 4. Skill Benchmark Harness (from Caveman)
- **What:** New `benchmark` subcommand on `/sk:eval`. Runs identical prompts with/without a skill, measures token delta and quality.
- **Why:** No way to quantitatively measure skill effectiveness before this.
- **Impact:** New files: `.claude/evals/<skill>/prompts.json`, `.claude/evals/<skill>/results/`

### 5. Multi-Format Plugin Distribution (from Caveman)
- **What:** New `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, enriched `.claude-plugin/plugin.json`. CI workflow `.github/workflows/sync-skills.yml` to auto-sync versions.
- **Why:** ShipKit only distributed via npm. Adding Codex and Agents marketplace formats expands reach.
- **Impact:** Three plugin manifests auto-synced from `package.json` version on push to main.

---

## Files Changed

| File | Change |
|------|--------|
| `.shipkit/config.json` | Added `intensity`, `intensity_overrides` fields |
| `skills/sk:skill-creator/SKILL.md` | Added anti-patterns + auto-clarity writing guide sections |
| `skills/sk:autopilot/SKILL.md` | Added intensity routing section with per-phase table |
| `skills/sk:start/SKILL.md` | Added `--intensity` override flag |
| `skills/sk:review/SKILL.md` | Added intensity section (default: deep) |
| `skills/sk:explain/SKILL.md` | Added intensity section |
| `skills/sk:gates/SKILL.md` | Added intensity section (default: lite) |
| `skills/sk:eval/SKILL.md` | Added `benchmark` subcommand |
| `.claude-plugin/plugin.json` | Enriched with version, skills path |
| `.codex-plugin/plugin.json` | New — Codex plugin manifest |
| `.agents/plugins/marketplace.json` | New — Agents marketplace manifest |
| `.github/workflows/sync-skills.yml` | New — CI version sync workflow |
| `.claude/docs/maintenance-guide.md` | Added intensity + plugin manifest sections |
| `CLAUDE.md` | Updated eval command description |
| `commands/sk/help.md` | Updated eval description, start flag, added intensity docs |
| `skills/sk:setup-claude/templates/CLAUDE.md.template` | Updated eval command description |
| `docs/FEATURES.md` | Bumped spec dates, added sk-skill-creator + sk-eval entries |
| `docs/sk:features/sk-autopilot.md` | Added intensity routing section |
| `docs/sk:features/sk-explain.md` | Added intensity section |
| `docs/sk:features/sk-gates.md` | Added intensity section |
| `docs/sk:features/sk-start.md` | Added --intensity flag |
| `docs/sk:features/sk-skill-creator.md` | New — full feature spec |
| `docs/sk:features/sk-eval.md` | New — full feature spec |
| `docs/dashboard.html` | Updated eval command description |
