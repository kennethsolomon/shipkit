---
name: sk:e2e
description: "Run E2E behavioral verification as the final quality gate before finalize. Uses Playwright CLI when E2E spec files already exist; uses agent-browser (accessibility-tree snapshots, no screenshots) for interactive verification when they don't. Tests the complete, reviewed, secure implementation from a user's perspective."
model: sonnet
---

# /sk:e2e

E2E behavioral verification — the final quality gate before `/sk:finish-feature`. Runs after Review. **Hard gate:** all scenarios must pass. Zero failures allowed.

## Allowed Tools

Bash, Read, Glob, Grep

## Steps

### 1. Read Context

Read to understand what to test:
- `tasks/todo.md` — planned features and acceptance criteria
- `tasks/findings.md` — design decisions and expected behaviors
- `tasks/progress.md` — implementation notes

### 2. Detect E2E Runner

> **Token note:** agent-browser uses accessibility tree text snapshots (refs like `@e1`, `@e2`) — no screenshots required. This is 10–20× fewer tokens than screenshot-based verification. Playwright MCP (not CLI) is the screenshot-heavy path; this skill avoids it.

**Priority 1 — Playwright CLI with existing spec files (fastest path)**

```bash
ls playwright.config.ts 2>/dev/null || ls playwright.config.js 2>/dev/null
find e2e tests/e2e -name "*.spec.ts" -o -name "*.spec.js" 2>/dev/null | head -1
```

If config exists AND E2E spec files exist (in `e2e/` or `tests/e2e/`) → use Playwright CLI (Step 3a). Tests are already written — just run them. Advantages: headless Chromium, no screenshots, `webServer` auto-starts dev server.

> **Note:** Unit test spec files (`src/**/*.spec.ts`, Vitest/Jest) do not count — only files under `e2e/` or `tests/e2e/`.

**Config requirements (verify before running):**
- `headless: true` under `use:`
- `channel: undefined` (omit) — NOT `'chrome'` or `'msedge'`
- `webServer.reuseExistingServer: true`

If config has `channel: 'chrome'` or `headless: false`, warn:
> "playwright.config.ts uses system Chrome or headed mode — this may conflict with a running browser. Consider setting `headless: true` and `channel: undefined`."

**Priority 2 — agent-browser (preferred for interactive verification)**

```bash
agent-browser --version
```

Use when: NO spec files exist yet, OR Playwright is not configured. agent-browser's refs system navigates by accessibility tree — no screenshot needed, no DOM fragility.

**Priority 3 — fallback (neither available)**

```
Neither Playwright spec files nor agent-browser found.

Option A (recommended for interactive verification) — agent-browser:
  npm install -g agent-browser
  agent-browser install

Option B (if you prefer spec files) — Playwright:
  npm install -D @playwright/test
  npx playwright install chromium
  # Create playwright.config.ts with headless: true, channel: undefined

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

If spec files exist:
```bash
npx playwright test --reporter=list 2>&1
```

To run a specific file:
```bash
npx playwright test e2e/my-feature.spec.ts --reporter=list
```

**Interpreting results:**
- Exit 0 = all passed; Exit 1 = failures (shows test name, expected vs. actual, screenshot path if `trace: 'on-first-retry'`)

If no spec files exist → derive scenarios from `tasks/todo.md` acceptance criteria, write to `e2e/<feature>.spec.ts`, check `e2e/helpers/` for shared utilities, then run.

Record per test: name/suite, PASS or FAIL, on FAIL: error + snapshot excerpt.

Skip to **Step 5**.

### 3b. Detect Local Server (agent-browser only)

Playwright's `webServer` handles this automatically — only needed for agent-browser.

- Check `package.json` scripts (`dev`, `start`), `artisan serve`, `vite`, `next dev`
- Check common ports: 3000, 5173, 8000, 8080; use existing server or start one in background

### 4. Locate E2E Test Files (agent-browser only)

```bash
find . -name "*.e2e.*" -o -name "*.spec.*" | grep -v node_modules
ls tests/e2e/ 2>/dev/null
```

If none exist, derive scenarios from `tasks/todo.md` and `tasks/findings.md`.

### 4b. Run E2E Scenarios via agent-browser

```bash
agent-browser open <url>
agent-browser snapshot -i              # token-efficient ref-based snapshot
agent-browser click @e1                # use @refs — never CSS selectors
agent-browser fill @e2 "input value"
agent-browser press Enter
agent-browser find role button         # semantic locators when @refs unstable
agent-browser find text "Expected Text"
agent-browser find label "Email"
agent-browser snapshot                 # assert state
agent-browser find text "Success Message"
```

**Use @refs or semantic locators (`find role`, `find text`, `find label`, `find placeholder`). Never CSS selectors.**

Record per scenario: name, steps, PASS/FAIL, on FAIL: expected vs. actual + snapshot excerpt.

Skip to **Step 5**.

### 5. Report Results

```
E2E Runner: Playwright CLI  (or: agent-browser)
E2E Results:
  PASS  [scenario name]
  FAIL  [scenario name] — expected "X" but found "Y"

Total: X passed, Y failed
```

All pass → no action needed. Any fail → apply Fix & Retest Protocol.

## Fix & Retest Protocol

Classify before committing:

| Type | Action |
|------|--------|
| Style/config/wording (CSS, copy, selector) | Include in gate's squash commit, re-run `/sk:e2e`. No user prompt. |
| Logic change (branch, condition, data path, query, function, API) | 1) Update/add failing unit tests 2) `/sk:test` at 100% coverage 3) Commit tests + fix: `fix(e2e): [description]` 4) Re-run `/sk:e2e` from scratch |
| Formatter auto-fixes | Never logic changes — bypass protocol automatically. |

Squash gate commits: collect all fixes, then one commit: `fix(e2e): resolve failing E2E scenarios`.

**This gate cannot be skipped.** All scenarios must pass before `/sk:update-task`.

### Pre-existing Issues

If a bug is found outside the current feature, do NOT fix inline. Log to `tasks/tech-debt.md`:

```
### [YYYY-MM-DD] Found during: sk:e2e
File: path/to/file.ext:line
Issue: description
Severity: critical | high | medium | low
```

Pre-existing bugs don't block this gate unless they affect the current feature's scenarios.

## Next Steps

- All pass: "E2E gate clean. Run `/sk:update-task` to mark the task done." (fixes were auto-committed)
- Failures remain: "Re-running /sk:e2e — [N] scenarios still failing."

---

## Playwright Setup Reference

```bash
npm install -D @playwright/test
npx playwright install chromium
```

Minimal `playwright.config.ts`:

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

E2E helpers go in `e2e/helpers/`. Auth helper pattern:

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

Test credentials in `.env.local` (never hardcoded):
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
