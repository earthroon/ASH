# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R7-C2

## Residency Count U32 Type Seal / Saturating-Multiply Receiver Inference Closure / No Runtime Semantic Mutation

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R7-C1`  
> Failure class: Rust compile-time numeric inference  
> Runtime admission: `HOLD` until Cargo check and physical run

## Observed compiler failure

```text
error[E0689]: can't call method `saturating_mul` on ambiguous numeric type `{integer}`
```

The ambiguous value was produced by an untyped integer `match` in `BaseTrainLayerWeightResidencySlot::counts()`.

## Canonical type contract

`BaseTrainLayerWeightResidencyCounts` already defines both residency counters as `u32`:

```rust
pub resident_decoder_block_count: u32,
pub resident_checkpoint_weight_tensor_count: u32,
```

C2 seals the implementation to the existing ABI:

```rust
let resident_decoder_block_count: u32 = match guard.resident_bundle.is_some() {
    true => 1u32,
    false => 0u32,
};
let resident_checkpoint_weight_tensor_count =
    resident_decoder_block_count.saturating_mul(9u32);
```

## Changed source

```text
crates/model_core/src/base_train_layer_weight_residency_authority.rs
```

No other source, Cargo, CLI or WGSL file changes.

## Preserved semantics

```text
resident decoder-block cardinality = 0 or 1
resident checkpoint weight tensor cardinality = block count × 9
single residency slot authority unchanged
execution lease unchanged
layer-0 eviction unchanged
layer-1 adoption unchanged
residency generation unchanged
hidden-state ownership unchanged
payload readback count unchanged
```

This patch does not change a receipt schema, saturation behavior or runtime transition.

## Static validation

```text
explicit u32 binding = PASS
match arms typed as u32 = PASS
saturating multiplier typed as u32 = PASS
ambiguous binding form absent = PASS
receipt field types remain u32 = PASS
changed file count = 1
Rust delimiter balance = PASS
overlay ZIP entries = 1
full code-bake ZIP entries = 6837
ZIP integrity = PASS
Markdown/JSON/SHA256 sidecars in code ZIPs = 0
```

Cargo, rustc and rustfmt were unavailable in the bake environment. Cargo check and physical GPU execution remain user-side admission gates.

## Commands

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r7_layer_weight_micro_residency_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r7_layer_weight_micro_residency_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r7.args"
```
