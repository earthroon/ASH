# ASH-TCU-K7N-D1R2 SPEC

## Scratch and Pipeline Admission Contract

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT`
- Status: `PASS_ASH_TCU_K7N_D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT_PREPARATION_PATH_SEALED_NO_RUNTIME_PREPARATION_INVOCATION_NO_DISPATCH_NO_READBACK_NO_PARITY_NO_OUTPUT_COMMIT`
- Path: `specs/ASH_TCU_K7N_D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT_SPEC.md`
- Class: projection-scoped shadow resource preparation contract
- Next: `ASH-TCU-K7N-D1R3_SINGLE_SHADOW_DISPATCH`

D1R2 implements a projection-scoped preparation path for one future shadow dispatch. The audit proves the path without invoking it. It does not encode commands, dispatch, submit, read back, compare parity, commit shadow output, or replace Burn output.

## 2. Parent

Required D1R1 state:

- execution: `d1r1-2c56e90fa4b95b5635ac`
- eligibility: `eligible_for_d1r2_scratch_and_pipeline_admission_contract`
- generation owner and identity: resolved
- token mint authority: `generation_step_shadow_coordinator`
- slot reservation authority: `generation_step_shadow_coordinator`
- Device and Queue authority: `burn_wgpu_runtime`
- LHS/RHS lease admission: `authorized_for_next_stage`
- lease order: `lhs_then_rhs`
- partial rollback and invalidation: sealed
- token, slot, leases, scratch, pipeline: absent
- output authority: Burn

Manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r1_local_manifest_latest.json`

## 3. Core Distinction

```text
runtime_preparation_path_implemented=true
runtime_preparation_path_invoked_current_audit=false
```

Implementation existence is not runtime invocation.

## 4. State Ownership SSOT

Runtime owner:

`ActiveSingleShadowConsumerProjectionScope`

Resource-bundle SSOT:

`PreparedShadowDispatchBundle<'projection>`

The bundle owns the consumed admission proof, active consumer guard, Device-limit snapshot, LHS/RHS leases, 64-byte ABI buffer, scratch buffer, bind-group layout, shader module, pipeline layout, compute pipeline, and bind group.

The bundle must not implement `Clone`, `Copy`, `Serialize`, `Deserialize`, `Send`, or `Sync`. It must not escape the projection call.

## 5. Runtime Entry Point

```rust
pub fn prepare_vocab_atlas_shadow_dispatch<'projection>(
    coordinator: &mut GenerationStepShadowCoordinator,
    bridge: &'projection BurnToRawWgpuBridge,
    lhs: &'projection Tensor<InferenceBackend, 2>,
    rhs: &'projection Tensor<InferenceBackend, 2>,
    projection: VocabAtlasProjectionInvocation,
    snapshot: ShadowPreparationSnapshot,
    stats: &mut BridgeStats,
) -> Result<PreparedShadowDispatchBundle<'projection>, ShadowPreparationError>
```

Properties:

- crate-internal, synchronous, projection-call scoped
- full-tile only
- ragged tail rejected
- no background task, Registry registration, or route mutation

## 6. Type-State and Order

```text
Vacant slot
→ one token mint
→ one slot reservation
→ token consumption
→ runtime Device-limit snapshot
→ LHS strict lexical lease
→ RHS strict lexical lease
→ frozen snapshot revalidation
→ consumer activation
→ ABI params and 64-byte uniform buffer
→ scratch allocation
→ explicit bind-group layout
→ canonical shader module
→ explicit pipeline layout
→ ephemeral compute pipeline
→ bind group
→ PreparedShadowDispatchBundle seal
```

Constructors for token, reservation, activation, and bundle sealing remain private to D1R2 modules.

## 7. Runtime Limits

The authoritative Burn WGPU Device is checked for workgroup dimensions, invocations, workgroups per dimension, storage binding size, storage/uniform alignment, bind groups, and storage/uniform buffers per stage.

Required geometry:

```text
workgroup=16x16x1
invocations=256
```

No reduced-workgroup fallback is permitted.

## 8. Input Leases

LHS:

```text
shape=[M,K]
stride=[K,1]
dtype=f32
read-only=true
binding-relative offset=true
```

RHS:

```text
stored shape=[N,K]
stored stride=[K,1]
logical shape=[K,N]
logical stride=[1,K]
dtype=f32
strategy=stride_aware_view
materialized transpose=false
```

RHS index:

`rhs_binding_relative_offset + k + n*K`

Lease clone, serialization, persistent storage, async escape, and cross-generation reuse are forbidden.

## 9. Snapshot Revalidation

After both leases and before activation, revalidate generation step ID, generation epoch digest, route epoch, candidate and consumer digests, Device/Queue authority, buffer windows, atlas and model identity, and cancellation state.

Failure drops leases, marks the slot invalidated or failed-closed, creates no scratch or pipeline, and preserves Burn authority.

## 10. ABI and Scratch

ABI:

```text
16 u32 words
64 bytes
Rust/WGSL field-order parity
binding-relative offsets
```

Scratch:

```text
shape=[M,N]
dtype=f32
span=checked_mul(checked_mul(M,N),4)
usage=STORAGE | COPY_SRC
mapped_at_creation=false
output_commit_authorized=false
```

Scratch contents are undefined until D1R3 proves full shader-write coverage. D1R2 performs no clear dispatch or readback.

## 11. Binding and Pipeline SSOT

Group 0:

```text
binding 0 = LHS read-only storage
binding 1 = RHS read-only storage
binding 2 = scratch read-write storage
binding 3 = 64-byte uniform params
```

Shader:

`crates/burn_webgpu_backend/src/shaders/tensorcube_k7n_d0r3_vocab_atlas_tile_candidate_16x16_kpanel4.wgsl`

Entry point: `main`

Route variant: `ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`

Pipeline rules:

```text
explicit bind-group layout=true
explicit pipeline layout=true
push constants=none
pipeline cache=none
cross-generation pipeline reuse=false
```

## 12. Dispatch Capability Boundary

The only future dispatch capability is `PreparedShadowDispatchBundle<'projection>`. D1R3 must consume it by value. A dispatch function accepting arbitrary independent buffers or pipelines is forbidden.

Current state:

`dispatch_authorized_current_patch=false`

## 13. Rollback

Semantic reverse drop order:

```text
bind group
→ compute pipeline
→ pipeline layout
→ shader module
→ bind-group layout
→ scratch
→ ABI parameter buffer
→ active consumer guard
→ RHS lease
→ LHS lease
→ slot guard
```

No slot rearm or same-generation retry is allowed. Dropping a prepared bundle must never trigger dispatch or Queue submission.

## 14. Static Call-Graph Gate

Preparation must reach token, reservation, consumption, limit query, LHS/RHS lease, revalidation, activation, params, scratch, bind-group layout, shader, pipeline layout, compute pipeline, bind group, and bundle seal.

Preparation must not reach command encoder, compute pass, dispatch, Queue submit, copy, map/readback, parity, output commit, merged logits, route mutation, or Registry writes.

String tables in the audit are not executable reachability evidence. The audit checks call-shaped use in the runtime preparation module.

## 15. Zero Audit Execution

During D1R2 audit, all runtime preparation, token, slot, limit query, lease, parameter buffer, scratch, bind-group, shader, pipeline, command, dispatch, submit, readback, parity, output commit, route mutation, output change, and weight mutation counters remain zero.

## 16. Protected State

Before and after hashes must match for Registry v4, route slots/epoch, D1R1 receipts, D1 contract, D0R3 candidate identity/bindings/kernel/geometry, K6P config/WGSL, raw bridge, Burn projection, atlas weights, and model weights.

## 17. Implementation Surfaces

Backend modules use the prefix:

`crates/burn_webgpu_backend/src/tensorcube_k7n_d1r2_`

They include preparation snapshot/error, token, slot, limits, leases, revalidation, activation, ABI buffer, scratch, bind-group layout, shader, pipeline layout, compute pipeline, bind group, prepared bundle, rollback, runtime prepare, receipt, audit, and verdict.

Model integration:

`crates/model_core/src/vocab_atlas_shadow_dispatch_preparation_contract.rs`

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r2_scratch_and_pipeline_admission_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r2_scratch_and_pipeline_admission_contract.rs
```

## 18. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r2_scratch_and_pipeline_admission_contract -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r1-pass `
  --require-d1r1-execution d1r1-2c56e90fa4b95b5635ac `
  --require-d1r2-admission-eligibility `
  --require-generation-owner-resolved `
  --require-generation-identity-resolved `
  --require-token-mint-authority generation_step_shadow_coordinator `
  --require-slot-reservation-authority generation_step_shadow_coordinator `
  --require-runtime-device-authority burn_wgpu_runtime `
  --require-runtime-queue-authority burn_wgpu_runtime `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-lhs-lease-admission authorized_for_next_stage `
  --require-rhs-lease-admission authorized_for_next_stage `
  --require-lease-order lhs_then_rhs `
  --require-partial-rollback-sealed `
  --require-lease-invalidation-sealed `
  --require-route-epoch 1 `
  --require-full-tile-candidate-only `
  --require-ragged-tail-burn-only `
  --bind-runtime-preparation-entry-point `
  --verify-single-use-token-mint-path `
  --verify-single-slot-reservation-path `
  --verify-token-consumption-path `
  --verify-runtime-limit-query-path `
  --verify-lhs-lease-runtime-path `
  --verify-rhs-lease-runtime-path `
  --verify-frozen-snapshot-revalidation-path `
  --verify-consumer-activation-path `
  --verify-abi-parameter-construction `
  --verify-abi-parameter-buffer-path `
  --verify-scratch-allocation-path `
  --verify-explicit-bind-group-layout-path `
  --verify-canonical-shader-module-path `
  --verify-explicit-pipeline-layout-path `
  --verify-compute-pipeline-path `
  --verify-bind-group-path `
  --verify-prepared-dispatch-bundle-path `
  --verify-preparation-type-state-order `
  --verify-token-before-reservation `
  --verify-runtime-limits-before-leases `
  --verify-lhs-before-rhs-acquisition `
  --verify-both-leases-before-activation `
  --verify-snapshot-revalidation-before-activation `
  --verify-scratch-after-activation `
  --verify-bind-group-after-all-resources `
  --verify-prepared-bundle-projection-lifetime `
  --reject-prepared-bundle-clone `
  --reject-prepared-bundle-serialization `
  --reject-prepared-bundle-background-transfer `
  --verify-abi-word-count 16 `
  --verify-abi-size-bytes 64 `
  --verify-rust-wgsl-abi-parity `
  --verify-scratch-usage storage_copy_src `
  --verify-scratch-span-overflow-checked `
  --verify-scratch-no-commit `
  --verify-binding-slot-order lhs_rhs_output_params `
  --verify-binding-relative-offset-contract `
  --verify-canonical-shader-digest `
  --verify-canonical-entry-point `
  --verify-workgroup-geometry 16x16x1 `
  --verify-no-persistent-pipeline-cache `
  --verify-preparation-rollback-order `
  --verify-prepared-bundle-drop-fails-closed `
  --verify-dispatch-unreachable-from-preparation `
  --verify-readback-unreachable-from-preparation `
  --verify-parity-unreachable-from-preparation `
  --verify-output-commit-unreachable-from-preparation `
  --classify-d1r2-admission-eligibility `
  --require-no-runtime-preparation-invocation `
  --require-no-shadow-consumer-instance `
  --require-no-shadow-consumer-reservation `
  --require-no-shadow-consumer-activation `
  --require-no-admission-token-mint `
  --require-no-admission-token-consume `
  --require-no-runtime-limit-query `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-abi-param-buffer `
  --require-no-scratch-output `
  --require-no-binding-resource `
  --require-no-bind-group-layout `
  --require-no-bind-group `
  --require-no-shader-module `
  --require-no-pipeline-layout `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-compute-pass `
  --require-no-tensorcube-dispatch `
  --require-no-queue-submit `
  --require-no-readback `
  --require-no-parity-comparison `
  --require-no-shadow-output-commit `
  --require-no-downstream-output-commit `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-d1r1-admission-contract-unchanged `
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

## 19. PASS

Marker:

`PASS_ASH_TCU_K7N_D1R2_SCRATCH_AND_PIPELINE_ADMISSION_CONTRACT_PREPARATION_PATH_SEALED_NO_RUNTIME_PREPARATION_INVOCATION_NO_DISPATCH_NO_READBACK_NO_PARITY_NO_OUTPUT_COMMIT`

Verdict:

`projection_scoped_shadow_resource_preparation_contract_sealed_with_single_use_token_slot_reservation_runtime_limits_lexical_lhs_rhs_leases_snapshot_revalidation_consumer_activation_abi_params_scratch_bind_group_shader_and_pipeline_paths_bound_into_a_non_cloneable_prepared_dispatch_bundle_and_candidate_eligible_for_d1r3_single_shadow_dispatch_without_runtime_preparation_invocation_dispatch_readback_parity_output_commit_or_burn_authority_change`

Expected state:

```text
scratch_pipeline_admission_eligibility=eligible_for_d1r3_single_shadow_dispatch_contract
runtime_preparation_path=implemented_not_invoked
prepared_bundle_lifetime=projection_call
prepared_bundle_cloneable=false
persistent_pipeline_cache=false
runtime_preparation_invoked=false
token_minted=false
slot_reserved=false
consumer_activated=false
lhs_lease_acquired=false
rhs_lease_acquired=false
scratch_output_state=absent
pipeline_state=absent
dispatch_authorized=false
dispatch_performed=false
readback_performed=false
parity_performed=false
shadow_output_commit_authorized=false
output_authority=burn
runtime_output_changed=false
```

## 20. Non-Authorization

D1R2 PASS does not authorize audit-time preparation invocation, persistent token/slot/lease state, prepared-bundle persistence, cross-generation scratch reuse, persistent pipeline caching, command encoding, compute pass creation, Queue submission, TensorCube dispatch, readback, parity, output commit, ragged-tail execution, Registry registration, route-epoch change, promotion, performance claims, or production-readiness claims.

Only `ASH-TCU-K7N-D1R3_SINGLE_SHADOW_DISPATCH` is authorized next.
