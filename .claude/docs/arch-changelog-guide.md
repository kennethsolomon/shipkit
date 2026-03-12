# Architectural Changes Guide

Create an entry when you change architecture (data flow, patterns, schema strategy, global state, major subsystem refactors, skill interactions, context flow).

## Quick Start: Auto-Detection (Recommended)

When running `/finish-feature`, step 4 automatically:

1. **Analyzes your diff** to detect architectural changes
2. **Auto-generates a markdown draft** in `.claude/docs/architectural_change_log/`
3. **Shows you the draft** with TODO sections pre-filled
4. **You review and edit** the Detailed Changes and Before/After sections
5. **You commit** the final arch log

**Example:**
```bash
/finish-feature
# Step 4: Check for Architectural Changes
✓ Detected: Data Flow + Control Flow changes
✓ Generated: .claude/docs/architectural_change_log/2026-03-04-context-threading.md

# Edit the file to fill in TODO sections
# Then: git add .claude/docs/... && git commit -m "docs: add arch log"
```

## Manual Creation (If Needed)

If you need to create an arch log manually (or if auto-detection missed something):

1. **Run the detector** to get a draft:
   ```bash
   python3 $HOME/.claude/plugins/claude-skills/skills/setup-claude/scripts/detect_arch_changes.py
   ```

2. **Edit the generated file** at `.claude/docs/architectural_change_log/`

3. **Fill in the TODO sections:**
   - What specifically changed in the architecture?
   - Before/after explanation
   - Verification checklist

## What Counts as Architectural Change

| Category | Examples |
|----------|----------|
| **Control Flow** | Skills interact differently, execution order changed, new workflow steps |
| **Data Flow** | New context files, findings.md/lessons.md reads/writes added, context threading |
| **Pattern** | New design patterns, changed template patterns, new conventions |
| **Subsystem** | Major refactor of existing component, breaking changes to API |
| **Integration** | New connections between skills, new inter-skill communication |

## Naming Convention

**Format:** `YYYY-MM-DD-{topic}.md`

**Examples:**
- `2026-03-03-context-threading-enhancement.md`
- `2026-02-15-skill-interaction-refactor.md`
- `2026-01-10-data-flow-optimization.md`

## File Location

All arch logs go in: `.claude/docs/architectural_change_log/`

This directory is referenced by `CLAUDE.md` and never cleared (similar to `tasks/lessons.md`).

## Auto-Detection Script

**Location:** `setup-claude/scripts/detect_arch_changes.py`

**What it detects** (works for ANY project):
- **Schema/Database changes** — migrations, schema.prisma, models/ → Data Flow
- **API/Route changes** — routes, endpoints, controllers, middleware → Control Flow
- **Component/Module changes** — src/components/, pages/, lib/ → Pattern
- **Subsystem changes** — new top-level directories → Subsystem
- **Configuration changes** — config files that affect architecture → Configuration
- **Dependency changes** — package.json, requirements.txt → Integration
- **Context integration** — findings.md, lessons.md reads/writes → Integration
- **Documentation** — README, docs/ updates → Documentation

**Usage:**
```bash
# See what would be detected (dry-run):
python3 detect_arch_changes.py --dry-run

# Generate and save arch log draft:
python3 detect_arch_changes.py

# Debug: show analysis details:
python3 detect_arch_changes.py --show-analysis
```

**Example detections:**
```
Next.js project:
  → Changes to src/components/ → Component Architecture Update
  → Schema changes in prisma/ → Data Model Refactor
  → API routes in app/api/ → API Structure Enhancement

Django project:
  → Changes to models.py → Data Model Refactor
  → Changes to urls.py → API Structure Enhancement
  → New apps/ → Subsystem Refactor

Python project:
  → Changes to requirements.txt → Dependency Upgrade
  → Changes to src/core/ → Component Architecture Update
```

## Benefits of Architectural Logging

✅ Maintains system knowledge across sessions
✅ Documents "why" changes were made (rationale, trade-offs)
✅ Helps future developers understand architecture
✅ Audit trail of system evolution
✅ Auto-detection means 80% already drafted — you just add context
✅ Consistent format across all projects

