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
1. **Structure Discovery**: Auto-discovers actual project directories, documentation, and workflows
2. **Comparison Analysis**: Compares what's documented vs what actually exists in the project
3. **Gap Detection**: Identifies undocumented directories, missing documentation links, and workflow gaps
4. **Line count check**: Optimal <150 lines
5. **Section verification**: Ensures essential sections (Stack, Quick Start, Development)
6. **Stale detection**: Finds outdated information and generic placeholders
7. **Stack-specific suggestions**: Context-aware recommendations based on detected framework
8. **Improved version**: Generates suggestion with fixes

### Detection Capabilities:
- **Project Structure**: Discovers src/, tests/, docs/, config/, and other directories
- **Documentation**: Finds README, CONTRIBUTING, docs/*.md, and other documentation
- **Workflows**: Detects npm scripts, Makefile targets, GitHub Actions workflows
- **Stack Analysis**: Identifies framework (React, Django, FastAPI, etc.) for better suggestions
- **Gaps**: Reports what's undocumented and what documentation exists but isn't referenced
- **Content**: Detects generic placeholders and stale information

## Usage

```bash
# Diagnose current CLAUDE.md
/doctor-claude
```

## Output

Displays:
- 🔍 **Project Structure Detected**: Discovered directories, documentation files, and workflows
- 📊 **Line count and section breakdown**: Current state vs optimal
- ⚠️ **Issues found**: Undocumented directories, missing sections, outdated information
- 💡 **Specific suggestions**: Context-aware improvements including stack-specific recommendations
- 📝 **Improved version**: Suggested fixes in CLAUDE.md.setup-claude.md

## Issues Detected

### Common Problems:
1. **File too long** - Exceeds 150 line target
2. **Missing sections** - Stack, Quick Start, or Development sections absent
3. **Outdated content** - Mentions tools not in project.json
4. **Unreplaced placeholders** - Template variables not filled
5. **Incomplete setup** - Missing environment or dependency info

## Workflow

1. Run `/doctor-claude` to see current state
2. Review discovered structure and detected issues
3. Review suggestions (both generic and stack-specific)
4. Manually update CLAUDE.md with recommendations
5. Run `/optimize-claude` if file is too long
6. Run `/doctor-claude` again to verify improvements

## Example Output

For a React project with incomplete documentation:

```
🔍 Project Structure Detected:
   📂 5 directories: src, tests, docs, config, .github
   📚 4 documentation files
   🔧 Workflows: npm (3 scripts)

⚠️  Issues found:
   1. Project has undocumented directories: config, .github
   2. Found 4 documentation files but no documentation section

💡 Suggestions:
   1. Add documentation for: config, .github
   2. Add a 'Documentation & Resources' section linking to docs
   3. Document additional npm scripts: lint, format
   4. Consider adding a 'Components & Architecture' section for React projects
```
