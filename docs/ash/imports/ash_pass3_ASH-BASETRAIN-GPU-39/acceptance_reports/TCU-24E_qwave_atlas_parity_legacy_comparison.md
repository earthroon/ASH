# TCU-24E — QWave Atlas Parity / Legacy Comparison

## SSOT
- Baseline path: `LegacyElevenBuffer`
- Candidate paths: `FlatMegaAtlasCandidate`, `ScalarTileAtlas8x8Candidate`, `Vec4TileAtlas8x8Candidate`, `Vec4TileAtlas8x8StagedCandidate`
- State owner: `crates/burn_webgpu_backend/src/qwave_atlas_parity.rs`

## Acceptance
1. Legacy 11-buffer output remains the baseline.
2. TCU-24A flat mega atlas output is compared against legacy when native dispatch is available.
3. TCU-24B scalar tile atlas output is compared against legacy when native dispatch is available.
4. TCU-24C vec4 tile atlas output is compared against legacy when native dispatch is available.
5. TCU-24D staged vec4 tile atlas output is compared against legacy when native dispatch is available.
6. Deterministic QWave parity fixture is generated from a sealed seed.
7. 11 QWave maps are all supported by `qwave_maps_field_slice()`.
8. Map comparisons record max abs error, max relative error, mean abs error, and mismatch count.
9. NaN and Infinity are parity failures.
10. Adapter-unavailable is NotRun, not mismatch.
11. `portable_parity_pass` and `strict_native_parity_pass` are separated.
12. Static atlas/deatlasize roundtrip parity is available without GPU.
13. Production default is unchanged.
14. Direct replacement is forbidden.
15. Fastest candidate selection is forbidden.
16. Benchmark mode is disabled.
17. TensorCube MatMul replacement is disabled.
18. Subgroup fast path is disabled.

## Runtime artifacts
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_fixture_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_comparison_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_report_latest.json`

## Seal
TCU-24E may observe and compare. It must not select, promote, mutate, benchmark, or replace.
