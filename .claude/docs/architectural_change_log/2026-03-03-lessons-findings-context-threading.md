# Lessons + Findings Context Threading (March 3, 2026)

## Summary

Completed the compounding lesson system by ensuring every skill that makes design or planning decisions reads `tasks/lessons.md` and every skill that accepts handoff reads `tasks/findings.md`.

## Changes

### Skill Files Modified

1. **`brainstorming/SKILL.md`**
   - Now reads `tasks/findings.md` and `tasks/lessons.md` at start
   - Checklist item 1: reads findings + lessons before exploring context
   - "Understanding the idea" block: applies lessons as design constraints

2. **`frontend-design/SKILL.md`**
   - Added "Before You Start" block
   - Reads `tasks/findings.md` as design brief (avoids re-asking prior decisions)
   - Reads `tasks/lessons.md` for Bug constraints related to component architecture

3. **`setup-claude/templates/commands/`**
   - `finish-feature.md.template`: Scans diff against lessons.md Bug patterns before merge (final gate)
   - `plan.md.template`: Applies lessons.md as constraints when filling todo.md
   - `brainstorm.md.template`, `execute-plan.md.template`, `write-plan.md.template`: Updated with findings/lessons pattern

### Documentation

- **`README.md`**: Added "Workflow Scenarios" section with 4 detailed examples:
  1. Feature branch workflow (8 steps with 2FA example)
  2. Bug fix with lesson learning (demonstrates /debug deep dive)
  3. Command reference table (when/why to use each skill)
  4. Lessons compounding over time (multi-day feedback loop)

## Impact

### System Architecture

- **Context threading complete**: findings.md flows through brainstorm → write-plan → frontend-design; lessons.md read by 6+ skills
- **Prevention loop active**: One bug debugged with `/debug` now becomes a constraint on 5+ subsequent workflows
- **Compounding knowledge**: Each session makes the system smarter per-project without resetting context

### Workflow Pattern

```
/brainstorm (reads findings.md + lessons.md)
    ↓ (writes to findings.md)
/write-plan (reads findings.md + lessons.md)
    ↓ (writes to todo.md)
/execute-plan (reads lessons.md + progress.md)
    ↓ (writes to progress.md + findings.md)
/write-tests (reads lessons.md)
/review (reads lessons.md as targeted checks)
/finish-feature (scans diff against lessons.md Bug patterns)
    ↓ (final gate before merge)
/debug (if needed: writes findings.md + lessons.md)
```

### Bug Reduction Mechanism

The lessons.md hard constraint pattern now covers:
1. **Planning phase**: `/write-plan` applies lessons as constraints
2. **Execution phase**: `/execute-plan` reads lessons before each batch
3. **Testing phase**: `/write-tests` reads lessons before generating tests
4. **Review phase**: `/review` uses lessons' Bug field as targeted checks
5. **Pre-merge phase**: `/finish-feature` scans diff against Bug patterns
6. **Debug phase**: `/debug` writes lessons for prevention

## Files Changed

- `brainstorming/SKILL.md` (added 5 lines to checklist + understanding section)
- `frontend-design/SKILL.md` (added "Before You Start" block)
- `setup-claude/templates/commands/finish-feature.md.template` (added "Before You Start" block)
- `setup-claude/templates/commands/plan.md.template` (added "Before You Start" block)
- `setup-claude/templates/commands/brainstorm.md.template` (updated)
- `setup-claude/templates/commands/execute-plan.md.template` (updated)
- `setup-claude/templates/commands/write-plan.md.template` (updated)
- `README.md` (added comprehensive "Workflow Scenarios" section)
- `.gitignore` (removed brainstorming/ and frontend-design/ — custom skills, not auto-installed)

## Verification

✅ All skills that make decisions read lessons.md
✅ All skills that accept handoff read findings.md
✅ Graceful degradation: reads skip if task files don't exist
✅ Works identically for new and existing projects
✅ README updated with step-by-step tutorials and scenarios

## Commit

`7a3f4c8` — "feat: close remaining skill gaps with lessons + findings context threading"
