---
name: sk:e2e
description: "Run E2E behavioral verification using agent-browser as the final quality gate before finalize. Tests the complete, reviewed, secure implementation from a user's perspective."
---

# /sk:e2e

E2E behavioral verification — the final quality gate before `/sk:finish-feature`. Runs after Review to verify the complete, reviewed, secure implementation works end-to-end from a user's perspective.

**Hard gate:** all scenarios must pass. Zero failures allowed.

## Allowed Tools

Bash, Read, Glob, Grep

## Steps

### 1. Read Context

Read these files to understand what to test:
- `tasks/todo.md` — planned features and acceptance criteria
- `tasks/findings.md` — design decisions and expected behaviors
- `tasks/progress.md` — implementation notes

### 2. Check agent-browser is Available

```bash
agent-browser --version
```

If not found, instruct the user:
```
agent-browser is required. Install it:
  npm install -g agent-browser
  agent-browser install   # downloads Chrome (~100MB)
Then re-run /sk:e2e.
```
Stop if not available.

### 3. Detect Local Server

Determine what URL to test against:
- Check for a dev server command in `package.json` scripts (`dev`, `start`)
- Check for `artisan serve` in Laravel projects (`php artisan serve`)
- Check for `vite` or `next dev`
- If a server is already running (check common ports: 3000, 5173, 8000, 8080), use it
- If no server is running, start one in the background and note the URL

### 4. Locate E2E Test Files

Find E2E test scenarios written during the Write Tests step:
```bash
find . -name "*.e2e.*" -o -name "*.spec.*" | grep -v node_modules
ls tests/e2e/ 2>/dev/null
```

If no E2E test files exist, derive scenarios from `tasks/todo.md` acceptance criteria and `tasks/findings.md`.

### 5. Run E2E Scenarios

For each scenario, use agent-browser following this core pattern:

```bash
# Navigate to the page
agent-browser open <url>

# Get interactive elements (token-efficient ref-based snapshot)
agent-browser snapshot -i

# Interact using @refs (never CSS selectors)
agent-browser click @e1
agent-browser fill @e2 "input value"
agent-browser press Enter

# Use semantic locators when @refs aren't stable
agent-browser find role button
agent-browser find text "Expected Text"
agent-browser find label "Email"

# Assert expected state
agent-browser snapshot   # check content
agent-browser find text "Success Message"
```

**Ref-based interaction is required.** Never use CSS selectors (`#id`, `.class`) — use semantic locators (`find role`, `find text`, `find label`, `find placeholder`) for stability.

For each scenario, record:
- Scenario name
- Steps executed
- Result: PASS or FAIL
- On FAIL: what was expected vs. what was found (include snapshot excerpt)

### 6. Report Results

```
E2E Results:
  PASS  [scenario name]
  PASS  [scenario name]
  FAIL  [scenario name] — expected "X" but found "Y"

Total: X passed, Y failed
```

If all pass → proceed to Fix & Retest Protocol section (no action needed).
If any fail → apply Fix & Retest Protocol.

## Fix & Retest Protocol

When this gate requires a fix, classify it before committing:

**a. Style/config/wording change** (CSS tweak, copy change, selector fix) → commit and re-run `/sk:e2e` (no unit test update needed)

**b. Logic change** (new branch, modified condition, new data path, query change, new function, API change) → trigger protocol:
1. Update or add failing unit tests for the new behavior
2. Re-run `/sk:test` — must pass at 100% coverage
3. Commit (tests + fix together in one commit)
4. Re-run `/sk:e2e` from scratch

**Exception:** Formatter auto-fixes are never logic changes — bypass protocol automatically.

**This gate cannot be skipped.** All scenarios must pass before proceeding to `/sk:update-task`.

## Next Steps

If all scenarios pass:
> "E2E gate clean. Run `/sk:update-task` to mark the task done."

If failures remain after fixes:
> "Re-running /sk:e2e — [N] scenarios still failing."

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:e2e"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
