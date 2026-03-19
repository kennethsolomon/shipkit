# TODO — 2026-03-19 — Three Improvements: sk:context + sk:mvp docs + decisions log

## Goal

Three targeted improvements inspired by vibe-coding-starter-kit's session continuity patterns:
- **A)** `sk:mvp` auto-generates project context docs after scaffolding (vision, PRD, tech-design)
- **B)** New `sk:context` skill — session brief reader that auto-loads context files + outputs a readable summary
- **C)** `sk:brainstorming` appends ADR entries to a persistent `docs/decisions.md`

## Constraints (from lessons.md)

- All commands use `/sk:` prefix
- Never overwrite `tasks/lessons.md` — append only
- New skill (sk:context) requires updating: CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, CLAUDE.md.template, CHANGELOG.md, lessons.md
- All 3 approaches are independent — can be parallelized

---

## Milestone 1: Tests (TDD Red Phase)

#### Wave 1 (parallel — all independent)

- [ ] Update `tests/verify-workflow.sh` — add assertions for Approach A (sk:mvp docs)
  - `assert_contains` — `skills/sk:mvp/SKILL.md` contains `"vision.md"`
  - `assert_contains` — `skills/sk:mvp/SKILL.md` contains `"prd.md"`
  - `assert_contains` — `skills/sk:mvp/SKILL.md` contains `"tech-design.md"`
  - `assert_contains` — `skills/sk:mvp/SKILL.md` contains `"docs/"` (new phase generates docs)

- [ ] Update `tests/verify-workflow.sh` — add assertions for Approach B (sk:context)
  - `assert_file_exists` — `skills/sk:context/SKILL.md` exists
  - `assert_contains` — `skills/sk:context/SKILL.md` contains `"SESSION BRIEF"`
  - `assert_contains` — `skills/sk:context/SKILL.md` contains `"tasks/todo.md"`
  - `assert_contains` — `skills/sk:context/SKILL.md` contains `"tasks/workflow-status.md"`
  - `assert_contains` — `skills/sk:context/SKILL.md` contains `"tasks/lessons.md"`
  - `assert_contains` — `CLAUDE.md` contains `"sk:context"`
  - `assert_contains` — `README.md` contains `"sk:context"`
  - `assert_contains` — `.claude/docs/DOCUMENTATION.md` contains `"sk:context"`
  - `assert_contains` — `install.sh` contains `"sk:context"`

- [ ] Update `tests/verify-workflow.sh` — add assertions for Approach C (decisions log)
  - `assert_contains` — `skills/sk:brainstorming/SKILL.md` contains `"docs/decisions.md"`
  - `assert_contains` — `skills/sk:brainstorming/SKILL.md` contains `"decisions.md"`

---

## Milestone 2: Implementation

#### Wave 2 (parallel — all three approaches are independent)

- [ ] **Approach A** — Update `skills/sk:mvp/SKILL.md`
  - Rename existing "Step 9 — Present the Output" to "Step 10 — Present the Output"
  - Insert new "Step 9 — Generate Project Context Docs" between Step 8 and Step 10
  - Step 9 generates 3 files in `docs/` using info already gathered in Step 1 + Step 2:
    - `docs/vision.md` — product name, value prop, target audience, key features, north star metric
    - `docs/prd.md` — feature list with acceptance criteria, user stories derived from Step 1 features
    - `docs/tech-design.md` — tech stack, scaffold structure, component map (landing + app pages), data model (waitlist schema or key entities)
  - These docs are generated from Step 1 + Step 2 data — no new user questions needed
  - Add note: "These docs persist context for future sessions. Run `/sk:context` to load them."

- [ ] **Approach B** — Create `skills/sk:context/SKILL.md`
  - Purpose: Session initializer — reads all context files AND outputs a formatted session brief
  - Files it reads (in order):
    1. `tasks/todo.md` — current task name, milestone progress, pending checkboxes count
    2. `tasks/workflow-status.md` — current step status, `>> next <<` step + command
    3. `tasks/progress.md` — last 5 entries (most recent work done)
    4. `tasks/findings.md` — current decisions and open questions
    5. `tasks/lessons.md` — all active lessons (apply as constraints for this session)
    6. `docs/decisions.md` — if exists, last 3 ADR entries
    7. `docs/vision.md` — if exists, product name + value prop
  - Output format (session brief):
    ```
    ╔══════════════════════════════╗
    ║       SESSION BRIEF          ║
    ╚══════════════════════════════╝
    Branch:     feature/xxx (or main)
    Task:       [task name from todo.md]
    Step:       [current step #] [step name] → next: [command]
    Last done:  [last progress.md entry, 1 line]
    Pending:    [N] checkboxes remaining
    Lessons:    [count] active — [most critical 1-liner]
    Open Qs:    [any open questions from findings.md, or "none"]
    Product:    [value prop from vision.md, or "no vision.md found"]
    ════════════════════════════════
    ```
  - After outputting the brief: apply all lessons from lessons.md as active constraints for the session
  - If `tasks/todo.md` is missing or task is complete: show "No active task — ready to start fresh"
  - Model Routing section: sonnet for all profiles (lightweight read-only skill)

- [ ] **Approach C** — Update `skills/sk:brainstorming/SKILL.md`
  - In "Step 5 — Write findings" section, add a second write target after `tasks/findings.md`:
  - **Append** an ADR entry to `docs/decisions.md` (create if not exists, never overwrite)
  - ADR entry format:
    ```markdown
    ## [YYYY-MM-DD] [Feature/Task Name]

    **Context:** [problem being solved — 1-2 sentences]
    **Decision:** [chosen approach — 1 sentence]
    **Rationale:** [why this approach over alternatives]
    **Consequences:** [trade-offs accepted]
    **Status:** accepted
    ```
  - Rule note: `docs/decisions.md` is append-only — never overwrite existing entries
  - If `docs/decisions.md` does not exist, create it with a header before the first entry:
    ```markdown
    # Architecture Decision Records

    A cumulative log of key design decisions made across features. Append-only — never overwrite.
    ```

---

## Milestone 3: Documentation Updates (for new sk:context command)

#### Wave 3 (parallel — all independent)

- [ ] Update `CLAUDE.md` — add `sk:context` to commands table
  - Add row: `| \`/sk:context\` | Load all context files + output session brief for fast session start |`
  - Place near `/sk:status` and `/sk:dashboard` (utility commands section)

- [ ] Update `README.md` — add `sk:context` to commands section
  - Same row format as CLAUDE.md

- [ ] Update `.claude/docs/DOCUMENTATION.md` — add `sk:context` to skills section
  - Add entry: purpose, when to use (start of every session), what files it reads, brief output format

- [ ] Update `install.sh` — add `sk:context` to workflow commands echo block
  - Add line: `echo "  /sk:context      — Load context + session brief (run at session start)"`

- [ ] Update `skills/sk:setup-claude/templates/CLAUDE.md.template` — add `sk:context`
  - Add same row as CLAUDE.md in the commands table section of the template

- [ ] Update `CHANGELOG.md` — document all 3 improvements
  - New section for v3.6.0 (or next version)
  - Three bullet points: A (sk:mvp docs), B (sk:context), C (decisions log)

- [ ] Append `tasks/lessons.md` — add sk:context tracking entry
  - New entry: "[2026-03-19] sk:context — update its docs when the skill changes"
  - Note the files: SKILL.md, CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, CLAUDE.md.template

---

## Verification

```bash
# Approach A: sk:mvp has new doc generation step
grep -n "vision.md" skills/sk:mvp/SKILL.md
grep -n "prd.md" skills/sk:mvp/SKILL.md
grep -n "tech-design.md" skills/sk:mvp/SKILL.md

# Approach B: sk:context skill exists with correct content
ls skills/sk:context/SKILL.md
grep "SESSION BRIEF" skills/sk:context/SKILL.md
grep "tasks/todo.md" skills/sk:context/SKILL.md
grep "tasks/lessons.md" skills/sk:context/SKILL.md

# Approach B: sk:context documented everywhere
grep "sk:context" CLAUDE.md
grep "sk:context" README.md
grep "sk:context" .claude/docs/DOCUMENTATION.md
grep "sk:context" install.sh
grep "sk:context" skills/sk:setup-claude/templates/CLAUDE.md.template

# Approach C: sk:brainstorming writes decisions.md
grep "docs/decisions.md" skills/sk:brainstorming/SKILL.md

# Run full test suite
bash tests/verify-workflow.sh
```

## Acceptance Criteria

- [ ] `skills/sk:mvp/SKILL.md` Step 9 generates `docs/vision.md`, `docs/prd.md`, `docs/tech-design.md`
- [ ] `skills/sk:context/SKILL.md` exists with SESSION BRIEF output format
- [ ] `sk:context` reads 7 context files and applies lessons as constraints
- [ ] `sk:context` handles missing files gracefully (no active task, no vision.md, etc.)
- [ ] `sk:brainstorming/SKILL.md` appends ADR entries to `docs/decisions.md`
- [ ] `docs/decisions.md` is append-only — rule documented in sk:brainstorming
- [ ] `sk:context` present in CLAUDE.md, README.md, DOCUMENTATION.md, install.sh, CLAUDE.md.template
- [ ] `CHANGELOG.md` documents all 3 improvements
- [ ] `tasks/lessons.md` updated with sk:context tracking entry
- [ ] All tests in `tests/verify-workflow.sh` pass

## Risks/Unknowns

- `tasks/progress.md` may be very long — sk:context should read only the last 5 entries, not the full file
- `docs/decisions.md` may not exist for existing projects — sk:brainstorming must create it gracefully
- sk:setup-claude templates: check if CLAUDE.md.template has the same commands table format before updating
