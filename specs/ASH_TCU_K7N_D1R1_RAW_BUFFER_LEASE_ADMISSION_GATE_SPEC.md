# ASH-TCU-K7N-D1R1 SPEC

## Raw Buffer Lease Admission Gate

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE`
- Status: `PASS_ASH_TCU_K7N_D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE_NO_TOKEN_MINT_NO_SLOT_RESERVATION_NO_RAW_LEASE_NO_SCRATCH_NO_PIPELINE_NO_DISPATCH_NO_OUTPUT_CHANGE`
- Path: `specs/ASH_TCU_K7N_D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE_SPEC.md`
- Class: generation-scoped raw-buffer lease admission contract
- Next: `ASH-TCU-K7N-D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT`

D1R1 seals the admission conditions for one future single-use token, one future consumer-slot reservation, and projection-call-scoped LHS/RHS raw-buffer leases. It does not mint, reserve, export, lease, allocate, create a pipeline, dispatch, read back, compare parity, or change Burn output.

## 2. Parent

Required parent:

- patch: `ASH-TCU-K7N-D1_SINGLE_SHADOW_CONSUMER_CONTRACT`
- execution: `d1-e17507c1631311be4928`
- eligibility: `eligible_for_d1r1_raw_buffer_lease_admission_gate`
- consumer cardinality: `max_one_per_generation_step`
- maximum active consumers: `1`
- slot state: `vacant`
- token state: `unminted`
- consumer instance: `absent`
- current dispatch budget: `0`
- output authority: `burn`
- raw lease authorized: `false`
- pipeline creation authorized: `false`
- dispatch authorized: `false`

Manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d1_local_manifest_latest.json`

## 3. Gate Semantics

D1R1 distinguishes contract admission from resource acquisition.

```text
lease_admission_contract_complete=true
raw_buffer_lease_authorized_for_next_stage=true
raw_buffer_lease_acquired=false
```

The audit binary must remain zero-execution. Authorization applies only to the next named patch consuming the sealed receipt.

## 4. Concrete Generation Owner

Conceptual owner:

`GenerationStepShadowCoordinator`

Concrete owner binding:

- source: `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observer_owner.rs`
- type: `TensorCubeGenerationShadowSession`
- step identity: `TensorCubeGenerationShadowSession::generation_step_ordinal`
- generation epoch identity: `GenerationScopedTensorCubeRouteSnapshot::snapshot_digest`
- cancellation source: `RuntimeEngine::cancel_generation / Arc<AtomicBool>`
- completion source: `TensorCubeGenerationShadowSession::finalize / Finalized`
- owner lifetime: one generation

Cancellation evidence source:

`crates/runtime_unz/src/engine.rs`

Forbidden identity fallbacks:

- local audit counter
- random UUID
- wall-clock time
- process ID
- thread ID
- route epoch alone
- Registry entry
- vector length inference

The step ordinal and generation snapshot epoch remain separate identities.

## 5. Generation Identity Contract

Required:

```text
route_epoch=1
step_id_stable_during_projection=true
epoch_stable_during_projection=true
identity_reuse_across_steps=false
local_counter_fallback_allowed=false
random_identity_fallback_allowed=false
```

The generation-step identity is owned by the existing shadow session. D1R1 does not create a second generation identity SSOT.

## 6. Authority Ownership

Future token mint authority:

`GenerationStepShadowCoordinator`

Future slot reservation authority:

`GenerationStepShadowCoordinator`

Admission evaluation authority:

`SingleShadowLeaseAdmissionGate`

Future lease acquisition authority:

`ActiveSingleShadowConsumerProjectionScope`

The raw bridge, Registry, route snapshot, model singleton, atlas, pipeline cache, and consumer itself are not token-mint authorities.

## 7. Token Mint Gate

Required gate state:

```text
required_slot_state=vacant
route_epoch_required=1
generation_identity_required=true
device_authority_required=true
queue_authority_required=true
runtime_limit_recheck_required=true
revocation_clear_required=true
token_single_use_required=true
token_mint_authorized_for_next_stage=true
token_minted_current_patch=false
```

The token schema remains non-cloneable, non-transferable, and non-reusable.

## 8. Slot Reservation Gate

Required:

```text
initial_state=vacant
reserved_state=reserved
maximum_reservations_per_generation_step=1
valid_token_required=true
same_generation_required=true
same_candidate_required=true
reservation_authorized_for_next_stage=true
reservation_performed_current_patch=false
second_reservation_allowed=false
```

The D1R1 audit result leaves the slot `vacant`.

## 9. Runtime Device Authority

Required source:

- path: `crates/burn_webgpu_backend/src/raw_bridge.rs`
- symbol: `BurnToRawWgpuBridge::device`
- authority: `ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`
- generation: `wgpu-26.0.1`

Required:

```text
same_device_as_burn_backend=true
new_device_creation_allowed=false
device_handle_exported=false
```

## 10. Runtime Queue Authority

Required source:

- path: `crates/burn_webgpu_backend/src/raw_bridge.rs`
- symbol: `BurnToRawWgpuBridge::queue`
- paired Device authority: `ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`

Required:

```text
same_queue_as_burn_backend=true
new_queue_creation_allowed=false
queue_clone_for_background_use_allowed=false
queue_submission_authorized=false
```

D1R1 proves Queue ownership but grants no submission authority.

## 11. Runtime Limit Admission

Required geometry:

```text
workgroup_size=[16,16,1]
invocation_count=256
```

Required named limits:

1. `max_compute_workgroup_size_x`
2. `max_compute_workgroup_size_y`
3. `max_compute_workgroup_size_z`
4. `max_compute_invocations_per_workgroup`
5. `max_compute_workgroups_per_dimension`
6. `max_storage_buffer_binding_size`
7. `min_storage_buffer_offset_alignment`
8. `min_uniform_buffer_offset_alignment`
9. `max_bind_groups`
10. `max_storage_buffers_per_shader_stage`

Required state:

```text
limit_snapshot_required=true
limit_recheck_authorized_for_next_stage=true
limit_recheck_performed_current_patch=false
failure_behavior=fail_closed_to_burn_only
```

D1R1 binds the limit contract. It does not query the runtime Device.

## 12. Raw Reference Export Admission

Required:

```text
lhs_export_required=true
rhs_export_required=true
export_owner=active_single_shadow_consumer_projection_scope
export_scope=projection_call
read_only=true
buffer_handle_clone_allowed=false
exported_reference_storage_allowed=false
exported_reference_escape_allowed=false
export_authorized_for_next_stage=true
export_performed_current_patch=false
```

Raw handles, pointers, and process-local resource IDs must not enter receipts.

## 13. LHS Lease Admission

Required LHS contract:

```text
logical_shape=[M,K]
current_M=1
physical_stride=[K,1]
dtype=f32
read_only=true
nonzero_storage_offset_allowed=true
binding_relative_offset_contract=true
```

Required predicate results:

```text
candidate_identity_match=true
generation_identity_match=true
device_authority_match=true
dtype_match=true
rank_match=true
logical_shape_match=true
physical_stride_match=true
binding_window_proven=true
offset_alignment_proven=true
span_within_buffer_bounds=true
lease_scope_projection_call=true
lease_admission_authorized_for_next_stage=true
lease_acquired_current_patch=false
blocker=none
```

Source evidence is the D0R2R3 LHS precondition and binding-window receipt.

## 14. RHS Lease Admission

Required RHS contract:

```text
stored_shape=[N,K]
stored_stride=[K,1]
logical_shape=[K,N]
logical_stride=[1,K]
dtype=f32
read_only=true
selected_strategy=stride_aware_view
materialized_transpose=false
```

Index identity:

```text
rhs_index = rhs_binding_relative_offset + k + n*K
```

Required predicate results:

```text
candidate_identity_match=true
route_variant_match=true
selected_strategy_match=true
stored_shape_match=true
stored_stride_match=true
logical_shape_match=true
logical_stride_match=true
rhs_index_identity_proven=true
binding_window_proven=true
offset_alignment_proven=true
span_within_buffer_bounds=true
materialization_required=false
lease_scope_projection_call=true
lease_admission_authorized_for_next_stage=true
lease_acquired_current_patch=false
blocker=none
```

Source evidence is the D0R2R3 RHS precondition and binding-window receipt.

## 15. Deterministic Acquisition Order

Future acquisition order:

```text
1. mint one admission token
2. reserve one consumer slot
3. consume token
4. acquire LHS lexical lease
5. acquire RHS lexical lease
6. validate both leases against the frozen snapshot
7. activate the consumer only after both leases pass
```

Required:

```text
lhs_before_rhs=true
both_leases_before_activation=true
both_leases_before_scratch=true
both_leases_before_pipeline=true
```

D1R1 records the order but performs none of its operational steps.

## 16. Partial-Acquisition Rollback

### LHS acquisition failure

```text
rhs_attempted=false
consumer_activated=false
scratch_created=false
terminal_state=failed_closed
Burn_authority_preserved=true
```

### RHS acquisition failure after LHS success

```text
lhs_released=true
rhs_absent=true
consumer_activated=false
scratch_created=false
terminal_state=failed_closed
Burn_authority_preserved=true
```

### Frozen-snapshot mismatch after both acquisitions

```text
lhs_released=true
rhs_released=true
consumer_activated=false
scratch_created=false
terminal_state=invalidated
Burn_authority_preserved=true
```

Required general policy:

```text
release_reverse_order=true
partial_state_reuse_allowed=false
activation_before_both_leases=false
scratch_before_both_leases=false
pipeline_before_both_leases=false
```

## 17. Lease Lifetime

Required:

```text
lhs_scope=projection_call
rhs_scope=projection_call
same_projection_call_required=true
same_generation_step_required=true
same_device_required=true
same_candidate_required=true
may_escape_projection_call=false
may_cross_async_suspend=false
may_be_cloned=false
may_be_stored=false
release_required_before_return=true
```

The generation session may outlive a projection call. Raw leases may not.

## 18. Invalidation Hooks

A future lease is invalidated by:

- generation cancellation
- generation epoch change
- route epoch change
- candidate digest change
- Device loss
- Device authority change
- Queue authority change
- atlas replacement
- model-weight replacement
- binding-window change
- buffer identity change

Required:

```text
stale_lease_reuse_allowed=false
invalidation_receipt_required=true
```

## 19. Admission Snapshot

One immutable snapshot must bind:

- D1 manifest
- generation owner source
- generation identity
- candidate identity
- consumer identity
- token schema
- Device authority
- Queue authority
- runtime-limit contract
- LHS layout and binding window
- RHS layout and binding window
- route epoch
- Burn projection source
- atlas identity
- model-weight identity

The same snapshot drives all gate decisions. Mid-audit refresh is forbidden.

## 20. Admission Receipt

Required PASS receipt:

```text
generation_owner_resolved=true
generation_identity_bound=true
device_authority_bound=true
queue_authority_bound=true
runtime_limit_contract_bound=true
lhs_admission_predicate_pass=true
rhs_admission_predicate_pass=true
acquisition_order_sealed=true
partial_rollback_sealed=true
invalidation_hooks_sealed=true

token_mint_authorized_for_next_stage=true
slot_reservation_authorized_for_next_stage=true
lhs_lease_authorized_for_next_stage=true
rhs_lease_authorized_for_next_stage=true

token_minted_current_patch=false
slot_reserved_current_patch=false
lhs_lease_acquired_current_patch=false
rhs_lease_acquired_current_patch=false
scratch_created_current_patch=false
pipeline_created_current_patch=false
dispatch_performed_current_patch=false
Burn_authority_preserved=true
```

## 21. Eligibility

Required eligibility:

`eligible_for_d1r2_scratch_and_pipeline_admission_contract`

Blocked classes include:

- parent D1 contract invalid
- generation owner unresolved
- generation identity unresolved
- token authority unresolved
- slot authority unresolved
- Device authority unresolved
- Queue authority unresolved
- runtime-limit contract incomplete
- raw reference export path unresolved
- LHS predicate incomplete
- RHS predicate incomplete
- acquisition order incomplete
- partial rollback incomplete
- invalidation incomplete
- protected-state drift
- execution contamination

## 22. Zero-Execution Contract

All counters must remain zero:

```text
shadow_consumer_instance_count
shadow_consumer_reservation_count
shadow_consumer_activation_count
admission_token_mint_count
admission_token_consume_count
raw_buffer_reference_export_count
raw_buffer_lease_count
lhs_raw_buffer_lease_count
rhs_raw_buffer_lease_count
buffer_handle_clone_count
runtime_limit_query_count
scratch_output_creation_count
output_buffer_creation_count
binding_resource_creation_count
bind_group_layout_creation_count
bind_group_creation_count
shader_module_creation_count
pipeline_layout_creation_count
compute_pipeline_creation_count
command_encoder_creation_count
queue_submit_count
tensorcube_dispatch_count
readback_count
parity_comparison_count
shadow_output_commit_count
downstream_output_commit_count
registry_write_count
route_mutation_count
route_epoch_change_count
runtime_output_change_count
model_weight_mutation_count
new_runtime_device_count
new_runtime_queue_count
```

## 23. Protected State

Hash before and after:

- Registry v4
- route epoch and slots
- D1 final seal and manifest
- D1 consumer identity, owner, and token schema
- D0R2R3 LHS/RHS lease preconditions and binding windows
- D0R3 candidate evidence
- runtime WGPU authority source
- raw bridge source
- K6P config and shader
- Burn vocab-atlas projection
- vocab-atlas weights
- model weights

Required differences: zero.

## 24. Burn Authority

Required expression remains:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

Required downstream path:

```text
Burn tile logits
→ merged logits
→ final TensorData
→ sampler
```

D1R1 inserts no output into this path.

## 25. Implementation Files

Backend modules:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_generation_owner_binding.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_generation_identity_contract.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_token_mint_gate.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_slot_reservation_gate.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_runtime_device_authority.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_runtime_queue_authority.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_runtime_limit_contract.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_raw_reference_export_admission.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_lhs_lease_admission.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_rhs_lease_admission.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_lease_acquisition_order.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_partial_acquisition_rollback.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_lease_lifetime_contract.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_lease_invalidation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_admission_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_admission_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_contract_audit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r1_verdict.rs
```

Model integration:

`crates/model_core/src/vocab_atlas_raw_buffer_lease_admission_gate.rs`

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r1_raw_buffer_lease_admission_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r1_raw_buffer_lease_admission_gate.rs
```

The audit binary path-binds the D1R1 modules.

## 26. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r1_raw_buffer_lease_admission_gate -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1-pass `
  --require-d1-execution d1-e17507c1631311be4928 `
  --require-d1r1-lease-admission-eligibility `
  --require-consumer-cardinality max_one_per_generation_step `
  --require-max-active-consumers 1 `
  --require-slot-state vacant `
  --require-token-state unminted `
  --require-consumer-state absent `
  --require-current-dispatch-budget 0 `
  --require-selected-strategy stride_aware_view `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-full-tile-candidate-only `
  --require-ragged-tail-burn-only `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --resolve-concrete-generation-step-owner `
  --bind-generation-step-identity-source `
  --bind-generation-epoch-source `
  --bind-generation-cancellation-source `
  --bind-generation-completion-source `
  --reject-local-generation-counter-fallback `
  --bind-token-mint-authority `
  --bind-slot-reservation-authority `
  --bind-runtime-device-authority `
  --bind-runtime-queue-authority `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --bind-runtime-device-limit-contract `
  --require-future-runtime-limit-recheck `
  --bind-raw-buffer-reference-export-admission `
  --bind-lhs-lease-admission-predicate `
  --bind-rhs-lease-admission-predicate `
  --verify-lhs-binding-window `
  --verify-rhs-binding-window `
  --verify-storage-offset-alignment `
  --verify-binding-relative-offset-contract `
  --verify-rhs-index-identity `
  --require-no-transpose-materialization `
  --seal-deterministic-lease-acquisition-order `
  --require-lhs-before-rhs-acquisition `
  --require-both-leases-before-activation `
  --bind-partial-acquisition-rollback `
  --bind-lease-lifetime-contract `
  --bind-lease-invalidation-hooks `
  --authorize-next-stage-token-mint `
  --authorize-next-stage-slot-reservation `
  --authorize-next-stage-lhs-lease `
  --authorize-next-stage-rhs-lease `
  --classify-d1r1-admission-eligibility `
  --require-no-shadow-consumer-instance `
  --require-no-shadow-consumer-reservation `
  --require-no-shadow-consumer-activation `
  --require-no-admission-token-mint `
  --require-no-admission-token-consume `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-runtime-limit-query `
  --require-no-scratch-output `
  --require-no-binding-resource `
  --require-no-bind-group-layout `
  --require-no-bind-group `
  --require-no-shader-module `
  --require-no-pipeline-layout `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-tensorcube-dispatch `
  --require-no-readback `
  --require-no-parity-comparison `
  --require-no-shadow-output-commit `
  --require-no-downstream-output-commit `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-d1-consumer-contract-unchanged `
  --verify-d0r3-candidate-contract-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-audit-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-performance-claim
```

## 27. PASS

Marker:

`PASS_ASH_TCU_K7N_D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE_NO_TOKEN_MINT_NO_SLOT_RESERVATION_NO_RAW_LEASE_NO_SCRATCH_NO_PIPELINE_NO_DISPATCH_NO_OUTPUT_CHANGE`

Verdict:

`generation_scoped_raw_buffer_lease_admission_gate_sealed_with_concrete_generation_owner_token_and_slot_authorities_burn_runtime_device_queue_binding_runtime_limit_recheck_lhs_rhs_predicates_deterministic_acquisition_partial_rollback_and_invalidation_proven_and_candidate_eligible_for_d1r2_scratch_and_pipeline_admission_without_token_mint_slot_reservation_raw_lease_scratch_pipeline_dispatch_or_output_change`

Expected state:

```text
lease_admission_eligibility=eligible_for_d1r2_scratch_and_pipeline_admission_contract
generation_owner_source=resolved
generation_identity_source=resolved
token_mint_authority=generation_step_shadow_coordinator
slot_reservation_authority=generation_step_shadow_coordinator
runtime_device_authority=burn_wgpu_runtime
runtime_queue_authority=burn_wgpu_runtime
runtime_limit_recheck_required=true
lhs_lease_admission=authorized_for_next_stage
rhs_lease_admission=authorized_for_next_stage
lease_acquisition_order=lhs_then_rhs
partial_acquisition_rollback=sealed
lease_invalidation_hooks=sealed
token_minted=false
slot_reserved=false
consumer_activated=false
lhs_lease_acquired=false
rhs_lease_acquired=false
scratch_output_state=absent
pipeline_creation_authorized=false
dispatch_authorized=false
output_authority=burn
runtime_output_changed=false
```

## 28. Non-Authorization

D1R1 PASS does not authorize token mint, token consumption, slot reservation, consumer activation, raw-reference export, LHS or RHS lease acquisition, Device or Queue creation, Queue submission, runtime-limit query, scratch allocation, binding creation, shader or pipeline creation, command encoding, dispatch, readback, parity, output commit, ragged-tail execution, Registry registration, route-epoch change, promotion, performance claims, or production-readiness claims.

Only `ASH-TCU-K7N-D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT` is authorized next.
