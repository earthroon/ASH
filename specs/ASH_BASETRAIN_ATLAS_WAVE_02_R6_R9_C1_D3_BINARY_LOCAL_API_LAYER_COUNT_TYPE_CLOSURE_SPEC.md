# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D3

## Binary-Local API Generation Closure / R6-R7 Rebind Export / R6-R8 Resident-Layer Executor Export / Checkpoint Layer-Count u64 SSOT / Checked Decoder-Index Boundary Seal

> Parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D2`  
> Observed compile failures: unresolved R6-R7/R6-R8 imports plus `u32`/`u64` layer-count mismatches  
> Runtime C1 semantics: unchanged  
> Artifact wave-map semantics: unchanged  
> Proof ledger: `HOLD` until Cargo/WGPU physical rerun

## 1. Observed failures

The C1-D2 gate compiled its R6-R9 coordinator against operator-side binary-local R6-R7 and R6-R8 sources that did not expose the APIs required by the coordinator:

```text
rebind_resident_decoder_layer
execute_resident_decoder_layer_from_session
```

The same compile also exposed a latent type split:

```text
checkpoint config num_hidden_layers = u64
C1 execution window decoder indexes = u32
R6R9ForwardCoordinatorSession.checkpoint_layer_count = u32   // incorrect ownership
```

The checkpoint layer count is metadata authority and must retain its canonical `u64` type. Decoder indexes remain bounded `u32` values at the execution boundary.

## 2. API distribution closure

The D3 overlay atomically carries the binary-local runtime chain and direct authority dependencies required by the exported APIs:

```text
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_artifact_wave_map.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_runtime.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_artifact_wave_map.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r7_layer_weight_loader.rs
crates/model_core/src/actual_decoder_block_split_forward.rs
crates/model_core/src/base_train_layer_attention_authority.rs
crates/model_core/src/base_train_layer_weight_residency_authority.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

Required exported surfaces:

```rust
pub fn rebind_resident_decoder_layer(...)

pub fn execute_resident_decoder_layer_from_session(...)
```

The R6-R9 gate continues to use binary-local `#[path = ...]` modules and does not depend on a crate-root re-export for these runtime modules.

## 3. Layer-count type SSOT

Canonical checkpoint metadata remains:

```rust
pub num_hidden_layers: u64
```

C1 keeps decoder target indexes in `u32`:

```rust
R6R9ExecutionWindow {
    first_target_layer: u32,
    max_layer_steps: u32,
    expected_final_weight_layer: u32,
    expected_final_hidden_layer: u32,
}
```

The coordinator session stores the checkpoint-owned count without narrowing:

```rust
pub checkpoint_layer_count: u64
```

The C1 target range is checked against checkpoint metadata using widening conversion:

```rust
u64::from(last_target_exclusive) <= layer_count
```

The R6-R7 rebind range check follows the same rule:

```rust
u64::from(target_layer_index) < session.checkpoint.config.num_hidden_layers
```

Unchecked `as u32` narrowing of checkpoint layer metadata is forbidden.

## 4. Preserved C1 behavior

D3 does not change:

```text
first target layer = 2
max layer steps = 1
weight layer 1 -> 2
weight generation 1 -> 2
hidden layer 2 -> 3
hidden generation 2 -> 3
automatic continuation = 0
all-layer preload = 0
next-layer prefetch = 0
re-embedding = 0
payload readback = 0
```

D2 artifact construction remains:

```text
transaction receipt = 2 waves / 4 lanes
final receipt = 4 waves / 8 lanes
manifest = 2 waves / 4 lanes
R6-R9 json! macro sites = 0
```

## 5. Failure-class separation

```text
missing R6-R7 rebind export       -> distribution/API generation failure
missing R6-R8 executor export     -> distribution/API generation failure
u32/u64 layer-count mismatch      -> type ownership failure
physical decoder execution error  -> runtime failure, not claimed by D3
```

D3 must not hide any of these through fallback or synthetic adapters.

## 6. Static validation

```text
R6-R7 rebind public function = present
R6-R8 resident-layer executor public function = present
checkpoint num_hidden_layers type = u64
R6-R9 checkpoint_layer_count type = u64
C1 target window compare uses u64 widening = present
R6-R7 target range compare uses u64 widening = present
unchecked checkpoint-count narrowing = absent in D3 edits
R6-R9 json! macro sites = 0
recursion_limit workaround = 0
Rust lexical delimiter scan = PASS
D3 overlay required file count = 13
.md in code ZIPs = 0
.sha256 in code ZIPs = 0
manifest JSON in code ZIPs = 0
artifacts/ in code ZIPs = 0
manifests/ in code ZIPs = 0
```

Cargo, rustc and rustfmt are unavailable in the bake environment. Type-check and physical WGPU execution remain operator-side gates.

## 7. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

## 8. Revision identity

```text
patchId = ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C1-D3
buildRevision = r6-r9-c1-d3-binary-local-api-and-layer-count-type-closure-v1
```

## Seal

> R6-R9 C1-D3 keeps checkpoint layer cardinality in its canonical u64 domain, converts only bounded decoder indexes upward for comparison, and distributes the R6-R7/R6-R8 binary-local execution APIs together with the authority surfaces they require.
