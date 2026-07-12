# ASH-TCU-K7N-D1R3 SPEC

## Single Shadow Dispatch

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R3_SINGLE_SHADOW_DISPATCH`
- Status: `PASS_ASH_TCU_K7N_D1R3_SINGLE_SHADOW_DISPATCH_ONE_PREPARATION_ONE_COMMAND_BUFFER_ONE_DISPATCH_ONE_SUBMIT_NO_READBACK_NO_PARITY_NO_OUTPUT_COMMIT`
- Path: `specs/ASH_TCU_K7N_D1R3_SINGLE_SHADOW_DISPATCH_SPEC.md`
- Class: bounded projection-scoped TensorCube shadow submission
- Next: `ASH-TCU-K7N-D1R4_SHADOW_COMPLETION_AND_READBACK_GATE`

D1R3 is the first K7N patch that executes one real TensorCube GPU submission. It consumes one projection-scoped D1R2 preparation bundle, encodes one compute pass, calls `dispatch_workgroups` once, and submits one command buffer to the authoritative Burn WGPU Queue.

D1R3 does not observe completion, copy or map scratch, read back output, compare numerical parity, commit shadow output, replace Burn output, mutate merged logits, or promote a route.

## 2. Parent

Required parent:

- patch: `ASH-TCU-K7N-D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT`
- execution: `d1r2-4857eac4166c9b66504e`
- eligibility: `eligible_for_d1r3_single_shadow_dispatch_contract`
- preparation path: `implemented_not_invoked`
- prepared bundle lifetime: `projection_call`
- prepared bundle cloneable: false
- persistent pipeline cache: false
- output authority: Burn

Parent manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r2_local_manifest_latest.json`

## 3. Submission Boundary

D1R3 distinguishes Queue submission from GPU completion.

```text
submission_state=submitted_unobserved
gpu_completion_observed=false
```

A successful `Queue::submit` proves that one command buffer was submitted. It does not prove shader completion, valid scratch contents, numerical correctness, or parity with Burn.

Completion observation and scratch readback remain exclusive to D1R4.

## 4. Execution Mode

```rust
pub enum TensorCubeShadowExecutionMode {
    Disabled,
    SingleDispatchAudit,
}
```

Default mode is `Disabled`.

Only explicit audit CLI configuration may select `SingleDispatchAudit`. Environment variables, debug builds, file presence, Registry state, GPU vendor, random sampling, and production fallback must not activate D1R3.

## 5. Runtime Authority

Required authority:

`ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`

Required Device and Queue sources:

- `BurnToRawWgpuBridge::device`
- `BurnToRawWgpuBridge::queue`

Required cardinality:

```text
burn_runtime_context_count=1
tensorcube_extra_device_count=0
tensorcube_extra_queue_count=0
```

The fixture tensors, raw leases, scratch, pipeline, encoder, and Queue submission must use the same authoritative Burn WGPU runtime.

## 6. Deterministic Fixture

Fixture ID:

`ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1`

Dimensions:

```text
M=1
N=16
K=4
```

LHS:

```text
shape=[1,4]
stride=[4,1]
dtype=f32
values=[1.0,-2.0,0.5,3.0]
```

Stored RHS:

```text
shape=[16,4]
stride=[4,1]
dtype=f32
```

For row `n`:

```text
rhs[n,0]=n+1
rhs[n,1]=-(n+2)
rhs[n,2]=(n+3)*0.25
rhs[n,3]=(n*2)+1
```

Logical post-swap RHS:

```text
shape=[4,16]
stride=[1,4]
strategy=stride_aware_view
materialized_transpose=false
```

D1R3 does not inspect numerical output.

## 7. Ownership

Conceptual owner:

`GenerationStepShadowCoordinator`

Concrete owner lineage:

- generation owner: `TensorCubeGenerationShadowSession`
- step ID source: `generation_step_ordinal`
- generation epoch identity: generation-scoped route snapshot digest
- cancellation source: `RuntimeEngine::cancel_generation / Arc<AtomicBool>`
- completion boundary: `TensorCubeGenerationShadowSession::finalize`

The audit fixture uses generation step ID `1` as explicit fixture data, not as a process-global fallback counter.

## 8. Preparation Bundle and Permit

D1R3 invokes the D1R2 entry point exactly once:

`prepare_vocab_atlas_shadow_dispatch`

The returned SSOT is:

`PreparedShadowDispatchBundle<'projection>`

The bundle is consumed by value. A reusable borrowed bundle or arbitrary individual buffers must not be accepted by the dispatch function.

D1R2 retains:

```text
dispatch_authorized_current_patch=false
```

D1R3 does not rewrite that parent invariant. Explicit `SingleDispatchAudit` mode mints a D1R3-only non-cloneable, non-reusable `SingleUseShadowDispatchPermit`.

One bundle and one permit authorize at most one dispatch.

## 9. Exactly-Once Cardinality

Required successful counts:

```text
runtime_preparation_invocation_count=1
admission_token_mint_count=1
admission_token_consume_count=1
shadow_consumer_reservation_count=1
shadow_consumer_activation_count=1
runtime_limit_query_count=1
lhs_raw_buffer_lease_count=1
rhs_raw_buffer_lease_count=1
abi_param_buffer_creation_count=1
scratch_output_creation_count=1
bind_group_layout_creation_count=1
shader_module_creation_count=1
pipeline_layout_creation_count=1
compute_pipeline_creation_count=1
bind_group_creation_count=1
prepared_bundle_creation_count=1
prepared_bundle_consumption_count=1
command_encoder_creation_count=1
compute_pass_creation_count=1
pipeline_set_count=1
bind_group_set_count=1
tensorcube_dispatch_call_count=1
command_buffer_finish_count=1
queue_submit_count=1
```

Second dispatch, second permit, same-generation retry, second encoder, second pass, second command buffer, and second Queue submission must fail closed.

## 10. Strict Raw Leases

Required bridge evidence:

```text
BridgeStats.raw_borrows=2
BridgeStats.host_uploads=0
```

One raw borrow belongs to LHS and one to RHS. Host-upload fallback is forbidden because it would invalidate the D1R1/D1R2 lexical raw-lease chain.

## 11. Pre-Dispatch Revalidation

Immediately before command encoding, D1R3 revalidates:

- cancellation remains clear
- generation step ID remains `1`
- route epoch remains `1`
- candidate identity matches the permit
- preparation snapshot digest matches the permit
- dispatch geometry digest matches the permit
- fixture is exactly `M1/N16/K4`
- scratch is `[1,16]`, 16 f32 values, 64 bytes
- full-tile policy remains true
- ragged-tail policy remains false

Failure before encoding produces zero dispatch and zero submit.

## 12. Full-Write Static Proof

D1R3 does not read scratch. It binds a static proof to the canonical shader, entry point, workgroup geometry, fixture shape, and output-index mapping.

Required fixture proof:

```text
valid_output_write_count=16
guarded_nonwriter_count=240
```

Each valid output element has exactly one responsible invocation. Out-of-range invocations perform no output write. Scratch is not read before write and output atomics are absent.

The proof must be derived from canonical shader source. Workgroup size alone is not sufficient evidence.

## 13. Command Encoding

Required operations:

```rust
let mut encoder = device.create_command_encoder(...);
{
    let mut pass = encoder.begin_compute_pass(...);
    pass.set_pipeline(&bundle.resources.compute_pipeline);
    pass.set_bind_group(0, &bundle.resources.bind_group, &[]);
    pass.dispatch_workgroups(1, 1, 1);
}
let command_buffer = encoder.finish();
```

Required geometry:

```text
workgroup_geometry=16x16x1
dispatch_geometry=1x1x1
```

Exactly one encoder, one compute pass, one pipeline bind, one bind-group bind, one dispatch call, and one command-buffer finish are allowed.

Timestamp queries, dynamic offsets, push constants, alternate pipelines, buffer copies, scratch clear, render passes, and second compute passes are forbidden.

## 14. Queue Submission

Required operation:

```rust
let submission_index = queue.submit(std::iter::once(command_buffer));
```

Required Queue:

`BurnToRawWgpuBridge::queue`

Required counts:

```text
queue_submit_call_count=1
submitted_command_buffer_count=1
```

Raw submission indices are process-local evidence and must not enter canonical digests. The receipt records only `submission_index_observed=true`.

## 15. No Completion Claim

D1R3 must not call:

- `device.poll`
- completion callback APIs
- `map_async`
- scratch readback

Required state:

```text
submission_observed=true
completion_observed=false
```

## 16. Scratch State

Required scratch:

```text
logical_shape=[1,16]
dtype=f32
element_count=16
span_bytes=64
usage=STORAGE|COPY_SRC
```

Before dispatch:

`scratch_content_state=undefined`

After submission:

`scratch_content_state=submitted_write_unobserved`

Required zero counts:

```text
scratch_clear_count=0
scratch_copy_count=0
scratch_map_count=0
scratch_readback_count=0
scratch_commit_count=0
```

## 17. Submitted State

Required submitted state:

```text
submission_state=SubmittedUnobserved
readback_authorized=false
parity_authorized=false
output_commit_authorized=false
```

The submitted object is consumed into a no-readback observational receipt. Raw WGPU handles must not be serialized or persisted in Registry, route snapshots, model state, static caches, or background tasks.

## 18. Slot State

Allowed transition:

```text
Active -> SubmittedNoReadback
```

`SubmittedNoReadback` is terminal for D1R3.

It must not transition back to Active, Reserved, or Vacant, and it must not authorize a second dispatch.

## 19. Cancellation and Failure

Cancellation checkpoints are required:

1. before runtime preparation
2. after preparation and before encoder creation
3. after command-buffer finish and immediately before Queue submit

Before-submit failure uses lexical reverse-order release and produces zero Queue submissions.

After Queue submit, work cannot be retracted. D1R3 uses containment, not rollback:

- scratch remains non-authoritative
- no readback
- no parity
- no commit
- no merged-logits mutation
- no sampler mutation
- Burn remains authoritative

Asynchronous device loss after submit is classified as completion unobserved, not success or failure. D1R4 owns completion and device-loss observation.

## 20. Burn Output Authority

Required authority:

`Burn`

Preserved expression:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

Required downstream path:

```text
Burn tile-local logits
-> merged logits
-> final TensorData
-> sampler
```

The shadow submission is sidecar-only. Burn output must not wait for or depend on scratch.

## 21. Allowed and Forbidden Runtime Operations

Allowed only in the D1R3 runtime dispatch module:

- `prepare_vocab_atlas_shadow_dispatch`
- `create_command_encoder`
- `begin_compute_pass`
- `set_pipeline`
- `set_bind_group`
- `dispatch_workgroups`
- `finish`
- `Queue::submit`

Forbidden:

- buffer copy
- scratch clear
- `map_async`
- `device.poll`
- completion callback
- readback
- parity comparison
- shadow-output commit
- Burn-output replacement
- merged-logits mutation
- route mutation
- Registry write

## 22. Required Files

Backend:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_execution_mode.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_runtime_fixture.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_dispatch_cardinality.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_single_use_dispatch_permit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_pre_dispatch_revalidation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_full_write_proof.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_command_encoding.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_queue_submission.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_submitted_shadow_dispatch.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_submission_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_dispatch_error.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_pre_submit_rollback.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_post_submit_containment.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_single_shadow_dispatch.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_contract_audit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r3_verdict.rs
```

Model contract:

`crates/model_core/src/vocab_atlas_single_shadow_dispatch_contract.rs`

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r3_single_shadow_dispatch_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r3_single_shadow_dispatch.rs
```

## 23. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r3_single_shadow_dispatch -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r2-pass `
  --require-d1r2-execution d1r2-4857eac4166c9b66504e `
  --require-d1r3-dispatch-eligibility `
  --require-runtime-preparation-path implemented_not_invoked `
  --require-prepared-bundle-lifetime projection_call `
  --require-prepared-bundle-non-cloneable `
  --require-no-persistent-pipeline-cache `
  --require-runtime-device-authority burn_wgpu_runtime `
  --require-runtime-queue-authority burn_wgpu_runtime `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-route-epoch 1 `
  --require-full-tile-candidate-only `
  --require-ragged-tail-burn-only `
  --execution-mode single_dispatch_audit `
  --bind-actual-shadow-dispatch-callsite `
  --require-callsite-id call-66cc14a91d31bf8452215b67 `
  --build-deterministic-runtime-fixture `
  --require-fixture-id ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1 `
  --require-fixture-m 1 `
  --require-fixture-n 16 `
  --require-fixture-k 4 `
  --require-rhs-strategy stride_aware_view `
  --require-no-transpose-materialization `
  --create-one-authoritative-burn-runtime-context `
  --reject-extra-tensorcube-device `
  --reject-extra-tensorcube-queue `
  --invoke-runtime-preparation-exactly-once `
  --require-token-mint-count 1 `
  --require-slot-reservation-count 1 `
  --require-token-consume-count 1 `
  --require-runtime-limit-query-count 1 `
  --require-lhs-lease-count 1 `
  --require-rhs-lease-count 1 `
  --require-consumer-activation-count 1 `
  --require-prepared-bundle-count 1 `
  --verify-prepared-bundle-consumed-by-value `
  --bind-single-use-dispatch-permit `
  --reject-second-dispatch-permit `
  --revalidate-frozen-snapshot-before-dispatch `
  --verify-full-write-static-proof `
  --require-valid-output-write-count 16 `
  --require-guarded-nonwriter-count 240 `
  --require-workgroup-geometry 16x16x1 `
  --require-dispatch-geometry 1x1x1 `
  --create-one-command-encoder `
  --create-one-compute-pass `
  --set-one-pipeline `
  --set-one-bind-group `
  --dispatch-workgroups-exactly-once `
  --finish-one-command-buffer `
  --submit-one-command-buffer `
  --require-submission-state submitted_unobserved `
  --require-submission-index-observed `
  --require-gpu-completion-unobserved `
  --seal-no-readback-submission-receipt `
  --verify-pre-submit-rollback-contract `
  --verify-post-submit-containment-contract `
  --verify-burn-output-authority `
  --classify-d1r3-dispatch-eligibility `
  --require-runtime-preparation-invocation-count 1 `
  --require-command-encoder-count 1 `
  --require-compute-pass-count 1 `
  --require-dispatch-call-count 1 `
  --require-command-buffer-count 1 `
  --require-queue-submit-count 1 `
  --require-no-second-dispatch `
  --require-no-second-submit `
  --require-no-scratch-clear `
  --require-no-buffer-copy `
  --require-no-device-poll `
  --require-no-completion-callback `
  --require-no-readback `
  --require-no-parity-comparison `
  --require-no-shadow-output-commit `
  --require-no-downstream-output-commit `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-d1r2-preparation-contract-unchanged `
  --verify-d1r1-admission-contract-unchanged `
  --verify-d1-consumer-contract-unchanged `
  --verify-d0r3-candidate-contract-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-runtime-dispatch-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-performance-claim
```

## 24. PASS Marker

```text
PASS_ASH_TCU_K7N_D1R3_SINGLE_SHADOW_DISPATCH_ONE_PREPARATION_ONE_COMMAND_BUFFER_ONE_DISPATCH_ONE_SUBMIT_NO_READBACK_NO_PARITY_NO_OUTPUT_COMMIT
```

## 25. PASS Verdict

```text
one_projection_scoped_tensorcube_shadow_dispatch_submitted_on_the_authoritative_burn_wgpu_runtime_with_exactly_one_preparation_token_slot_activation_lhs_rhs_lease_command_encoder_compute_pass_dispatch_command_buffer_and_queue_submission_full_tile_static_write_coverage_proven_and_candidate_eligible_for_d1r4_completion_and_readback_without_gpu_completion_claim_readback_parity_output_commit_route_mutation_or_burn_authority_change
```

Expected state:

```text
single_shadow_dispatch_eligibility=eligible_for_d1r4_shadow_completion_and_readback_gate
execution_mode=single_dispatch_audit
fixture_id=ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1
runtime_authority=burn_wgpu_runtime
runtime_preparation_count=1
token_mint_count=1
slot_reservation_count=1
consumer_activation_count=1
lhs_lease_count=1
rhs_lease_count=1
prepared_bundle_count=1
prepared_bundle_consumed=true
command_encoder_count=1
compute_pass_count=1
dispatch_call_count=1
command_buffer_count=1
queue_submit_count=1
workgroup_geometry=16x16x1
dispatch_geometry=1x1x1
valid_output_write_count=16
guarded_nonwriter_count=240
submission_state=submitted_unobserved
submission_index_observed=true
gpu_completion_observed=false
readback_performed=false
parity_performed=false
shadow_output_commit_authorized=false
shadow_output_committed=false
output_authority=burn
runtime_output_changed=false
```

## 26. Non-Authorization

D1R3 PASS does not authorize a second dispatch, same-generation retry, persistent prepared-bundle storage, persistent pipeline cache, production full-vocab routing, ragged-tail dispatch, GPU-completion claims, polling, completion callbacks, staging-buffer allocation, scratch copy, `map_async`, readback, numerical parity, output commit, Burn-output replacement, merged-logits substitution, sampler substitution, Registry registration, route-epoch mutation, production promotion, performance claims, or production-readiness claims.

## 27. Next State

Only the following patch is authorized next:

`ASH-TCU-K7N-D1R4_SHADOW_COMPLETION_AND_READBACK_GATE`

D1R4 must consume the submitted-unobserved contract, observe completion and device-loss state, allocate one staging buffer, perform exactly one scratch-to-staging copy and bounded map, validate 64 bytes of finite f32 data, and still perform no numerical parity judgment or output commit.