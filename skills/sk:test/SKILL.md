---
name: sk:test
description: "Auto-detect BE + FE test runners, run both in parallel, verify 100% coverage on new code, fix failures and re-run until all pass."
---

# Test Verification

## Overview

Auto-detect the project's backend and frontend testing frameworks from config files, run all suites in parallel, and verify 100% coverage on new code. This is the **verification step** (TDD green check) — tests should already exist from `/sk:write-tests`. This skill does NOT write tests.

## Allowed Tools

Bash, Read, Glob, Grep

## Steps

You MUST complete these steps in order:

### 0. Check Project Lessons

If `tasks/lessons.md` exists, read it before doing anything else. Apply every active lesson as a standing constraint. Look for:
- Known flaky tests in this project
- Environment-specific runner issues
- Coverage tool quirks

### 1. Detect Testing Frameworks

Scan for **all** testing stacks by checking config files:

**Backend detection:**
```bash
cat composer.json 2>/dev/null    # Pest / PHPUnit
cat pyproject.toml 2>/dev/null   # pytest
cat go.mod 2>/dev/null           # Go testing
cat Cargo.toml 2>/dev/null       # Rust cargo test
```

**Frontend detection:**
```bash
cat package.json 2>/dev/null     # Vitest / Jest
```

**Detection table:**

| Config file | Indicator | Runner | Command |
|-------------|-----------|--------|---------|
| `composer.json` | `pestphp/pest` in require-dev | Pest | `./vendor/bin/pest --coverage --compact` |
| `composer.json` | `phpunit/phpunit` (no Pest) | PHPUnit | `./vendor/bin/phpunit --coverage-text` |
| `package.json` | `vitest` in devDependencies | Vitest | `npx vitest run --coverage` |
| `package.json` | `jest` in devDependencies | Jest | `npx jest --coverage` |
| `pyproject.toml` | `pytest` in dependencies | pytest | `python -m pytest --cov` |
| `go.mod` | present | Go test | `go test -cover ./...` |
| `Cargo.toml` | present | cargo test | `cargo test` |

Report what was detected:
```
Backend:  [runner] — [command]
Frontend: [runner] — [command]
```

If only one stack exists, report that and proceed with what is available.

### 2. Setup Vitest (conditional)

**Only if Vitest is detected but not yet configured** (no `vitest.config.ts` exists):

Install dependencies:
```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitejs/plugin-react @vitest/coverage-v8
```

Create `vitest.config.ts`:
```ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    test: {
        environment: 'jsdom',
        globals: true,
        setupFiles: ['./resources/js/__tests__/setup.ts'],
        include: ['resources/js/__tests__/**/*.{test,spec}.{ts,tsx}'],
        coverage: {
            provider: 'v8',
            include: ['resources/js/**/*.{ts,tsx}'],
            exclude: ['resources/js/__tests__/**', 'resources/js/types/**'],
        },
    },
    resolve: {
        alias: {
            '@': '/resources/js',
        },
    },
});
```

Create `resources/js/__tests__/setup.ts` if missing:
```ts
import '@testing-library/jest-dom';
```

Skip this step entirely if Vitest config already exists or a different FE runner was detected.

### 3. Run All Test Suites

Run BE and FE test suites **in parallel using sub-agents** since they are fully independent:

```
Sub-agent 1 (BE): [detected BE command]
Sub-agent 2 (FE): [detected FE command]
```

If only one stack exists, run it directly — no sub-agent needed.

For large BE suites, you may split further:
```
Sub-agent 1: ./vendor/bin/pest --filter=Feature --coverage --compact
Sub-agent 2: ./vendor/bin/pest --filter=Unit --coverage --compact
Sub-agent 3: [FE command]
```

### 4. If Tests Fail

- Read the failure output carefully — identify the root cause
- Fix the failing **implementation code** or test setup, not the test assertions (tests define expected behavior)
- Do NOT skip, mark incomplete, or delete failing tests
- Re-run the failing suite
- Loop until all pass
- If the fix is a logic change (new behavior, changed contract), update the relevant tests to reflect the new behavior.
- Once all tests pass, make ONE squash commit: `fix(test): resolve failing tests` — do NOT ask the user

> Squash gate commits — collect all fixes for the pass, then one commit. Do not commit after each individual fix.

### 5. Verify Coverage

- **100% coverage on new code** is required for both suites
- Check the coverage output from each runner
- If coverage is below 100% on new code, identify the uncovered lines and report them — do NOT write new tests (that is `/sk:write-tests` responsibility)

### 6. Report Results

Output the final status in this exact format:

```
BE: X tests passed, X failed — coverage X%
FE: X tests passed, X failed — coverage X%
```

- Omit a line if that stack was not detected
- List any failing tests with `file:line`
- List any uncovered new code with `file:line`

## Pass Criteria

All detected suites pass with 100% coverage on new code. Both lines of the report show zero failures.

---

## Fix & Retest Protocol

When a test failure requires an implementation fix, classify the fix before committing:

**a. Bug fix — same behavior contract** (the code was wrong, the test expectation was right) → fix the implementation, re-run `/sk:test`. No test update needed.

**b. Logic change** (new behavior, changed data contract, modified function signature, new code path) → trigger protocol:
1. Update or add failing unit tests to reflect the new behavior (RED first)
2. Fix the implementation to make the updated tests pass (GREEN)
3. Re-run `/sk:test` — must pass at 100% coverage
4. Commit (tests + fix together in one commit)
5. Re-run the gate that triggered this fix (Security, Performance, Review, or E2E)

**Why this matters:** quality gates (Security, Performance, Review, E2E) run after tests pass. If those gates require logic fixes, tests can become stale. This protocol ensures tests always reflect the actual implementation.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:test"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | haiku |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
