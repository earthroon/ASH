# ASH-LORA-MIN1-R1

# One GPU Parameter Update / Independent Before-After and Reference Parity /
# Same-Device Gradient and Optimizer State Binding / Compact Evidence Readback /
# Zero CPU Apply Fallback Physical Proof Seal

## 0. Metadata

- Parent truth authority: `ASH-TRUTH-AUDIT-01-R2`
- Sibling proof: `ASH-TCU-DECODE-MIN1-R1`
- Patch class: minimal LoRA training physical proof
- Production training promotion: not authorized
- Multi-batch training: forbidden
- Checkpoint promotion: not authorized
- New receipt hierarchy: not authorized

## 1. Purpose

The current truth audit accepts Decode MIN1 but remains HOLD because LoRA has no runtime-owned physical update proof. LoRA MIN1 proves the smallest non-vacuous unit:

```text
one GPU-owned LoRA parameter region
-> one forward result
-> one scalar loss
-> one gradient
-> one AdamW m update
-> one AdamW v update
-> one parameter update
-> one compact readback
-> one independent reference comparison
```

Requested, performed, observed, and verified meanings remain separate. A request, dispatch plan, counter, or propagated `verified` field cannot create physical authority.

## 2. Two-lane proof

```text
Lane A: deterministic AdamW fixture parity
Lane B: runtime-owned lm_head.lora_b parameter window
```

Both lanes execute the native WGPU update kernel. Both are compared with an independent CPU reference. The CPU may compare compact evidence but may not apply, reconstruct, upload, or commit the update.

## 3. Canonical evidence window

```text
element_count=8
parameter_dtype=f32
accumulator_dtype=f32
step=1
```

The selected region is fixed before dispatch. Post hoc selection of changed elements is forbidden.

## 4. Forward, loss, and gradient contract

The MIN1 kernel computes:

```text
prediction = sum(parameter[i] * input[i])
loss = 0.5 * (prediction - target)^2
gradient[i] = (prediction - target) * input[i]
```

The selected parameter is therefore directly present in the loss graph.

Required:

```text
forward_count=1
loss_compute_count=1
backward_count=1
target_in_loss_graph=true
target_requires_grad=true
loss_is_finite=true
```

A caller-provided post-backward gradient is forbidden.

## 5. Canonical AdamW semantics

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

## 6. Same-device ownership

Parameter, gradient, Adam m, Adam v, input, loss, pipeline, and queue must belong to one WGPU execution context.

```text
parameter_same_device=true
gradient_same_device=true
moment_m_same_device=true
moment_v_same_device=true
optimizer_same_queue=true
```

Cross-device copies, host reconstruction, and legacy optimizer storage are forbidden.

## 7. Ordered before and after evidence

The command encoder records:

```text
copy parameter_before
copy m_before
copy v_before
dispatch forward/backward/AdamW
copy gradient
copy parameter_after
copy m_after
copy v_after
copy loss
```

The before snapshot must precede the update in the same command stream.

## 8. Compact readback

For eight `f32` elements:

```text
parameter_before  32 bytes
m_before          32 bytes
v_before          32 bytes
gradient          32 bytes
parameter_after   32 bytes
m_after           32 bytes
v_after           32 bytes
loss               4 bytes
total             228 bytes
```

The staging allocation may be 256 bytes for alignment, but the artifact records the 228-byte evidence payload. Readback above 512 bytes is forbidden. Full LoRA tensors, full gradients, and full optimizer states may not be mapped.

## 9. Independent comparator

The CPU reference receives only compact canonical input values and frozen hyperparameters. It independently computes gradient, loss, parameter after, m after, and v after.

It may not call the GPU kernel, derive expected values from GPU output, or upload expected values into live parameter storage.

Initial `f32` tolerance:

```text
absolute_tolerance=1e-5
relative_tolerance=1e-4
comparison_mode=abs_or_relative
```

Required parity:

```text
parameter_reference_parity_verified=true
moment_m_reference_parity_verified=true
moment_v_reference_parity_verified=true
gradient_reference_parity_verified=true
loss_reference_parity_verified=true
```

## 10. Non-vacuous gradient and update

```text
gradient_resolve_attempt_count=1
gradient_resolve_success_count=1
gradient_nonzero_count>0
gradient_nan_count=0
gradient_inf_count=0

gpu_optimizer_dispatch_count=1
gpu_optimizer_completion_count=1
gpu_parameter_apply_count=1
parameter_changed_count>0
moment_m_changed_count>0
moment_v_changed_count>0
```

No-error with zero gradient or unchanged state cannot pass.

## 11. Zero CPU apply seal

All must remain zero:

```text
cpu_parameter_apply_count
cpu_optimizer_step_count
cpu_gradient_materialize_for_apply_count
host_parameter_reconstruction_count
host_upload_apply_count
legacy_optimizer_fallback_count
cpu_shadow_state_commit_count
```

`cpu_reference_comparator_count` is allowed because it is comparison-only.

## 12. Runtime artifact

Canonical path:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json
```

Schema:

```text
ash.lora.min1.r1.runtime_artifact.v1
```

Canonical identity:

```text
patch_id=ASH-LORA-MIN1-R1
target_module_id=lm_head.lora_b
target_parameter_kind=lora_b
target_parameter_element_count=8
```

Compatibility fields consumed by R2 are derived from detailed runtime evidence:

```text
dispatch_observed
parameter_delta_observed
optimizer_state_delta_observed
reference_parity_verified
observed_execution_count
verified_result_count
```

Caller input cannot set these fields.

## 13. Artifact digest

The digest covers the canonical JSON after replacing `artifact_digest` with an empty string.

```text
artifact_digest=sha256:<hex>
```

The digest proves integrity only, not physical execution.

## 14. Lifecycle

```text
NotStarted
-> TargetResolved
-> BeforeSnapshotCaptured
-> ForwardCompleted
-> LossCompleted
-> BackwardCompleted
-> GradientResolved
-> OptimizerPrepared
-> EncoderCreated
-> UpdateRecorded
-> Submitted
-> CompletionObserved
-> AfterSnapshotCaptured
-> ReferenceCompared
-> Finalized
```

Validation error, panic, device loss, map failure, comparator failure, or forbidden fallback moves the lifecycle to `Invalid`. A second optimizer dispatch is forbidden.

## 15. PASS

LoRA MIN1 passes only when:

```text
fixture_pass=true
live_pass=true
target_in_loss_graph=true
target_requires_grad=true
forward_count=1
loss_compute_count=1
backward_count=1
loss_is_finite=true
gradient_resolve_success_count=1
gradient_nonzero_count>0
gradient_nan_count=0
gradient_inf_count=0
all same-device fields=true
optimizer_same_queue=true
gpu_optimizer_dispatch_count=1
gpu_optimizer_completion_count=1
gpu_parameter_apply_count=1
parameter_changed_count>0
moment_m_changed_count>0
moment_v_changed_count>0
all reference parity fields=true
all CPU apply and fallback counters=0
update_terminal_state=Finalized
lora_min1_physical_proof_pass=true
```

## 16. FAIL

The following force failure:

```text
validation error
panic
device loss
map failure
zero or nonfinite gradient
parameter unchanged
m unchanged
v unchanged
reference mismatch
CPU apply
host-upload apply
legacy optimizer fallback
readback above 512 bytes
second optimizer dispatch
PASS with zero execution
```

## 17. Truth-audit integration

`ASH-TRUTH-AUDIT-01-R2` accepts:

```text
--lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json
```

It verifies schema, patch ID, digest, non-vacuous counters, same-device ownership, parameter/m/v changes, all comparator results, zero forbidden counters, and terminal state.

Evidence mapping:

```text
GPU completion + compact before/after -> RuntimeObservation
independent parameter/m/v/gradient/loss parity -> IndependentComparator
full LoRA MIN1 PASS -> IndependentPhysicalVerification
```

## 18. Governance freeze

This proof does not authorize full base training, multi-layer LoRA training, long SFT runs, checkpoint promotion, optimizer-state checkpoint promotion, Atlas-wide apply, production replacement, or a new manifest authority.

## 19. Canonical seal

```text
LoRA training is not proven because an optimizer step was requested.
LoRA training is not proven because a dispatch was reported.
LoRA training is not proven because a counter advanced.

LoRA MIN1 is proven only when one GPU-owned LoRA parameter region participates
in a real loss graph, produces a nonzero finite gradient, updates parameter,
Adam m and Adam v on one GPU queue, and an independent reference reproduces the
compact observed result.

The CPU may compare compact evidence.
The CPU may not apply, reconstruct, upload or commit the update.

One forward.
One backward.
One GPU optimizer dispatch.
One compact comparison.
No zero-gradient PASS.
No unchanged-state PASS.
No CPU apply fallback.
No receipt-made authority.
```
