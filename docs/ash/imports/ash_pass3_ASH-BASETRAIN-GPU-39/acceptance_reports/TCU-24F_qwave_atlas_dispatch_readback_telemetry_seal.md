# TCU-24F — QWave Atlas Dispatch / Readback Telemetry Seal

## Status

`PASS_STATIC_TCU_24F_WITH_NATIVE_TESTS_NOT_RUN`

## SSOT

Input SSOT: `ash_pass3_TCU-24E_qwave_atlas_parity_legacy_comparison_baked.zip`

TCU-24F uses the TCU-24E QWave atlas parity report as source evidence and adds path-level dispatch/readback telemetry. It does not introduce a new QWave math path.

## Sealed paths

1. `LegacyElevenBuffer`
2. `FlatMegaAtlasCandidate`
3. `ScalarTileAtlas8x8Candidate`
4. `Vec4TileAtlas8x8Candidate`
5. `Vec4TileAtlas8x8StagedCandidate`

## Acceptance criteria

- TCU-24E parity report is the source of telemetry.
- Legacy output/readback buffer count is sealed as 11.
- Flat/scalar/vec4/staged atlas output/readback buffer count is sealed as 1.
- Path telemetry events contain sequence/hash linkage.
- NotRunAdapterUnavailable is telemetry NotRun, not telemetry failure.
- Readback/deatlasize/parity-link summary is created per path.
- Benchmark mode remains disabled.
- Fastest candidate selection remains disabled.
- Production default remains unchanged.
- Direct replacement remains forbidden.
- TensorCube MatMul replacement remains disabled.
- Subgroup fast path remains disabled.

## Runtime artifacts

- `workspace/runtime/tensorcube/ash_qwave_atlas_telemetry_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_dispatch_events_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_readback_summary_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_telemetry_report_latest.json`

## Native test status

Rust/native WGPU tests were not executed in this container because `cargo` / `rustc` are unavailable.
