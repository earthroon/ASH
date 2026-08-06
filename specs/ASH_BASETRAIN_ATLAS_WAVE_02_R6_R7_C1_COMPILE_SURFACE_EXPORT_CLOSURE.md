# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R7-C1

## Compile Surface Export Closure / Atomic R6-R7 Overlay Reapplication / Module-Qualified Import / Typed Fold Accumulator Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R7`  
> Gate: Rust compile  
> Runtime semantics: unchanged  
> Physical admission: `HOLD`

## Observed failure

The R6-R7 binary and Cargo bin entry were present while the local source tree still exposed pre-R6-R7 crate roots. The compiler could not resolve the R6-R7 BaseTrain loader, ModelCore builder and residency state, OrchestratorLocal runtime modules, or R6-R7 patch constants. Two byte-count `try_fold` closures also required explicit accumulator types after the unresolved import cascade.

## Root cause

```text
R6-R7 gate present
R6-R7 Cargo bin present
R6-R7 module declarations/root exports stale or absent
```

This is a partial-overlay compile surface. C1 redistributes the complete 13-file R6-R7 code surface atomically rather than patching only the gate.

## Export closure

BaseTrain declares and explicitly exports:

```text
base_train_atlas_wave_02_r6_r7_layer_weight_loader
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
BASETRAIN_ATLAS_WAVE_02_R6_R7_BUILD_REVISION
BASETRAIN_ATLAS_WAVE_02_R6_R7_PATCH_ID
```

ModelCore declares and exports:

```text
base_train_layer_weight_residency_authority
BaseTrainLayerWeightResidencyState
build_r6_r7_actual_decoder_block_for_layer
```

OrchestratorLocal declares:

```text
base_train_atlas_wave_02_r6_r6_runtime
base_train_atlas_wave_02_r6_r7_layer_weight_residency
```

The shared R6-R6 runtime remains feature-gated by `orchestrator_tcu_audit_bins`, which is also required by the R6-R7 binary.

## Gate import seal

The gate imports new symbols from their canonical modules rather than relying on crate-root glob re-exports:

```text
base_train::base_train_atlas_wave_02_r6_r7_layer_weight_loader
model_core::actual_decoder_block_split_forward
model_core::base_train_layer_weight_residency_authority
orchestrator_local::base_train_atlas_wave_02_r6_r6_runtime
orchestrator_local::base_train_atlas_wave_02_r6_r7_layer_weight_residency
```

Both byte-count folds use an explicit `u64` accumulator:

```rust
.try_fold(0u64, |acc: u64, tensor| { ... })
```

## Atomic overlay set

```text
crates/base_train/src/lib.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r7_layer_weight_loader.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
crates/model_core/src/lib.rs
crates/model_core/src/base_train_layer_weight_residency_authority.rs
crates/model_core/src/actual_decoder_block_split_forward.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_runtime.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r7_layer_weight_micro_residency_gate.rs
crates/orchestrator_local/Cargo.toml
specs/cli/ash_basetrain_atlas_wave_02_r6_r7.args
```

## Preserved semantics

```text
single decoder-block slot
layer-0 execution lease
layer-0 eviction
VacantForRebind transition
layer-1 nine-tensor checkpoint load
layer-1 actual block adoption
residency generation 0 -> 1
layer-1 hidden non-mutation
no all-layer preload
no next-layer prefetch
no layer-1 forward
no payload readback
```

## Static validation

```text
compile-surface checks = 40 / 40 PASS
overlay files = 13
BaseTrain module/export closure = PASS
ModelCore module/export closure = PASS
OrchestratorLocal module closure = PASS
module-qualified gate imports = PASS
explicit u64 fold accumulators = 2 / 2
R6-R7 Cargo bin registration = PASS
Rust delimiter scan = PASS
Markdown in code ZIP = 0
.sha256 sidecar in code ZIP = 0
```

The bake environment has no Cargo, rustc or rustfmt. Rust type-check and physical GPU execution remain external admission gates.

## Commands

```powershell
cargo clean `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  -p base_train `
  -p model_core `
  -p orchestrator_local
```

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
