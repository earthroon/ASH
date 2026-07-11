# ASH-TCU-K7N-D0R2 SPEC

## Vocab-Atlas Tile Shape / Physical Layout / Ragged Tail / Route Identity Contract

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R2_VOCAB_ATLAS_TILE_SHAPE_LAYOUT_TAIL_ROUTE_IDENTITY_CONTRACT`
- Status target: `PASS_ASH_TCU_K7N_D0R2_VOCAB_ATLAS_TILE_SHAPE_LAYOUT_TAIL_ROUTE_IDENTITY_CONTRACT_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R2_VOCAB_ATLAS_TILE_SHAPE_LAYOUT_TAIL_ROUTE_IDENTITY_CONTRACT_SPEC.md`

## 2. Parent

Required parent:

- `ASH-TCU-K7N-D0R1_GENERATION_SCOPED_ROUTE_SNAPSHOT_SHADOW_OBSERVER_OWNER_SSOT`
- required status: `PASS_ASH_TCU_K7N_D0R1_GENERATION_SCOPED_ROUTE_SNAPSHOT_SHADOW_OBSERVER_OWNER_SSOT_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- required verdict: `generation_scoped_route_snapshot_route_read_shadow_parity_observer_and_no_dispatch_synchronization_owners_established_for_vocab_atlas_projection_without_tensorcube_execution_or_runtime_output_change`

D0R2 validates the current-tree D0R1 final seal and local manifest. A parent ZIP is not required.

## 3. Purpose

D0R2 closes the contract for the vocab-atlas tile projection candidate without executing TensorCube. It establishes:

1. an operation-specific route family identity;
2. M/N/K source evidence;
3. LHS, swapped RHS and expected output layout classifications;
4. full-tile versus ragged-tail policy;
5. f32 input, output and accumulation contract;
6. raw-buffer lease preconditions;
7. same-device identity requirements;
8. concrete WGPU type-generation compatibility;
9. an exact eligible or blocked verdict.

D0R2 does not bind a runtime consumer, lease a buffer, dispatch TensorCube, compare outputs, mutate Registry v4 or change model output.

## 4. Target Boundary

- source: `crates/model_core/src/native_wgpu.rs`
- symbol: `NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas`
- D0 callsite: `call-66cc14a91d31bf8452215b67`
- operation family: `vocab_atlas_tile_projection`

Existing Burn computation remains authoritative:

```rust
last_hidden
    .clone()
    .matmul(tile.weight.clone().swap_dims(0, 1))
```

Existing output construction remains authoritative:

```rust
Tensor::<NativeInferenceBackend, 2>::from_data(
    TensorData::new(merged_logits, [1, atlas.vocab_size]),
    &self.device,
)
```

## 5. Confirmed Shape Evidence

D0R2 binds:

- M expression: `last_hidden.dims()[0]`
- M evidence: `derived_from_tensor_shape`
- N expression: `tile.token_len`
- N evidence: `runtime_symbolic`
- K expression: `self.spec.dimensions.hidden_size`
- K evidence: `model_config_constant`

Semantic shapes:

- LHS: `[M,K]`
- stored tile weight: `[N,K]`
- matmul RHS after `swap_dims(0,1)`: `[K,N]`
- tile-local output: `[M,N]`
- merged Burn output: `[M,vocab_size]`

Required dtype contract:

- LHS: f32
- RHS: f32
- output: f32
- accumulation: f32

Required invariants:

```text
M > 0
N > 0
K > 0
last_hidden.dims()[1] == K
tile.weight.dims()[0] == N
tile.weight.dims()[1] == K
```

M=1 may be recorded as the normal one-token generation observation, but must not be treated as a universal constant. M>1 must be explicitly classified against the existing `[1, vocab_size]` return contract.

## 6. Route Family Identity

D0R2 declares the local contract-only identity:

`ash_tcu_vocab_atlas_tile_projection_f32_shadow_family_v1`

The identity means:

- operation: vocab-atlas tile projection;
- LHS: `[M,K]`;
- stored weight: `[N,K]`;
- matmul RHS: `[K,N]`;
- output: `[M,N]`;
- dtype and accumulation: f32;
- output authority: Burn;
- execution state: not bound;
- Registry registration state: local contract only.

The route family is not added to Registry v4 in D0R2.

The K6P identity `ash_tcu_k6p_row_major_emit_candidate_v1` must not be aliased to the vocab-atlas route. K6P may be used only as a comparator or capability reference.

The route identity digest must include semantic shape, dtype, transpose, tail, output authority, raw-lease class and WGPU compatibility class. It must exclude absolute paths, host/user names, timestamps, process IDs, adapter marketing names and filesystem order.

## 7. Tile Coverage Contract

The atlas constructor must prove:

- first `token_start == 0`;
- each next range begins at `previous.token_start + previous.token_len`;
- each `token_len > 0`;
- tile weight row count equals `token_len`;
- the sum of all `token_len` values equals `vocab_size`;
- overlap count is zero;
- gap count is zero.

The source constructor proof is:

```rust
let token_len = tile_vocab.min(vocab_size - token_start);
...
token_start += token_len;
```

Any gap, overlap, zero-length tile, hidden-size mismatch or incomplete vocabulary coverage is fail-closed.

## 8. Full Tile and Ragged Tail

Canonical tile capacity must come from `NativeVocabAtlas::tile_vocab` or another typed source. D0R2 must not invent a numeric tile capacity.

Classification:

- full tile: `token_len == tile_vocab`;
- ragged tail: `0 < token_len < tile_vocab`;
- invalid: zero values or `token_len > tile_vocab`.

D0R2 policy:

- full tiles may be evaluated for later shadow eligibility;
- ragged tails remain Burn-only;
- TensorCube ragged-tail dispatch is forbidden;
- padding is forbidden;
- masking is forbidden;
- silent zero-fill is forbidden.

Padding, masking or a dedicated tail kernel requires a separate patch.

## 9. LHS Layout Contract

LHS source is `last_hidden` with logical shape `[M,K]` and no logical transpose.

D0R2 must classify:

- physical strides;
- element offset;
- row-major contiguity;
- strided-view status;
- backend-opaque status;
- source or fixture evidence.

Allowed classes:

- `confirmed_contiguous_row_major`;
- `confirmed_strided_view`;
- `backend_opaque`;
- `unknown`.

Raw lease eligibility requires `confirmed_contiguous_row_major`. D0R2 must not insert a contiguous copy.

## 10. Stored Weight and RHS Layout Contract

Stored tile weight has semantic shape `[N,K]`.

After:

```rust
tile.weight.clone().swap_dims(0, 1)
```

the matmul RHS has logical shape `[K,N]`.

A logical transpose view is not proof of a physically materialized row-major transpose.

Allowed classifications:

- `logical_strided_transpose_view`;
- `materialized_contiguous_transpose`;
- `backend_opaque_transpose`;
- `unknown`.

A strided RHS is eligible only when the future TensorCube kernel has an explicit stride contract with bounds proof. A materialized RHS is eligible only when a model-lifetime same-device contiguous `[K,N]` buffer already exists and is source-confirmed. D0R2 must not materialize a transpose.

The assumption “`swap_dims` implies a physically contiguous `[K,N]` buffer” is forbidden.

## 11. Output Layout Contract

The future tile-local shadow output contract is:

- rank 2;
- shape `[M,N]`;
- f32;
- contiguous row-major;
- no downstream publication.

D0R2 does not allocate this output. The merged `[M,vocab_size]` output remains owned by Burn.

## 12. Raw-Buffer Lease Preconditions

D0R2 may inspect but must not invoke `BurnToRawWgpuBridge` or construct `RawWgpuBufferLease`.

Required classifications:

- bridge symbol presence;
- `NativeWgpuRuntimeHandles` presence;
- same-device identity;
- LHS and RHS STORAGE usage compatibility;
- offsets and alignment;
- size bounds;
- operation lifetime;
- output lifetime.

Symbol presence alone is not eligibility.

Allowed lease outcomes include:

- `eligible_by_contract_only_no_lease_executed`;
- blocked non-contiguous LHS;
- blocked RHS transpose layout;
- blocked usage flags;
- blocked alignment;
- blocked bounds;
- blocked lifetime;
- blocked device identity;
- blocked WGPU generation;
- insufficient evidence.

Required actual lease count: zero.

## 13. Device and Queue Identity

Required future identity:

```text
Burn tensor storage device
== NativeWgpuModel runtime handle device
== future TensorCube dispatch device
```

Required future queue identity:

```text
future TensorCube queue
== NativeWgpuModel runtime handle queue
```

Allowed verdicts:

- same device confirmed;
- same adapter but device identity unproven;
- different device;
- runtime handles unavailable;
- insufficient evidence.

Only same-device-confirmed may proceed to candidate closure.

## 14. WGPU Type-Generation Compatibility

D0R2 must capture concrete package versions and type ownership for:

- Burn backend Device, Queue and Buffer;
- bridge Device, Queue and Buffer;
- TensorCube Device, Queue and Buffer;
- relevant feature sets.

Allowed verdicts:

- `compatible_exact_generation`;
- `compatible_through_typed_adapter`;
- `feature_split`;
- `version_split`;
- `type_owner_split`;
- `unknown`.

A typed adapter is valid only when it is an explicit source module with safe conversion, ownership and lifetime proof, plus focused compile tests.

Forbidden bridges:

- `transmute`;
- raw pointer reinterpretation between WGPU generations;
- undocumented ABI assumptions;
- `ManuallyDrop` ABI bridges;
- `repr(C)` layout assumptions.

Only exact-generation compatibility or a proven typed adapter may proceed.

## 15. Contract Completion and Eligibility

D0R2 separates contract completion from execution eligibility.

Contract completion may PASS when all fields are classified and exact blockers are emitted, even when the candidate remains blocked.

Allowed eligibility values:

- eligible for candidate closure audit;
- blocked shape;
- blocked LHS layout;
- blocked RHS layout;
- blocked tail policy;
- blocked route identity;
- blocked raw lease precondition;
- blocked device identity;
- blocked WGPU compatibility;
- blocked multiple.

Unknown evidence must never be promoted to compatible.

## 16. Required Implementation

Backend:

- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_vocab_atlas_route_identity.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_vocab_atlas_shape_contract.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_vocab_atlas_layout_contract.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_vocab_atlas_tail_policy.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_raw_lease_preconditions.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_wgpu_compatibility.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_contract_audit.rs`
- `crates/burn_webgpu_backend/src/tensorcube_k7n_d0r2_verdict.rs`

Model contract:

- `crates/model_core/src/vocab_atlas_tile_projection_contract.rs`

Orchestrator:

- `crates/orchestrator_local/src/ash_tcu_k7n_d0r2_vocab_atlas_tile_shape_layout_tail_route_identity_report.rs`
- `crates/orchestrator_local/src/bin/ash_tcu_k7n_d0r2_vocab_atlas_tile_shape_layout_tail_route_identity_audit.rs`

Focused tests must cover route identity, shape, layout, tail, lease preconditions, WGPU split and model contract integration.

## 17. Static Guards

D0R2 implementation modules must not contain executable calls to:

```text
queue.submit
dispatch_workgroups
create_compute_pipeline
create_command_encoder
map_async
device.poll
execute_tensorcube
run_tensorcube
commit_route
advance_epoch
set_default
set_user_visible
set_production
transmute
```

References to bridge and WGPU types are allowed only for contract inspection. Constructors, leases and dispatch calls remain forbidden.

## 18. Protected State

Hash before and after:

- Registry v4;
- R1F final seal;
- D0 and D0R1 final seals and local manifests;
- D0 shape/layout census;
- canonical K6P source;
- model weights and route mutation evidence when present.

PASS requires:

- Registry diff 0;
- route slot diff 0;
- route epoch diff 0;
- K6P source diff 0;
- model weight diff 0;
- runtime output authority diff 0.

`native_wgpu.rs` is protected by semantic fingerprint. The existing Burn matmul, tile ranges, merged-logits ordering and `[1, atlas.vocab_size]` output construction must remain present.

## 19. Runtime Artifacts

The bake ZIP is source-only and must not include D0R2 runtime artifacts, manifests, receipts or SHA sidecars.

The Rust audit binary generates:

- immutable bundle: `artifacts/tensorcube/k7n_d0r2/<execution_id>/`;
- latest mirrors: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d0r2_*_latest.json`;
- local manifest: `ash_tensorcube_k7n_d0r2_local_manifest_latest.json`.

Required artifact families:

- prior D0R1 receipt;
- route family identity;
- shape contract;
- tile coverage;
- LHS, RHS and output layout;
- tail policy;
- raw lease preconditions;
- device identity;
- WGPU compatibility;
- shadow eligibility;
- protected-state guard;
- static checks;
- report;
- final seal;
- verdict;
- local manifest.

## 20. Required Execution

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r2_vocab_atlas_tile_shape_layout_tail_route_identity_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r1-pass `
  --require-d0r1-owner-ssot `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --target-vocab-atlas-projection-boundary `
  --bind-vocab-atlas-route-family-identity `
  --resolve-m-from-last-hidden `
  --resolve-n-from-tile-token-len `
  --resolve-k-from-model-hidden-size `
  --verify-tile-weight-shape `
  --verify-tile-range-coverage `
  --capture-lhs-physical-layout `
  --capture-rhs-post-swap-physical-layout `
  --capture-output-layout-contract `
  --classify-full-and-ragged-tiles `
  --require-ragged-tail-burn-only `
  --require-no-padding `
  --require-no-masking `
  --audit-raw-buffer-lease-preconditions `
  --audit-same-device-identity `
  --audit-wgpu-type-generation-compatibility `
  --classify-shadow-eligibility `
  --require-k6p-route-not-aliased `
  --require-no-raw-buffer-lease `
  --require-no-tensorcube-dispatch `
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

## 21. PASS Conditions

- D0R1 PASS, verdict and manifest validate;
- Registry v4 remains valid at epoch 1;
- vocab-atlas route family identity is deterministic and distinct from K6P;
- M/N/K semantics are resolved;
- tile coverage is complete and non-overlapping;
- LHS, swapped RHS and output layouts are explicitly classified;
- ragged tail is Burn-only;
- padding, masking and TensorCube tail dispatch remain disabled;
- raw lease preconditions are fully classified;
- Device/Queue identity and WGPU generations are classified;
- eligibility or exact blockers are emitted;
- all dispatch, lease, output, comparison and route mutation counters remain zero;
- Burn output remains authoritative;
- protected state is unchanged;
- no performance, production or Tensor Core execution claim is emitted.

## 22. Final Outcomes

Eligible:

`vocab_atlas_tile_shape_layout_tail_route_identity_contract_completed_and_candidate_is_eligible_for_closure_audit_without_runtime_dispatch_or_output_change`

Blocked:

`vocab_atlas_tile_shape_layout_tail_route_identity_contract_completed_but_candidate_remains_explicitly_blocked_without_runtime_dispatch_or_output_change`

Both are valid D0R2 contract PASS outcomes. A blocked outcome must contain at least one exact blocker code.

## 23. Explicit Non-Authorization

D0R2 PASS does not authorize:

- raw-buffer lease;
- TensorCube pipeline creation or dispatch;
- route registration or epoch change;
- Candidate, Default, UserVisible or Production change;
- tail padding or TensorCube ragged-tail execution;
- parity execution;
- D1 binding;
- performance or production claims.

## 24. Next State

Eligible outcome authorizes only:

`ASH-TCU-K7N-D0R3_VOCAB_ATLAS_FIRST_SHADOW_CONSUMER_CANDIDATE_CLOSURE_AUDIT`

Blocked outcome authorizes only:

`ASH-TCU-K7N-D0R2R_<BLOCKER>_PREREQUISITE_REPAIR`

The candidate closure audit must consume the D0R1 owner SSOT and the D0R2 route, shape, layout, tail, raw-lease and WGPU compatibility contracts. It may recommend D1 but may not dispatch TensorCube.
