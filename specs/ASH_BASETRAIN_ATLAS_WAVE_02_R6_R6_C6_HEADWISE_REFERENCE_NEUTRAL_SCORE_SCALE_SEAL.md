# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C6

## Headwise Reference Neutral Score Scale Seal

Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C5`

Observed failure:

```text
R6R6FinalHiddenParityMismatch:violations=27942:nonfinite=0:max_abs=0.131510913:max_rel=1.998866677:first=Some(2048)
```

## Evidence

For final hidden shape `[1,32,2048]`, linear index `2048` is token 1, lane 0. Token 0 matched completely and token 1 was the first mismatch. In causal attention token 0 sees one key, so score scaling cannot change its softmax result. Token 1 sees multiple keys, so a score-scale mismatch begins exactly at index 2048.

## Root cause

The shared W5/W6/W7 path uses canonical QK scale:

```text
1 / sqrt(64) = 0.125
```

R6-R6 built the Headwise reference from `HeadwiseAtlasRuntimeSpec::default()`. The default text-density uniform uses `density_gate = 0.0`. The Headwise shader clamps that field with `max(density_gate, 0.25)`, so its effective score scale became:

```text
0.125 * 0.25 = 0.03125
```

The physical-PASS R6-R5 parent instead supplied the neutral identity uniform:

```text
density_lane = 0
packed_path_id = 0
shader_weight_scale = 1.0
density_gate = 1.0
cairo_risk_proxy = 0.0
coda_weight_mean = 0.0
curvature_mean = 0.0
active_tensor_zero_copy = 1
```

## Repair

R6-R6 now supplies the same explicit neutral uniform and verifies it fail-closed after preparation. Failure token:

```text
R6R6HeadwiseReferenceScoreScaleNotCanonical
```

Changed runtime source:

```text
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
```

Preserved:

```text
micro-atlas streaming
actual decoder block
QKV and NeoX RoPE
W4/W5/W6/W7
OProj and SwiGLU MLP
layer-1 hidden CAS
strict stage parity
exact replay parity
C5 mixed final-hidden envelope
zero payload readback
```

No tolerance was widened.

## Commands

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r6.args"
```
