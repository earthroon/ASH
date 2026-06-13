# 16AI-QW-38G-R6A-SALAD-03B — Rollback Controlled Execute / KV-Restored Safe Resample Seal

## Status

- static_status: PASS_STATIC
- cargo_check: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
- runtime_smoke: NOT_RUN
- default_enable: false

## Baked files

- `crates/model_core/src/salad03b_controlled_execute.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampler_parity.rs`
- `workspace/salad03b_controlled_execute_schema.json`
- `workspace/salad03b_steps.jsonl`
- `workspace/salad03b_summary.json`
- `workspace/salad03b_static_checks.json`
- `workspace/salad03b_probe_prompts.jsonl`
- `acceptance_reports/16AI-QW-38G-R6A-SALAD-03B_acceptance.md`

## Contract

SALAD-03B is the first rollback execute seal, but it remains default-off.
Behavior changes are only allowed when `ASH_SALAD03B_MODE=controlled_execute` or `strict_controlled_execute`, `ASH_SALAD03B_BEHAVIOR_CHANGE_ALLOWED=true`, and the gate sees `restore_verified_for_salad03b=true`.

The patch forbids string-only rollback. A valid execute receipt must show KV restore, position restore, token ledger truncate, safe resample, original tail capture, replacement token capture, and post-resample risk check.

## Runtime example

```bash
ASH_SALAD03B_MODE=controlled_execute \
ASH_SALAD03B_BEHAVIOR_CHANGE_ALLOWED=true \
ASH_SALAD03B_REQUIRE_VERIFIED_RESTORE=true \
ASH_SALAD03B_MAX_ROLLBACK_DEPTH=8 \
ASH_SALAD03B_MAX_ROLLBACKS_PER_WINDOW=1 \
ASH_SALAD03B_RECEIPT=workspace/salad03b_steps.jsonl \
ASH_SALAD03B_SUMMARY=workspace/salad03b_summary.json
```

## Next recommended patch

`16AI-QW-38G-R6A-STOP-01 — Safe Stop Controlled Execute Seal`

SALAD-03B keeps `safe_stop_executed=false`; STOP-01 should own actual generation termination.
