# ASH-TCU-K7N-D1 SPEC

## Single Shadow Consumer Contract

## 1. Identity

- Patch: `ASH-TCU-K7N-D1_SINGLE_SHADOW_CONSUMER_CONTRACT`
- Status: `PASS_ASH_TCU_K7N_D1_SINGLE_SHADOW_CONSUMER_CONTRACT_NO_CONSUMER_INSTANCE_NO_TOKEN_MINT_NO_RAW_LEASE_NO_PIPELINE_NO_DISPATCH_NO_OUTPUT_CHANGE`
- Path: `specs/ASH_TCU_K7N_D1_SINGLE_SHADOW_CONSUMER_CONTRACT_SPEC.md`
- Class: generation-scoped shadow-consumer ownership contract
- Next: `ASH-TCU-K7N-D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE`

D1 seals ownership, cardinality, admission-token schema, lexical lifetime, scratch ownership, no-commit policy, cancellation, invalidation, and result-receipt schema for one shadow consumer. It does not instantiate a consumer, mint a token, acquire a raw-buffer lease, create scratch output, create a pipeline, dispatch TensorCube, read back output, compare parity, or change Burn output.

## 2. Parent

Required parent:

- patch: `ASH-TCU-K7N-D0R3_VOCAB_ATLAS_TILE_CANDIDATE_CLOSURE_AUDIT`
- execution: `d0r3-b8b46b862fbf3f493bf3`
- eligibility: `eligible_for_d1_single_shadow_consumer_contract`
- strategy: `stride_aware_view`
- route: `ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`
- full tile: true
- ragged tail: false
- output authority: Burn
- runtime execution: false
- raw lease: false
- pipeline creation: false
- dispatch: false
- parity: not executed

Manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r3_local_manifest_latest.json`

## 3. State Ownership SSOT

Owner kind:

`GenerationStepShadowCoordinator`

Ownership hierarchy:

```text
generation step
└─ GenerationStepShadowCoordinator
   └─ maximum one shadow consumer slot
      └─ one vocab-atlas projection invocation
         ├─ future LHS/RHS lexical leases
         └─ future scratch output
```

The D1 contract defines the owner boundary but does not bind a concrete runtime generation-step source. Concrete source binding is reserved for D1R1.

Required owner state:

```text
owner_scope=one_active_generation_step
consumer_subscope=one_vocab_atlas_projection_invocation
concrete_runtime_source_bound=false
runtime_source_binding_authorized=false
pending_runtime_source_patch=ASH-TCU-K7N-D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE
```

Forbidden owners:

- global or static state
- Registry v4
- route registry or route snapshot
- model singleton
- vocab-atlas object
- persistent runtime cache
- worker-global state
- next-token session cache

## 4. Consumer Identity

Required values:

```text
consumer_kind=vocab_atlas_full_tile_projection_shadow
callsite=call-66cc14a91d31bf8452215b67
route_variant=ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1
selected_rhs_strategy=stride_aware_view
generation_owner_kind=generation_step_shadow_coordinator
```

The consumer identity digest binds the D0R3 candidate identity, callsite, route variant, strategy, and owner kind.

## 5. Cardinality

```text
minimum_consumers_per_generation_step=0
maximum_consumers_per_generation_step=1
maximum_active_consumers=1
maximum_admission_tokens=1
token_reuse_allowed=false
slot_rearm_allowed=false
second_activation_allowed=false
```

Consumer cardinality is not a tile-dispatch count. D1 authorizes zero dispatches.

## 6. Slot State Machine

States:

```text
Vacant
Reserved
Active
CompletedNoCommit
Cancelled
Invalidated
FailedClosed
```

Allowed transitions:

```text
Vacant -> Reserved
Reserved -> Active
Reserved -> Cancelled
Reserved -> Invalidated
Active -> CompletedNoCommit
Active -> Cancelled
Active -> Invalidated
Active -> FailedClosed
```

Terminal states cannot return to `Vacant` within the same generation step. A new generation step requires a new slot.

## 7. Admission Token Schema

D1 defines a type-level token schema only.

```text
generation_step_id_required=true
generation_epoch_required=true
route_epoch_required=true
route_epoch_value=1
single_use=true
cloneable=false
transferable=false
reusable=false
mint_authorized=false
activation_authorized=false
```

Future token authority is the `GenerationStepShadowCoordinator`. The consumer, route snapshot, Registry, model, atlas, GPU backend, and global helper cannot mint the token.

## 8. Lifetime

```text
owner_scope=generation_step
maximum_consumer_scope=projection_invocation
maximum_input_lease_scope=projection_call
maximum_scratch_scope=projection_invocation
may_escape_generation_step=false
may_escape_projection_call=false
may_be_stored_in_route_snapshot=false
may_be_stored_in_registry=false
may_be_sent_to_background_task=false
```

Consumer descriptor lifetime and raw-buffer lease lifetime are distinct. A future lease cannot survive the projection call.

## 9. Lexical Lease Contract

```text
lhs_lease_required=true
rhs_lease_required=true
output_lease_required=false
lease_scope=projection_call
lease_owner=active_single_shadow_consumer
lease_clone_allowed=false
lease_escape_allowed=false
lease_storage_allowed=false
lease_acquisition_authorized=false
```

Required future acquisition order:

1. validate admission token
2. validate slot
3. validate candidate digests
4. validate route epoch
5. validate Device and Queue authority
6. validate runtime device limits
7. acquire LHS lexical lease
8. acquire RHS lexical lease
9. acquire scratch ownership
10. activate consumer

Partial acquisition cannot activate the consumer or commit output.

## 10. Scratch Output Ownership

```text
owner=active_single_shadow_consumer
logical_shape=[M,N]
dtype=f32
creation_authorized=false
reuse_across_generation_steps=false
reuse_across_consumers=false
may_attach_to_model=false
may_attach_to_atlas=false
may_attach_to_route_snapshot=false
may_enter_merged_logits=false
may_enter_sampler=false
commit_authorized=false
destruction_required=true
```

Shadow scratch is observational only. Burn remains the only downstream output authority.

## 11. No-Commit Policy

Forbidden flows:

```text
shadow scratch -> merged logits
shadow scratch -> final logits
shadow scratch -> sampler
shadow scratch -> next-token decision
shadow scratch -> KV-state mutation
```

Preserved flow:

```text
Burn tile logits -> merged logits -> final TensorData -> sampler
```

## 12. Dispatch Budget

```text
maximum_consumer_activations_per_generation_step=1
authorized_dispatches_current_patch=0
maximum_tile_dispatches_future=unbound
budget_source=d1r1_or_later_explicit_contract
budget_rebind_required=true
budget_exhaustion_behavior=fail_closed_to_burn_only
dispatch_authorized=false
```

D1 does not infer a future dispatch budget from atlas tile count.

## 13. Cancellation and Invalidation

Cancellation sources:

- generation cancellation
- projection cancellation
- user abort
- runtime shutdown
- budget revocation
- admission revocation

Cancellation properties:

```text
partial_commit_allowed=false
partial_result_authoritative=false
burn_recompute_required=false
burn_output_preserved=true
terminal_state=cancelled
cancellation_receipt_required=true
```

Invalidation triggers:

- candidate, kernel, binding, or geometry digest drift
- route epoch change
- device loss
- atlas replacement
- model-weight change
- generation-step end
- lease failure
- pipeline-admission failure

Stale consumer reuse is forbidden.

## 14. Result Receipt Initial State

```text
slot_state=vacant
execution_state=not_instantiated
generation_step_id=none
generation_epoch=none
admission_token_digest=none
dispatch_count=0
scratch_created=false
readback_performed=false
parity_performed=false
output_committed=false
burn_output_authority_preserved=true
```

## 15. Rollback

Target:

`no_shadow_consumer_burn_only`

```text
consumer_slot_present=false
admission_token_present=false
raw_lease_present=false
scratch_present=false
pipeline_present=false
dispatch_present=false
burn_authority_preserved=true
evidence_preserved=true
route_mutation_required=false
```

D1 failure does not delete D0R3 candidate evidence.

## 16. Eligibility

Required PASS eligibility:

`eligible_for_d1r1_raw_buffer_lease_admission_gate`

PASS means the ownership contract is complete. It does not mean a consumer exists or execution is admitted.

## 17. Zero-Execution Counters

All must remain zero:

- consumer instance, reservation, and activation
- admission-token mint and consumption
- Buffer export, raw lease, and handle clone
- scratch and output-buffer creation
- binding resource, bind-group layout, and bind group
- shader module, pipeline layout, and compute pipeline
- command encoder, Queue submit, and TensorCube dispatch
- readback, parity comparison, and output commit
- Registry write, route mutation, and route epoch change
- runtime output change and model-weight mutation
- new Device and Queue

## 18. Protected State

Hash before and after:

- D0R3 manifest and final seal
- D0R3 candidate identity, kernel, binding, dispatch, parity, rollback, admission, and revocation receipts
- Registry v4 and route epoch
- WGPU raw bridge
- canonical K6P config and WGSL
- Burn vocab-atlas projection
- model weights

Required differences: zero.

Preserved expression:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

## 19. Implementation Files

Backend contracts:

- `tensorcube_k7n_d1_shadow_consumer_identity.rs`
- `tensorcube_k7n_d1_generation_step_owner.rs`
- `tensorcube_k7n_d1_consumer_cardinality.rs`
- `tensorcube_k7n_d1_consumer_slot_state.rs`
- `tensorcube_k7n_d1_admission_token_schema.rs`
- `tensorcube_k7n_d1_consumer_lifetime.rs`
- `tensorcube_k7n_d1_lexical_lease_contract.rs`
- `tensorcube_k7n_d1_scratch_output_ownership.rs`
- `tensorcube_k7n_d1_no_commit_policy.rs`
- `tensorcube_k7n_d1_dispatch_budget.rs`
- `tensorcube_k7n_d1_cancellation_contract.rs`
- `tensorcube_k7n_d1_invalidation_contract.rs`
- `tensorcube_k7n_d1_result_receipt_schema.rs`
- `tensorcube_k7n_d1_no_shadow_rollback.rs`
- `tensorcube_k7n_d1_single_shadow_consumer_contract.rs`
- `tensorcube_k7n_d1_contract_audit.rs`
- `tensorcube_k7n_d1_verdict.rs`

Model integration:

- `vocab_atlas_single_shadow_consumer_contract.rs`

Orchestrator:

- `ash_tcu_k7n_d1_single_shadow_consumer_contract_report.rs`
- `ash_tcu_k7n_d1_single_shadow_consumer_contract_audit.rs`

The audit binary path-binds D1 modules so crate-root overlay order cannot cause E0432 failures.

## 20. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1_single_shadow_consumer_contract_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r3-pass `
  --require-d0r3-execution d0r3-b8b46b862fbf3f493bf3 `
  --require-d1-shadow-consumer-contract-eligibility `
  --require-selected-strategy stride_aware_view `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-full-tile-candidate-only `
  --require-ragged-tail-burn-only `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --bind-single-shadow-consumer-identity `
  --bind-generation-step-owner-contract `
  --require-max-one-consumer-per-generation-step `
  --require-max-one-active-consumer `
  --bind-single-use-admission-token-schema `
  --reject-token-clone `
  --reject-token-transfer `
  --reject-token-reuse `
  --bind-consumer-slot-state-machine `
  --reject-slot-rearm-within-generation-step `
  --bind-projection-invocation-consumer-lifetime `
  --bind-projection-call-lexical-lease-boundary `
  --reject-consumer-generation-step-escape `
  --reject-lease-projection-call-escape `
  --bind-shadow-scratch-output-ownership `
  --require-shadow-output-no-commit `
  --reject-shadow-output-merged-logits-entry `
  --reject-shadow-output-sampler-entry `
  --bind-zero-dispatch-budget `
  --require-future-dispatch-budget-rebind `
  --bind-cancellation-contract `
  --bind-invalidation-contract `
  --bind-shadow-result-receipt-schema `
  --require-result-state-not-instantiated `
  --bind-no-shadow-rollback-contract `
  --verify-burn-output-authority `
  --classify-d1-contract-eligibility `
  --require-no-shadow-consumer-instance `
  --require-no-shadow-consumer-reservation `
  --require-no-shadow-consumer-activation `
  --require-no-admission-token-mint `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
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

## 21. PASS

Marker:

`PASS_ASH_TCU_K7N_D1_SINGLE_SHADOW_CONSUMER_CONTRACT_NO_CONSUMER_INSTANCE_NO_TOKEN_MINT_NO_RAW_LEASE_NO_PIPELINE_NO_DISPATCH_NO_OUTPUT_CHANGE`

Verdict:

`single_generation_step_owned_shadow_consumer_contract_sealed_with_cardinality_one_single_use_admission_projection_call_lexical_lease_scratch_no_commit_cancellation_invalidation_result_receipt_and_burn_authority_preserved_without_consumer_instantiation_token_mint_raw_lease_pipeline_dispatch_or_output_change`

Expected state:

```text
consumer_contract_eligibility=eligible_for_d1r1_raw_buffer_lease_admission_gate
consumer_cardinality=max_one_per_generation_step
maximum_active_consumers=1
slot_state=vacant
admission_token_state=unminted
consumer_instance_state=absent
consumer_activation_state=not_activated
current_dispatch_budget=0
future_tile_dispatch_budget=unbound
scratch_output_state=absent
shadow_output_commit_authorized=false
output_authority=burn
runtime_execution_authorized=false
raw_buffer_lease_authorized=false
pipeline_creation_authorized=false
dispatch_authorized=false
parity_state=not_executed
```

## 22. Non-Authorization

D1 PASS does not authorize consumer creation, reservation, activation, token mint, token consumption, raw-buffer lease, scratch allocation, binding or pipeline creation, dispatch, readback, parity, output commit, ragged-tail execution, Registry registration, route-epoch change, promotion, performance claims, or production-readiness claims.

Only `ASH-TCU-K7N-D1R1_RAW_BUFFER_LEASE_ADMISSION_GATE` is authorized next.
