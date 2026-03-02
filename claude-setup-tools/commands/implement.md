# How to Implement CLAUDE.md

Complete workflow for creating and optimizing your project's CLAUDE.md file.

## Workflow Overview

```
1. Create/Detect → 2. Review → 3. Diagnose → 4. Optimize → 5. Finalize
```

## Step 1: Create or Generate CLAUDE.md

### For New Projects

```bash
/setup-starter
```

This command:
- Detects your tech stack automatically
- Generates optimized CLAUDE.md
- Includes all essential sections
- Takes ~30 seconds

**Result**: CLAUDE.md ready to customize

### For Existing Projects

If you already have a custom CLAUDE.md, we'll create a suggestion file instead:
- Checks if CLAUDE.md has the generation marker
- If marked (generated), updates it directly
- If custom (no marker), creates CLAUDE.md.setup-claude.md suggestion

## Step 2: Review the Generated File

After `/setup-starter`, check:

✅ **Project name and description** - Correct?
✅ **Stack table** - All technologies listed?
✅ **Quick start command** - Does it work?
✅ **Key files section** - Important directories listed?
✅ **Development commands** - Are commands accurate?

### Common Customizations

- Update description with more detail
- Add framework-specific notes
- Include deployment instructions
- Add links to documentation
- Note any special conventions

## Step 3: Diagnose Issues

```bash
/doctor-claude
```

This command:
- Checks for missing sections
- Validates line count (< 150)
- Detects outdated information
- Suggests improvements

**Example output**:
```
⚠️ Issues found:
   1. File is too long: 180 lines (target: < 150)
   2. Missing essential sections: Development

💡 Suggestions:
   1. Run `/optimize-claude` to trim unnecessary sections
   2. Add a 'Development' section with setup instructions
```

## Step 4: Optimize if Needed

If your CLAUDE.md exceeds 150 lines:

```bash
/optimize-claude
```

This command:
- Removes redundancy
- Tightens descriptions
- Collapses related sections
- Preserves essential information

**Result**: Optimized file under 150 lines

### Before Optimization (180 lines):
- Verbose descriptions
- Redundant information
- Multiple empty lines
- Extra examples

### After Optimization (140 lines):
- Concise, clear descriptions
- No duplication
- Single spacing between sections
- Essential examples only

## Step 5: Final Review

Run `/doctor-claude` again to verify:

```bash
/doctor-claude
```

Expected output:
```
✅ No major issues found!
📊 Lines: 142/150
📑 Sections: Stack, Quick Start, Project Structure, ...
```

## Timeline

| Step | Command | Time |
|------|---------|------|
| Create | `/setup-starter` | 30 sec |
| Review | Manual | 5 min |
| Diagnose | `/doctor-claude` | 10 sec |
| Optimize | `/optimize-claude` | 10 sec |
| Verify | `/doctor-claude` | 10 sec |
| **Total** | **All** | **~6 min** |

## Tips & Tricks

### For New Projects
1. Start fresh with `/setup-starter`
2. Customize with project-specific details
3. Run `/doctor-claude` to verify
4. Commit to repository

### For Existing Projects
1. Run `/doctor-claude` first
2. Review suggested improvements
3. Run `/optimize-claude` if needed
4. Manually merge suggestions if desired
5. Verify with final `/doctor-claude` run

### Common Issues & Solutions

**Issue**: File is custom (no marker)
- **Solution**: Changes are written to `.setup-claude.md` suggestions file
- **Fix**: Review the suggestion and manually merge good ideas

**Issue**: Commands don't match actual project
- **Solution**: Edit CLAUDE.md directly after generation
- **Action**: Update command sections with real values

**Issue**: File keeps growing
- **Solution**: Run `/optimize-claude` to trim
- **Action**: Remove verbose descriptions, consolidate sections

**Issue**: Missing sections
- **Solution**: Add manually after generation
- **Action**: Review what's important for new contributors

## Advanced: Customization

### Adding Custom Sections

After `/setup-starter`, you can add:
- Architecture diagram (ASCII art)
- Deployment process
- Known limitations
- Common pitfalls
- Performance considerations
- Security notes

### Keeping It Current

Review CLAUDE.md when:
- Adding new dependencies
- Changing build process
- Restructuring directories
- Updating deployment strategy
- Onboarding new team members

### Integration with setup-claude

If using `/setup-claude` for project scaffolding:
1. Run `/setup-claude` first (creates project structure)
2. Then run `/setup-starter` (creates CLAUDE.md)
3. Customize CLAUDE.md with project details
4. Verify with `/doctor-claude`

## Next Steps

- **Learn sections**: Read `/explain-claude` for detailed section guide
- **Review quality**: Check `/review-claude` for quality checklist
- **Optimize**: Use `/optimize-claude` when file grows
- **Diagnose**: Use `/doctor-claude` to find issues

---

**Commands Summary**:
- `/setup-starter` - Create CLAUDE.md
- `/doctor-claude` - Diagnose issues
- `/optimize-claude` - Trim to < 150 lines
- `/explain-claude` - Understand sections
- `/review-claude` - Quality checklist
