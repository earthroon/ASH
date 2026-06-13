# 16AI-QW-38G-R6A-MINP-P0 — Min-P Sampling SSOT / Canonical Decode Config Seal

## Status

- status: `MINP_SSOT_DEFINED`
- canonical field: `min_p`
- canonical owner: `RuntimeSamplingConfig.min_p`
- source patch: `16AI-QW-38G-R6A-LORA-RT-02B-F`

## Implemented

- Added `GenerateConfig.min_p: Option<f32>` as the request/config intake slot, with serde aliases `minP`, `samplingMinP`, and `sampling_min_p`.
- Added `RuntimeSamplingConfig.min_p: AppliedField<f32>` with a disabled default of `Applied(0.0)`.
- Added `normalize_min_p(value: f32) -> f32` with NaN/Inf coercion to `0.0` and clamp range `0.0..=0.95`.
- Lowered `GenerateConfig.min_p` into `RuntimeSamplingConfig.min_p` in the runtime engine bootstrap.
- Removed the active runtime `causal_lm.rs` fixed `min_p: None` bridge and replaced it with canonical runtime sampling state.
- Switched infer/orchestrator normalization sites to use the canonical `normalize_min_p` helper.
- Added `min_p` / `applied_min_p` telemetry fields to `GenerateEvent::AshGate`.
- Mirrored the type surface into archived `runtime_unz` to prevent schema drift, without making it canonical.

## Non-scope deliberately preserved

- No GPU shader semantics change.
- No CPU fallback sampler implementation.
- No desktop UI slider or `model.generate` infer-path rewire.
- No top-p active-set renormalization change.

## Validation

Static pattern checks passed: `True`

`cargo check` and `cargo fmt` were not run because `cargo` / `rustfmt` are not installed in this execution container.

See `workspace/minp_p0_ssot_summary.json` for machine-readable validation.
