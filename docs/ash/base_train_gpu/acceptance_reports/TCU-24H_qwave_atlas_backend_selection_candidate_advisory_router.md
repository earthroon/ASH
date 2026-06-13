# TCU-24H — QWave Atlas Backend Selection Candidate / Advisory Router

## SSOT

- Source parity: `crates/burn_webgpu_backend/src/qwave_atlas_parity.rs`
- Source telemetry: `crates/burn_webgpu_backend/src/qwave_atlas_telemetry.rs`
- Source timing: `crates/burn_webgpu_backend/src/qwave_atlas_timing_probe.rs`
- New advisory router: `crates/burn_webgpu_backend/src/qwave_atlas_backend_router.rs`

## Acceptance status

`PASS_STATIC_TCU_24H_WITH_NATIVE_TESTS_NOT_RUN`

## Fixed safety contract

TCU-24H may rank and nominate an advisory candidate. It must not apply, switch, mutate production defaults, or replace runtime behavior.

Fixed flags:

```text
router_mode = AdvisoryOnly
advisory_decision_allowed = true
backend_switch_allowed = false
production_default_change_allowed = false
direct_replacement_allowed = false
runtime_apply_allowed = false
backend_policy_mutation_allowed = false
tensorcube_matmul_replacement_enabled = false
subgroup_fast_path_enabled = false
```

## Candidate paths

1. `LegacyElevenBuffer`
2. `FlatMegaAtlasCandidate`
3. `ScalarTileAtlas8x8Candidate`
4. `Vec4TileAtlas8x8Candidate`
5. `Vec4TileAtlas8x8StagedCandidate`

## Evidence inputs

TCU-24H consumes:

- TCU-24E `QWaveAtlasParityReport`
- TCU-24F `QWaveAtlasTelemetryReport`
- TCU-24G `QWaveAtlasTimingProbeReport`

It produces:

- `QWaveAtlasBackendCandidateEvidence`
- `QWaveAtlasBackendCandidateScore`
- `QWaveAtlasBackendAdvisoryDecision`
- `QWaveAtlasBackendRouterReport`

## Completion criteria

- Source evidence status is classified deterministically.
- Each QWave path gets a candidate evidence bundle.
- Correctness, telemetry, timing, stability, and safety scores are computed.
- Candidate ranking is deterministic.
- `fallback_path` is fixed to `LegacyElevenBuffer`.
- `eligible_for_apply` is always false.
- Advisory candidate may be produced only when source evidence and score gates pass.
- Portable/not-run source evidence produces a sealed not-run report, not a production switch.
- Runtime JSON fixtures are emitted under `workspace/runtime/tensorcube`.
