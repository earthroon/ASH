# ASH text qwave phase1 cheon-ji-in patch

Status: applied to source tree

Scope:
- crates/tokenizer_core/src/hangul_tensor.rs
- crates/tokenizer_core/src/structure_tensor.rs
- crates/text_kernel/src/types.rs
- crates/text_kernel/src/observer.rs

Phase1 rules:
- No WGSL uniform change
- No burn_webgpu backend struct expansion
- No runtime prompt contract rewrite
- SSOT stays in structure observation plus text qwave hints

Applied changes:
1. Added cheon_core, ji_support, in_bridge, axis_bits to HangulFeatureRow.
2. Added cheon/ji/in LUT driven derivation at hangul feature build time.
3. Added cheon_core_mean, ji_support_mean, in_bridge_mean, binding_energy_mean to StructureTensorObservation.
4. Added cheon/ji/in gains to DensityControlParams.
5. Added cheon_core_mean, ji_support_mean, in_bridge_mean, binding_energy_mean, clarity_pressure to TextQWaveInferenceHints.
6. Added clarity_pressure and binding_energy recomposition in observe_text_kernel().
7. Routed the new energy axes into density gate and shader_weight_scale.

Not applied in phase1:
- text_density_gate.rs uniform expansion
- text_density_gate.wgsl changes
- direct GPU side cheon/ji/in fields

Validation note:
- Structural patch applied and cross-reference sweep completed.
- Rust toolchain was not available in the execution environment, so cargo check was not run here.
