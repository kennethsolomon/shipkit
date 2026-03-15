---
name: setup-optimizer
description: Diagnose, enrich, and maintain CLAUDE.md with comprehensive project context
triggers:
  - optimize claude
  - optimize setup
  - enrich claude
  - maintain claude
  - doctor claude
  - check claude
  - diagnose claude
allowed-tools:
  - Bash
  - Read
  - Write
---

## Overview

Diagnoses your CLAUDE.md for problems, then enriches it with comprehensive project context. Combines health-checking with intelligent auto-discovery.

### What It Does

1. **Diagnoses** — finds missing sections, stale info, inconsistencies, and gaps
2. **Discovers** — scans project structure, docs, and workflows
3. **Enriches** — merges discoveries into CLAUDE.md while preserving your edits

## Usage

```bash
/optimize-claude
```

### Step 0: Diagnose

Before making any changes, runs a diagnostic pass on the existing CLAUDE.md:

- **Missing sections** — checks for essential sections (Stack, Quick Start, Development, etc.)
- **Stale content** — detects outdated info (stale model/route counts, removed dependencies still referenced, generic placeholders)
- **Inconsistencies** — compares documented vs actual project state (directories, scripts, workflows)
- **Section completeness** — flags sections that exist but are empty or have only placeholder text
- **Line count** — warns if file exceeds 150-line target

Reports findings before proceeding. If issues are found, they inform the enrichment step.

### Step 1: Scan & Enrich

After diagnosis, proceeds with discovery and enrichment:

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
