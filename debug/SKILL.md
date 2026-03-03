---
name: debug
description: "Structured bug investigation: reproduce, isolate, hypothesize, verify, fix. Logs findings systematically."
---

# Structured Debugging Workflow

## Overview

Systematic bug investigation that follows a disciplined process: reproduce, isolate, hypothesize, verify, fix. Every finding is logged to prevent repeated work and build project knowledge.

<HARD-GATE>
Do NOT jump to fixing code before you understand the bug. No code changes until a hypothesis is CONFIRMED through systematic investigation. Random fixes waste time and mask root causes.
</HARD-GATE>

## Anti-Patterns — Do NOT Do These

- **Changing code before understanding** — Read and analyze first
- **Trying random fixes** — "Maybe if I change this..." is not debugging
- **Ignoring stack traces** — They tell you exactly where to look
- **Fixing symptoms, not causes** — A try/catch around a crash is not a fix
- **Skipping reproduction** — If you can't reproduce it, you can't verify the fix
- **Debugging in production** — Reproduce locally first

## Allowed Tools

Bash, Read, Write, Edit, Glob, Grep, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_console_messages, mcp__plugin_playwright_playwright__browser_network_requests, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_snapshot

## Steps

You MUST complete these steps in order:

### 1. Gather Information

Parse what the user tells you:

- **Error message**: Extract the exact error text
- **Stack trace**: Identify the file, line, and call chain
- **Expected vs actual behavior**: What should happen vs what does happen
- **Trigger conditions**: When does it happen? Always, sometimes, under specific conditions?
- **Recent changes**: Did it work before? What changed?

If the user provides insufficient information, ask specific questions — don't guess.

### 2. Read Project Context

Check for existing knowledge:

```
CLAUDE.md                  — Project conventions, known issues
tasks/findings.md          — Previous debugging sessions, known bugs
tasks/lessons.md           — Patterns that caused issues before
```

**If `tasks/lessons.md` exists, read it in full.** For each active lesson, apply its prevention rule to your investigation — treat lessons as standing constraints, not just history. For example: if a lesson says "always check env vars before checking application code", do that first.

Check if this bug (or something similar) has been investigated before.

### 3. Check Recent Changes

```bash
git log --oneline -10
git diff HEAD~3 --stat
```

Correlate the bug timeline with recent changes. Did the bug start after a specific commit?

### 4. Reproduce the Bug

**Determine the bug surface first:**

#### A. Server / CLI / Non-Browser Bug

Run the specific command, test, or action that triggers the bug. Capture the full output.

```bash
# Run the failing test/command
[specific command that triggers the bug]
```

#### B. Browser / UI Bug

If the bug is visual, involves JavaScript errors, or requires a browser to reproduce, use the Playwright MCP plugin instead of Bash:

1. **Navigate to the page**:
   ```
   mcp__plugin_playwright_playwright__browser_navigate({ url: "http://localhost:[PORT]/[path]" })
   ```

2. **Capture JS errors** (most useful for runtime exceptions):
   ```
   mcp__plugin_playwright_playwright__browser_console_messages({ level: "error" })
   ```

3. **Inspect failed network requests** (useful for API/fetch failures):
   ```
   mcp__plugin_playwright_playwright__browser_network_requests({ includeStatic: false })
   ```

4. **Screenshot the visual state** to document what the bug looks like:
   ```
   mcp__plugin_playwright_playwright__browser_take_screenshot({ type: "png" })
   ```

5. **Capture accessibility snapshot** for structural/DOM-level inspection:
   ```
   mcp__plugin_playwright_playwright__browser_snapshot()
   ```

Use the console errors and network failures as primary evidence in Step 6 (Hypotheses).

---

If you cannot reproduce (either path):
- Check environment differences
- Check for race conditions or timing issues
- Ask the user for exact reproduction steps
- Do NOT proceed to fixing without reproduction

### 5. Isolate the Problem

Read the relevant code, tracing the execution path:

1. Start at the error location (from stack trace)
2. Trace backward through the call chain
3. Identify the inputs and state at each step
4. Find where actual behavior diverges from expected

Use targeted searches:

```bash
# Find related code
grep -r "functionName" src/
grep -r "ERROR_CODE" .
```

### 6. Form Hypotheses

Generate 2-3 ranked hypotheses based on your investigation:

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

Log these to `tasks/findings.md` under a dated heading.

### 7. Test Hypotheses Systematically

For each hypothesis, starting with the most likely:

1. Design a specific diagnostic step (not a fix)
2. Execute it and observe the result
3. Update the hypothesis status: **CONFIRMED** / **REJECTED** / **PARTIAL**

Diagnostic steps might include:
- Adding a temporary log statement to check a value
- Running with different inputs
- Checking database state
- Inspecting environment variables
- Running a minimal reproduction

**Do NOT change production code during this phase.** Diagnostic changes only.

### 8. Update Findings

Update `tasks/findings.md` with results:

```markdown
### [Date] Bug: [brief description]

**Symptom:** [what the user reported]
**Root cause:** [H1/H2/H3 — which was confirmed]
**Evidence:** [what confirmed it]
**Status:** CONFIRMED → fix proposed
```

### 9. Propose Minimal Fix

Once a hypothesis is confirmed, propose the smallest possible fix:

- Change as few lines as possible
- Don't refactor surrounding code
- Don't add "while I'm here" improvements
- Explain why this fix addresses the root cause

Present the fix and **wait for user approval** before applying.

### 10. Verify Fix + Regression Check

After the fix is applied:

1. Re-run the original reproduction steps — bug should be gone
2. Run the full test suite — no new failures
3. If there was a related test, confirm it passes
4. If there was no test, suggest writing one (reference `/write-tests`)

```bash
# Verify the specific fix
[reproduction command]

# Regression check
[test suite command]
```

### 11. Document

**Root cause in `tasks/findings.md`:**
Update the entry from step 8 with the final resolution.

**Lesson in `tasks/lessons.md`** (only if the pattern could recur):

```markdown
### [Date] Lesson: [brief title]
**Bug:** [what happened]
**Root cause:** [why it happened]
**Prevention:** [how to avoid it in the future]
```

Skip the lesson entry if it was a simple typo or one-off mistake.
