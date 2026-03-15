---
name: sk:write-tests
description: "TDD: Auto-detect BE + FE testing stacks, write failing tests before implementation. Updates existing tests when behavior changes."
---

# Test Generation (TDD)

## Overview

Auto-detect the project's backend AND frontend testing frameworks, read the plan from `tasks/todo.md`, and write comprehensive failing tests BEFORE implementation. Tests define the expected behavior — implementation makes them pass.

## Allowed Tools

Bash, Read, Write, Edit, Glob, Grep

**When the detected framework is `@playwright/sk:test`**, also use:
mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_run_code, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_take_screenshot

## Steps

You MUST complete these steps in order:

### 0. Check Project Lessons

If `tasks/lessons.md` exists, read it before doing anything else. Apply every active lesson as a standing constraint. Look for:
- Known flaky test patterns in this project
- Mocking approaches that caused issues before
- Framework-specific gotchas
- File location conventions that broke in the past

### 1. Read the Plan

- Read `tasks/todo.md` to understand what will be implemented
- Read `tasks/progress.md` for context from brainstorm/design steps
- Identify all code that will be created or modified
- This is the **source of truth** for what tests to write

### 2. Detect ALL Testing Frameworks

Scan for **both backend and frontend** testing stacks:

**Backend detection:**
```bash
cat composer.json 2>/dev/null       # PHPUnit / Pest
cat pyproject.toml 2>/dev/null      # pytest
cat go.mod 2>/dev/null              # Go testing
cat Cargo.toml 2>/dev/null          # Rust #[cfg(test)]
cat Gemfile 2>/dev/null             # RSpec / Minitest
cat build.gradle 2>/dev/null        # JUnit
```

**Frontend detection:**
```bash
cat package.json 2>/dev/null        # Jest, Vitest, Mocha, Cypress, Playwright
```

Check for framework-specific config:
- `vitest.config.ts` / `vite.config.ts` (Vitest)
- `jest.config.js` / `jest.config.ts` (Jest)
- `phpunit.xml` / `pest` in composer.json (PHPUnit / Pest)
- `pytest.ini` / `conftest.py` (pytest)
- `cypress.config.ts` (Cypress)
- `playwright.config.ts` (Playwright)

Report ALL detected frameworks:
```
Backend:  [framework] ([language]) — [test runner command]
Frontend: [framework] ([language]) — [test runner command]
```

If only one stack exists (e.g., API-only with no FE, or FE-only SPA), report that and proceed with what's available.

### 3. Check Existing Tests

- Find existing tests related to the code being changed
- If modifying existing behavior: **update those tests first** to expect the new behavior
- If adding new code: identify what test files need to be created
- Report: "Updating X existing test files, creating Y new test files"

### 4. Learn Project Test Conventions

Find and read 1-2 existing test files **per stack** to learn patterns:

From existing tests, learn:
- Import style and aliases
- Test structure (describe/it, test(), func TestX)
- Assertion library and patterns
- Mocking approach
- Setup/teardown patterns
- File naming convention
- Test file location (co-located vs `tests/` directory)

If **no existing tests** are found, use `references/patterns.md` for framework-appropriate templates.

### 5. Analyze Target Code from Plan

Based on the plan in `tasks/todo.md`, identify test cases for each piece of planned code:

**Backend tests:**
- **Happy path**: Normal expected behavior for each endpoint/function
- **Edge cases**: Empty inputs, boundary values, null/undefined
- **Error handling**: Invalid inputs, thrown exceptions, error responses
- **Authorization**: Ensure policies/guards are tested
- **Validation**: All form request / input validation rules

**Frontend tests:**
- **Component rendering**: Correct output for given props
- **User interactions**: Click, type, submit, navigate
- **Conditional rendering**: Show/hide based on state
- **Error states**: Loading, empty, error displays
- **Form handling**: Validation, submission, reset

### 6. Determine Test File Locations

Follow the project's existing convention:

| Convention | Pattern | Example |
|-----------|---------|---------|
| Co-located | Same directory as source | `src/auth/login.test.ts` |
| Mirror `tests/` | Parallel directory structure | `tests/auth/login.test.ts` |
| `__tests__/` | Jest/Vitest convention | `src/auth/__tests__/login.test.ts` |
| `test_` prefix | Python convention | `tests/test_login.py` |
| `_test` suffix | Go convention | `auth/login_test.go` |
| `tests/Feature/` + `tests/Unit/` | Laravel/Pest convention | `tests/Feature/ServerTest.php` |

### 7. Write Backend Test Files

Generate complete test files matching the project's style:
- One test per behavior, not per line of code
- Descriptive test names that explain expected behavior
- Arrange-Act-Assert pattern
- Mock external dependencies, not the code under test
- Test behavior, not implementation details

### 8. Write Frontend Test Files

If a frontend stack was detected, generate FE test files:
- Component tests for every new/modified component
- Page tests for every new/modified page
- Hook tests for custom hooks
- Mock framework helpers (e.g., Inertia's `useForm`, Next.js `useRouter`, SvelteKit `goto`)
- Use `@testing-library` conventions: prefer `getByRole`, `getByText`, `getByLabelText`

Skip this step if no FE stack was detected.

### 8b. Playwright-Specific (conditional)

**Only if `@playwright/sk:test` is detected:**

Use the Playwright MCP plugin to inspect live page state for more accurate selectors:

1. Navigate to target URL
2. Capture accessibility snapshot for role-based selectors
3. Screenshot for visual reference
4. Optionally run inline assertions for complex interactions

### 9. Verify Tests Fail (Red Phase)

Run both suites to confirm tests fail as expected:

- **Tests SHOULD fail** — this confirms they're testing the right thing
- If tests pass without implementation, they're not testing anything useful — rewrite them
- Report which tests fail and why (missing class, missing route, missing component, etc.)

### 10. Report

Output:
```
BE tests written: X tests in Y files ([framework])
FE tests written: X tests in Y files ([framework])  ← omit if no FE stack
Existing tests updated: X files
Status: RED (tests fail as expected — ready for implementation)
```

## Key Principle

Tests define the **expected behavior**. Implementation makes them pass. If you're unsure what a piece of code should do, the test is where you decide.

---

## Model Routing

Read `.shipkit/sk:config.json` from the project root if it exists.

- If `model_overrides["sk:write-tests"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | sonnet |
| `balanced` | sonnet |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
