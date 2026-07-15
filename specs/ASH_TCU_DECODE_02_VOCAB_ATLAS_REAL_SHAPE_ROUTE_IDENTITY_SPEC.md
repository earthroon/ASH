# ASH-TCU-DECODE-02 SPEC

## VOCAB_ATLAS_REAL_SHAPE_ROUTE_IDENTITY

```text
patch_id=ASH-TCU-DECODE-02_VOCAB_ATLAS_REAL_SHAPE_ROUTE_IDENTITY
parent_patch=ASH-TCU-DECODE-01_GENERATION_SHADOW_SESSION_LIFECYCLE_SEAL
parent_package=ash_pass3_ASH-TCU-DECODE-01_generation_shadow_session_lifecycle_seal_code_baked_no_spec_no_docs_no_runtime_artifacts_no_sha.zip
parent_package_sha256=a4d6d44b69bdf8ba69a2d5e1691ddd8f377dd6b6fa7d244150d6cdec25eca106
parent_execution_id=decode01-a2451f265d020ab00457
parent_status=PASS_ASH_TCU_DECODE_01_GENERATION_SHADOW_SESSION_LIFECYCLE_SEAL
mutation_class=runtime_shape_identity_observation_only
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 1. Purpose

DECODE-01 sealed the lifetime of the generation-scoped TensorCube shadow observer. The observer now begins, crosses the Burn vocab-atlas projection boundary, and finalizes exactly once on every reachable termination path.

The next blocker is route identity. The current observer records only projection-level metadata such as input row count, hidden size, atlas tile count and vocabulary size. It does not bind the actual full-tile `M/N/K`, logical and physical RHS layout, canonical dispatch geometry, model-shape identity, tile capacity, tail classification or route digest consumed by a future live shadow dispatch.

DECODE-02 introduces one deterministic, model-bound and runtime-value-bound vocab-atlas route identity contract. It resolves the exact canonical default full-tile route for the current ASH model while preserving Burn as the sole output authority and leaving TensorCube execution disabled.

This patch is identity and observation only. It must not acquire raw buffers, create a TensorCube command encoder, dispatch a TensorCube kernel, read back TensorCube output, compare parity, merge logits, mutate a route registry or change generated tokens.

## 2. Critical dimension correction

The LM-head and vocab-atlas projection reduction dimension is:

```text
K = ModelSpec.dimensions.hidden_size
```

It is not:

```text
ModelSpec.dimensions.intermediate_size
```

For the current v5 ASH model:

```text
vocab_size=48259
hidden_size=2048
intermediate_size=5632
```

Therefore the canonical vocab-atlas route must bind:

```text
M=1
N=1024
K=2048
```

The value `5632` belongs to the FFN intermediate domain and must never be used as the vocab-atlas projection K. Existing TensorCube observer tests or audit fixtures that call `observe_before_vocab_atlas_projection(..., 5632, ...)` must be repaired to derive K from the model-shape identity or use the canonical `2048` fixture.

DECODE-02 must fail when any live vocab-atlas route identity reads `dimensions.intermediate_size` as K or preserves a hardcoded `5632` projection-hidden fixture.

## 3. Current source truth

The supplied parent source establishes the following ownership chain:

```text
ModelSpec.dimensions.hidden_size
  -> NativeWgpuModel.spec.dimensions.hidden_size
  -> checkpoint full.hidden_size
  -> NativeVocabTile.hidden_size
  -> tile.weight shape [token_len, hidden_size]

request native_vocab_tile_size
  -> MemoryBudgetDecision.effective_native_vocab_tile_size
  -> NativeWgpuModel::from_full_checkpoints_with_vocab_atlas(vocab_tile_size)
  -> NativeVocabAtlas.tile_vocab
  -> NativeVocabTile.token_len

NativeWgpuModel::slice_last_hidden_row
  -> last_hidden shape [1, hidden_size]
  -> project_last_hidden_to_logits_vocab_atlas_observed
  -> Burn matmul [1,K] x logical [K,N]
  -> tile logits [1,N]
```

Current source expressions:

```text
M = last_hidden.dims()[0]
N = tile.token_len
K = tile.hidden_size and last_hidden.dims()[1]
stored RHS = tile.weight with logical storage shape [N,K]
Burn RHS view = tile.weight.clone().swap_dims(0,1) with logical shape [K,N]
Burn tile output = [1,N]
merged Burn output = [1,vocab_size]
```

The effective tile capacity authority is `NativeVocabAtlas.tile_vocab` after request parsing and memory-budget clamping. The requested value alone is not route truth.

## 4. Canonical current-model census

With the canonical default configuration:

```text
vocab_size=48259
hidden_size=2048
effective_native_vocab_tile_size=1024
dtype=f32
accumulation_dtype=f32
```

The atlas census is:

```text
tile_count=48
full_tile_count=47
ragged_tail_count=1
full_tile_token_len=1024
ragged_tail_token_len=131
first_full_tile_token_start=0
last_full_tile_token_start=47104
ragged_tail_token_start=48128
full_tile_weight_bytes=8388608
ragged_tail_weight_bytes=1073152
full_vocab_weight_bytes=395337728
```

The canonical full-tile dispatch geometry is:

```text
workgroup=[16,16,1]
dispatch=[64,1,1]
k_panel_extent=4
k_panel_count=512
k_tail=0
output_bounds_guard_required=true
reduction_bounds_guard_required=false
```

`output_bounds_guard_required=true` is expected because M is 1 while the workgroup Y extent is 16. This is not the vocab ragged-tail class.

## 5. Authority boundary

The patch must preserve:

```text
burn_output_authority=true
production_authority=false
raw_buffer_lease_count=0
tensorcube_dispatch_count=0
tensorcube_output_count=0
parity_comparison_count=0
downstream_output_commit_count=0
route_registry_mutation_count=0
route_epoch_change_count=0
queue_submit_count=0
device_poll_count=0
buffer_map_count=0
runtime_output_changed=false
```

The patch may change TensorCube observation metadata and local audit artifacts. It must not change logits, token IDs, top-k ordering, stop behavior, sampling behavior, KV state, tokenizer state, model weights, LoRA weights or BaseTrain state.

## 6. SSOT ownership

| Domain | SSOT owner |
|---|---|
| model family and version | `ModelSpec.model_spec_id`, `ModelSpec.version` |
| vocabulary size | `ModelSpec.dimensions.vocab_size`, cross-checked against `NativeVocabAtlas.vocab_size` |
| reduction K | `ModelSpec.dimensions.hidden_size`, cross-checked against last-hidden and every tile weight |
| FFN intermediate | `ModelSpec.dimensions.intermediate_size`, explicitly excluded from route K |
| projection M | `last_hidden.dims()[0]`, required to equal 1 for this route |
| effective full-tile N | `NativeVocabAtlas.tile_vocab` after memory-budget resolution |
| per-tile actual N | `NativeVocabTile.token_len` and `tile.weight.dims()[0]` |
| stored RHS layout | `TensorData::new(tile_slice.to_vec(), [token_len, hidden_size])` |
| logical RHS view | `tile.weight.clone().swap_dims(0,1)` |
| tile span | `NativeVocabTile.token_start`, `NativeVocabTile.token_len` |
| route digest | new DECODE-02 canonical digest owner in `burn_webgpu_backend` |
| live adapter | new model-core vocab-atlas route resolver |
| audit artifacts and manifest | DECODE-02 Rust audit executable |

No command-line default, test fixture, copied receipt or console string may override these owners.

## 7. Two-level identity contract

DECODE-02 must separate route identity from tile invocation identity.

### 7.1 Route identity

A route identifies reusable compute semantics and must contain:

```rust
pub struct VocabAtlasRealShapeRouteIdentity {
    pub schema_version: String,
    pub route_family_id: String,
    pub route_id: String,
    pub operation_family: String,
    pub source_callsite_id: String,
    pub source_symbol: String,
    pub model_shape_identity_digest: String,
    pub model_spec_id: String,
    pub model_spec_version: u32,
    pub vocab_size: u32,
    pub m: u32,
    pub n: u32,
    pub k: u32,
    pub lhs_logical_shape: [u32; 2],
    pub lhs_logical_stride: [u32; 2],
    pub rhs_storage_shape: [u32; 2],
    pub rhs_storage_stride: [u32; 2],
    pub rhs_logical_shape: [u32; 2],
    pub rhs_logical_stride: [u32; 2],
    pub output_shape: [u32; 2],
    pub output_stride: [u32; 2],
    pub dtype: String,
    pub accumulation_dtype: String,
    pub workgroup: [u32; 3],
    pub dispatch: [u32; 3],
    pub k_panel_extent: u32,
    pub k_panel_count: u32,
    pub k_tail: u32,
    pub output_bounds_guard_required: bool,
    pub reduction_bounds_guard_required: bool,
    pub shader_digest: String,
    pub abi_digest: String,
    pub pipeline_layout_digest: String,
    pub output_authority: String,
    pub shadow_dispatch_authorized: bool,
    pub production_output_authorized: bool,
    pub route_digest: String,
}
```

Canonical schema and family:

```text
schema_version=ash_tensorcube_decode02_vocab_atlas_real_shape_route_v1
route_family_id=ash.tensorcube.decode02.vocab_atlas.f32.rhs_strided_view.v1
operation_family=vocab_atlas_tile_projection
source_callsite_id=call-66cc14a91d31bf8452215b67
source_symbol=NativeWgpuModel::project_last_hidden_to_logits_vocab_atlas_observed
```

Canonical route values:

```text
m=1
n=1024
k=2048
lhs_logical_shape=[1,2048]
lhs_logical_stride=[2048,1]
rhs_storage_shape=[1024,2048]
rhs_storage_stride=[2048,1]
rhs_logical_shape=[2048,1024]
rhs_logical_stride=[1,2048]
output_shape=[1,1024]
output_stride=[1024,1]
dtype=f32
accumulation_dtype=f32
workgroup=[16,16,1]
dispatch=[64,1,1]
k_panel_extent=4
k_panel_count=512
k_tail=0
output_authority=burn
shadow_dispatch_authorized=false
production_output_authorized=false
```

The route ID must be digest-derived:

```text
ash.tensorcube.decode02.vocab_atlas.m1.n1024.k2048.f32.<route_digest_prefix>
```

The digest prefix is presentation only. Full equality uses the complete 64-character digest.

### 7.2 Tile invocation identity

A tile invocation identifies the runtime tile span and must contain:

```rust
pub struct VocabAtlasTileInvocationIdentity {
    pub schema_version: String,
    pub route_digest: String,
    pub generation_step_ordinal: u64,
    pub tile_id: u32,
    pub tile_token_start: u32,
    pub tile_token_len: u32,
    pub tile_weight_shape: [u32; 2],
    pub tile_weight_bytes: u64,
    pub tile_class: VocabAtlasRuntimeTileClass,
    pub invocation_digest: String,
}
```

`tile_token_start` and `tile_id` must not split identical full-tile shapes into separate routes. They belong to the invocation digest.

For the canonical model, all 47 full tiles share one route digest. Their invocation digests differ.

## 8. Model-shape identity

The route must bind a projection-relevant semantic model identity rather than an absolute model-spec path.

```rust
pub struct VocabAtlasModelShapeIdentity {
    pub schema_version: String,
    pub model_spec_id: String,
    pub model_spec_version: u32,
    pub vocab_size: u32,
    pub hidden_size: u32,
    pub intermediate_size: u32,
    pub lm_head_dtype: String,
    pub tie_word_embeddings: bool,
    pub semantic_digest: String,
}
```

The semantic digest includes `intermediate_size` only as a collision and diagnostic field. Route K must still equal `hidden_size`.

Validation requires:

```text
vocab_size=48259
hidden_size=2048
intermediate_size=5632
lm_head_dtype=f32 or a source-proven runtime f32 conversion contract
hidden_size != intermediate_size
route.k == hidden_size
route.k != intermediate_size
```

If the local model spec differs, the audit must emit HOLD rather than silently coercing it to the canonical route.

## 9. Runtime tile classification

```rust
pub enum VocabAtlasRuntimeTileClass {
    CanonicalDefaultFullTile,
    NonCanonicalFullTileCandidate,
    RaggedTailBurnOnly,
    Invalid,
}
```

Classification rules:

```text
CanonicalDefaultFullTile:
  M=1
  N=1024
  K=2048
  token_len == atlas.tile_vocab
  tile.weight.dims == [1024,2048]
  dtype=f32

NonCanonicalFullTileCandidate:
  M=1
  N == atlas.tile_vocab
  token_len == atlas.tile_vocab
  dimensions positive
  exact identity differs from canonical default
  no dispatch authorization in DECODE-02

RaggedTailBurnOnly:
  0 < token_len < atlas.tile_vocab
  token_start + token_len == vocab_size
  no padding
  no masking
  no zero-fill promotion
  no TensorCube route activation

Invalid:
  zero dimension
  token_len > atlas.tile_vocab
  hidden mismatch
  overlapping or gapped token span
  weight shape mismatch
  M != 1
  unsupported dtype
  arithmetic overflow
```

The current final tile with N=131 is `RaggedTailBurnOnly`. It must not be inserted into an active TensorCube route registry by this patch.

## 10. Atlas census contract

Before the Burn tile loop, model_core must build one immutable census from actual runtime metadata without materializing weight values or logits.

```rust
pub struct VocabAtlasRealShapeCensus {
    pub schema_version: String,
    pub model_shape_identity: VocabAtlasModelShapeIdentity,
    pub input_m: u32,
    pub input_k: u32,
    pub atlas_vocab_size: u32,
    pub effective_tile_capacity: u32,
    pub tile_count: u32,
    pub full_tile_count: u32,
    pub ragged_tail_count: u32,
    pub invalid_tile_count: u32,
    pub first_token_start: u32,
    pub covered_token_count: u32,
    pub gap_count: u32,
    pub overlap_count: u32,
    pub canonical_full_tile_route: Option<VocabAtlasRealShapeRouteIdentity>,
    pub ragged_tail_summary: Option<VocabAtlasRaggedTailIdentity>,
    pub census_digest: String,
}
```

Required current-model truth:

```text
input_m=1
input_k=2048
atlas_vocab_size=48259
effective_tile_capacity=1024
tile_count=48
full_tile_count=47
ragged_tail_count=1
invalid_tile_count=0
first_token_start=0
covered_token_count=48259
gap_count=0
overlap_count=0
```

The census checks every `NativeVocabTile`:

```text
tile_id is contiguous from zero
token_start equals previous token end
token_len is positive
token_len <= atlas.tile_vocab
tile.hidden_size == model hidden_size
tile.weight.dims == [token_len, hidden_size]
tile.bytes == token_len * hidden_size * sizeof(f32)
final token end == atlas.vocab_size
```

## 11. Observer integration

Extend the generation shadow observation metadata with route-resolution evidence.

The existing projection-level call remains before the Burn loop, but it must receive or construct the real-shape census rather than only `(input_rows, hidden_size, atlas_tile_count, vocab_size)`.

Required observation state:

```rust
pub enum TensorCubeShadowRouteIdentityState {
    Unresolved,
    CanonicalRouteResolvedNoExecution,
    NonCanonicalRouteObservedNoExecution,
    RaggedTailBurnOnlyObserved,
    InvalidBlocked,
}
```

The receipt must bind:

```text
model_shape_identity_digest
census_digest
canonical_route_id
canonical_route_digest
full_tile_count
ragged_tail_count
route_identity_state
burn_output_authority=true
runtime_output_changed=false
```

The session remains generation-scoped. The route identity is stable for all projection steps in one generation. A later step that produces a different model-shape or atlas-capacity digest must block observation and must not silently replace the session identity.

## 12. Existing route separation

The D1R7 and D1R9 shape catalog contains microbenchmark signatures such as K values 1, 3, 4, 5, 15, 16 and 17. Those routes are not aliases for the live vocab-atlas projection.

DECODE-02 must prove:

```text
live_route_k=2048
microbenchmark_route_alias_count=0
k6p_route_alias=false
legacy_d0r2_family_alias=false
active_d1r9_registry_mutation_count=0
route_epoch_change_count=0
```

Existing shaders, ABI and pipeline-layout sources may be referenced by digest. Existing micro-shape route IDs must never be reused merely because the operation family and shader are the same.

## 13. Layout contract

The canonical logical contract is:

```text
LHS logical [M,K]
LHS row stride K
stored RHS [N,K] contiguous row-major
logical RHS [K,N] through strided transpose view
RHS k stride 1
RHS n stride K
output [M,N] contiguous row-major
output row stride N
```

Current ABI binding:

```text
lhs_row_stride_elements=K
rhs_k_stride_elements=1
rhs_n_stride_elements=K
output_row_stride_elements=N
tile_token_len=N
tail_class=0 for full tile
```

DECODE-02 does not claim that Burn raw buffer offsets or buffer-usage flags are already lease-safe. Those are DECODE-03 responsibilities. It must record:

```text
logical_layout_resolved=true
stored_rhs_constructor_contiguous=true
rhs_logical_transpose_is_strided_view=true
raw_buffer_offset_resolved=false unless source-proven
raw_buffer_usage_resolved=false unless source-proven
raw_buffer_lease_authorized=false
```

No physical transpose materialization may be invented.

## 14. Tail contract

The canonical ragged tail is:

```text
token_start=48128
token_len=131
weight_shape=[131,2048]
weight_bytes=1073152
class=ragged_tail_burn_only
```

Required tail rules:

```text
ragged_tail_burn_only=true
tensorcube_tail_dispatch_authorized=false
padding_allowed=false
masking_allowed=false
silent_zero_fill_allowed=false
tail_route_registry_insert_allowed=false
```

The shader's output bounds guard does not authorize a ragged vocab tail. Tail authorization remains a separate semantic policy.

## 15. Required source changes

Modify:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_shadow_observer_owner.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d0r1_contract_audit.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/tensorcube_generation_shadow_session.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/lib.rs
crates/model_core/tests/ash_tcu_decode_01_generation_shadow_session_lifecycle.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Add backend identity contracts:

```text
crates/burn_webgpu_backend/src/tensorcube_decode_02_vocab_atlas_model_shape_identity.rs
crates/burn_webgpu_backend/src/tensorcube_decode_02_vocab_atlas_real_shape_route.rs
crates/burn_webgpu_backend/src/tensorcube_decode_02_vocab_atlas_tile_invocation.rs
crates/burn_webgpu_backend/src/tensorcube_decode_02_vocab_atlas_tail_identity.rs
crates/burn_webgpu_backend/src/tensorcube_decode_02_vocab_atlas_census.rs
```

Add model-core adapter:

```text
crates/model_core/src/vocab_atlas_real_shape_route_identity.rs
```

Add tests:

```text
crates/burn_webgpu_backend/tests/ash_tcu_decode_02_vocab_atlas_real_shape_route.rs
crates/model_core/tests/ash_tcu_decode_02_vocab_atlas_real_shape_route_integration.rs
```

Add Rust report and executable:

```text
crates/orchestrator_local/src/ash_tcu_decode_02_vocab_atlas_real_shape_route_identity_report.rs
crates/orchestrator_local/src/bin/ash_tcu_decode_02_vocab_atlas_real_shape_route_identity.rs
```

No new WGSL file is required. DECODE-02 binds the current canonical shader, ABI and pipeline-layout source digests without dispatching them.

## 16. Static fail-closed audit

The Rust audit must inspect actual source and fail when any of the following is nonzero:

```text
vocab_projection_k_from_intermediate_size_count
hardcoded_projection_hidden_5632_fixture_count
live_projection_microbenchmark_route_alias_count
live_projection_k6p_alias_count
unclassified_vocab_atlas_projection_callsite_count
unclassified_effective_tile_capacity_owner_count
unclassified_tile_weight_shape_owner_count
unclassified_tail_tile_count
route_digest_collision_count
invocation_digest_collision_count
full_tile_route_cardinality_mismatch_count
ragged_tail_tensorcube_authorization_count
active_route_registry_mutation_count
route_epoch_mutation_count
raw_buffer_lease_count
tensorcube_dispatch_count
tensorcube_output_count
parity_comparison_count
downstream_output_commit_count
runtime_output_change_count
```

Static presence of a field name is not sufficient. The audit must validate constructors, digest recomputation, runtime census wiring, model-core callsite wiring and tests.

## 17. Required tests

### 17.1 Dimension ownership

- K is derived from `ModelSpec.dimensions.hidden_size`.
- Current K equals 2048.
- Intermediate size equals 5632 and is rejected as route K.
- A model hidden-size change produces a different model-shape and route digest.
- A mismatched tile hidden size is invalid.

### 17.2 Canonical atlas census

- `48259 / 1024` produces 48 tiles.
- Full tile count is 47.
- Ragged tail count is 1.
- Tail N is 131.
- Coverage begins at 0 and ends at 48259.
- Gap, overlap, zero-length and invalid counts are zero.

### 17.3 Canonical route

- Route is exactly M1-N1024-K2048-f32.
- LHS, RHS storage, RHS logical and output shapes are exact.
- RHS logical strides are `[1,2048]`.
- Workgroup is `[16,16,1]`.
- Dispatch is `[64,1,1]`.
- K panel count is 512 and K tail is zero.
- Burn authority is true.
- Shadow dispatch and production output authorization are false.

### 17.4 Route and invocation separation

- All canonical full tiles share one route digest.
- Different tile starts produce different invocation digests.
- `tile_token_start` does not alter route digest.
- N, K, dtype, shader digest, ABI digest, pipeline-layout digest or model-shape changes alter route digest.
- Duplicate route digests with different semantic fields fail.

### 17.5 Tail policy

- N131 is classified as `RaggedTailBurnOnly`.
- Tail padding, masking, zero fill and route activation are false.
- Tail identity is present in census but absent from active route candidates.

### 17.6 Runtime protection

- Burn token logits are byte-equivalent before and after observation for deterministic fixtures.
- TensorCube execution counters remain zero.
- Registry bytes and epoch remain unchanged.
- DECODE-01 finalization remains exactly once.
- Repeated generation steps retain the same route identity within one lifecycle.
- Route identity drift during one lifecycle blocks observation.

## 18. Rust-owned artifacts

The bake package contains source only. It must not contain pre-generated DECODE-02 manifests, receipts, reports, verdicts, final seals, latest mirrors, immutable bundles or SHA sidecars.

The sole artifact owner is:

```text
ash_tcu_decode_02_vocab_atlas_real_shape_route_identity
```

Immutable root:

```text
artifacts/tensorcube/decode_02/<execution_id>/
```

Latest mirror root:

```text
workspace/runtime/tensorcube/
```

The Rust executable generates:

```text
parent_binding
model_shape_identity
source_callsite_audit
effective_tile_capacity_owner
atlas_shape_census
canonical_full_tile_route_identity
ragged_tail_burn_only_identity
route_invocation_separation
route_collision_guard
legacy_route_alias_guard
protected_behavior_guard
source_digest_manifest
report
verdict
final_seal
local_manifest
```

`local_manifest` is generated last from the actual bytes produced by the same Rust execution. It binds immutable and latest paths with SHA-256 digests.

Required packaging truth:

```text
runtime_generated=true
rust_artifact_owner=ash_tcu_decode_02_vocab_atlas_real_shape_route_identity
spec_baked_into_zip=false
docs_baked_into_zip=false
packaged_runtime_artifact_count=0
sha256_sidecars_baked=false
```

Python, shell, ZIP tooling and copied console output must not synthesize PASS evidence.

## 19. Required execution

Canonical local PowerShell execution:

```powershell
cargo run --locked `
  --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_decode_02_vocab_atlas_real_shape_route_identity -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --model-spec ".\specs\model_spec_v5_48259.toml" `
  --parent-manifest ".\workspace\runtime\tensorcube\ash_tensorcube_decode_01_local_manifest_latest.json" `
  --effective-vocab-tile-size 1024 `
  --require-vocab-size 48259 `
  --require-hidden-size 2048 `
  --require-intermediate-size 5632 `
  --require-projection-m 1 `
  --require-f32 `
  --require-canonical-full-tile-route `
  --require-ragged-tail-burn-only `
  --require-route-invocation-identity-separation `
  --require-no-legacy-route-alias `
  --require-burn-output-authority `
  --require-no-raw-buffer-lease `
  --require-no-tensorcube-dispatch `
  --require-no-route-mutation `
  --require-no-runtime-output-change `
  --write-runtime-artifacts `
  --write-local-manifest
```

The executable must validate the DECODE-01 parent manifest and final seal before producing DECODE-02 artifacts.

## 20. PASS conditions

PASS requires all of the following:

```text
parent_decode_01_manifest_valid=true
parent_decode_01_pass=true
model_spec_loaded=true
model_shape_identity_valid=true
vocab_size=48259
hidden_size=2048
intermediate_size=5632
projection_k_owner=hidden_size
projection_k=2048
projection_k_intermediate_confusion_count=0
effective_tile_capacity_owner=NativeVocabAtlas.tile_vocab
canonical_effective_tile_capacity=1024
atlas_tile_count=48
full_tile_count=47
ragged_tail_count=1
invalid_tile_count=0
gap_count=0
overlap_count=0
canonical_route_count=1
canonical_route_shape=M1_N1024_K2048
canonical_route_dtype=f32
canonical_dispatch=64x1x1
canonical_k_panel_count=512
canonical_k_tail=0
full_tile_shared_route_digest_count=1
full_tile_invocation_count=47
ragged_tail_n=131
ragged_tail_burn_only=true
legacy_route_alias_count=0
route_digest_collision_count=0
active_registry_mutation_count=0
route_epoch_change_count=0
raw_buffer_lease_count=0
tensorcube_dispatch_count=0
tensorcube_output_count=0
parity_comparison_count=0
downstream_output_commit_count=0
burn_output_authority=true
runtime_output_changed=false
rust_artifacts_generated=true
local_manifest_written_last=true
```

## 21. HOLD and FAIL

HOLD examples:

```text
model_spec_not_resolved
parent_decode_01_artifact_not_resolved
current_model_dimensions_differ_from_canonical_identity
effective_tile_capacity_not_canonical_default
runtime_dtype_not_source_proven_f32
physical_raw_buffer_layout_not_yet_resolved_for_decode_03
```

A noncanonical effective tile capacity may still produce a diagnostic candidate identity, but it must not produce the canonical PASS route.

FAIL examples:

```text
parent_manifest_digest_mismatch
model_hidden_and_tile_hidden_mismatch
projection_k_bound_to_intermediate_size
atlas_coverage_gap_or_overlap
tile_weight_shape_mismatch
route_digest_nondeterministic
route_digest_collision
legacy_microbenchmark_route_aliased_to_live_projection
ragged_tail_tensorcube_authorized
active_registry_mutated
route_epoch_changed
raw_buffer_lease_observed
tensorcube_dispatch_observed
runtime_output_changed
protected_source_or_model_state_mutated
```

## 22. Expected PASS

```text
PASS_ASH_TCU_DECODE_02_VOCAB_ATLAS_REAL_SHAPE_ROUTE_IDENTITY
verdict=canonical_default_vocab_atlas_m1_n1024_k2048_route_identity_sealed_from_model_hidden_size_with_47_shared_full_tile_invocations_and_n131_ragged_tail_burn_only
output_authority=burn
production_authority=false
runtime_output_changed=false
```

## 23. Next-state contract

DECODE-02 authorizes only:

```text
ASH-TCU-DECODE-03_LIVE_SAME_DEVICE_SHADOW_DISPATCH_SPLICE
```

DECODE-03 may consume only the exact DECODE-02 route digest and model-shape identity digest sealed by the local manifest. It must revalidate:

```text
M=1
N=1024
K=2048
dtype=f32
full tile class
same model-shape digest
same shader digest
same ABI digest
same pipeline-layout digest
same effective atlas tile capacity
same Device and Queue identity
```

Any mismatch must preserve Burn-only execution. DECODE-02 does not authorize tail dispatch, output promotion, production authority or BaseTrain integration.
