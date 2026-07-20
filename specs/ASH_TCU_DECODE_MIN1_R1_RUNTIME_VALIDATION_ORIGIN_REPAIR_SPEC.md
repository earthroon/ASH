# ASH-TCU-DECODE-MIN1-R1 Runtime Validation Origin Repair

# Fixture-First Validation Origin Capture / Argmax-Only Pipeline Isolation /
# Single-Workgroup Direct Readback / First-Error Preservation /
# Invalid Encoder Non-Reuse / Fixture Failure Live-Lane Abort /
# Runtime-Owned Encoder Lifecycle SSOT Seal

- Parent: `ASH-TCU-DECODE-MIN1-R1`
- Patch class: runtime validation origin repair
- Functional revision increase: not authorized
- New production decode revision: not authorized
- New truth-audit revision: not authorized
- New promotion or receipt hierarchy: not authorized
- 16-worker execution: forbidden
- General production apply: not authorized

## 1. Confirmed failure

The current MIN1 run failed before live-model execution:

```text
wgpu Validation Error
In a CommandEncoder
In a pass parameter
Encoder is invalid
```

The artifact simultaneously reported:

```text
fixture_token_parity_verified=false
forward_observed=false
fusion_resolve_ok=false
raw_resource_borrow_ok=false
gpu_argmax_dispatch_count=0
encoder_terminal_state=Invalid
```

Therefore live Fusion resolution and live same-device raw borrowing remain untested. `Encoder is invalid` is treated as a secondary consequence until the first invalidating validation stage is captured.

## 2. Objectives

This repair must:

1. initialize only the pipelines required by the MIN1 argmax fixture;
2. skip the finalize pass when the fixture fits one workgroup;
3. wrap each validation-capable WGPU stage in a validation error scope;
4. preserve the first validation error stage and message;
5. prohibit all encoder operations after invalidation;
6. abort the live lane whenever the fixture lane fails;
7. keep encoder lifecycle state in one runtime-owned SSOT;
8. preserve the existing MIN1 artifact path and patch ID.

## 3. Allowed scope

```text
crates/model_core/src/decode_min1.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_min1_r1.rs
crates/lora_train/src/bin/ash_truth_audit_01_r2.rs
focused MIN1 tests
this specification
```

The existing 16-worker coordinator, sampled decoder, LoRA path, production route, and manifest hierarchy are out of scope.

## 4. Argmax-only fixture initialization

The fixture must not construct the full general-purpose penalty and sampling pipeline collection.

The fixture may initialize only:

```text
argmax first-pass shader
argmax first-pass bind-group layout
argmax first-pass pipeline
optional argmax finalize shader/layout/pipeline
fixture buffers
one command encoder
```

Penalty application, top-N, top-k, top-p, min-p, legacy sampling, and unrelated finalize pipelines must not be created by the fixture.

## 5. Single-workgroup direct readback

The canonical fixture uses:

```text
batch=1
sequence=1
vocab=32
dtype=f32
workgroup_size=256
first_pass_group_count=1
```

Required execution:

```text
first argmax pass
→ copy the first-pass compact result directly
→ 16-byte readback
```

Required counters:

```text
fixture_first_pass_dispatch_count=1
fixture_finalize_dispatch_count=0
fixture_readback_count=1
fixture_readback_bytes=16
```

The single-workgroup path is not a fallback. It is the same argmax authority with an unnecessary reduction stage removed.

For future multi-workgroup fixtures, the finalize pipeline may be created and dispatched only when `first_pass_group_count > 1`.

## 6. Validation stage taxonomy

Canonical fixture stages:

```text
fixture_adapter_request
fixture_device_request
fixture_shader_module_create
fixture_bind_group_layout_create
fixture_first_pipeline_create
fixture_finalize_pipeline_create
fixture_input_buffer_create
fixture_readback_buffer_create
fixture_first_bind_group_create
fixture_finalize_bind_group_create
fixture_encoder_create
fixture_first_pass_record
fixture_finalize_pass_record
fixture_copy_record
fixture_encoder_finish
fixture_queue_submit
fixture_completion_poll
fixture_map_async
fixture_readback_decode
fixture_reference_compare
fixture_finalize
```

A generic `gpu_failed`, `fixture_panic`, or `Encoder is invalid` marker may summarize a failure, but it may not replace the first-stage origin.

## 7. Error-scope contract

Every validation-capable WGPU stage must use:

```text
device.push_error_scope(Validation)
perform exactly one stage
pop the scope
inspect the captured error
```

The first captured validation error owns:

```text
first_validation_error_stage
first_validation_error_message
encoder_invalid_origin
```

Later errors increment `secondary_validation_error_count` and must not overwrite the first origin.

## 8. Encoder lifecycle SSOT

Canonical state:

```text
NotCreated
Created
FirstPassRecorded
FinalizePassRecorded
CopyRecorded
Finished
Submitted
CompletionObserved
ReadbackCompleted
Finalized
Invalid
```

One runtime-owned lifecycle object is authoritative. Receipt-local, shadow, or boolean lifecycle duplicates may not independently decide completion.

Allowed single-workgroup transition:

```text
NotCreated
→ Created
→ FirstPassRecorded
→ CopyRecorded
→ Finished
→ Submitted
→ CompletionObserved
→ ReadbackCompleted
→ Finalized
```

Any validation failure transitions immediately to `Invalid`.

After `Invalid`, the following are forbidden:

```text
begin_compute_pass
copy_buffer_to_buffer
finish
submit
encoder reuse
```

## 9. Panic semantics

`catch_unwind` is only a final process-boundary guard used to write a fail-closed artifact. It is not a validation detector or encoder recovery mechanism.

A panic records:

```text
panic_observed=true
panic_stage=<current boundary>
encoder_terminal_state=Invalid
decode_min1_physical_proof_pass=false
```

A panic hook line on stderr does not create runtime observation or verification authority.

## 10. Fixture-gated live lane

Required order:

```text
fixture device and pipeline validation
→ fixture GPU dispatch
→ fixture compact readback
→ CPU reference comparison
→ fixture_lane_pass=true
→ live_lane_authorized=true
→ live lane may start
```

The live lane must not start when any of the following occurs:

```text
validation error
fixture panic
encoder Invalid
first-pass dispatch count != 1
readback count != 1
readback bytes > 16
token parity mismatch
score parity mismatch
```

Required failure fields:

```text
fixture_lane_pass=false
live_lane_authorized=false
live_lane_started=false
live_lane_skip_reason=<first fixture failure stage>
```

## 11. Buffer and ABI contract

Fixture logits buffer:

```text
usage=STORAGE|COPY_DST
size=32 * sizeof(f32)
```

Partial and final GPU output buffers:

```text
usage includes STORAGE and COPY_SRC
```

Readback buffer:

```text
usage=MAP_READ|COPY_DST
size=16
```

Compact output ABI:

```rust
#[repr(C)]
struct GpuPenaltyArgmaxOut {
    token_id: u32,
    padding0: u32,
    score: f32,
    padding1: f32,
}
```

Required parity:

```text
Rust size=16
WGSL size=16
copy size=16
readback size=16
```

## 12. Artifact schema repair

Canonical path remains:

```text
workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json
```

Schema:

```text
ash.tcu.decode.min1.r1.runtime_artifact.v1.1
```

Required added fields:

```text
repair_id
fixture_lane_pass
live_lane_authorized
live_lane_started
live_lane_skip_reason
last_successful_stage
first_validation_error_stage
first_validation_error_message
encoder_invalid_origin
secondary_validation_error_count
panic_observed
panic_stage
fixture_first_pass_group_count
fixture_first_pass_dispatch_count
fixture_finalize_dispatch_count
fixture_input_buffer_size
fixture_partial_output_buffer_size
fixture_final_output_buffer_size
fixture_readback_buffer_size
fixture_lifecycle_unfinalized_count
live_lifecycle_unfinalized_count
```

Existing MIN1 evidence and digest fields remain.

## 13. Verdict rules

FAIL:

```text
validation error
encoder invalidation
panic
fixture parity mismatch
invalid encoder reuse
binding or pipeline mismatch
readback ABI mismatch
unfinalized lifecycle count > 0
```

HOLD:

```text
fixture passes
live lane starts
live prerequisites remain incomplete without validation contamination
```

PASS additionally requires:

```text
fixture_lane_pass=true
live_lane_authorized=true
live_lane_started=true
first_validation_error_stage=null
encoder_invalid_origin=null
fixture_encoder_terminal_state=finalized
encoder_terminal_state=finalized
fixture and live unfinalized counts=0
all original MIN1 physical proof conditions pass
```

## 14. Truth-audit integration

`ASH-TRUTH-AUDIT-01-R2` may accept artifact schemas `v1` and `v1.1`, but `v1.1` physical proof requires:

```text
fixture_lane_pass=true
live_lane_authorized=true
live_lane_started=true
first_validation_error_stage=null
encoder_invalid_origin=null
fixture_encoder_terminal_state=finalized
fixture_lifecycle_unfinalized_count=0
live_lifecycle_unfinalized_count=0
```

Artifact existence and digest validity alone remain insufficient.

## 15. Required tests

```text
vocab=32 produces one first-pass dispatch and zero finalize dispatches
invalid first pass prevents finalize, copy, finish, submit, and live start
first validation error survives any secondary Encoder-is-invalid message
compact output ABI remains exactly 16 bytes
caller cannot set runtime-owned dispatch, completion, validation, or parity fields
fixture failure leaves live_lane_started=false
```

## 16. Completion definition

The repair is complete when:

```text
fixture initializes only argmax machinery
single-workgroup fixture skips finalize
first validation origin is captured with exact stage and message
invalid encoder is never reused
fixture failure aborts the live lane
fixture token and score match the independent CPU reference
fixture encoder reaches Finalized
```

Live-model PASS remains governed by the original MIN1 completion conditions.

## 17. Canonical seal

```text
An invalid encoder is a consequence, not a root cause.

The first validation error remains authoritative after every secondary
failure, panic hook, lifecycle drop, and fail-closed return.

A failing fixture cannot authorize the live lane.
A single-workgroup argmax cannot execute an unnecessary finalize pass.
No encoder operation is permitted after invalidation.
No generic error may erase the first validation origin.
```
