---
name: release
description: "Automate releases: bump version, update CHANGELOG, create git tag, push to GitHub"
---

# Release Automation Skill

Automate the release process: prompt for version, update CHANGELOG.md with release notes, create git tag, and push to GitHub.

## When to Use

Use this skill when you're ready to release a new version:
- After features are implemented, tested, and merged
- When CHANGELOG.md has [Unreleased] section with changes
- To create reproducible, consistent releases

## How It Works

The skill will:

1. **Auto-detect project info:**
   - Project name (from CLAUDE.md, package.json, pyproject.toml, Cargo.toml, etc.)
   - Current version (from CLAUDE.md version line)
   - GitHub repo URL (from git config)

2. **Prompt for missing data:**
   - If version not found, ask user to enter it
   - If GitHub URL not detected, ask for it
   - Ask for release title (with AI suggestion based on [Unreleased] section)

3. **Update files:**
   - Move [Unreleased] → [Version] in CHANGELOG.md
   - Update version in CLAUDE.md
   - Stage changes and create commit

4. **Create release:**
   - Create annotated git tag
   - Push tag to GitHub
   - Provide link to GitHub releases page

## Requirements

- Project must have a `CHANGELOG.md` file (with [Unreleased] section)
- Project should have a version line in `CLAUDE.md` (optional, will prompt if missing)
- Git repository with remote origin configured
- Bash 4.0+

## Usage

```bash
/release
```

Then follow the prompts:
1. Confirm/enter new version (validates semantic versioning format)
2. Confirm/enter release title
3. Review changelog changes
4. Confirm commit and tag creation
5. Confirm push to GitHub

## Workflow Integration

Typical release workflow:
1. Implement features with `/brainstorm` → `/write-plan` → `/execute-plan`
2. Write tests with `/write-tests`
3. When ready to release: `/release`
4. Create GitHub release from the pushed tag

## Notes

- Release process is interactive — you control each step
- Can skip commit or push if desired
- Supports semantic versioning (v1.0.0, v0.2.0-beta, etc.)
- Works with any project type (Node, Python, Go, Rust, etc.)
