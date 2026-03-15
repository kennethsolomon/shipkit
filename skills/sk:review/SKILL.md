---
name: sk:review
description: "Rigorous self-review of all branch changes across 7 dimensions: correctness, security, performance, reliability, design quality, best practices, and testing. Report-only — no PR creation (that's /sk:finish-feature's job). Use when code is complete and ready for review before merging."
---

# Self-Review

## Overview

Perform a rigorous, multi-dimensional review of all changes on the current branch. This review aims for the quality bar of a senior engineer at a top-tier tech company — thorough, specific, and honest.

**You are the reviewer, not the cheerleader.** Your job is to find problems, not to praise the code. If you find nothing wrong, look harder. Real code almost always has something worth flagging. Think about what could go wrong in production at scale, under adversarial conditions, and over time as the codebase evolves.

This is a **report-only** step. If Critical or Warning issues are found, the user loops back to `/sk:debug` → `/sk:smart-commit` → `/sk:review` until the branch is clean. Once clean, the user runs `/sk:finish-feature` to finalize and create the PR.

## Allowed Tools

Bash, Read, Glob, Grep

**Intentionally NO Write or Edit** — this skill is report-only. If issues are found, the user decides what to fix.

## Steps

You MUST complete these steps in order:

### 1. Read Project Context

```
CLAUDE.md                  — Coding standards, conventions, known patterns
tasks/lessons.md           — Recurrent bug patterns for this project (if exists)
tasks/security-findings.md — Prior security audit results (if exists)
```

Understand what "correct" looks like for this project — the tech stack, conventions, and known pitfalls.

If `tasks/lessons.md` exists, read it in full. Use each active lesson's **Bug** field
as an additional targeted check during analysis — treat each lesson as a known failure
mode to explicitly scan for across all review dimensions.

If `tasks/security-findings.md` exists, read the most recent audit. Use any unresolved
Critical/High findings as additional targeted checks — verify the current diff doesn't
reintroduce previously flagged vulnerabilities.

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

Read the full content of every changed file (not just the diff hunks) to understand context around the changes.

### 3. Analyze — Correctness & Bugs

The most important dimension. A bug that ships is worse than ugly code that works.

**Logic errors:**
- Wrong operator (`&&` vs `||`, `==` vs `===`, `<` vs `<=`)
- Inverted conditions, missing negation
- Missing `break`/`return`/`continue` in control flow
- Off-by-one errors in loops, array indexing, string slicing, pagination

**Null/undefined safety:**
- Missing null checks before property access
- Optional chaining needed but not used
- Nullable values passed where non-null expected
- Array/object destructuring on potentially undefined values

**Async correctness:**
- Missing `await` on async calls (floating promises)
- Unhandled promise rejections
- Race conditions from shared state mutation across async boundaries
- Async operations in loops without proper batching (`Promise.all` vs sequential)

**Data integrity:**
- Partial updates without transactions (DB operations that should be atomic)
- Missing rollback on error in multi-step operations
- Stale closures capturing outdated state
- Cache invalidation gaps (data updated but cache not cleared)

**Edge cases:**
- Empty arrays/strings/objects not handled
- Negative numbers, zero, MAX_INT boundaries
- Unicode/special characters in user input
- Concurrent access to shared resources

### 4. Analyze — Security

Load `references/security-checklist.md` and apply its grep patterns systematically. Check for:

**Injection (OWASP A03):**
- SQL, NoSQL, OS command, LDAP, template injection
- String concatenation/interpolation in queries instead of parameterized queries
- `eval()`, `exec()`, `Function()` with any dynamic input

**Cross-Site Scripting (OWASP A03):**
- `dangerouslySetInnerHTML`, `innerHTML`, `v-html` without sanitization
- URL parameters reflected without encoding
- User content rendered in `href`, `src`, or event handler attributes

**Authentication & Authorization (OWASP A01, A07):**
- Hardcoded secrets, API keys, tokens in source code
- Missing auth checks on endpoints (especially admin, destructive operations)
- IDOR — user-controlled IDs accessing other users' resources without ownership verification
- Weak session management, missing token rotation

**Data exposure (OWASP A02):**
- Credentials, PII, or tokens in logs
- Stack traces or internal errors leaked to clients
- Sensitive data in client-side bundles (secret keys in frontend code)
- Missing encryption for sensitive data at rest

**Configuration (OWASP A05):**
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Overly permissive CORS (`origin: '*'`)
- Debug mode enabled in production paths
- Missing rate limiting on auth/sensitive endpoints

### 5. Analyze — Performance

Think about what happens at 10x, 100x current scale. Performance bugs are often invisible in development but catastrophic in production.

**Database & queries:**
- N+1 query patterns (fetching related data in a loop instead of a join or batch)
- Missing database indexes for frequently queried columns
- `SELECT *` when only specific columns are needed
- Unbounded queries without `LIMIT`/pagination
- Missing connection pooling or pool exhaustion risks

**Algorithm & data structures:**
- O(n²) or worse in hot paths (nested loops over large collections)
- Repeated expensive computations that should be memoized
- Large data structures held in memory unnecessarily
- String concatenation in tight loops (use array join/builder)

**Frontend performance (React/Next.js):**
- Unnecessary re-renders (missing `React.memo`, `useMemo`, `useCallback` where beneficial)
- Large bundle imports (importing entire library when only one function needed)
- Missing code splitting for heavy routes/components
- Images without lazy loading or size optimization
- Blocking operations on the main thread

**Network & I/O:**
- Sequential API calls that could be parallelized
- Missing request timeouts on external service calls
- Large payloads without compression or pagination
- Missing caching headers for static/rarely-changing resources

**Memory:**
- Event listeners added but never removed (memory leaks)
- Growing arrays/maps without bounds or cleanup
- Large file processing without streaming
- Closures capturing large scopes unnecessarily

### 6. Analyze — Reliability & Error Handling

Production code must handle failure gracefully. The question isn't "does it work?" but "what happens when things go wrong?"

**Error handling quality:**
- Swallowed errors (empty catch blocks, `.catch(() => {})`)
- Generic catch blocks that hide the actual error type
- Missing error messages that would help debugging
- Errors caught but not logged or reported
- Cleanup logic missing in error paths (connections, file handles, locks)

**Graceful degradation:**
- What happens when an external service is down? Does the whole feature break?
- Missing fallback behavior for optional dependencies
- Timeout handling on external calls (HTTP, database, third-party APIs)
- Missing retry logic with backoff for transient failures

**Data validation at boundaries:**
- API inputs not validated before processing
- Missing type/schema validation on external data (webhooks, API responses)
- File uploads without type/size validation
- Trusting client-side validation without server-side checks

**State management:**
- Inconsistent error states (loading indicator stays forever on error)
- Missing loading/error/empty states in UI
- Optimistic updates without rollback on failure

### 7. Analyze — Design & Best Practices

Think about the next engineer who reads this code. Is the intent clear? Does the design scale with the codebase?

**Separation of concerns:**
- Business logic mixed with presentation/routing/data access
- Components doing too many things (should be split)
- Side effects in pure functions or constructors

**API design (if endpoints changed):**
- Breaking changes to existing API contracts without versioning
- Inconsistent response format across endpoints
- Missing or inconsistent HTTP status codes
- Unclear or missing error response schema

**Code clarity:**
- Naming — are names descriptive and consistent with project conventions?
- Dead code — commented-out code, unused imports, unreachable branches
- DRY violations — copy-pasted logic that should be extracted
- Function length — functions over ~50 lines that should be split
- Deeply nested logic (>3 levels) that should be flattened with early returns

**Dependency management:**
- New dependencies added — are they necessary? Well-maintained? License-compatible?
- Are there lighter alternatives for heavy imports?
- Lock file updated when dependencies change?

### 8. Analyze — Framework-Specific

Based on what the project uses:

**React/Next.js:**
- Missing keys in list rendering (or using array index as key for dynamic lists)
- `useEffect` dependency arrays — missing deps cause stale data, unnecessary deps cause infinite loops
- Client vs server component boundaries (Next.js App Router) — using hooks in server components, importing server-only code in client
- State updates on unmounted components
- Missing `Suspense` boundaries for async components
- Missing `ErrorBoundary` for component-level error isolation

**Python:**
- Missing type hints on public functions and API endpoints
- Mutable default arguments (`def f(items=[])`)
- Bare `except:` clauses (should catch specific exceptions)
- Async context managers not used (`async with` for DB connections)
- Missing `__all__` exports in public modules

**Go:**
- Unchecked error returns (especially on `Close()`, `Write()`, `Flush()`)
- Deferred function errors ignored (`defer f.Close()` without checking error)
- Goroutine leaks (goroutines started without cancellation context)
- Missing mutex for concurrent access to shared state
- Context not propagated through call chain

**Node.js/Express:**
- Missing error-handling middleware
- Unhandled promise rejections in route handlers
- Missing `helmet` or equivalent security headers
- `req.body` used without validation middleware

**General:**
- Environment-specific code without feature flags or env checks
- Missing input validation at system boundaries
- Inconsistent error response format across endpoints
- Magic numbers/strings that should be named constants

### 9. Analyze — Testing (if tests are included in the diff)

If the diff includes test files, review them with the same rigor as production code.

- **Coverage gaps:** Are all new code paths exercised? Happy path AND error paths?
- **Edge cases:** Do tests cover boundary conditions, empty inputs, invalid data?
- **Test isolation:** Do tests depend on external state, order, or other tests?
- **Assertion quality:** Are assertions specific enough to catch regressions? (not just `toBeTruthy`)
- **Test naming:** Do test names describe the behavior being verified?
- **Mocking:** Are mocks minimal and realistic? Over-mocking hides real bugs.
- **Flakiness risks:** Timing-dependent assertions, network calls, random data without seeding

### 10. Generate Review Report

Format findings with severity levels and review dimensions:

```markdown
## Code Review: [branch-name]

**Changes:** X files changed, +Y/-Z lines
**Commits:** N commits
**Review dimensions:** Correctness, Security, Performance, Reliability, Design, Best Practices, Testing

### Critical (must fix before merge)
- **[Correctness]** [FILE:LINE] Description of critical issue
  **Why:** Explanation of impact — what breaks, who is affected, how likely
- **[Security]** [FILE:LINE] Description
  **Why:** ...

### Warning (should fix)
- **[Performance]** [FILE:LINE] Description
  **Why:** Explanation of risk — what degrades, under what conditions
- **[Reliability]** [FILE:LINE] Description
  **Why:** ...

### Nitpick (consider for next time)
- **[Design]** [FILE:LINE] Description
  **Why:** Explanation of improvement — readability, maintainability, conventions

### What Looks Good
- Brief acknowledgment of well-done aspects (1-3 bullet points max)
```

**Severity guidelines:**
- **Critical:** Will cause bugs in production, security vulnerability, data loss, or crash. Must fix.
- **Warning:** Likely to cause problems at scale, makes future bugs likely, or degrades reliability/performance meaningfully. Should fix.
- **Nitpick:** Style, conventions, minor improvements. Won't break anything but worth noting.

**Rules:**
- Maximum 20 items total (prioritize by severity, then by category)
- Every item must tag its review dimension: `[Correctness]`, `[Security]`, `[Performance]`, `[Reliability]`, `[Design]`, `[Best Practices]`, `[Testing]`
- Every item must reference a specific file and line
- Every item must explain **why** it matters — the impact, not just the symptom
- Include a brief "What Looks Good" section (2-3 items) — acknowledge strong patterns so they're reinforced. This isn't cheerleading — it's calibrating signal.
- If you genuinely find nothing wrong after all 7 dimensions, say so — but that's rare

### 11. Next Steps

After presenting the review:

If there are **Critical** or **Warning** items:
> "Review found issues that should be addressed. Fix them with `/sk:debug`, commit with `/sk:smart-commit`, then re-run `/sk:review` to verify."

If there are only **Nitpick** items (no Critical/Warning):
> "Review complete — no critical issues found, but there are some nitpicks. Would you like to fix them now, or proceed to `/sk:finish-feature`?"

If the user wants to fix nitpicks, loop back to `/sk:debug` + `/sk:smart-commit` → `/sk:review`.

If the review is **completely clean**:
> "Review complete — no issues found. Run `/sk:finish-feature` to finalize the branch and create a PR."

---

## Model Routing

Read `.shipkit/sk:config.json` from the project root if it exists.

- If `model_overrides["sk:review"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
