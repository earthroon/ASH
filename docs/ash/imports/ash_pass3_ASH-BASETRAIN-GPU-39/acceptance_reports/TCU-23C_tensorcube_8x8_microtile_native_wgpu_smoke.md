# TCU-23C — TensorCube 8x8 MicroTile Native WGPU Smoke Runner / Adapter-Gated Dispatch

## Status

`PASS_STATIC_TCU_23C_WITH_NATIVE_TESTS_NOT_RUN`

## SSOT

TCU-23C is based on the TCU-23B parity runner bake.

TCU-23C lowers the TCU-23B WGSL parity contract into an adapter-gated native WGPU smoke runner.
It does not promote the TensorCube 8x8 microtile kernels into production inference, SFT pass1, backend policy, LoRA, hot reload, safe tensor mode, subgroup fast path, or contiguous 16x16 paths.

## Contract

```text
TCU-23B parity fixture
↓
CPU scalar 8x8 reference
↓
TCU-23C native adapter gate
↓
vec4 WGSL smoke dispatch, when adapter exists
workgroup WGSL smoke dispatch, when adapter exists
↓
readback output-only C atlas
↓
CPU tolerance comparison
```

## Acceptance Criteria

1. TCU-23B parity fixture is reused.
2. TCU-23B CPU reference is reused.
3. TCU-23B vec4 parity WGSL shader can be dispatched by the native WGPU smoke runner when an adapter is available.
4. TCU-23B workgroup parity WGSL shader can be dispatched by the native WGPU smoke runner when an adapter is available.
5. Adapter absence is recorded as `NotRunAdapterUnavailable`.
6. Adapter absence is not treated as parity mismatch.
7. `require_native_adapter = true` turns adapter absence into a blocked environment state, not a silent pass.
8. Vec4 smoke preserves 16 `vec4<f32>` slots and 256-byte A/B/C buffers.
9. Workgroup smoke preserves the 64-lane 8x8 tile reference contract.
10. Native GPU readback output is compared against the CPU reference with abs/rel tolerance.
11. NaN and Infinity output are failures.
12. Output vec4 length mismatch is a failure.
13. Production dispatch remains disabled.
14. SFT-GPU-8H pass1 replacement remains disabled.
15. Runtime inference replacement remains disabled.
16. Backend policy connection remains disabled.
17. Subgroup fast path remains disabled.
18. Contiguous 16x16 tile creation remains disabled.
19. Runtime JSON artifacts are emitted under `workspace/runtime/tensorcube`.

## Added Files

```text
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_native_smoke.rs
crates/burn_webgpu_backend/tests/tcu_23c_native_smoke_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_23c_native_smoke_adapter_status.rs
crates/burn_webgpu_backend/tests/tcu_23c_native_smoke_result_comparison.rs
crates/burn_webgpu_backend/tests/tcu_23c_native_smoke_no_production_dispatch.rs
crates/orchestrator_local/src/tcu_23c_tensorcube_microtile_native_smoke_report.rs
crates/orchestrator_local/src/bin/tcu_23c_tensorcube_microtile_native_smoke_audit.rs
crates/orchestrator_local/tests/tcu_23c_tensorcube_microtile_native_smoke_report.rs
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_smoke_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_vec4_smoke_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_workgroup_smoke_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_smoke_report_latest.json
```

## Safety Seal

```text
Adapter unavailable is not smoke failure.
Dispatch mismatch is smoke failure.
Production path connection is forbidden.
```

## Not Run

The current bake container does not provide `cargo` or `rustc`, so Rust-native tests and actual WGPU dispatch were not executed here.
