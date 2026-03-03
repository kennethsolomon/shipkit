# CHANGELOG.md Guide

Maintain the project's changelog to track **user-visible changes**.

Related: See [Architectural Changes Guide](./arch-changelog-guide.md) for documenting internal architecture changes (not user-visible).

## Format

Follow Keep a Changelog format:
- `[Unreleased]` section at the top
- Categories: **Added** / **Changed** / **Fixed** / **Deprecated** / **Removed** / **Security**
- Each entry describes what the user sees/experiences

**Example:**
```markdown
## [Unreleased]

### Added
- Two-factor authentication for user login
- API rate limiting on password reset endpoint

### Fixed
- Email validation now accepts + character (RFC 5321 compliance)

### Changed
- User settings panel reorganized for better UX
```

## CHANGELOG.md vs Architectural Log

| What | CHANGELOG.md | Arch Log |
|------|--------------|----------|
| **Audience** | Users, product team | Developers, maintainers |
| **Content** | What users can see/do | How the system works internally |
| **Examples** | "Added dark mode", "Fixed login bug" | "Changed skill interaction patterns", "Added context threading" |
| **Timing** | Before every merge | When architecture actually changes |
| **When to add** | Every feature, bug fix, breaking change | Major refactors, new system patterns, control/data flow changes |

**User-Visible ≠ Architectural**
- Adding a feature = CHANGELOG.md (users see it) + maybe Arch Log (if system architecture changed)
- Bug fix = CHANGELOG.md (fixed a user-facing issue) + maybe Arch Log (if fix required architecture change)
- Adding lessons.md reads to a skill = Arch Log only (users don't see this, it's internal)
- Optimizing performance = CHANGELOG.md (users see faster response) + maybe Arch Log (if optimization changed architecture)

## Rule of thumb

✅ **Add to CHANGELOG.md if:**
- User sees the change (feature, UI update, new endpoint)
- User behavior changes (new workflow, breaking change)
- User experience improves (bug fix, performance improvement)

✅ **Add to Architectural Log if:**
- How skills interact changed
- Data flow through system changed
- New constraints or patterns applied
- Major refactor of system component
- Context threading or integration added

✅ **Add both if:**
- You're adding a feature (CHANGELOG.md) that required architectural changes (Arch Log)
- You're fixing a bug (CHANGELOG.md) that involved discovering a pattern to prevent future bugs (Arch Log lesson)

## Where to Edit

- **CHANGELOG.md** — in project root
- **Architectural Log** — `.claude/docs/architectural_change_log/YYYY-MM-DD-{topic}.md`

Both are checked by `/finish-feature` before merge.

