---
name: smart-commit
description: "Analyze staged changes, auto-detect commit type, and generate conventional commit messages with approval workflow."
---

# Smart Conventional Commits

## Overview

Analyze staged git changes, auto-classify the commit type, detect scope from file paths, and generate a conventional commit message. Present for approval before committing.

## Safety Contract

- **Never** use `--no-verify` — always run pre-commit hooks
- **Never** auto-commit — always present the message for approval first
- **Never** force-push or amend without explicit user request
- **Warn immediately** if on `main` or `master` branch

## Allowed Tools

Bash, Read

## Steps

You MUST complete these steps in order:

### 1. Read Progress Context (Optional)

If `tasks/progress.md` exists, read the most recent Work Log entry. Use this to
understand *why* the staged changes were made — include a concise rationale in
the commit body when the reason isn't obvious from the diff alone.

### 2. Check Branch Safety

```bash
git branch --show-current
```

If the current branch is `main` or `master`, warn the user:

> **Warning:** You are on `main`. Commits should typically go on feature branches. Continue anyway?

Wait for confirmation before proceeding. If denied, stop.

### 3. Analyze Working Tree

```bash
git status --short
git diff --staged --stat
```

Report what's staged vs unstaged.

### 4. Handle Nothing Staged

If nothing is staged (`git diff --staged` is empty):

- Show unstaged changes grouped by directory
- Suggest logical groupings (e.g., "all files in `src/auth/`" or "all test files")
- Ask the user what to stage
- Stage the selected files with `git add`
- If the user wants to stage everything, use `git add` with specific file paths (never `git add -A`)

### 5. Read Full Diff

```bash
git diff --staged
```

Read the full diff to understand the nature of the changes.

### 6. Auto-Classify Commit Type

Classify based on what changed:

| Type | When |
|------|------|
| `feat` | New functionality, new files with business logic, new API endpoints |
| `fix` | Bug fixes, error corrections, fixing broken behavior |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or updating tests only |
| `docs` | Documentation changes only (README, comments, JSDoc) |
| `style` | Formatting, whitespace, semicolons — no logic change |
| `perf` | Performance improvements |
| `chore` | Dependencies, config, tooling, CI — no production code |
| `ci` | CI/CD pipeline changes only |
| `build` | Build system or external dependency changes |

If changes span multiple types, use the most significant one (feat > fix > refactor > others).

### 7. Detect Scope

Determine scope from file paths:

- Single directory: use directory name (e.g., `auth`, `api`, `components`)
- Single file type: use the domain (e.g., `config`, `deps`)
- Cross-cutting: omit scope

### 8. Generate Commit Message

Format: `type(scope): description`

Rules:
- Imperative mood ("add", "fix", "update" — not "added", "fixes", "updated")
- Under 72 characters for the subject line
- Lowercase first word after colon
- No period at end
- If the change is complex, add a body separated by blank line with bullet points

Example:
```
feat(auth): add JWT refresh token rotation

- Store refresh tokens in httpOnly cookies
- Add 7-day expiry with sliding window
- Invalidate old tokens on rotation
```

### 9. Present for Approval

Show the generated message and ask the user to choose:

1. **Commit** — execute as-is
2. **Edit** — let the user modify the message
3. **Split** — help break into multiple smaller commits
4. **Cancel** — abort

### 10. Execute Commit

Use a heredoc to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
type(scope): description

Optional body here.
EOF
)"
```

After committing, show the result:

```bash
git log -1 --oneline
```

### 11. Continue?

Check if there are remaining unstaged changes:

```bash
git status --short
```

If changes remain, ask: "There are more changes. Stage and commit another batch?"

If yes, go back to step 4. If no, done.
