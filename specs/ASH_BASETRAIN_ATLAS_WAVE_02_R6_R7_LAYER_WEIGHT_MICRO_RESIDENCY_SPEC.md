# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R7

## Layer Weight Micro-Residency / Single DecoderBlock Slot / Generation-Sealed Layer Rebind / Layer-0 Weight Eviction / Layer-1 Weight Adoption / No All-Layer Weight Residency Seal

> Parent physical SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6-C6`  
> Route: BaseTrain FullPrefill  
> Layer-1 forward: `BLOCKED`  
> Production inference: `BLOCKED`  
> Backward / optimizer: `BLOCKED`  
> Proof ledger: `HOLD`

## Full specification identity

The complete 1,318-line bake specification is distributed separately with the code-bake response.

```text
file = ASH_BASETRAIN_ATLAS_WAVE_02_R6_R7_LAYER_WEIGHT_MICRO_RESIDENCY_SPEC.md
sha256 = e4f2a98e290fcbc0419dae8c12cec86b2d906c0c6a3af873abe91e70d7024f2d
bytes = 34,991
```

This repository document is the compact commit seal for that full specification. Runtime and admission semantics below are authoritative and match the full document.

## Parent evidence

R6-R7 begins from the physical R6-R6-C6 state:

```text
micro_atlas_waves = 8
micro_atlas_peak_bytes = 32768
mega_atlas_create = 0
qkv_projection_count = 1
final_compared_scalar_count = 65536
final_mismatch_count = 0
final_nonfinite_count = 0
layer1_hidden_commit_count = 1
payload_readback_count = 0
```

R6-R7 must run the parent route in the same process and on the same WGPU device/queue lineage. A copied receipt, subprocess result, metadata-only block, synthetic checkpoint or shadow residency is forbidden.

## Weight residency SSOT

```rust
BaseTrainLayerWeightResidencySlot
```

The slot is the sole owner of the currently resident actual decoder-block bundle.

```text
resident decoder block count ∈ {0,1}
resident checkpoint weight tensor count ∈ {0,9}
active decoded checkpoint payload layer count <= 1
```

The resident bundle owns exactly:

```text
input RMSNorm
Q projection
K projection
V projection
O projection
post-attention RMSNorm
gate projection
up projection
down projection
prepared runtime LoRA set
```

Layer hidden state remains owned by `LayerHiddenAuthoritySlot`. Attention selection remains owned by `BaseTrainLayerAttentionAuthoritySlot`.

R6-R7 proves live resource ownership and residency cardinality. It does not claim that the driver allocator returns physical VRAM pages at the exact Rust `drop()` boundary.

## State machine

```rust
pub enum BaseTrainLayerWeightResidencyState {
    Resident,
    EvictionArmed,
    VacantForRebind,
    RecoveryRequired,
}
```

Required transition:

```text
Resident(layer=0, generation=0, serial=0)
  -> EvictionArmed(layer=0, target=1, generation=0, serial=1)
  -> VacantForRebind(layer=None, target=1, generation=0, serial=2)
  -> Resident(layer=1, generation=1, serial=3)
```

`residency_generation` increments only when a new block is successfully adopted. `transition_serial` increments on each authority transition.

A failure after vacancy must become `RecoveryRequired`. Same-invocation layer-0 reconstruction, Headwise fallback and partial layer-1 adoption are forbidden.

## Execution lease

Actual decoder execution must acquire:

```rust
BaseTrainLayerWeightExecutionLease
```

The lease captures layer index, residency generation, transition serial, pointer digest and block identity. Eviction requires:

```text
active execution lease count = 0
slot-owned strong reference count = 1
layer-0 completion digest present
layer-1 hidden committed and published
```

The strong-owner check occurs before destructive slot take.

## Actual implementation path

The R6-R6 gate body is extracted into the shared in-process runtime:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_runtime.rs
```

Both gates call:

```rust
run_r6_r6_live_body_session()
```

The returned session owns checkpoint authority, existing WGPU bootstrap/device/queue lineage, the weight slot, the hidden slot, the layer-1 hidden pointer, layer-0 completion digest, and parent final receipts.

R6-R6 installs the actual layer-0 block into the slot before QKV projection and accesses it only through the execution lease. The lease is released before the session is returned.

R6-R7 then performs:

```text
same-process R6-R6 physical execution
  -> verify active lease count zero
  -> arm layer-0 eviction
  -> take and drop sole layer-0 block
  -> device.poll(Wait)
  -> mark slot VacantForRebind
  -> read exactly nine layer-1 checkpoint payloads
  -> build actual layer-1 decoder block
  -> adopt layer 1 into the same slot
  -> residency generation 0 -> 1
```

Layer 1 is adopted but not executed in this patch.

## Layer-aware loader and module binding

The loader validates:

```text
selected_layer < num_hidden_layers
nine tensors belong to the selected layer
canonical tensor roles match
production shapes match
synthetic tensor count = 0
checkpoint mutation count = 0
```

Module targets are sealed with the selected layer:

```text
layers.{L}.attn.q_proj
layers.{L}.attn.k_proj
layers.{L}.attn.v_proj
layers.{L}.attn.o_proj
layers.{L}.ffn.gate_proj
layers.{L}.ffn.up_proj
layers.{L}.ffn.down_proj
```

Binding layer-1 checkpoint tensors to `layers.0.*` is forbidden.

The largest decoded individual layer-1 tensor buffer must be nonzero and no greater than `device.max_buffer_size` before GPU block construction.

## No all-layer residency

Required counts:

```text
checkpoint payload read layer count = 2
checkpoint payload overlap count = 0
peak decoded payload layer count = 1
actual decoder block construction count = 2
peak resident decoder block count = 1
peak resident checkpoint weight tensor count = 9
all-layer model construction count = 0
all-layer payload preload count = 0
next-layer prefetch count = 0
weight upload overlap count = 0
source-target simultaneous residency count = 0
```

The two payload layers are layer 0 from the parent physical execution and layer 1 loaded only after vacancy.

## Hidden non-mutation

The layer-1 hidden pointer must be identical before and after rebind:

```text
layer index = 1
hidden generation = 1
pointer digest unchanged
buffer identity digest unchanged
completion token digest unchanged
shape unchanged
payload readback = 0
layer-2 hidden commit count = 0
```

## Receipts

```text
00_parent_r6_r6_physical_pass.json
01_checkpoint_layer_inventory.json
02_layer0_weight_residency_pointer.json
03_layer0_execution_completion.json
04_layer_weight_rebind_transaction.json
05_layer0_weight_eviction.json
06_weight_slot_vacant.json
07_layer1_weight_tensor_selection.json
08_layer1_actual_decoder_block_build.json
09_layer1_weight_adoption.json
10_generation_sealed_rebind.json
11_no_all_layer_weight_residency.json
12_layer1_hidden_non_mutation.json
13_failure_atomicity.json
14_r6_r7_final.json
ash_basetrain_atlas_wave_02_r6_r7_local_manifest.json
```

Receipt aggregation uses deterministic atlas wave-lane ordering. Runtime manifests and proof artifacts are excluded from distributed code ZIPs.

## Changed code/config/CLI files

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r7_layer_weight_loader.rs
crates/base_train/src/lib.rs
crates/model_core/src/actual_decoder_block_split_forward.rs
crates/model_core/src/base_train_layer_weight_residency_authority.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_runtime.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r7_layer_weight_micro_residency_gate.rs
crates/orchestrator_local/src/lib.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r7.args
```

No WGSL change is introduced.

## Bake validation

```text
static validation = 54 / 54 PASS
changed file set = 13 exact
R6-R7 subprocess invocation count = 0
all-layer model constructor count = 0
all-layer payload preload path count = 0
next-layer prefetch path count = 0
synthetic fallback path count = 0
WGSL modification count = 0
new recursion-limit workaround count = 0
.sha256 sidecar count = 0
```

The bake environment did not contain Cargo, rustc or rustfmt. Rust type-check and physical GPU execution are external admission gates and are not claimed by the bake.

## Physical commands

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

## Admission matrix

```text
R6-R6 layer-0 live body = ADMITTED by parent physical PASS
R6-R7 sequential weight rebind = ADMITTED only on this gate PASS
layer-1 forward = BLOCKED
N-layer coordinator = BLOCKED
final norm / LM head = BLOCKED
forward loss = BLOCKED
backward = BLOCKED
optimizer = BLOCKED
production inference = BLOCKED
proof ledger = HOLD
```

## Terminal log

```text
[r6-r7-layer-weight-residency] source_layer=0 source_evicted=1 target_layer=1 target_adopted=1 residency_generation=0->1 peak_resident_blocks=1 peak_resident_weight_tensors=9 payload_layers=2 payload_overlap=0 all_layer_preload=0 prefetch=0 layer1_hidden_mutation=0 layer2_commit=0 weight_readback=0
```

## PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R7_LAYER_WEIGHT_MICRO_RESIDENCY_R6_R6_C6_PHYSICAL_PASS_PARENT_SINGLE_DECODER_BLOCK_SLOT_AUTHORITATIVE_OWNER_ACTUAL_LAYER0_EXECUTION_LEASE_COMPLETION_BOUND_LAYER0_WEIGHT_EVICTION_EXPLICIT_VACANT_TRANSITION_LAYER1_NINE_TENSOR_REAL_CHECKPOINT_PAYLOAD_ADOPTION_LAYER_AWARE_MODULE_TARGETS_LAYER_AWARE_RUNTIME_LORA_BINDING_GENERATION_SEALED_SEQUENTIAL_REBIND_RESIDENCY_GENERATION_ZERO_TO_ONE_PEAK_RESIDENT_BLOCK_ONE_PEAK_RESIDENT_WEIGHT_TENSORS_NINE_ACTIVE_DECODED_PAYLOAD_LAYER_ONE_NO_ALL_LAYER_MODEL_CONSTRUCTION_ALL_LAYER_PAYLOAD_PRELOAD_NEXT_LAYER_PREFETCH_WEIGHT_UPLOAD_OVERLAP_SOURCE_TARGET_SIMULTANEOUS_RESIDENCY_STALE_LEASE_DUPLICATE_OPERATION_SILENT_FALLBACK_PARTIAL_ADOPTION_LAYER1_HIDDEN_MUTATION_LAYER2_HIDDEN_COMMIT_PAYLOAD_READBACK_BACKWARD_OPTIMIZER_WEIGHT_OR_CHECKPOINT_MUTATION_LAYER_WEIGHT_REBIND_ADMITTED_LAYER1_FORWARD_AND_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

## Next boundary

R6-R8 consumes the already-resident layer-1 block and unchanged layer-1 hidden. It must not reload or rebuild layer 1 before execution.