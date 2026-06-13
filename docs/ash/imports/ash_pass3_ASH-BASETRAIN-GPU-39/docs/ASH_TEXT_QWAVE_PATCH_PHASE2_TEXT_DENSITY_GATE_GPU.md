# ASH text qwave phase2 text density gate GPU patch

Status: applied to source tree

Scope:
- crates/burn_webgpu_backend/src/text_density_gate.rs
- crates/burn_webgpu_backend/src/shaders/text_density_gate.wgsl
- crates/model_core/src/lib.rs
- crates/runtime/src/infer.rs

Phase2 rules:
- Expand GPU-side uniform to carry cheon/ji/in energy axes
- Keep phase1 SSOT as the source of truth
- Route only derived hint values into the GPU gate
- Avoid introducing a second text-only state contract outside TextQWaveInferenceHints

Applied changes:
1. Expanded TextDensityGateUniform and raw GPU layout with cheon_core_mean, ji_support_mean, in_bridge_mean, binding_energy_mean, clarity_pressure.
2. Extended WGSL uniform struct to 16 scalar slots for stable packing.
3. Added GPU-side selected lane derivation from binding_energy_mean, clarity_pressure, cheon_core_mean, in_bridge_mean.
4. Added GPU-side density multiplier boosts from the new cheon/ji/in energy axes.
5. Added model_core configure_text_density_gate() parameters and NativeTextDensityState fields for the new axes.
6. Updated runtime infer wiring so text hints pass the new values into the native text density gate.

Not changed in phase2:
- tokenizer_core phase1 derivation logic
- text_kernel phase1 clarity and binding recomposition logic
- probe buffer schema or orchestration JSON output fields

Validation note:
- Source tree patch applied and cross-reference sweep completed.
- Rust toolchain was not available in the execution environment, so cargo check was not run here.
