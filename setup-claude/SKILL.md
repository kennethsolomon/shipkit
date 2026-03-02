---
name: setup-claude
description: "Bootstrap/repair Claude project scaffolding (.claude docs/commands + tasks planning files). Adds plan/progress/findings to reduce errors."
user-invocable: true
---

# /setup-claude Skill

Bootstrap or optimize Claude Code infrastructure on any project.

## Overview

When invoked as `/setup-claude`, this skill:
1. **Initializes** planning files (`tasks/todo.md`, `tasks/findings.md`, `tasks/progress.md`)
2. **Scans** the project state (tech stack, existing files) and logs detection results
3. **Presents** a summary and waits for user confirmation
4. **Generates/updates** all missing or stale Claude Code infrastructure from templates
5. **Reports** what was created, updated, or skipped

Works on new projects and existing projects. Fully idempotent — safe to re-run.

Templates live in `~/.agents/skills/setup-claude/templates/`.
Detection heuristics are in `~/.agents/skills/setup-claude/references/detection.md`.
Template selection rules are in `~/.agents/skills/setup-claude/references/templates.md`.

---

## Planning-with-Files Behavioral Rules

These rules apply throughout ALL phases of this skill:

- **2-Action Rule**: After every 2 file reads/searches/explorations, write findings to `tasks/findings.md` before continuing
- **3-Strike Protocol**:
  - Attempt 1: Diagnose + fix root cause
  - Attempt 2: Different approach — never repeat the exact same failing action
  - Attempt 3: Question assumptions; search broadly
  - After 3 failures: Stop and explain the blocker to the user
- **Read-Before-Decide**: Re-open `tasks/todo.md` before major decisions or before moving to a new phase
- **Log Everything**: Errors go in `tasks/todo.md` Errors table immediately when encountered

---

## Implementation Strategy

This skill spawns an Explore subagent to parallelize file reads, then orchestrates template rendering and writes based on detection results. Return only summaries from the subagent, never raw full-file content.

---

## Step 1: Initialize Planning Files

Before any scanning, ensure planning infrastructure exists.

1. Create `tasks/` directory if missing
2. For each planning file — if missing, create from template; if present, do NOT overwrite:
   - `tasks/todo.md` → from `~/.agents/skills/setup-claude/templates/tasks-todo.md.template`
   - `tasks/findings.md` → from `~/.agents/skills/setup-claude/templates/tasks-findings.md.template`
   - `tasks/progress.md` → from `~/.agents/skills/setup-claude/templates/tasks-progress.md.template`
3. Append to `tasks/findings.md`: "Setup Claude infra started — [DATE]"
4. Append plan skeleton to `tasks/todo.md ## Plan`:
   - [ ] Scan project + detect stack
   - [ ] Present detection summary
   - [ ] Apply file changes
   - [ ] Report results

Also check for `.claude/commands/plan.md` and `.claude/commands/status.md`. If missing, create from:
- `~/.agents/skills/setup-claude/templates/plan.md.template`
- `~/.agents/skills/setup-claude/templates/status.md.template`

---

## Step 2: Scan + Detect (Parallel)

Delegate to Explore subagent for parallel reads. Return only a detection summary — never raw file content.

### 2a: Files to Read

- `package.json` / `composer.json` / `pyproject.toml` / `go.mod` / `Gemfile`
- `CLAUDE.md`, `.claude/commands/finish-feature.md`
- `.claude/docs/changelog-guide.md`, `.claude/docs/arch-changelog-guide.md`
- `tasks/lessons.md`, `CHANGELOG.md`, `tasks/todo.md`
- Top-level directory listing + one level of `src/`, `lib/`, or `app/`

### 2b: Analyze Existing CLAUDE.md (if present)

Classify as:
- **Good** — ≤120 lines, has "Workflow Orchestration" + "Core Principles" sections, no wrong-project artifacts
- **Verbose** — >120 lines or has inline guide sections
- **Wrong artifacts** — project name mismatch, stale tool refs, dead links
- **Missing sections** — incomplete Workflow or Principles

### 2c: Analyze finish-feature.md (if present)

Classify as:
- **Stale** — missing paths, wrong project name, obsolete stack
- **Correct** — current paths, accurate descriptions

### 2d: Detect Stack

See full detection logic in `~/.agents/skills/setup-claude/references/detection.md`.

Key outputs:
- `language`, `framework`, `database`, `ui`, `testing`, `ai`, `browserAutomation`
- `devCmd`, `buildCmd`, `lintCmd`, `testCmd`
- `projectName`, `projectDescription`
- `keyDirs` (table of detected important directories)

### 2e: Arch Log Directory Detection (Typo-Safe)

```
if .claude/docs/achritectural_change_log/ exists:
    ARCH_LOG_DIR = ".claude/docs/achritectural_change_log/"
else:
    ARCH_LOG_DIR = ".claude/docs/architectural_change_log/"
```

**Never create a new arch log dir if the typo version already exists.**
All generated files reference `[ARCH_LOG_DIR]` filled with the detected value.

### 2f: Write to tasks/findings.md

After detection, append a section to `tasks/findings.md`:

```markdown
## Stack Detection — [DATE]

- Language: [LANGUAGE]
- Framework: [FRAMEWORK]
- Database: [DATABASE]
- UI: [UI]
- Arch log dir: [ARCH_LOG_DIR]
- Template selection: [SELECTED_TEMPLATE]

### File States
- CLAUDE.md: [good / verbose / wrong artifacts / missing]
- finish-feature.md: [correct / stale / missing]
- changelog-guide.md: [present / missing]
- arch-changelog-guide.md: [present / missing]
- tasks/lessons.md: [present / missing]
- CHANGELOG.md: [present / missing]
```

---

## Step 3: Present Summary & Confirm

Display detection summary and planned changes:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /setup-claude — Detection Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project:          [PROJECT_NAME]
Description:      [ONE_SENTENCE_DESCRIPTION]
Language:         [LANGUAGE]
Framework:        [FRAMEWORK]
Database:         [DATABASE]
UI:               [UI]
Testing:          [TESTING]
AI/LLM:           [AI]
Browser Automation: [BROWSER_AUTOMATION]

Key Directories:
  • [DIR] — [PURPOSE]
  ...

Build Commands:
  • Dev:   [DEV_CMD]
  • Build: [BUILD_CMD]
  • Lint:  [LINT_CMD]

Files to create:
  • [list of missing files]

Files to update:
  • [list of stale files with reason]

Files to skip (already correct):
  • [list] ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Does this look right? Type 'yes' to proceed,
or describe what to correct:
```

Use `AskUserQuestion` to get confirmation. If user corrects something, re-run Step 2 with adjusted parameters and loop back to Step 3.

---

## Step 4: Apply Changes

For each file, follow the decision tree. After each phase, update `tasks/progress.md` and tick off completed items in `tasks/todo.md`.

### Decision Tree

#### `CLAUDE.md`
- **Missing** → Create from `templates/CLAUDE.md.template`, fill all `[PLACEHOLDERS]`
- **Good (≤120 lines, all sections, no artifacts)** → Skip with ✅
- **Verbose (>120 lines)** → Rewrite: keep fixed sections, trim to ~88 total lines
- **Wrong artifacts** → Replace entirely with correct template

Fill template placeholders per detected stack values. Omit Tech Stack table rows where value is not detected. Reference `references/templates.md` for CLAUDE.md line count target and optimization rules.

#### `.claude/commands/finish-feature.md`
- **Missing** → Create from `templates/finish-feature.md.template`, fill adaptive sections
- **Present + stale/wrong paths** → Replace with project-aware version
- **Present + correct** → Skip with ✅

Select adaptive content from `references/templates.md` based on detected stack.

Template selection logic (see `references/detection.md` for full table):
- Supabase + Next.js → "Next.js + Supabase"
- Supabase + non-Next.js → "Supabase (Any Framework)"
- Laravel → "Laravel + Eloquent ORM"
- Next.js + Drizzle → "Next.js + Drizzle ORM"
- Next.js + Prisma → "Next.js + Prisma"
- FastAPI + SQLAlchemy → "Python + FastAPI + SQLAlchemy"
- Fallback → "Generic / Minimal Stack"

#### `.claude/docs/changelog-guide.md`
- **Missing** → Create from `templates/changelog-guide.md.template`
- **Present** → Overwrite (static guide content, safe to refresh)

#### `.claude/docs/arch-changelog-guide.md`
- **Missing** → Create from `templates/arch-changelog-guide.md.template`, fill `[ARCH_LOG_DIR]`
- **Present** → Overwrite (static guide content, safe to refresh)

#### `tasks/lessons.md`
- **Missing** → Create from `templates/tasks-lessons.md.template`
- **Present** → Skip with ✅ (never overwrite accumulated knowledge)

#### `CHANGELOG.md`
- **Missing** → Create from `templates/CHANGELOG.md.template`
- **Present** → Skip with ✅ (never overwrite history)

#### Directories to Create if Missing
- `.claude/docs/`
- `.claude/commands/`
- `tasks/`
- `[ARCH_LOG_DIR]` (only if neither typo nor correct dir exists)

### Progress Logging

After each file written/updated, append to `tasks/progress.md`:
```
- [timestamp] Created/Updated [filename] — [reason]
```

---

## Step 5: Report Results

After all writes complete, display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  /setup-claude — Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Created:    [list of created files]

🔄 Updated:   [list of updated files with reason]

⏭️  Skipped:   [list of skipped files with reason]

Next Steps:
  1. Review CLAUDE.md and adjust descriptions/key dirs as needed
  2. Customize finish-feature.md with your own architectural notes if desired
  3. Start tracking lessons in tasks/lessons.md
  4. Commit with: git add .claude/ tasks/ CLAUDE.md CHANGELOG.md
                  git commit -m "chore: initialize Claude Code infrastructure"
```

Fill `tasks/todo.md ## Results` with a summary of what was done.

---

## Idempotency Rules

**Never overwrite:**
- `CHANGELOG.md` — destroys history
- `tasks/lessons.md` — destroys accumulated knowledge
- `tasks/todo.md` — destroys in-progress work
- `tasks/findings.md` — destroys detection context
- `tasks/progress.md` — destroys session log

**Safe to overwrite (static guide content):**
- `.claude/docs/changelog-guide.md`
- `.claude/docs/arch-changelog-guide.md`

**Optimize in-place when needed:**
- `CLAUDE.md` — if verbose (>120 lines) or has wrong-project artifacts
- `.claude/commands/finish-feature.md` — if stale references or wrong stack

---

## Detection Ambiguity Handling

If detection is unclear (e.g., monorepo with multiple stacks):
- Prompt user: "Found both Next.js and FastAPI — which is primary?"
- Let user pick or describe the stack
- Proceed with adjusted detection

---

## Test Scenarios

1. **Existing project with `.claude/` + `tasks/`**: mostly "skip" but creates missing `tasks/findings.md`, `tasks/progress.md`, and `plan`/`status` commands
2. **Empty scratch repo**: creates full scaffold from templates
3. **Repo with typo arch dir** (`achritectural_change_log`): generated docs reference typo dir — no new dir created
4. **Re-run idempotency**: second run shows "no changes" — planning files not overwritten, guide files refreshed

---

## File Reference Map

| Generated file | Template source |
|----------------|----------------|
| `CLAUDE.md` | `templates/CLAUDE.md.template` |
| `.claude/commands/finish-feature.md` | `templates/finish-feature.md.template` + `references/templates.md` adaptive sections |
| `.claude/commands/plan.md` | `templates/plan.md.template` |
| `.claude/commands/status.md` | `templates/status.md.template` |
| `.claude/docs/changelog-guide.md` | `templates/changelog-guide.md.template` |
| `.claude/docs/arch-changelog-guide.md` | `templates/arch-changelog-guide.md.template` |
| `tasks/todo.md` | `templates/tasks-todo.md.template` |
| `tasks/findings.md` | `templates/tasks-findings.md.template` |
| `tasks/progress.md` | `templates/tasks-progress.md.template` |
| `tasks/lessons.md` | `templates/tasks-lessons.md.template` |
| `CHANGELOG.md` | `templates/CHANGELOG.md.template` |
