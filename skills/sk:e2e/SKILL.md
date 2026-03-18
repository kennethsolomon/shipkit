---
name: sk:e2e
description: "Run E2E behavioral verification as the final quality gate before finalize. Prefers Playwright CLI when playwright.config.ts is detected; falls back to agent-browser otherwise. Tests the complete, reviewed, secure implementation from a user's perspective."
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

### 2. Detect E2E Runner

Check which runner is available, in priority order:

**Priority 1 — Playwright (preferred)**

```bash
ls playwright.config.ts 2>/dev/null || ls playwright.config.js 2>/dev/null
```

If a Playwright config exists → use Playwright CLI (Step 3a). This is the preferred path because:
- Uses headless Chromium (no conflict with system Chrome)
- No additional global install required (`@playwright/test` in devDeps)
- Test files in `e2e/` or `tests/e2e/` are picked up automatically
- `webServer` in `playwright.config.ts` auto-starts the dev server

**Playwright config requirements** (verify before running):
- `headless: true` must be set under `use:`
- `channel: undefined` (or omitted) — must NOT be `'chrome'` or `'msedge'` to avoid system browser conflicts
- `webServer.reuseExistingServer: true` — avoids double-starting the dev server

If config has `channel: 'chrome'` or `headless: false`, warn:
> "playwright.config.ts uses system Chrome or headed mode — this may conflict with a running browser. Consider setting `headless: true` and `channel: undefined`."

**Priority 2 — agent-browser (fallback)**

```bash
agent-browser --version
```

Only use `agent-browser` if NO `playwright.config.ts` / `playwright.config.js` exists.

If `agent-browser` is also not found, AND no Playwright config exists:

```
Neither Playwright nor agent-browser is configured. To fix permanently:

Option A (recommended) — Playwright:
  npm install -D @playwright/test
  npx playwright install chromium
  # Create playwright.config.ts with headless: true, channel: undefined

Option B — agent-browser:
  npm install -g agent-browser
  agent-browser install

Then re-run /sk:e2e.
```
Stop if neither runner is available.

### 3a. Run E2E via Playwright CLI

Locate test files:
```bash
ls e2e/ 2>/dev/null
ls tests/e2e/ 2>/dev/null
find . -name "*.spec.ts" -not -path "*/node_modules/*"
```

If spec files exist, run them:
```bash
npx playwright test --reporter=list
```

To run a specific file:
```bash
npx playwright test e2e/my-feature.spec.ts --reporter=list
```

To run with visible output on failure:
```bash
npx playwright test --reporter=list 2>&1
```

**Interpreting results:**
- Exit code 0 = all tests passed
- Exit code 1 = one or more tests failed (output includes which tests and why)
- Each failing test shows: test name, expected vs. actual, screenshot path (if `trace: 'on-first-retry'` is set)

If no spec files exist → derive scenarios from `tasks/todo.md` acceptance criteria and write them to `e2e/<feature>.spec.ts` before running. Follow the test file patterns already present in the project (check `e2e/helpers/` for shared utilities).

After running, record for each test:
- Test name / suite
- Result: PASS or FAIL
- On FAIL: error message and relevant snapshot

Skip to **Step 5 (Report Results)**.

### 3b. Detect Local Server (agent-browser path only)

Only needed if using agent-browser (Playwright's `webServer` handles this automatically).

Determine what URL to test against:
- Check for a dev server command in `package.json` scripts (`dev`, `start`)
- Check for `artisan serve` in Laravel projects (`php artisan serve`)
- Check for `vite` or `next dev`
- If a server is already running (check common ports: 3000, 5173, 8000, 8080), use it
- If no server is running, start one in the background and note the URL

### 4. Locate E2E Test Files (agent-browser path only)

Find E2E test scenarios written during the Write Tests step:
```bash
find . -name "*.e2e.*" -o -name "*.spec.*" | grep -v node_modules
ls tests/e2e/ 2>/dev/null
```

If no E2E test files exist, derive scenarios from `tasks/todo.md` acceptance criteria and `tasks/findings.md`.

### 4b. Run E2E Scenarios via agent-browser

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

### 5. Report Results

```
E2E Runner: Playwright CLI  (or: agent-browser)
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

## Playwright Setup Reference

When setting up Playwright for the first time in a project:

```bash
npm install -D @playwright/test
npx playwright install chromium
```

Minimal `playwright.config.ts` (headless, no system Chrome conflict):

```ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: 'list',
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL ?? 'http://localhost:3000',
    headless: true,          // REQUIRED — avoids system Chrome conflict
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], channel: undefined }, // REQUIRED — use Playwright's Chromium, not system Chrome
    },
  ],
  webServer: {
    command: 'npm run dev',  // or 'php artisan serve', 'yarn dev', etc.
    url: 'http://localhost:3000',
    reuseExistingServer: true,
    timeout: 120_000,
  },
})
```

E2E test helpers go in `e2e/helpers/`. Auth helper pattern:

```ts
// e2e/helpers/auth.ts
import { Page } from '@playwright/test'

export async function signIn(page: Page, email: string, password: string) {
  await page.goto('/login')
  await page.getByLabel(/email/i).fill(email)
  await page.getByLabel(/password/i).fill(password)
  await page.getByRole('button', { name: /sign in|log in/i }).click()
  await page.waitForURL('/dashboard', { timeout: 15_000 })
}

export const TEST_USERS = {
  regular: {
    email: process.env.E2E_USER_EMAIL ?? '',
    password: process.env.E2E_USER_PASSWORD ?? '',
  },
  admin: {
    email: process.env.E2E_ADMIN_EMAIL ?? '',
    password: process.env.E2E_ADMIN_PASSWORD ?? '',
  },
}
```

Test credentials go in `.env.local` (never hardcoded):
```
E2E_USER_EMAIL=...
E2E_USER_PASSWORD=...
E2E_ADMIN_EMAIL=...
E2E_ADMIN_PASSWORD=...
```

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
