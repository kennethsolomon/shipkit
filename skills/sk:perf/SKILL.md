---
name: sk:perf
description: Performance audit. Use before /sk:review to catch performance issues: bundle size, N+1 queries, slow DB queries, Core Web Vitals, memory leaks, caching opportunities. Auto-detects stack. Fixes critical/high in-scope findings and auto-commits. Logs pre-existing issues to tech-debt.
license: Complete terms in LICENSE.txt
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
---

## Purpose

Audit the implementation for performance issues before `/sk:review`. Produces a findings report, fixes in-scope critical/high findings, auto-commits. Pre-existing findings (outside branch diff) are logged to `tasks/tech-debt.md`.

## Hard Rules

- Fix all critical and high in-scope findings (files in `git diff main..HEAD --name-only`). Re-run until critical/high = 0. ONE squash commit: `fix(perf): resolve performance findings`.
- Medium/low in-scope: fix if straightforward, otherwise log to `tasks/tech-debt.md`.
- Pre-existing findings (outside branch diff): log only — do NOT fix inline:
  ```
  ### [YYYY-MM-DD] Found during: sk:perf
  File: path/to/file.ext:line
  Issue: description of the performance issue
  Severity: critical | high | medium | low
  ```
- Squash gate commits — one commit per pass, not per fix.
- Every finding must cite a specific file:line, estimated impact (high/medium/low), and a recommendation.
- Auto-detect stack — only run checks relevant to what's present.

## Before You Start

1. Detect stack: read `CLAUDE.md`, check for `package.json`, `composer.json`, `go.mod`, `requirements.txt`, `Cargo.toml`.
2. Determine scope: `git diff main..HEAD --name-only`.
3. If `tasks/perf-findings.md` exists, read it — check if prior findings were addressed.
4. If `tasks/lessons.md` exists, read it — apply performance-related lessons.

## Stack Detection

| Indicator | Checks to run |
|-----------|--------------|
| `package.json` with React/Next/Vue | Frontend bundle, render performance, Core Web Vitals |
| `package.json` with Express/Node | Node.js backend performance |
| `composer.json` (Laravel/PHP) | PHP/Laravel backend performance |
| `go.mod` | Go performance checks |
| `requirements.txt` / `pyproject.toml` | Python performance checks |
| Any ORM detected | Database query performance |

## Audit Checklist

### Frontend Performance

**Bundle & Loading**
- Unused imports or dependencies included in the bundle
- Large dependencies that could be code-split or lazy-loaded
- Images without lazy loading (`loading="lazy"`) or without `width`/`height` attributes
- Fonts without `font-display: swap` or preloaded without need
- No tree-shaking unfriendly imports (`import * from` large libraries)

**Render Performance**
- React: missing `memo`, `useMemo`, `useCallback` on expensive operations in hot render paths
- React: unnecessary re-renders from unstable object/array/function references passed as props
- React: large lists without virtualization (`react-window` or similar)
- Synchronous operations blocking the main thread (large loops, heavy computation in render)
- Missing Suspense boundaries for code-split routes

**Core Web Vitals**
- LCP (Largest Contentful Paint): hero image/text not prioritized, no preload hint
- CLS (Cumulative Layout Shift): images/embeds without reserved dimensions, dynamic content inserted above existing content
- INP (Interaction to Next Paint): heavy click/input event handlers, no debouncing on frequent events

### Backend Performance

**Database (all ORMs)**
- N+1 query patterns: loops that query inside a loop without eager loading
- Missing indexes on foreign keys, frequently filtered columns, or join columns
- `SELECT *` where only specific columns are needed
- Unindexed `WHERE` clauses on large tables
- Missing pagination on endpoints that return collections
- Queries inside loops that could be batched

**Laravel-Specific**
- Missing `with()` eager loading on Eloquent relationships
- `all()` on large tables without `limit()`/`paginate()`
- Expensive operations not queued (emails, notifications, file processing)
- Missing cache on expensive repeated queries
- Missing database indexes defined in migrations

**Node.js-Specific**
- Blocking `fs.readFileSync` / `execSync` in request handlers
- Missing connection pooling on database clients
- Unbounded promise arrays (`Promise.all` on thousands of items)
- Memory leaks from event listeners not removed

**Go-Specific**
- Missing goroutine cleanup (goroutine leaks)
- Repeated allocations in hot paths that could use `sync.Pool`
- Blocking operations in goroutines without context cancellation

**General Backend**
- Missing HTTP response caching headers (`Cache-Control`, `ETag`) on static/infrequently-changing resources
- Missing compression (gzip/brotli) on text responses
- API responses without pagination on collection endpoints
- Expensive computations not cached (Redis, in-memory, etc.)
- External API calls in the critical path without timeout or circuit breaker

### Memory & Reliability

- Memory leaks: global caches/maps that grow without bounds
- Missing cleanup in component unmount / service shutdown
- Large objects held in memory longer than needed
- Recursive functions without memoization on repeated inputs

## Severity Levels

- **Critical**: Will cause production degradation at scale (N+1 on large table, unbounded memory growth)
- **High**: Measurable user-facing impact (LCP > 2.5s, missing pagination, blocking I/O in handler)
- **Medium**: Noticeable but not breaking (unnecessary re-renders, missing cache on moderate traffic)
- **Low**: Best practice / minor optimization (missing `loading="lazy"`, minor bundle bloat)

## Generate Report

Write findings to `tasks/perf-findings.md` (never overwrite — append with date header):

```markdown
# Performance Audit — YYYY-MM-DD

**Scope:** Changed files on branch `<branch-name>`
**Stack:** [detected stack]
**Files audited:** N

## Critical

- [ ] **[FILE:LINE]** Description
  **Impact:** What happens at scale
  **Recommendation:** How to fix
- [x] **[FILE:LINE]** Description *(resolved)*

## High

- [ ] **[FILE:LINE]** Description
  **Impact:** ...
  **Recommendation:** ...

## Medium

- [ ] **[FILE:LINE]** Description
  **Recommendation:** ...

## Low

- [ ] **[FILE:LINE]** Description
  **Recommendation:** ...

## Passed Checks

- [Categories with no findings]

## Summary

| Severity | Open | Resolved this run |
|----------|------|-------------------|
| Critical | N    | N                 |
| High     | N    | N                 |
| Medium   | N    | N                 |
| Low      | N    | N                 |
| **Total** | **N** | **N**            |
```

Write the report first, then apply fixes.

## Fix Critical/High Findings via Agent

Invoke the **`performance-optimizer`** agent:

```
Task: "Read tasks/perf-findings.md. Fix all Critical and High in-scope findings
(files in git diff main..HEAD). Run tests before and after each fix — tests must
pass before AND after. Commit: fix(perf): resolve performance findings"
```

Agent works in worktree isolation. After completion, merge its worktree branch and verify fixes in `tasks/perf-findings.md`.

## Fix & Retest Protocol

| Fix type | Action |
|----------|--------|
| Config/infrastructure (cache headers, compression, CDN config, pool size) | Commit → re-run `/sk:perf`. No test update needed. |
| Logic change (N+1 fix, algorithm refactor, pagination, data structure) | 1) Update/add failing tests 2) `/sk:test` at 100% 3) Commit tests+fix together 4) Re-run `/sk:perf` |

Logic changes include: N+1 fix (query count/data shape), algorithm change (output correctness), pagination (result set size). Tests must verify the optimized path produces correct results.

## When Done

> "Performance audit complete. Findings saved to `tasks/perf-findings.md`.
> - **Critical:** N | **High:** N | **Medium:** N | **Low:** N
>
> All critical/high in-scope findings have been fixed and committed. Pre-existing issues logged to `tasks/tech-debt.md`. Run `/sk:review` to proceed."

If no critical/high findings:
> "No critical or high performance issues found. N medium/low findings noted in `tasks/perf-findings.md`. Run `/sk:review` to proceed."

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:perf"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
