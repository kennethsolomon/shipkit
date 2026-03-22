#!/bin/bash
# Claude Code PreToolUse hook: Validates git commit commands
# Receives JSON on stdin with tool_input.command
# Exit 0 = allow, Exit 2 = block (stderr shown to Claude)
#
# Validates: conventional commit format, debug statements, hardcoded secrets

INPUT=$(cat)

# Parse command — use jq if available, fall back to grep
if command -v jq >/dev/null 2>&1; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
else
    COMMAND=$(echo "$INPUT" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"command"[[:space:]]*:[[:space:]]*"//;s/"$//')
fi

# Only process git commit commands
if ! echo "$COMMAND" | grep -qE '^git[[:space:]]+commit'; then
    exit 0
fi

WARNINGS=""

# Extract commit message from -m flag
COMMIT_MSG=$(echo "$COMMAND" | grep -oE '\-m[[:space:]]+"[^"]*"' | sed 's/-m[[:space:]]*"//;s/"$//' || echo "")
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG=$(echo "$COMMAND" | grep -oE "\-m[[:space:]]+'[^']*'" | sed "s/-m[[:space:]]*'//;s/'$//" || echo "")
fi

# Validate conventional commit format (type(scope): message or type: message)
if [ -n "$COMMIT_MSG" ]; then
    if ! echo "$COMMIT_MSG" | grep -qE '^(feat|fix|docs|refactor|chore|test|style|perf|ci|build|revert)(\([a-zA-Z0-9_-]+\))?(!)?:[[:space:]].+'; then
        WARNINGS="$WARNINGS\nCOMMIT: Message does not follow conventional commit format: type(scope): message"
    fi
fi

# Check staged files for debug statements
STAGED=$(git diff --cached --name-only 2>/dev/null)
if [ -n "$STAGED" ]; then
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            # JavaScript/TypeScript debug
            if echo "$file" | grep -qE '\.(js|ts|jsx|tsx)$'; then
                if git diff --cached "$file" 2>/dev/null | grep -E '^\+.*console\.(log|debug|warn)\(' | grep -qv '//.*console'; then
                    WARNINGS="$WARNINGS\nDEBUG: $file has console.log/debug/warn in staged changes"
                fi
                if git diff --cached "$file" 2>/dev/null | grep -qE '^\+.*debugger'; then
                    WARNINGS="$WARNINGS\nDEBUG: $file has debugger statement in staged changes"
                fi
            fi
            # PHP debug
            if echo "$file" | grep -qE '\.php$'; then
                if git diff --cached "$file" 2>/dev/null | grep -qE '^\+.*(dd\(|dump\(|var_dump\(|print_r\()'; then
                    WARNINGS="$WARNINGS\nDEBUG: $file has dd/dump/var_dump in staged changes"
                fi
            fi
            # Python debug
            if echo "$file" | grep -qE '\.py$'; then
                if git diff --cached "$file" 2>/dev/null | grep -qE '^\+.*(breakpoint\(\)|pdb\.set_trace\(\))'; then
                    WARNINGS="$WARNINGS\nDEBUG: $file has breakpoint/pdb in staged changes"
                fi
            fi
        fi
    done <<< "$STAGED"

    # Check for potential hardcoded secrets in staged diffs
    DIFF_CONTENT=$(git diff --cached 2>/dev/null)
    if echo "$DIFF_CONTENT" | grep -qE '^\+.*(PRIVATE_KEY|SECRET_KEY|API_KEY|PASSWORD|TOKEN)[[:space:]]*=.*[a-zA-Z0-9]{16,}'; then
        WARNINGS="$WARNINGS\nSECRET: Staged changes may contain hardcoded secrets. Review before committing."
    fi
fi

# Print warnings (non-blocking) and allow commit
if [ -n "$WARNINGS" ]; then
    echo -e "=== Commit Validation Warnings ===$WARNINGS\n================================" >&2
fi

exit 0
