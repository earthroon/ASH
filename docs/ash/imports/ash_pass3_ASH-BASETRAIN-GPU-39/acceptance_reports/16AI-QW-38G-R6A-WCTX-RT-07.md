# 16AI-QW-38G-R6A-WCTX-RT-07 Acceptance

## Acceptance criteria

- Total cases >= 41.
- Positive draft shadow cases >= 4.
- Negative blocked cases >= 37.
- Missing upstream receipt keys are blocked.
- Surface chain digest missing/mismatch and invalid step count are blocked.
- Draft shadow not allowed, missing, invalid UTF-8, empty, and missing digest are blocked.
- Production candidate text, review-ready candidate, and commit-ready candidate leaks are blocked.
- Candidate envelope finalization, candidate id issuance, review queue insertion, auto accept, auto commit, target mutation, runtime apply, production subtitle mutation, training, backward, and weight commit are blocked.
- Accepted cases preserve no production candidate / no review / no commit boundary.

## Static bake status

`BAKED_STATIC_NO_CARGO`

See `WCTX_RT_07_STATIC_CHECKS.txt` and `WCTX_RT_07_BAKE_MANIFEST.json`.
