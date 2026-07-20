# ASH-LORA-MIN1-R1

# Authoritative LM-Head LoRA-B Raw Storage Borrow /
# Live Gradient and Adam State Same-Device Binding /
# In-Place Native GPU Update /
# Compact Window Evidence /
# Synthetic Lane Elimination Repair

## 0. Metadata

- Parent: `ASH-LORA-MIN1-R1 One GPU Parameter Update / Independent Before-After and Reference Parity / Zero CPU Apply Fallback Physical Proof Seal`
- Predecessor state: `AwaitingLiveStorageBinding`
- Patch class: live-storage authority and in-place update repair
- Functional revision increase: not authorized
- New optimizer family: not authorized
- Full training promotion: not authorized
- Checkpoint promotion: not authorized
- Synthetic live substitution: forbidden

## 1. Starting state

The predecessor correctly emits:

```text
HOLD_ASH_LORA_MIN1_R1
live_storage_bound=false
hold_reason=live_lora_storage_not_bound
update_terminal_state=AwaitingLiveStorageBinding
lora_min1_physical_proof_pass=false
```

The deterministic fixture proves GPU AdamW arithmetic but does not prove mutation of a runtime-owned LoRA parameter.

## 2. Repair objective

This repair must establish one physical chain:

```text
Burn Autodiff lm_head.lora_b Param
-> one real forward and cross-entropy loss
-> one real backward gradient associated with the same ParamId
-> strict same-device raw parameter lease
-> strict same-device raw gradient lease
-> authoritative Adam m/v state owned by the MIN1 live optimizer session
-> one native WGPU AdamW dispatch
-> in-place mutation of the borrowed parameter storage
-> compact before/after evidence
-> independent reference comparison
```

No diagnostic label, receipt, caller flag, or temporary buffer may create live authority.

## 3. Canonical live target

```text
target_module_id=lm_head.lora_b
target_parameter_kind=lora_b
```

The live lane uses a real `TrainableLoraAdapter<Autodiff<Wgpu>>` parameter object. The parameter identity must be derived from the runtime raw lease and may not be hardcoded.

The MIN1 live session is deliberately small:

```text
hidden_size=8
vocab_size=8
rank=1
parameter_window_elements=8
sample_count=1
forward_count=1
backward_count=1
optimizer_step_count=1
```

This is a physical update proof, not production training promotion.

## 4. Authoritative parameter borrow

The parameter tensor is obtained from the live model parameter owner:

```text
model.lora_b.val().inner()
```

It is passed to the strict same-device raw bridge.

Required:

```text
parameter_raw_borrow_attempt_count=1
parameter_raw_borrow_success_count=1
bridge_mode=RawBorrowed
host_upload_count=0
```

The raw lease must expose:

```text
tensor seam identity
primitive identity
stream identity
buffer
buffer offset
buffer size
element count
bytes per element
```

The runtime-derived seam identity becomes `target_parameter_tensor_id`.

## 5. Live backward gradient borrow

The gradient must be produced by:

```text
loss.backward()
GradientsParams::from_grads(...)
GradientsParams::get(inner_backend, model.lora_b ParamId)
```

Required relationship:

```text
gradient belongs to the exact lora_b ParamId used in forward
```

The gradient tensor is passed to the same strict raw bridge.

Required:

```text
gradient_raw_borrow_attempt_count=1
gradient_raw_borrow_success_count=1
gradient_authority=live_burn_backward
host_upload_count=0
```

Caller-provided, fixture, random, stale, or disk-loaded gradients are forbidden.

## 6. Live loss graph

The proof must execute one real model loss:

```text
hidden -> LoRA A -> LoRA B -> logits -> cross entropy
```

Required:

```text
forward_count=1
loss_compute_count=1
backward_count=1
loss_is_finite=true
target_in_loss_graph=true
target_requires_grad=true
```

A detached synthetic scalar loss is forbidden.

## 7. Adam state ownership

The live MIN1 optimizer session owns the authoritative state for this isolated physical step:

```text
Adam m
Adam v
step index
```

Required authority values:

```text
moment_m_authority=lora_min1_native_optimizer_registry
moment_v_authority=lora_min1_native_optimizer_registry
step_authority=lora_min1_native_optimizer_registry
update_authority=lora_min1_native_optimizer
```

The states are initialized once by the live optimizer owner on the same raw device. They are not fixture states, caller states, or CPU mirrors.

Required:

```text
moment_m_raw_borrow_attempt_count=1
moment_m_raw_borrow_success_count=1
moment_v_raw_borrow_attempt_count=1
moment_v_raw_borrow_success_count=1
```

## 8. Same-device and same-queue contract

Parameter, gradient, m, v, pipeline, command encoder, and queue must use the `ExistingDeviceBootstrap` runtime.

Required:

```text
parameter_same_device=true
gradient_same_device=true
moment_m_same_device=true
moment_v_same_device=true
optimizer_same_queue=true
```

The MIN1 binary may not create a second disconnected device for the live lane.

## 9. Storage binding limit

The live optimizer shader uses four storage bindings:

```text
binding 1: parameter read_write
binding 2: gradient read
binding 3: Adam m read_write
binding 4: Adam v read_write
```

Binding zero is the optimizer uniform.

This remains within a four-storage-buffer compute-stage limit. A private synthetic state atlas may not replace the authoritative live parameter or gradient.

## 10. In-place update

The native optimizer shader writes directly to:

```text
borrowed parameter raw storage
live optimizer m storage
live optimizer v storage
```

Required:

```text
authoritative_parameter_in_place=true
gpu_optimizer_dispatch_count=1
gpu_optimizer_completion_count=1
gpu_parameter_apply_count=1
```

Forbidden:

```text
temporary GPU result followed by CPU commit
parameter readback followed by host upload
private parameter replacement buffer
detached apply
second optimizer dispatch
```

## 11. AdamW semantics

```text
m_t = beta1 * m_(t-1) + (1 - beta1) * g_t
v_t = beta2 * v_(t-1) + (1 - beta2) * g_t^2
m_hat = m_t / (1 - beta1^t)
v_hat = v_t / (1 - beta2^t)
p_t = p_(t-1)
      - learning_rate * m_hat / (sqrt(v_hat) + epsilon)
      - learning_rate * weight_decay * p_(t-1)
```

Required metadata:

```text
optimizer_kind=adamw
weight_decay_mode=decoupled
epsilon_placement=outside_sqrt
bias_correction_enabled=true
step_index_origin=one_based
gradient_scale_policy=none
gradient_clip_policy=none
```

## 12. Ordered compact evidence

Before dispatch, the command stream copies:

```text
parameter_before
gradient
m_before
v_before
```

After dispatch, it copies:

```text
parameter_after
m_after
v_after
```

For eight `f32` values per region:

```text
7 regions * 8 values * 4 bytes = 224 bytes
```

The scalar loss contributes four additional evidence bytes through the live Burn loss readback.

Canonical evidence payload:

```text
228 bytes
```

The staging allocation may be 256 bytes for alignment.

Full tensor readback is forbidden.

## 13. Independent comparator

The CPU comparator may receive only compact evidence and frozen optimizer metadata.

It independently computes:

```text
cross-entropy loss
LoRA-B gradient
Adam m after
Adam v after
parameter after
```

It may not call the production GPU optimizer or upload its expected values.

Initial tolerance:

```text
absolute_tolerance=1e-5
relative_tolerance=1e-4
comparison_mode=abs_or_relative
```

Required:

```text
parameter_reference_parity_verified=true
moment_m_reference_parity_verified=true
moment_v_reference_parity_verified=true
gradient_reference_parity_verified=true
loss_reference_parity_verified=true
```

## 14. Non-vacuous update

Required:

```text
gradient_nonzero_count>0
gradient_nan_count=0
gradient_inf_count=0
parameter_changed_count>0
moment_m_changed_count>0
moment_v_changed_count>0
```

No-error plus unchanged state is not PASS.

## 15. Synthetic lane elimination

The deterministic fixture remains explicitly fixture-only.

The live lane must report:

```text
synthetic_parameter_buffer_count=0
synthetic_gradient_buffer_count=0
synthetic_optimizer_state_buffer_count=0
synthetic_target_identity_count=0
```

The former hardcoded identity:

```text
authoritative_lm_head_lora_b_window
```

is forbidden as a PASS identity. Truth Audit must reject it.

## 16. Forbidden fallback counters

All must remain zero:

```text
cpu_parameter_apply_count
cpu_optimizer_step_count
cpu_gradient_materialize_for_apply_count
host_parameter_reconstruction_count
host_upload_apply_count
legacy_optimizer_fallback_count
cpu_shadow_state_commit_count
detached_gpu_parameter_apply_count
temporary_result_commit_count
```

`cpu_reference_comparator_count=2` is allowed: one fixture comparator and one live compact comparator.

## 17. Runtime artifact

Path remains:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json
```

Schema:

```text
ash.lora.min1.r1.runtime_artifact.v1.1
```

Atlas Map sections:

```text
identity
raw_borrow
range
optimizer
execution
gradient
ownership
update
parity
evidence
forbidden
authority
terminal
```

Duplicate keys across sections fail artifact assembly.

## 18. Runtime-owned live binding

```text
live_storage_bound =
    parameter raw borrow success
    AND gradient raw borrow success
    AND m state ownership success
    AND v state ownership success
    AND authoritative in-place update target established
```

There is no direct caller setter.

## 19. PASS conditions

```text
fixture_pass=true
live_storage_bound=true
live_pass=true
runtime tensor identity is non-empty and non-hardcoded
parameter and gradient raw borrow successes=1
m and v state ownership successes=1
all authority fields match live owners
target_in_loss_graph=true
target_requires_grad=true
forward/loss/backward counts=1
loss finite=true
gradient nonzero and finite
all same-device fields=true
optimizer_same_queue=true
one dispatch, completion, and in-place apply
parameter/m/v changed
all five comparator results=true
all synthetic counters=0
all fallback counters=0
update_terminal_state=Finalized
lora_min1_physical_proof_pass=true
```

## 20. HOLD conditions

Raw bridge or authoritative gradient unavailability may produce HOLD only when no fallback or synthetic substitution was attempted.

Canonical reasons include:

```text
authoritative_parameter_raw_storage_unavailable
authoritative_gradient_unavailable
authoritative_optimizer_state_unavailable
```

HOLD emits no physical verification authority.

## 21. FAIL conditions

```text
shader or pipeline validation failure
invalid raw range
host-upload bridge
stale or nonfinite gradient
zero gradient
device or queue mismatch
parameter unchanged
m unchanged
v unchanged
reference mismatch
synthetic live substitution
CPU apply
host-upload apply
legacy fallback
second optimizer dispatch
```

## 22. Truth Audit integration

`ASH-TRUTH-AUDIT-01-R2` accepts only schema v1.1 and verifies:

```text
dynamic non-empty runtime tensor identity
hardcoded former identity rejected
all raw borrow success counts=1
all authority values match live owners
authoritative_parameter_in_place=true
all same-device and same-queue fields=true
one forward, backward, dispatch, completion, apply
parameter/m/v changes
all comparator results
all synthetic and fallback counters zero
terminal state Finalized
artifact digest valid
```

Evidence mapping:

```text
authoritative in-place GPU mutation -> RuntimeObservation
independent compact parity -> IndependentComparator
full LoRA MIN1 PASS -> IndependentPhysicalVerification
```

## 23. Governance freeze

This repair does not authorize:

```text
production-sized LM-head training
multi-layer LoRA updates
multiple optimizer steps
gradient accumulation
checkpoint promotion
base-weight updates
full SFT
production model replacement
```

## 24. Canonical seal

```text
A diagnostic buffer is not live LoRA storage.
A hardcoded label is not a parameter identity.
A copied gradient is not live backward authority.

LoRA MIN1 begins at a real Burn model Param and the gradient associated with
that exact ParamId. Both are borrowed from the same registered WGPU runtime.
The native optimizer owns its m/v states on that device and mutates the
borrowed parameter storage in place exactly once.

Compact evidence may observe and compare.
It may not own, apply, reconstruct, upload, or commit.

No synthetic parameter.
No synthetic gradient.
No fake live identity.
No detached GPU result.
No CPU apply fallback.
No receipt-made authority.
```
