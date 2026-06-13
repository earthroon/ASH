# 16AI-QW-38G-R6A-SAMPLER-05 Acceptance

## Status
STATIC_BAKE_ONLY / RUNTIME_NOT_RUN

## Accepted in this bake
- SAMPLER-05 module added.
- SAMPLER-03 append hook now forwards to SAMPLER-05 receipt when `ASH_SAMPLER05_PARITY` is enabled.
- GPU top-p/min-p scan threshold now uses weighted score for pre-min-p max.
- Top-k transition-awareness risk is exposed through controlled bypass policy, default off.
- Workspace receipt/schema/summary/static-check artifacts included.

## Not accepted as runtime pass
- Cargo check/test: NOT_RUN, cargo unavailable in container.
- WGSL compile: NOT_RUN, target GPU compiler unavailable in container.
- Runtime parity probe: NOT_RUN, requires target runtime.

## Promotion block
`ready_for_dynamic_sampler=false` until actual `workspace/sampler05_parity_steps.jsonl` is produced by runtime probe and summary is updated from real receipts.
