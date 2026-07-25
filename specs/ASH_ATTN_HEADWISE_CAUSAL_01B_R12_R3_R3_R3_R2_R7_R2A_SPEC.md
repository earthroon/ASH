# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2A

## Existing Headwise Tensor Texture Asset Adoption / Shader and Runtime Source Identity / Reuse Boundary Registry / Duplicate Primitive Zero / Active Path Reconnection Preparation Seal

## 0. Document state

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2A
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R1
PATCH_CLASS=asset-adoption,source-identity,reuse-boundary,static-truth,reconnection-preparation
DEFAULT_VERDICT=HOLD
RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
PREBAKED_RUNTIME_ARTIFACTS=forbidden
```

This revision does not introduce or promote a new texture-attention runtime. It identifies the existing Headwise tensor-texture assets, seals their exact source identity and reuse boundaries, proves single-owner primitive authority, and emits the preparation plan required to reconnect those assets to the active Headwise path in R7-R2B and later revisions.

## 1. Inherited authority

R7-R2A inherits without replacement:

- component-scoped ABI identity;
- strict CLI registry and canonical run contract;
- parent artifact and manifest binding;
- negative-control execution discipline;
- source digest and receipt conventions;
- rollback anchors and authority commit ordering;
- the R7 active buffer-based Headwise route, output ABI, guard ownership, same-device policy, and host-materialization prohibition.

R7-R2A must not redefine the current backend ABI, model-core ABI, active production kernel, active production route, output ABI, or logical Q/K/V tensor semantics.

## 2. Problem statement

The repository already contains separate assets for:

1. the active Headwise buffer dispatcher and same-device raw bridge;
2. an RGBA4 `textureLoad` attention shader and math LUT integration;
3. the active query-head to KV-head GQA mapping and output indexing;
4. texture finite, signature, checksum, and failure classification logic;
5. vec4 LUT, lane identity, pack-owner, and overlap-rejection precedent;
6. texture-layout vocabulary for integer coordinates, no filtering, no mipmapping, and RGBA packing.

These assets are not yet connected as one active execution path. Implementing another tensor-texture stack would risk duplicate packing rules, duplicate GQA maps, divergent coordinate authority, divergent guard semantics, multiple dispatcher or pipeline owners, and ambiguous route identity. R7-R2A prevents that split before runtime reconnection begins.

## 3. Goals

R7-R2A must prove that:

- every adopted source asset exists and is identified by exact source-byte digest;
- every required symbol or semantic primitive is present in executable code, not only in comments or strings;
- each reused primitive has one authoritative owner;
- permitted adaptation and prohibited reuse surfaces are explicit;
- semantic duplicate primitive count is zero;
- active production route, shader, binding layout, output ABI, dispatcher owner, pipeline owner, and submission owner remain unchanged;
- a complete binding, parameter, coordinate, and runtime-owner delta exists for R7-R2B;
- no texture candidate is activated and no production route is mutated by this revision.

## 4. Non-goals

R7-R2A must not create or promote:

- a WGPU `Texture` or `TextureView` owner;
- KV page residency, page sealing, or buffer-to-texture migration;
- GQA2, GQA4, or GQA8 cluster kernels;
- cluster guard finalization or batched downstream commit;
- route-LUT mutation or performance promotion;
- `rgba16float` adoption;
- pre-baked runtime JSON, manifest, receipt, or performance evidence.

## 5. Component revision contract

```text
backend_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
model_core_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
active_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
active_route_policy_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
asset_adoption_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2A
cli_contract_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2A
```

Cross-component revision equality must not be required. The new authority in this patch is the asset-adoption and CLI-contract revision only. The active kernel and route remain R7.

## 6. Authoritative asset registry

Rust must emit an exact registry entry for each adopted source:

```rust
pub struct TextureAssetRegistryEntry {
    pub asset_id: String,
    pub source_path: String,
    pub asset_kind: TextureAssetKind,
    pub source_sha256: String,
    pub source_git_blob_sha: Option<String>,
    pub semantic_role: TextureAssetSemanticRole,
    pub adoption_mode: TextureAssetAdoptionMode,
    pub active_before_r2a: bool,
    pub active_after_r2a: bool,
    pub mutation_allowed: bool,
    pub fork_allowed: bool,
    pub authoritative_primitives: Vec<String>,
    pub prohibited_reuse_surfaces: Vec<String>,
}
```

The supported adoption modes are:

```text
reuse-exact
reuse-with-binding-rebind
reuse-with-coordinate-split
extract-guard-only
extract-primitive-only
reference-only
reject-for-active-path
```

## 7. Required source assets and reuse boundaries

### 7.1 Active Headwise runtime

Path:

```text
crates/burn_webgpu_backend/src/headwise_atlas.rs
```

Role and permitted reuse:

- active dispatcher lifecycle;
- same-device raw bridge;
- GQA metadata and `query_heads_per_kv` authority;
- pipeline-cache ownership;
- command-encoder and queue-submission ownership;
- current buffer-route shape and output validation.

Adoption mode: `reuse-with-binding-rebind`.

Forbidden:

- pretending a buffer binding is a texture binding;
- replacing or removing the current buffer route in R7-R2A;
- introducing another device, queue, dispatcher, pipeline cache, or submission owner.

### 7.2 RGBA tensor-texture attention shader

Path:

```text
crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_texture_lut_exp.wgsl
```

Role and permitted reuse:

- RGBA4 tensor payload load;
- exact integer `textureLoad`;
- vec4 dot-product accumulation;
- existing exp/log math-LUT integration;
- mip-level-zero access.

Adoption mode: `reuse-with-coordinate-split`.

Required later adaptation:

- split query-head and KV-head coordinate authority;
- use buffer Q plus immutable texture K/V in the hybrid route;
- separate `seq_q` and `seq_kv`;
- add page-table-driven physical-layer lookup.

Forbidden:

- applying one `head` index to Q, K, and V under GQA;
- replicating K/V rows per query head;
- normalized KV coordinates;
- `textureSample` for tensor payload access.

### 7.3 Current buffer attention shader

Path:

```text
crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention.wgsl
```

Role:

- authoritative query-head to KV-head mapping;
- current output indexing and output ABI;
- numerical and bounds baseline.

Adoption mode: `extract-primitive-only`.

Forbidden:

- a second texture-only GQA mapping implementation;
- route-specific integer-division semantics;
- hard-coded 32/4/8 model geometry;
- output ABI mutation.

### 7.4 Texture guard shader

Path:

```text
crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_texture_lut_alpha_scale.wgsl
```

Role and permitted extraction:

- finite max, denominator, LSE, and output checks;
- overflow and underflow classification;
- signature generation and expected-signature comparison;
- checksum and failure-flag encoding.

Adoption mode: `extract-guard-only`.

Forbidden:

- importing RGB-payload plus A-scale packing;
- using A as metadata or scale in the RGBA4 KV payload route;
- changing the checksum algorithm silently.

All RGBA channels in the future KV texture route remain tensor payload authority.

### 7.5 Texture-layout policy precedent

Path:

```text
crates/ash_core/src/sft_ffn_texture_atlas.rs
```

Role:

- RGBA4 packing vocabulary;
- `textureLoad`-only and integer-coordinate policy;
- no-filter, no-mipmap, no-sRGB policy;
- layout-digest precedent.

Adoption mode: `reference-only`.

Forbidden:

- using FFN tile coordinates as KV coordinates;
- treating the FFN manifest as a runtime texture owner;
- treating FFN payload identity as KV content identity.

### 7.6 Vec4 LUT and pack-owner precedent

Path:

```text
crates/burn_webgpu_backend/src/qwave_vec4_tile_atlas.rs
```

Role:

- vec4 lane identity;
- logical-to-physical LUT precedent;
- pack-owner write ownership;
- overlap rejection and canonical LUT serialization.

Adoption mode: `extract-primitive-only`.

Forbidden:

- reusing Q-wave tensor semantics as KV semantics;
- treating byte offsets as texture coordinates;
- accepting different layout digests as one identity.

## 8. Exact source identity

Every source identity must include:

```rust
pub struct TextureAssetSourceIdentity {
    pub canonical_path: String,
    pub normalized_relative_path: String,
    pub byte_length: u64,
    pub sha256: String,
    pub git_blob_sha: Option<String>,
    pub line_ending_policy: String,
    pub encoding_policy: String,
    pub extraction_revision: String,
}
```

Requirements:

- paths are repository-root-relative, forward-slash-normalized, case-sensitive canonical identities;
- `..` components and symlink escapes are forbidden;
- SHA-256 is calculated from actual source bytes;
- a path, filename, revision string, or hard-coded digest must not substitute for source bytes;
- WGSL identities include raw digest, normalized diagnostic digest, entrypoint-signature digest, binding-layout digest, and semantic-primitive digest.

## 9. Symbol identity extraction

The Rust/WGSL lexical extractor must:

- extract Rust structs, enums, impls, constants, functions, modules, pipeline entries, and binding declarations;
- extract WGSL groups, bindings, compute entrypoints, workgroup sizes, functions, address spaces, texture declarations, `textureLoad`, `textureSample`, and `textureSampleLevel`;
- ignore identifiers appearing only in comments or string literals;
- use exact token boundaries;
- forbid source-wide substring counts as authority.

## 10. Reuse-boundary and primitive ownership registry

Every primitive must have exactly one authoritative owner, explicit allowed consumers, allowed adaptations, and prohibited reimplementation surfaces.

Required primitive IDs:

```text
P01 rgba4_tensor_payload_load
P02 integer_texel_fetch
P03 query_head_to_kv_head_map
P04 vec4_dot_accumulation
P05 attention_output_indexing
P06 finite_output_guard
P07 signature_generation
P08 checksum_classification
P09 exp_lut_lookup
P10 log1p_lut_lookup
P11 same_device_raw_bridge
P12 pipeline_cache_owner
P13 command_encoder_owner
P14 submission_owner
P15 vec4_lane_identity
P16 logical_to_physical_lut_pattern
P17 texture_layout_digest_pattern
P18 no_filter_payload_policy
P19 mip_zero_payload_policy
P20 output_abi_identity
```

The authoritative dispatcher lifecycle remains `headwise_atlas.rs`. The RGBA4 payload loader remains the existing texture-LUT shader. The GQA map and output indexing remain the active buffer shader. Guard primitives remain the existing texture guard shader, excluding its alpha-scale payload convention.

## 11. Duplicate primitive zero

A semantic duplicate is two or more implementations with the same semantic role, input shape, output shape, binding class, coordinate policy, channel packing, numerical operation, and route consumer, without an explicit baseline/candidate identity boundary.

Required counters:

```text
duplicate_rgba_payload_loader_count=0
duplicate_query_to_kv_mapping_count=0
duplicate_texture_coordinate_authority_count=0
duplicate_guard_classifier_count=0
duplicate_texture_layout_digest_owner_count=0
duplicate_dispatcher_owner_count=0
duplicate_pipeline_cache_owner_count=0
duplicate_submission_owner_count=0
duplicate_output_abi_owner_count=0
unowned_reused_primitive_count=0
```

Buffer and texture loaders, reference and candidate kernels, and rgba32/rgba16 candidates may coexist only when they have separate route and primitive IDs.

## 12. Active-path reconnection preparation

Rust must emit a reconnection plan containing:

- current dispatcher, baseline shader, texture shader, and guard asset IDs;
- required binding changes;
- required parameter changes;
- required coordinate changes;
- required new runtime owners;
- forbidden runtime-owner forks.

Planned binding delta:

```text
current:
Q=storage-buffer
K=storage-buffer
V=storage-buffer

future hybrid candidate:
Q=same-device storage-buffer
K=immutable tensor texture
V=immutable tensor texture
page-LUT=read-only storage-buffer
math-LUT=existing sampled texture
```

Planned parameter delta includes batch, q-head count, KV-head count, query-heads-per-KV, `seq_q`, `seq_kv`, head dimension, dimension-group count, page size, page count, layout revision, and active generation.

Planned coordinate delta:

```text
Q: batch + query-head + q-position
K/V: logical token -> page LUT -> physical page -> KV-head layer -> dimension group
```

New owners permitted only in R7-R2B:

```text
HeadwiseKvTextureResidency
HeadwiseKvTexturePageTable
HeadwiseKvTextureLayout
```

New `Device`, `Queue`, `Dispatcher`, `PipelineCache`, encoder authority, or submission authority is forbidden.

## 13. Active-path protection

Before and after snapshots must prove exact parity for:

- production route LUT identity;
- active buffer shader digest;
- active dispatcher source digest;
- active bind-group-layout identity;
- active output ABI identity;
- active guard policy identity;
- active submission topology identity.

Required counters:

```text
production_route_mutation_count=0
active_shader_replacement_count=0
active_binding_layout_mutation_count=0
production_pipeline_cache_mutation_count=0
production_output_abi_mutation_count=0
```

## 14. CLI extension

The R7-R1 strict registry is extended with:

```text
--texture-asset-adoption-policy existing-assets-only-v1
--texture-asset-registry-mode exact-source-identity-v1
--texture-reuse-boundary-policy single-owner-v1
--texture-duplicate-primitive-policy semantic-zero-v1
--texture-active-path-policy prepare-only-no-route-mutation-v1
--texture-source-extractor rust-wgsl-lexical-v1
--require-texture-source-digest true
--require-texture-symbol-identity true
--require-texture-reuse-boundary-registry true
--require-texture-duplicate-primitive-zero true
--require-texture-active-route-unchanged true
--require-texture-dispatcher-owner-unchanged true
--require-texture-pipeline-cache-owner-unchanged true
--require-texture-submission-owner-unchanged true
--require-texture-reconnection-plan true
--require-texture-unresolved-adoption-zero true
--require-texture-unregistered-fork-zero true
```

Duplicate keys, unknown keys, missing values, unexpected positionals, token adhesion, last-write-wins, and silent defaults remain forbidden.

## 15. Negative controls

R7-R2A adds at least 50 executed negative controls. The total expected count is derived from the registry, not hard-coded as authority.

Groups and required cases:

### Source identity

`SRC01` missing source, `SRC02` canonical-path mismatch, `SRC03` path traversal, `SRC04` SHA mismatch, `SRC05` byte-length mismatch, `SRC06` encoding mismatch, `SRC07` raw/normalized substitution, `SRC08` stale digest, `SRC09` wrong entrypoint, `SRC10` unregistered source mutation.

### Symbol identity

`SYM01` missing function, `SYM02` duplicate symbol, `SYM03` comment-only symbol, `SYM04` string-only symbol, `SYM05` binding mismatch, `SYM06` workgroup mismatch, `SYM07` entrypoint-signature mismatch, `SYM08` output-ABI mismatch, `SYM09` missing GQA map, `SYM10` missing `textureLoad`.

### Reuse boundary

`RUB01` unowned primitive, `RUB02` multiple owners, `RUB03` prohibited consumer, `RUB04` forbidden adaptation, `RUB05` mutation outside boundary, `RUB06` modified exact-reuse asset, `RUB07` activated reference-only asset, `RUB08` adopted rejected asset, `RUB09` alpha-scale semantics leaked, `RUB10` FFN layout treated as KV layout.

### Duplicate primitive

`DUP01` duplicate RGBA loader, `DUP02` duplicate GQA map, `DUP03` duplicate coordinate authority, `DUP04` duplicate guard classifier, `DUP05` duplicate layout-digest owner, `DUP06` duplicate dispatcher, `DUP07` duplicate pipeline cache, `DUP08` duplicate submission owner, `DUP09` duplicate output-ABI owner, `DUP10` duplicate page-LUT pattern owner.

### Active-path protection

`ACT01` route mutation, `ACT02` shader replacement, `ACT03` binding-layout mutation, `ACT04` pipeline-key mutation, `ACT05` output-ABI mutation, `ACT06` guard-policy mutation, `ACT07` submission-topology mutation, `ACT08` device-owner mutation, `ACT09` queue-owner mutation, `ACT10` hidden texture-candidate activation.

## 16. Runtime artifacts

Rust emits, at minimum:

```text
..._r7_r2a_texture_asset_registry.json
..._r7_r2a_texture_source_identities.json
..._r7_r2a_texture_symbol_identities.json
..._r7_r2a_texture_reuse_boundary_registry.json
..._r7_r2a_texture_primitive_ownership.json
..._r7_r2a_texture_duplicate_primitive_receipt.json
..._r7_r2a_texture_active_path_snapshot_before.json
..._r7_r2a_texture_active_path_snapshot_after.json
..._r7_r2a_texture_active_path_parity_receipt.json
..._r7_r2a_texture_reconnection_plan.json
..._r7_r2a_texture_binding_delta.json
..._r7_r2a_texture_parameter_delta.json
..._r7_r2a_texture_coordinate_delta.json
..._r7_r2a_negative_control_registry_extension.json
..._r7_r2a_negative_control_outcomes_extension.json
..._r7_r2a_static_checks.json
..._r7_r2a_cli_option_registry.json
..._r7_r2a_raw_cli_tokens.json
..._r7_r2a_cli_parse_receipt.json
..._r7_r2a_cli_semantic_group_receipts.json
..._r7_r2a_canonical_run_contract.json
..._r7_r2a_canonical_run_command.ps1
..._r7_r2a_runtime_artifact.json
..._r7_r2a_local_manifest.json
..._r7_r2a_verdict.json
```

No runtime output is pre-baked into the code archive.

## 17. Manifest groups

The manifest must include:

```text
binding
abi_identity
cli_contract
asset_identity
symbol_identity
reuse_boundary
duplicate_primitive
active_path_protection
reconnection_preparation
verification
```

R7-R1 groups remain parent evidence and must not be overwritten.

## 18. Promotion and HOLD rules

R7-R2A success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2A_EXISTING_TEXTURE_ASSET_ADOPTION_AND_RECONNECTION_PREPARATION_SEALED
```

This token authorizes R7-R2B work only. It does not promote a texture runtime or production route.

HOLD tokens:

```text
HOLD_..._R7_R2A_TEXTURE_SOURCE_IDENTITY_INCOMPLETE
HOLD_..._R7_R2A_TEXTURE_REUSE_BOUNDARY_AMBIGUOUS
HOLD_..._R7_R2A_DUPLICATE_TEXTURE_PRIMITIVE_PRESENT
HOLD_..._R7_R2A_ACTIVE_PRODUCTION_PATH_MUTATED_DURING_PREPARATION
HOLD_..._R7_R2A_ACTIVE_PATH_RECONNECTION_PLAN_INCOMPLETE
```

## 19. Fail-closed conditions

The gate writes diagnostic artifacts but must return HOLD or FAIL if any required source is absent, any source digest or symbol identity is invalid, a primitive has multiple or zero owners, a prohibited reuse surface is detected, an unregistered fork appears, the active route or output ABI mutates, or any negative control fails. Silent fallback is forbidden.

## 20. Completion and next stage

R7-R2A completes only when all required assets and symbols are verified, source identity is exact, all 20 primitives have one owner, duplicate and unowned counts are zero, the active path remains unchanged, the reconnection plan is complete, all negative controls pass, and Rust emits the runtime artifact and manifest.

The next revision is:

```text
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
Native KV Tensor Texture Residency Owner /
Immutable Physical Page Table /
GPU-Native RGBA4 Population /
Zero-Rebake and Zero-Host-Upload Seal
```

## 21. Final seal statement

Existing Headwise tensor-texture assets are identified by exact source identity, assigned explicit semantic roles, constrained by a single-owner reuse boundary, and verified to contain no ambiguous duplicate primitive. The active production path remains unchanged. A complete binding, parameter, coordinate, and ownership delta is emitted for the next-stage runtime reconnection. No new texture runtime, production route, or pre-baked artifact is promoted by this revision.
