---
name: sk:safety-guard
description: "Protect against destructive operations with careful, freeze, and guard modes."
disable-model-invocation: true
---

# /sk:safety-guard — Destructive Operation Protection

Three modes of protection that prevent accidental destructive operations and constrain file edits to specific directories.

## Usage

```
/sk:safety-guard careful              # intercept destructive commands
/sk:safety-guard freeze --dir src/    # lock edits to src/ only
/sk:safety-guard guard --dir src/     # both careful + freeze
/sk:safety-guard off                  # disable all guards
/sk:safety-guard status               # show current mode
```

## Model Routing

Read `.shipkit/config.json` from the project root if it exists.

| Profile | Model |
|---------|-------|
| `full-sail` | haiku |
| `quality` | haiku |
| `balanced` | haiku |
| `budget` | haiku |

> Config read/write — haiku is sufficient.

## Modes

### Careful Mode

Intercepts destructive commands before execution:

| Command Pattern | Risk |
|----------------|------|
| `rm -rf`, `rm -fr` | File deletion |
| `git push --force`, `git push -f` | History rewrite |
| `git reset --hard` | Uncommitted changes lost |
| `git clean -f` | Untracked files deleted |
| `DROP TABLE`, `DROP DATABASE` | Data loss |
| `chmod 777`, `chmod -R 777` | Security vulnerability |
| `--no-verify` | Hook bypass |

When a destructive command is detected:
```
BLOCKED by safety-guard (careful mode): destructive command detected.
  Command: rm -rf /tmp/build
  Pattern: rm -rf
  Disable: /sk:safety-guard off
```

### Freeze Mode

Locks file edits (Edit/Write tools) to a specific directory tree:

```
/sk:safety-guard freeze --dir src/api/
```

After activation:
- Edit/Write to `src/api/**` → allowed
- Edit/Write to `src/models/**` → **BLOCKED**
- Edit/Write to `tests/**` → **BLOCKED**
- Bash commands → not restricted (use careful mode for that)

When a write outside the frozen directory is detected:
```
BLOCKED by safety-guard (freeze mode): write outside frozen directory.
  File: tests/api/auth.test.ts
  Allowed: src/api/
  Disable: /sk:safety-guard off
```

### Guard Mode

Combines careful + freeze. Both protections active simultaneously.

### Off

Disables all guards. Removes `.claude/safety-guard.json`.

## Implementation

### Configuration File

Safety guard state is stored in `.claude/safety-guard.json`:

```json
{
  "mode": "guard",
  "freeze_dir": "src/api/",
  "activated_at": "2026-03-25T10:30:00Z",
  "activated_by": "user"
}
```

### Hook Integration

The `safety-guard.sh` hook (deployed to `.claude/hooks/`) reads this config file on every PreToolUse event for Bash/Edit/Write tools. If no config file exists, the hook exits immediately (no overhead).

## Steps

When invoked:

1. Parse the mode argument (`careful` | `freeze` | `guard` | `off` | `status`)
2. For freeze/guard: require `--dir` argument
3. Write config to `.claude/safety-guard.json`
4. Confirm activation:
   ```
   Safety guard activated: guard mode
   Freeze directory: src/api/
   Destructive commands: blocked
   Disable: /sk:safety-guard off
   ```

For `status`:
```
Safety guard: guard mode (active since 2026-03-25 10:30)
  Freeze directory: src/api/
  Blocked actions: 3 (2 destructive commands, 1 out-of-scope write)
  Log: .claude/safety-guard.log
```

## Best Practices

- Use **freeze mode** during `/sk:autopilot` to prevent scope creep in file edits
- Use **careful mode** as a default for new team members
- Use **guard mode** for production hotfixes — maximum protection
- Always disable after the focused task is complete
