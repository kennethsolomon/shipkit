---
name: claude-doctor
description: Diagnose and suggest improvements for CLAUDE.md
triggers:
  - doctor claude
  - check claude
  - diagnose claude
allowed-tools:
  - Bash
  - Read
---

## Overview

Analyzes your CLAUDE.md file and provides a diagnostic report with actionable suggestions for improvement.

### What it does:
1. Checks line count (optimal: < 150 lines)
2. Verifies essential sections present
3. Detects outdated information
4. Checks for unreplaced placeholders
5. Generates improved version as suggestion
6. Provides specific recommendations

### Detection Checks:
- **Length**: Warns if exceeds 150 lines
- **Structure**: Verifies essential sections (Stack, Quick Start, Development)
- **Content**: Detects stale information and generic placeholders
- **Completeness**: Suggests missing common sections

## Usage

```bash
# Diagnose current CLAUDE.md
/doctor-claude
```

## Output

Displays:
- Line count and section breakdown
- List of issues found
- Specific suggestions for improvement
- Improved version as CLAUDE.md.setup-claude.md (optional)

## Issues Detected

### Common Problems:
1. **File too long** - Exceeds 150 line target
2. **Missing sections** - Stack, Quick Start, or Development sections absent
3. **Outdated content** - Mentions tools not in project.json
4. **Unreplaced placeholders** - Template variables not filled
5. **Incomplete setup** - Missing environment or dependency info

## Workflow

1. Run `/doctor-claude` to see current state
2. Review suggestions
3. Run `/optimize-claude` if file is too long
4. Manually update CLAUDE.md with other suggestions
5. Run `/doctor-claude` again to verify improvements
