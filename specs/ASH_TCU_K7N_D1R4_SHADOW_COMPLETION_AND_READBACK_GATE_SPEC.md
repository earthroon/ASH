# ASH-TCU-K7N-D1R4 SPEC

## Shadow Completion and Readback Gate

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R4_SHADOW_COMPLETION_AND_READBACK_GATE`
- Status: `PASS_ASH_TCU_K7N_D1R4_SHADOW_COMPLETION_AND_READBACK_GATE_ONE_DISPATCH_ONE_COPY_TWO_SUBMITS_ONE_BOUNDED_MAP_16_FINITE_F32_NO_PARITY_NO_OUTPUT_COMMIT`
- Path: `specs/ASH_TCU_K7N_D1R4_SHADOW_COMPLETION_AND_READBACK_GATE_SPEC.md`
- Class: bounded completion observation and scratch readback gate
- Next: `ASH-TCU-K7N-D1R5_NUMERICAL_PARITY_GATE`

D1R4 replays the sealed deterministic fixture in a fresh bounded process. It does not resurrect D1R3 process-local buffers, devices, queues, submission indices, or raw handles.

## 2. Parent

Required parent:

- patch: `ASH-TCU-K7N-D1R3_SINGLE_SHADOW_DISPATCH`
- execution: `d1r3-8078717eea17f15ae8f7`
- eligibility: `eligible_for_d1r4_shadow_completion_and_readback_gate`
- submission state: `submitted_unobserved`
- GPU completion observed: false
- readback performed: false
- output authority: Burn

Parent manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r3_local_manifest_latest.json`

## 3. Process Boundary

D1R4 consumes D1R3 evidence, not D1R3 GPU resources. The current execution creates a new authoritative Burn runtime context and reproduces the same fixture contract.

Forbidden:

- restoring raw WGPU handles from JSON
- reusing a process-local submission index
- locating prior scratch in Registry
- reactivating the prior generation slot

## 4. Runtime Authority

Required authority:

`ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`

Required Device and Queue source:

- `BurnToRawWgpuBridge::device`
- `BurnToRawWgpuBridge::queue`

Required counts:

```text
burn_runtime_context_count=1
tensorcube_extra_device_count=0
tensorcube_extra_queue_count=0
```

Dispatch, copy and map must use the same authoritative Burn runtime.

## 5. Deterministic Fixture

Fixture ID:

`ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1`

Geometry:

```text
M=1
N=16
K=4
workgroup=16x16x1
dispatch=1x1x1
```

LHS shape is `[1,4]`. Stored RHS shape is `[16,4]`. Logical RHS view is `[4,16]` with stride `[1,4]`. Transpose materialization is forbidden.

## 6. Strict Primitive Registration

Required registration:

```text
LHS Fusion tensor ID -> LHS raw CubeTensor
RHS Fusion tensor ID -> RHS raw CubeTensor
```

Required counters:

```text
fixture_handle_registration_count=2
primitive_handle_map_hits=2
primitive_handle_map_misses=0
raw_borrows=2
host_uploads=0
metadata_only=0
```

Host-upload and metadata-only fallback are forbidden.

## 7. Current Execution Sequence

```text
create deterministic fixture
-> register two raw primitives
-> invoke D1R2 preparation once
-> dispatch TensorCube once
-> submit dispatch command buffer once
-> retain current scratch capsule
-> create one 64-byte staging buffer
-> encode one scratch-to-staging copy
-> submit copy command buffer once
-> request one READ map
-> bounded poll
-> observe map completion
-> read exactly 64 bytes
-> decode exactly 16 f32 values
-> require all 16 values finite
-> release mapped range
-> unmap staging once
-> seal readback receipt
```

## 8. Dispatch Cardinality

Required:

```text
runtime_preparation_count=1
token_mint_count=1
slot_reservation_count=1
consumer_activation_count=1
lhs_lease_count=1
rhs_lease_count=1
prepared_bundle_count=1
prepared_bundle_consumed=true

dispatch_command_encoder_count=1
compute_pass_count=1
dispatch_call_count=1
dispatch_command_buffer_count=1
dispatch_queue_submit_count=1
```

No second dispatch or same-generation retry is allowed.

## 9. Staging and Copy

Staging buffer:

```text
size=64 bytes
usage=MAP_READ | COPY_DST
mapped_at_creation=false
```

Copy contract:

```text
source=scratch
destination=staging
source_offset=0
destination_offset=0
copy_size=64 bytes
```

Required copy counters:

```text
staging_buffer_count=1
copy_command_encoder_count=1
copy_buffer_to_buffer_count=1
copy_command_buffer_count=1
copy_queue_submit_count=1
```

Total Queue submissions:

```text
total_queue_submit_count=2
```

Submit 1 is dispatch. Submit 2 is scratch-to-staging copy.

## 10. Bounded Map and Completion

Required map:

```text
mode=READ
offset=0
size=64 bytes
map_async_count=1
```

Required bounded poll policy:

```text
maximum_duration_ms=10000
maximum_poll_iterations=1024
infinite_wait=false
```

Completion authority:

`staging_map_after_ordered_dispatch_and_copy`

A successful staging map after the ordered copy proves that both the preceding dispatch and copy completed on the same Queue.

Required state:

```text
gpu_completion_observed=true
bounded_poll_completed=true
```

Queue submit return alone is not completion evidence.

## 11. Readback Contract

Required:

```text
readback_byte_length=64
readback_f32_count=16
finite_count=16
non_finite_count=0
```

Exact IEEE-754 bit patterns must be retained. Negative zero and finite subnormal values must not be normalized. NaN and infinities block the gate.

Required receipt digests:

- raw bytes digest
- sixteen-value bit-pattern digest

## 12. No Numerical Parity

D1R4 must not compute:

- CPU reference matmul
- Burn reference vector comparison
- absolute error
- relative error
- ULP distance
- tolerance result
- parity PASS or FAIL

Required state:

```text
parity_state=not_evaluated
parity_performed=false
```

Finite readback is not numerical correctness.

## 13. No Output Commit

Required:

```text
shadow_output_commit_authorized=false
shadow_output_committed=false
merged_logits_mutated=false
sampler_input_mutated=false
output_authority=burn
runtime_output_changed=false
```

Readback values are evidence only.

## 14. Cleanup

Required order:

```text
copy mapped bytes to owned array
-> drop mapped-range view
-> unmap staging buffer
-> release staging
-> release scratch resources
```

Required counters:

```text
mapped_range_release_count=1
staging_unmap_count=1
```

Mapped slices and raw pointers must not enter JSON receipts.

## 15. Failure Closure

Before dispatch submit, failure submits nothing. After dispatch submit, work is contained rather than falsely rolled back. Copy failure requests no map. Map timeout, map failure, device loss, byte-length mismatch, decode failure, or non-finite values all fail closed.

Every error path preserves Burn output authority and performs no parity or output commit.

## 16. Required Files

Backend:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_execution_mode.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_readback_capsule.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_staging_buffer.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_copy_encoding.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_bounded_poll.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_completion_observation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_mapped_range_validation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_f32_readback.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_finite_gate.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_readback_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_readback_error.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_cancellation_containment.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_device_loss.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_runtime_readback.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_contract_audit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r4_verdict.rs
```

Model contract:

`crates/model_core/src/vocab_atlas_shadow_completion_readback_contract.rs`

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r4_shadow_completion_readback_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r4_shadow_completion_and_readback_gate.rs
```

## 17. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r4_shadow_completion_and_readback_gate -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r3-pass `
  --require-d1r3-execution d1r3-8078717eea17f15ae8f7 `
  --require-d1r4-readback-eligibility `
  --require-parent-submission-state submitted_unobserved `
  --require-parent-gpu-completion-unobserved `
  --require-parent-readback-false `
  --require-runtime-device-authority burn_wgpu_runtime `
  --require-runtime-queue-authority burn_wgpu_runtime `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-route-epoch 1 `
  --execution-mode completion_and_readback_audit `
  --reject-parent-resource-resurrection `
  --build-deterministic-runtime-fixture `
  --require-fixture-id ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1 `
  --require-fixture-m 1 `
  --require-fixture-n 16 `
  --require-fixture-k 4 `
  --register-two-fixture-primitives `
  --require-primitive-handle-map-hits 2 `
  --require-primitive-handle-map-misses 0 `
  --require-host-upload-count 0 `
  --invoke-runtime-preparation-exactly-once `
  --dispatch-workgroups-exactly-once `
  --submit-dispatch-command-buffer-exactly-once `
  --retain-submitted-readback-capsule `
  --create-one-staging-buffer `
  --require-staging-size-bytes 64 `
  --require-staging-usage map_read_copy_dst `
  --create-one-copy-command-encoder `
  --copy-scratch-to-staging-exactly-once `
  --require-copy-size-bytes 64 `
  --finish-one-copy-command-buffer `
  --submit-copy-command-buffer-exactly-once `
  --require-total-queue-submit-count 2 `
  --map-staging-read-exactly-once `
  --require-map-offset 0 `
  --require-map-size-bytes 64 `
  --poll-map-to-bounded-deadline `
  --require-poll-timeout-ms 10000 `
  --require-max-poll-iterations 1024 `
  --require-completion-method staging_map_after_ordered_dispatch_and_copy `
  --require-gpu-completion-observed `
  --validate-mapped-range-length 64 `
  --decode-readback-f32-count 16 `
  --preserve-readback-f32-bits `
  --require-finite-count 16 `
  --require-non-finite-count 0 `
  --write-raw-bytes-digest `
  --write-value-bits-digest `
  --release-mapped-range `
  --unmap-staging-exactly-once `
  --require-parity-state not_evaluated `
  --require-no-cpu-reference-matmul `
  --require-no-absolute-error `
  --require-no-relative-error `
  --require-no-tolerance-judgment `
  --require-no-shadow-output-commit `
  --require-no-downstream-output-commit `
  --verify-burn-output-authority `
  --classify-d1r4-readback-eligibility `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-d1r3-dispatch-contract-unchanged `
  --verify-d1r2-preparation-contract-unchanged `
  --verify-d1r1-admission-contract-unchanged `
  --verify-d1-consumer-contract-unchanged `
  --verify-d0r3-candidate-contract-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-runtime-readback-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-performance-claim
```

## 18. PASS Marker

```text
PASS_ASH_TCU_K7N_D1R4_SHADOW_COMPLETION_AND_READBACK_GATE_ONE_DISPATCH_ONE_COPY_TWO_SUBMITS_ONE_BOUNDED_MAP_16_FINITE_F32_NO_PARITY_NO_OUTPUT_COMMIT
```

## 19. PASS Verdict

```text
one_projection_scoped_tensorcube_shadow_dispatch_and_one_ordered_scratch_to_staging_copy_completed_on_the_authoritative_burn_wgpu_runtime_with_exactly_two_queue_submissions_one_bounded_map_and_exactly_sixteen_finite_f32_values_observed_and_candidate_eligible_for_d1r5_numerical_parity_without_cpu_reference_comparison_tolerance_judgment_output_commit_route_mutation_or_burn_authority_change
```

Expected state:

```text
shadow_completion_readback_eligibility=eligible_for_d1r5_numerical_parity_gate
execution_mode=completion_and_readback_audit
fixture_id=ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1
runtime_authority=burn_wgpu_runtime
primitive_handle_registration_count=2
primitive_handle_map_hits=2
primitive_handle_map_misses=0
host_upload_count=0
runtime_preparation_count=1
dispatch_call_count=1
dispatch_queue_submit_count=1
staging_buffer_count=1
copy_call_count=1
copy_queue_submit_count=1
total_queue_submit_count=2
map_async_count=1
bounded_poll_completed=true
completion_observation_method=staging_map_after_ordered_dispatch_and_copy
gpu_completion_observed=true
readback_byte_length=64
readback_f32_count=16
finite_count=16
non_finite_count=0
parity_state=not_evaluated
parity_performed=false
shadow_output_commit_authorized=false
shadow_output_committed=false
output_authority=burn
runtime_output_changed=false
```

## 20. Non-Authorization

D1R4 PASS does not authorize a second dispatch, second readback, full-vocab production routing, ragged-tail execution, persistent scratch or staging storage, persistent mapped memory, CPU reference matmul, absolute or relative error calculation, ULP comparison, tolerance judgment, numerical parity, shadow-output commit, Burn-output replacement, merged-logits substitution, sampler substitution, Registry registration, route-epoch mutation, production promotion, performance claims, or production-readiness claims.

## 21. Next State

Only the following patch is authorized next:

`ASH-TCU-K7N-D1R5_NUMERICAL_PARITY_GATE`

D1R5 consumes the sixteen-f32 readback evidence, computes the deterministic reference, evaluates absolute and relative error under explicit tolerances, records mismatch indices, and still performs no output commit.