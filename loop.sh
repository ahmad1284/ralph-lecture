#!/bin/bash
# Ralph × codev — SPIR build loop
#
# Usage:
#   ./loop.sh specify      — S: study and lock specs
#   ./loop.sh plan         — P: create implementation plan
#   ./loop.sh [N]          — I: implement (N iterations or infinite)
#   ./loop.sh review       — R: review and document lessons learned

PHASE="${1:-implement}"
MAX_ITERATIONS=0
SINGLE_SHOT=false

case "$PHASE" in
  specify) PROMPT_FILE="codev/porch/prompts/specify.md"; SINGLE_SHOT=true ;;
  plan)    PROMPT_FILE="codev/porch/prompts/plan.md";    SINGLE_SHOT=true ;;
  review)  PROMPT_FILE="codev/porch/prompts/review.md";  SINGLE_SHOT=true ;;
  [0-9]*) PHASE="implement"; MAX_ITERATIONS=$1; PROMPT_FILE="codev/porch/prompts/implement.md" ;;
  *)       PHASE="implement"; PROMPT_FILE="codev/porch/prompts/implement.md" ;;
esac

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase:  $PHASE"
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
