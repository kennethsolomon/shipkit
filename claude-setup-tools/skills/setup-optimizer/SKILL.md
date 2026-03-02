---
name: setup-optimizer
description: Optimize CLAUDE.md to stay under 150 lines
triggers:
  - optimize setup
  - optimize claude
  - trim claude
allowed-tools:
  - Bash
  - Read
  - Write
---

## Overview

Automatically optimizes your CLAUDE.md file to stay under the 150-line target while preserving essential information.

### What it does:
1. Analyzes current line count
2. Applies optimization strategies
3. Removes redundancy and verbose descriptions
4. Collapses sections where possible
5. Updates file directly or creates sidecar
6. Reports before/after line counts

### Optimization Strategies:
- Remove multiple consecutive empty lines
- Tighten section descriptions
- Combine related information
- Remove verbose examples
- Clean up formatting
- Preserve all essential sections

## Usage

```bash
# Optimize current CLAUDE.md
/optimize-claude
```

## Output

Shows:
- Before/after line counts
- Bytes/lines saved
- Success message or sidecar location

## How It Works

### For Generated Files (with marker):
- Updates file directly
- Preserves all sections
- Applies intelligent trimming

### For Custom Files (no marker):
- Creates CLAUDE.md.setup-claude.md suggestion
- Never modifies original file
- Shows suggestions for review

## Line Count Target

**Goal**: Keep CLAUDE.md under 150 lines

**Why**:
- Easier to review and understand
- Better Claude context efficiency
- Forces prioritization of essential info
- Remains scannable at a glance

## Optimization Examples

### Before (180 lines):
```
- Lengthy descriptions
- Multiple empty lines between sections
- Verbose examples
- Redundant information
```

### After (140 lines):
```
- Concise descriptions
- Single empty lines between sections
- Brief examples
- No repetition
```

## Next Steps

1. Run `/optimize-claude` if file > 150 lines
2. Review the optimized version
3. If sidecar was created, merge manually
4. Run `/doctor-claude` to verify
