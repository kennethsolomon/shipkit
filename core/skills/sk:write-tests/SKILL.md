---
name: sk:write-tests
description: "TDD: Auto-detect BE + FE testing stacks, write failing tests before implementation. Updates existing tests when behavior changes."
---

# Test Generation (TDD)

Auto-detect backend AND frontend testing frameworks, read `tasks/todo.md`, write comprehensive failing tests BEFORE implementation. Tests define expected behavior — implementation makes them pass.

> **Requirements changed mid-workflow?** Run `/sk:change` first. Never update tests based on a changed requirement without going through `/sk:change` first.

## Allowed Tools

Bash, Read, Write, Edit, Glob, Grep

**When detected framework is `@playwright/sk:test`**, also use:
mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_take_screenshot

## Steps (complete in order)

### 0. Check Project Lessons

If `tasks/lessons.md` exists, read it first. Apply every active lesson as a standing constraint. Look for: flaky test patterns, mocking approaches that caused issues, framework-specific gotchas, file location conventions that broke.

### 1. Read the Plan

Read `tasks/todo.md` (source of truth for what to test) and `tasks/progress.md` for brainstorm/design context. Identify all code to be created or modified.

### 2. Detect ALL Testing Frameworks

**Backend:**
```bash
cat composer.json 2>/dev/null   # PHPUnit / Pest
cat pyproject.toml 2>/dev/null  # pytest
cat go.mod 2>/dev/null          # Go testing
cat Cargo.toml 2>/dev/null      # Rust #[cfg(test)]
cat Gemfile 2>/dev/null         # RSpec / Minitest
cat build.gradle 2>/dev/null    # JUnit
```

**Frontend:**
```bash
cat package.json 2>/dev/null    # Jest, Vitest, Mocha, Cypress, Playwright
```

Check for config files: `vitest.config.ts`, `jest.config.js`, `phpunit.xml`, `pytest.ini`, `conftest.py`, `cypress.config.ts`, `playwright.config.ts`.

Report all detected frameworks:
```
Backend:  [framework] ([language]) — [test runner command]
Frontend: [framework] ([language]) — [test runner command]
```

If only one stack exists, report that and proceed.

### 3. Check Existing Tests

Find tests related to code being changed. If modifying existing behavior: update those tests first to expect the new behavior. Report: "Updating X existing test files, creating Y new test files."

### 4. Learn Project Test Conventions

Read 1–2 existing test files per stack. Learn: import style, test structure, assertion library, mocking approach, setup/teardown, file naming, file location. If no existing tests, use `references/patterns.md`.

### 5. Analyze Target Code from Plan

**Backend test cases:**
- Happy path, edge cases (empty/boundary/null), error handling, authorization, validation

**Frontend test cases:**
- Component rendering, user interactions, conditional rendering, error/loading/empty states, form handling

### 6. Determine Test File Locations

| Convention | Pattern | Example |
|---|---|---|
| Co-located | Same dir as source | `src/auth/login.test.ts` |
| Mirror `tests/` | Parallel structure | `tests/auth/login.test.ts` |
| `__tests__/` | Jest/Vitest | `src/auth/__tests__/login.test.ts` |
| `test_` prefix | Python | `tests/test_login.py` |
| `_test` suffix | Go | `auth/login_test.go` |
| `tests/Feature/` + `tests/Unit/` | Laravel/Pest | `tests/Feature/ServerTest.php` |

### 7. Write Backend Test Files

- One test per behavior, not per line of code
- Descriptive names that explain expected behavior
- Arrange-Act-Assert pattern
- Mock external dependencies, not the code under test
- Test behavior, not implementation details

### 8. Write Frontend Test Files

If a frontend stack was detected: component tests, page tests, hook tests, mock framework helpers (Inertia `useForm`, Next.js `useRouter`, SvelteKit `goto`). Use `@testing-library` conventions: prefer `getByRole`, `getByText`, `getByLabelText`. Skip if no FE stack.

### 8b. Write E2E Spec Files (conditional)

**Only if `playwright.config.ts` or `playwright.config.js` is in the project root.**

Write `e2e/<feature>.spec.ts` files covering acceptance criteria from `tasks/todo.md`:
- Use `test.describe` / `test` blocks (not `describe`/`it`)
- Role-based locators only: `getByRole`, `getByLabel`, `getByText`, `getByPlaceholder` — never CSS selectors
- `test.beforeEach` for shared setup (auth, navigation)
- `test.skip(!email, 'ENV_VAR not set — skipping')` guards for credential-dependent tests
- Auth credentials from env vars via `e2e/helpers/auth.ts` — never hardcode
- Soft assertions (`expect.soft`) for non-critical checks; hard `expect` for gate conditions

```ts
import { test, expect } from '@playwright/test'
import { signIn, TEST_USERS } from './helpers/auth'

test.describe('[Feature] — [scenario]', () => {
  test.beforeEach(async ({ page }) => {
    const { email, password } = TEST_USERS.regular
    test.skip(!email, 'E2E_USER_EMAIL not set — skipping')
    await signIn(page, email, password)
  })

  test('[behavior description]', async ({ page }) => {
    await page.goto('/dashboard/feature')
    await expect(page.getByRole('heading', { name: /title/i })).toBeVisible()
  })
})
```

Create `e2e/helpers/auth.ts` if it doesn't exist (see `/sk:e2e` Playwright Setup Reference).

Run to confirm RED phase:
```bash
npx playwright test e2e/<feature>.spec.ts --reporter=list
```

### 8c. Playwright MCP Inspection (optional)

Only if Playwright MCP plugin is active AND live selectors are needed: navigate to target URL, capture accessibility snapshot, screenshot for visual reference.

### 9. Verify Tests Fail (Red Phase)

Run both suites. Tests SHOULD fail — this confirms they test the right thing. If tests pass without implementation, rewrite them. Report which tests fail and why.

### 10. Report

```
BE tests written: X tests in Y files ([framework])
FE tests written: X tests in Y files ([framework])  ← omit if no FE stack
E2E specs written: X tests in Y files (Playwright)  ← omit if no playwright.config.ts
Existing tests updated: X files
Status: RED (tests fail as expected — ready for implementation)
```

## Key Principle

Tests define **expected behavior**. Implementation makes them pass. If unsure what code should do, the test is where you decide.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:write-tests"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
