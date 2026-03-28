---
name: sk:review
description: "Rigorous self-review of all branch changes across 7 dimensions: correctness, security, performance, reliability, design quality, best practices, and testing. Report-only — no PR creation (that's /sk:finish-feature's job). Use when code is complete and ready for review before merging."
model: sonnet
---

# Self-Review

## Overview

Perform a rigorous, multi-dimensional review of all changes on the current branch. This review aims for the quality bar of a senior engineer at a top-tier tech company — thorough, specific, and honest.

**You are the reviewer, not the cheerleader.** Your job is to find problems, not to praise the code. If you find nothing wrong, look harder. Real code almost always has something worth flagging. Think about what could go wrong in production at scale, under adversarial conditions, and over time as the codebase evolves.

This is a **report-only** step. If Critical or Warning issues are found, the user loops back to `/sk:debug` → `/sk:smart-commit` → `/sk:review` until the branch is clean. Once clean, the user runs `/sk:finish-feature` to finalize and create the PR.

**exhaustiveness commitment:** Partial completion is unacceptable. Every dimension (Steps 3–9) must be fully analyzed before generating the report. If you find nothing wrong in a dimension, state it explicitly (`"No issues found"`) — do not skip or leave it blank. Skipping a dimension is a failure.

## Allowed Tools

Bash, Read, Glob, Grep, Skill

**Step 0 only:** the `simplify` skill is invoked via the Skill tool, which carries its own Write/Edit permissions. All other steps are read-only — no direct Write or Edit calls. If issues are found in the main review, the user decides what to fix.

## Steps

You MUST complete these steps in order:

### 0. Run Simplify First

Before reviewing, invoke the built-in `simplify` skill on the changed files to catch reuse, quality, and efficiency issues automatically:

> "Review the changed files on this branch for reuse, quality, and efficiency. Fix any issues found."

Use `git diff main..HEAD --name-only` to identify the changed files, then run simplify on them.

If simplify makes any changes:
1. Verify the changes are correct
2. Auto-commit them with message `fix(review): simplify pre-pass` before continuing the review. Do not ask the user.
3. Note in the review report: "Simplify pre-pass: X files updated"

If simplify makes no changes, proceed directly to step 1.

**Note:** Simplify runs automatically as part of `/sk:review` — users do not need to run it separately.

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

### 2. Collect Changes + Blast Radius

Instead of reading the entire codebase or only the diff, build a **blast radius** — the minimal set of files that could be affected by the changes. This produces focused, high-signal context that leads to better review quality.

**2a — Baseline git info:**

```bash
# Determine base branch
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

# Changed files and stats
CHANGED_FILES=$(git diff $BASE..HEAD --name-only)
git diff $BASE..HEAD --stat
git log $BASE..HEAD --oneline

# Full diff for reference
git diff $BASE..HEAD

# Check for uncommitted changes
git status --short
```

If there are uncommitted changes, warn:
> **Warning:** You have uncommitted changes. These will NOT be included in the review. Commit or stash them first.

**2b — Extract changed symbols:**

Use **git hunk headers** as the primary extraction method. Git already parses the enclosing function/class name into every `@@` header — this is more reliable than regex or AST tools:

```bash
# Phase 1: Enclosing scope names from hunk headers (free from git, no parsing needed)
git diff $BASE..HEAD -U0 | grep '^@@' | sed 's/.*@@\s*//' | \
  grep -oE '[A-Za-z_][A-Za-z0-9_]*\s*\(' | sed 's/\s*(//' | sort -u
```

Then supplement with **new/modified definitions** from added lines using language-specific patterns. Only match definition keywords — not `const`, `export`, `type`, or other high-noise terms:

```bash
# Phase 2: Definitions from added lines (supplement, not replace)
# JS/TS:   function foo(, class Foo, interface Foo
# Python:  def foo(, class Foo
# Go:      func foo(, func (r *T) foo(
# PHP:     function foo(, class Foo
# Rust:    fn foo(, struct Foo, impl Foo, trait Foo
git diff $BASE..HEAD | grep '^+' | grep -v '^+++' | \
  grep -oE '(function|class|interface|def|fn|func|struct|trait|impl)\s+[A-Za-z_][A-Za-z0-9_]+' | \
  awk '{print $2}' | sort -u
```

Combine both phases. Filter out symbols shorter than 3 characters (too generic for blast-radius search).

Classify each symbol:
- **Modified/removed** — existed before the branch, changed or deleted now. These can break callers. **Run blast radius on these.**
- **New** — added in this branch, no prior callers exist. **Skip blast radius** (nothing to break).

To classify, check if the symbol appears in the base branch:
```bash
# If symbol exists in base branch files, it's modified/removed → needs blast radius
git show $BASE:$FILE 2>/dev/null | grep -q "\b$SYMBOL\b"
```

**2c — Find blast radius (modified/removed symbols only):**

For each modified/removed symbol, use **import-chain narrowing** to find dependents with minimal false positives:

```bash
# Step 1: Find files that import the module containing the changed symbol
CHANGED_MODULE_PATHS=$(echo "$CHANGED_FILES" | sed 's/\.[^.]*$//' | sed 's/\/index$//')
for module_path in $CHANGED_MODULE_PATHS; do
  rg -l "(import|require|from|use)\s.*$(basename $module_path)" \
    --glob '!node_modules/**' --glob '!vendor/**' --glob '!dist/**' \
    --glob '!build/**' --glob '!*.lock' --glob '!*.md' \
    2>/dev/null
done | sort -u > /tmp/importers.txt

# Step 2: Within importers, find which ones reference the specific changed symbols
for symbol in $MODIFIED_SYMBOLS; do
  rg -wl "$symbol" $(cat /tmp/importers.txt) 2>/dev/null
done | sort -u > /tmp/dependents.txt

# Remove files already in the changed set
comm -23 /tmp/dependents.txt <(echo "$CHANGED_FILES" | sort) > /tmp/blast_radius.txt
```

**Noise guard:** If a symbol produces >100 matches, it's too generic for grep-based analysis. Note it in the review as "unable to determine blast radius for `symbol` — manual verification recommended."

Log the blast radius before reading:
```
Blast Radius Summary
──────────────────────────────────
Changed files:           X
Blast-radius dependents: Y  (files importing changed symbols)
Total review scope:      X+Y files
Symbols analyzed:        N modified, M new (skipped)

Symbol → Dependents:
  processOrder  → src/checkout/cart.ts, src/api/orders.ts
  validateInput → src/middleware/auth.ts
──────────────────────────────────
```

**2d — Read context (focused, not exhaustive):**

Read in this priority order:
1. **Changed files in full** — not just the diff. The full file provides surrounding context (imports, related functions, class-level state) needed to judge whether the change is correct. For files >500 lines, read the changed function + 30 lines of surrounding context instead.
2. **The diff** — for precise change tracking (already collected above).
3. **Blast-radius dependent files** — read only the call sites that reference changed symbols. Use `rg -B5 -A10 "\bsymbol\b" dependent_file` to get the call site with surrounding context, not the entire file.
4. **Test files** for changed symbols — verify existing tests still cover the changed behavior.

Do **not** read unchanged files outside the blast radius.

Carry the blast-radius mapping (symbol → dependents) forward into Steps 3-9. When analyzing a changed function, always cross-reference its dependents.

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 3. Analyze — Correctness & Bugs

The most important dimension. A bug that ships is worse than ugly code that works.

**Blast-radius check (mandatory):** For every modified/removed symbol, verify its dependents (from Step 2c) are still compatible:
- Do callers pass arguments the changed function still accepts?
- Do callers depend on return values whose shape/type changed?
- Do callers rely on side effects the changed code no longer produces?

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

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 4. Analyze — Security

Load `references/security-checklist.md` and apply its grep patterns against the **diff and blast-radius files** (not the entire codebase). Only flag patterns **newly introduced** in the diff — pre-existing issues are out of scope unless they interact with the changed code.

**Blast-radius check:** If a validation or auth function was modified, check all its callers (from Step 2c) — a weakened check affects every endpoint that depends on it.

Check for:

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

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

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

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 6. Analyze — Reliability & Error Handling

Production code must handle failure gracefully. The question isn't "does it work?" but "what happens when things go wrong?"

**Blast-radius check:** If error handling changed (e.g., function now throws instead of returning null, or error type changed), check all callers from Step 2c — they may not have matching try/catch or null checks.

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

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 7. Analyze — Design & Best Practices

Think about the next engineer who reads this code. Is the intent clear? Does the design scale with the codebase?

**Separation of concerns:**
- Business logic mixed with presentation/routing/data access
- Components doing too many things (should be split)
- Side effects in pure functions or constructors

**API design (if endpoints or function signatures changed):**
- Breaking changes to existing API contracts without versioning
- **Blast-radius check:** If a function signature changed, the blast radius from Step 2c is the definitive answer to whether it's a breaking change — every dependent file that calls the old signature will break
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

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

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

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

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
**Blast radius:** X changed files + Y dependents = Z total review scope
**Review dimensions:** Correctness, Security, Performance, Reliability, Design, Best Practices, Testing, Blast Radius

### Critical (must fix before merge)
- **[Correctness]** [src/checkout/cart.ts:42:processOrder:function] Description of critical issue
  **Why:** Explanation of impact — what breaks, who is affected, how likely
- **[Security]** [FILE:LINE:SYMBOL] Description
  **Why:** ...

### Warning (should fix)
- **[Performance]** [FILE:LINE:SYMBOL] Description
  **Why:** Explanation of risk — what degrades, under what conditions
- **[Reliability]** [FILE:LINE:SYMBOL] Description
  **Why:** ...

### Nitpick (consider for next time)
- **[Design]** [FILE:LINE:SYMBOL] Description
  **Why:** Explanation of improvement — readability, maintainability, conventions

### What Looks Good
- Brief acknowledgment of well-done aspects (1-3 bullet points max)
```

**Symbol format:** `file:line:name:type` — use `:symbol` as placeholder in examples. Type is one of: `function`, `method`, `class`, `variable`, `hook`, `component`

**Severity guidelines:**
- **Critical:** Will cause bugs in production, security vulnerability, data loss, or crash. Must fix.
- **Warning:** Likely to cause problems at scale, makes future bugs likely, or degrades reliability/performance meaningfully. Should fix.
- **Nitpick:** Style, conventions, minor improvements. Won't break anything but worth noting.

**Rules:**
- Maximum 20 items total (prioritize by severity, then by category)
- Every item must tag its review dimension: `[Correctness]`, `[Security]`, `[Performance]`, `[Reliability]`, `[Design]`, `[Best Practices]`, `[Testing]`, `[Blast Radius]`
- Use `[Blast Radius]` for issues found in dependent files — callers broken by changed signatures, importers affected by removed exports, tests that no longer cover the changed behavior
- Every item must reference a specific file, line, and symbol using `[FILE:LINE:SYMBOL]` format
- Every item must explain **why** it matters — the impact, not just the symptom
- Include a brief "What Looks Good" section (2-3 items) — acknowledge strong patterns so they're reinforced. This isn't cheerleading — it's calibrating signal.
- If you genuinely find nothing wrong after all 7 dimensions, say so — but that's rare

### 11. Fix and Re-run

After presenting the review report, fix **all** findings regardless of severity (Critical, Warning, and Nitpick). Do not ask the user whether to fix nitpicks — fix everything.

**For each finding:**
- If the issue is in a file **within** the current branch diff (`git diff $BASE..HEAD --name-only`): fix it inline, include in the auto-commit
- If the issue is in a file **outside** the current branch diff (pre-existing issue found via blast-radius): log it to `tasks/tech-debt.md` — do NOT fix it inline:
  ```
  ### [YYYY-MM-DD] Found during: sk:review
  File: path/to/file.ext:line
  Issue: description of the problem
  Severity: critical | high | medium | low
  ```

After all in-scope fixes are applied: make ONE squash commit with `fix(review): address review findings`. Do not ask the user. Re-run `/sk:review` from scratch.

Loop until the review is completely clean (0 findings across all severities for in-scope code).

When clean:
> "Review complete — 0 findings. Run `/sk:finish-feature` to finalize the branch and create a PR."

> Squash gate commits — collect all fixes for the pass, then one commit. Do not commit after each individual fix.

### Fix & Retest Protocol

When applying a fix from this review, classify it before committing:

**a. Style/naming/comment change** (rename variable, add doc comment, reorder imports, extract constant) → commit and re-run `/sk:review`. No test update needed.

**b. Logic change** (fix incorrect condition, add missing null check, change data flow, refactor algorithm, fix async bug) → trigger protocol:
1. Update or add failing unit tests for the corrected behavior
2. Re-run `/sk:test` — must pass at 100% coverage
3. Auto-commit tests + fix together with `fix(review): [description]`.
4. Re-run `/sk:review` from scratch

**Why:** Review catches logic bugs. Fixing a logic bug without updating tests leaves the test suite asserting on the old (wrong) behavior.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:review"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
