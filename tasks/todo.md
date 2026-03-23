# TODO — 2026-03-23 — ShipKit Workflow Acceleration (Auto-Skip, Autopilot, Team, Smart Start)

## Goal

Add 4 workflow acceleration features to ShipKit that reduce friction without compromising quality:
1. **Auto-skip intelligence** (Feature 11) — auto-detect and skip obviously non-applicable optional steps in both manual and autopilot modes
2. **`/sk:autopilot`** (Feature 12) — hands-free workflow mode that runs all 21 steps with minimal interruptions
3. **`/sk:team`** (Feature 13) — parallel domain agents (backend + frontend + QA) for full-stack tasks
4. **`/sk:start`** (Feature 14) — smart entry point that classifies tasks and routes to the optimal flow/mode/agents

## Constraints (from lessons.md)

- All commands use `/sk:` prefix
- When adding new commands: update CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, CHANGELOG.md
- Never overwrite `tasks/lessons.md` — append only
- Each new skill needs a lessons.md entry tracking its dependent files
- For existing projects: `/sk:setup-optimizer` handles upgrades (not re-running `/sk:setup-claude`)
- Skills are symlinked via `install.sh` — new skills auto-available after re-install
- Model routing via `commands/sk/set-profile.md` — new skills need entries in the model table

---

## Milestone 1: Tests (TDD Red Phase)

#### Wave 1 (parallel — all test groups are independent)

- [ ] Add assertions for **auto-skip intelligence** to `tests/verify-workflow.sh`:
  - `assert_contains` — `CLAUDE.md` contains `"Auto-skipped"`
  - `assert_contains` — `CLAUDE.md` contains `"auto-skip"` or `"auto_skip"`
  - `assert_contains` — `CLAUDE.md.template` contains `"Auto-skipped"`
  - `assert_contains` — `CLAUDE.md.template` contains `"auto-skip"` or `"auto_skip"`

- [ ] Add assertions for **`/sk:autopilot`** skill:
  - `assert_file_exists` — `skills/sk:autopilot/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"auto-advance"`
  - `assert_contains` — `SKILL.md` contains `"auto-skip"`
  - `assert_contains` — `SKILL.md` contains `"auto-commit"`
  - `assert_contains` — `SKILL.md` contains `"Direction approval"`
  - `assert_contains` — `SKILL.md` contains `"3-strike"`
  - `assert_contains` — `SKILL.md` contains `"PR push"`
  - `assert_contains` — `SKILL.md` contains `"quality gate"`

- [ ] Add assertions for **`/sk:team`** skill:
  - `assert_file_exists` — `skills/sk:team/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"Backend Agent"`
  - `assert_contains` — `SKILL.md` contains `"Frontend Agent"`
  - `assert_contains` — `SKILL.md` contains `"QA Agent"`
  - `assert_contains` — `SKILL.md` contains `"API contract"`
  - `assert_contains` — `SKILL.md` contains `"worktree"`
  - `assert_contains` — `SKILL.md` contains `"merge"`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/.claude/agents/backend-dev.md`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md`
  - `assert_file_exists` — `skills/sk:setup-claude/templates/.claude/agents/qa-engineer.md`
  - `assert_contains` — `backend-dev.md` contains `"backend"`
  - `assert_contains` — `frontend-dev.md` contains `"frontend"`
  - `assert_contains` — `qa-engineer.md` contains `"E2E"`

- [ ] Add assertions for **`/sk:start`** skill:
  - `assert_file_exists` — `skills/sk:start/SKILL.md`
  - `assert_contains` — `SKILL.md` contains `"Classify"`
  - `assert_contains` — `SKILL.md` contains `"Recommend"`
  - `assert_contains` — `SKILL.md` contains `"Route"`
  - `assert_contains` — `SKILL.md` contains `"debug"`
  - `assert_contains` — `SKILL.md` contains `"hotfix"`
  - `assert_contains` — `SKILL.md` contains `"fast-track"`
  - `assert_contains` — `SKILL.md` contains `"autopilot"`
  - `assert_contains` — `SKILL.md` contains `"team"`
  - `assert_contains` — `SKILL.md` contains `"--manual"`

- [ ] Add assertions for **documentation updates**:
  - `assert_contains` — `CLAUDE.md` contains `"/sk:start"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:autopilot"`
  - `assert_contains` — `CLAUDE.md` contains `"/sk:team"`
  - `assert_contains` — `README.md` contains `"/sk:start"`
  - `assert_contains` — `README.md` contains `"/sk:autopilot"`
  - `assert_contains` — `README.md` contains `"/sk:team"`
  - `assert_contains` — `DOCUMENTATION.md` contains `"sk:start"`
  - `assert_contains` — `DOCUMENTATION.md` contains `"sk:autopilot"`
  - `assert_contains` — `DOCUMENTATION.md` contains `"sk:team"`

- [ ] Add assertions for **set-profile model table**:
  - `assert_contains` — `commands/sk/set-profile.md` contains `"start"`
  - `assert_contains` — `commands/sk/set-profile.md` contains `"autopilot"`
  - `assert_contains` — `commands/sk/set-profile.md` contains `"team"`

- [ ] Add assertions for **setup-optimizer** upgrade support:
  - `assert_contains` — `skills/sk:setup-optimizer/SKILL.md` contains `"sk:start"`
  - `assert_contains` — `skills/sk:setup-optimizer/SKILL.md` contains `"auto-skip"`

---

## Milestone 2: Auto-Skip Intelligence (Feature 11)

#### Wave 2 (sequential — CLAUDE.md changes must be consistent across files)

- [ ] Update `CLAUDE.md` — add auto-skip rules to Workflow Tracker Rules section:
  - New rule: "Auto-skip optional steps when detection criteria are met"
  - Detection table: step 4 (no frontend keywords), step 5 (no frontend keywords), step 8 (no DB keywords), step 15 (no frontend AND no DB)
  - Output format: `Auto-skipped: [Step Name] ([reason])`
  - Step 21 (Release) is never auto-skipped
  - Auto-skip applies in both manual and autopilot modes

- [ ] Update `skills/sk:setup-claude/templates/CLAUDE.md.template` — same auto-skip rules:
  - Mirror the exact same auto-skip rules added to CLAUDE.md
  - Ensure template placeholders are preserved

---

## Milestone 3: `/sk:autopilot` Skill (Feature 12)

#### Wave 3 (parallel — skill + command are independent files)

- [ ] Create `skills/sk:autopilot/SKILL.md`:
  - Frontmatter: name, description, triggers, allowed-tools (Agent, Skill, Read, Write, Bash, Glob, Grep)
  - Step 0: Auto-reset workflow tracker if stale (has done/skipped steps from a different task)
  - Step 1: Read `tasks/todo.md` + `tasks/lessons.md` + `tasks/findings.md` (auto, no prompt)
  - Step 2: Run brainstorm internally — present ONE direction summary, wait for y/n
  - Step 3: On approval, auto-advance through remaining steps:
    - Auto-skip intelligence for optional steps (Feature 11)
    - Auto-plan (no approval prompt — brainstorm approval covers direction)
    - Auto-branch
    - Auto-write-tests → auto-implement
    - Auto-commit with conventional format
    - Auto-run all gates (via `/sk:gates` if available, else sequential)
    - Auto-update task
  - Step 4: Stop for PR push confirmation (always — visible to others)
  - Step 5: Auto-sync features, ask about release
  - 3-strike protocol: if any step fails 3 times, stop and ask user
  - Quality guarantee section: explicit statement that all gates enforced
  - Model routing section: read `.shipkit/config.json`

- [ ] Create `commands/sk/autopilot.md` command shortcut:
  - Points to `skills/sk:autopilot/SKILL.md`
  - Description: "Hands-free workflow — all 21 steps, minimal interruptions"

---

## Milestone 4: `/sk:team` Skill (Feature 13)

#### Wave 4a (parallel — agent templates are independent)

- [ ] Create `skills/sk:setup-claude/templates/.claude/agents/backend-dev.md`:
  - Frontmatter: name, model (sonnet), description, allowed_tools
  - Prompt: "You are the Backend Agent. Your job is to write backend tests and implement backend code."
  - Reads API contract from `tasks/todo.md` (the plan)
  - Writes backend tests (models, controllers, services, validation)
  - Implements backend code to make tests pass
  - Runs backend test suite before reporting done
  - Auto-commits with `feat(backend):` prefix
  - 3-strike protocol on failures
  - Tools: Bash, Read, Edit, Write, Glob, Grep

- [ ] Create `skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md`:
  - Frontmatter: name, model (sonnet), description, allowed_tools
  - Prompt: "You are the Frontend Agent. Your job is to write frontend tests and implement UI code."
  - Reads API contract from `tasks/todo.md` — mocks backend endpoints
  - Writes frontend tests (components, composables, pages)
  - Implements frontend code to make tests pass
  - Runs frontend test suite before reporting done
  - Auto-commits with `feat(frontend):` prefix
  - 3-strike protocol on failures
  - Tools: Bash, Read, Edit, Write, Glob, Grep

- [ ] Create `skills/sk:setup-claude/templates/.claude/agents/qa-engineer.md`:
  - Frontmatter: name, model (sonnet), description, allowed_tools
  - Prompt: "You are the QA Agent. Your job is to write E2E test scenarios."
  - Reads plan from `tasks/todo.md` — extracts user flows
  - Writes E2E test scenarios (Playwright or agent-browser)
  - Covers happy path + key edge cases
  - Reports scenario count and coverage summary
  - Does NOT run E2E tests (that happens after merge in gates)
  - Tools: Bash, Read, Write, Glob, Grep

#### Wave 4b (depends on 4a — skill references agent names)

- [ ] Create `skills/sk:team/SKILL.md`:
  - Frontmatter: name, description, triggers, allowed-tools (Agent, Skill, Read, Write, Bash, Glob, Grep)
  - Step 0: Validate prerequisites — check `tasks/todo.md` has API contract section
  - Step 1: If no API contract, warn and fall back to single-agent mode
  - Step 2: Spawn agents in parallel:
    - Backend Agent (worktree isolation) — steps 9+10 combined for backend
    - Frontend Agent (worktree isolation) — steps 9+10 combined for frontend
    - QA Agent (background) — writes E2E scenarios
  - Step 3: Wait for Backend + Frontend agents to complete
  - Step 4: Merge worktrees back to feature branch
    - Auto-resolve non-conflicting changes
    - If conflicts: attempt auto-resolution, escalate to user if ambiguous
  - Step 5: Collect QA Agent's E2E scenarios
  - Step 6: Report team results — files changed per agent, test counts, merge status
  - Fallback: if worktree creation fails, run single-agent sequential mode
  - Works in both manual and autopilot modes
  - Model routing section: read `.shipkit/config.json`

- [ ] Create `commands/sk/team.md` command shortcut:
  - Points to `skills/sk:team/SKILL.md`
  - Description: "Parallel domain agents for full-stack implementation"

- [ ] Update `skills/sk:setup-claude/scripts/apply_setup_claude.py`:
  - Add 3 new agent templates to the deployment mapping (backend-dev.md, frontend-dev.md, qa-engineer.md)
  - Same pattern as existing 5 agent deployments

---

## Milestone 5: `/sk:start` Skill (Feature 14)

#### Wave 5 (depends on Milestones 3+4 — start routes to autopilot and team)

- [ ] Create `skills/sk:start/SKILL.md`:
  - Frontmatter: name, description, triggers, allowed-tools (Agent, Skill, Read, Write, Bash, Glob, Grep)
  - Step 1 — Classify (automatic, no prompt):
    - Read task description from arguments
    - Read `tasks/todo.md` for additional context
    - Scan for signal keywords:
      - Bug signals: "bug", "fix", "broken", "error", "regression", "failing"
      - Hotfix signals: "urgent", "prod down", "hotfix", "emergency", "critical"
      - Small change signals: "config", "bump", "typo", "copy", "rename", "dependency"
      - Frontend signals: "component", "page", "view", "CSS", "UI", "form", "modal", "button"
      - Backend signals: "API", "endpoint", "controller", "model", "migration", "service", "queue"
    - Classify: flow (feature/debug/hotfix/fast-track) + scope (full-stack/frontend/backend)
  - Step 2 — Recommend (one prompt):
    - Display detected classification
    - Recommend: flow + mode (autopilot/manual) + agents (team/solo)
    - Show override options: `y`, `manual`, `no-team`, `--debug`, `--hotfix`, `--fast-track`
    - Wait for user confirmation
  - Step 3 — Route:
    - Reset `tasks/workflow-status.md` with chosen flow/mode/agent config
    - Add `mode:` and `agents:` metadata to tracker header
    - Dispatch to chosen flow:
      - If autopilot: invoke `/sk:autopilot` with the task description
      - If manual + team: proceed step-by-step, activate `/sk:team` at step 9
      - If manual + solo: proceed step-by-step (current behavior)
      - If debug/hotfix/fast-track: invoke the respective skill
  - Override flags: `--manual`, `--no-team`, `--team`, `--debug`, `--hotfix`, `--fast-track`
  - Model routing section: read `.shipkit/config.json` (haiku for classification, main model for routing)

- [ ] Create `commands/sk/start.md` command shortcut:
  - Points to `skills/sk:start/SKILL.md`
  - Description: "Smart entry point — classifies task and routes to optimal flow"

---

## Milestone 6: Profile + Optimizer Updates

#### Wave 6 (parallel — set-profile and setup-optimizer are independent)

- [ ] Update `commands/sk/set-profile.md` — add new skills to model table:
  - Add row: `start` → haiku across all profiles (lightweight classification)
  - Add row: `autopilot` → same as brainstorm row (opus/opus/sonnet/sonnet — orchestrator needs planning-level model)
  - Add row: `team (orchestrator)` → same as execute-plan row
  - Update Step 5 confirm display to show new skill assignments

- [ ] Update `skills/sk:setup-optimizer/SKILL.md`:
  - Add `/sk:start` to the list of commands it checks for in CLAUDE.md
  - Add auto-skip rules to the workflow section it updates
  - Add `/sk:autopilot` and `/sk:team` to detected commands
  - Ensure it can upgrade existing projects to include auto-skip rules in their CLAUDE.md

---

## Milestone 7: Documentation + Lessons

#### Wave 7 (parallel — all doc files are independent, but depend on Milestones 2-5)

- [ ] Update `CLAUDE.md` — add 3 new commands to commands table:
  - `| /sk:start | Smart entry point — classifies task, routes to optimal flow/mode/agents |`
  - `| /sk:autopilot | Hands-free workflow — all 21 steps, minimal interruptions |`
  - `| /sk:team | Parallel domain agents (backend + frontend + QA) for full-stack tasks |`

- [ ] Update `README.md` — add 3 new commands:
  - `/sk:start` under "Getting Started" or top of commands (primary entry point)
  - `/sk:autopilot` under "Development" category
  - `/sk:team` under "Development" category
  - Add "Quick Start" section showing `/sk:start` as the recommended entry

- [ ] Update `.claude/docs/DOCUMENTATION.md`:
  - Add sk:start, sk:autopilot, sk:team to skills section
  - Add "Auto-Skip Intelligence" section explaining detection rules
  - Add "Workflow Modes" section explaining manual vs autopilot vs team
  - Update "What's New" section

- [ ] Update `CHANGELOG.md`:
  - Add new version section with `### Added` for all 4 features

- [ ] Update `install.sh`:
  - Add sk:start, sk:autopilot, sk:team to commands echo block

- [ ] Append to `tasks/lessons.md` — tracking entries for new skills:
  - sk:start: SKILL.md + command + CLAUDE.md + README.md + DOCUMENTATION.md + feature spec
  - sk:autopilot: SKILL.md + command + CLAUDE.md + README.md + DOCUMENTATION.md + feature spec
  - sk:team: SKILL.md + command + 3 agent templates + apply_setup_claude.py + CLAUDE.md + README.md + DOCUMENTATION.md + feature spec
  - Auto-skip: CLAUDE.md + CLAUDE.md.template + setup-optimizer

---

## Verification

```bash
# Run full test suite
bash tests/verify-workflow.sh

# Verify new skills exist
ls skills/sk:start/SKILL.md
ls skills/sk:autopilot/SKILL.md
ls skills/sk:team/SKILL.md

# Verify new agent templates exist
ls skills/sk:setup-claude/templates/.claude/agents/backend-dev.md
ls skills/sk:setup-claude/templates/.claude/agents/frontend-dev.md
ls skills/sk:setup-claude/templates/.claude/agents/qa-engineer.md

# Verify new commands exist
ls commands/sk/start.md
ls commands/sk/autopilot.md
ls commands/sk/team.md

# Verify auto-skip in CLAUDE.md
grep -q "Auto-skipped" CLAUDE.md
grep -q "Auto-skipped" skills/sk:setup-claude/templates/CLAUDE.md.template

# Verify docs updated with all new commands
for cmd in start autopilot team; do
  grep "sk:$cmd" CLAUDE.md README.md .claude/docs/DOCUMENTATION.md
done

# Verify set-profile has new entries
grep "start" commands/sk/set-profile.md
grep "autopilot" commands/sk/set-profile.md
```

## Acceptance Criteria

### Auto-Skip Intelligence (Milestone 2)
- [ ] CLAUDE.md contains auto-skip detection rules for steps 4, 5, 8, 15
- [ ] CLAUDE.md.template contains matching auto-skip rules
- [ ] Auto-skip output format is `Auto-skipped: [Step Name] ([reason])`
- [ ] Step 21 (Release) is never auto-skipped
- [ ] Auto-skip works in both manual and autopilot modes

### `/sk:autopilot` (Milestone 3)
- [ ] Skill runs all 21 steps in order
- [ ] All quality gates enforced (same as manual)
- [ ] Auto-skip intelligence active
- [ ] Auto-advances between steps
- [ ] Auto-commits with conventional format
- [ ] Stops only for: direction approval (step 3), 3-strike failures, PR push (step 19)
- [ ] Model routing reads `.shipkit/config.json`

### `/sk:team` (Milestone 4)
- [ ] 3 agent templates exist: backend-dev, frontend-dev, qa-engineer
- [ ] Skill validates API contract prerequisite before spawning
- [ ] Backend + Frontend agents run in parallel worktrees
- [ ] QA Agent runs in background
- [ ] Merge step handles worktree consolidation
- [ ] Falls back to single-agent if no API contract or single-domain task
- [ ] `apply_setup_claude.py` deploys 3 new agent templates

### `/sk:start` (Milestone 5)
- [ ] Classifies tasks into: feature, debug, hotfix, fast-track
- [ ] Detects scope: full-stack, frontend-only, backend-only
- [ ] Recommends flow + mode + agents in one prompt
- [ ] Override flags work: `--manual`, `--no-team`, `--team`, `--debug`, `--hotfix`, `--fast-track`
- [ ] Routes to correct flow after user confirmation
- [ ] Resets workflow tracker with chosen config

### Profile + Optimizer (Milestone 6)
- [ ] `set-profile.md` model table includes start, autopilot, team
- [ ] `setup-optimizer` can upgrade existing projects with auto-skip rules + new commands

### Documentation (Milestone 7)
- [ ] All 3 new commands in CLAUDE.md, README.md, DOCUMENTATION.md
- [ ] CHANGELOG.md documents all 4 features
- [ ] install.sh lists all 3 new commands
- [ ] lessons.md updated with tracking entries
- [ ] All tests pass

## Risks/Unknowns

- **Autopilot brainstorm quality**: Running brainstorm non-interactively may produce less refined direction than interactive brainstorm. Mitigation: direction approval checkpoint after brainstorm.
- **Team worktree merging**: Git worktree merge conflicts between backend and frontend agents could be complex. Mitigation: agents work on different directories (backend in `app/`, frontend in `resources/`), merge step has auto-resolve + escalation.
- **Start classification accuracy**: Keyword-based classification may misroute tasks. Mitigation: user always confirms before routing; override flags available.
- **Agent template installation**: `apply_setup_claude.py` needs to handle 8 agent templates total (5 existing + 3 new). Verify the deployment loop handles growth.
- **Cross-file consistency**: 4 features touching 15+ files — high risk of stale references. Mitigation: test assertions verify all doc files contain new command names.
