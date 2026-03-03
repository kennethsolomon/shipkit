---
name: review
description: "Honest self-review of all branch changes with severity levels. Flags bugs, security issues, code quality. Creates PR via gh."
---

# Self-Review + PR Creation

## Overview

Perform an honest, thorough review of all changes on the current branch. Flag bugs, security issues, and code quality problems with severity levels. Then create a PR via `gh` if requested.

**You are the reviewer, not the cheerleader.** Your job is to find problems, not to praise the code. If you find nothing wrong, look harder. Real code almost always has something worth flagging.

## Allowed Tools

Bash, Read, Glob, Grep

**Intentionally NO Write or Edit** — this skill is report-only. If issues are found, the user decides what to fix.

## Steps

You MUST complete these steps in order:

### 1. Read Project Conventions

```
CLAUDE.md                  — Coding standards, conventions, known patterns
```

Understand what "correct" looks like for this project.

### 2. Collect All Changes

```bash
# Determine base branch
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"

# All changes on this branch
git diff main..HEAD
git diff main..HEAD --stat
git log main..HEAD --oneline

# Check for uncommitted changes
git status --short
```

If there are uncommitted changes, warn:
> **Warning:** You have uncommitted changes. These will NOT be included in the review. Commit or stash them first.

### 3. Analyze — Bugs

Review the diff for common bug patterns:

- **Off-by-one errors**: Loop bounds, array indexing, string slicing
- **Null/undefined access**: Missing null checks, optional chaining needed
- **Unhandled promises**: Missing await, unhandled rejections, floating promises
- **Race conditions**: Shared state mutation, async ordering assumptions
- **Resource leaks**: Unclosed connections, file handles, event listeners
- **Logic errors**: Wrong operator, inverted condition, missing break/return
- **Type mismatches**: Implicit coercion, wrong argument types
- **State inconsistency**: Partial updates, missing rollback on error

### 4. Analyze — Security

Load `references/security-checklist.md` and check for:

- **Injection**: SQL, NoSQL, command, LDAP, template injection
- **XSS**: Unescaped output, dangerouslySetInnerHTML, innerHTML
- **Authentication**: Weak tokens, missing validation, hardcoded secrets
- **Authorization**: Missing access checks, IDOR, privilege escalation
- **Sensitive data**: Credentials in code, PII in logs, missing encryption
- **Dependencies**: Known vulnerable packages, outdated security patches

### 5. Analyze — Code Quality

- **Naming**: Are names descriptive and consistent with project conventions?
- **Dead code**: Commented-out code, unused imports, unreachable branches
- **DRY violations**: Copy-pasted logic that should be extracted
- **Function length**: Functions over ~50 lines that should be split
- **Error handling**: Swallowed errors, generic catch blocks, missing error messages
- **Complexity**: Deeply nested logic, excessive branching

### 6. Analyze — Framework-Specific

Based on what the project uses:

**React/Next.js:**
- Missing keys in lists
- useEffect dependency arrays (missing deps, unnecessary deps)
- Client vs server component boundaries (Next.js App Router)
- State updates on unmounted components

**Python:**
- Missing type hints on public functions
- Mutable default arguments
- Bare except clauses
- Async context managers not used

**Go:**
- Unchecked error returns
- Deferred function errors ignored
- Goroutine leaks
- Missing mutex for shared state

**General:**
- Environment-specific code without feature flags
- Missing input validation at system boundaries
- Inconsistent error response format

### 7. Generate Review Report

Format findings with severity levels:

```markdown
## Code Review: [branch-name]

**Changes:** X files changed, +Y/-Z lines
**Commits:** N commits

### Critical (must fix before merge)
- [FILE:LINE] Description of critical issue
  **Why:** Explanation of impact

### Warning (should fix)
- [FILE:LINE] Description of warning
  **Why:** Explanation of risk

### Nitpick (consider for next time)
- [FILE:LINE] Description of suggestion
  **Why:** Explanation of improvement
```

Rules:
- Maximum 15 items total (prioritize by severity)
- Every item must reference a specific file and line
- Every item must explain **why** it matters, not just what's wrong
- If you genuinely find nothing, say so — but that's rare

### 8. Ask About PR

After presenting the review:

> Review complete. Would you like to create a pull request?

If the user says no, stop here.

### 9. Create PR

If the user wants a PR:

1. **Check remote status:**
```bash
git remote -v
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "no upstream"
```

2. **Push branch if needed:**
```bash
git push -u origin HEAD
```

3. **Generate PR title and body:**
   - Title: Short, imperative, under 70 characters
   - Body: Summary of changes, review findings (if any critical/warnings), test status

4. **Create PR:**
```bash
gh pr create --title "title here" --body "$(cat <<'EOF'
## Summary
- bullet points of key changes

## Review Notes
- Any critical or warning items from the review

## Test Plan
- How to verify the changes

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

5. Report the PR URL to the user.
