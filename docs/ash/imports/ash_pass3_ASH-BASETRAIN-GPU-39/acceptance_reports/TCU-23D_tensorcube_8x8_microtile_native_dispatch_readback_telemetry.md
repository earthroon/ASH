# TCU-23D — TensorCube 8x8 MicroTile Native Dispatch / Readback Telemetry Seal

## Status

`PASS_STATIC_TCU_23D_WITH_NATIVE_TESTS_NOT_RUN`

## SSOT

Base ZIP: `ash_pass3_TCU-23C_tensorcube_8x8_microtile_native_wgpu_smoke_baked.zip`

TCU-23D adds an observational telemetry layer over TCU-23C native WGPU smoke output.

## Scope

TCU-23D seals:

1. dispatch telemetry config
2. Vec4Atlas phase event chain
3. WorkgroupTile phase event chain
4. readback shape telemetry
5. CPU comparison telemetry fields
6. NotRun adapter telemetry
7. no-benchmark / no-production guard

## Explicit Non-Scope

TCU-23D does not enable:

- production inference dispatch
- SFT-GPU-8H pass1 replacement
- runtime inference replacement
- backend policy connection
- TCU-22 policy candidate connection
- LoRA attach/detach
- hot reload
- safe tensor mode direct apply
- subgroup fast path
- readback-free benchmark
- GPU timestamp query by default
- contiguous 16x16 tile creation

## Acceptance Criteria

- TCU-23C native smoke report is used as telemetry source.
- Vec4Atlas dispatch phase telemetry is generated.
- WorkgroupTile dispatch phase telemetry is generated.
- adapter unavailable is sealed as NotRun telemetry.
- adapter unavailable is not dispatch/readback failure.
- phase events carry sequence_no / previous_event_hash / event_hash.
- reason / failures / warnings are excluded from phase event hash source.
- buffer byte accounting is recorded.
- workgroup size and dispatch workgroup shape are recorded.
- readback buffer size is sealed as 256 bytes.
- readback expected vec4 count is sealed as 16.
- readback expected scalar count is sealed as 64.
- NaN / Infinity readback is failure.
- CPU reference comparison result is represented in telemetry.
- host phase timing is allowed; GPU timestamp query remains disabled by default.
- benchmark mode remains false.
- production dispatch remains false.
- SFT-GPU-8H pass1 replacement remains false.
- runtime inference replacement remains false.
- backend policy connection remains false.
- subgroup fast path remains false.
- contiguous 16x16 tile creation remains false.
- runtime JSON artifacts are emitted under `workspace/runtime/tensorcube`.

## Runtime Artifacts

- `workspace/runtime/tensorcube/ash_tensorcube_microtile_dispatch_telemetry_config_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_microtile_dispatch_phase_telemetry_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_microtile_readback_telemetry_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_microtile_dispatch_telemetry_report_latest.json`

## Verification Commands

```bash
cargo test -p burn_webgpu_backend tcu_23d_dispatch_telemetry_config_gate
cargo test -p burn_webgpu_backend tcu_23d_dispatch_phase_event_seal
cargo test -p burn_webgpu_backend tcu_23d_readback_telemetry_shape
cargo test -p burn_webgpu_backend tcu_23d_telemetry_notrun_status
cargo test -p burn_webgpu_backend tcu_23d_no_benchmark_or_production_dispatch
cargo test -p orchestrator_local tcu_23d_tensorcube_microtile_dispatch_telemetry_report
cargo run -p orchestrator_local --bin tcu_23d_tensorcube_microtile_dispatch_telemetry_audit
```

## Native Test Note

This bake environment has no `cargo` / `rustc`, so native Rust tests were not executed here. Static file presence and guard checks were performed instead.
