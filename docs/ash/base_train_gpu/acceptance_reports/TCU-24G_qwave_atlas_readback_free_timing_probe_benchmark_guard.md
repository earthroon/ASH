# TCU-24G — QWave Atlas Readback-Free Timing Probe / Benchmark Guard

## 확정

TCU-24G adds a readback-free timing probe layer over the TCU-24F QWave atlas dispatch/readback telemetry seal.

Observed paths:

1. LegacyElevenBuffer
2. FlatMegaAtlasCandidate
3. ScalarTileAtlas8x8Candidate
4. Vec4TileAtlas8x8Candidate
5. Vec4TileAtlas8x8StagedCandidate

## Contract

- Source telemetry: TCU-24F `QWaveAtlasTelemetryReport`
- Readback: disabled
- Output validation: disabled
- Benchmark result: advisory-only
- Fastest candidate selection: forbidden
- Production default mutation: forbidden
- Backend router activation: forbidden
- TensorCube MatMul replacement: forbidden
- Subgroup fast path: forbidden

## Completion checklist

- `qwave_atlas_timing_probe.rs` added.
- Timing config, descriptor, sample, summary, advisory comparison, and report types added.
- Source telemetry guard validates TCU-24F `telemetry_seal_pass`.
- Readback and output validation are blocked when enabled.
- Timing sample hash chain uses `sample_sequence_no`, `previous_sample_hash`, and `sample_hash`.
- Warmup samples are excluded from timing summary statistics.
- NotRunAdapterUnavailable is not treated as benchmark failure.
- Runtime JSON fixtures are generated under `workspace/runtime/tensorcube`.

## Status

`PASS_STATIC_TCU_24G_WITH_NATIVE_TESTS_NOT_RUN`
