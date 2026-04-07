---
name: sk:autopilot
description: Hands-free workflow — runs all 8 phases (including scope check, learn, retro) with auto-skip, auto-advance, auto-commit. Stops only for direction approval, 3-strike failures, and PR push.
allowed-tools: Read, Write, Bash, Glob, Grep, Agent, Skill
---

# Autopilot Mode

Hands-free workflow that executes all 8 phases (including scope check, learn, and retro) of the ShipIt workflow with minimal interruptions. Same quality gates, same fix loops, same 100% coverage — just fewer stops.

## When to Use

- You know roughly what you want built and trust the workflow to handle details
- You want to minimize context switches and manual step advancement
- The task is well-defined enough for a single direction-approval checkpoint

## When NOT to Use

- Exploratory work where you want to steer each step
- Tasks requiring frequent design decisions mid-implementation
- When you want to review intermediate outputs before proceeding

## Quality Guarantee

Autopilot runs the EXACT same workflow as manual mode (8 phases + optional pre-phases: investigate, explore, design, plan, branch, implement + scope check, commit, gates, ship + learn + retro):
- ALL quality gates enforced (lint, test, security, perf, review, e2e)
- ALL fix-rerun loops active
- 100% test coverage required on new code
- 0 security issues required
- The ONLY difference: auto-advance between steps instead of stopping

## Steps

### 0. Task Classification (silent, auto — no user prompt)

Before loading context, classify the input to route any pre-processing.

**Check A — Bug with unknown root cause:**
Signals: prompt contains `bug`, `error`, `broken`, `crash`, `failing`, `not working`, `issue`, `unexpected behavior`, `regression`
AND no known-cause anchors: no `file:line`, no `"the issue is"`, no specific error code pointing to a cause, no function name + symptom pair.

Examples: "something is broken with auth", "payments failing intermittently", "dashboard is slow and I don't know why"

If matched:
→ Log: `[Autopilot] Bug with unknown root cause — running /sk:deep-dive to investigate.`
→ Invoke `Skill("sk:deep-dive")` with the original task description
→ Deep-dive writes `tasks/spec.md` with root cause + fix scope
→ Continue with bug fix flow: branch (step 4) → write-tests → execute-plan → commit → gates → finalize
→ Skip steps 1–3 (brainstorm/design/plan are replaced by the spec)

**Check B — Vague feature or improvement:**
No bug signals from Check A, AND no concrete anchors:
- No file paths, no function/method names, no specific error messages
- Open-ended verbs: `improve`, `enhance`, `make better`, `add features`, `build`, `clean up`, `refactor`
- References a system area without scope: "the auth system", "the dashboard", "notifications"

If matched:
→ Log: `[Autopilot] Open-ended request — running /sk:deep-interview to clarify requirements.`
→ Invoke `Skill("sk:deep-interview")` with the original task description
→ Deep-interview writes `tasks/spec.md`
→ Continue to Step 0.5 (investigate) — do not skip Check C's logic, fall through

**Check C — Clear input (default):**
Has concrete anchors OR is a specific bounded request.
→ Fall through to Step 0.5 — no log, no deep-interview.

---

### 0.5. Investigate (auto-skip unless unfamiliar area)

**Auto-skip rule:** Skip this step if ANY is true:
- Task description contains concrete anchors (file paths like `app/Models/User.php`, function names with symptom, line numbers)
- Check A matched (bug flow — deep-dive handles its own investigation)
- Repo is greenfield (no `package.json` / `composer.json` / `go.mod` / `Cargo.toml` detected)
- User passed `--skip-investigate` via `/sk:start`
- `tasks/investigation.md` already exists and was written within the last 4 hours for this same task

Otherwise, check for unfamiliar-area signals:
- References to subsystems: "the billing module", "our auth flow", "the webhook system", "the dashboard", "the notifications area"
- Exploration verbs: `add to`, `extend`, `modify`, `touch`, `work on`, `how does`, `explore`, `figure out`, `map out`

If unfamiliar-area signals match AND auto-skip rule did not fire:
→ Log: `[Autopilot] Existing-area task — running /sk:investigate to map terrain.`
→ Invoke `Skill("sk:investigate")` with the original task description
→ Investigate writes `tasks/investigation.md` (read-only exploration — no code changes)
→ Continue to Step 1 (brainstorm reads investigation.md + spec.md automatically)

If no unfamiliar-area signals:
→ Log: `Auto-skipped: Investigate (task has concrete anchors or is greenfield)` — silent if no signals at all
→ Proceed to Step 1

---

### 1. Load Context + Brainstorm + Direction Approval (STOP — requires user input)

- Read `tasks/todo.md`, `tasks/lessons.md`, `tasks/findings.md`, `tasks/tech-debt.md`
- Run brainstorm internally (3 parallel Explore agents)
- Propose 2-3 approaches with trade-offs

**Present ONE direction summary and ask:**
> "Direction: [1-2 sentence summary of chosen approach]
> Scope: [what will be built/changed]
> Acceptance Criteria:
>   - [ ] [criterion 1 — testable, specific]
>   - [ ] [criterion 2]
>   - [ ] [criterion 3]
> Auto-skipping: [list of steps that will be auto-skipped and why]
> Proceed? (y/n)"

Wait for explicit `y` before continuing. This is the ONLY planning stop.

### 2. Design (auto-skip if no frontend/API keywords)

Run `/sk:frontend-design` or `/sk:api-design` if applicable. Auto-skip if no frontend/API keywords detected. Log: `Auto-skipped: Design ([reason])`

### 3. Plan (auto-advance)

Write the implementation plan to `tasks/todo.md`. Do NOT ask for plan approval — the direction approval in step 1 covers this.

### 4. Branch (auto-advance)

Create feature branch auto-named from the task. Do NOT ask for confirmation.

### 5. Write Tests + Implement (auto-advance)

- Run `/sk:write-tests` (TDD red phase)
- Run `/sk:schema-migrate` if database keywords detected
- Run `/sk:execute-plan` (TDD green phase)
- Auto-advance when done

### 5.5. Scope Check (auto-advance)

Run `/sk:scope-check` to compare the implementation against `tasks/todo.md`.

- If scope creep detected: log findings, trim the excess, re-commit
- If on-scope: auto-advance silently

### 6. Commit (auto-commit)

Auto-commit with conventional commit format. Do NOT ask for commit message approval.
Format: `type(scope): description`

### 7. Gates (auto-advance on clean pass)

Run all quality gates via `/sk:gates`:
1. Lint + deps-audit (CVE scan, license compliance, outdated packages)
2. Security (0 issues)
3. Performance (if not auto-skipped)
4. Test (100% coverage)
5. Review + simplify
6. E2E

Each gate auto-fixes and re-runs internally. Squash gate commits — one commit per gate pass.

### 7.5. Verify Acceptance Criteria (auto)

Before the PR push stop, verify each acceptance criterion defined in step 1:
- Run the relevant test, command, or check for each criterion
- Mark ✓ passing or ✗ failing
- All must be ✓ before proceeding to step 8
- If any ✗: fix → re-run `/sk:gates` (step 7) → re-verify criteria

Log result: `[Autopilot] Acceptance criteria: X/X passed.`

### 8. PR Push (STOP — requires user confirmation)

**This is the second mandatory stop.** Present:
> "All gates passed. Ready to create PR.
> Title: [conventional format]
> Changes: [file count] files, [line count] lines
> Confirm push + PR? (y/n)"

Wait for explicit confirmation — pushing is visible to others.

After confirmation:
- Create PR
- Sync features (`/sk:features`)
- Ask about release (never auto-skipped)

### 8.5. Learn (auto-advance)

Run `/sk:learn` to extract reusable patterns from this session.

- Patterns are saved to `~/.claude/skills/learned/` automatically
- Auto-advance after saving — no confirmation needed in autopilot

### 8.6. Retro (auto-advance)

Run `/sk:retro` to capture velocity, blockers, and action items for this feature.

- Output is brief — 3-5 bullets covering what went well, what slowed down, and next actions
- Appended to `tasks/progress.md`

## 3-Strike Protocol

If any step fails 3 times:
- **STOP immediately**
- Report: what failed, what was tried, error details
- Ask user for guidance before continuing
- This overrides auto-advance — 3 strikes always stops

## Stops Summary

| Stop | When | Why |
|------|------|-----|
| Direction approval | After brainstorm (step 1) | User must approve the approach |
| 3-strike failure | Any step fails 3x | Needs human judgment |
| PR push | Before creating PR (step 8) | Visible to others — always confirm |
| Release | After step 8.6 | Never auto-skipped — always ask |

Everything else auto-advances.

## Intensity Routing

Read `.shipkit/config.json` for the `intensity` field (default: `full`) and `intensity_overrides` map.

**Resolution order:** `intensity_overrides["sk:<phase>"]` → phase auto-select (below) → global `intensity` → `full`.

Autopilot auto-selects intensity per phase for optimal output:

| Phase | Auto-selected | Why |
|-------|--------------|-----|
| investigate (step 0.5) | lite | Factual mapping — tables and lists, not essays |
| brainstorm (step 1) | full | Need substance for direction approval |
| design (step 2) | full | Design decisions need clarity |
| write-plan (step 3) | full | Plans must be decision-complete |
| write-tests (step 5) | lite | Tests are code — minimal prose |
| execute-plan (step 5) | lite | Implementation — minimal prose |
| scope-check (step 5.5) | lite | Pass/fail comparison |
| gates (step 7) | lite | Pass/fail, not essays |
| review (step 7, batch 3) | deep | Security/perf findings need full detail |
| finalize (step 8) | full | PR descriptions need clarity |
| learn (step 8.5) | lite | Pattern extraction — concise |
| retro (step 8.6) | lite | Bullets, not paragraphs |

**Intensity levels:**

| Level | Behavior |
|-------|----------|
| **lite** | No filler/hedging. Keep articles + full sentences. Professional but tight. |
| **full** | Standard output. Clear, complete explanations. Default. |
| **deep** | Exhaustive analysis. Include edge cases, alternatives, and reasoning. No shortcuts. |

User can override globally (`"intensity": "lite"` in config) or per-skill (`"intensity_overrides": {"sk:review": "deep"}`).

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:autopilot"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit. When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
