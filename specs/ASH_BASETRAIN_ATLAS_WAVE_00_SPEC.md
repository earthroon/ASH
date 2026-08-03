# ASH-BASETRAIN-ATLAS-WAVE-00

## Training Step Transaction SSOT /
## Causal·Padding·Position·RoPE Authority /
## Same-Generation Fence /
## Atlas Route Random-Init Rejection /
## No Generic Attention Fallback /
## Legacy G206D Namespace Disambiguation Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-00`  
> Build revision: `ATLAS-WAVE-00-training-step-transaction-ssot-v1`  
> Physical parent: `ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01`  
> Physical parent state: `PASS_ASH_BASETRAIN_G206D_..._NO_SILENT_FALLBACK_SEALED`  
> Legacy audit predecessor: `ASH-BASETRAIN-GPU-70K-G197D`  
> Implementation SSOT: attached G206D-R3 body  
> GitHub lineage reference: `earthroon/ASH`, inspected `main` head `e7d1e7cbd21612eacb82274f8c934c04f2decc92`  
> Runtime mutation authority: none  
> Forward, backward, optimizer, apply, commit authority: none

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-00` establishes the first non-fixture authority boundary for the Atlas Parallel Sequential Wave training line.

This patch does not train the model. It defines exactly what one training step is allowed to read, which component owns its state, which sequence geometry is authoritative, and which generation identities must remain immutable until a later atomic commit patch.

The patch closes six structural holes before any live Headwise, TensorCube, backward, optimizer, or weight apply path is connected.

```text
AtlasGroupedSequential route
  -> explicit checkpoint-backed model source
  -> explicit dataset batch sequence authority
  -> explicit causal + padding + position + RoPE authority
  -> explicit source generation fence
  -> one BaseTrain-owned step transaction
  -> future Headwise/TensorCube execution admission packet
```

Forbidden canonical flow:

```text
AtlasGroupedSequential
  -> grouped load deferred
  -> AshModel::new random weights
  -> generic Burn grouped_query_attention
  -> unmasked softmax
  -> loss labelled causal
```

The patch therefore converts the current Atlas route from an unsafe executable placeholder into a fail-closed prepared transaction surface.

---

# 1. Source-grounded problem statement

## 1.1 Atlas route currently constructs a random model

Current source:

```text
crates/base_train/src/training.rs:386-393
```

Current behavior:

```rust
BaseTrainRoute::AtlasGroupedSequential => {
    println!("... grouped checkpoint load is deferred ...");
    model_core::AshModel::<B>::new(spec.clone(), device)
}
```

`AshModel::new` initializes token embedding, LM head, attention projections, and MLP projections with random tensors. Therefore the current Atlas route is not checkpoint-backed even though `BaseTrainRoute::AtlasGroupedSequential` is the default route.

AW-00 must make this path unrepresentable for Atlas execution.

## 1.2 Generic training attention has no causal or padding mask

Current source:

```text
crates/model_core/src/model_layers.rs:284-312
```

Current behavior:

```rust
let scores = q
    .matmul(k.swap_dims(3, 4))
    .div_scalar((head_dim as f32).sqrt());
let attn = softmax(scores, 4);
let ctx = attn.matmul(v);
```

No causal mask, key padding mask, query padding zeroing, explicit position IDs, or RoPE application is present in this generic function.

The generic primitive may remain for explicit reference and fixture use. It must not remain a silent fallback for `AtlasGroupedSequential`.

## 1.3 Existing `base_train_step.rs` is an audit-only G197D contract

Current source:

```text
crates/base_train/src/base_train_step.rs:39-180
```

The existing `BaseTrainStepInputContract`, `BaseTrainStepOutputContract`, and `base_train_step_contract` belong to `ASH-BASETRAIN-GPU-70K-G197D`. The output is hard-bound to `BaseTrainRunKind::AuditOnly`, and optimizer, weight commit, checkpoint mutation, and route promotion remain blocked.

AW-00 must not silently repurpose or overwrite this legacy audit contract. The new canonical public type is:

```rust
BaseTrainAtlasWaveStepTransaction
```

The bare alias `BaseTrainStepTransaction` is not introduced in AW-00.

## 1.4 Two different G206D identities already coexist

Legacy decision route:

```text
ASH-BASETRAIN-GPU-70K-G206D
module: ash_basetrain_gpu_70k_g206d_decision_outcome_routing
```

Physical delta materialization route:

```text
ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01
module: base_train_g206d_isolated_weight_delta_materialization
```

A bare `G206D` parent key, directory, log label, or receipt field is ambiguous. AW-00 introduces typed full lineage identities and forbids new bare-G206D authority fields.

---

# 2. Scope

## 2.1 In scope

```text
BaseTrain Atlas Wave step transaction schema
Single writer and state ownership contract
Checkpoint-backed Atlas model-source admission
Causal mask semantic authority
Attention padding semantic authority
Explicit position-ID authority
RoPE configuration authority
Source and candidate generation fence
Atlas route random-init rejection
Atlas route generic-attention fallback rejection
Legacy G197D step-contract separation
Legacy 70K G206D and physical G206D identity separation
Deterministic receipt digest and replay
Host-side validation gate
Source-surface static closure checks
```

## 2.2 Out of scope

```text
WGPU adapter or device creation
Native runtime handle borrowing
Safetensors slice-to-Atlas residency
Atlas triple-ring allocation
Headwise training prefill execution
TensorCube Stage10, Stage11, or Stage12 execution
Loss computation
Backward execution
Gradient accumulation
Optimizer candidate execution
G206D live delta consumption
Inactive weight application
Resident weight mutation
Optimizer-state mutation
Training cursor mutation
Pointer swap
Checkpoint write or finalization
Decode route mutation
Quality or convergence claim
```

AW-00 PASS means the training step can be prepared safely. It does not mean the training loop has executed.

---

# 3. Authority map

## 3.1 State ownership

| State or contract | Canonical owner | M