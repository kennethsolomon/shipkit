# Security Findings

> Populated by `/security-check`. Never overwritten — new audits append below.
> Referenced by `/review`, `/finish-feature`, and `/brainstorm` for security context.

# Security Audit — 2026-03-08

**Scope:** Changed files on branch `feat/workflow-tracker`
**Stack:** Python / Markdown templates
**Files audited:** 5

## Critical (must fix before deploy)

None.

## High (fix before production)

None.

## Medium (should fix)

None.

## Low / Informational

None.

## Passed Checks

- **A01 Broken Access Control** — No auth logic in changed files. Script is a local CLI tool, no network access.
- **A02 Cryptographic Failures** — `hashlib.sha256` used only for template change detection (non-security purpose), appropriate usage.
- **A03 Injection** — No user input flows into shell commands, SQL, or template rendering. `render_template()` performs static string replacement on controlled template placeholders only. No `eval()`, `exec()`, or `subprocess` calls.
- **A04 Insecure Design** — File write operations use `Path` API with controlled paths derived from template mappings, not user input.
- **A05 Security Misconfiguration** — No server, no network listeners, no credentials.
- **A06 Vulnerable Components** — No external dependencies (stdlib only).
- **A07 Auth Failures** — N/A (local CLI tool).
- **A08 Data Integrity Failures** — Template hash system uses SHA256 for integrity checking. No deserialization of untrusted data.
- **A09 Logging Failures** — N/A (CLI tool, stdout only).
- **A10 SSRF** — No network requests.
- **Path Traversal** — `render_template()` replaces placeholders with values from `Detection` dataclass (populated from `package.json`). Template paths are hardcoded in the `apply()` function, not user-controlled. The `repo_root` argument is resolved via `Path.resolve()` at `apply_setup_claude.py:420`.
- **Python-specific** — No `eval()`, `exec()`, `pickle`, `subprocess.shell=True`, or `os.system()`. JSON parsing uses `json.loads()` with proper exception handling.
- **Test file** — Tests use `tempfile.TemporaryDirectory()` for isolation. No hardcoded paths or credentials.
- **Markdown templates** — Static content only. No executable code, no secrets, no PII.

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High     | 0 |
| Medium   | 0 |
| Low      | 0 |
| **Total** | **0** |
