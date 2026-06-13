# TCU-23E — TensorCube 8x8 MicroTile Readback-Free Timing Probe / Benchmark Guard

## Status

`PASS_STATIC_TCU_23E_WITH_NATIVE_TESTS_NOT_RUN`

## SSOT

Base ZIP:

`ash_pass3_TCU-23D_tensorcube_8x8_microtile_native_dispatch_readback_telemetry_baked.zip`

TCU-23E adds a readback-free timing probe and benchmark guard on top of TCU-23D telemetry.

## Scope

TCU-23E introduces:

- `TensorCubeMicroTileTimingProbeConfig`
- `TensorCubeMicroTileTimingProbeDescriptor`
- `TensorCubeMicroTileTimingSample`
- `TensorCubeMicroTileTimingSummary`
- `TensorCubeMicroTileTimingProbeReport`
- readback-free timing probe guard
- advisory-only faster-kernel observation field
- NotRun adapter-unavailable seal for environments without native WGPU

## Contract

```text
TCU-23E measures dispatch timing without readback.
It does not select, promote, replace, or mutate production runtime behavior.
```

## Guarded off

The following remain sealed as `false`:

- `fastest_kernel_selection_allowed`
- `production_dispatch_allowed`
- `sft_pass1_replacement_allowed`
- `runtime_inference_replacement_allowed`
- `backend_policy_connection_allowed`
- `subgroup_fast_path_enabled`
- `creates_contiguous_16x16_tile`

## Readback-free boundary

TCU-23E is not a correctness authority.
Correctness authority remains with:

- TCU-23B CPU/WGSL parity contract
- TCU-23C native smoke comparison
- TCU-23D dispatch/readback telemetry seal

TCU-23E keeps:

- `readback_enabled = false`
- `output_validation_enabled = false`

## Runtime outputs

- `workspace/runtime/tensorcube/ash_tensorcube_microtile_timing_probe_config_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_microtile_vec4_timing_probe_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_microtile_workgroup_timing_probe_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_microtile_timing_probe_report_latest.json`

## Acceptance criteria

1. TCU-23D dispatch/readback telemetry report is treated as prior evidence.
2. Missing prior telemetry blocks timing probe when required.
3. Readback-free timing probe config is added.
4. `readback_enabled` is fixed to `false`.
5. `output_validation_enabled` is fixed to `false`.
6. Vec4Atlas timing probe descriptor is generated.
7. WorkgroupTile timing probe descriptor is generated.
8. Warmup iterations and sample iterations are separated.
9. Warmup samples are excluded from timing summary statistics.
10. Only passed non-warmup samples are included in min/max/mean/median statistics.
11. `NotRunAdapterUnavailable` is not treated as benchmark failure.
12. GPU timestamp query is disabled by default.
13. Timestamp query is only allowed as feature-gated experimental path.
14. `advisory_faster_kernel` can be recorded.
15. `advisory_faster_kernel` cannot be used for production selection.
16. `fastest_kernel_selection_allowed` is false.
17. Production dispatch remains closed.
18. SFT-GPU-8H pass1 replacement remains closed.
19. Runtime inference replacement remains closed.
20. Backend policy connection remains closed.
21. Subgroup fast path remains closed.
22. Contiguous 16x16 tile creation remains closed.
23. Runtime JSON outputs are created.

## Native execution

Native tests were not run in this container because `cargo` / `rustc` are unavailable.

Expected commands in a Rust-capable environment:

```bash
cargo test -p burn_webgpu_backend tcu_23e_timing_probe_config_gate
cargo test -p burn_webgpu_backend tcu_23e_readback_free_probe_guard
cargo test -p burn_webgpu_backend tcu_23e_timing_sample_summary
cargo test -p burn_webgpu_backend tcu_23e_timestamp_query_feature_gate
cargo test -p burn_webgpu_backend tcu_23e_no_production_selection
cargo test -p orchestrator_local tcu_23e_tensorcube_microtile_timing_probe_report
cargo run -p orchestrator_local --bin tcu_23e_tensorcube_microtile_timing_probe_audit
```
