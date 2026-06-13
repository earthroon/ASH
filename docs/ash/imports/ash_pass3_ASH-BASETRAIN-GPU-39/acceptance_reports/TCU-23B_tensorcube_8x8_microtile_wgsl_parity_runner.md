# TCU-23B — TensorCube 8x8 MicroTile WGSL Parity Runner / CPU Reference Comparison

## Status

`PASS_STATIC_TCU_23B_PORTABLE_CPU_REFERENCE_ONLY`

## SSOT

Input SSOT ZIP:

`ash_pass3_TCU-23A_tensorcube_8x8_atlas_microtile_kernel_consolidation_baked.zip`

TCU-23B extends the TCU-23A 8x8 Vec4F32 atlas microtile layout and adds a parity runner contract.

## Scope

TCU-23B adds:

1. deterministic 8x8 parity fixture generation
2. 8x8 tile pack/unpack to 16 `vec4<f32>` atlas entries
3. CPU scalar 8x8 matmul reference execution
4. WGSL vec4 parity runner contract
5. WGSL workgroup parity runner contract
6. tolerance-based comparison against CPU reference
7. NotRun status separation for adapter/runner unavailable environments
8. portable pass vs strict GPU parity pass distinction

## Explicit Non-Scope

TCU-23B does not enable:

- production dispatch
- SFT-GPU-8H pass1 replacement
- runtime inference replacement
- backend policy mutation
- LoRA attach/detach or hot reload wiring
- safe tensor mode application
- subgroup fast path by default
- contiguous 16x16 tile creation

## Completion Criteria

- TCU-23A 8x8 Vec4F32 layout is reused.
- Deterministic fixture includes A/B 8x8 tiles and expected C tile.
- Tile pack/unpack preserves 16 vec4 layout.
- CPU scalar reference produces 8x8 matmul output.
- WGSL vec4 parity shader fixture is added.
- WGSL workgroup parity shader fixture is added.
- Adapter unavailable is recorded as NotRun, not Failed.
- Runner unavailable and adapter unavailable states are distinct.
- CPU reference and candidate output comparison supports abs/rel tolerance.
- NaN/Infinity are treated as parity failures.
- `portable_pass` and `strict_gpu_parity_pass` are separate.
- Production dispatch remains disabled.
- SFT pass1 replacement remains disabled.
- Runtime inference replacement remains disabled.
- Subgroup fast path remains disabled by default.
- No contiguous 16x16 tile is created.
- Runtime JSON artifacts are emitted under `workspace/runtime/tensorcube`.

## Added Files

```text
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_parity.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_vec4.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_workgroup.wgsl
crates/burn_webgpu_backend/tests/tcu_23b_microtile_fixture_pack_unpack.rs
crates/burn_webgpu_backend/tests/tcu_23b_microtile_cpu_reference_comparison.rs
crates/burn_webgpu_backend/tests/tcu_23b_microtile_parity_tolerance.rs
crates/burn_webgpu_backend/tests/tcu_23b_microtile_runner_status_gate.rs
crates/burn_webgpu_backend/tests/tcu_23b_no_production_dispatch.rs
crates/orchestrator_local/src/tcu_23b_tensorcube_microtile_parity_report.rs
crates/orchestrator_local/src/bin/tcu_23b_tensorcube_microtile_parity_audit.rs
crates/orchestrator_local/tests/tcu_23b_tensorcube_microtile_parity_report.rs
```

## Runtime Artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_microtile_parity_fixture_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_cpu_reference_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_wgsl_vec4_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_wgsl_workgroup_parity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_parity_report_latest.json
```

## Native Test Commands

```bash
cargo test -p burn_webgpu_backend tcu_23b_microtile_fixture_pack_unpack
cargo test -p burn_webgpu_backend tcu_23b_microtile_cpu_reference_comparison
cargo test -p burn_webgpu_backend tcu_23b_microtile_parity_tolerance
cargo test -p burn_webgpu_backend tcu_23b_microtile_runner_status_gate
cargo test -p burn_webgpu_backend tcu_23b_no_production_dispatch
cargo test -p orchestrator_local tcu_23b_tensorcube_microtile_parity_report
cargo run -p orchestrator_local --bin tcu_23b_tensorcube_microtile_parity_audit
```

## Native Test Status

Native Rust tests were not executed in this bake environment because `cargo` / `rustc` are unavailable.

Static audit status:

`PASS_STATIC_TCU_23B_WITH_NATIVE_TESTS_NOT_RUN`
