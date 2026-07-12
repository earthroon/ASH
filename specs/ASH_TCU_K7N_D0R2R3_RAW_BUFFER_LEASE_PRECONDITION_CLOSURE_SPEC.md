# ASH-TCU-K7N-D0R2R3 SPEC

## Raw Buffer Lease Precondition Closure

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE`
- Status target: `PASS_ASH_TCU_K7N_D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE_SPEC.md`
- Patch class: blocker-specific prerequisite closure
- Target blocker: `raw_buffer_lease_preconditions_incomplete`

D0R2R3 proves whether future read-only raw-buffer leases can be admitted safely. It does not create a lease, export a Buffer, create bindings, build a pipeline, dispatch TensorCube, compare outputs, or replace Burn output.

## 2. Parent State

Required parent:

- `ASH-TCU-K7N-D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR`
- required status: `PASS_ASH_TCU_K7N_D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- required verdict: `rhs_stride_aware_view_strategy_selected_and_index_abi_bounds_route_contract_closed_without_raw_buffer_lease_tensorcube_dispatch_or_output_change`
- required execution: `d0r2r2a-7bf8a16edcfc2df9f15e`
- selected strategy: `stride_aware_view`
- route variant: `ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`
- cleared blocker: `rhs_stride_aware_kernel_or_materialized_transpose_required`
- remaining blocker: `raw_buffer_lease_preconditions_incomplete`

Required parent manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r2r2a_local_manifest_latest.json`

The current-tree D0R2R2A final seal, blocker transition, single-strategy seal, route variant, Rust/WGSL ABI receipt, D0R2R2 layout receipts, and D0R2R1 runtime WGPU authority are the parent SSOT.

## 3. Confirmed Input Contracts

### LHS

- logical shape: `[M,K]`
- current projection: `M=1`
- physical strides: `[K,1]`
- dtype: `f32`
- absolute storage offset: source-proven, nonzero allowed
- logical span: `M*K` elements
- classification: contiguous row-major span

### RHS

- stored shape: `[N,K]`
- logical TensorCube shape: `[K,N]`
- stored strides: `[K,1]`
- logical RHS strides: `[1,K]`
- dtype: `f32`
- absolute storage offset: `0`
- same source storage: `true`
- materialized transpose: `false`

RHS identity:

```text
rhs[k,n] == stored_rhs[n,k]
```

Physical RHS index:

```text
rhs_absolute_offset
+ k * rhs_k_stride_elements
+ n * rhs_n_stride_elements
```

Current values:

```text
rhs_k_stride_elements=1
rhs_n_stride_elements=K
```

## 4. Purpose

D0R2R3 closes:

1. one authoritative WGPU 26 Device/Queue/Buffer family;
2. exact input owner classification;
3. read-only `STORAGE` binding requirements;
4. aligned binding-base calculation;
5. binding-relative ABI offsets;
6. storage-span and device-limit bounds;
7. projection-call-only lexical lifetime;
8. generation-step and route-snapshot escape rejection;
9. deterministic invalidation requirements;
10. exact blocker transition to candidate re-audit.

Unknown evidence must never be promoted silently.

## 5. Governing Rules

### 5.1 Buffer Handle Is Not Ownership

A cloned WGPU Buffer handle must not be interpreted as transferred ownership or an extended lease. Burn tensor storage and native vocab-atlas storage remain authoritative.

### 5.2 Tensor Offset Is Not Binding Offset

The contract separates:

- absolute logical start;
- aligned binding base;
- binding-relative byte offset;
- binding-relative element offset.

A tensor storage offset is not automatically a legal WGPU binding offset.

### 5.3 Usage Must Be Proven

Each future input binding requires `STORAGE` usage and a read-only storage binding contract. Mapping and copy usages are neither required nor authorized.

### 5.4 Lease Scope Is Lexical

A future lease may not escape the projection call, generation step, route snapshot, background task, or owner lifetime.

### 5.5 No Actual Lease

D0R2R3 may add only pure-data descriptors and type-level future boundaries. It must not construct `RawWgpuBufferLease`, `BindingResource`, bind groups, or pipelines.

## 6. Runtime WGPU Authority

Required authority:

```text
authority_id=ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1
package=wgpu
version=26.0.1
alias=wgpu26
```

Required concrete family:

- `RuntimeWgpuDevice`
- `RuntimeWgpuQueue`
- `RuntimeWgpuBuffer`

Required relation:

```text
lhs_buffer_device_authority
== rhs_buffer_device_authority
== native_runtime_device_authority
== future_tensorcube_device_authority
```

Queue relation:

```text
native_runtime_queue_authority
== future_tensorcube_queue_authority
```

No new Device or Queue may be created.

## 7. Lease Precondition SSOT

Authoritative type:

```rust
pub struct VocabAtlasRawBufferLeasePreconditionContract {
    pub schema_version: String,
    pub operation_family: String,
    pub source_callsite_id: String,
    pub selected_rhs_strategy: String,
    pub route_variant: String,
    pub runtime_authority: RawBufferRuntimeAuthorityEvidence,
    pub lhs: RawBufferInputLeasePrecondition,
    pub rhs: RawBufferInputLeasePrecondition,
    pub lifetime: RawBufferLeaseLifetimeContract,
    pub invalidation: RawBufferLeaseInvalidationContract,
    pub compatibility: RawBufferLeasePreconditionCompatibility,
    pub cleared_blockers: Vec<String>,
    pub remaining_blockers: Vec<String>,
    pub runtime_limit_recheck_required_at_actual_lease_admission: bool,
}
```

Required schema:

`ash_tcu_vocab_atlas_raw_buffer_lease_precondition_contract_v1`

Required operation:

`vocab_atlas_tile_projection`

Required callsite:

`call-66cc14a91d31bf8452215b67`

This contract is the only SSOT for lease preconditions. Future bridge, candidate audit, and D1 shadow-consumer work must consume it rather than reconstruct independent facts.

## 8. Per-Input Contract

```rust
pub struct RawBufferInputLeasePrecondition {
    pub role: RawBufferInputRole,
    pub logical_shape_formula: [String; 2],
    pub physical_strides_formula: [String; 2],
    pub absolute_storage_offset_elements: u64,
    pub element_size_bytes: u64,
    pub storage_length_bytes: u64,
    pub logical_required_span_elements: u64,
    pub logical_required_span_bytes: u64,
    pub binding_window: RawBufferBindingWindow,
    pub buffer_usage: RawBufferUsageEvidence,
    pub device_relation: RawBufferDeviceRelation,
    pub owner: RawBufferOwnerEvidence,
    pub same_storage_relation_preserved: bool,
    pub materialized_transpose_present: bool,
    pub eligible: bool,
    pub blocker: Option<String>,
}
```

Input roles:

- `LhsLastHidden`
- `RhsStoredVocabAtlasTile`

## 9. Aligned Binding Window

```rust
pub struct RawBufferBindingWindow {
    pub absolute_logical_start_bytes: u64,
    pub absolute_logical_end_bytes_exclusive: u64,
    pub binding_base_bytes: u64,
    pub binding_size_bytes: u64,
    pub binding_relative_offset_bytes: u64,
    pub binding_relative_offset_elements: u64,
    pub min_storage_buffer_offset_alignment: u64,
    pub max_storage_buffer_binding_size: u64,
    pub alignment_proven: bool,
    pub bounds_proven: bool,
}
```

Binding base:

```text
binding_base_bytes
= floor(absolute_logical_start_bytes / alignment) * alignment
```

Required alignment:

```text
binding_base_bytes % alignment == 0
```

Relative offset:

```text
binding_relative_offset_bytes
= absolute_logical_start_bytes - binding_base_bytes
```

Element conversion:

```text
binding_relative_offset_elements
= binding_relative_offset_bytes / element_size_bytes
```

Required divisibility:

```text
binding_relative_offset_bytes % element_size_bytes == 0
```

Binding size:

```text
binding_size_bytes
= absolute_logical_end_bytes_exclusive - binding_base_bytes
```

Required bounds:

```text
binding_base_bytes + binding_size_bytes <= storage_length_bytes
binding_size_bytes <= max_storage_buffer_binding_size
binding_size_bytes > 0
```

D0R2R2A ABI offset semantics are sealed as binding-relative element offsets, not storage-absolute offsets.

## 10. Device-Limit Handling

D0R2R3 validates arithmetic and type contracts against conservative representative fixtures. It must not claim that fixture values are the active adapter's hardware limits.

The future actual lease admission must query the authoritative runtime Device and revalidate:

- `min_storage_buffer_offset_alignment`;
- `max_storage_buffer_binding_size`;
- `max_storage_buffers_per_shader_stage`.

Required contract field:

```text
runtime_limit_recheck_required_at_actual_lease_admission=true
```

This prevents source defaults from becoming hidden hardware claims.

## 11. LHS Preconditions

Required LHS:

```text
shape=[M,K]
stride=[K,1]
dtype=f32
element_size_bytes=4
current M=1
```

Absolute logical start:

```text
lhs_absolute_start_elements
= source-proven last-hidden row offset
```

Logical span:

```text
lhs_logical_span_elements=M*K
```

Required checks:

- offset known;
- checked arithmetic;
- span within storage;
- aligned binding base;
- element-aligned relative offset;
- binding size within runtime-limit contract;
- `STORAGE` usage;
- same runtime Device authority;
- owner outlives projection call;
- no contiguous copy.

## 12. RHS Preconditions

Required RHS:

```text
stored shape=[N,K]
stored stride=[K,1]
logical shape=[K,N]
logical stride=[1,K]
dtype=f32
element_size_bytes=4
absolute offset=0
```

Required span:

```text
(K-1)*1 + (N-1)*K + 1 == N*K
```

Required checks:

- checked `N*K` arithmetic;
- span within source atlas storage;
- `STORAGE` usage;
- read-only storage binding;
- same runtime Device authority;
- same source-storage relation;
- no materialized transpose;
- strategy remains `stride_aware_view`;
- full-tile candidate only;
- ragged tail remains Burn-authoritative.

## 13. Usage and Binding Type

```rust
pub struct RawBufferUsageEvidence {
    pub storage_usage_present: bool,
    pub copy_src_present: bool,
    pub copy_dst_present: bool,
    pub map_read_present: bool,
    pub map_write_present: bool,
    pub binding_type: RawBufferBindingTypeEvidence,
    pub metadata_only_inspection: bool,
}
```

Required binding type:

`storage_read_only`

`StorageReadWrite`, mapped access, and host-upload fallback are not authorized.

## 14. Ownership

Owner mapping:

```text
LHS -> BurnTensorStorage
RHS -> NativeVocabAtlasStorage
```

Required properties:

- owner outlives projection call;
- owner remains authoritative;
- TensorCube does not receive ownership;
- Buffer-handle clone does not extend lease scope;
- no Buffer handle is stored in route state.

## 15. Lifetime Contract

```rust
pub struct RawBufferLeaseLifetimeContract {
    pub maximum_lease_scope: RawBufferLeaseScope,
    pub may_escape_projection_call: bool,
    pub may_escape_generation_step: bool,
    pub may_be_stored_in_route_snapshot: bool,
    pub may_be_sent_to_background_task: bool,
    pub cloneable: bool,
    pub static_lifetime_allowed: bool,
}
```

Required values:

```text
maximum_lease_scope=projection_call
may_escape_projection_call=false
may_escape_generation_step=false
may_be_stored_in_route_snapshot=false
may_be_sent_to_background_task=false
cloneable=false
static_lifetime_allowed=false
```

## 16. Invalidation Contract

Required invalidation:

- projection return;
- generation-step end;
- tensor drop;
- atlas replacement;
- device loss;
- route epoch change.

Required stale policy:

```text
stale_lease_reuse_allowed=false
```

## 17. Compatibility

```rust
pub enum RawBufferLeasePreconditionCompatibility {
    EligibleForCandidateReaudit,
    BlockedRuntimeAuthority,
    BlockedBufferIdentity,
    BlockedUsageFlags,
    BlockedReadOnlyBinding,
    BlockedAlignment,
    BlockedStorageBounds,
    BlockedDeviceLimits,
    BlockedOwnerLifetime,
    BlockedGenerationEscape,
    BlockedInvalidation,
    BlockedMultiple,
}
```

Required PASS compatibility:

`eligible_for_candidate_reaudit`

This does not authorize an actual lease. It authorizes the D0R2 candidate re-audit.

## 18. Blocker Transition

PASS transition:

```text
cleared_blocker=raw_buffer_lease_preconditions_incomplete
remaining_blockers=none
compatibility=eligible_for_candidate_reaudit
```

Invalid or unknown evidence must emit an exact blocker, including:

- `lhs_buffer_storage_usage_missing`
- `rhs_buffer_storage_usage_missing`
- `runtime_buffer_device_authority_mismatch`
- `lhs_binding_window_alignment_invalid`
- `lhs_binding_size_exceeds_device_limit`
- `rhs_binding_size_exceeds_device_limit`
- `raw_buffer_owner_lifetime_unproven`
- `raw_buffer_lease_generation_escape_possible`
- `raw_buffer_lease_invalidation_contract_incomplete`

## 19. Implementation Files

Backend:

- `raw_buffer_runtime_authority_evidence.rs`
- `raw_buffer_usage_evidence.rs`
- `raw_buffer_binding_window.rs`
- `raw_buffer_owner_evidence.rs`
- `raw_buffer_lease_lifetime_contract.rs`
- `raw_buffer_lease_invalidation_contract.rs`
- `tensorcube_k7n_d0r2r3_raw_buffer_lease_precondition_contract.rs`
- `tensorcube_k7n_d0r2r3_contract_audit.rs`
- `tensorcube_k7n_d0r2r3_verdict.rs`

Model Core:

- `vocab_atlas_raw_buffer_lease_precondition_contract.rs`

Orchestrator:

- `ash_tcu_k7n_d0r2r3_raw_buffer_lease_precondition_closure_report.rs`
- `ash_tcu_k7n_d0r2r3_raw_buffer_lease_precondition_closure_audit.rs`

The audit binary path-binds the D0R2R3 contract modules directly so compile correctness does not depend on crate-root export overlay order.

## 20. Focused Tests

Tests cover:

1. aligned binding base;
2. relative-offset separation;
3. element alignment;
4. storage usage;
5. runtime authority;
6. owner lifetime;
7. generation-escape rejection;
8. invalidation completeness;
9. LHS preconditions;
10. RHS stride-aware source storage;
11. model-core integration.

## 21. Static Prohibitions

Forbidden on the D0R2R3 execution surface:

- actual raw-lease construction;
- Buffer export or ownership transfer;
- binding-resource creation;
- bind-group creation;
- pipeline-layout creation;
- compute-pipeline creation;
- command-encoder creation;
- queue submission;
- TensorCube dispatch;
- output-buffer creation;
- mapping;
- host upload;
- unsafe raw conversion;
- route commit;
- route epoch advancement.

## 22. Zero-Execution Counters

All must remain zero:

- raw-buffer reference export;
- raw-buffer lease;
- Buffer-handle clone for lease;
- binding resource;
- bind-group layout;
- bind group;
- pipeline layout;
- compute pipeline;
- command encoder;
- queue submit;
- TensorCube dispatch and output;
- output buffer;
- parity comparison;
- downstream output commit;
- route mutation and epoch change;
- runtime output change;
- model-weight mutation;
- new runtime Device and Queue.

## 23. Protected State

Hash before and after:

- Registry v4;
- R1F final seal;
- D0R2R1 runtime authority receipt;
- D0R2R2A final seal and manifest;
- D0R2R2A blocker transition;
- D0R2R2A strategy seal;
- D0R2R2A route variant;
- D0R2R2A ABI receipt;
- K6P canonical source;
- runtime WGPU authority source;
- raw bridge source.

Preserve Burn projection expression:

```rust
tile.weight.clone().swap_dims(0, 1)
```

D0R2R3 must not replace the Burn matmul path.

## 24. Runtime Artifacts

The source ZIP contains no pre-generated D0R2R3 runtime artifacts.

Immutable bundle:

`artifacts/tensorcube/k7n_d0r2r3/<execution_id>/`

Latest mirrors include prior receipt, runtime authority, LHS/RHS preconditions, binding windows, usage flags, device limits, owner/lifetime evidence, generation-escape guard, invalidation contract, compatibility, blocker transition, protected-state guard, static checks, report, final seal, verdict, and local manifest.

Canonical digests exclude absolute paths, timestamps, process IDs, raw pointer values, process-local Buffer identities, hardware marketing names, and filesystem order.

## 25. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r2r3_raw_buffer_lease_precondition_closure_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r2r2a-pass `
  --require-selected-strategy stride_aware_view `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-blocker raw_buffer_lease_preconditions_incomplete `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --bind-runtime-wgpu-authority `
  --inspect-lhs-buffer-authority `
  --inspect-rhs-buffer-authority `
  --verify-lhs-rhs-same-runtime-device `
  --verify-runtime-queue-authority `
  --inspect-lhs-buffer-usage `
  --inspect-rhs-buffer-usage `
  --require-lhs-storage-usage `
  --require-rhs-storage-usage `
  --require-read-only-input-bindings `
  --inspect-storage-buffer-device-limits `
  --calculate-lhs-aligned-binding-window `
  --calculate-rhs-aligned-binding-window `
  --bind-abi-offsets-as-binding-relative-elements `
  --verify-lhs-binding-window-bounds `
  --verify-rhs-binding-window-bounds `
  --verify-binding-offset-alignment `
  --verify-binding-size-device-limits `
  --verify-lhs-owner-lifetime `
  --verify-rhs-owner-lifetime `
  --bind-projection-call-lease-scope `
  --reject-projection-call-escape `
  --reject-generation-step-escape `
  --reject-route-snapshot-lease-storage `
  --reject-background-task-transfer `
  --bind-lease-invalidation-contract `
  --verify-ragged-tail-burn-only `
  --classify-lease-precondition-compatibility `
  --emit-exact-blocker-transition `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-buffer-handle-clone-for-lease `
  --require-no-binding-resource `
  --require-no-bind-group `
  --require-no-pipeline-layout `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-tensorcube-dispatch `
  --require-no-output-buffer `
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

## 26. PASS Conditions

- D0R2R2A parent seal and execution identity validate;
- selected strategy and route variant validate;
- one runtime WGPU authority validates;
- LHS/RHS usage contracts are read-only storage;
- aligned binding windows validate;
- ABI offsets are binding-relative elements;
- spans are in bounds;
- runtime Device limits must be rechecked at actual lease admission;
- owners remain authoritative;
- lease scope is projection-call only;
- no generation or route-state escape exists;
- invalidation contract is complete;
- all execution counters remain zero;
- protected state remains unchanged;
- Burn output remains authoritative.

## 27. Status and Verdict

Required marker:

`PASS_ASH_TCU_K7N_D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`

Required verdict:

`generation_scoped_read_only_lhs_rhs_raw_buffer_lease_preconditions_closed_with_aligned_binding_windows_binding_relative_offsets_runtime_authority_bounds_lifetime_and_invalidation_proven_without_raw_lease_tensorcube_dispatch_or_output_change`

Expected transition:

```text
cleared_blockers=raw_buffer_lease_preconditions_incomplete
remaining_blockers=
compatibility=eligible_for_candidate_reaudit
```

## 28. Explicit Non-Authorization

D0R2R3 PASS does not authorize:

- actual Buffer export;
- actual raw-buffer lease;
- Buffer-handle clone;
- bind group or layout;
- compute pipeline;
- command encoder;
- queue submit;
- TensorCube dispatch;
- output buffer;
- parity comparison;
- production route registration;
- route epoch change;
- Burn output replacement;
- D1 consumer binding;
- performance or production claims.

## 29. Next State

Only the following patch is authorized after PASS:

`ASH-TCU-K7N-D0R2R4_VOCAB_ATLAS_TILE_CANDIDATE_REAUDIT`

D0R2R4 must re-audit:

- original D0R2 candidate contract;
- all historical blockers;
- WGPU authority;
- physical layout;
- stride-aware RHS strategy;
- raw-buffer lease preconditions;
- zero-execution state.

D0R2R4 still must not create a lease or dispatch TensorCube.
