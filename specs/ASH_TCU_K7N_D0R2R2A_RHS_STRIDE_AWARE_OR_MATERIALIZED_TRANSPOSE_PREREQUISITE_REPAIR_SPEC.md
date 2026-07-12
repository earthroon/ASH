# ASH-TCU-K7N-D0R2R2A SPEC

## RHS Stride-Aware or Materialized Transpose Prerequisite Repair

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR`
- Status target: `PASS_ASH_TCU_K7N_D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR_SPEC.md`
- Patch class: blocker-specific prerequisite repair
- Target blocker: `rhs_stride_aware_kernel_or_materialized_transpose_required`

D0R2R2A selects exactly one RHS access strategy. It must not enable both a stride-aware path and a materialized-transpose path, and it must not introduce runtime fallback between them.

## 2. Parent State

Required parent:

- `ASH-TCU-K7N-D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE`
- required status: `PASS_ASH_TCU_K7N_D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- required verdict: `lhs_and_rhs_physical_layout_evidence_closed_but_post_swap_rhs_is_a_confirmed_strided_transpose_view_requiring_stride_aware_kernel_or_materialized_transpose_without_runtime_dispatch`
- required compatibility: `blocked_rhs_strided_transpose`
- required execution: `d0r2r2-19e1fd4cffa5a85bb91b`

Required parent transition:

- cleared: `lhs_physical_layout_not_proven`
- cleared: `rhs_post_swap_physical_layout_not_contiguous`
- replacement blocker: `rhs_stride_aware_kernel_or_materialized_transpose_required`
- remaining blocker: `raw_buffer_lease_preconditions_incomplete`

D0R2R2A validates the current-tree D0R2R2 final seal, blocker transition, post-swap layout receipt, local manifest, and D0R2R1 WGPU authority. A parent ZIP is not required.

## 3. Confirmed Layout

D0R2R2 established:

- LHS logical shape `[M,K]`, physical stride `[K,1]`;
- stored atlas weight logical shape `[N,K]`, physical stride `[K,1]`;
- post-swap RHS logical shape `[K,N]`, physical stride `[1,K]`;
- post-swap RHS shares storage with the stored atlas weight;
- no physical transpose materialization was observed.

The current RHS is therefore a confirmed strided transpose view, not a contiguous `[K,N]` buffer.

## 4. Selected Strategy

D0R2R2A selects:

`stride_aware_view`

Rejected alternative:

`model_lifetime_materialized_transpose`

Selection reason:

- the source `[N,K]` atlas remains the single weight storage;
- the proven post-swap access can be represented with explicit element strides;
- no duplicate model-lifetime GPU weight storage is required;
- no source/transpose epoch synchronization SSOT is added;
- no model-load transpose materialization is needed;
- per-token transpose remains forbidden.

The materialized alternative remains documented as a non-selected contract only.

## 5. Strategy SSOT

The single SSOT is `VocabAtlasRhsAccessStrategyContract`.

It contains:

- schema version;
- operation family;
- source callsite ID;
- selected decision;
- single-strategy seal;
- stride-aware contract;
- rejected materialized alternative;
- local route variant;
- blocker transition.

Required schema:

`ash_tcu_vocab_atlas_rhs_access_strategy_contract_v1`

Required operation:

`vocab_atlas_tile_projection`

Required callsite:

`call-66cc14a91d31bf8452215b67`

Required single-strategy seal:

- `selected_strategy=stride_aware_view`
- `stride_aware_enabled=true`
- `materialized_enabled=false`
- `runtime_fallback_allowed=false`

## 6. Stride-Aware RHS Contract

Logical RHS:

`[K,N]`

Physical element strides:

`[1,K]`

Required fields:

- `rhs_offset_elements`
- `rhs_k_stride_elements=1`
- `rhs_n_stride_elements=K`
- `element_size_bytes=4`
- `same_storage_as_stored_weight=true`
- `materialization_required=false`

All strides are measured in elements. Byte conversion is performed only after the checked element index is calculated.

## 7. Index Identity

Logical RHS element:

`rhs[k,n]`

Physical element index:

`rhs_offset_elements + k * rhs_k_stride_elements + n * rhs_n_stride_elements`

Under this contract:

`rhs_offset_elements + k + n*K`

The required identity is:

`rhs[k,n] == stored_rhs[n,k]`

The implementation must prove the identity with checked arithmetic and representative fixtures, including:

- `K=1`;
- `N=1`;
- full tile;
- a nonzero offset;
- a large hidden-size fixture;
- an overflow rejection case.

A contiguous `[K,N]` formula such as `k*N+n` is forbidden for the selected route.

## 8. Bounds Contract

Required maximum index:

`rhs_offset + (K-1)*1 + (N-1)*K`

Required element span:

`max_index + 1`

Required byte span:

`required_span_elements * 4`

All multiplication and addition must use checked arithmetic. The contract must reject:

- zero dimensions;
- element-index overflow;
- byte-span overflow;
- required span larger than the storage length.

Concrete buffer length and binding alignment are deferred to D0R2R3 because D0R2R2A does not lease a raw buffer.

## 9. Scalar ABI

The Rust/WGSL scalar ABI contains sixteen `u32` words in this exact order:

1. `m`
2. `n`
3. `k`
4. `lhs_offset_elements`
5. `lhs_row_stride_elements`
6. `rhs_offset_elements`
7. `rhs_k_stride_elements`
8. `rhs_n_stride_elements`
9. `output_offset_elements`
10. `output_row_stride_elements`
11. `tile_token_start`
12. `tile_token_len`
13. `tail_class`
14. `reserved0`
15. `reserved1`
16. `reserved2`

Required ABI size:

`64 bytes`

The ABI may contain only scalar values. It must not contain Device, Queue, Buffer, pointers, or HAL objects.

Required values for the selected route:

- `lhs_row_stride_elements=K`
- `rhs_k_stride_elements=1`
- `rhs_n_stride_elements=K`
- `output_row_stride_elements=N`
- reserved fields are zero.

The audit must verify Rust/WGSL field-order parity and the RHS index formula.

## 10. Tail Policy

`N=tile.token_len` remains runtime tile metadata.

Full tile:

- stride-aware contract may proceed to raw-lease prerequisite audit.

Ragged final tile:

- Burn remains authoritative;
- TensorCube dispatch is forbidden;
- the ABI may represent the dimensions, but no ragged TensorCube eligibility is granted.

D0R2R2A does not introduce padding, masking, or a dedicated tail kernel.

## 11. Route Variant

Base route family:

`ash_tcu_vocab_atlas_tile_projection_f32_shadow_family_v1`

Selected local variant:

`ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`

Variant semantics:

- LHS `[M,K]`, contiguous row-major;
- stored RHS `[N,K]`, contiguous row-major;
- logical RHS `[K,N]`;
- physical RHS stride `[1,K]`;
- expected output `[M,N]`;
- full tile only;
- Burn output authoritative;
- execution state not bound.

The variant is local contract metadata only. D0R2R2A must not register it in Registry v4 or change route epoch.

## 12. Materialized Alternative

The rejected alternative contract records:

- source shape `[N,K]`;
- materialized shape `[K,N]`;
- materialized stride `[N,1]`;
- different storage required;
- owner `NativeVocabAtlas`;
- model-lifetime ownership;
- creation at model load or atlas construction;
- same runtime Device;
- synchronized source and transpose epochs;
- per-token materialization count zero.

The alternative is not selected and no transpose buffer is created.

## 13. Blocker Transition

Clear:

`rhs_stride_aware_kernel_or_materialized_transpose_required`

Remaining:

`raw_buffer_lease_preconditions_incomplete`

New blocker:

none

The cleared strategy blocker means that indexing, ABI, bounds formulas, and route identity are closed. It does not mean that a raw WGPU buffer has been leased or that alignment and usage flags are already proven.

## 14. Required Implementation

Backend:

- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_rhs_access_strategy.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_stride_aware_rhs_contract.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_materialized_rhs_contract.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_rhs_index_contract.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_rhs_abi.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_route_variant.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_contract_audit.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2r2a_verdict.rs`
- `crates/burn_webgpu_backend/src/shaders/tensorcube_k7n_vocab_atlas_rhs_stride_contract.wgsl`

Model core:

- `crates/model_core/src/vocab_atlas_rhs_access_strategy_contract.rs`

Orchestrator:

- `crates/orchestrator_local/src/ash_tcu_k7n_d0r2r2a_rhs_strategy_repair_report.rs`
- `crates/orchestrator_local/src/bin/ash_tcu_k7n_d0r2r2a_rhs_stride_aware_or_materialized_transpose_prerequisite_repair_audit.rs`

Focused tests must cover index identity, bounds, ABI, single-strategy seal, route variant, materialized alternative, audit bundle, and model integration.

## 15. Zero-Execution Requirements

All of the following must remain zero:

- raw-buffer reference export;
- raw-buffer lease;
- tensor storage copy;
- transpose materialization;
- pipeline creation;
- command-encoder creation;
- queue submit;
- TensorCube dispatch and output;
- parity comparison;
- downstream output commit;
- route mutation;
- runtime output change;
- model-weight mutation;
- runtime Device creation.

## 16. Protected State

Protect before and after:

- Registry v4;
- route slots and epoch;
- R1F final seal;
- D0R2R1 WGPU authority;
- D0R2R2 final seal, manifest, blocker transition, and post-swap layout;
- canonical K6P source;
- vocab-atlas Burn projection semantics;
- model weights.

The following Burn expression must remain authoritative:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

D0R2R2A does not replace that expression with a TensorCube call.

## 17. Runtime Artifacts

The source bake must not include D0R2R2A runtime artifacts, receipts, local manifests, specs, docs, or SHA sidecars.

The audit binary writes an immutable bundle under:

`artifacts/tensorcube/k7n_d0r2r2a/<execution_id>/`

and latest mirrors under:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r2r2a_*_latest.json`

Required artifact families:

- prior D0R2R2 receipt;
- strategy decision;
- single-strategy seal;
- stride-aware contract;
- materialized alternative;
- RHS index proof;
- RHS storage bounds;
- Rust/WGSL ABI parity;
- route variant;
- blocker transition;
- protected-state guard;
- static checks;
- report;
- final seal;
- verdict;
- local manifest.

## 18. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r2r2a_rhs_stride_aware_or_materialized_transpose_prerequisite_repair_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r2r2-pass `
  --require-blocked-rhs-strided-transpose `
  --require-blocker rhs_stride_aware_kernel_or_materialized_transpose_required `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --target-vocab-atlas-projection-boundary `
  --evaluate-stride-aware-rhs-first `
  --bind-rhs-stride-unit-elements `
  --bind-rhs-k-stride 1 `
  --bind-rhs-n-stride-from-hidden-size `
  --verify-rhs-index-identity `
  --verify-rhs-storage-span-bounds `
  --verify-rhs-abi-u32-range `
  --verify-rust-wgsl-abi-parity `
  --verify-full-tile-stride-contract `
  --require-ragged-tail-burn-only `
  --bind-single-rhs-strategy `
  --bind-rhs-route-variant `
  --reject-runtime-strategy-fallback `
  --classify-materialized-transpose-alternative `
  --emit-exact-blocker-transition `
  --require-no-raw-buffer-reference-export `
  --require-no-raw-buffer-lease `
  --require-no-tensor-copy `
  --require-no-transpose-materialization `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-tensorcube-dispatch `
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

## 19. PASS Conditions

- D0R2R2 parent status, verdict, compatibility, and blocker transition are valid;
- WGPU authority remains unchanged;
- selected strategy is exactly `stride_aware_view`;
- runtime fallback is false;
- physical RHS stride is `[1,K]` in element units;
- CPU reference index identity passes;
- checked bounds formulas pass;
- ABI values fit `u32` for accepted fixtures;
- Rust and WGSL field order match;
- full-tile contract is valid;
- ragged tail remains Burn-only;
- local route variant is bound only in the contract namespace;
- raw lease, dispatch, output change, route mutation, and model-weight mutation remain zero.

## 20. Final Status and Verdict

Required status:

`PASS_ASH_TCU_K7N_D0R2R2A_RHS_STRIDE_AWARE_OR_MATERIALIZED_TRANSPOSE_PREREQUISITE_REPAIR_NO_RAW_LEASE_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`

Required verdict:

`rhs_stride_aware_view_strategy_selected_and_index_abi_bounds_route_contract_closed_without_raw_buffer_lease_tensorcube_dispatch_or_output_change`

Expected output fields:

- `selected_strategy=stride_aware_view`
- `route_variant=ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1`
- `cleared_blockers=rhs_stride_aware_kernel_or_materialized_transpose_required`
- `remaining_blockers=raw_buffer_lease_preconditions_incomplete`

## 21. Explicit Non-Authorization

D0R2R2A PASS does not authorize:

- raw WGPU Buffer export;
- raw-buffer lease;
- storage-buffer binding;
- pipeline creation;
- command encoder creation;
- TensorCube dispatch;
- parity comparison;
- ragged-tail TensorCube execution;
- Registry route registration;
- route epoch change;
- Burn output replacement;
- performance claim;
- D1 consumer binding.

## 22. Next State

After PASS, only the following patch is authorized:

`ASH-TCU-K7N-D0R2R3_RAW_BUFFER_LEASE_PRECONDITION_CLOSURE`

D0R2R3 must consume:

- `selected_strategy=stride_aware_view`;
- logical RHS `[K,N]`;
- physical RHS stride `[1,K]`;
- original stored atlas `[N,K]` buffer;
- the D0R2R2A scalar ABI;
- the D0R2R2A route variant;
- the remaining blocker `raw_buffer_lease_preconditions_incomplete`.
