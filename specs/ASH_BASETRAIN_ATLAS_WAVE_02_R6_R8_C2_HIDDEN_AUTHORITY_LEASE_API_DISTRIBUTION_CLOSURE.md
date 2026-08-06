# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8-C2

## Hidden Authority Lease API Distribution Closure / Counts·Acquire·Release Surface Reapplication / Commit-While-Read Guard Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8-C1` / Pass31  
> Failure class: dependency source surface not applied  
> Runtime semantics: unchanged  
> Physical admission: `HOLD`

## Observed failure

```text
error[E0599]: no method named `counts` found for struct `LayerHiddenAuthoritySlot`
error[E0599]: no method named `acquire_execution_lease` found for struct `LayerHiddenAuthoritySlot`
```

The R6-R8 consumer compiled from the updated runtime source while the operator-side `model_core/src/base_train_layer_attention_authority.rs` remained on the pre-R6-R8 hidden-authority surface.

## Root cause

Pass31 C1 redistributed the binary-local runtime module chain but did not re-carry the ModelCore hidden-authority source. An installation that missed the Pass30 ModelCore file could therefore compile the new consumer against an older `LayerHiddenAuthoritySlot` implementation.

## Atomic distribution closure

C2 redistributes these files together:

```text
crates/model_core/src/base_train_layer_attention_authority.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate.rs
```

The ModelCore source contains:

```rust
pub struct LayerHiddenAuthorityCounts {
    pub active_execution_lease_count: u32,
}

pub struct LayerHiddenExecutionLease<'a> { /* captured authority lineage */ }

impl LayerHiddenAuthoritySlot {
    pub fn counts(&self) -> Result<LayerHiddenAuthorityCounts>;

    pub fn acquire_execution_lease(
        &self,
        expected_layer: u32,
        expected_generation: u64,
        expected_digest: &str,
    ) -> Result<LayerHiddenExecutionLease<'_>>;
}
```

The lease captures the hidden layer, generation, pointer digest, buffer identity digest, completion token digest, semantic shape and tensor handle. It supports pre-use revalidation, explicit release and Drop fallback release.

`commit_next_layer()` rejects a commit while a hidden read lease remains active:

```text
R6R8HiddenCommitWhileReadLeaseActive
```

## Canonical execution ordering

```text
hidden active lease count = 0
  -> acquire hidden execution lease
  -> execute actual layer-1 body
  -> complete parity and replay gates
  -> wait for GPU completion
  -> release weight lease
  -> release hidden lease
  -> hidden active lease count = 0
  -> commit layer-2 hidden once
```

## Preserved semantics

```text
already-resident layer-1 weight consumption
no re-embedding
no layer-1 weight reload
no layer-1 block rebuild
single layer-1 QKV
shared W5/W6/W7 attention
actual OProj and SwiGLU MLP
single layer-2 hidden commit
payload readback = 0
```

No WGSL, Cargo, CLI, parity envelope, receipt schema, weight residency transition or hidden pointer transition changes.

## Revision identity

```rust
pub const BASE_TRAIN_LAYER_HIDDEN_EXECUTION_LEASE_API_REVISION: &str =
    "ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8-C2";
```

The marker distinguishes the physically applied source without changing runtime state.

## Static validation

```text
static checks = 27 / 27 PASS
LayerHiddenAuthorityCounts present = true
LayerHiddenExecutionLease present = true
counts() present = true
acquire_execution_lease() present = true
tensor()/validate/release present = true
Drop release present = true
commit-while-read guard present = true
R6-R8 counts calls = 2
R6-R8 hidden lease acquisition = 1
R6-R8 hidden lease release = 1
release precedes commit = true
binary-local R6/R7/R8 chain retained = true
raw delimiter scan = PASS
```

Cargo, rustc and rustfmt were unavailable in the bake environment. Cargo check and physical GPU execution remain operator-side admission gates.

## Commands

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p model_core `
  -p orchestrator_local
```

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r8.args"
```
