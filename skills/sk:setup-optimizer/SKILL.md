---
name: sk:setup-optimizer
description: "Diagnose, update workflow, deploy hooks, enrich CLAUDE.md, and keep project infrastructure current. The single command for ongoing ShipKit maintenance."
triggers:
  - optimize claude
  - optimize setup
  - enrich claude
  - maintain claude
  - doctor claude
  - check claude
  - diagnose claude
  - refresh claude
  - update claude
  - re-setup
allowed-tools:
  - Bash
  - Read
  - Write
---

## Overview

The single command to keep your entire ShipKit project infrastructure current. Diagnoses problems, updates the workflow, deploys missing hooks, scans your codebase, and enriches CLAUDE.md with project context — all while preserving your customizations.

### What It Does

1. **Diagnoses** — finds missing sections, stale info, inconsistencies, and gaps
2. **Updates workflow** — refreshes the workflow section to the latest template version
3. **Deploys hooks** — installs missing hooks and updates settings.json wiring
4. **Discovers** — scans project structure, docs, and workflows
5. **Enriches** — merges discoveries into CLAUDE.md while preserving your edits

## Usage

```bash
/sk:setup-optimizer
```

### Step 0: Diagnose

Before making any changes, runs a diagnostic pass on the existing CLAUDE.md:

- **Missing sections** — checks for essential sections (Workflow, Sub-Agent Patterns, Cross-Platform Tracking, Project Memory, Lessons Capture, Testing, Commands, etc.)
- **Stale content** — detects outdated info (stale model/route counts, removed dependencies, old command names like `/laravel-lint` instead of `/sk:lint`)
- **Inconsistencies** — compares documented vs actual project state (directories, scripts, workflows)
- **Section completeness** — flags sections that exist but are empty or have only placeholder text
- **Outdated workflow** — checks if the workflow matches the current 8-step flow with `/sk:gates` as single gate step
- **Missing commands** — checks for `sk:start`, `sk:autopilot`, `sk:team`, `sk:learn`, `sk:context-budget`, `sk:health`, `sk:save-session`, `sk:resume-session`, `sk:safety-guard`, `sk:eval` in the Commands table
- **Auto-skip rules** — checks for auto-skip detection rules in the workflow section
- **Stale tracker references** — checks for `tasks/workflow-status.md` references (removed — progress tracked via git branch + todo.md checkboxes)
- **Missing hooks** — checks if `.claude/hooks/` exists and contains both core and enhanced hooks

Reports findings before proceeding. If issues are found, they inform subsequent steps.

### Step 1: Update Workflow

If the workflow section is outdated or missing, replace it with the latest version:

**Current workflow (8 steps, TDD with `/sk:gates` as single gate step):**
```
Explore → Design → Plan → Branch → Write Tests + Implement → Commit → Gates → Finalize
```

**What gets updated:**
- Workflow table (8 steps — `/sk:brainstorm`, `/sk:frontend-design` or `/sk:api-design`, `/sk:write-plan`, `/sk:branch`, `/sk:write-tests` + `/sk:execute-plan`, `/sk:smart-commit`, `/sk:gates`, `/sk:finish-feature`)
- Step details (TDD red/green/verify descriptions)
- Workflow rules (auto-advance, conditional summary, auto-skip, squash gate commits)
- Bug fix flow section (7 steps)
- Hotfix flow section (6 steps)
- Sub-Agent Patterns section (if missing)
- Cross-Platform Tracking section (if missing)
- Project Memory section (if missing)
- Lessons Capture section (if missing)
- Testing TDD section (if missing)
- 3-Strike Protocol (if missing)
- Fix & Retest Protocol section (if missing)
- Requirement Change Flow section (if missing)
- Auto-skip detection rules (if missing)
- Remove `tasks/workflow-status.md` references (tracker removed)

**What gets preserved:**
- Everything marked with `<!-- LOCK -->` is never touched
- Project-specific content below the workflow (conventions, models, routes, architecture)
- Stack section, Build & Run section
- Any section with `<!-- EDITED -->` marker

**How it works:**
1. Read the latest workflow template from `~/.claude/skills/sk:setup-claude/templates/CLAUDE.md.template`
2. Compare with the current CLAUDE.md workflow section
3. If different, replace the workflow section (between `## Workflow` and the next `##` that isn't a workflow subsection)
4. Insert missing sections (Sub-Agent Patterns, Project Memory, etc.) in their correct positions
5. Preserve all `<!-- LOCK -->` and project-specific sections

### Step 1.5: Hooks Deployment

After updating the workflow, check and deploy hooks:

1. **Check if `.claude/hooks/` exists** — if not, create it
2. **Check for core hooks** — `session-start.sh`, `session-stop.sh`, `pre-compact.sh`, `validate-commit.sh`, `validate-push.sh`, `log-agent.sh`
3. **Check for enhanced hooks** — `config-protection.sh`, `post-edit-format.sh`, `console-log-warning.sh`, `cost-tracker.sh`, `suggest-compact.sh`, `safety-guard.sh`
4. **Check `.claude/settings.json`** — verify hooks are wired correctly

**Report status and prompt:**

> "Hooks: [X/6 core, Y/6 enhanced] installed
> Install missing hooks? [y/n]"

**If yes:**

1. **Locate templates** — resolve the ShipKit templates directory:
   - `~/.claude/skills/sk:setup-claude/templates/hooks/` (symlinked install)
   - Or the npm global path if installed via `npm install -g`

2. **Deploy missing hook scripts** (create-if-missing, never overwrite existing):
   ```bash
   # For each missing hook file:
   cp "$TEMPLATE_DIR/hooks/<hook>.sh" ".claude/hooks/<hook>.sh"
   chmod +x ".claude/hooks/<hook>.sh"
   ```

3. **Update `.claude/settings.json`** — read the latest `settings.json.template` and merge new hook entries into the existing settings.json:
   - **Preserve** existing hooks, permissions, statusline config
   - **Add** only missing hook entries (new PreToolUse, PostToolUse, Stop entries)
   - **Never remove** existing entries — additive merge only

4. **Report what was deployed:**
   ```
   Deployed hooks:
     + config-protection.sh (PreToolUse — blocks linter config edits)
     + post-edit-format.sh (PostToolUse — auto-format after edits)
     + console-log-warning.sh (Stop — warn on debug statements)
     + cost-tracker.sh (Stop — session metadata logging)
     + suggest-compact.sh (PreToolUse — compact suggestions)
     + safety-guard.sh (PreToolUse — freeze/careful mode)
     ~ Updated .claude/settings.json with new hook wiring
   ```

**If no:** skip hook deployment, continue to Step 2.

**Idempotency:** Never overwrite existing hook files — the user may have customized them. Only deploy hooks that don't exist yet. For settings.json, merge additively.

### Step 2: Scan & Enrich

After workflow update, proceeds with codebase discovery and enrichment:

1. Scans project for directories, docs, and workflows
2. Reads your existing CLAUDE.md
3. Intelligently merges discoveries with your content (prioritizing diagnosed gaps)
4. Preserves any user customizations
5. Updates CLAUDE.md with comprehensive context

## What Gets Discovered

### Directories
Auto-documents: src/, tests/, docs/, public/, scripts/, config/, migrations/, and more (intelligently excludes node_modules/, vendor/, etc.)

### Documentation
Finds and links: README.md, CONTRIBUTING.md, CHANGELOG.md, docs/*.md, .github/CONTRIBUTING.md, and more

### Workflows
Detects: Makefile targets, npm/yarn scripts, GitHub Actions workflows

## Smart Features

### 1. User Customization Preservation

**Dual Detection:**
- Compares content to detect user edits
- Looks for `<!-- EDITED -->` markers
- Automatically preserves customized sections

**Auto-Locking:**
- `Important Context` section - auto-locked if has content
- `Known Issues` section - auto-locked
- Any section with `<!-- LOCK -->` comment - permanently locked

**Result:** Run multiple times during development without losing work!

### 2. Intelligent Merging

When updating CLAUDE.md:
- ✅ Keeps user customizations intact
- ✅ Updates auto-generated discovery sections
- ✅ Adds newly discovered items
- ✅ Reports what was preserved

### 3. Flexible Line Count

- **Target:** Stay under 200 lines when possible
- **Philosophy:** Comprehensive context > artificial line limit
- **Strategy:** Link to docs instead of inlining if extensive

## Maintenance Workflow

### During Development

```bash
# After adding new test directory
mkdir tests

# Run optimizer to discover it
/optimize-claude

# CLAUDE.md now documents tests/ automatically!
```

### When Customizing

```bash
# Edit Important Context with custom notes
vim CLAUDE.md

# The edit is automatically preserved on next run
/optimize-claude

# ✅ Your notes stay intact!
```

## Configuration

### Smart Defaults (Auto-Locked)
- **Important Context** - Your project decisions
- **Known Issues** - Problems/limitations
- Any section with `<!-- LOCK -->` comment

### Explicit Locking

```markdown
## My Custom Section
<!-- LOCK -->
This content will never be regenerated.
```

## When to Use

✅ **Use `/sk:setup-optimizer` when:**
- ShipKit was updated and your project needs the latest hooks/commands
- You've added new directories to your project
- You've created documentation files
- You want to refresh project context
- Monthly maintenance of CLAUDE.md and hooks

✅ **Safe to run multiple times** — existing customizations and hook files are never overwritten.
