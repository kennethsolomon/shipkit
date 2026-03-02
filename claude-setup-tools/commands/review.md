# CLAUDE.md Review Checklist

Use this checklist to verify your CLAUDE.md is complete, correct, and ready for use.

## Quick Check (5 minutes)

- [ ] File exists and is readable
- [ ] No syntax errors (valid Markdown)
- [ ] Line count reasonable (under 150 lines)
- [ ] No unreplaced placeholders like `[PROJECT]`

**Command**: `wc -l CLAUDE.md`

## Content Accuracy (10 minutes)

### Project Information
- [ ] Project name matches directory/package.json
- [ ] Description is accurate and up-to-date
- [ ] Description is 1-2 sentences (concise)

### Technology Stack
- [ ] Language is correct (JavaScript, Python, Go, Rust, etc.)
- [ ] Framework listed correctly
- [ ] Database system accurate (or "None" if not applicable)
- [ ] UI framework/library correct
- [ ] Testing framework correct

**Test**: Check `package.json` or equivalent configuration file

### Commands
- [ ] Dev command actually works: `[DEV_COMMAND]`
- [ ] Build command is accurate: `[BUILD_COMMAND]`
- [ ] Test command works: `[TEST_COMMAND]`
- [ ] Lint command is valid: `[LINT_COMMAND]`

**Test**: Run each command and verify success

## Structure Validation (5 minutes)

Essential Sections Present:
- [ ] Project header with name and description
- [ ] Stack table with tech layers
- [ ] Quick Start with working command
- [ ] Project Structure with directory overview
- [ ] Key Files with important paths
- [ ] Development section with commands
- [ ] Important Context noting tech decisions

Optional but Recommended:
- [ ] Build & Deploy section
- [ ] Environment Variables guide
- [ ] Common Tasks with examples
- [ ] Documentation links

## Quality Checks (10 minutes)

### Clarity
- [ ] Instructions are specific and clear
- [ ] No vague terms ("some", "various", "etc.")
- [ ] Commands have actual values, not placeholders
- [ ] File paths are real and correct

### Completeness
- [ ] New contributor can start with Quick Start
- [ ] All major technologies mentioned
- [ ] Build/deploy process documented
- [ ] Environment setup explained

### Accuracy
- [ ] Run `/doctor-claude` - no major issues
- [ ] All technology versions still supported
- [ ] No outdated information
- [ ] Commands match actual project

### Efficiency
- [ ] No redundant information
- [ ] No verbose descriptions
- [ ] Each section has clear purpose
- [ ] Line count under 150

## Automated Check

```bash
# Run doctor to catch common issues
/doctor-claude
```

Expected output:
```
✅ No major issues found!
📊 Lines: 120/150
📑 Sections: Stack, Quick Start, Project Structure, ...
```

## Before Final Commit

### Pre-Commit Checklist
- [ ] Run `/doctor-claude` - passes
- [ ] File is properly formatted (no syntax errors)
- [ ] All commands tested and working
- [ ] Team members reviewed
- [ ] Documentation links verified

### For New Projects
- [ ] Based on generated version from `/setup-starter`
- [ ] Customized with project specifics
- [ ] Technology choices documented
- [ ] Onboarding guide is complete

### For Existing Projects
- [ ] Updated after tech stack changes
- [ ] Commands verified with recent code
- [ ] Any deprecations addressed
- [ ] Suggestions from `/doctor-claude` applied

## Common Issues and Fixes

| Issue | Fix | Command |
|-------|-----|---------|
| File too long (> 150 lines) | Use optimization tool | `/optimize-claude` |
| Missing sections | Add required sections manually | - |
| Outdated commands | Test and update commands | - |
| Unreplaced placeholders | Find and replace with real values | - |
| Tech stack mismatch | Verify against package.json | - |

## Issue Resolution Steps

### If `/doctor-claude` finds issues:

1. **Read the suggestions** carefully
2. **For length issues**:
   - Run `/optimize-claude` to auto-trim
   - Or manually remove verbose descriptions
3. **For missing sections**:
   - Add the required section
   - Or verify it's covered elsewhere
4. **For outdated information**:
   - Update with current values
   - Test commands to verify
5. **Run `/doctor-claude` again** to verify fixes

## Manual Review Tips

### Look For:
- ✅ Specific command examples (`npm run dev`, not `run dev`)
- ✅ Real file paths (`src/components/`, not `src/`)
- ✅ Actual technology names (React, not `frontend framework`)
- ✅ Correct line breaks and spacing
- ✅ Proper Markdown formatting

### Avoid:
- ❌ Generic placeholders (replace all `[WORD]` patterns)
- ❌ Vague instructions (be specific)
- ❌ Outdated technology versions
- ❌ Broken documentation links
- ❌ Verbose or redundant sections

## Final Sign-Off

Before considering CLAUDE.md complete:

```bash
# 1. Run diagnostic
/doctor-claude

# 2. Test all commands
npm run dev      # or equivalent
npm test         # or equivalent
npm run build    # or equivalent

# 3. Check optimization
echo "Line count: $(wc -l < CLAUDE.md)"
# Should be under 150

# 4. Have teammate review
# Ask: "Can you start this project using CLAUDE.md?"

# 5. If all good, commit
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md with current stack"
```

## Workflow Integration

### For New Projects
1. Generate with `/setup-starter`
2. Customize manually
3. Use this checklist to verify
4. Commit to repository

### For Existing Projects
1. Run `/doctor-claude` to find issues
2. Use this checklist to guide fixes
3. Apply suggestions from doctor
4. Run `/optimize-claude` if needed
5. Final verification and commit

### For Maintenance
1. Update CLAUDE.md when tech stack changes
2. Run `/doctor-claude` periodically
3. Use this checklist before major updates
4. Commit changes promptly

## Quick Reference Commands

```bash
# Generate CLAUDE.md for new project
/setup-starter

# Check for issues
/doctor-claude

# Trim to < 150 lines if needed
/optimize-claude

# Understand sections better
/explain-claude

# Full workflow walkthrough
/implement-claude
```

---

**Pass all checks?** Great! Your CLAUDE.md is ready for production use.
