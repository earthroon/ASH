# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C4

## Exact Parity API / Positive Relative-Floor Canonicalization / Zero-over-Zero NaN Retirement Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C3`  
> Observed failure: `HeadwiseOutputParityRelativeFloorInvalid`  
> Failure position: deterministic replay context comparison  
> BaseTrain live admission: `HOLD` until physical rerun

## 0. Observed failure

The R6-R6 live-body gate reached the deterministic replay comparison after native bootstrap and micro-atlas streaming, then called the shared parity pipeline with:

```text
absolute tolerance = 0
relative tolerance = 0
relative floor = 0
```

The shared pipeline correctly rejected the non-positive relative floor:

```text
HeadwiseOutputParityRelativeFloorInvalid
```

## 1. Root cause

R6-R6 used the tolerance-oriented `compare()` API for three bit-exact comparisons:

```text
live context vs deterministic replay context
live final hidden vs deterministic replay final hidden
committed layer-1 hidden vs published layer-1 hidden
```

The exact comparisons do not need a relative tolerance envelope, but the WGSL still computes a relative-error statistic:

```text
absolute_error / max(max(abs(a), abs(b)), relative_floor)
```

A zero floor permits `0 / 0` for equal zero-valued elements. Even though absolute tolerance zero would still enforce exact equality, the relative statistic could become NaN and the host admission rejected the call before dispatch.

## 2. Repair

A dedicated exact-comparison API is added:

```rust
HeadwiseOutputParityPipeline::compare_exact(...)
```

Canonical exact parameters:

```text
absolute tolerance = 0
relative tolerance = 0
relative floor = f32::MIN_POSITIVE
```

`f32::MIN_POSITIVE` is not an accuracy tolerance. It is the smallest positive normal denominator floor used only to keep the diagnostic relative-error calculation finite for equal zeros.

Exact pass authority remains:

```text
absolute_error must equal 0 for every element
non-finite input count must equal 0
compared element count must equal expected element count
```

## 3. Preserved shared contract

The existing tolerance-oriented `compare()` API is not weakened.

```text
relative_floor > 0 remains mandatory
absolute tolerance validation unchanged
relative tolerance validation unchanged
WGSL unchanged
bind groups unchanged
compact readback unchanged
payload readback count remains 0
```

No arbitrary epsilon is repeated at R6-R6 call sites.

## 4. R6-R6 call-site migration

The following comparisons now call `compare_exact()`:

```text
replay context parity
replay final-hidden parity
layer-1 publication parity
```

The reference-vs-live final-hidden comparison continues to use CLI-specified absolute tolerance, relative tolerance and relative floor through `compare()`.

## 5. Changed source

```text
crates/burn_webgpu_backend/src/headwise_output_parity.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
```

## 6. Preserved runtime semantics

```text
micro-atlas tile-map streaming unchanged
actual checkpoint decoder block unchanged
QKV/W4/W5/W6/W7 unchanged
OProj and MLP unchanged
layer-1 hidden CAS unchanged
Headwise rollback-only policy unchanged
receipt wave-map unchanged
no backward or optimizer
```

## 7. Static validation

```text
R6-R6 exact comparison call count = 3
R6-R6 exact comparison zero-floor call count = 0
compare_exact canonical floor = f32::MIN_POSITIVE
shared compare positive-floor guard retained = PASS
WGSL modification count = 0
changed-hunk delimiter balance = PASS
ZIP integrity = PASS
.sha256 sidecar count = 0
```

Cargo type-check and physical GPU execution remain user-side gates.

## 8. Commands

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
