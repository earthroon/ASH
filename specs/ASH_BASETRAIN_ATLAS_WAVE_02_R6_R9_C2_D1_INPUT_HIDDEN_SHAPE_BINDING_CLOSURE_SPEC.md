# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C2-D1

## Input Hidden Shape Evidence Binding Closure / Lease-Captured BQH Variable Adoption / Coordinator Evidence Truth Preservation Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C2`  
> Observed compile failure: unresolved local value `input_hidden_shape_bqh` in `base_train_atlas_wave_02_r6_r8_layer1_live_body.rs`  
> Failure class: local evidence-construction binding mismatch  
> Runtime decoder semantics: unchanged  
> Coordinator evidence semantics: unchanged  
> Proof ledger: `HOLD` until Cargo/WGPU rerun

## 1. Failure

The C2 implementation correctly captures the hidden lease semantic BQH shape as:

```rust
let input_hidden_lease_shape_bqh = hidden_lease.captured_semantic_shape_bqh;
```

and validates the live input tensor shape against that lease-captured authority:

```rust
input_shape_bqh == input_hidden_lease_shape_bqh
```

However the later `R6R8LayerExecutionEvidence` initializer used field-init shorthand:

```rust
input_hidden_shape_bqh,
```

No local variable with that name exists in the function scope, so Rust reports `E0425`.

## 2. Closure

Bind the typed evidence field explicitly to the already-authoritative lease-captured local:

```rust
input_hidden_shape_bqh: input_hidden_lease_shape_bqh,
```

No new value, fallback, cast, copied geometry, or recomputation is introduced.

## 3. SSOT preservation

The input-hidden geometry chain remains:

```text
LayerHiddenExecutionLease.captured_semantic_shape_bqh
  -> input_hidden_lease_shape_bqh
  -> live tensor shape equality gate
  -> R6R8LayerExecutionEvidence.input_hidden_shape_bqh
  -> R6R9 runtime geometry truth
```

Therefore C2 still derives runtime compared scalar count from live typed hidden evidence rather than from a fixture constant.

## 4. Non-goals

D1 does not change:

```text
R6-R5 W5/W6/W7 dispatch evidence
R6-R8 QKV or continuation execution
R6-R9 dispatch aggregation
weight pointer provenance
hidden pointer provenance
weight/hidden generation lineage
step completion digest
AtlasParallelStreamingWaveMap
C1 Layer-2 single-step window
checkpoint loader
WGSL
CLI
```

The compiler warning:

```text
unused import: bail
```

is non-blocking and outside this D1 semantic closure. It must not be confused with the E0425 failure.

## 5. Changed source

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
```

The distributed overlay preserves the C2/D3 binary-local dependency closure so this corrected source cannot be applied against an older runtime surface.

## 6. Static validation

```text
undefined shorthand `input_hidden_shape_bqh,` in evidence initializer = 0
explicit lease-shape evidence binding = 1
lease-captured BQH local declaration = 1
live input-shape equality against lease BQH = present
R6-R9 fixed 65536 factual authority = 0
R6-R9 arithmetic synthetic execution truth = 0
R6-R9 json! artifact construction = 0
recursion_limit workaround = 0
WGSL semantic changed file count = 0
.md in code ZIPs = 0
.sha256 in code ZIPs = 0
manifest JSON in code ZIPs = 0
artifacts/ in code ZIPs = 0
manifests/ in code ZIPs = 0
```

Cargo/rustc are unavailable in the bake environment. Compile and physical WGPU admission remain operator-side gates.

## 7. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## Seal

> C2-D1 does not manufacture a new input shape. It binds the evidence field to the BQH shape already captured and validated by the hidden execution lease.
