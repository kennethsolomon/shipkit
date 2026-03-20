# Security Findings

> Populated by `/security-check`. Never overwritten — new audits append below.
> Referenced by `/review`, `/finish-feature`, and `/brainstorm` for security context.

---

# Security Audit — 2026-03-20

**Scope:** Changed files on branch `feature/gate-auto-commit-tech-debt`
**Stack:** Node.js (bin only) / Bash / Markdown
**Files audited:** 29 (28 markdown/template + 1 shell script)

## Critical (must fix before deploy)

*None*

## High (fix before production)

*None*

## Medium (should fix)

*None*

## Low / Informational

*None*

## Passed Checks

- A01 Broken Access Control — N/A (no auth layer in changed files)
- A02 Cryptographic Failures — N/A (no crypto operations)
- A03 Injection — `tests/verify-workflow.sh`: all grep patterns and file paths are hardcoded, not user-supplied; shell variables are double-quoted throughout
- A04 Insecure Design — N/A
- A05 Security Misconfiguration — `.gitignore` correctly excludes `.shipkit/` (config with profile settings)
- A06 Vulnerable Components — `npm audit`: 0 vulnerabilities (verified in Step 12)
- A07 Auth Failures — N/A
- A08 Data Integrity Failures — N/A
- A09 Logging Failures — N/A
- A10 SSRF — `tests/verify-workflow.sh:82`: `curl` targets `http://localhost:${port}` only — no external URLs, no user-controlled hostname
- Shell safety — `set -euo pipefail` on line 6; `BASH_SOURCE[0]` path construction is properly quoted; process substitution `$()` used safely with fixed args

## Summary

| Severity | Open | Resolved this run |
|----------|------|-------------------|
| Critical | 0    | 0                 |
| High     | 0    | 0                 |
| Medium   | 0    | 0                 |
| Low      | 0    | 0                 |
| **Total** | **0** | **0**           |

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

---

# Security Audit — 2026-03-16

**Scope:** Changed files on branch `feature/workflow-e2e-fix-retest-sk-prefix`
**Stack:** Shell/Bash, Markdown
**Files audited:** 22

## Critical (must fix before deploy)

None.

## High (fix before production)

None.

## Medium (should fix)

- **[install.sh:109]** `npm install -g agent-browser` has no version pin — installs latest at time of execution.
  **Standard:** OWASP A06 — Vulnerable and Outdated Components (CWE-1395)
  **Risk:** Supply chain attack; a malicious publish to npm could execute arbitrary code on installer machines.
  **Recommendation:** Pin to a specific version: `npm install -g agent-browser@<version>` and document the expected version in the README.

## Low / Informational

- **[tests/verify-workflow.sh:6]** `set -uo pipefail` is missing the `-e` flag. Without `-e`, the script continues after a failing command in some contexts (e.g., outside of pipelines or `[[ ]]` constructs), which can mask silent failures in the assertion helpers.
  **Recommendation:** Change to `set -euo pipefail` for consistency and early-exit safety.

- **[install.sh:109-110]** `npm install -g agent-browser && agent-browser install` downloads a ~100MB Chrome binary with no checksum verification.
  **Standard:** OWASP A08 — Software and Data Integrity Failures (CWE-494)
  **Risk:** If the CDN or npm package is compromised, a malicious binary could be silently installed. Low likelihood for a dev tool but worth noting.
  **Recommendation:** Document the expected hash of the Chrome binary in the README, or use `agent-browser`'s built-in integrity check if it provides one.

## Passed Checks

- **A01 Broken Access Control** — No auth logic. All changed files are local shell scripts and Markdown docs.
- **A02 Cryptographic Failures** — No cryptographic operations introduced.
- **A03 Injection** — `install.sh` constructs no shell commands from user input. All paths are derived from `${BASH_SOURCE[0]}` and `${REPO_DIR}`. No eval, no dynamic string exec.
- **A04 Insecure Design** — Symlink creation limited to `~/.claude/skills/` and `~/.claude/commands/sk/`. Stale symlink cleanup uses a hardcoded allow-list. No arbitrary path traversal possible.
- **A05 Security Misconfiguration** — No servers, no network listeners, no credentials. `install.sh` outputs a WARN (not silent fail) when npm is missing.
- **A07 Auth Failures** — N/A (local install script, no auth).
- **A09 Logging Failures** — N/A (stdout-only CLI tool).
- **A10 SSRF** — No URL construction from user input. `npm install` and `agent-browser install` use hardcoded package/tool names.
- **Shell injection** — All variable expansions in `install.sh` are double-quoted. `basename` is called on controlled paths. No `$()` or backtick expansion on user-provided data.
- **Markdown/SKILL.md files** — Static documentation only. No executable code, no secrets, no PII.
- **verify-workflow.sh** — Uses `grep -q` on controlled file paths. No user input flows into shell commands.

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High     | 0 |
| Medium   | 1 |
| Low      | 2 |
| **Total** | **3** |

---

# Security Audit — 2026-03-16 (branch: feature/sk-seo-audit-checklist-format)

**Scope:** Changed files on branch `feature/sk-seo-audit-checklist-format`
**Stack:** Shell/Bash, Markdown
**Files audited:** 14

## Critical (must fix before deploy)

None.

## High (fix before production)

None.

## Medium (should fix)

None.

## Low / Informational

None.

## Passed Checks

- **A01 Broken Access Control** — No auth logic. All changed files are static markdown docs and a test script.
- **A02 Cryptographic Failures** — No cryptographic operations introduced.
- **A03 Injection** — `tests/verify-workflow.sh` additions use `grep -q` on controlled paths from `$REPO` (derived from `BASH_SOURCE[0]`). No user input flows into any shell command.
- **A04 Insecure Design** — No new design surface. `sk:seo-audit/SKILL.md` instructs probing localhost ports only (hardcoded: 3000, 5173, 8000, 8080, 4321, 4000, 8888) with `--max-time 2` timeout.
- **A05 Security Misconfiguration** — `install.sh` change is a single static `echo` line. No new config surface.
- **A06 Vulnerable Components** — No new dependencies introduced.
- **A08 Data Integrity** — No new deserialization or binary downloads.
- **A10 SSRF** — `sk:seo-audit` curl probes are localhost-only with hardcoded ports. No user-controlled URL construction.
- **Shell injection** — All variable expansions in new `verify-workflow.sh` assertions are double-quoted. No dynamic exec.
- **Prior LOW resolved** — `tests/verify-workflow.sh:6` now correctly uses `set -euo pipefail` (includes `-e`). Low finding from 2026-03-16 prior audit is resolved.
- **Markdown/SKILL.md files** — Static documentation only. No executable code, no secrets, no PII.

## Summary

| Severity | Open | Resolved this run |
|----------|------|-------------------|
| Critical | 0    | 0                 |
| High     | 0    | 0                 |
| Medium   | 0    | 0                 |
| Low      | 0    | 1                 |
| **Total** | **0** | **1** |

---

# Security Audit — 2026-03-19 (branch: feature/context-mvp-docs-decisions)

**Scope:** Changed files on branch `feature/context-mvp-docs-decisions`
**Stack:** Shell/Bash, Markdown
**Files audited:** 12

## Critical (must fix before deploy)

None.

## High (fix before production)

None.

## Medium (should fix)

None.

## Low / Informational

None.

## Passed Checks

- **A01 Broken Access Control** — No auth logic. All 12 files are Markdown skill definitions or documentation.
- **A02 Cryptographic Failures** — No cryptographic operations introduced.
- **A03 Injection** — `install.sh` change is a static `echo` line. `tests/verify-workflow.sh` additions use `grep -q` on controlled paths via existing `assert_contains` helper. No user input in any shell command.
- **A04 Insecure Design** — `sk:context/SKILL.md` reads local filesystem files only (tasks/, docs/). No network access, no external data.
- **A05 Security Misconfiguration** — No servers, no network listeners, no credentials introduced.
- **A06 Vulnerable Components** — No new dependencies.
- **A08 Data Integrity** — `sk:brainstorming` ADR append uses file write, not deserialization. No integrity risk.
- **A10 SSRF** — No URL construction from user input. No network requests.
- **Shell injection** — All variable expansions in new test assertions are double-quoted. No dynamic exec.
- **Markdown/SKILL.md files** — Static documentation and skill instructions only. No executable code, no secrets, no PII.

## Summary

| Severity | Open | Resolved this run |
|----------|------|-------------------|
| Critical | 0    | 0                 |
| High     | 0    | 0                 |
| Medium   | 0    | 0                 |
| Low      | 0    | 0                 |
| **Total** | **0** | **0**            |
