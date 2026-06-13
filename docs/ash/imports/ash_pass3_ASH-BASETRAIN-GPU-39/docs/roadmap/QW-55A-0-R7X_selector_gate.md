# Roadmap — QW-55A-0-R7X

R7X collapses the earlier R7/R8 shadow plan into one explicit selector gate patch.

## Implemented in this bake

1. R6 projected feature rows are converted into score rows.
2. Score rows are aggregated deterministically.
3. Aggregate rows are sorted by `aggregate_score desc`, then `root_rank asc`.
4. Selector result is created.
5. Selected token candidate and selected root rank candidate are created.
6. Runtime commit remains blocked.

## Next

`QW-55A-RUNTIME-00 — Runtime TopK Snapshot Bind / Explicit Enable No Greedy Fallback Seal`
