# ASH-TCU-K7N-D0R2R4 SPEC

## Vocab Atlas Tile Candidate Reaudit

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R2R4_VOCAB_ATLAS_TILE_CANDIDATE_REAUDIT`
- Status target: `PASS_ASH_TCU_K7N_D0R2R4_VOCAB_ATLAS_TILE_CANDIDATE_REAUDIT_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R2R4_VOCAB_ATLAS_TILE_CANDIDATE_REAUDIT_SPEC.md`
- Patch class: candidate eligibility reaudit

D0R2R4 does not add a new runtime path. It re-audits the original D0R2 vocab-atlas tile candidate against the evidence produced by D0R2R1, D0R2R2, D0R2R2A, and D0R2R3.

D0R2R4 must preserve the historical D0R2 `BlockedMultiple` result. It creates a separate current-state eligibility receipt and must not rewrite the original D0R2 receipt.

## 2. Direct Parent

Required direct parent:

`ASH-TCU-K7N-D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE`

Required parent state:

- status: `PASS_ASH_TCU_K7N_D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- verdict: `generation_scoped_read_only_lhs_rhs_raw_buffer_lease_preconditions_closed_with_aligned_binding_windows_binding_relative_offsets_runtime_authority_bounds_lifetime_and_invalidation_proven_without_raw_lease_tensorcube_dispatch_or_output_change`
- compatibility: `eligible_for_candidate_reaudit`
- execution ID: `d0r2r3-1f59d2cd4d39c52b8bb4`
- cleared blocker: `raw_buffer_lease_preconditions_incomplete`
- remaining blockers: none

Required parent manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r2r3_local_manifest_latest.json`

## 3. Original Candidate Identity

The candidate under reaudit is the original D0R2 operation:

- callsite: `call-66cc14a91d31bf8452215b67`
- source symbol: `NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`
- source file: `crates/model_core/src/native_wgpu.rs`
- operation family: `vocab_atlas_tile_projection`
- base route family: `ash_tcu_vocab_atlas_tile_projection_f32_shadow_family_v1`
- selected route variant: `ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`
- selected RHS strategy: `stride_aware_view`

Logical dimensions:

```text
M = last_hidden.dims()[0]
N = tile.token_len
K = self.spec.dimensions.hidden_size
```

Logical shapes:

```text
LHS            [M,K]
stored RHS     [N,K]
logical RHS    [K,N]
tile output    [M,N]
```

The current generation path requires `M=1`.

Input, accumulation, and output dtype remain `f32`.

## 4. Historical D0R2 State

Required original D0R2 execution:

`d0r2-14196acbf30d92b8b5f4`

Required original eligibility:

`blocked_multiple`

Required historical blockers:

1. `lhs_physical_layout_not_proven`
2. `rhs_post_swap_physical_layout_not_contiguous`
3. `raw_buffer_lease_preconditions_incomplete`
4. `wgpu_version_split`

The original final seal, manifest, and eligibility receipt must remain byte-identical before and after D0R2R4.

D0R2R4 must not represent the historical state as if the candidate had always been eligible.

## 5. Evidence Chain

Required ordered evidence chain:

```text
D0R2   original candidate contract and BlockedMultiple result
D0R2R1 WGPU runtime type-generation authority repair
D0R2R2 LHS/RHS physical-layout evidence closure
D0R2R2A single RHS strategy and Rust/WGSL ABI closure
D0R2R3 raw-buffer lease precondition closure
D0R2R4 candidate reaudit
```

Required execution lineage:

```text
D0R2   d0r2-14196acbf30d92b8b5f4
D0R2R1 d0r2r1-1d06b8ed23cd8fc281da
D0R2R2 d0r2r2-19e1fd4cffa5a85bb91b
D0R2R2A d0r2r2a-7bf8a16edcfc2df9f15e
D0R2R3 d0r2r3-1f59d2cd4d39c52b8bb4
```

Each evidence node must contain:

- patch ID
- execution ID
- status marker
- verdict
- final-seal SHA-256
- local-manifest SHA-256

The chain is invalid if a node is missing, substituted, duplicated, or reordered.

## 6. Evidence Lineage SSOT

Authoritative schema:

`ash_tcu_vocab_atlas_candidate_evidence_lineage_v1`

Authoritative types:

- `EvidenceNodeReference`
- `VocabAtlasCandidateEvidenceLineage`
- `CandidateBlockerLineageEntry`
- `CandidateBlockerSummary`
- `VocabAtlasTileCandidateReauditContract`

The lineage digest must exclude absolute paths, drive letters, timestamps, process IDs, host names, hardware marketing names, and filesystem discovery order.

## 7. Blocker Lineage

### 7.1 WGPU Generation

Original blocker:

`wgpu_version_split`

Closure authority:

- patch: `ASH-TCU-K7N-D0R2R1_WGPU_TYPE_GENERATION_SPLIT_PREREQUISITE_REPAIR`
- execution: `d0r2r1-1d06b8ed23cd8fc281da`
- authority ID: `ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`
- package generation: `wgpu-26.0.1`

Current state: `cleared`.

### 7.2 LHS Layout

Original blocker:

`lhs_physical_layout_not_proven`

Closure authority:

- patch: `ASH-TCU-K7N-D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE`
- execution: `d0r2r2-19e1fd4cffa5a85bb91b`

Required LHS evidence:

```text
logical shape      [M,K]
physical stride    [K,1]
dtype               f32
contiguous span     true
nonzero offset      allowed
```

Current state: `cleared`.

### 7.3 RHS Layout and Strategy

Original blocker:

`rhs_post_swap_physical_layout_not_contiguous`

D0R2R2 established:

```text
logical shape       [K,N]
physical stride     [1,K]
same storage        true
materialized        false
class               confirmed_strided_view
```

The ambiguous blocker was replaced with:

`rhs_stride_aware_kernel_or_materialized_transpose_required`

D0R2R2A then selected:

- strategy: `stride_aware_view`
- rejected alternative: `model_lifetime_materialized_transpose`
- route variant: `ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`
- index identity: `rhs[k,n] == stored_rhs[n,k]`
- physical index: `rhs_offset + k + n*K`

Both the ambiguous blocker and its exact replacement are currently closed.

### 7.4 Raw-Buffer Lease Preconditions

Original blocker:

`raw_buffer_lease_preconditions_incomplete`

Closure authority:

- patch: `ASH-TCU-K7N-D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE`
- execution: `d0r2r3-1f59d2cd4d39c52b8bb4`
- compatibility: `eligible_for_candidate_reaudit`

Required closed preconditions:

- same WGPU runtime Device authority
- same runtime Queue authority
- read-only `STORAGE` usage
- aligned binding windows
- binding-relative ABI offsets
- storage spans within bounds
- runtime device-limit recheck at actual lease admission
- projection-call lexical lifetime
- no generation-step escape
- no route-snapshot lease storage
- no background transfer
- complete invalidation contract

Current state: `cleared`.

## 8. Candidate Scope

Only a full vocab-atlas tile may be considered eligible.

Full tile:

```text
N == tile_vocab
```

Ragged tail:

```text
0 < N < tile_vocab
```

Required ragged-tail state:

- Burn-only
- TensorCube candidate: false
- candidate-closure authorization: false

The reaudit must not mix full-tile and ragged-tail receipts.

## 9. Candidate Reaudit Contract

Authoritative schema:

`ash_tcu_vocab_atlas_tile_candidate_reaudit_contract_v1`

Required historical state:

```text
d0r2_execution_id=d0r2-14196acbf30d92b8b5f4
eligibility=blocked_multiple
historical_blocker_count=4
```

Required current state:

```text
prerequisite_blockers=[]
selected_rhs_strategy=stride_aware_view
selected_route_variant=ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1
full_tile_eligible=true
ragged_tail_eligible=false
runtime_execution_authorized=false
output_authority=burn
execution_state=contract_only
```

Required current eligibility:

`eligible_for_d0r3_candidate_closure`

This eligibility does not authorize a raw lease, pipeline, dispatch, output, or parity comparison.

## 10. ABI Reaudit

D0R2R4 must revalidate the D0R2R2A ABI receipt.

Required ABI:

- 16 scalar `u32` fields
- 64 bytes total
- Rust/WGSL field-order parity
- RHS K stride: `1`
- RHS N stride: `K`
- LHS row stride: `K`
- offset unit: binding-relative elements

D0R2R4 does not allocate an output buffer.

## 11. Binding-Window Reaudit

Required distinction:

```text
absolute tensor storage offset
!=
WGPU binding base offset
```

Required evidence:

- aligned binding base
- binding-relative byte offset
- binding-relative element offset
- nonzero binding size
- binding window within storage
- actual lease admission requires runtime device-limit recheck

D0R2R4 does not inspect or bind a live WGPU Buffer.

## 12. Runtime Authority Reaudit

Required authority:

```text
authority_id=ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1
wgpu_generation=wgpu-26.0.1
```

Required relation:

```text
Burn tensor Device
== Native runtime Device
== future TensorCube Device authority
```

No new Device or Queue may be created.

## 13. Evidence Monotonicity

D0R2R4 must verify:

- D0R2R1 changes only WGPU authority evidence
- D0R2R2 adds layout evidence without changing WGPU authority
- D0R2R2A selects the RHS strategy without changing physical layout
- D0R2R3 adds lease preconditions without changing the selected strategy
- D0R2R4 performs classification only and changes no prerequisite contract

Forbidden drift:

- changed M/N/K meaning
- changed selected route variant
- changed RHS stride
- unexpected materialized transpose
- changed WGPU generation
- raw lease created in a prerequisite audit
- Burn output authority replaced

## 14. Zero-Execution Chain

All counters must remain zero:

```text
raw_buffer_reference_export_count
raw_buffer_lease_count
buffer_handle_clone_for_lease_count
binding_resource_creation_count
bind_group_layout_creation_count
bind_group_creation_count
pipeline_layout_creation_count
compute_pipeline_creation_count
command_encoder_creation_count
queue_submit_count
tensorcube_dispatch_count
tensorcube_output_count
output_buffer_creation_count
parity_comparison_count
tensor_storage_copy_count
transpose_materialization_count
route_mutation_count
route_epoch_change_count
registry_write_count
runtime_output_change_count
downstream_output_commit_count
model_weight_mutation_count
new_runtime_device_count
new_runtime_queue_count
```

Any nonzero counter denies candidate closure.

## 15. Protected State

Hash before and after:

- Registry v4
- route epoch and route receipts
- D0R2 original manifest, seal, and eligibility receipt
- D0R2R1 manifest, seal, blocker clearance, and WGPU authority
- D0R2R2 manifest, seal, layout receipts, and blocker transition
- D0R2R2A manifest, seal, strategy, route, ABI, and blocker transition
- D0R2R3 manifest, seal, input preconditions, compatibility, and blocker transition
- canonical K6P WGSL
- runtime WGPU authority source

Required protected-state differences: zero.

Required preserved Burn computation:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

Burn remains the only output authority.

## 16. Required Implementation

Backend:

- `tensorcube_k7n_d0r2r4_candidate_identity.rs`
- `tensorcube_k7n_d0r2r4_evidence_lineage.rs`
- `tensorcube_k7n_d0r2r4_blocker_lineage.rs`
- `tensorcube_k7n_d0r2r4_candidate_reaudit_contract.rs`
- `tensorcube_k7n_d0r2r4_contract_audit.rs`
- `tensorcube_k7n_d0r2r4_verdict.rs`

Model Core:

- `vocab_atlas_tile_candidate_reaudit_contract.rs`

Orchestrator:

- `ash_tcu_k7n_d0r2r4_vocab_atlas_tile_candidate_reaudit_report.rs`
- `ash_tcu_k7n_d0r2r4_vocab_atlas_tile_candidate_reaudit.rs`

The audit binary must path-bind D0R2R4 modules directly so compilation does not depend on crate-root overlay order.

## 17. Static Prohibitions

The D0R2R4 execution surface must not:

- create or export a raw WGPU Buffer lease
- create binding resources or bind groups
- create a pipeline layout or compute pipeline
- create a command encoder
- submit a Queue
- dispatch TensorCube
- create an output buffer
- map or copy a buffer
- materialize an RHS transpose
- mutate Registry v4
- advance route epoch
- change model weights
- replace Burn output

## 18. Runtime Artifacts

Source ZIP contains no pre-generated D0R2R4 runtime artifacts.

Immutable bundle:

`artifacts/tensorcube/k7n_d0r2r4/<execution_id>/`

Latest mirrors include:

- five prior receipt summaries
- candidate identity
- evidence lineage
- blocker lineage
- historical state
- current state
- tile scope
- route contract
- ABI reaudit
- binding-window reaudit
- runtime-authority reaudit
- zero-execution chain
- protected-state guard
- eligibility
- report
- final seal
- verdict
- local manifest

## 19. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r2r4_vocab_atlas_tile_candidate_reaudit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r2-original-blocked-multiple `
  --require-d0r2-execution d0r2-14196acbf30d92b8b5f4 `
  --require-d0r2r1-pass `
  --require-d0r2r1-execution d0r2r1-1d06b8ed23cd8fc281da `
  --require-d0r2r2-pass `
  --require-d0r2r2-execution d0r2r2-19e1fd4cffa5a85bb91b `
  --require-d0r2r2a-pass `
  --require-d0r2r2a-execution d0r2r2a-7bf8a16edcfc2df9f15e `
  --require-d0r2r3-pass `
  --require-d0r2r3-execution d0r2r3-1f59d2cd4d39c52b8bb4 `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --target-vocab-atlas-projection-boundary `
  --bind-original-candidate-identity `
  --rebuild-evidence-lineage `
  --verify-parent-child-receipt-chain `
  --verify-historical-d0r2-receipt-unchanged `
  --verify-wgpu-blocker-closure `
  --verify-lhs-layout-blocker-closure `
  --verify-rhs-layout-blocker-lineage `
  --verify-rhs-strategy-blocker-closure `
  --verify-raw-lease-blocker-closure `
  --require-no-current-prerequisite-blockers `
  --require-selected-strategy stride_aware_view `
  --require-route-variant ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --verify-rhs-index-identity `
  --verify-rust-wgsl-abi-receipt `
  --verify-binding-relative-offset-contract `
  --verify-raw-lease-precondition-receipt `
  --require-full-tile-candidate-only `
  --require-ragged-tail-burn-only `
  --verify-runtime-wgpu-authority `
  --verify-zero-execution-chain `
  --classify-candidate-eligibility `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-binding-resource `
  --require-no-bind-group `
  --require-no-pipeline-layout `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-tensorcube-dispatch `
  --require-no-output-buffer `
  --require-no-parity-comparison `
  --require-no-downstream-output-commit `
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

## 20. PASS Conditions

Historical state:

- D0R2 original receipt remains `blocked_multiple`
- all four historical blockers remain recorded
- original execution ID and digest are unchanged

Evidence lineage:

- all five prerequisite nodes validate
- execution IDs and SHA-256 values validate
- node order is canonical

Current candidate:

```text
current_prerequisite_blockers=[]
current_eligibility=eligible_for_d0r3_candidate_closure
selected_strategy=stride_aware_view
full_tile_candidate=true
ragged_tail_candidate=false
runtime_execution_authorized=false
output_authority=burn
```

Integrity:

- all execution counters remain zero
- protected state remains unchanged
- Burn projection remains authoritative

## 21. Status and Verdict

Required marker:

`PASS_ASH_TCU_K7N_D0R2R4_VOCAB_ATLAS_TILE_CANDIDATE_REAUDIT_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`

Required verdict:

`vocab_atlas_full_tile_candidate_reaudit_completed_with_all_d0r2_prerequisites_closed_evidence_lineage_valid_stride_aware_rhs_and_raw_lease_preconditions_proven_and_candidate_eligible_for_d0r3_closure_without_raw_lease_tensorcube_dispatch_or_output_change`

Expected output state:

```text
historical_eligibility=blocked_multiple
current_eligibility=eligible_for_d0r3_candidate_closure
current_prerequisite_blockers=
selected_strategy=stride_aware_view
full_tile_candidate=true
ragged_tail_candidate=false
runtime_execution_authorized=false
```

## 22. Explicit Non-Authorization

D0R2R4 PASS does not authorize:

- actual raw-buffer lease
- Buffer export
- bind-group creation
- pipeline creation
- command encoder creation
- Queue submission
- TensorCube dispatch
- output-buffer creation
- parity comparison
- ragged-tail TensorCube execution
- Registry route registration
- route epoch change
- Burn output replacement
- D1 consumer binding
- performance or production-readiness claims

## 23. Next State

Only the following patch is authorized after PASS:

`ASH-TCU-K7N-D0R3_VOCAB_ATLAS_TILE_CANDIDATE_CLOSURE_AUDIT`

D0R3 must close:

1. final candidate identity seal
2. input and future output binding contract
3. pipeline-layout candidate contract
4. workgroup and dispatch geometry contract
5. dispatch-independent CPU reference fixture
6. future parity receipt schema
7. rollback boundary
8. candidate admission and revocation rules

D0R3 still does not authorize production route registration.
