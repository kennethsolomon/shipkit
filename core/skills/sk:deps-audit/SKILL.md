---
name: sk:deps-audit
description: Dependency security audit — CVE scanning, license compliance, and outdated package detection across npm, Composer, Cargo, pip, Go modules, and Bundler.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Dependency Audit

Scans all project dependencies for CVEs, license violations, and critically outdated packages. Writes findings to `tasks/security-findings.md`. Auto-fixes safe version bumps (patch/minor with no breaking changes).

## When to Use

- Automatically in `/sk:gates` Batch 1 (parallel with lint, security, perf)
- On demand before adding new dependencies
- Before any release (`/sk:release`)

## Step 1 — Detect Package Managers

Scan project root for lockfiles/manifests:

| File | Package Manager | Audit Command |
|------|----------------|---------------|
| `package.json` + `package-lock.json` / `yarn.lock` / `bun.lock` | npm/yarn/bun | `npm audit --json` / `yarn audit --json` / `bun audit` |
| `composer.json` + `composer.lock` | Composer | `composer audit --format=json` |
| `Cargo.toml` + `Cargo.lock` | Cargo | `cargo audit --json` (requires `cargo-audit`) |
| `requirements.txt` / `pyproject.toml` | pip | `pip-audit --format=json` (requires `pip-audit`) |
| `go.mod` | Go modules | `govulncheck ./...` (requires `govulncheck`) |
| `Gemfile` + `Gemfile.lock` | Bundler | `bundle audit check --update` (requires `bundler-audit`) |

If no package manager found: output `Auto-skipped: Deps Audit (no package manager detected)` and stop.

If audit tool is missing, note it and skip that ecosystem (do not fail the gate).

## Step 2 — Run CVE Scan

Run all detected audit commands. Capture JSON output. Parse findings into:

```
[CRITICAL] package-name@version — CVE-YYYY-NNNNN
  Severity: Critical | CVSS: 9.8
  Fix: upgrade to X.Y.Z
  Details: <brief description>

[HIGH] package-name@version — CVE-YYYY-NNNNN
  ...
```

## Step 3 — Check Outdated Packages

Run outdated check per ecosystem:

| Ecosystem | Command |
|-----------|---------|
| npm | `npm outdated --json` |
| Composer | `composer outdated --direct --format=json` |
| Cargo | `cargo outdated` (if installed) |

Flag packages that are **2+ major versions** behind as High priority.
Flag packages with known security advisories as Critical/High regardless of version gap.
Skip minor/patch outdated packages — those are not blocking.

## Step 4 — License Compliance

Check for licenses that are incompatible with the project's license (read from `package.json#license`, `composer.json#license`, or `LICENSE` file):

**Always flag:**
- GPL/AGPL in a non-GPL project (copyleft contamination risk)
- Unknown/unlicensed packages
- SSPL in commercial projects

**Never flag:**
- MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC (permissive — always compatible)

If no project license found: skip license check, note it.

## Step 5 — Auto-Fix Safe Bumps

For Critical/High CVE findings where a fixed version exists:
- If fix requires **patch or minor bump** with no breaking changes: auto-apply
  ```bash
  npm update <package>  # or composer update <package>, etc.
  ```
- If fix requires **major bump**: report it, do NOT auto-fix (breaking change risk)
- If no fix exists: report as unfixable, log to `tasks/security-findings.md`

After applying fixes, re-run the audit to confirm resolution.

## Step 6 — Write Findings

Append findings to `tasks/security-findings.md` (never overwrite existing content):

```markdown
## Deps Audit — [YYYY-MM-DD] [branch-name]

### Critical / High CVEs
- [CRITICAL] lodash@4.17.15 — CVE-2021-23337 (prototype pollution) → fixed: upgraded to 4.17.21 ✓
- [HIGH] axios@0.21.0 — CVE-2021-3749 (ReDoS) → fix: upgrade to 0.21.4 (manual — major bump)

### License Issues
- (none)

### Significantly Outdated (2+ major versions)
- react@16.x → latest: 19.x (manual upgrade required)
```

If no findings: append a one-liner: `## Deps Audit — [date] — clean ✓`

## Step 7 — Report

Output a summary to the terminal:

```
=== Deps Audit ===
Critical CVEs:  N (N auto-fixed, N need manual upgrade)
High CVEs:      N
License issues: N
Outdated (2+):  N

[clean / N issues require attention — see tasks/security-findings.md]
```

Exit clean if: zero Critical/High CVEs remain after auto-fix. License issues and outdated packages are informational — they do not block the gate.

## 3-Strike Protocol

If audit tool crashes or produces unparseable output:
1. Log to `tasks/progress.md`
2. Try alternate audit approach (e.g., fall back to `npm audit` without `--json`)
3. On 3rd failure: skip this gate, log reason, do not block pipeline

## Model Routing

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Deps audit is mechanical — haiku is sufficient.
