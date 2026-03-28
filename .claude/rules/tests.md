---
paths:
  - "tests/**"
  - "**/*.test.ts"
  - "**/*.test.js"
  - "**/*.spec.ts"
  - "**/*.spec.js"
  - "**/*.test.php"
---

# Testing Rules

- Tests must be deterministic — no random data, no time-dependent assertions without mocking time
- One concept per test — split large tests into small, focused ones
- Test names describe behavior, not implementation: `it('rejects invalid email')` not `it('calls validator')`
- AAA pattern: Arrange → Act → Assert, with blank lines between each section
- No test dependencies — each test sets up its own state from scratch
- Use factories/fixtures for complex objects — no copy-paste setup across tests
- Mock only at system boundaries: external APIs, filesystem — not internal functions
- Coverage: 100% on new code lines, branches, and functions (enforced by gates)
- No `test.skip`, `it.skip`, `xit`, `xtest` — fix the test or delete it
- Assertion messages: include expected vs actual context when the assertion isn't self-explanatory
- Integration tests: use real database — mock only external services
- Snapshot tests: review snapshots in every PR — they should capture meaningful structure, not noise
