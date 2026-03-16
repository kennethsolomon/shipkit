---
name: sk:setup-optimizer
description: "Diagnose, update workflow, enrich, and maintain CLAUDE.md. The single command to keep any CLAUDE.md current."
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

The single command to keep your CLAUDE.md current. Diagnoses problems, updates the workflow to the latest version, scans your codebase, and enriches with project context — all while preserving your customizations.

### What It Does

1. **Diagnoses** — finds missing sections, stale info, inconsistencies, and gaps
2. **Updates workflow** — refreshes the workflow section to the latest template version
3. **Discovers** — scans project structure, docs, and workflows
4. **Enriches** — merges discoveries into CLAUDE.md while preserving your edits

## Usage

```bash
/sk:setup-optimizer
```

### Step 0: Diagnose

Before making any changes, runs a diagnostic pass on the existing CLAUDE.md:

- **Missing sections** — checks for essential sections (Workflow, Sub-Agent Patterns, Project Memory, Lessons Capture, Testing, Commands, etc.)
- **Stale content** — detects outdated info (stale model/route counts, removed dependencies, old command names like `/laravel-lint` instead of `/sk:lint`)
- **Inconsistencies** — compares documented vs actual project state (directories, scripts, workflows)
- **Section completeness** — flags sections that exist but are empty or have only placeholder text
- **Outdated workflow** — checks if the workflow matches the current 27-step TDD flow with hard gates

Reports findings before proceeding. If issues are found, they inform subsequent steps.

### Step 1: Update Workflow

If the workflow section is outdated or missing, replace it with the latest version:

**Current workflow (27 steps, TDD with hard gates):**
```
Read → Explore → Design → Accessibility → Plan → Branch → Migrate → Write Tests → Implement → Lint → Verify Tests → Security → Performance → Review → E2E Tests → Finish → Sync Features
```

**What gets updated:**
- Workflow table (27 steps with correct commands: `/sk:write-tests`, `/sk:lint`, `/sk:test`, `/sk:accessibility`, `/sk:perf`, `/sk:e2e`)
- Step details (TDD red/green/verify descriptions)
- Tracker rules (hard gates at 12, 14, 16, 20, 22; optional steps 4, 5, 8, 18, 27)
- Step completion summary rule (NON-NEGOTIABLE)
- Bug fix flow section
- Sub-Agent Patterns section (if missing)
- Project Memory section (if missing)
- Lessons Capture section (if missing)
- Testing TDD section (if missing)
- 3-Strike Protocol (if missing)
- Fix & Retest Protocol section (if missing)
- Requirement Change Flow section (if missing)

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

✅ **Use `/optimize-claude` when:**
- You've added new directories to your project
- You've created documentation files
- You want to refresh project context
- Monthly maintenance of CLAUDE.md

✅ **Safe to run multiple times during development** - Your customizations are always preserved!
