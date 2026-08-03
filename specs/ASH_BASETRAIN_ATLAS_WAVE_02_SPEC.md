# ASH-BASETRAIN-ATLAS-WAVE-02

## Actual Batch Embedding Residency /
## Layer-Scoped QKV Projection Input Binding /
## Headwise Training Prefill Live Dispatch /
## Causal·Padding·Position·RoPE Receipt Consumption /
## TensorCube Candidate Handoff /
## No Loss·Backward·Optimizer Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02`  
> Build revision: `ATLAS-WAVE-02-actual-batch-headwise-prefill-v1`  
> Direct parent: `ASH-BASETRAIN-ATLAS-WAVE-01`  
> Parent state: `ResidencyHandoffReady`  
> Training-step parent state: `Prepared` unchanged  
> Forward scope: selected decoder layer 0 only  
> Loss, backward, optimizer, delta, apply and commit authority: none

---

# 0. Purpose

AW-02 is the first Atlas Wave patch that admits actual token IDs and checkpoint-backed resident weights into a live compute path.

The canonical flow is:

```text
AW-00 Prepared transaction
  + AW-01 borrowed same-device residency owner
  + actual BaseBatchCpu
    -> actual embedding lookup
    -> selected layer-0 RMSNorm
    -> actual Q/K/V projection
    -> explicit position IDs and RoPE
    -> causal and padding-aware Headwise training prefill
    -> selected-layer context oracle
    -> live TensorCube candidate handoff
    -> stop before TensorCube Stage10, loss, backward or optimizer
```

AW-02 does not claim a closed training loop. It proves the first live forward segment and preserves all later writer boundaries.

---

# 1. Parent adoption closure

AW-01 PASS proves upload and residency, but AW-02 must consume a live in-process owner rather than reconstructing GPU state from JSON receipts.

Required:

```text
AW-01 local manifest PASS
AW-01 residency state ResidencyHandoffReady
same runtime holder
same device and queue epoch
same source weight generation
live ring buffers present
resident buffers storage-bindable
parent transaction digest unchanged
```

Forbidden:

```text
receipt-only GPU residency reconstruction
secondary adapter or device creation
resident weight re-upload under a new owner
CPU full-tensor reconstruction
random-init substitution
latest-generation substitution
```

The AW-01 coordinator or equivalent live residency holder must survive through AW-02 execution.

---

# 2. Canonical selected layer

The first physical AW-02 gate selects decoder layer 0.

```text
selected_layer == 0
```

Embedding output is a valid input only for layer 0. A later layer requires an explicit upstream-layer output receipt and live buffer lease.

Forbidden:

```text
embedding output relabelled as layer N input where N > 0
synthetic hidden-state fixture presented as production upstream output
missing selected-layer identity
mixed layer weights
```

---

# 3. Actual batch authority

The batch is the exact `BaseBatchCpu` payload admitted by AW-00 sequence authority.

Required batch fields:

```text
input token IDs
batch size
padded sequence length
row valid lengths
position IDs
attention validity receipt
loss selection metadata retained but not consumed
```

Canonical physical geometry:

```text
batch size   2
sequence     4
valid rows   [4, 1]
hidden size  8
heads        2
head dim     4
```

The gate uses nonzero, nonuniform token IDs and preserves right padding.

---

# 4. Embedding residency

Embedding lookup executes against checkpoint-backed resident embedding weights on the borrowed native device and queue.

Required:

```text
token IDs device-visible
embedding table device-visible
embedding output device-local
output shape [batch, seq, hidden]
invalid padded positions remain excluded downstream
embedding output digest recorded
```

Forbidden:

```text
host embedding lookup used as production result
fresh random embedding table
full embedding table host materialization after AW-01 residency
cross-device copy
```

---

# 5. Layer-scoped RMSNorm and QKV projection

AW-02 consumes the selected layer's exact RMSNorm and Q/K/V projection weights.

Required:

```text
RMSNorm epsilon explicit
Q, K and V weight identities distinct
same source weight generation
same runtime holder
same selected layer
Q/K/V outputs device-local
Q/K/V digests recorded
```

No output projection, residual add or MLP is admitted.

---

# 6. Position and RoPE authority

Position IDs derive from AW-00 sequence authority.

For right-padded rows:

```text
valid positions   0..row_valid_length-1
invalid positions carry no downstream attention authority
```

RoPE applies to Q and K only.

Required receipt fields:

```text
position ID digest
RoPE theta
head dimension
selected layer
Q rotation applied
K rotation applied
V rotation count 0
```

---

# 7. Headwise training prefill

AW-02 introduces a training-specific Headwise prefill ABI.

It is not the decode production session API.

Required semantics:

```text
query valid = q < row_valid_lengths[b]
key valid   = k < row_valid_lengths[b]
causal      = k <= q
admitted    = query valid && key valid && causal
```

Required behavior:

```text
invalid keys excluded before softmax
future keys excluded before softmax
invalid query context exact zero
no decode session mutation
no persistent KV cache mutation
no Burn generic attention fallback
no silent fallback
```

The Headwise result is the AW-02 context oracle.

---

# 8. TensorCube candidate handoff

AW-02 does not execute TensorCube Stage10.

It publishes a live in-process handoff containing:

```text
Q buffer lease
K buffer lease
V buffer lease
Headwise context oracle buffer lease
row-valid-length buffer lease
position and RoPE receipt digest
runtime holder identity
source weight generation
selected layer
forward invocation digest
```

Required counters:

```text
TensorCube Stage10 dispatch  0
TensorCube Stage11 dispatch  0
TensorCube Stage12 dispatch  0
TensorCube output commit     0
TensorCube forward authority false
```

JSON receipts alone may not reconstruct the handoff.

---

# 9. State ownership

The serialized AW-00 transaction remains byte-identical and in `Prepared` state.

AW-02 introduces a child phase receipt:

```text
parent transaction state  Prepared
child phase               ForwardWaveActive
parent mutation count     0
```

The live buffer owner remains in-process and is not transferred to the artifact writer.

---

# 10. Mutation firewall

Required zero counters:

```text
loss computation
logits publication
backward execution
gradient write
gradient accumulation
optimizer execution
optimizer-state write
delta materialization
resident weight write
weight commit
training cursor write
pointer swap
checkpoint write
checkpoint finalize
route promotion
decode mutation
quality claim
silent fallback
```

Allowed nonzero counters:

```text
borrowed runtime handle use
GPU buffer binding
shader module creation
bind group creation
pipeline creation
Headwise training prefill dispatch
bounded verification readback
artifact write
```

---

# 11. Runtime artifacts

Rust writes atomically to:

```text
workspace/runtime/basetrain/atlas_wave/02/
```

Required artifacts:

```text
01_parent_aw01_receipt.json
02_execution_receipt.json
03_backend_dispatch_receipt.json
04_tensorcube_handoff_receipt.json
05_actual_batch_receipt.json
06_resident_weight_binding_receipt.json
07_sequence_authority_consumption_receipt.json
08_headwise_training_prefill_receipt.json
09_tensorcube_candidate_handoff_receipt.json
10_mutation_firewall_receipt.json
11_static_source_closure_receipt.json
12_gate_coverage_receipt.json
13_child_phase_receipt.json
14_same_device_receipt.json
15_live_buffer_lease_receipt.json
16_artifact_write_receipt.json
ash_basetrain_atlas_wave_02_local_manifest.json
```

No runtime artifact or manifest is pre-generated in the code package.

---

# 12. Physical gate

Binary:

```text
ash_basetrain_atlas_wave_02_physical_gate
```

Minimum coverage:

```text
positive assertions  96
negative controls    128
```

The gate must use the existing native runtime bootstrap and execute one real GPU Headwise training-prefill dispatch.

---

# 13. Direct execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_physical_gate `
  -- `
  "@specs/cli/ash_basetrain_atlas_wave_02.args"
```

Expected PASS token:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_ACTUAL_BATCH_EMBEDDING_RESIDENCY_LAYER_SCOPED_QKV_PROJECTION_INPUT_BINDING_HEADWISE_TRAINING_PREFILL_LIVE_DISPATCH_CAUSAL_PADDING_POSITION_ROPE_RECEIPT_CONSUMPTION_TENSORCUBE_CANDIDATE_HANDOFF_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER_NO_DELTA_NO_WEIGHT_WRITE_NO_CURSOR_WRITE_NO_POINTER_SWAP_NO_CHECKPOINT_WRITE_NO_ROUTE_PROMOTION_NO_DECODE_MUTATION_SEALED
```

---

# 14. Completion state

After PASS:

```text
AW-00 transaction
  Prepared

AW-01 residency
  ResidencyHandoffReady

AW-02 child phase
  ForwardWaveActive

Headwise training prefill
  LiveDispatchBound
  ContextOracleBound

TensorCube
  LiveCandidateHandoffBound
  Stage10NotDispatched
  OutputAuthorityForbidden
```

Next patch:

```text
ASH-BASETRAIN-ATLAS-WAVE-03

TensorCube Stage10 Live QK Binding /
Headwise Context Oracle Parity /
Online Softmax Stage11 Admission /
V Weighted Accumulation Stage12 Admission /
No OProj·Loss·Backward Seal
```
