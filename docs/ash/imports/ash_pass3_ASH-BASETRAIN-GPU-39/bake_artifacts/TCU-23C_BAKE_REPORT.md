# TCU-23C Bake Report

## Commit

`TCU-23C — TensorCube 8x8 MicroTile Native WGPU Smoke Runner / Adapter-Gated Dispatch`

## Result

`PASS_STATIC_TCU_23C_WITH_NATIVE_TESTS_NOT_RUN`

## Summary

This bake adds a native WGPU smoke runner for the TensorCube 8x8 microtile parity shaders introduced in TCU-23B.
The runner is adapter-gated and readback-only. It can dispatch the vec4 atlas shader and the workgroup tile shader when a native WGPU adapter is available, then compare the readback result against the CPU scalar reference.

The bake intentionally preserves all non-production gates.

## Production Gates

```text
production_dispatch_allowed = false
sft_pass1_replacement_allowed = false
runtime_inference_replacement_allowed = false
backend_policy_connection_allowed = false
subgroup_fast_path_enabled = false
creates_contiguous_16x16_tile = false
```

## Runtime Outputs

```text
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_smoke_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_vec4_smoke_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_workgroup_smoke_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_native_smoke_report_latest.json
```

## Native Test Status

Rust-native tests were not executed in this container because `cargo` / `rustc` are unavailable.

Recommended verification:

```bash
cargo test -p burn_webgpu_backend tcu_23c_native_smoke_config_gate
cargo test -p burn_webgpu_backend tcu_23c_native_smoke_adapter_status
cargo test -p burn_webgpu_backend tcu_23c_native_smoke_result_comparison
cargo test -p burn_webgpu_backend tcu_23c_native_smoke_no_production_dispatch
cargo test -p orchestrator_local tcu_23c_tensorcube_microtile_native_smoke_report
cargo run -p orchestrator_local --bin tcu_23c_tensorcube_microtile_native_smoke_audit
```
