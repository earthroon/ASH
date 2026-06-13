# QW-52A-R2 Bake Report

## Result
Static bake completed.

## Added / changed
- `crates/model_core/src/cheonjiin_projection_input_bridge.rs`
- `crates/lora_train/src/qwave_conditioning_cheonjiin_projection_bridge.rs`
- `crates/lora_train/src/bin/qw52a_r2_projection_rebind_validate.rs`
- `crates/model_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/model_core/src/hangul_qwave_candidate_awareness.rs`

## Validation
- Static validation: PASS
- Zip integrity: pending at packaging time
- Cargo check: NOT RUN - cargo unavailable in bake environment
- Runtime probe: NOT RUN - cargo unavailable in bake environment

## Safety
- Projection dry-run is existing-source rebind only.
- No Python analyzer/validator was added.
- No WGSL shader was added.
- No hidden-state fusion was applied.
