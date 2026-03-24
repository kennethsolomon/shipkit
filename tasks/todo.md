# TODO — 2026-03-24 — ECC-Inspired ShipKit Intelligence Upgrade

## Goal

Add 12 features inspired by the [everything-claude-code](https://github.com/affaan-m/everything-claude-code) repo to make ShipKit smarter about context, learning, safety, and session management. Single branch: `feat/ecc-intelligence-upgrade`.

## User Decisions

- Hooks installation: **prompt user** (opt-in, not auto-install) — both in `/sk:setup-claude` and `/sk:setup-optimizer`
- Session persistence: stored in **`.claude/sessions/`**
- Single branch, dependency-ordered milestones

## Constraints (from lessons.md)

- All commands use `/sk:` prefix
- Every new skill needs: SKILL.md, command .md, CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, CHANGELOG.md, lessons.md tracking entry, set-profile.md, setup-optimizer
- Never overwrite `tasks/lessons.md` — append only
- Skills are symlinked via `install.sh`

---

## Milestone 1: Tests (TDD Red Phase)

- [ ] Add assertions for **new hook templates** to `tests/verify-workflow.sh`:
  - `assert_file_exists` — `skills/sk:setup-claude/templates/hooks/config-protection.sh`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/hooks/post-edit-format.sh`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/hooks/console-log-warning.sh`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/hooks/cost-tracker.sh`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/hooks/suggest-compact.sh`
  - `assert_contains` — `settings.json.template` contains `"config-protection"`
  - `assert_contains` — `settings.json.template` contains `"console-log"`

- [ ] Add assertions for **`/sk:learn`**:
  - `assert_file_exists` — `skills/sk:learn/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"pattern"`
  - `assert_contains` — `SKILL.md` contains `"instinct"` or `"extract"`
  - `assert_contains` — `SKILL.md` contains `"confidence"`

- [ ] Add assertions for **`/sk:context-budget`**:
  - `assert_file_exists` — `skills/sk:context-budget/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"token"`
  - `assert_contains` — `SKILL.md` contains `"MCP"`
  - `assert_contains` — `SKILL.md` contains `"overhead"`

- [ ] Add assertions for **`/sk:save-session`** and **`/sk:resume-session`**:
  - `assert_file_exists` — `skills/sk:save-session/SKILL.md`
  - `assert_file_exists` — `skills/sk:resume-session/SKILL.md`
  - `assert_contains` — save `SKILL.md` contains `".claude/sessions/"`
  - `assert_contains` — resume `SKILL.md` contains `".claude/sessions/"`

- [ ] Add assertions for **`/sk:safety-guard`**:
  - `assert_file_exists` — `skills/sk:safety-guard/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"freeze"`
  - `assert_contains` — `SKILL.md` contains `"careful"`
  - `assert_contains` — `SKILL.md` contains `"destructive"`

- [ ] Add assertions for **`/sk:eval`**:
  - `assert_file_exists` — `skills/sk:eval/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"pass@k"` or `"pass@"`
  - `assert_contains` — `SKILL.md` contains `"capability"`
  - `assert_contains` — `SKILL.md` contains `"regression"`
  - `assert_contains` — `SKILL.md` contains `"grader"`

- [ ] Add assertions for **`/sk:health`**:
  - `assert_file_exists` — `skills/sk:health/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"scorecard"` or `"score"`
  - `assert_contains` — `SKILL.md` contains `"Context Efficiency"` or `"context"`
  - `assert_contains` — `SKILL.md` contains `"Quality Gates"` or `"gates"`

- [ ] Add assertions for **enriched `/sk:start`**:
  - `assert_contains` — `skills/sk:start/SKILL.md` contains `"Missing Context"` or `"missing context"`

- [ ] Add assertions for **documentation updates**:
  - `assert_contains` — `CLAUDE.md` contains `"/sk:learn"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:context-budget"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:health"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:eval"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:safety-guard"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:save-session"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:resume-session"`
  - `assert_contains` — `README.md` contains `"/sk:learn"`
  - `assert_contains` — `README.md` contains `"/sk:health"`

---

## Milestone 2: Enhanced Hooks (Features 1, 11, 12)

New hook scripts in `skills/sk:setup-claude/templates/hooks/`:

- [ ] Create `config-protection.sh` — PreToolUse hook for Edit/Write:
  - Detects edits to linter/formatter configs: `.eslintrc*`, `.prettierrc*`, `biome.json`, `phpstan.neon`, `pint.json`, `rector.php`, `.stylelintrc*`, `tsconfig.json`
  - Outputs warning: "BLOCKED: Modifying linter config. Fix the code instead of weakening the rules."
  - Exit code 2 to block the edit
  - Env var `SHIPKIT_ALLOW_CONFIG_EDIT=1` to override

- [ ] Create `post-edit-format.sh` — PostToolUse hook for Edit:
  - Auto-detects formatter: Biome (`biome.json`), Prettier (`.prettierrc*`), Pint (`pint.json`), `gofmt`, `cargo fmt`
  - Runs formatter on the edited file only
  - Silent on success, outputs only on error
  - Async (non-blocking)

- [ ] Create `console-log-warning.sh` — Stop hook:
  - Scans git-modified files for `console.log`, `console.warn`, `console.error`, `dd(`, `dump(`, `var_dump(`
  - Reports count and file locations if found
  - Non-blocking (warning only)

- [ ] Create `cost-tracker.sh` — Stop hook (async):
  - Appends session end timestamp + branch to `.claude/sessions/cost-log.jsonl`
  - Tracks session count per day
  - Lightweight — no token counting (not available via hooks)

- [ ] Create `suggest-compact.sh` — PreToolUse hook for Edit/Write:
  - Tracks tool call count in `/tmp/shipkit-tool-count-$$`
  - At threshold (50 calls), suggests: "Consider running /compact — you've made 50+ tool calls this session"
  - Repeats every 25 calls after threshold
  - `SHIPKIT_COMPACT_THRESHOLD` env var to configure
  - Non-blocking (exit 0)

- [ ] Update `settings.json.template` — wire 5 new hooks:
  - PreToolUse: config-protection (matcher: `Edit|Write`, timeout: 5000)
  - PostToolUse: post-edit-format (matcher: `Edit`, async: true, timeout: 10000)
  - Stop: console-log-warning (timeout: 10000)
  - Stop: cost-tracker (async: true, timeout: 5000)
  - PreToolUse: suggest-compact (matcher: `Edit|Write`, timeout: 3000)

- [ ] Update `skills/sk:setup-claude/SKILL.md` — add prompt for hooks:
  - After generating files, prompt: "Install lifecycle hooks? (config-protection, auto-format, console.log warning, compact suggestions) [y/n]"
  - If yes: deploy hooks + update settings.json
  - If no: skip hooks entirely
  - Document the prompt behavior in the SKILL.md

- [ ] Update `skills/sk:setup-optimizer/SKILL.md` — add hooks detection:
  - Diagnose step: check if `.claude/hooks/` exists and has the new hooks
  - If hooks missing: prompt "Install enhanced hooks? [y/n]"
  - If hooks outdated: prompt "Update hooks to latest version? [y/n]"

---

## Milestone 3: Intelligence Skills (Features 2, 3, 8)

### `/sk:learn` — Extract Reusable Patterns

- [ ] Create `skills/sk:learn/SKILL.md`:
  - Analyzes current session for extractable patterns
  - Pattern types: error resolution, debugging techniques, workarounds, project conventions
  - Output format: creates pattern file in `~/.claude/skills/learned/[pattern-name].md`
  - Each pattern has: Problem, Solution, Example, When to Use
  - Confidence scoring: tentative (0.3) → strong (0.7) → near-certain (0.9)
  - Asks user to confirm before saving
  - Filters out trivial fixes (typos, syntax errors)
  - Model routing: haiku (pattern detection is lightweight)

- [ ] Create `commands/sk/learn.md`:
  - Description: "Extract reusable patterns from the current session"
  - Points to skill

### `/sk:context-budget` — Audit Token Consumption

- [ ] Create `skills/sk:context-budget/SKILL.md`:
  - Phase 1: Inventory — scan agents, skills, rules, MCP tools, CLAUDE.md for token counts
    - Token estimation: `words * 1.3` for prose, `chars / 4` for code
    - Flag: agents >200 lines, skills >400 lines, rules >100 lines, MCP >20 tools
  - Phase 2: Classify — always needed / sometimes needed / rarely needed
  - Phase 3: Detect issues — bloated descriptions, redundant components, MCP over-subscription, CLAUDE.md bloat
  - Phase 4: Report — table with component breakdown, issues found, top 3 optimizations with token savings
  - `--verbose` flag for per-file breakdown
  - Model routing: haiku (counting/classification)

- [ ] Create `commands/sk/context-budget.md`:
  - Description: "Audit context window token consumption and find savings"

### `/sk:health` — Harness Self-Audit Scorecard

- [ ] Create `skills/sk:health/SKILL.md`:
  - 7 scoring categories (0-10 each, max 70):
    1. Tool Coverage — hooks, agents, rules present
    2. Context Efficiency — CLAUDE.md size, MCP tool count, skill count
    3. Quality Gates — lint, test, security, perf, review, e2e configured
    4. Memory Persistence — tasks files exist, lessons.md populated, session hooks active
    5. Eval Coverage — test assertions exist, coverage targets defined
    6. Security Guardrails — validate-commit hook, validate-push hook, deny rules in settings
    7. Cost Efficiency — model routing configured, compact suggestions active, context budget awareness
  - Scoring from file/config checks (deterministic, reproducible)
  - Output: scorecard with category scores, concrete findings, top 3 actions
  - Model routing: haiku (file checks + arithmetic)

- [ ] Create `commands/sk/health.md`:
  - Description: "Run harness self-audit and produce a health scorecard"

---

## Milestone 4: Session & Safety (Features 4, 6)

### `/sk:save-session` and `/sk:resume-session`

- [ ] Create `skills/sk:save-session/SKILL.md`:
  - Saves current session state to `.claude/sessions/[timestamp]-[branch].md`
  - Captures: current branch, active task from todo.md, recent findings, progress summary, open questions
  - Notifies user of saved path
  - Model routing: haiku (serialization)

- [ ] Create `skills/sk:resume-session/SKILL.md`:
  - Lists available sessions from `.claude/sessions/`
  - User picks one (or auto-picks most recent)
  - Reads session file and injects context
  - Reports: "Resumed session from [date] on branch [branch]"
  - Model routing: haiku (deserialization)

- [ ] Create `commands/sk/save-session.md` and `commands/sk/resume-session.md`

### `/sk:safety-guard` — Freeze Mode

- [ ] Create `skills/sk:safety-guard/SKILL.md`:
  - 3 modes:
    - **Careful mode** — intercepts destructive commands before execution (rm -rf, force push, reset --hard, DROP TABLE, chmod 777, --no-verify). Warns + asks confirmation.
    - **Freeze mode** — locks file edits to a specific directory tree. `--dir src/api/` → blocks writes outside that path. Uses PreToolUse hook.
    - **Guard mode** — both combined
  - `off` — disables all guards
  - Implementation: writes guard config to `.claude/safety-guard.json`, hooks read it
  - Log blocked actions to `.claude/safety-guard.log`
  - Model routing: haiku (config read/write)

- [ ] Create `commands/sk/safety-guard.md`

- [ ] Create `skills/sk:setup-claude/templates/hooks/safety-guard.sh`:
  - Reads `.claude/safety-guard.json` for active mode and directory constraints
  - PreToolUse hook for Bash/Edit/Write
  - Checks command/path against rules
  - Blocks with exit code 2 + explanation on violation

---

## Milestone 5: Eval + Enrichments (Features 5, 7, 9, 10)

### `/sk:eval` — Eval-Driven Development

- [ ] Create `skills/sk:eval/SKILL.md`:
  - Subcommands: `define`, `check`, `report`
  - Eval types:
    - Capability evals — test if Claude can do something new
    - Regression evals — ensure changes don't break existing
  - Grader types:
    - Code-based (deterministic: grep, test pass/fail, build success)
    - Model-based (LLM-as-judge rubric, score 1-5)
    - Human (flag for manual review)
  - Metrics: pass@k (at least 1 success in k), pass^k (all k succeed)
  - Storage: `.claude/evals/[feature].md` (definition), `.claude/evals/[feature].log` (history)
  - Workflow: define before coding → check during → report after
  - Model routing: sonnet (eval analysis needs reasoning)

- [ ] Create `commands/sk/eval.md`

### Enrich `/sk:start` — Missing Context Detection

- [ ] Edit `skills/sk:start/SKILL.md`:
  - Add Phase 1.5 after classification, before recommendation:
    - **Missing Context Detection** — scan task description for gaps:
      - Tech stack specified? (auto-detect from project if missing)
      - Acceptance criteria present?
      - Scope boundaries (what NOT to do)?
      - Security requirements mentioned? (if auth/user data involved)
      - Testing expectations stated?
    - If 3+ critical items missing: include in recommendation output, suggest user clarify
    - Does NOT block — informational only
  - Keep existing classify → recommend → route flow intact

### Search-First in `/sk:brainstorm`

- [ ] Edit brainstorm skill (find the right file — `skills/sk:brainstorming/SKILL.md`):
  - Add a "Research" phase before proposing approaches:
    - "Before proposing, search: does this already exist in the repo? Is there a package for this? Is there an MCP server?"
    - Quick checklist: (1) grep codebase, (2) search package registry, (3) check existing skills
    - Decision matrix: Adopt existing / Extend / Build custom
  - Keep existing brainstorm flow intact — this is an additive phase

### Codebase Onboarding in `/sk:setup-claude`

- [ ] Edit `skills/sk:setup-claude/SKILL.md`:
  - Add "Phase 0: Reconnaissance" before stack detection:
    - Scan top 2 levels of directory tree
    - Identify entry points (main.*, index.*, app.*, server.*)
    - Detect architecture pattern (monolith, monorepo, microservices)
    - Data flow trace: request → validation → logic → DB
  - Output: append architecture summary to `tasks/findings.md`
  - Only runs on FIRST setup (not idempotent re-runs)

---

## Milestone 6: Documentation + Model Routing

- [ ] Update `CLAUDE.md` — add 7 new commands to commands table:
  - `/sk:learn`, `/sk:context-budget`, `/sk:health`
  - `/sk:save-session`, `/sk:resume-session`
  - `/sk:safety-guard`, `/sk:eval`

- [ ] Update `skills/sk:setup-claude/templates/CLAUDE.md.template` — add same 7 commands

- [ ] Update `README.md` — add new commands to appropriate sections:
  - `/sk:learn` under "On-Demand Tools" or new "Intelligence" section
  - `/sk:context-budget` under "On-Demand Tools"
  - `/sk:health` under "On-Demand Tools"
  - `/sk:save-session` / `/sk:resume-session` under "Session Management" (new section)
  - `/sk:safety-guard` under "Safety" (new section)
  - `/sk:eval` under "Quality" section

- [ ] Update `.claude/docs/DOCUMENTATION.md` — add all 7 new skills

- [ ] Update `install.sh` — add new commands to echo block

- [ ] Update `CHANGELOG.md` — new version entry with `### Added` for all features

- [ ] Update `commands/sk/set-profile.md` — add model routing for new skills:
  - `learn` → haiku (all profiles)
  - `context-budget` → haiku (all profiles)
  - `health` → haiku (all profiles)
  - `save-session` → haiku (all profiles)
  - `resume-session` → haiku (all profiles)
  - `safety-guard` → haiku (all profiles)
  - `eval` → sonnet (balanced/quality), haiku (budget)

- [ ] Update `skills/sk:setup-optimizer/SKILL.md`:
  - Add all 7 new commands to the list it checks for in CLAUDE.md
  - Add hooks detection + prompt for hook installation/update

- [ ] Append to `tasks/lessons.md` — tracking entries for all 7 new skills + hooks

---

## Verification

```bash
# Run full test suite
bash tests/verify-workflow.sh

# Verify all new skills exist
for skill in learn context-budget health save-session resume-session safety-guard eval; do
  ls "skills/sk:${skill}/SKILL.md"
done

# Verify all new commands exist
for cmd in learn.md context-budget.md health.md save-session.md resume-session.md safety-guard.md eval.md; do
  ls "commands/sk/${cmd}"
done

# Verify all new hook templates exist
for hook in config-protection.sh post-edit-format.sh console-log-warning.sh cost-tracker.sh suggest-compact.sh safety-guard.sh; do
  ls "skills/sk:setup-claude/templates/hooks/${hook}"
done

# Verify docs contain all new commands
for cmd in learn context-budget health save-session resume-session safety-guard eval; do
  grep -q "sk:${cmd}" CLAUDE.md && echo "CLAUDE.md: sk:${cmd} OK" || echo "CLAUDE.md: sk:${cmd} MISSING"
  grep -q "sk:${cmd}" README.md && echo "README.md: sk:${cmd} OK" || echo "README.md: sk:${cmd} MISSING"
done

# Verify settings.json.template has new hooks
grep -q "config-protection" skills/sk:setup-claude/templates/.claude/settings.json.template
grep -q "console-log" skills/sk:setup-claude/templates/.claude/settings.json.template
```

## Acceptance Criteria

### Hooks (Milestone 2)
- [ ] 5 new hook scripts exist and are functional
- [ ] settings.json.template wires all new hooks
- [ ] `/sk:setup-claude` prompts user before installing hooks
- [ ] `/sk:setup-optimizer` detects missing hooks and prompts to install
- [ ] Config protection blocks linter config edits by default

### Intelligence Skills (Milestone 3)
- [ ] `/sk:learn` extracts patterns with confidence scoring
- [ ] `/sk:context-budget` produces token audit report with top 3 savings
- [ ] `/sk:health` produces 7-category scorecard (0-70)

### Session & Safety (Milestone 4)
- [ ] `/sk:save-session` creates session files in `.claude/sessions/`
- [ ] `/sk:resume-session` lists and loads sessions
- [ ] `/sk:safety-guard` supports careful/freeze/guard/off modes
- [ ] Freeze mode blocks writes outside specified directory

### Eval + Enrichments (Milestone 5)
- [ ] `/sk:eval` supports define/check/report subcommands
- [ ] `/sk:start` warns about missing context (3+ gaps)
- [ ] Brainstorm includes search-first research phase
- [ ] Setup-claude runs reconnaissance on first setup

### Documentation (Milestone 6)
- [ ] All 7 new commands in CLAUDE.md, README.md, DOCUMENTATION.md
- [ ] install.sh lists new commands
- [ ] CHANGELOG.md documents all features
- [ ] lessons.md has tracking entries for all new skills
- [ ] set-profile.md has model routing for all new skills
- [ ] All tests pass

## Risks

- **Hook compatibility** — hooks use shell scripts; Windows users may need Node.js wrappers (existing pattern from ECC)
- **Config protection false positives** — legitimate config edits blocked; mitigated by `SHIPKIT_ALLOW_CONFIG_EDIT=1` override
- **Context budget accuracy** — token estimates are approximate (words * 1.3); good enough for relative comparison
- **Session file growth** — `.claude/sessions/` could accumulate; add `.gitignore` entry
- **Cross-file consistency** — 7 new skills × 10 files each = 70+ file touches; test assertions verify
