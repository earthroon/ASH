# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R8

## Layer-1 Hidden Lease Consumption / Already-Resident Layer-1 Block Adoption / No Re-Embedding / No Weight Reload / Actual Layer-1 Input RMSNorm / Single Layer-1 QKV / Shared W5·W6·W7 Attention / Actual Layer-1 OProj·MLP / Layer-2 Hidden Commit Seal

> Parent physical SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R7-C2` with operator-supplied R6-R7 physical PASS  
> Route: BaseTrain FullPrefill  
> Layer-1 forward: `HOLD` until physical run  
> Layer-2 weight adoption: `BLOCKED`  
> Production inference: `BLOCKED`  
> Backward / optimizer: `BLOCKED`  
> Proof ledger: `HOLD`

## Full specification identity

The complete design specification is retained as the bake-side document:

```text
file = ASH_BASETRAIN_ATLAS_WAVE_02_R6_R8_SPEC.md
lines = 1,695
bytes = 38,932
sha256 = 45f493e553860f856a27967165f3085c4504665ae13908bbc4d8b9ef3fe86706
```

This repository document is the implementation-aligned commit seal for that full specification.

## Starting state

```text
weight slot state = Resident
resident weight layer = 1
weight residency generation = 1
resident decoder block count = 1
resident checkpoint weight tensor count = 9
hidden layer = 1
hidden generation = 1
layer-1 hidden committed = true
layer-1 forward count = 0
```

## Ending state

```text
weight slot state = Resident
resident weight layer = 1
weight residency generation = 1
hidden layer = 2
hidden generation = 2
layer-2 hidden commit count = 1
```

The layer-1 weight pointer must be byte-for-byte unchanged across R6-R8.

## Same-process parent chain

R6-R7 is extracted into an in-process session runner:

```rust
run_r6_r6_live_body_session()
  -> run_r6_r7_layer_weight_residency_session()
    -> run_r6_r8_layer1_live_body_session()
```

The chain preserves the same checkpoint authority, Burn device, native WGPU device/queue lineage, weight residency slot and hidden authority slot. Subprocess execution is forbidden.

## Lease pair

R6-R8 acquires both:

```rust
BaseTrainLayerWeightExecutionLease
LayerHiddenExecutionLease
```

The weight lease captures layer index, residency generation, transition serial, pointer digest and decoder-block identity.

The hidden lease captures layer index, hidden generation, pointer digest, buffer identity digest, completion token digest and semantic BQH shape.

The lease pair must resolve to layer 1 and generation 1. Both leases are revalidated after final parity. GPU completion is observed with `device.poll(PollType::Wait)`, then both input leases are released before layer-2 commit.

`LayerHiddenAuthoritySlot::commit_next_layer()` now fails closed when any hidden read lease remains active:

```text
R6R8HiddenCommitWhileReadLeaseActive
```

## No-reload boundary

The R6-R8 execution module contains no calls to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
build_r6_r7_actual_decoder_block_for_layer
execute_base_train_atlas_wave_02_r6_r6_micro_atlas_tilemap_wave_stream
load_base_train_atlas_wave_02_r6_r6_decoder_block
```

Required R6-R8-local counts:

```text
embedding dispatch count = 0
micro-atlas wave count = 0
checkpoint payload read count = 0
checkpoint weight upload count = 0
decoder block build count = 0
runtime LoRA build count = 0
layer-1 eviction count = 0
layer-2 weight prefetch count = 0
layer-2 weight adoption count = 0
```

R6-R7 may physically execute R6-R6 and load/adopt layer 1 as its parent work. Those parent counts are not attributed to the R6-R8-local execution segment.

## Actual layer-1 body

The already-resident layer-1 decoder block consumes the layer-1 hidden tensor through the lease pair:

```text
layer-1 hidden
  -> actual input RMSNorm
  -> single Q projection
  -> single K projection
  -> single V projection
  -> NeoX RoPE
  -> W4 BQHD direct texture pack
  -> W5 Stage10
  -> W6 Stage11
  -> W7 Stage12
  -> actual OProj
  -> attention residual
  -> post-attention RMSNorm
  -> actual SwiGLU gate/up/SiLU multiply/down
  -> FFN residual
  -> layer-2 hidden candidate
```

Expected fixture counts:

```text
input norm = 1
Q/K/V = 1/1/1
stage10 = 2
stage11 = 1
stage12 = 4
OProj = 1
post-attention norm = 1
gate/up/down = 1/1/1
```

## Reference and replay gates

The Headwise reference uses the canonical neutral score-scale contract:

```text
density lane = 0
packed path = 0
shader weight scale = 1.0
density gate = 1.0
cairo/coda/curvature = 0.0
active tensor zero-copy = 1
```

R6-R8 requires:

```text
shared/replay context exact parity = PASS
shared/reference final hidden mixed-envelope parity = PASS
shared/replay final hidden exact parity = PASS
layer-2 publication exact parity = PASS
final compared scalar count = 65,536
final mismatch count = 0
final non-finite count = 0
payload readback count = 0
```

## Commit ordering

```text
actual body and parity complete
  -> revalidate weight lease
  -> revalidate hidden lease
  -> device.poll(Wait)
  -> release weight lease
  -> release hidden lease
  -> confirm both active lease counts are zero
  -> commit layer-2 hidden once
  -> exact publication parity
```

A layer-2 commit while the layer-1 hidden is still leased is forbidden.

## Failure atomicity

Before layer-2 commit, any failure leaves:

```text
resident weight layer = 1
weight residency generation = 1
hidden layer = 1
hidden generation = 1
weight reload count = 0
block rebuild count = 0
same-invocation fallback count = 0
layer-2 commit count = 0
```

After layer-2 commit, a publication-proof failure does not silently roll the hidden authority back. The committed layer-2 pointer remains and the proof ledger stays `HOLD`.

## Changed code/config files

```text
crates/model_core/src/base_train_layer_attention_authority.rs
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r7_layer_weight_micro_residency_gate.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r8_layer1_live_body_gate.rs
crates/orchestrator_local/src/lib.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r8.args
```

No WGSL change is introduced.

## Static bake validation

```text
static checks = 39 / 39 PASS
changed code/config files = 8
R6-R8 loader calls = 0
R6-R8 block-builder calls = 0
R6-R8 embedding/micro-atlas calls = 0
same-process R6-R7 runner = present
weight execution lease = present
hidden execution lease = present
commit-while-read-lease guard = present
PollType::Wait before lease release = present
mixed final parity = present
exact replay parity = present
exact publication parity = present
Rust delimiter scan = PASS
Markdown/JSON/SHA256 sidecars in code ZIPs = 0
```

Cargo, rustc and rustfmt were unavailable in the bake environment. Rust type-check, WGPU pipeline creation and physical execution remain operator-side gates.

## Physical commands

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

## Terminal log contract

```text
[r6-r8-layer1-live-body] resident_layer=1 weight_generation=1->1 hidden_layer=1->2 hidden_generation=1->2 reembedding=0 weight_reload=0 block_rebuild=0 input_norm=1 qkv=1 stage10=2 stage11=1 stage12=4 live_oproj=1 final_compared=65536 final_mismatch=0 final_nonfinite=0 layer2_commit=1 weight_lease_after=0 hidden_lease_after=0 payload_readback=0
```

## Admission matrix

```text
R6-R7 layer weight residency = ADMITTED by parent physical PASS
R6-R8 layer-1 forward = ADMITTED only on physical PASS
layer-2 weight adoption = BLOCKED
N-layer coordinator = BLOCKED
final norm / LM head = BLOCKED
forward loss = BLOCKED
backward = BLOCKED
optimizer = BLOCKED
production inference = BLOCKED
proof ledger = HOLD
```

## Next boundary

R6-R9 combines the proven rebind transaction and resident-layer executor into a checkpoint-resolved sequential decoder-layer loop. It must begin from weight layer 1 / hidden layer 2, evict layer 1, adopt layer 2, consume layer-2 hidden, and commit layer 3 without all-layer residency.