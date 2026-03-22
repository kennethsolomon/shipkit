# claude-skills

Custom [Claude Code](https://claude.ai/code) skills for bootstrapping and maintaining projects.

## ✨ What's New (March 2026)

**5 new commands added** — `/sk:fast-track`, `/sk:gates`, `/sk:retro`, `/sk:reverse-doc`, `/sk:scope-check`:
- `/sk:fast-track` — Abbreviated workflow for small changes, skips planning but keeps all gates
- `/sk:gates` — Run all quality gates in optimized parallel batches (single command replaces 6)
- `/sk:retro` — Post-ship retrospective: velocity, blockers, action items
- `/sk:reverse-doc` — Generate architecture/design docs from existing code
- `/sk:scope-check` — Compare implementation against plan, detect scope creep

**Workflow expanded to 21 steps (v3.7.0)** — New skills and protocols:
- `/sk:e2e` (Step 17) — E2E behavioral verification using agent-browser; hard gate after Review
- **Fix & Retest Protocol** — applies to all code-producing gates (Lint, Test, Security, Performance, Review, E2E): logic changes require updating unit tests before committing
- **Sync Features step** (Step 20) — `/sk:features` runs after Finalize to keep feature specs in sync with shipped code
- **Dependency audit** folded into `/sk:lint` — runs `composer audit` / `npm audit` / `pip-audit` alongside code linters
- All commands standardized to `/sk:` prefix throughout docs and templates

**Pencil MCP Integration** — `/frontend-design` now optionally creates visual `.pen` mockups:
- After the text design summary, prompts: "Would you like me to create a Pencil visual mockup? (y/n)"
- Saves `.pen` files to `docs/design/` in the project
- Requires Pencil app open with MCP connected

**Mobile Store Readiness Audits** — `/release` now supports `--android` and `--ios` flags:
- Covers signing, permissions, icons, privacy policy, SDK levels, store listing, and common rejection reasons
- Auto-detects framework (Expo, React Native, Flutter, native), checks configs, reports PASS/FAIL per item

**Lessons + Findings Context Threading** — Every skill that makes decisions reads `tasks/lessons.md`; every skill that accepts handoff reads `tasks/findings.md`.

**Intelligent Architectural Change Detection** — `/finish-feature` auto-generates 80% of arch log markdown from your diff.

---

## Table of Contents

- [What's New (March 2026)](#-whats-new-march-2026)
- [Installation](#installation)
- [Why This Workflow](#why-this-workflow)
- [Complete Workflow Flow](#complete-workflow-flow)
- [Tutorial — Building a Feature End to End](#tutorial--building-a-feature-end-to-end)
- [New User Quick Start](#new-user-quick-start)
- [Recommended Workflow](#recommended-workflow)
- [Workflow Scenarios: When to Use Each Skill](#workflow-scenarios-when-to-use-each-skill)
- [Skills](#skills)
- **[→ View Complete Features Guide](./FEATURES.md)** — Context threading, auto-detection, lessons compounding
  - [`/setup-claude`](#setup-claude) — Bootstrap project infrastructure
  - [`/claude-setup-tools`](#claude-setup-tools) — Create, diagnose, maintain CLAUDE.md
  - [`/schema-migrate`](#schema-migrate) — Multi-ORM schema change analysis
  - [`/commit`](#commit) — Smart conventional commits
  - [`/frontend-design`](#frontend-design) — Production-grade UI design + optional Pencil mockup
  - [`/api-design`](#api-design) — REST/GraphQL API contract design
  - [`/accessibility`](#accessibility) — WCAG 2.1 AA audit
  - [`/write-tests`](#write-tests) — TDD: write failing tests before implementation
  - [`/debug`](#debug) — Structured debugging
  - [`/perf`](#perf) — Performance audit (bundle, N+1, Core Web Vitals)
  - [`/review`](#review) — Self-review across 7 dimensions (report-only)
  - [`/sk:e2e`](#ske2e) — E2E behavioral verification using agent-browser — final quality gate
  - [`/hotfix`](#hotfix) — Emergency fix workflow
  - [`/finish-feature`](#finish-feature-per-project-command) — Pre-merge checklist (per-project)
  - [`/release`](#release) — Release automation + mobile store audits
- [What Gets Created by `/setup-claude`](#what-gets-created-by-setup-claude)
- [Requirements](#requirements)

---

## Installation

### Step 1: Clone and install (one-time setup)

```bash
git clone git@github.com:kennethsolomon/claude-skills.git
cd claude-skills
./install.sh
```

This symlinks each skill into `~/.claude/skills/` and each command into `~/.claude/commands/`, which is where Claude Code discovers personal skills and commands. After this, **global skills** are immediately available in every project when you type `/` — no per-project setup needed.

### Step 2: Set up a project (per-project)

```bash
cd /path/to/your-project
# Then in Claude Code, run:
/setup-claude
```

This generates **per-project commands** (like `/finish-feature`, `/write-plan`, `/execute-plan`) into your project's `.claude/commands/` directory. These commands are tailored to your project's stack and are only available inside that project.

### What's available when?

| Type | Available after | Scope | Commands |
|------|----------------|-------|----------|
| **Global skills** | Step 1 (clone + link) | Every project | `/sk:brainstorm`, `/sk:frontend-design`, `/sk:api-design`, `/sk:accessibility`, `/sk:write-tests`, `/sk:execute-plan`, `/sk:smart-commit`, `/sk:lint`, `/sk:test`, `/sk:debug`, `/sk:security-check`, `/sk:perf`, `/sk:review`, `/sk:e2e`, `/sk:hotfix`, `/sk:update-task`, `/sk:finish-feature`, `/sk:features`, `/sk:release`, `/sk:schema-migrate`, `/setup-claude`, `/setup-optimizer` |
| **Per-project commands** | Step 2 (`/setup-claude`) | That project only | `/finish-feature`, `/write-plan`, `/execute-plan`, `/plan`, `/status`, `/re-setup` |

### Updating

Pull the latest changes — no re-install needed since it's a symlink:

```bash
cd claude-skills
git pull
```

---

## Complete Workflow Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CLAUDE SKILLS WORKFLOW (21 STEPS)                   │
│                        (Auto-context & Bug Prevention)                       │
└─────────────────────────────────────────────────────────────────────────────┘

PHASE 1: READ (No Code)
  Step 1 — Read tasks/todo.md         Pick the next incomplete task
  Step 2 — Read tasks/lessons.md      Review past corrections before writing code

PHASE 2: DESIGN (No Code)
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 3 — /brainstorm                                                     │
│ • Reads: tasks/findings.md (prior decisions), tasks/lessons.md          │
│ • Clarifies requirements, proposes approaches, gets approval             │
│ • Writes: tasks/findings.md (design decision + rationale)               │
└──────────────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 4 — /frontend-design or /api-design  (OPTIONAL)                    │
│ • /frontend-design: UI mockups, layouts, visual direction (NO CODE)     │
│   → Prompts to create Pencil .pen mockup (saved to docs/design/)        │
│ • /api-design: REST/GraphQL endpoint contracts, request/response shapes │
│ • Skip if pure backend with no UI and no new API                        │
│ • Writes: findings.md (design artifacts + decisions)                    │
└──────────────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 5 — /accessibility  (OPTIONAL)                                      │
│ • WCAG 2.1 AA audit on the design spec                                  │
│ • Checks: color contrast, keyboard nav, ARIA, forms, motion, content    │
│ • Writes: tasks/accessibility-findings.md (append-only)                 │
│ • Skip if backend-only with no frontend                                 │
└──────────────────────────────────────────────────────────────────────────┘
                              ↓
PHASE 3: PLAN (No Code)
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 6 — /write-plan                                                     │
│ • Reads: tasks/findings.md (all design outputs), tasks/lessons.md       │
│ • Writes: tasks/todo.md (decision-complete checklist)                   │
│ • Applies lessons as plan constraints                                   │
└──────────────────────────────────────────────────────────────────────────┘
                              ↓
PHASE 4: BRANCH + MIGRATE
  Step 7 — /branch            Create feature branch auto-named from task
  Step 8 — /schema-migrate    (OPTIONAL) Analyze schema changes safely

PHASE 5: IMPLEMENT (Code Time)
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 9 — /write-tests   TDD RED: write failing tests first              │
│ Step 10 — /execute-plan TDD GREEN: implement to make tests pass         │
│ Step 11 — /smart-commit Commit tests + implementation                   │
└──────────────────────────────────────────────────────────────────────────┘
                              ↓
PHASE 6: QUALITY GATES (all are HARD GATES — cannot be skipped)
┌──────────────────────────────────────────────────────────────────────────┐
│ Step 12 — /sk:lint  ★ HARD GATE (Lint + Dep Audit)                     │
│ • All linting tools must pass. Fix, auto-commit, and re-run until clean.│
├──────────────────────────────────────────────────────────────────────────┤
│ Step 13 — /sk:test  ★ HARD GATE — 100% coverage on new code            │
│ • All test suites must pass. Fix, auto-commit, and re-run until clean.  │
├──────────────────────────────────────────────────────────────────────────┤
│ Step 14 — /sk:security-check  ★ HARD GATE — 0 issues all severities   │
│ • Reads: tasks/security-findings.md (prior audits), tasks/lessons.md   │
│ • OWASP Top 10, CWE references, stack-specific checks                  │
│ • Writes: tasks/security-findings.md (severity-rated findings)          │
│ • Pre-existing issues logged to tasks/tech-debt.md                     │
├──────────────────────────────────────────────────────────────────────────┤
│ Step 15 — /sk:perf  (OPTIONAL GATE — loop until critical/high = 0)    │
│ • Frontend: bundle size, render perf, Core Web Vitals (LCP, CLS, INP) │
│ • Backend: N+1 queries, missing indexes, unbounded queries, caching    │
│ • Writes: tasks/perf-findings.md (append-only)                         │
│ • Pre-existing issues logged to tasks/tech-debt.md                     │
├──────────────────────────────────────────────────────────────────────────┤
│ Step 16 — /sk:review  ★ HARD GATE — 0 issues including nitpicks        │
│ • 7 dimensions: Correctness, Security, Performance, Reliability,       │
│   Design, Best Practices, Testing                                       │
│ • Reads: tasks/lessons.md, tasks/security-findings.md                  │
├──────────────────────────────────────────────────────────────────────────┤
│ Step 17 — /sk:e2e  ★ HARD GATE — E2E behavioral verification           │
│ • Agent-browser end-to-end tests — final quality gate                  │
│ • Verifies full user flows, not just unit behavior                     │
└──────────────────────────────────────────────────────────────────────────┘
                              ↓
PHASE 7: FINISH
  Step 18 — /sk:update-task     Mark task done in tasks/todo.md
  Step 19 — /sk:finish-feature  Changelog + arch log (auto-committed) + PR
  Step 20 — /sk:features        Sync Features
  Step 21 — /sk:release         (OPTIONAL) Version bump + tag + store audits

PERSISTENT CONTEXT FILES (Never Cleared)
┌──────────────────────────────────────────────────────────────────────────┐
│ tasks/findings.md              ← Decisions, discoveries, prior context  │
│ tasks/lessons.md               ← Prevention rules (read by 8+ skills)  │
│ tasks/security-findings.md     ← Security audit results                 │
│ tasks/accessibility-findings.md← WCAG audit results                     │
│ tasks/perf-findings.md         ← Performance audit results              │
│ tasks/tech-debt.md             ← Pre-existing issues found during gates │
│ tasks/todo.md                  ← Current plan (checkboxes)              │
│ tasks/progress.md              ← Session work log + error log           │
└──────────────────────────────────────────────────────────────────────────┘

KEY PRINCIPLES
✓ Hard gates: steps 12 (Lint+Dep Audit), 13 (Verify Tests), 14 (Security), 16 (Review+Simplify), 17 (E2E Tests) BLOCK all forward progress until clean
✓ Optional steps (4, 5, 8, 15, 21) require explicit confirmation to skip
✓ Every skill that makes decisions reads lessons.md
✓ Every skill that accepts handoff reads findings.md
✓ No context reset = no repeated mistakes
```

---

## Why This Workflow

AI-assisted development without structure produces more bugs, not fewer. The reason is simple: AI has no memory, no discipline, and no accountability without explicit guardrails. Left to itself, it will make architectural decisions inline, inconsistently, without user visibility, and reset all context every session. This workflow enforces the guardrails that prevent that.

**The five root causes of bugs in AI-assisted projects — and how each step addresses them:**

1. **Building the wrong thing** → `/brainstorm` forces requirement clarity before a single line is written. You cannot skip it and expect the right outcome. It reads existing `tasks/findings.md` so prior decisions are never re-litigated accidentally. Also reads `tasks/lessons.md` to apply known constraints.

2. **Ad-hoc implementation** → `/write-plan` writes a decision-complete plan into `tasks/todo.md` — and reads `tasks/lessons.md` first, so known failure patterns become plan constraints. Without an approved plan, Claude makes architectural decisions inline — inconsistently and without user visibility.

3. **Untested code reaching review** → `/write-tests` after every feature. Tests are not optional in this workflow. A feature without tests is not done. Reads lessons.md to apply known test patterns and avoid past mistakes.

4. **Symptom masking instead of root-cause fixing** → `/debug` has a hard gate: no code changes until a hypothesis is confirmed. Random fixes are explicitly forbidden by the skill. It reads `tasks/progress.md` to correlate recent error patterns, reads `tasks/findings.md` and `tasks/lessons.md` to apply prior knowledge, and writes both when finding root causes.

5. **Repeated mistakes** → `tasks/lessons.md` is read by `/execute-plan`, `/write-plan`, `/write-tests`, `/debug`, `/review`, and `/finish-feature` before they start. The system compounds knowledge instead of resetting each session. When you correct the agent mid-execution, it writes the lesson immediately. Lessons become active constraints, not just documentation.

**Architectural Changes Without Manual Guessing:**
→ `/finish-feature` step 4 now auto-detects architectural changes using intelligent script analysis. No more "did I need an arch log?" questions. The script analyzes your diff, generates a markdown draft (80% complete), and you edit the final 20%.

**The opinionated rule:** Follow all steps in order. Optional steps (design, accessibility, performance) can be skipped with confirmation. Hard gates (lint, tests, security, review, e2e) can never be skipped. A "quick fix" that bypasses brainstorm and planning is the source of most production bugs in AI-assisted codebases.

This is an opinionated workflow. It will feel slower at first. It is faster over the lifetime of a project because rework is the most expensive operation in software development.

---

## Tutorial — Building a Feature End to End

A concrete walkthrough: *Add user avatar upload to a Next.js app.*

```
Step 1 — Explore: /brainstorm add user avatar upload
→ Reads existing tasks/findings.md (none yet); asks clarifying questions:
  "S3 or server storage? Max file size? Instant crop or manual?"
  saves approach decision to tasks/findings.md

Step 1a — Design: /frontend-design
→ Reads findings.md (brainstorm decision: S3, 10MB, instant crop);
  Creates UI mockups: upload form, progress indicator, crop interface
  (no code yet—just design artifacts)
  Writes design to tasks/findings.md

Step 2 — Plan: /write-plan
→ Reads findings.md (both brainstorm + frontend-design outputs);
  Reads lessons.md + CLAUDE.md;
  Writes unified 8-step plan to tasks/todo.md:
  [ ] S3 bucket configuration + upload endpoint
  [ ] Frontend upload form component (from design)
  [ ] Crop preview component (from design)
  [ ] Tests for endpoint + components
  [ ] Manual testing on staging

Step 3 — Implement: /execute-plan
→ Reads lessons.md + progress.md error log, runs batch 1 (items 1–3),
  logs to tasks/progress.md; prompts: run /commit after batch passes

Step 4 — Commit: /commit
→ Reads tasks/progress.md for rationale; generates:
  feat(avatar): add S3 upload endpoint

Step 5 — Test: /write-tests src/avatar/upload.ts
→ Reads lessons.md, generates upload.test.ts with 6 test cases, all pass

Step 6 — Review: /review
→ Reads CLAUDE.md + lessons.md Bug fields as targeted checks;
  flags 1 warning (missing file-size validation); no criticals

Step 7 — Finalize: /finish-feature
→ Checklist: changelog updated ✓, test coverage >80% ✓, PR approved ✓
```

Each step hands context to the next. The design + plan approach ensures frontend and backend are aligned before code starts. The lesson loop means a mistake caught in Step 6 becomes a prevention rule that Step 2 applies on the next feature.

---

## New User Quick Start

### Prerequisites

Install these before using the skills:

- [Claude Code CLI](https://claude.ai/code) — the AI coding agent
- [GitHub CLI (`gh`)](https://cli.github.com/) — required for `/finish-feature` PR creation
- Python 3 — required for the `/setup-claude` deterministic bootstrap script
- `playwright@claude-plugins-official` plugin — required for browser verification in `/frontend-design`, `/debug`, and `/write-tests` (Playwright projects). Enable in Claude Code settings under Plugins.

### Your First Project

Four commands to go from zero to a fully configured project:

```bash
# 1. Clone and install the skills (one-time, global)
git clone git@github.com:kennethsolomon/claude-skills.git
cd claude-skills && ./install.sh

# 2. Open your project in Claude Code
cd /path/to/your-project

# 3. Bootstrap the project (run inside Claude Code)
/setup-claude

# 4. Verify your CLAUDE.md looks right
/doctor-claude
```

After these four steps: `CLAUDE.md` is configured for your stack, `tasks/` planning files exist, and all workflow commands (`/brainstorm`, `/frontend-design`, `/api-design`, `/write-plan`, `/write-tests`, `/execute-plan`, `/lint`, `/test`, `/security-check`, `/perf`, `/review`, `/finish-feature`) are available.

### Daily Workflow

During normal development, follow the 27-step workflow: Read → Explore → Design → Accessibility → Plan → Branch → Migrate → Write Tests → Implement → Lint → Verify Tests → Security → Performance → Review → E2E Tests → Finish → Sync Features. See the [Complete Workflow Flow](#complete-workflow-flow) above for the full diagram with all hard gates and optional steps.

---

## Recommended Workflow

The complete 27-step workflow from idea to merge with **automatic context threading and bug prevention**:

| # | Step | Command | Notes |
|---|------|---------|-------|
| 1 | Read Todo | read `tasks/todo.md` | Pick the next incomplete task |
| 2 | Read Lessons | read `tasks/lessons.md` | Review past corrections |
| 3 | Explore | `/sk:brainstorm` | Clarify requirements — no code |
| 4 | Design | `/sk:frontend-design` or `/sk:api-design` | Optional — skip if pure backend |
| 5 | Accessibility | `/sk:accessibility` | Optional — skip if no frontend |
| 6 | Plan | `/sk:write-plan` | Decision-complete plan — no code |
| 7 | Branch | `/sk:branch` | Auto-named from current task |
| 8 | Migrate | `/sk:schema-migrate` | Optional — skip if no schema changes |
| 9 | Write Tests | `/sk:write-tests` | TDD red: failing tests first |
| 10 | Implement | `/sk:execute-plan` | TDD green: make tests pass |
| 11 | Commit | `/sk:smart-commit` | Commit tests + implementation |
| 12 | **Lint + Dep Audit** | `/sk:lint` | **HARD GATE** — gates own commits; fix-commit-rerun internally |
| 13 | **Verify Tests** | `/sk:test` | **HARD GATE** — gates own commits; 100% coverage |
| 14 | **Security** | `/sk:security-check` | **HARD GATE** — gates own commits; 0 issues |
| 15 | Performance | `/sk:perf` | Optional gate — critical/high must reach 0 |
| 16 | **Review + Simplify** | `/sk:review` | **HARD GATE** — gates own commits; 0 issues |
| 17 | **E2E Tests** | `/sk:e2e` | **HARD GATE** — gates own commits; all scenarios pass |
| 18 | Update | `/sk:update-task` | Mark done, log completion |
| 19 | Finalize | `/sk:finish-feature` | Changelog + PR |
| 20 | Sync Features | `/sk:features` | Sync feature specs with shipped code |
| 21 | Release | `/sk:release` | Optional — version bump + tag |

### Key Features

✅ **5 Hard Gates** — Lint+Dep Audit (12), Tests (13), Security (14), Review+Simplify (16), E2E Tests (17) block all forward progress until clean
✅ **TDD Enforced** — Tests written before implementation (step 9), verified after (step 14)
✅ **Context Threading** — findings.md flows brainstorm → design → plan; never re-ask decisions
✅ **Compounding Lessons** — One bug debugged = one lesson written = 8+ skills apply it next time
✅ **Auto-Architecture Detection** — `/finish-feature` intelligently detects & documents arch changes
✅ **No Context Reset** — findings.md, lessons.md, security-findings.md, perf-findings.md persist across sessions

### Design Phase Options

`/brainstorm` is required. Design step (4) is optional — choose based on what you're building:

- **`/brainstorm` (required)** — explores user intent, clarifies requirements, proposes approaches, and gets approval. No code is written.
- **`/frontend-design` (optional)** — for UI work: mockups, layouts, visual direction, optional Pencil `.pen` mockup. Skip for backend-only.
- **`/api-design` (optional)** — for new APIs: endpoint design, request/response shapes, auth flows, error codes. Skip if no new API surface.
- **`/accessibility` (optional, step 5)** — WCAG 2.1 AA audit on the design spec. Skip if no frontend.
- **`/write-plan` (required)** — incorporates brainstorm + design outputs into a unified plan.

**With UI work:**
```
/brainstorm        ← clarify: what are we building?
/frontend-design   ← design: UI mockups, layouts (no code)
/accessibility     ← WCAG 2.1 AA audit on the design
/write-plan        ← unified plan for frontend + backend
```

**With new API:**
```
/brainstorm    ← clarify requirements
/api-design    ← design: endpoints, payloads, auth, errors
/write-plan    ← plan the implementation
```

**Backend-only (no UI, no new API):**
```
/brainstorm    ← clarify: what are we building?
/write-plan    ← plan the implementation
```

---

## Workflow Scenarios: When to Use Each Skill

Three concrete scenarios showing how the full skill system works together — **works identically for both new and existing projects.**

### Scenario 1: Add a Feature (Feature Branch)

**Context:** You're working in an existing project (Next.js app) or a new project just bootstrapped with `/setup-claude`. You want to add a new feature.

```
START:  I want to add two-factor authentication to user login

Step 1 — DESIGN (no code yet)
   /brainstorm Add two-factor authentication to login
   → Reads tasks/findings.md (if it exists from prior work)
   → Asks: SMS, email, or app-based? Required or optional?
   → Asks: Should we store backup codes?
   → Proposes 3 approaches, gets your approval
   → Writes design decision to tasks/findings.md

Step 2 — PLAN (no code yet)
   /write-plan
   → Reads tasks/findings.md (uses your prior design decision)
   → Reads tasks/lessons.md (if prior bugs taught us lessons, applies them)
   → Writes detailed 6-step plan to tasks/todo.md
     [ ] Generate backup codes
     [ ] Add QR code verification endpoint
     [ ] Add 2FA toggle to user settings
     [ ] Write tests for backup code recovery
     [ ] Update API docs
     [ ] Manual testing on staging

Step 3 — IMPLEMENT (code time)
   /execute-plan
   → Reads tasks/todo.md (knows exactly what to do)
   → Reads tasks/lessons.md (applies past lessons as constraints)
   → Implements item 1, logs to tasks/progress.md
   → Prompts: /commit after this batch? (you say yes)

Step 4 — COMMIT
   /commit
   → Analyzes staged changes (generates, tests, types)
   → Auto-classifies: feat(2fa): add backup code generation
   → Asks approval: create this commit? (you say yes)

   [repeat: /execute-plan batch → /commit after logical unit]

Step 5 — TEST
   /write-tests src/2fa/verify.ts
   → Reads tasks/lessons.md (knows what not to do)
   → Generates test cases: valid code, expired code, rate limiting
   → Tests pass on first run

Step 6 — DEBUG (if something breaks)
   /debug The QR code endpoint returns 500 on iOS
   → Reproduces: navigates to page, checks console errors
   → Forms hypotheses: wrong CORS header? Image format issue?
   → Tests hypothesis #1: checks CORS config
   → CONFIRMED: missing Access-Control-Allow-Origin
   → Proposes fix, you approve
   → Logs finding to tasks/findings.md
   → Writes lesson: "Always verify CORS headers for cross-origin image loads"
     (this lesson will now be read by /write-plan, /execute-plan, /review on next feature)

Step 7 — SECURITY AUDIT
   /security-check
   → Reads tasks/security-findings.md (prior audits)
   → Audits changed files against OWASP Top 10 + stack-specific checks
   → Finds: 1 Medium (missing rate limiting on QR endpoint)
   → Writes findings to tasks/security-findings.md
   → User fixes and re-runs: all clear ✓

Step 8 — REVIEW
   /review
   → Reads tasks/lessons.md (uses Bug patterns as targeted checks)
   → Reads tasks/security-findings.md (checks prior audit resolved)
   → Scans diff for: CORS issues ✓, QR code encoding ✓, token expiry ✓
   → Flags: 1 warning (missing refresh token rotation), no criticals
   → User fixes with /debug, commits, re-runs /review: all clean ✓

Step 9 — FINALIZE + PR
   /finish-feature
   → Updates CHANGELOG.md, auto-commits: "docs: update CHANGELOG.md"
   → AUTO-DETECTS arch changes, generates draft, auto-commits: "docs: add arch log"
   → Security gate: no unresolved Critical/High findings ✓
   → Tests pass ✓, coverage >80% ✓
   → Scans diff for lesson patterns (CORS lesson applies here)
   → Creates PR via gh pr create
   → Reports PR URL

SHIP: PR created, ready for merge ✅
```

### Scenario 2: Bug Fix with Lesson Learning (The Debug Loop)

**Context:** Code shipped, users report a bug. You need to fix it and prevent it from happening again.

```
START:  The reset password endpoint is failing for users with special chars in email

Step 1 — ASSESS (quick look)
   git log --oneline
   git diff main
   → Last changed 2 days ago in "feat: password reset"
   → Suspicious: email validation looks too simple

Step 2 — DEBUG (structured investigation)
   /debug Users with + or _ in email can't reset password

   PHASE 1: REPRODUCE
   → Creates test user: user+test@example.com
   → Tries password reset endpoint
   → CONFIRMED: 400 Bad Request (not 200)

   PHASE 2: ISOLATE
   → Checks: is it the email validation? The token generation? The DB query?
   → Runs curl with email-encoded: user%2Btest@example.com
   → ISOLATED: email validation regex rejects + character

   PHASE 3: HYPOTHESIZE (forms 3 ranked guesses)
   → Hypothesis #1 (likely): Regex in email validation doesn't allow +
     (RFC 5321 allows +, so this is a bug)
   → Hypothesis #2: Database column encoding issue
   → Hypothesis #3: Password reset token generation strips special chars

   PHASE 4: VERIFY
   → Checks src/auth/email-validation.ts
   → Line 12: /^[a-zA-Z0-9._-]+@/ ← BUG! Should be /^[a-zA-Z0-9._+-]+@/
   → Confirms: RFC 5321 allows +, dash, underscore, period

   PHASE 5: FIX & VERIFY
   → Proposes: update regex to /^[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$/
   → Tests: user+test@example.com ✓, user_test@example.com ✓, user-test@example.com ✓
   → Regression: user123@example.com ✓

   PHASE 6: DOCUMENT LESSON
   → Writes to tasks/findings.md:
     ## Email Validation Bug (March 5)
     - Issue: Regex didn't allow + in email local part
     - Fix: Updated to /^[a-zA-Z0-9._+-]+@.../
     - Reference: RFC 5321 allows these chars

   → Writes to tasks/lessons.md (NEW LESSON):
     **Bug:** Email validation too restrictive
     **Root cause:** Regex pattern didn't follow RFC 5321 spec
     **Prevention:** Always validate email against RFC 5321; allow +-._ in local part
     (This lesson will now be read by /write-tests, /review, /execute-plan)

Step 3 — TEST THE FIX
   /write-tests src/auth/email-validation.ts
   → Reads tasks/lessons.md (sees new email lesson)
   → Generates tests: valid +, valid _, valid -, edge case: many special chars
   → All pass

Step 4 — COMMIT
   /commit
   → Auto-classifies: fix(auth): allow special chars in email validation (RFC 5321)

Step 5 — REVIEW (with lesson checking!)
   /review
   → Reads tasks/lessons.md (email lesson is active)
   → Checks diff for: email validation ✓, RFC compliance ✓
   → No warnings — review is clean

Step 6 — FINALIZE + PR
   /finish-feature
   → Updates CHANGELOG.md, auto-commits docs
   → Reads tasks/lessons.md
   → Scans diff against email lesson: ✓ Pattern not found (we fixed it)
   → Creates PR via gh pr create

RESULT: Bug fixed + lesson learned. Next time you work on email validation,
/write-plan will read that lesson and remind you about RFC 5321 ✅
```

### Scenario 3: When to Use Each Command

| Situation | Command | Why? |
|-----------|---------|------|
| **Starting a new feature** | `/brainstorm` | Lock in design before coding. Prevents "building the wrong thing." |
| **Building UI** | `/frontend-design` | Design mockups before code. Optional Pencil visual mockup. |
| **Building a new API** | `/api-design` | Design contracts before code. Endpoint, payloads, errors. |
| **UI design needs review** | `/accessibility` | WCAG 2.1 AA audit before planning. |
| **Feature planned, ready to code** | `/write-plan` | Creates checklist. Applies lessons as constraints. |
| **Implementing the plan** | `/execute-plan` | Batches work, logs to progress.md, reads lessons before each batch. |
| **Logical unit done** | `/smart-commit` | After each 2-3 tasks. Generates conventional commit message. |
| **Feature ready for tests** | `/write-tests` | TDD: write failing tests first, then implement. |
| **Something breaks** | `/debug` | Structured investigation. Reproduces, isolates, hypothesizes, verifies. |
| **Code complete — lint gate** | `/lint` | All linters must pass. Hard gate — cannot skip. |
| **Code complete — test gate** | `/test` | 100% coverage on new code. Hard gate — cannot skip. |
| **Code complete, pre-review** | `/security-check` | OWASP Top 10, 0 issues required. Hard gate. |
| **Performance concerns** | `/perf` | Bundle, N+1, Core Web Vitals. Optional gate. |
| **Ready for review** | `/review` | 7-dimension self-review. 0 issues required. Hard gate. |
| **Production emergency** | `/hotfix` | Skips design/TDD, quality gates still enforced. |
| **Review clean, ready to ship** | `/finish-feature` | Changelog + arch log + security gate + create PR. |

### Scenario 4: Lessons Compounding Over Time

Day 1: `/debug` finds race condition in cache invalidation → writes lesson
```
**Bug:** Cache not invalidated on concurrent updates
**Root cause:** Missing mutex lock on cache write
**Prevention:** Always use cache.invalidate() AFTER db.update(), never before
```

Day 5: `/write-plan` reads lesson, applies it to new feature:
```
Step 3: Update user profile
   [Apply lesson: cache invalidation after DB update, never before]

→ Plan now says: "Update DB, then invalidate cache"
```

Day 6: `/execute-plan` reads lesson as standing constraint:
```
Implementing "Update user profile"...
→ Reading lessons.md for constraints
→ Found: cache invalidation after DB update
→ Applying: invalidate() call happens AFTER update() ✓
```

Day 10: `/review` scans diff against lessons:
```
Checking diff for cache patterns...
→ Lesson says: "cache.invalidate() AFTER db.update()"
→ Scanning diff... ✓ invalidate() on line 42 is AFTER update() on line 39
→ No warnings
```

**Result:** One lesson learned → read by 3+ subsequent skills → prevents the same bug from happening again.

---

## Skills

### `/setup-claude`

Bootstrap or repair Claude Code infrastructure on any project.

**What it does:**
- Detects your tech stack (Next.js, Laravel, Python, Go, Ruby, etc.)
- Creates or optimizes `CLAUDE.md`, project commands in `.claude/commands/`, and Claude docs in `.claude/docs/`
- Adds `tasks/findings.md` + `tasks/progress.md` for persistent context across long sessions
- Adds project-level workflow commands: `/re-setup`, `/brainstorm`, `/write-plan`, `/execute-plan`, `/plan`, `/status`, `/security-check`, `/finish-feature`
- Fully idempotent — safe to re-run on existing projects

**Supported stacks:** Next.js + Drizzle, Next.js + Prisma, Next.js + Supabase, Laravel + Eloquent, Supabase (any framework), Python + FastAPI, Generic

**Usage:** Open any project in Claude Code and run:
```
/setup-claude
```

#### Tutorial: Recommended Workflow

1. Run `/setup-claude` (creates scaffolding + commands).
2. Read `tasks/todo.md` (pick next task) and `tasks/lessons.md` (past corrections).
3. Run `/brainstorm` to explore requirements (no code).
4. *(Optional)* Run `/frontend-design` or `/api-design` for design artifacts (no code).
5. *(Optional)* Run `/accessibility` for WCAG 2.1 AA audit on the design.
6. Run `/write-plan` to write a decision-complete plan into `tasks/todo.md`.
7. Run `/branch` to create a feature branch.
8. *(Optional)* Run `/schema-migrate` for database changes.
9. Run `/write-tests` to write failing tests first (TDD red phase).
10. Run `/execute-plan` to implement in small batches (TDD green phase).
11. Run `/smart-commit` to commit tests + implementation.
12. Run `/sk:lint` — **hard gate** (Lint + Dep Audit), fix and re-run until clean.
13. Run `/sk:test` — **hard gate**, 100% coverage on new code.
14. Run `/sk:security-check` — **hard gate**, 0 issues across all severities.
15. *(Optional)* Run `/sk:perf` for performance audit.
16. Run `/sk:review` — **hard gate** (Review + Simplify), 0 issues including nitpicks.
17. Run `/sk:e2e` — **hard gate**, E2E behavioral verification.
18. Run `/sk:update-task` to mark the task done.
19. Run `/sk:finish-feature` to finalize (changelog, arch log, security gate, create PR).
20. Run `/sk:features` to sync features.
21. Run `/sk:release` to tag and push (add `--android` or `--ios` for store audits).

#### Deterministic Bootstrap Script

If you want the bootstrap to be deterministic (not dependent on an agent following instructions), run:

```bash
cd /path/to/project
python3 "$HOME/.claude/skills/setup-claude/scripts/apply_setup_claude.py" "$(pwd)"
```

If your repo already has a custom `CLAUDE.md`, `/setup-claude` will not overwrite it. Instead it writes a generated draft to `CLAUDE.setup-claude.md` that you can copy/paste from.

Preview what would change (no writes):

```bash
python3 "$HOME/.claude/skills/setup-claude/scripts/apply_setup_claude.py" "$(pwd)" --dry-run
```

Print detected values (JSON):

```bash
python3 "$HOME/.claude/skills/setup-claude/scripts/apply_setup_claude.py" "$(pwd)" --print-detection
```

Optional: update previously generated files only (files containing `<!-- Generated by /setup-claude -->`):

```bash
python3 "$HOME/.claude/skills/setup-claude/scripts/apply_setup_claude.py" "$(pwd)" --update-generated
```

**What it does:**
- Detects basic stack info (from `package.json` and common config files)
- Renders templates from `~/.claude/skills/setup-claude/templates/`
- Creates planning files in `tasks/` (create-if-missing)
- Creates/updates `.claude/commands/*`, `.claude/docs/*`, and `CLAUDE.md` (updates only if generated)
- Creates `CHANGELOG.md` if missing (never overwrites)

---

### `/claude-setup-tools`

Create, diagnose, and intelligently maintain `CLAUDE.md` files with auto-detection, comprehensive context discovery, and safe re-running during development.

**Three Skills + Three Guides:**

**Skills:**
- `/setup-starter` — Auto-generate CLAUDE.md with intelligent project discovery (ENHANCED)
- `/doctor-claude` — Diagnose issues with context-aware suggestions (ENHANCED)
- `/optimize-claude` — Enrich CLAUDE.md with project context and safely re-run during development

**Guides:**
- `/explain-claude` — Learn what each CLAUDE.md section means
- `/implement-claude` — Step-by-step workflow to create perfect CLAUDE.md
- `/review-claude` — Quality checklist before committing

**What `/setup-starter` Does (Enhanced):**
- 🔍 **Auto-discovers** actual project directories: src/, tests/, docs/, config/, scripts/, etc.
- 📚 **Finds documentation**: README.md, CONTRIBUTING.md, docs/*.md, .github/CONTRIBUTING.md
- 🔧 **Detects workflows**: npm scripts, Makefile targets, GitHub Actions workflows
- 📄 **Generates tailored CLAUDE.md** specific to each project (not generic)
- 📊 **Reports discoveries** showing directories, docs, and workflows found
- ✅ Preserves all file safety features (sidecar handling, markers)

**What `/doctor-claude` Does (Enhanced):**
- 🔍 **Discovers project structure** during diagnosis for comparison
- 📊 **Compares documented vs actual** content to identify gaps
- ⚠️ **Reports undocumented** directories and missing documentation sections
- 💡 **Stack-specific suggestions**: Tailored to React, Django, FastAPI, etc.
- 🔧 **Detects workflows** and suggests documentation improvements
- ✅ Shows "Project Structure Detected" in diagnostic output

**What `/optimize-claude` Does:**
- 🔍 **Auto-discovers** project structure: src/, tests/, docs/, config/, etc.
- 📚 **Finds documentation**: README.md, CONTRIBUTING.md, docs/*.md, etc.
- 🔧 **Detects workflows**: Makefile targets, npm scripts, GitHub Actions
- 🔄 **Safely re-runs** during development without losing customizations
- 🔒 **Preserves edits** with smart detection + auto-locking of user sections
- 📊 **Reports findings** showing what was added and preserved

**Key Features:**
- ✅ Auto-detects JavaScript, Python, Go, Rust projects
- ✅ Generates CLAUDE.md in seconds (100-150 lines)
- ✅ Stays under 200 lines with comprehensive context
- ✅ Safe to run multiple times (preserves all user work)
- ✅ Never overwrites without permission (marker system)
- ✅ Works with real project structure (not templates)

**Why use it:**
- 💨 Saves 15+ minutes per project vs manual writing
- 🔄 Maintenance command - run during development to keep CLAUDE.md fresh
- 🛡️ Smart customization preservation - your edits are always safe
- 📚 Comprehensive yet maintainable - grows with your project
- 🤖 Automated discovery - new dirs/docs/workflows auto-detected

**Supported stacks:** Node.js (React, Next.js, etc.), Python (FastAPI, Django, Flask), Go, Rust, and any project (manual customization)

**Typical Usage:**
```bash
/setup-starter          # Create initial CLAUDE.md
                        # (auto-discovers: 7 directories, 10 doc files, workflows)

# Verify the generated CLAUDE.md
/doctor-claude          # Shows discovered structure and suggestions

# Later, after adding directories/docs:
/optimize-claude        # Discovers and adds them automatically!

# Edit Important Context with custom notes
vim CLAUDE.md
/optimize-claude        # ✅ Your edits preserved!
```

**Example Output from `/setup-starter`:**
```
✓ CLAUDE.md created: CLAUDE.md
  Lines: 104/150
  Sections: Stack, Quick Start, Project Structure, Key Files, Development,
            Build & Deploy, Important Context, Environment Variables,
            Common Tasks, Documentation, Key Directories,
            Documentation & Resources, Common Workflows

📁 Discoveries from project structure:
   📂 7 directories found
   📚 10 documentation files
   🔧 Workflows discovered and documented

✅ CLAUDE.md created successfully!
```

**Example Output from `/doctor-claude`:**
```
🔍 Project Structure Detected:
   📂 7 directories: src, tests, docs, public, scripts, config, .github
   📚 10 documentation files
   🔧 Workflows: npm (4 scripts)

⚠️ Issues found:
   1. Project has undocumented directories: tests, scripts

💡 Suggestions:
   1. Add documentation for: tests, scripts
   2. Document additional npm scripts: lint, format, type-check
   3. Consider adding 'Components & Architecture' section for React
```

**Example:** For a React + Prisma + Jest project with docs/, the tool discovers all structure automatically and generates complete, organized documentation in under 30 seconds.

---

### `/frontend-design`

Design distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics — producing UI mockups and design artifacts (not code) with visual browser preview.

**What it does:**
- Takes brainstorm findings and produces detailed UI designs: mockups, layouts, visual direction, component sketches
- Commits to a bold aesthetic direction (brutalist, maximalist, refined minimal, retro-futuristic, etc.)
- Creates design artifacts with distinctive typography, color, motion, and spatial composition
- Avoids clichéd choices (Inter/Roboto, purple gradients, cookie-cutter layouts)
- **NO CODE YET** — this is a design phase, not implementation
- **Browser Preview** (optional): shows visual mockups of the proposed design for feedback

**Usage:**
```
/frontend-design build a landing page for a design agency
/frontend-design create a dark dashboard with data visualizations
```

> **Workflow:** Run `/brainstorm` first to lock in requirements, then `/frontend-design` to design, then `/write-plan` to create a unified plan, then `/execute-plan` to implement. See [Brainstorming + Frontend Design](#brainstorming--frontend-design).

> Requires the `playwright@claude-plugins-official` plugin for visual preview. Without it, design artifact generation still works — only the preview step is skipped.

---

### `/schema-migrate`

Analyze schema changes safely before applying them — works across 5 ORMs with auto-detection.

**What it does:**
- Auto-detects your ORM from project files (no configuration needed)
- Scans schema files, migration history, and git diff
- Classifies every change by risk (safe / careful / breaking)
- Detects breaking changes: column drops, type changes, NOT NULL additions, renames
- Detects data issues: orphan rows, duplicate defaults, NULL violations, migration drift
- Provides ORM-specific and dialect-specific migration plans
- Read-only — never auto-executes migrations

**Usage:** Inside any supported project, run before any schema push:
```
/schema-migrate
```

**Compatibility:**

| Stack | Supported | Auto-Detected By |
|-------|-----------|-----------------|
| Node.js + Drizzle + SQLite | ✅ | `drizzle.config.ts` |
| Node.js + Drizzle + PostgreSQL | ✅ | `drizzle.config.ts` |
| Node.js + Drizzle + MySQL | ✅ | `drizzle.config.ts` |
| Node.js + Drizzle + Supabase | ✅ | `drizzle.config.ts` + `supabase/config.toml` |
| Node.js + Prisma (any DB) | ✅ | `prisma/schema.prisma` |
| Node.js + Prisma + Supabase | ✅ | `prisma/schema.prisma` + `supabase/config.toml` |
| Laravel + Eloquent + MySQL | ✅ | `composer.json` → `laravel/framework` |
| Laravel + Eloquent + PostgreSQL | ✅ | `composer.json` → `laravel/framework` |
| Laravel + Eloquent + SQLite | ✅ | `composer.json` → `laravel/framework` |
| Python + SQLAlchemy + Alembic | ✅ | `alembic.ini` |
| Ruby on Rails + ActiveRecord | ✅ | `Gemfile` → `rails` gem |

---

### `/commit`

Smart conventional commits with auto-classification and approval workflow.

**What it does:**
- Checks branch safety (warns if on main/master)
- Analyzes staged changes; if nothing staged, suggests smart groupings
- Auto-classifies commit type: feat, fix, refactor, test, docs, style, perf, chore, ci, build
- Detects scope from file paths
- Generates conventional commit message (`type(scope): description`)
- Presents for approval: commit / edit / split / cancel
- Never uses `--no-verify`, never auto-commits

**Usage:** After staging changes:
```
/commit
```

---

### `/write-tests`

Generate comprehensive test files matching your project's framework and conventions.

**What it does:**
- Auto-detects testing framework (Vitest, Jest, pytest, Go testing, Rust, Mocha, PHPUnit, **Playwright**)
- Reads 1-2 existing test files to learn your project's patterns and style
- Analyzes target code for test cases: happy path, edge cases, error handling, branches
- Writes test file following project conventions (co-located, `tests/` dir, or `__tests__/`)
- **Playwright projects**: uses `browser_snapshot` to capture the live ARIA tree for role-based selector generation (`getByRole`, `getByLabel`) before writing assertions
- Runs the tests and fixes failures (up to 3 attempts)
- Falls back to built-in templates if no existing tests found

**Usage:** Point it at code to test:
```
/write-tests src/auth/login.ts
/write-tests              # tests most recently changed files
```

---

### `/debug`

Structured bug investigation with hypothesis tracking and documentation.

**What it does:**
- Follows a disciplined process: reproduce → isolate → hypothesize → verify → fix
- Hard gate: no code changes until a hypothesis is confirmed
- **Browser/UI bugs**: uses Playwright MCP to navigate to the page, capture JS console errors, inspect failed network requests, and screenshot the visual state — all as primary evidence for hypotheses
- **Server/CLI bugs**: reproduces via Bash as before
- Forms 2-3 ranked hypotheses, tests each systematically
- Checks recent git changes and existing project knowledge
- Proposes minimal fix and waits for approval
- Logs findings to `tasks/findings.md` and lessons to `tasks/lessons.md`

**Usage:** When something is broken:
```
/debug                    # describe the bug when prompted
/debug the API returns 500 on login
```

---

### `/review`

Rigorous multi-dimensional code review across 7 dimensions — the quality bar of a senior engineer at a top-tier tech company. Report-only — PR creation is handled by `/finish-feature`.

**What it does:**
- Reviews all changes on the current branch against main across **7 dimensions:**
  1. **Correctness** — logic errors, null safety, async bugs, race conditions, edge cases, data integrity
  2. **Security** — OWASP Top 10, injection, XSS, auth/authz, data exposure, hardcoded secrets
  3. **Performance** — N+1 queries, O(n²) in hot paths, memory leaks, unnecessary re-renders, missing pagination
  4. **Reliability** — error handling quality, graceful degradation, timeouts, retry logic, validation at boundaries
  5. **Design** — separation of concerns, API contract changes, code clarity, dependency management
  6. **Best Practices** — framework-specific (React, Python, Go, Node.js), conventions, testing quality
  7. **Testing** — coverage gaps, edge cases, assertion quality, test isolation, flakiness risks
- Every finding tagged with dimension, file:line, and **why** it matters
- Generates severity-leveled report: Critical / Warning / Nitpick (max 20 items)
- Critical/Warning: loop `/debug` + `/commit` + `/review` until clean
- Nitpick only: asks user — fix now or proceed to `/finish-feature`?
- Report-only: intentionally cannot modify files

**Usage:** When ready for review:
```
/review
```

---

### `/finish-feature` (per-project command)

> This is not a global skill — it's a project-level command generated by `/setup-claude` into `.claude/commands/finish-feature.md`.

After running `/setup-claude` on your project, you'll have `/finish-feature` available. It provides a comprehensive, stack-aware checklist for finalizing a feature branch including:

**Pre-merge Verification:**
- Git branch validation (feature/fix/chore naming)
- Branch summary review (changes and commits)
- CHANGELOG.md entry verification
- **Intelligent architectural changes detection** (auto-generate arch log drafts)

**Comprehensive Test Verification (for reviewers):**
- ✅ **Automated Tests**: Execute test suite, verify >80% coverage, no skipped tests
- ✅ **Manual Testing**: Framework-specific guidance (React/frontend, FastAPI/backend, CLI/desktop)
- ✅ **Regression Testing**: Verify related functionality still works
- ✅ **Code Quality**: Check for debugging code, hardcoded data, proper error handling

The test checklist is **framework-aware** — generated with guidance specific to your project's stack (language, framework, testing framework). For example:
- **React + Vitest**: Component rendering, state updates, user interactions
- **FastAPI + pytest**: HTTP status codes, request/response validation, database state
- **Express + Jest**: API endpoints, middleware, error handling

#### Smart Architectural Change Detection

When you run `/finish-feature`, Step 4 automatically:

1. **Scans your diff** for architectural changes using the `detect_arch_changes.py` script
2. **Analyzes patterns** like control flow changes, data flow changes, skill integrations
3. **Auto-generates** a markdown draft for the architecture log (80% complete)
4. **Shows you the draft** with TODO sections for you to fill in:
   - What specifically changed in the architecture?
   - Before/after explanation
   - Verification checklist

**Example: Automatic Detection**

```bash
$ /finish-feature
...
Step 4: Check for Architectural Changes
→ Running auto-detector...
✓ Detected: Data Flow + Control Flow changes
✓ Generated draft: .claude/docs/architectural_change_log/2026-03-03-context-threading-enhancement.md

Edit the draft to fill in:
  [ ] Detailed Changes section
  [ ] Before & After description
  [ ] Review verification checklist

Then: git add .claude/docs/architectural_change_log/ && git commit -m "docs: add arch log"
```

**What Gets Detected:**
- Skill files modified → Control Flow changes
- Template changes → Pattern changes
- findings.md/lessons.md reads/writes → Data Flow changes
- Documentation updates → Integration/documentation changes
- New inter-skill connections → System architecture changes

No more manual guessing about whether something is an "architectural change" — the detector analyzes your actual code and tells you.

---

### `/release`

Automate releases with optional mobile store submission audits.

**Modes:**

| Invocation | What happens |
|---|---|
| `/release` | Git release: version bump, CHANGELOG update, git tag, push to GitHub |
| `/release --android` | Git release + Play Store readiness audit |
| `/release --ios` | Git release + App Store readiness audit |
| `/release --android --ios` | Git release + both store audits |

**What the store audit does:**
- Auto-detects your mobile framework (Expo, React Native, Flutter, native Android/iOS, Capacitor/Ionic, .NET MAUI)
- Detects first-time submission vs update (checks versionCode, signing configs, bundle IDs)
- Walks through every section of the store checklist, checking your actual config files
- Reports status per item: **PASS** / **FAIL** / **WARN** / **MANUAL CHECK NEEDED**
- Proposes fixes for config issues (with your approval before applying)
- Guides you through manual steps (screenshots, store listing, privacy policy, etc.)
- Presents a structured summary report with build/submit commands

**Android checklist covers (14 sections):** Developer account, app identity, signing (keystore/EAS), AndroidManifest permissions, target SDK levels, AAB format, icons, splash screen, privacy & data safety, content rating, store listing, testing tracks, build commands, common rejection reasons.

**iOS checklist covers (14 sections):** Developer account, bundle ID, code signing (certs/provisioning/EAS), Info.plist permission descriptions, privacy manifest (2024 requirement), app icons, launch screen, deployment target, privacy & data collection, App Store Connect setup, App Review guidelines, build commands, TestFlight, review preparation.

**Usage:**
```
/release                    # Just tag and push
/release --android          # + Play Store audit
/release --ios              # + App Store audit
/release --android --ios    # + both audits
```

---

### `/api-design`

Design REST/GraphQL API contracts before any implementation begins.

**What it does:**
- Designs endpoint structure, resource relationships, and URL conventions
- Defines request/response shapes, status codes, and error format
- Covers auth flows (JWT, OAuth, API keys), rate limiting, and versioning strategy
- Output: complete API Design Specification — no code, design only

**Usage:** After `/brainstorm`, before `/write-plan`:
```
/api-design
```

---

### `/accessibility`

WCAG 2.1 AA compliance audit on frontend design specs and existing UI code.

**What it does:**
- Audits 7 categories: color/contrast, keyboard navigation, ARIA/semantics, images/media, forms, motion/animation, content/structure
- Every finding includes: WCAG criterion, severity (Critical/High/Medium/Low), specific recommendation
- Writes to `tasks/accessibility-findings.md` (append-only — never overwritten)

**Usage:** After `/frontend-design`, before `/write-plan`:
```
/accessibility
```

---

### `/perf`

Performance audit — auto-detects stack and checks both frontend and backend.

**What it does:**
- **Frontend:** bundle size, render performance, Core Web Vitals (LCP, CLS, INP)
- **Backend:** N+1 queries, missing indexes, unbounded queries, missing caching
- Severity levels: Critical / High / Medium / Low
- Writes to `tasks/perf-findings.md` (append-only)
- Optional gate (step 18): loop until critical/high findings = 0

**Usage:** After security check, before review:
```
/perf
```

---

### /sk:seo-audit

SEO audit for web projects. Dual-mode: scans source templates (`.blade.php`, `.jsx`, `.tsx`, `.vue`, `.html`, etc.) and optionally fetches from a running dev server to validate rendered output. Ask-before-fix for mechanical issues. Outputs checklist findings (with `- [ ]` / `- [x]` items) to `tasks/seo-findings.md`, appended per run.

Run at any point after implementation — not a numbered workflow step.

---

### /sk:context

Session initializer — loads all project context files and outputs a formatted session brief. Run at the start of every conversation.

**What it does:**
- Reads 7 context files: `tasks/todo.md`, `tasks/workflow-status.md`, `tasks/progress.md`, `tasks/findings.md`, `tasks/lessons.md`, `docs/decisions.md`, `docs/vision.md`
- Outputs a formatted SESSION BRIEF with branch, task, step, pending items, lessons, and open questions
- Applies all active lessons from `tasks/lessons.md` as standing constraints for the session
- Graceful fallback for missing files — notes them in the brief instead of erroring

**When to use:** Start of every new conversation. Gives instant orientation without manually reading 5+ files.

---

### /sk:dashboard

Read-only workflow Kanban board served on localhost. Shows workflow status across all git worktrees as a visual dashboard.

**What it does:**
- Serves a browser-based Kanban board displaying workflow step status for the current project
- Scans all git worktrees and reads each `tasks/workflow-status.md` to build the board
- Read-only — no mutations, no side effects
- Standalone optional command, not a numbered workflow step

**Usage:**
```bash
node skills/sk:dashboard/server.js
```
Starts a local server on port 3333 by default. Open `http://localhost:3333` in your browser.

---

### `/hotfix`

Emergency fix workflow for production incidents — skips design and TDD, quality gates still enforced.

**What it does:**
- 15-step flow: investigate → branch → fix → lint → test → security → review → finish
- Skips: brainstorm, design, accessibility, write-tests phases
- All 5 quality gates still enforced (lint, test, security, review, e2e cannot be skipped)
- After merging: prompts to add a regression test and a lessons.md entry

**Usage:** Production emergency only:
```
/hotfix
```

---

### /sk:scope-check

Compare implementation against `tasks/todo.md` to detect scope creep. Classifies changes as On Track, Minor Creep, Significant Creep, or Out of Control based on unplanned additions.

---

### /sk:retro

Post-ship retrospective that analyzes velocity, blockers, gate performance, and patterns from `tasks/progress.md` and git history. Generates 3-5 action items.

---

### /sk:reverse-doc

Generate architecture and design documentation from existing code. Analyzes patterns, asks clarifying questions to distinguish intent from accident, and drafts docs for approval.

---

### /sk:gates

Orchestrator that runs all quality gates in optimized parallel batches: lint+security+perf in parallel, then tests, then review, then E2E. Single command replaces 6 manual invocations.

---

### /sk:fast-track

Abbreviated workflow for small, clear changes. Skips brainstorm, design, plan, and write-tests but enforces all quality gates via /sk:gates. Guard rails warn on large diffs (>300 lines).

---

## What Gets Created by `/setup-claude`

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project instructions for Claude — tech stack, key dirs, workflow rules |
| `.claude/commands/re-setup.md` | `/re-setup` — re-run the bootstrap script to refresh generated files |
| `.claude/commands/brainstorm.md` | `/brainstorm` — design exploration with no-code enforcement |
| `.claude/commands/write-plan.md` | `/write-plan` — write a decision-complete plan into `tasks/todo.md` |
| `.claude/commands/execute-plan.md` | `/execute-plan` — implement the plan in batches with checkpoints |
| `.claude/commands/finish-feature.md` | Branch finalization checklist (stack-aware) |
| `.claude/commands/plan.md` | `/plan` — create/refresh planning files |
| `.claude/commands/status.md` | `/status` — show task progress summary |
| `.claude/docs/changelog-guide.md` | How to maintain `CHANGELOG.md` |
| `.claude/docs/arch-changelog-guide.md` | How to log architectural decisions |
| `tasks/todo.md` | Active task tracker (Goal / Plan / Results / Errors) |
| `tasks/findings.md` | Detection notes and decisions log |
| `tasks/progress.md` | Session work log and error log |
| `tasks/lessons.md` | Accumulated project lessons — never overwritten |
| `CHANGELOG.md` | Keep a Changelog format — never overwritten if exists |

---

## Customizing Generated Commands

### Can I use my own custom commands instead?

**Yes!** Any command file without the `<!-- Generated by /setup-claude -->` marker is treated as custom and will never be overwritten by `/re-setup` or `/setup-claude`.

To use your own custom command:

1. **Delete the generated file** (e.g., `.claude/commands/finish-feature.md`)
2. **Create your own file** with the same name
3. **Add a different header** (or no header) — this prevents `/re-setup` from treating it as auto-generated

```bash
# Example: Replace generated finish-feature.md with custom version
rm .claude/commands/finish-feature.md
cat > .claude/commands/finish-feature.md <<'EOF'
# My Custom Finish Feature Command
[your custom content]
EOF
```

Your custom file will be preserved across future runs of `/re-setup`.

### Safe to Delete & Regenerate

These files contain the `<!-- Generated by /setup-claude -->` marker and can be safely deleted to regenerate from the latest template:

**Command Files (in `.claude/commands/`):**
- `brainstorm.md` — Design exploration
- `write-plan.md` — Plan creation
- `execute-plan.md` — Plan execution
- `plan.md` — Quick planning
- `status.md` — Task status
- `finish-feature.md` — Pre-merge checklist
- `re-setup.md` — Re-run bootstrap

**Doc Files (in `.claude/docs/`):**
- `changelog-guide.md` — CHANGELOG.md guide
- `arch-changelog-guide.md` — Arch log guide

### Regenerating After Deletion

After deleting any of these files, simply run `/re-setup` or use the bootstrap script:

```bash
# Using the Claude Code skill
/re-setup

# Or using the script directly
python3 ~/.claude/skills/setup-claude/scripts/apply_setup_claude.py "$(pwd)"
```

### Never Delete These

**User Content** — These are never auto-generated and should never be deleted:

- `tasks/todo.md` — Your active task list
- `tasks/findings.md` — Your design decisions
- `tasks/progress.md` — Your work log
- `tasks/lessons.md` — Your learned lessons (prevents repeated bugs)
- `CLAUDE.md` — Your project instructions (if custom, has no marker)
- `CHANGELOG.md` — Your release notes

### Template Hash Auto-Detection

As of March 2026, `/re-setup` now **automatically detects when templates have been updated** using template hash comparison. You don't need to manually delete and regenerate files unless you want to reset to defaults or adopt a custom version.

When templates improve (e.g., new guidance in `/finish-feature`), running `/re-setup` will automatically update any generated files that use outdated templates.

---

## Requirements

- [Claude Code CLI](https://claude.ai/code) installed and configured
- [GitHub CLI (`gh`)](https://cli.github.com/) — required for `/finish-feature` PR creation
- Python 3 — required for `/setup-claude` deterministic bootstrap script
- Git — required for `/commit`, `/review`, `/debug`, and `/finish-feature`
- `playwright@claude-plugins-official` plugin — required for browser verification in `/frontend-design`, browser reproduction in `/debug`, and live-page assertion capture in `/write-tests` (Playwright projects only). Enable in Claude Code settings under Plugins.
