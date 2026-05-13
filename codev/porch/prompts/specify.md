# Specify Phase

Study @specs/* and @README.md carefully using parallel subagents.

## Your job
Ensure every spec is complete, unambiguous, and internally consistent before any code is written.

## Steps

1. Read every file in specs/ with parallel subagents.

2. Cross-check specs against each other. Flag any:
   - Gaps (e.g. what happens when a required tool is missing?)
   - Contradictions (e.g. two specs that disagree on output format)
   - Missing detail (e.g. error handling, edge cases)

3. Update specs in place to fill the gaps. Add a new spec file if a whole area is unaddressed.

4. Do NOT write any implementation code.

5. Commit: `specify: [summary of what was clarified or added]`

6. Update @codev/status.yaml: set `phase: plan`

## Output when done
`<signal>SPECIFY_COMPLETE</signal>`
