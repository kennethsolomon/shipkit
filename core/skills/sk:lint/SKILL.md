---
name: sk:lint
description: "Auto-detect and run all linting tools: formatters first (sequential), then analyzers in parallel. Fix and re-run until clean."
model: haiku
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
- `composer.json`: read `require-dev` keys for `laravel/pint`, `phpstan/phpstan`, `rector/rector`
- `package.json`: read `devDependencies` keys for `eslint`, `prettier`
- `pyproject.toml`: check `[tool.ruff]` section or `ruff` in `[project.optional-dependencies]` / `[build-system]`
- `go.mod` / `Cargo.toml`: presence of file is sufficient

Print detected stacks and tools before running anything.

### 3. Run Formatters — Sequential

Run in this order (formatters modify files — must not run in parallel):

1. Pint: `vendor/bin/pint --dirty`
2. Prettier: `npx prettier --write .`
3. ruff format: `ruff format .`
4. gofmt: `gofmt -w .`
5. cargo fmt: `cargo fmt`

Note which files changed. All formatters must finish before step 4.

### 4. Run Analyzers — Parallel Sub-Agents

Launch all detected analyzers in parallel using the Agent tool in a single message:

- PHPStan: `vendor/bin/phpstan analyse --memory-limit=512M`
- Rector: `vendor/bin/rector --dry-run`
- ESLint: `npx eslint .`
- ruff check: `ruff check .`
- golangci-lint: `golangci-lint run`
- cargo clippy: `cargo clippy`

Each agent: "Run `<command>`. Report all errors/changes with file:line."

### 5. Run Dependency Audit

| Stack | Command | Block on |
|-------|---------|----------|
| PHP (composer.json) | `composer audit` | any severity with fix available |
| Node (package.json) | `npm audit --audit-level=high` | high or critical |
| Node (yarn.lock) | `yarn audit --level high` | high or critical |
| Node (pnpm-lock.yaml) | `pnpm audit --audit-level high` | high or critical |
| Python (pyproject.toml / requirements.txt) | `pip-audit` | high or critical |

**Block (fail this gate):** PHP: any vuln with fix available (`composer audit` exits non-zero for all severities). Node/Python: critical or high with fix available.

**Warn (pass with note):** medium/low for Node/Python, or any severity with no fix — log but do not block.

### 6. Fix and Re-run

**Classify each issue before fixing:**

Run `git diff main..HEAD --name-only` to get branch diff.

- **Out-of-scope** (file not in branch diff): do NOT fix inline. Log to `tasks/tech-debt.md`:
  ```
  ### [YYYY-MM-DD] Found during: sk:lint
  File: path/to/file.ext:line
  Issue: description of the problem
  Severity: high | medium | low
  ```
- **In-scope** (file in branch diff): fix it.

**Fix loop (in-scope only):**
1. Fix all in-scope issues
2. Re-run formatters
3. Re-launch all analyzers in parallel
4. Re-run dep audit if any dependency was fixed
5. Repeat from step 3 until all tools exit clean
6. Make ONE squash commit: `fix(lint): resolve lint and dep audit issues` — do NOT ask the user

### 7. Report Results

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

Classify every fix before committing:

**a. Formatter auto-fix** (Pint, Prettier, gofmt, cargo fmt changed whitespace/style) → auto-commit and re-run. Never a logic change — bypass protocol.

**b. Analyzer fix** (PHPStan, Rector, ESLint, ruff) — classify:
- Type annotation, import order, unused var, style rule → **style fix** → auto-commit and re-run
- New guard clause, changed condition, extracted function, modified data flow → **logic change** → protocol:
  1. Update or add failing unit tests for the new behavior
  2. Re-run `/sk:test` — must pass at 100% coverage
  3. Auto-commit (tests + fix together)
  4. Re-run `/sk:lint` from scratch

**c. Dependency vulnerability fix** — classify:
- Version bump, no API change → **style fix** → auto-commit and re-run
- Version bump with API/behavior change → **logic change** → trigger protocol

All commits are automatic — do not prompt the user.

---

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

- If `model_overrides["sk:lint"]` is set, use that model — it takes precedence.
- Otherwise use the `profile` field. Default: `balanced`.

| Profile | Model |
|---------|-------|
| `full-sail` | opus (inherit) |
| `quality` | opus (inherit) |
| `balanced` | haiku |
| `budget` | haiku |

> `opus` = inherit (uses the current session model). When spawning sub-agents via the Agent tool, pass `model: "<resolved-model>"`.
