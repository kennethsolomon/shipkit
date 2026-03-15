---
name: lint
description: "Auto-detect and run all linting tools: formatters first (sequential), then analyzers in parallel. Fix and re-run until clean."
---

# /lint

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

### 5. Fix and Re-run

If any analyzer reports errors:
1. Fix all reported issues
2. Re-run formatters (fixes may need formatting)
3. Re-launch all analyzers in parallel
4. Loop until every tool exits clean

### 6. Report Results

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
```

Only include lines for detected tools. All must show "clean" before this skill passes.
