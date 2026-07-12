# ASH-TCU-K7N-D0R2R2 SPEC

## LHS / RHS Physical Layout Evidence Closure

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE`
- Status target: `PASS_ASH_TCU_K7N_D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE_SPEC.md`
- Patch class: blocker-specific prerequisite evidence closure

D0R2R2 closes physical-layout evidence. It does not insert a copy, materialize a transpose, lease a raw buffer, or dispatch TensorCube.

## 2. Parent State

Required parent:

- `ASH-TCU-K7N-D0R2R1_WGPU_TYPE_GENERATION_SPLIT_PREREQUISITE_REPAIR`
- required status: `PASS_ASH_TCU_K7N_D0R2R1_WGPU_TYPE_GENERATION_SPLIT_PREREQUISITE_REPAIR_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- required verdict: `runtime_wgpu_device_queue_and_buffer_type_generation_unified_under_burn_runtime_authority_and_non_authoritative_generations_quarantined_without_raw_buffer_lease_tensorcube_dispatch_or_output_change`
- required cleared blocker: `wgpu_version_split`
- required execution: `d0r2r1-1d06b8ed23cd8fc281da`

Required remaining blockers:

- `lhs_physical_layout_not_proven`
- `rhs_post_swap_physical_layout_not_contiguous`
- `raw_buffer_lease_preconditions_incomplete`

D0R2R2 validates the current-tree D0R2R1 final seal, blocker-clearance receipt, WGPU authority, and local manifest. A parent ZIP is not required.

## 3. Target Boundary

- source: `crates/model_core/src/native_wgpu.rs`
- symbol: `NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`
- callsite: `call-66cc14a91d31bf8452215b67`
- operation family: `vocab_atlas_tile_projection`

Existing Burn computation remains authoritative:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

## 4. Purpose

D0R2R2 must classify and seal:

1. LHS physical shape, strides, offset, span, and contiguity;
2. stored vocab-atlas tile weight physical layout;
3. clone storage semantics;
4. `swap_dims(0,1)` view versus materialization semantics;
5. post-swap RHS physical strides and contiguity;
6. exact blocker transition for the next prerequisite patch.

Logical shape is not accepted as physical-layout evidence. `swap_dims` is not accepted as materialization evidence.

## 5. Confirmed Shape Contract

- `M = last_hidden.dims()[0]`
- `N = tile.token_len`
- `K = self.spec.dimensions.hidden_size`
- LHS logical shape: `[M,K]`
- stored tile weight: `[N,K]`
- post-swap RHS logical shape: `[K,N]`
- tile output: `[M,N]`
- dtype and accumulation: `f32`

## 6. Source-Proven Layout Evidence

### 6.1 LHS

LHS is produced by:

```rust
hidden
    .slice([0..1, (seq_len - 1)..seq_len, 0..hidden_size])
    .reshape([1, hidden_size])
```

This selects the full hidden axis from exactly one row. The physical-layout formula is:

- shape: `[1,K]`
- strides: `[K,1]`
- offset: `(seq_len-1)*K`
- referenced span: `K` elements
- class: `confirmed_contiguous_non_zero_offset`

The nonzero offset remains a D0R2R3 alignment and bounds concern. It is not a physical-contiguity blocker.

### 6.2 Stored RHS

Each atlas tile is created by:

```rust
TensorData::new(tile_slice.to_vec(), [token_len, hidden_size])
```

The physical-layout formula is:

- shape: `[N,K]`
- strides: `[K,1]`
- offset: `0`
- referenced span: `N*K` elements
- class: `confirmed_contiguous_row_major`

### 6.3 Post-Swap RHS

The RHS expression is:

```rust
tile.weight.clone().swap_dims(0, 1)
```

The tensor clone is a handle/storage-sharing clone for this contract and must not be interpreted as a deep contiguous copy.

The post-swap physical-layout formula is:

- shape: `[K,N]`
- strides: `[1,K]`
- offset: `0`
- same underlying storage: `true`
- materialization observed: `false`
- class: `confirmed_strided_view`

A contiguous row-major `[K,N]` tensor would require strides `[N,1]`. Therefore post-swap RHS is not contiguous.

## 7. Physical Layout SSOT

Authoritative schema:

`ash_tcu_vocab_atlas_physical_layout_contract_v1`

Authoritative types:

- `TensorPhysicalLayoutEvidence`
- `TensorStorageIdentityRelation`
- `TensorViewTransformEvidence`
- `D0R2R2PhysicalLayoutAuditBundle`

The contract owns shape formulas, stride formulas, offset formulas, storage relation, contiguity, evidence source, compatibility, and blocker transition.

Reports and future raw-lease contracts consume this typed contract. They must not recreate independent layout facts.

## 8. Contiguity and Span Rules

Canonical row-major strides are calculated from the final dimension backward.

For dimensions `dims` and strides `strides`:

```text
required_span_elements
= offset + sum((dims[i]-1)*strides[i]) + 1
```

The implementation must reject:

- rank/stride-count mismatch;
- zero dimensions;
- arithmetic overflow;
- out-of-bounds spans;
- unsupported negative-stride representations;
- backend-opaque evidence promoted to contiguous.

Size-one dimensions may use canonical-equivalent strides, but that exception must be explicit.

## 9. Storage Identity

Storage identity is process-local audit evidence only.

Artifacts may record:

- `same_storage_as_input=true|false`
- `materialization_observed=true|false`

Artifacts must not record:

- raw pointer values;
- stable process-external storage identities;
- HAL handles;
- WGPU Buffer objects.

D0R2R2 exports no raw-buffer reference.

## 10. Scope

D0R2R2 may:

- add pure-data layout evidence types;
- calculate canonical strides and storage spans;
- bind source-proven LHS, stored-RHS, and post-swap-RHS formulas;
- classify clone and swap semantics;
- emit exact blocker transitions;
- write dedicated audit receipts and a final seal.

D0R2R2 must not:

- invoke `BurnToRawWgpuBridge`;
- create `RawWgpuBufferLease`;
- export `wgpu::Buffer`;
- create a contiguous copy;
- materialize a transpose;
- create a pipeline or command encoder;
- submit a queue;
- dispatch TensorCube;
- compare outputs;
- mutate weights, Registry v4, route slots, or epoch;
- change Burn output.

## 11. Compatibility Outcome

Required compatibility:

`blocked_rhs_strided_transpose`

D0R2R2 clears the ambiguous evidence blockers:

- `lhs_physical_layout_not_proven`
- `rhs_post_swap_physical_layout_not_contiguous`

It replaces the RHS blocker with the exact structural blocker:

`rhs_stride_aware_kernel_or_materialized_transpose_required`

Remaining blockers:

- `rhs_stride_aware_kernel_or_materialized_transpose_required`
- `raw_buffer_lease_preconditions_incomplete`

Clearing the old RHS blocker does not mean the RHS became contiguous. It means the physical layout is no longer unknown and has been proven to be strided.

## 12. Zero-Execution Counters

All of the following must remain zero:

- raw-buffer reference export;
- raw-buffer lease;
- tensor storage copy;
- new transpose materialization;
- TensorCube dispatch and output;
- parity comparison;
- queue submit;
- device poll;
- buffer map;
- pipeline and command-encoder creation;
- route mutation;
- downstream output commit;
- runtime output change;
- model-weight mutation.

## 13. Required Implementation

Backend:

- `crates/burn_webgpu_backend/src/tensor_storage_identity.rs`
- `crates/burn_webgpu_backend/src/tensor_physical_layout_evidence.rs`
- `crates/burn_webgpu_backend/src/tensor_layout_introspection.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2_contract_audit.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2_verdict.rs`

Model contract:

- `crates/model_core/src/vocab_atlas_projection_physical_layout_contract.rs`

Orchestrator:

- `crates/orchestrator_local/src/ash_tcu_k7n_d0r2r2_lhs_rhs_physical_layout_evidence_closure_report.rs`
- `crates/orchestrator_local/src/bin/ash_tcu_k7n_d0r2r2_lhs_rhs_physical_layout_evidence_closure_audit.rs`

Focused tests cover row-major calculation, storage span, storage relation, LHS layout, stored RHS, post-swap RHS, clone semantics, and model integration.

## 14. Protected State

Hash before and after:

- Registry v4;
- R1F final seal;
- D0R2R1 final seal and local manifest;
- D0R2R1 blocker-clearance receipt;
- runtime WGPU authority source;
- canonical K6P source.

The audit must also preserve semantic fingerprints for:

- LHS slice and reshape;
- tile `TensorData::new` constructor;
- `tile.weight.clone().swap_dims(0,1)`;
- merged-logits output construction.

## 15. Runtime Artifacts

The source bake contains no pre-generated D0R2R2 artifacts, receipts, manifests, or SHA sidecars.

The Rust audit binary writes:

- immutable bundle: `artifacts/tensorcube/k7n_d0r2r2/<execution_id>/`;
- latest mirrors: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r2r2_*_latest.json`;
- local manifest: `ash_tensorcube_k7n_d0r2r2_local_manifest_latest.json`.

Required receipt families include prior receipt, layout authority, LHS, stored RHS, post-swap RHS, clone semantics, storage relation, storage span, compatibility, blocker transition, protected-state guard, static checks, report, final seal, and verdict.

## 16. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r2r2_lhs_rhs_physical_layout_evidence_closure_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r2r1-pass `
  --require-wgpu-version-split-cleared `
  --require-blocker lhs_physical_layout_not_proven `
  --require-blocker rhs_post_swap_physical_layout_not_contiguous `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --target-vocab-atlas-projection-boundary `
  --bind-layout-introspection-authority `
  --inspect-lhs-rank-dims-strides-offset `
  --inspect-stored-rhs-rank-dims-strides-offset `
  --inspect-post-swap-rhs-rank-dims-strides-offset `
  --classify-lhs-contiguity `
  --classify-stored-rhs-contiguity `
  --classify-post-swap-rhs-contiguity `
  --resolve-clone-storage-semantics `
  --resolve-swap-view-or-materialization `
  --verify-storage-identity-relations `
  --verify-storage-span-bounds `
  --classify-physical-layout-compatibility `
  --emit-exact-blocker-transition `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-tensor-copy `
  --require-no-new-transpose-materialization `
  --require-no-tensorcube-dispatch `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-parity-comparison `
  --require-no-downstream-output-commit `
  --verify-runtime-wgpu-authority-unchanged `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
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

## 17. PASS Conditions

- D0R2R1 PASS and WGPU blocker clearance validate;
- LHS layout is source-proven contiguous with a possible nonzero offset;
- stored RHS is source-proven contiguous row-major `[N,K]`;
- post-swap RHS is source-proven `[K,N]` with strides `[1,K]`;
- clone shares storage and no materialization is claimed;
- ambiguous layout blockers are replaced with the exact stride/materialization blocker;
- all zero-execution counters remain zero;
- protected state remains unchanged;
- Burn output remains authoritative.

## 18. Final Verdict

Required verdict:

`lhs_and_rhs_physical_layout_evidence_closed_but_post_swap_rhs_is_a_confirmed_strided_transpose_view_requiring_stride_aware_kernel_or_materialized_transpose_without_runtime_dispatch`

Required marker:

`PASS_ASH_TCU_K7N_D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`

## 19. Explicit Non-Authorization

D0R2R2 PASS does not authorize:

- raw-buffer lease;
- contiguous copy or transpose materialization;
- stride-aware TensorCube execution;
- pipeline creation or dispatch;
- output allocation or parity comparison;
- route registration or epoch change;
- D0R3 candidate closure;
- D1 binding;
- performance or production claims.

## 20. Next State

Only the following patch is authorized:

`ASH-TCU-K7N-D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR`

D0R2R2A must select exactly one strategy:

- Option A: explicit RHS stride contract in the TensorCube kernel;
- Option B: model-lifetime same-device materialized `[K,N]` atlas.

The two strategies must not be introduced simultaneously.
