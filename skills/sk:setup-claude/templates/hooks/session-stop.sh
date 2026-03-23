#!/bin/bash
# Claude Code Stop hook: Log session accomplishments
# Runs when a Claude Code session ends

# Only log if tasks/ directory exists (ShipKit project)
if [ ! -d "tasks" ]; then
    exit 0
fi

TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S)

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Count commits in this session (last hour)
RECENT_COMMITS=$(git log --since="1 hour ago" --oneline 2>/dev/null | wc -l | tr -d ' ')

# Get current workflow step
CURRENT_STEP=""
if [ -f "tasks/workflow-status.md" ]; then
    CURRENT_STEP=$(grep -E ">>\s*next\s*<<" "tasks/workflow-status.md" 2>/dev/null | head -1 | sed 's/.*| //' | sed 's/ |.*//')
fi

# Append session end to progress.md
{
    echo ""
    echo "### [$TIMESTAMP] Session ended"
    echo "- Branch: $BRANCH"
    echo "- Commits this session: $RECENT_COMMITS"
    [ -n "$CURRENT_STEP" ] && echo "- Next step: $CURRENT_STEP"
} >> "tasks/progress.md" 2>/dev/null

exit 0
