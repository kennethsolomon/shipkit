---
name: sk:lint
description: "Auto-detect and run all linting tools: formatters first (sequential), then analyzers in parallel. Fix and re-run until clean."
---

# /sk:lint

Auto-detect project linting tools, run them, fix issues, repeat until clean.

## Steps

### 1. Read Project CLAUDE.md

Check for project-specific lint configuration or overrides in `CLAUDE.md` before proceeding.

### 2. Detect Stacks

Scan the project root for config files. Enable every matching stack:

| Config file | Stack | Formatter | Analyzers |
|---|---|---|---|
| `composer.json` with pint | Laravel/PHP | `vendor/bin/pint --dirty` | -- |
| `composer.json` with phpstan | Laravel/PHP | -- | `vendor/bin/phpstan analyse --memory-limit=512M` |
| `composer.json` with rector | Laravel/PHP | -- | `vendor/bin/rector --dry-run` |
| `package.json` with prettier | Node/TS | `npx prettier --write .` | -- |
| `package.json` with eslint | Node/TS | -- | `npx eslint .` |
| `pyproject.toml` with ruff | Python | `ruff format .` | `ruff check .` |
| `go.mod` | Go | `gofmt -w .` | `golangci-lint run` |
| `Cargo.toml` | Rust | `cargo fmt` | `cargo clippy` |

Detection logic:
- For `composer.json`: read `require-dev` keys for `laravel/pint`, `phpstan/phpstan`, `rector/rector`
- For `package.json`: read `devDependencies` keys for `eslint`, `prettier`
- For `pyproject.toml`: check `[tool.ruff]` section or `ruff` in `[project.optional-dependencies]` / `[build-system]`
- For `go.mod` / `Cargo.toml`: presence of file is sufficient

Print detected stacks and tools before running anything.

### 3. Run Formatters — Sequential

Formatters modify files, so run them one at a time in this order:

1. **Pint** (if detected): `vendor/bin/pint --dirty`
2. **Prettier** (if detected): `npx prettier --write .`
3. **ruff format** (if detected): `ruff format .`
4. **gofmt** (if detected): `gofmt -w .`
5. **cargo fmt** (if detected): `cargo fmt`

After each formatter, note which files changed. All formatters must finish before step 4.

### 4. Run Analyzers — Parallel Sub-Agents

Launch all detected analyzers in parallel using the Agent tool in a single message:

- **PHPStan**: `vendor/bin/phpstan analyse --memory-limit=512M`
- **Rector**: `vendor/bin/rector --dry-run`
- **ESLint**: `npx eslint .`
- **ruff check**: `ruff check .`
- **golangci-lint**: `golangci-lint run`
- **cargo clippy**: `cargo clippy`

Example with PHPStan + Rector + ESLint detected:
```
Agent 1: "Run vendor/bin/phpstan analyse --memory-limit=512M. Report all errors with file:line."
Agent 2: "Run vendor/bin/rector --dry-run. Report all suggested changes with file:line."
Agent 3: "Run npx eslint . Report all errors with file:line."
```

### 5. Run Dependency Audit

Run dependency vulnerability checks for detected stacks:

| Stack | Command | Block on |
|-------|---------|----------|
| PHP (composer.json) | `composer audit` | critical or high with fix available |
| Node (package.json) | `npm audit --audit-level=high` | high or critical |
| Node (yarn.lock) | `yarn audit --level high` | high or critical |
| Node (pnpm-lock.yaml) | `pnpm audit --audit-level high` | high or critical |
| Python (pyproject.toml / requirements.txt) | `pip-audit` | high or critical |

For each detected package manager, run the audit command and capture output.

**Block (fail this gate):** critical or high severity vulnerabilities that have a fix available — package name, CVE, current version, fix version.

**Warn (pass with note):** medium/low severity, or critical/high with no available fix — note in report but do not block.

Skip stacks not present in the project.

### 6. Fix and Re-run

If any analyzer reports errors or the dep audit blocks:
1. Fix all reported issues
2. Re-run formatters (fixes may need formatting)
3. Re-launch all analyzers in parallel
4. Re-run dep audit if any dependency was fixed
5. Loop until every tool exits clean

### 7. Report Results

Print one line per tool:

```
Pint:          X files formatted / clean
Prettier:      X files formatted / clean
ruff format:   X files formatted / clean
gofmt:         X files formatted / clean
cargo fmt:     X files formatted / clean
PHPStan:       X errors fixed / clean
Rector:        X changes applied / clean
ESLint:        X errors fixed / clean
ruff check:    X issues fixed / clean
golangci-lint: X issues fixed / clean
cargo clippy:  X warnings fixed / clean
composer audit: clean / X vulns blocked
npm audit:     clean / X vulns blocked
```

Only include lines for detected tools. All must show "clean" before this skill passes.

---

## Fix & Retest Protocol

When this gate requires a fix, classify it before committing:

**a. Formatter auto-fix** (Pint, Prettier, gofmt, cargo fmt changed whitespace/style) → commit and re-run `/sk:lint`. Never a logic change — bypass protocol.

**b. Analyzer fix** (PHPStan type error, Rector suggestion, ESLint error, ruff violation) → classify each fix:
  - Type annotation, import order, unused var, style rule → **style fix** → commit and re-run
  - New guard clause, changed condition, extracted function, modified data flow → **logic change** → trigger protocol:
    1. Update or add failing unit tests for the new behavior
    2. Re-run `/sk:test` — must pass at 100% coverage
    3. Commit (tests + fix together in one commit)
    4. Re-run `/sk:lint` from scratch

**c. Dependency vulnerability fix** (composer audit / npm audit finding) → classify:
  - Version bump with no API change → **style fix** → commit and re-run
  - Version bump with API/behavior change → **logic change** → trigger protocol

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:lint"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | sonnet |
| `quality` | sonnet |
| `balanced` | haiku |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
