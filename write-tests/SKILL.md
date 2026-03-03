---
name: write-tests
description: "Detect testing framework, analyze target code, and generate comprehensive test files matching project conventions."
---

# Test Generation

## Overview

Detect the project's testing framework, read existing test patterns, analyze target code, and generate comprehensive test files that match the project's style. Run the tests and fix failures.

## Allowed Tools

Bash, Read, Write, Edit, Glob, Grep

## Steps

You MUST complete these steps in order:

### 1. Detect Testing Framework

Check project configuration files to identify the testing stack:

```bash
# Check for config/dependency files
cat package.json 2>/dev/null        # Jest, Vitest, Mocha
cat pyproject.toml 2>/dev/null      # pytest
cat go.mod 2>/dev/null              # Go testing
cat Cargo.toml 2>/dev/null          # Rust #[cfg(test)]
cat composer.json 2>/dev/null       # PHPUnit
```

Also check for framework-specific config:
- `vitest.config.ts` / `vite.config.ts` (vitest)
- `jest.config.js` / `jest.config.ts` (Jest)
- `.mocharc.yml` / `.mocharc.js` (Mocha)
- `pytest.ini` / `conftest.py` / `setup.cfg` (pytest)
- `phpunit.xml` (PHPUnit)

Report what was detected:
```
Detected: [framework] ([language]) — [test runner command]
```

### 2. Identify Target Code

Determine what to write tests for, in order of priority:

1. **User-specified**: If the user named a file, function, or module — use that
2. **Recent changes**: `git diff --name-only HEAD~1` — test the most recently changed code
3. **Untested code**: Find source files without corresponding test files

Ask the user to confirm the target if ambiguous.

### 3. Learn Project Test Conventions

Find and read 1-2 existing test files to learn the project's patterns:

```bash
# Find existing tests
find . -name "*.test.*" -o -name "*.spec.*" -o -name "test_*.py" -o -name "*_test.go" | head -5
```

From existing tests, learn:
- Import style and aliases
- Test structure (describe/it, test(), func TestX)
- Assertion library and patterns
- Mocking approach (jest.mock, vi.mock, unittest.mock, etc.)
- Setup/teardown patterns
- File naming convention
- Test file location (co-located vs `tests/` directory)

If **no existing tests** are found, use `references/patterns.md` for framework-appropriate templates.

### 4. Analyze Target Code

Read the target file(s) and identify test cases:

- **Happy path**: Normal expected behavior for each function/method
- **Edge cases**: Empty inputs, boundary values, null/undefined, large inputs
- **Error handling**: Invalid inputs, thrown exceptions, error responses
- **Branches**: Every if/else, switch case, ternary, early return
- **Async behavior**: Promise resolution/rejection, timeout handling
- **Integration points**: API calls, database queries, external dependencies (mock these)

### 5. Determine Test File Location

Follow the project's existing convention:

| Convention | Pattern | Example |
|-----------|---------|---------|
| Co-located | Same directory as source | `src/auth/login.test.ts` |
| Mirror `tests/` | Parallel directory structure | `tests/auth/login.test.ts` |
| `__tests__/` | Jest convention subdirectory | `src/auth/__tests__/login.test.ts` |
| `test_` prefix | Python convention | `tests/test_login.py` |
| `_test` suffix | Go convention | `auth/login_test.go` |

If no convention exists, prefer co-located tests.

### 6. Write Test File

Generate the complete test file. Follow these principles:

- Match the project's existing style exactly (imports, structure, naming)
- One test per behavior, not per line of code
- Descriptive test names that explain the expected behavior
- Arrange-Act-Assert pattern
- Mock external dependencies, not the code under test
- Test behavior, not implementation details
- Include setup/teardown if needed

Write the file using the Write or Edit tool.

### 7. Run Tests

Execute only the new test file:

```bash
# Examples by framework
npx vitest run path/to/file.test.ts
npx jest path/to/file.test.ts
python -m pytest path/to/test_file.py -v
go test ./path/to/package/ -run TestName -v
cargo test test_name -- --nocapture
```

### 8. Fix Failures (up to 3 attempts)

If tests fail:

1. Read the error output carefully
2. Determine if it's a test bug or a real code bug
3. If test bug: fix the test
4. If real code bug: report to user, don't fix silently
5. Re-run the specific failing tests

Maximum 3 fix attempts. If still failing after 3, report the remaining failures to the user with analysis.

### 9. Report Results

Summarize:
- Tests written: count and file path
- Tests passing: count
- Tests failing: count (with details if any)
- Coverage: if available from the test runner output

### 10. Coverage (Optional)

If the user requests coverage or the framework supports it easily:

```bash
npx vitest run --coverage path/to/file.test.ts
python -m pytest --cov=module path/to/test_file.py
go test -cover ./path/to/package/
```

Report coverage for the target file(s).
