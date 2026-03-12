# Claude Skills: Complete Feature Set (March 2026)

A comprehensive overview of all features in the claude-skills system, with emphasis on recent enhancements.

## Core Features

### 1. Persistent Context System (`tasks/`)

**Files that persist across sessions:**

- **`tasks/findings.md`** — Design decisions, discoveries, prior context
  - Written by: `/brainstorm`, `/execute-plan`, `/debug`
  - Read by: `/brainstorm`, `/write-plan`, `/debug`, `/frontend-design`
  - Never cleared or reset

- **`tasks/lessons.md`** — Prevention rules (compounding knowledge)
  - Written by: `/debug`, `/write-tests` (when bugs found), `/execute-plan` (user corrections)
  - Read by: `/brainstorm`, `/write-plan`, `/execute-plan`, `/write-tests`, `/debug`, `/review`, `/security-check`, `/finish-feature`
  - Active constraints applied to 8+ skills
  - Never overwritten (idempotent append-only)

- **`tasks/security-findings.md`** — Security audit results (compounding security posture)
  - Written by: `/security-check`
  - Read by: `/brainstorm` (security constraints), `/review` (verify fixes), `/finish-feature` (security gate)
  - Never overwritten (new audits append below previous)

- **`tasks/todo.md`** — Current plan checkboxes
  - Written by: `/write-plan`
  - Read by: `/execute-plan`
  - Cleared only when user explicitly starts a new plan

- **`tasks/progress.md`** — Session work log and error log
  - Written by: `/execute-plan`
  - Read by: `/execute-plan` (error log for learning)
  - Helps correlate failures across batches

### 2. Design Phase: `/brainstorm`

**What it does:**
- Explores user intent and requirements
- Asks clarifying questions one at a time
- Proposes 2-3 approaches with trade-offs
- Gets design approval before proceeding
- No code is written

**Context Threading:**
- ✅ Reads `tasks/findings.md` (prior decisions)
- ✅ Reads `tasks/lessons.md` (design constraints)
- ✅ Writes `tasks/findings.md` (design decisions)

**Key feature:** If findings.md has prior decisions, brainstorm asks: "extend, revise, or start fresh?" — avoids re-exploring what's already decided.

### 3. Planning Phase: `/write-plan`

**What it does:**
- Creates a decision-complete plan in `tasks/todo.md`
- Checkbox-based with verification commands
- No code is written

**Context Threading:**
- ✅ Reads `tasks/findings.md` (design brief)
- ✅ Reads `tasks/lessons.md` (constraint: what not to do)
- ✅ Applies lessons as plan constraints

**Key feature:** Plan steps reflect lessons learned from prior bugs.

### 4. Implementation Phase: `/execute-plan`

**What it does:**
- Implements plan in small batches (3 items per batch)
- Logs all actions to `tasks/progress.md`
- Runs verification for each step
- Checkpoint-based (waits for user after each batch)

**Context Threading:**
- ✅ Reads `tasks/todo.md` (what to build)
- ✅ Reads `tasks/lessons.md` (standing constraints)
- ✅ Reads `tasks/progress.md` (error log — learns from failures)
- ✅ Writes `tasks/progress.md` (work log)
- ✅ Writes `tasks/findings.md` (discoveries during implementation)

**Key feature:** If a step fails, execution logs it and doesn't repeat the same action — learns from error log.

### 5. Smart Commits: `/commit`

**What it does:**
- Analyzes staged changes
- Auto-classifies commit type (feat, fix, test, docs, etc.)
- Generates conventional commit message
- Gets user approval before committing

**Context Threading:**
- Reads `tasks/progress.md` (for work context)

### 6. Test Generation: `/write-tests`

**What it does:**
- Auto-detects testing framework (Vitest, Jest, pytest, Go, Rust, Mocha, PHPUnit)
- Learns from existing tests in project
- Generates test file with 6-8 test cases
- Runs tests and fixes failures

**Context Threading:**
- ✅ Reads `tasks/lessons.md` (patterns to avoid in tests)
- ✅ Writes `tasks/lessons.md` (if code bug discovered during testing)

**Key feature:** Uses Playwright to capture live ARIA tree for role-based selectors.

### 7. Structured Debugging: `/debug`

**What it does:**
- Reproduces the bug (browser or server)
- Forms 2-3 ranked hypotheses
- Tests each hypothesis systematically
- **Hard gate:** No code changes until hypothesis confirmed
- Uses Playwright for browser bugs (console, network, visual)

**Context Threading:**
- ✅ Reads `tasks/findings.md` (what was already tried)
- ✅ Reads `tasks/lessons.md` (prevention rules — tries them first)
- ✅ Writes `tasks/findings.md` (root cause)
- ✅ Writes `tasks/lessons.md` (prevention rule)

**Key feature:** One bug debugged = one lesson written that 8+ skills apply next time.

### 8. Code Review: `/review`

**What it does:**
- Rigorous multi-dimensional review across **7 dimensions:**
  - Correctness, Security, Performance, Reliability, Design, Best Practices, Testing
- Every finding tagged with dimension, file:line, and impact explanation
- Framework-specific deep checks (React, Python, Go, Node.js)
- Performance analysis: N+1 queries, memory leaks, O(n²), unnecessary re-renders
- Reliability checks: error handling quality, graceful degradation, timeout handling
- Report-only — flags issues by severity (Critical, Warning, Nitpick)
- User loops `/debug` + `/commit` + `/review` until clean

**Context Threading:**
- ✅ Reads `tasks/lessons.md` (Bug patterns as targeted checks across all 7 dimensions)
- ✅ Reads `tasks/security-findings.md` (verify prior findings addressed)
- Uses lesson Bug field as automated checklist

**Key feature:** Reviews at the quality bar of a senior engineer at a top-tier tech company — thorough, specific, and honest. Thinks about what could go wrong in production at scale.

### 9. Security Audit: `/security-check`

**What it does:**
- Audits changed files (default) or full project (`--all`) for security vulnerabilities
- Checks against OWASP Top 10 (2021), CWE references, and stack-specific patterns
- Evaluates production readiness (error handling, input validation, secrets management)
- Rates findings by severity: Critical, High, Medium, Low
- Every finding cites file:line and the standard violated

**Context Threading:**
- Reads `tasks/security-findings.md` (check if prior findings addressed)
- Reads `tasks/lessons.md` (security-related lessons as targeted checks)
- Writes `tasks/security-findings.md` (audit results)

**Key feature:** Stack-aware — tailors checks to your framework (React XSS patterns, Express middleware, Python eval/exec, Go error handling, etc.). Downstream skills (`/review`, `/finish-feature`) read security-findings.md to enforce a security gate before merge.

### 10. Finalize + PR: `/finish-feature`

**What it does:**
- Verifies git branch (feature/fix/chore naming)
- Checks CHANGELOG.md entry (auto-commits if updated)
- **Intelligent arch change detection** (auto-commits arch log)
- **Security gate** — checks unresolved Critical/High findings from `/security-check`
- Verifies tests pass, coverage >80%
- Scans diff against lesson patterns (final bug gate)
- **Creates PR via `gh pr create`** — includes summary, review notes, security status

**Context Threading:**
- ✅ Reads `tasks/lessons.md` (Bug patterns to scan for)
- ✅ Reads `tasks/security-findings.md` (unresolved security findings)
- ✅ Auto-detects arch changes and generates draft logs

**Key feature:** Auto-commits documentation changes (changelog, arch log) so you don't need to loop back to `/commit` for docs-only work.

---

## New Features (March 2026)

### Feature 1: Lessons + Findings Context Threading

**The Problem:**
- AI systems have no memory between sessions
- Design decisions get re-asked
- Bugs get repeated
- Context resets with every invocation

**The Solution:**
Every skill that makes decisions now:
1. Reads `tasks/findings.md` (prior context)
2. Reads `tasks/lessons.md` (lessons from past mistakes)
3. Applies them as constraints before proceeding

**Impact:**
- No re-explaining decisions to `/brainstorm`
- No repeating bugs that `/debug` already fixed
- System gets smarter per-project over time
- Compounding knowledge across sessions

**Example Flow:**
```
Session 1: /debug finds cache invalidation bug → writes lesson
Session 2: /write-plan reads lesson → applies as plan constraint
Session 3: /execute-plan reads lesson → applies before implementation
Session 4: /review reads lesson → checks diff against bug pattern
```

### Feature 2: Intelligent Architectural Change Detection

**The Problem:**
- Manual question: "Is this an architectural change?"
- Arch logs are tedious to write (0% drafted)
- Inconsistent format across projects
- Users skip creating arch logs

**The Solution:**
`/finish-feature` step 4 now automatically:

1. **Analyzes git diff** using `detect_arch_changes.py` script (works for ANY project)
2. **Detects architecture-relevant changes:**
   - **Schema/Database** (migrations, models, databases) → Data Flow
   - **API/Routes** (endpoints, controllers, middleware) → Control Flow
   - **Components/Modules** (src/components, pages, lib) → Pattern
   - **Subsystems** (new top-level directories, major refactors) → Subsystem
   - **Configuration** (config files affecting architecture) → Configuration
   - **Dependencies** (package.json, requirements.txt) → Integration
   - **Context Integration** (findings.md, lessons.md reads/writes) → Integration

3. **Auto-generates markdown draft** (80% complete):
   - Auto-populated: Summary, type, files affected, statistics, impact
   - TODO sections: Detailed changes, before/after, affected components, migration notes

4. **User reviews/edits** the remaining 20%
5. **User commits** the final arch log

**Impact:**
- No guessing: script analyzes code, tells you if arch changed
- 80% already drafted: faster to complete
- Consistent format: same structure across all projects
- Works for ANY project: Next.js, Django, FastAPI, Python, Go, etc.
- Arch logs actually get created: not skipped

**Detection Examples:**
```
Next.js project:
  Changes to src/components/ → "Component Architecture Update"
  Schema.prisma changed → "Data Model Refactor"
  API routes changed → "API Structure Enhancement"

Django project:
  Models.py modified → "Data Model Refactor"
  URLs.py changed → "API Structure Enhancement"
  New apps/ directory → "Subsystem Refactor"

Python project:
  requirements.txt → "Dependency Upgrade"
  src/core/ refactored → "Component Architecture Update"
```

---

## Complete Workflow with Context Threading

```
User: "Add two-factor authentication"
    ↓
/brainstorm
  • Reads findings.md (none yet)
  • Reads lessons.md (cache invalidation lesson from prior work)
  • Asks: SMS, email, or app-based? Required or optional?
  • Proposes 3 approaches
  • User approves: "app-based, required"
  • Writes findings.md: design decision
    ↓
/write-plan
  • Reads findings.md: "app-based, required"
  • Reads lessons.md: apply cache invalidation lesson
  • Writes 6-step plan to todo.md
  • Applies lesson as constraint: "invalidate cache AFTER DB update"
    ↓
/execute-plan
  • Reads todo.md: "Generate backup codes", "Add QR endpoint", ...
  • Reads lessons.md: applies cache invalidation constraint
  • Implements batch 1 (3 items)
  • Logs to progress.md
    ↓
/commit (after batch)
  • Analyzes changes
  • Generates: "feat(2fa): add backup code generation"
    ↓
/write-tests
  • Reads lessons.md: check for cache invalidation pattern
  • Generates: backup code tests, recovery tests, edge cases
    ↓
/debug (if needed)
  • QR code endpoint returns 500 on iOS
  • Reads lessons.md: "CORS issue" (learned from prior work)
  • Checks CORS config FIRST
  • CONFIRMED: missing Access-Control-Allow-Origin
  • Fixes + writes lesson: "Always verify CORS headers for cross-origin resources"
    ↓
/security-check
  • Reads security-findings.md (prior audits)
  • Audits changed files: OWASP Top 10 + stack-specific checks
  • Finds: 1 Medium (missing rate limiting on 2FA endpoint)
  • Writes to security-findings.md
  • User fixes, re-runs: all clear ✓
    ↓
/review
  • Reads lessons.md: CORS, cache invalidation, QR code patterns
  • Reads security-findings.md: confirms prior findings addressed ✓
  • Scans diff: ✓ Cache invalidated after DB update (lesson applied)
  • Scans diff: ✓ CORS headers present (bug prevented)
  • Flags: 1 warning → user fixes with /debug, commits, re-runs /review: clean ✓
    ↓
/finish-feature
  • Updates CHANGELOG.md, auto-commits: "docs: update CHANGELOG.md"
  • AUTO-DETECTS: Control Flow + Data Flow changes
  • Auto-generates arch log draft, auto-commits: "docs: add arch log"
  • Security gate: no unresolved Critical/High findings ✓
  • Scans diff against lesson patterns (final gate)
  • Creates PR via gh pr create
  • Reports PR URL

Result:
✅ Two bugs prevented (cache invalidation, CORS)
✅ One security finding caught and fixed before merge
✅ One lesson written during debug
✅ That lesson will be applied to next 3 features
✅ Architectural decision documented
✅ PR created with full context
```

---

## Benefits Summary

| Aspect | Before | After |
|--------|--------|-------|
| **Context Persistence** | Resets every session | Findings + lessons persist |
| **Design Decisions** | Re-explained each time | Read from findings.md |
| **Bug Prevention** | Random fixes | Lessons applied as constraints |
| **Test Patterns** | Ad-hoc | Follow lesson patterns |
| **Code Review** | Generic checks | 7-dimension review with lesson + security patterns |
| **Security** | Ad-hoc or skipped | OWASP + stack-specific audit with security gate |
| **Arch Logs** | 0% drafted, tedious | 80% auto-generated |
| **System Knowledge** | Resets | Compounds over time |
| **Bug Repetition** | Likely | Prevented by lessons |

---

## For Users

**Starting a project:**
1. `/setup-claude` — Bootstrap
2. `/brainstorm` — Design (reads findings.md + lessons.md)
3. `/write-plan` — Plan (applies lessons as constraints)
4. `/execute-plan` → `/commit` → `/write-tests` — Implement
5. `/debug` (if needed) — Writes findings.md + lessons.md
6. `/security-check` — Audit changed files (OWASP, production quality, stack-specific)
7. `/review` — Self-review (report-only). Loop `/debug` + `/commit` until clean
8. `/finish-feature` — Changelog + arch log (auto-committed), security gate, create PR

**Over time:**
- lessons.md grows with project knowledge
- Each skill gets smarter (reads more lessons)
- Bugs get prevented instead of fixed
- Architectural changes are automatically documented
- System requires less guidance (lessons.md is self-enforcing)

---

## Technical Details

### Context Files Location
- **Global:** `tasks/findings.md`, `tasks/lessons.md`, `tasks/todo.md`, `tasks/progress.md`
- **Arch Logs:** `.claude/docs/architectural_change_log/YYYY-MM-DD-{topic}.md`

### Scripts
- **`detect_arch_changes.py`** — Auto-detects architectural changes, generates arch log drafts
  - Usage: `python3 detect_arch_changes.py [--dry-run]`
  - Integrated into `/finish-feature` step 4

### Skills Reading Lessons.md
1. `/brainstorm` — Design constraints
2. `/write-plan` — Plan constraints
3. `/execute-plan` — Standing constraints
4. `/write-tests` — Test pattern constraints
5. `/debug` — Prevention rules (try first)
6. `/security-check` — Security-related lessons as targeted checks
7. `/review` — Bug pattern checks
8. `/finish-feature` — Diff scanning (final gate)

### Skills Reading Findings.md
1. `/brainstorm` — Check if prior work exists
2. `/write-plan` — Extract design brief
3. `/debug` — Check what was already tried
4. `/frontend-design` — Design brief for UI work

### Skills Reading Security-Findings.md
1. `/brainstorm` — Factor recurring security patterns into design
2. `/security-check` — Check if prior findings addressed
3. `/review` — Verify security fixes, check for regressions
4. `/finish-feature` — Security gate (block on unresolved Critical/High)

---

## Future Possibilities

- Lessons.md auto-pruning (remove lessons that never match)
- Findings.md versioning (track decision evolution)
- Cross-project lesson sharing (learn from other projects)
- Visual dashboards (show system knowledge growth)
- Integration with bug trackers (link lessons to issues)

---

**Last Updated:** March 7, 2026
**Version:** 2.1.0 (Context Threading + Auto-Architecture Detection + Security Audit Gate)
