# sk:deps-audit — Dependency Security Audit

**Version:** v3.22.0
**Last Updated:** 2026-03-31

## Purpose

Scans all project dependencies for known CVEs, license violations, and critically outdated packages. Runs automatically as the 4th parallel agent in `/sk:gates` Batch 1. Can also be run on demand before adding new dependencies or before any release.

## Invocation

| Context | How |
|---------|-----|
| Automatic | `/sk:gates` Batch 1 (parallel with lint, security, perf) |
| On demand | `/sk:deps-audit` |
| Pre-release | Recommended before `/sk:release` |

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Package manifests | `package.json`, `composer.json`, `Cargo.toml`, `requirements.txt`, `go.mod`, `Gemfile` | Auto-detected |
| Lockfiles | `package-lock.json`, `yarn.lock`, `bun.lock`, `composer.lock`, `Cargo.lock`, `Gemfile.lock` | Auto-detected |
| Project license | `package.json#license`, `composer.json#license`, `LICENSE` file | Optional (skips license check if absent) |

## Outputs

| Output | Destination | Notes |
|--------|------------|-------|
| Findings report | `tasks/security-findings.md` | Appended — never overwrites |
| Terminal summary | stdout | Always shown |
| Auto-fix commits | git | Only for safe patch/minor bumps |

## Business Logic

### Step 1 — Ecosystem Detection

Scans project root for lockfiles/manifests. Maps each found file to its ecosystem and native audit tool.

**Auto-skip condition:** If no supported package manager is detected, outputs `Auto-skipped: Deps Audit (no package manager detected)` and exits clean.

**Missing tool condition:** If the audit tool is not installed (e.g., `cargo-audit` not present), notes it and skips that ecosystem — does not fail the gate.

### Step 2 — CVE Scan

Runs each ecosystem's native audit command with JSON output. Parses results into a normalized severity schema:

| Severity | Action |
|----------|--------|
| Critical | Blocks gate if unfixed. Auto-fix if safe bump available. |
| High | Blocks gate if unfixed. Auto-fix if safe bump available. |
| Medium | Informational only — logged, does not block. |
| Low | Informational only — logged, does not block. |

### Step 3 — Outdated Package Check

Flags packages that are **2+ major versions behind** the latest published version. These are informational — they do not block the gate.

Packages with known CVEs are always escalated to Critical/High regardless of version gap.

### Step 4 — License Compliance

Reads the project's own license. Flags incompatible dependency licenses:

| Flag | Reason |
|------|--------|
| GPL/AGPL in non-GPL project | Copyleft contamination risk |
| Unknown/unlicensed packages | Cannot assess compatibility |
| SSPL in commercial project | Server-side copyleft risk |

Never flags MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC — always permissive.

**Skip condition:** If no project license is found, license check is skipped with a note.

### Step 5 — Auto-Fix

For Critical/High findings with an available fixed version:
- **Patch or minor bump** — auto-applies the fix and re-runs the audit to confirm resolution.
- **Major bump** — reported as requiring manual upgrade. Never auto-applied (breaking change risk).
- **No fix available** — logged as `unfixable`, does not block the gate.

Auto-fix commits use the format: `fix(deps): upgrade [package] [old-version] → [new-version] (CVE-YYYY-NNNNN)`

### Step 6 — Gate Exit Condition

Gate exits clean if: **zero Critical/High CVEs remain after auto-fix attempts.**

License violations and outdated packages are informational — they are logged but never block the gate.

## Output Format

### tasks/security-findings.md entry

```markdown
## Deps Audit — [YYYY-MM-DD] [branch-name]

### Critical / High CVEs
- [CRITICAL] lodash@4.17.15 — CVE-2021-23337 → upgraded to 4.17.21 ✓
- [HIGH] axios@0.21.0 — CVE-2021-3749 → requires manual upgrade to 1.x (breaking)

### License Issues
- [WARN] some-package@1.0.0 — GPL-3.0 (incompatible with project MIT license)

### Significantly Outdated (2+ major versions)
- react@16.x → latest 19.x

## Deps Audit — 2026-03-31 — clean ✓   ← (if no findings)
```

### Terminal summary

```
=== Deps Audit ===
Critical CVEs:  1 (1 auto-fixed, 0 need manual upgrade)
High CVEs:      0
License issues: 1 (informational)
Outdated (2+):  2 (informational)

[gate: clean — 0 unresolved Critical/High]
```

## Hard Rules

1. **Never** auto-apply major version bumps — breaking change risk is too high.
2. **Never** overwrite existing `tasks/security-findings.md` — always append.
3. **Never** fail the gate for medium/low CVEs, license issues, or outdated packages — those are informational.
4. **Always** re-run the audit after auto-fixing to confirm resolution before reporting clean.
5. If the audit tool crashes or produces unparseable output: log to `tasks/progress.md`, try an alternate approach (e.g., `npm audit` without `--json`), and on 3rd failure skip the ecosystem and continue.

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No package manager found | Auto-skip with `Auto-skipped: Deps Audit (no package manager detected)` |
| Audit tool not installed | Skip that ecosystem, note in terminal, continue |
| CVE with no fix available | Log as unfixable, does not block gate |
| Major-bump-only fix available | Report to user, do not auto-apply |
| 3 audit tool crashes | Skip ecosystem after 3 attempts, continue gate |
| No project license file | Skip license check, note in terminal |

## Relationship to Other Skills

| Skill | Relationship |
|-------|-------------|
| `/sk:security-check` | Complementary — security-check does OWASP code analysis; deps-audit checks supply chain/CVEs |
| `/sk:gates` | Parent orchestrator — deps-audit runs as Batch 1 agent |
| `/sk:lint` | Independent — lint checks code style; deps-audit checks dependencies |
| `/sk:release` | Recommended to run deps-audit before tagging a release |
