---
name: sk:debug
description: "Structured bug investigation: reproduce, isolate, hypothesize, verify, fix. Logs findings systematically."
---

# Structured Debugging Workflow

<HARD-GATE>
Do NOT jump to fixing code before you understand the bug. No code changes until a hypothesis is CONFIRMED through systematic investigation. Random fixes waste time and mask root causes.
</HARD-GATE>

## Anti-Patterns

- Changing code before understanding — read and analyze first
- Trying random fixes — "maybe if I change this..." is not debugging
- Ignoring stack traces — they tell you exactly where to look
- Fixing symptoms, not causes — a try/catch around a crash is not a fix
- Skipping reproduction — if you can't reproduce it, you can't verify the fix
- Debugging in production — reproduce locally first

## Allowed Tools

Agent, Bash, Read, Write, Edit, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_console_messages, mcp__plugin_playwright_playwright__browser_network_requests, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_snapshot

## Agent Delegation

Delegate investigation to the **`debugger` agent**. Provide full problem context:

```
Task: "Investigate this bug: [error message / symptom].
Expected: [what should happen]. Actual: [what happens].
Trigger: [when does it occur].
Recent changes: [any commits near the bug onset].
Follow the reproduce → isolate → hypothesize → verify → fix protocol.
Log findings to tasks/findings.md."
```

The `debugger` agent handles the full investigation (steps 1–10 below) autonomously. After it completes:
- Review `tasks/findings.md` for root cause and proposed fix
- If fix is approved, proceed with the Bug Fix Flow: branch → write-tests → implement → gates

If `debugger` agent hits a 3-strike failure, fall back to manual steps below.

---

## Steps

Complete these steps in order:

### 1. Gather Information

Parse what the user tells you:

- **Error message** — exact error text
- **Stack trace** — file, line, and call chain
- **Expected vs actual** — what should happen vs what does happen
- **Trigger conditions** — always, sometimes, under specific conditions?
- **Recent changes** — did it work before? what changed?

If insufficient information, ask specific questions — don't guess.

### 2. Read Project Context

```
CLAUDE.md               — project conventions, known issues
tasks/findings.md       — previous debugging sessions, known bugs
tasks/lessons.md        — patterns that caused issues before
tasks/progress.md       — recent work log and error log
```

**If `tasks/lessons.md` exists, read it in full.** For each active lesson, apply its prevention rule — treat lessons as standing constraints, not just history.

**If `tasks/progress.md` exists**, scan the Error Log for failures near the bug's reported time — they often share a root cause.

### 3. Check Recent Changes

```bash
git log --oneline -10
git diff HEAD~3 --stat
```

Correlate the bug timeline with recent changes. Did the bug start after a specific commit?

### 4. Reproduce the Bug

**A. Server / CLI / Non-Browser Bug** — run the specific command, test, or action that triggers the bug. Capture the full output.

**B. Browser / UI Bug** — use the Playwright MCP plugin:

1. Navigate: `mcp__plugin_playwright_playwright__browser_navigate({ url: "http://localhost:[PORT]/[path]" })`
2. JS errors: `mcp__plugin_playwright_playwright__browser_console_messages({ level: "error" })`
3. Network failures: `mcp__plugin_playwright_playwright__browser_network_requests({ includeStatic: false })`
4. Screenshot: `mcp__plugin_playwright_playwright__browser_take_screenshot({ type: "png" })`
5. DOM snapshot: `mcp__plugin_playwright_playwright__browser_snapshot()`

Use console errors and network failures as primary evidence in Step 6.

If you cannot reproduce (either path): check environment differences, check for race conditions, ask for exact reproduction steps. Do NOT proceed to fixing without reproduction.

### 5. Isolate the Problem

Read the relevant code, tracing the execution path:

1. Start at the error location (from stack trace)
2. Trace backward through the call chain
3. Identify inputs and state at each step
4. Find where actual behavior diverges from expected

### 6. Form Hypotheses

Generate 2-3 ranked hypotheses and log to `tasks/findings.md`:

```markdown
## Hypotheses

### H1: [Most likely] Description
- Evidence: what supports this
- Test: how to confirm or reject

### H2: [Alternative] Description
- Evidence: what supports this
- Test: how to confirm or reject

### H3: [Less likely] Description
- Evidence: what supports this
- Test: how to confirm or reject
```

### 7. Test Hypotheses Systematically

For each hypothesis (most likely first):

1. Design a specific diagnostic step (not a fix)
2. Execute it and observe the result
3. Update status: **CONFIRMED** / **REJECTED** / **PARTIAL**

Diagnostic steps: add a temporary log statement, run with different inputs, check database state, inspect environment variables, run a minimal reproduction.

**Do NOT change production code during this phase.** Diagnostic changes only.

### 8. Update Findings

Update `tasks/findings.md`:

```markdown
### [Date] Bug: [brief description]

**Symptom:** [what the user reported]
**Root cause:** [H1/H2/H3 — which was confirmed]
**Evidence:** [what confirmed it]
**Status:** CONFIRMED → fix proposed
```

### 9. Propose Minimal Fix

Once a hypothesis is confirmed, propose the smallest possible fix — change as few lines as possible, don't refactor surrounding code, don't add "while I'm here" improvements. Explain why the fix addresses the root cause.

**Wait for user approval before applying.**

### 10. Verify Fix + Regression Check

```bash
# Verify the specific fix
[reproduction command]

# Regression check
[test suite command]
```

1. Re-run the original reproduction steps — bug should be gone
2. Run the full test suite — no new failures
3. If there was a related test, confirm it passes
4. If there was no test, suggest writing one (reference `/sk:write-tests`)

### 11. Document

**`tasks/findings.md`** — update the entry from step 8 with the final resolution.

**`tasks/lessons.md`** (only if the pattern could recur):

```markdown
### [Date] Lesson: [brief title]
**Bug:** [what happened]
**Root cause:** [why it happened]
**Prevention:** [how to avoid it in the future]
```

Skip the lesson entry if it was a simple typo or one-off mistake.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:debug"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | sonnet |
| `budget` | sonnet |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
