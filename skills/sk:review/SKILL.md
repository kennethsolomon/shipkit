---
name: sk:review
description: "Rigorous self-review of all branch changes across 8 dimensions: correctness, security, performance, reliability, design quality, best practices, documentation, and testing. Report-only — no PR creation (that's /sk:finish-feature's job). Use when code is complete and ready for review before merging."
model: sonnet
---

# Self-Review

## Overview

Perform a rigorous, multi-dimensional review of all changes on the current branch. Quality bar: senior engineer at a top-tier tech company — thorough, specific, and honest.

**You are the reviewer, not the cheerleader.** Find problems, not praise. If you find nothing wrong, look harder. Think about what could go wrong in production at scale, under adversarial conditions, and over time.

This is a **report-only** step. Critical or Warning issues loop back to `/sk:debug` → `/sk:smart-commit` → `/sk:review` until clean. Then run `/sk:finish-feature`.

**exhaustiveness commitment:** Every dimension (Steps 3–10) must be fully analyzed before generating the report. Skipping a dimension is a failure. If nothing is found in a dimension, state `"No issues found"` explicitly.

## Allowed Tools

Bash, Read, Glob, Grep, Skill

**Step 0 only:** the `simplify` skill carries its own Write/Edit permissions. All other steps are read-only — no direct Write or Edit calls.

## Steps

### 0. Run Simplify First

Invoke the built-in `simplify` skill on the changed files:

> "Review the changed files on this branch for reuse, quality, and efficiency. Fix any issues found."

Use `git diff main..HEAD --name-only` to identify changed files, then run simplify on them.

If simplify makes changes:
1. Verify the changes are correct
2. Auto-commit with `fix(review): simplify pre-pass` — do not ask the user
3. Note in the review report: "Simplify pre-pass: X files updated"

### 1. Read Project Context

```
CLAUDE.md                  — Coding standards, conventions, known patterns
tasks/lessons.md           — Recurrent bug patterns (if exists)
tasks/security-findings.md — Prior security audit results (if exists)
```

If `tasks/lessons.md` exists, treat each active lesson's **Bug** field as an additional targeted check across all dimensions.

If `tasks/security-findings.md` exists, verify the current diff doesn't reintroduce previously flagged unresolved Critical/High vulnerabilities.

### 2. Collect Changes + Blast Radius

Build a **blast radius** — the minimal set of files that could be affected by the changes.

**2a — Baseline git info:**

```bash
BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
CHANGED_FILES=$(git diff $BASE..HEAD --name-only)
git diff $BASE..HEAD --stat
git log $BASE..HEAD --oneline
git diff $BASE..HEAD
git status --short
```

If uncommitted changes exist, warn:
> **Warning:** You have uncommitted changes. These will NOT be included in the review. Commit or stash them first.

**2b — Extract changed symbols:**

Use git hunk headers as the primary extraction method:

```bash
# Phase 1: Enclosing scope names from hunk headers
git diff $BASE..HEAD -U0 | grep '^@@' | sed 's/.*@@\s*//' | \
  grep -oE '[A-Za-z_][A-Za-z0-9_]*\s*\(' | sed 's/\s*(//' | sort -u
```

Supplement with new/modified definitions from added lines:

```bash
# Phase 2: Definitions from added lines
# JS/TS: function foo(, class Foo, interface Foo
# Python: def foo(, class Foo
# Go: func foo(, func (r *T) foo(
# PHP: function foo(, class Foo
# Rust: fn foo(, struct Foo, impl Foo, trait Foo
git diff $BASE..HEAD | grep '^+' | grep -v '^+++' | \
  grep -oE '(function|class|interface|def|fn|func|struct|trait|impl)\s+[A-Za-z_][A-Za-z0-9_]+' | \
  awk '{print $2}' | sort -u
```

Combine both phases. Filter symbols shorter than 3 characters.

Classify each symbol:
- **Modified/removed** — existed before the branch, changed or deleted. **Run blast radius.**
- **New** — added in this branch, no prior callers. **Skip blast radius.**

```bash
# If symbol exists in base branch, it's modified/removed → needs blast radius
git show $BASE:$FILE 2>/dev/null | grep -q "\b$SYMBOL\b"
```

**2c — Find blast radius (modified/removed symbols only):**

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

comm -23 /tmp/dependents.txt <(echo "$CHANGED_FILES" | sort) > /tmp/blast_radius.txt
```

**Noise guard:** If a symbol produces >100 matches, note: "unable to determine blast radius for `symbol` — manual verification recommended."

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
1. **Changed files in full** — not just the diff. For files >500 lines, read the changed function + 30 lines of surrounding context.
2. **The diff** — for precise change tracking (already collected above).
3. **Blast-radius dependent files** — use `rg -B5 -A10 "\bsymbol\b" dependent_file` to get call sites with context, not the entire file.
4. **Test files** for changed symbols — verify existing tests still cover the changed behavior.

Do not read unchanged files outside the blast radius. Carry the blast-radius mapping (symbol → dependents) forward into Steps 3–10.

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 3. Analyze — Correctness & Bugs

The most important dimension. A bug that ships is worse than ugly code that works.

**Blast-radius check (mandatory):** For every modified/removed symbol, verify its dependents (from Step 2c):
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

Load `references/security-checklist.md` and apply its grep patterns against the **diff and blast-radius files** only. Flag only patterns **newly introduced** in the diff.

**Blast-radius check:** If a validation or auth function was modified, check all its callers — a weakened check affects every endpoint that depends on it.

**Injection (OWASP A03):**
- SQL, NoSQL, OS command, LDAP, template injection
- String concatenation/interpolation in queries instead of parameterized queries
- `eval()`, `exec()`, `Function()` with any dynamic input

**Cross-Site Scripting (OWASP A03):**
- `dangerouslySetInnerHTML`, `innerHTML`, `v-html` without sanitization
- URL parameters reflected without encoding
- User content in `href`, `src`, or event handler attributes

**Authentication & Authorization (OWASP A01, A07):**
- Hardcoded secrets, API keys, tokens in source code
- Missing auth checks on endpoints (especially admin, destructive operations)
- IDOR — user-controlled IDs accessing other users' resources without ownership verification
- Weak session management, missing token rotation

**Data exposure (OWASP A02):**
- Credentials, PII, or tokens in logs
- Stack traces or internal errors leaked to clients
- Sensitive data in client-side bundles
- Missing encryption for sensitive data at rest

**Configuration (OWASP A05):**
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Overly permissive CORS (`origin: '*'`)
- Debug mode enabled in production paths
- Missing rate limiting on auth/sensitive endpoints

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 5. Analyze — Performance

Think about what happens at 10x, 100x current scale.

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

The question isn't "does it work?" but "what happens when things go wrong?"

**Blast-radius check:** If error handling changed (e.g., function now throws instead of returning null, or error type changed), check all callers from Step 2c — they may not have matching try/catch or null checks.

**Error handling quality:**
- Swallowed errors (empty catch blocks, `.catch(() => {})`)
- Generic catch blocks that hide the actual error type
- Missing error messages that would help debugging
- Errors caught but not logged or reported
- Cleanup logic missing in error paths (connections, file handles, locks)

**Graceful degradation:**
- What happens when an external service is down?
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

Think about the next engineer who reads this code.

**Separation of concerns:**
- Business logic mixed with presentation/routing/data access
- Components doing too many things (should be split)
- Side effects in pure functions or constructors

**API design (if endpoints or function signatures changed):**
- Breaking changes to existing API contracts without versioning
- **Blast-radius check:** If a function signature changed, every dependent file that calls the old signature will break
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
- New dependencies — necessary? Well-maintained? License-compatible?
- Are there lighter alternatives for heavy imports?
- Lock file updated when dependencies change?

> Before analyzing this dimension, use a `<think>` block to: (1) identify which changed files and blast-radius dependents are most relevant here, and (2) list 3–5 specific things to look for given the nature of the change. This reasoning is not shown to the user — it improves analysis depth.

### 8. Analyze — Framework-Specific

**React/Next.js:**
- Missing keys in list rendering (or using array index as key for dynamic lists)
- `useEffect` dependency arrays — missing deps cause stale data, unnecessary deps cause infinite loops
- Client vs server component boundaries (Next.js App Router) — hooks in server components, server-only code in client
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

### 9. Analyze — Documentation (if docs are included in the diff)

If the diff includes `.md`, `.mdx`, README, or files with significant docstring/JSDoc changes, delegate to the `doc-reviewer` agent:

> "Review the documentation changes on this branch. Cross-reference every claim against the actual source code. Check for accuracy, completeness, staleness, and clarity."

Merge its findings into the final report under a `[Documentation]` dimension tag.

If no documentation files were changed, skip this section and note: `"Documentation: No doc files in diff — skipped."`

### 10. Analyze — Testing (if tests are included in the diff)

If the diff includes test files, review them with the same rigor as production code.

- **Coverage gaps:** All new code paths exercised? Happy path AND error paths?
- **Edge cases:** Boundary conditions, empty inputs, invalid data?
- **Test isolation:** Do tests depend on external state, order, or other tests?
- **Assertion quality:** Specific enough to catch regressions? (not just `toBeTruthy`)
- **Test naming:** Do test names describe the behavior being verified?
- **Mocking:** Minimal and realistic? Over-mocking hides real bugs.
- **Flakiness risks:** Timing-dependent assertions, network calls, random data without seeding

### 11. Generate Review Report

```markdown
## Code Review: [branch-name]

**Changes:** X files changed, +Y/-Z lines
**Commits:** N commits
**Blast radius:** X changed files + Y dependents = Z total review scope
**Review dimensions:** Correctness, Security, Performance, Reliability, Design, Best Practices, Documentation, Testing, Blast Radius

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
- **Nitpick:** Style, conventions, minor improvements. Won't break anything.

**Rules:**
- Maximum 20 items total (prioritize by severity, then by category)
- Every item must tag its review dimension: `[Correctness]`, `[Security]`, `[Performance]`, `[Reliability]`, `[Design]`, `[Best Practices]`, `[Testing]`, `[Documentation]`, `[Blast Radius]`
- Use `[Blast Radius]` for issues found in dependent files — callers broken by changed signatures, importers affected by removed exports, tests that no longer cover the changed behavior
- Every item must reference a specific file, line, and symbol using `[FILE:LINE:SYMBOL]` format
- Every item must explain **why** it matters — the impact, not just the symptom
- Include "What Looks Good" (2-3 items) — acknowledge strong patterns to reinforce them

### 12. Fix and Re-run

Fix **all** findings regardless of severity. Do not ask whether to fix nitpicks.

**For each finding:**
- Issue in a file **within** the current branch diff → fix it inline, include in auto-commit
- Issue in a file **outside** the current branch diff (pre-existing, found via blast-radius) → log to `tasks/tech-debt.md`, do NOT fix inline:
  ```
  ### [YYYY-MM-DD] Found during: sk:review
  File: path/to/file.ext:line
  Issue: description of the problem
  Severity: critical | high | medium | low
  ```

After all in-scope fixes: make ONE squash commit `fix(review): address review findings`. Re-run `/sk:review` from scratch. Loop until 0 findings.

When clean:
> "Review complete — 0 findings. Run `/sk:finish-feature` to finalize the branch and create a PR."

### Fix & Retest Protocol

Classify each fix before committing:

**a. Style/naming/comment change** (rename variable, add doc comment, reorder imports, extract constant) → commit and re-run `/sk:review`. No test update needed.

**b. Logic change** (fix incorrect condition, add missing null check, change data flow, refactor algorithm, fix async bug):
1. Update or add failing unit tests for the corrected behavior
2. Re-run `/sk:test` — must pass at 100% coverage
3. Auto-commit tests + fix together with `fix(review): [description]`
4. Re-run `/sk:review` from scratch

**Why:** Fixing a logic bug without updating tests leaves the test suite asserting on the old (wrong) behavior.

---

## Intensity

Read `.shipkit/config.json` for intensity settings. Resolution: `intensity_overrides["sk:review"]` → global `intensity` → `deep` (default for review).

Review defaults to **deep** — security and correctness findings need full detail. Do not compress review output even if global intensity is `lite`.

| Level | Review behavior |
|-------|----------------|
| **lite** | Top 5 critical/warning items only. No nitpicks. Compact report. |
| **full** | Standard review — all items up to 20, full explanations. |
| **deep** | Exhaustive — all dimensions fully analyzed, blast-radius explored, edge cases enumerated. Default for review. |

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
