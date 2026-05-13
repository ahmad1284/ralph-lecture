#!/bin/bash
# Usage:
#   ./loop.sh              — build mode, unlimited
#   ./loop.sh 10           — build mode, max 10 iterations
#   ./loop.sh plan         — planning mode (runs once)

MODE="build"
PROMPT_FILE="PROMPT_build.md"
MAX_ITERATIONS=0
SINGLE_SHOT=false

if [ "$1" = "plan" ]; then
    MODE="plan"
    PROMPT_FILE="PROMPT_plan.md"
    SINGLE_SHOT=true
elif [[ "$1" =~ ^[0-9]+$ ]]; then
    MAX_ITERATIONS=$1
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   $MODE"
echo "Prompt: $PROMPT_FILE"
[ $MAX_ITERATIONS -gt 0 ] && echo "Max:    $MAX_ITERATIONS iterations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

[ ! -f "$PROMPT_FILE" ] && { echo "Error: $PROMPT_FILE not found"; exit 1; }

while true; do
    [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ] && {
        echo "Reached max iterations: $MAX_ITERATIONS"; break
    }

    cat "$PROMPT_FILE" | claude -p \
        --dangerously-skip-permissions \
        --output-format stream-json \
        --verbose

    git push origin "$CURRENT_BRANCH" 2>/dev/null || true

    $SINGLE_SHOT && break

    ITERATION=$((ITERATION + 1))
    echo -e "\n\n════════════ LOOP $ITERATION ════════════\n"
done
