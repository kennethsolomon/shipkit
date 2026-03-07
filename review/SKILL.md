---
name: review
description: "Honest self-review of all branch changes with severity levels. Flags bugs, security issues, code quality. Report-only — no PR creation (that's /finish-feature's job)."
---

# Self-Review

## Overview

Perform an honest, thorough review of all changes on the current branch. Flag bugs, security issues, and code quality problems with severity levels.

**You are the reviewer, not the cheerleader.** Your job is to find problems, not to praise the code. If you find nothing wrong, look harder. Real code almost always has something worth flagging.

This is a **report-only** step. If Critical or Warning issues are found, the user loops back to `/debug` → `/commit` → `/review` until the branch is clean. Once clean, the user runs `/finish-feature` to finalize and create the PR.

## Allowed Tools

Bash, Read, Glob, Grep

**Intentionally NO Write or Edit** — this skill is report-only. If issues are found, the user decides what to fix.

## Steps

You MUST complete these steps in order:

### 1. Read Project Conventions

```
CLAUDE.md                  — Coding standards, conventions, known patterns
tasks/lessons.md           — Recurrent bug patterns for this project (if exists)
tasks/security-findings.md — Prior security audit results (if exists)
```

Understand what "correct" looks like for this project.

If `tasks/lessons.md` exists, read it in full. Use each active lesson's **Bug** field
as an additional targeted check during diff analysis in Steps 3–5 — treat each lesson
as a known failure mode to explicitly scan for.

If `tasks/security-findings.md` exists, read the most recent audit. Use any unresolved
Critical/High findings as additional targeted checks during the security analysis in
Step 4 — verify the current diff doesn't reintroduce previously flagged vulnerabilities.

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

### 8. Next Steps

After presenting the review:

If there are **Critical** or **Warning** items:
> "Review found issues that should be addressed. Fix them with `/debug`, commit with `/commit`, then re-run `/review` to verify."

If there are only **Nitpick** items (no Critical/Warning):
> "Review complete — no critical issues found, but there are some nitpicks. Would you like to fix them now, or proceed to `/finish-feature`?"

If the user wants to fix nitpicks, loop back to `/debug` + `/commit` → `/review`.

If the review is **completely clean**:
> "Review complete — no issues found. Run `/finish-feature` to finalize the branch and create a PR."
