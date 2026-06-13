# 16AI-QW-38G-R6A-DECODE-03E Report

## Seal
Dynamic Guard Strength Runtime Overlay Apply Seal

## SSOT
SALAD-04 overlay recommendation + DECODE-03D applied config + EVAL-01 backend parity status.

## Implemented files
- `crates/model_core/src/decode03e_guard_overlay.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampler_parity.rs`
- `workspace/decode03e_guard_overlay_schema.json`
- `workspace/decode03e_steps.jsonl`
- `workspace/decode03e_summary.json`
- `workspace/decode03e_static_checks.json`

## Contracts
- Default mode is `Off`.
- `ShadowOnly` computes overlay but does not apply behavior changes.
- `ControlledApply` / `StrictControlledApply` require `behavior_change_allowed=true`.
- Overlay is step-local only.
- Base decode config mutation is forbidden.
- Panic candidate execution is forbidden.
- Rollback/stop execution is forbidden in DECODE-03E.
- Unsupported backend features cannot be recorded as applied.

## Runtime env
```bash
ASH_DECODE03E_MODE=controlled_apply \
ASH_DECODE03E_BEHAVIOR_CHANGE_ALLOWED=true \
ASH_DECODE03E_REQUIRE_SALAD04=true \
ASH_DECODE03E_REQUIRE_EVAL01_SEMANTIC_PARITY=true \
ASH_DECODE03E_STEP_LOCAL_OVERLAY=true \
ASH_DECODE03E_RECEIPT=workspace/decode03e_steps.jsonl \
ASH_DECODE03E_SUMMARY=workspace/decode03e_summary.json
```

## Status
Static bake only. Cargo/runtime smoke was not executed in this container.
