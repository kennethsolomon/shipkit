#!/bin/bash
# Claude Code statusline: Shows persistent status in CLI
# Receives JSON on stdin with context_window, model info
# Outputs a single formatted line

INPUT=$(cat)

# Parse context and model — use jq if available
if command -v jq >/dev/null 2>&1; then
    MODEL=$(echo "$INPUT" | jq -r '.model // "unknown"' 2>/dev/null)
    CTX_USED=$(echo "$INPUT" | jq -r '.context_window.used // 0' 2>/dev/null)
    CTX_TOTAL=$(echo "$INPUT" | jq -r '.context_window.total // 1' 2>/dev/null)
else
    MODEL="unknown"
    CTX_USED=0
    CTX_TOTAL=1
fi

# Calculate context percentage
if [ "$CTX_TOTAL" -gt 0 ] 2>/dev/null; then
    CTX_PCT=$((CTX_USED * 100 / CTX_TOTAL))
else
    CTX_PCT=0
fi

# Branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "none")

# Current workflow step
STEP="—"
if [ -f "tasks/workflow-status.md" ]; then
    NEXT_LINE=$(grep -E ">>\s*next\s*<<" "tasks/workflow-status.md" 2>/dev/null | head -1)
    if [ -n "$NEXT_LINE" ]; then
        # Extract step number and name from table row
        STEP_NUM=$(echo "$NEXT_LINE" | grep -oE '^\|[[:space:]]*[0-9]+' | grep -oE '[0-9]+')
        STEP_NAME=$(echo "$NEXT_LINE" | sed 's/.*| *>> next << *|.*//' | sed 's/|.*//;s/^ *//;s/ *$//')
        if [ -n "$STEP_NUM" ]; then
            STEP="Step ${STEP_NUM}"
        fi
    fi
fi

# Task name from todo.md
TASK="—"
if [ -f "tasks/todo.md" ]; then
    TASK=$(head -1 "tasks/todo.md" 2>/dev/null | sed 's/^# TODO.*— //' | cut -c1-40)
fi

# Output single line
echo "[${CTX_PCT}%] ${MODEL} | ${STEP} | ${BRANCH} | ${TASK}"
