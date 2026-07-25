# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B

## Native KV Tensor Texture Residency Owner / Immutable Physical Page Table / GPU-Native RGBA4 Population / Zero-Rebake / Zero-Host-Upload Seal

## 0. Document state

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2A
PATCH_CLASS=runtime-owner,texture-residency,physical-page-table,gpu-native-population,zero-rebake,zero-host-upload
DEFAULT_VERDICT=HOLD
RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
PREBAKED_RUNTIME_EVIDENCE=forbidden
PRODUCTION_ROUTE_MUTATION=forbidden
```

R7-R2B connects the existing Headwise tensor-texture assets sealed by R7-R2A to one real WGPU residency owner. It establishes distinct K and V RGBA4 texture resources, an immutable generation-aware physical page table, and a same-device GPU population path. It does not activate texture-backed production attention, GQA cluster execution, or a production route change.

## 1. Parent authority

R7-R2B inherits the R7-R2A texture asset registry, exact source identity, symbol identity, reuse-boundary registry, single-owner primitive registry, duplicate-primitive-zero receipt, active-path parity receipt, binding delta, parameter delta, coordinate delta, and reconnection plan.

The parent must be promoted and must report:

```text
source_identity_pass=true
reuse_boundary_pass=true
duplicate_primitive_zero_pass=true
duplicate_primitive_count=0
unowned_primitive_count=0
active_path_unchanged_pass=true
```

R7-R2B must not create a second Device, Queue, Headwise dispatcher, global pipeline cache, command-encoder authority, submission authority, output ABI authority, or query-head-to-KV-head mapping authority.

## 2. New runtime owners

Exactly three new owner types are allowed:

```text
HeadwiseKvTextureLayout
HeadwiseKvTexturePageTable
HeadwiseKvTextureResidency
```

Diagnostic structures and receipts may observe these owners but must not become alternative authorities.

## 3. Component revisions

```text
backend_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
model_core_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
active_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
active_route_policy_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
texture_asset_adoption_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2A
texture_residency_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
cli_contract_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
```

Cross-component revision equality is forbidden.

## 4. Canonical texture layout

The canonical baseline is:

```text
logical_dtype=f32
texture_format=rgba32float
texture_dimension=2d-array
page_tokens=128
head_dim=64
rgba_lanes=4
dimension_groups=head_dim/4
x=dimension_group
y=token_in_page
array_layer=physical_page*layers_per_physical_page+batch*kv_head_count+kv_head
```

RGBA channel ownership is exact:

```text
R=dim_group*4+0
G=dim_group*4+1
B=dim_group*4+2
A=dim_group*4+3
```

All four channels are tensor payload. Alpha metadata, alpha scale, K/V interleaving, query-head-specific K/V texture copies, and candidate-specific K/V texture copies are forbidden.

K and V must be distinct WGPU Texture and TextureView allocation identities.

## 5. Capability gate

Rust must validate the exact canonical format, texture dimension, storage binding, sampled binding preparation, mip count, sample count, array-layer capacity, and device limits. Silent fallback to rgba16float, a buffer-only result, or another texture format is forbidden.

Capability failure emits diagnostic runtime evidence and HOLD:

```text
HOLD_..._R7_R2B_CANONICAL_TEXTURE_FORMAT_OR_USAGE_UNSUPPORTED
```

## 6. Physical page table

Each page entry contains:

```text
logical_page_index
physical_page_index
token_begin
valid_token_count
generation
state
k_layer_base
v_layer_base
layout_digest
content_generation_digest
```

Required invariants:

```text
one logical page generation -> zero or one active physical page
one active physical page -> exactly one logical page generation
one sealed page generation -> immutable content_generation_digest
logical_page_multi_binding_count=0
physical_page_multi_owner_count=0
page_table_duplicate_entry_count=0
page_generation_collision_count=0
```

## 7. Page state machine

Allowed states:

```text
Vacant
PopulationPending
PopulationSubmitted
SealPending
SealedImmutable
RetirementPending
Retired
```

Allowed transitions only:

```text
Vacant -> PopulationPending
PopulationPending -> PopulationSubmitted
PopulationSubmitted -> SealPending
SealPending -> SealedImmutable
SealedImmutable -> RetirementPending
RetirementPending -> Retired
```

Write-after-seal, sealed-page repopulation, retired-page reactivation under the same generation, and publication before completion evidence are forbidden.

## 8. Tail policy

The current incomplete decode tail remains authoritative in the existing KV buffer. R7-R2B populates only complete historical pages.

```text
valid_token_count=page_tokens
```

Partial tail texture authority is not allowed in this revision.

## 9. GPU-native RGBA4 population

Population source must be a same-device native K/V buffer or a same-device GPU-generated fixture buffer. The canonical flow is:

```text
same-device source K/V buffer
-> physical page reservation
-> GPU RGBA4 pack-owner dispatch
-> distinct K and V texture stores
-> queue submission accounting
-> device completion evidence
-> content_generation_digest commit
-> SealPending
-> SealedImmutable
-> page-table digest commit
```

One invocation owns one complete RGBA texel. Lane-wise writes, atomic channel assembly, partial RGBA writes, and multi-writer texels are forbidden.

## 10. Exact zero-host contract

The following counters must remain zero:

```text
kv_texture_host_materialization_count
kv_texture_host_pack_count
kv_texture_host_upload_count
kv_texture_write_texture_count
kv_texture_host_staging_count
kv_texture_readback_reupload_count
kv_texture_serialized_payload_load_count
```

Host-created page-table metadata and small uniform descriptors are allowed and must be accounted separately from KV payload.

R7-R2B must not claim buffer-to-texture physical zero-copy. The exact claim is:

```text
same-device GPU-native population
host-copy zero
host-materialization zero
single population per immutable page generation
```

## 11. Zero-rebake contract

Rebake includes same-generation population repetition, query-head-specific copies, candidate-specific copies, route-specific copies, and measurement-epoch-specific copies.

Required zero counters:

```text
same_generation_rebake_count
query_head_specific_rebake_count
candidate_specific_rebake_count
route_specific_rebake_count
measurement_epoch_rebake_count
write_after_seal_count
stale_generation_access_count
```

A retired physical page may be reused only for a new logical page generation with an explicit generation transition and new content-generation identity.

## 12. Content identity

Texture bytes are not read back to the CPU for hashing. `content_generation_digest` is derived from:

```text
source buffer identity
source logical range
source generation
population shader revision
layout digest
destination physical page identity
submission identity
completion identity
```

It must not be named or represented as a texture byte hash.

## 13. Runtime validation lifecycle

The minimum real GPU validation performs:

```text
batch=1
kv_heads=4
head_dim=64
page_tokens=128
physical_capacity>=4
logical_pages>=3
```

Required lifecycle:

```text
logical page 0 -> physical page 0 -> generation 1 -> sealed
logical page 1 -> physical page 1 -> generation 1 -> sealed
logical page 0 -> retired
logical page 2 -> physical page 0 -> generation 2 -> sealed
```

The texture validation consumer may execute exact integer `textureLoad` without CPU content readback. Production attention, production guard, O-proj, residual, route probe, and performance candidate consumers are forbidden.

## 14. Active-path protection

Before and after snapshots must prove parity for:

```text
production route LUT
active Headwise buffer shader
active attention bind-group layout
active attention pipeline identity
output ABI
guard policy
downstream policy
submission topology
```

Required zero counters:

```text
production_route_mutation_count
active_attention_shader_replacement_count
active_attention_binding_mutation_count
active_attention_pipeline_mutation_count
active_output_abi_mutation_count
hidden_texture_consumer_count
```

## 15. CLI extension

R7-R2A strict CLI is extended with:

```text
--kv-texture-residency-policy native-immutable-page-v1
--kv-texture-layout-policy rgba4-kv-head-owned-array-v1
--kv-texture-baseline-format rgba32float
--kv-texture-page-tokens 128
--kv-texture-tail-policy buffer-authoritative-until-full-v1
--kv-texture-population-policy same-device-gpu-native-v1
--kv-texture-page-table-policy immutable-generation-mapped-v1
--kv-texture-content-identity-policy source-generation-submission-v1
--kv-texture-capacity-policy explicit-generation-rebuild-v1
--require-kv-texture-k-v-resource-separation true
--require-kv-texture-rgba4-full-payload true
--require-kv-texture-alpha-metadata-zero true
--require-kv-texture-head-dim-divisible-by-four true
--require-kv-texture-host-materialization-zero true
--require-kv-texture-host-upload-zero true
--require-kv-texture-write-texture-zero true
--require-kv-texture-readback-reupload-zero true
--require-kv-texture-same-generation-rebake-zero true
--require-kv-texture-query-head-copy-zero true
--require-kv-texture-candidate-copy-zero true
--require-kv-texture-write-after-seal-zero true
--require-kv-texture-page-table-single-owner true
--require-kv-texture-residency-single-owner true
--require-kv-texture-production-consumer-zero true
--require-kv-texture-active-route-unchanged true
--require-kv-texture-capability-exact true
--require-kv-texture-authority-commit-order true
```

Unknown keys, duplicates, missing values, unexpected positionals, token adhesion, silent defaults, and last-write-wins remain forbidden.

## 16. Negative controls

At least 80 executed controls are required, ten each for:

```text
LAY layout and RGBA packing
RES texture resource identity
PAG page-table bijection and generation
STA state transitions
GPU same-device population
REB rebake prevention
HST host-path prohibition
ACT active-path protection
```

Expected count is derived from the registry, not hard-coded as promotion authority.

## 17. Rust runtime outputs

Rust emits the texture layout, capability, resource identities, allocation accounting, page table, page transitions, population receipts, population accounting, lifecycle, generation, zero-rebake, zero-host-upload, owner identity, consumer isolation, active-path snapshots, negative controls, CLI receipts, runtime artifact, local manifest, and verdict.

No spec, manifest, artifact, receipt, verdict, runtime JSON, PowerShell script, batch script, or run-command text file is included in the code ZIP. Runtime evidence is generated only by Rust execution.

## 18. PASS requirements

All of the following are required:

```text
R7-R2A parent binding pass
layout owner count=1
page-table owner count=1
residency owner count=1
K/V resource separation pass
RGBA4 full-payload pass
alpha metadata count=0
canonical capability pass
page-table bijection pass
generation and state-order pass
GPU-native population pass
host materialization/upload/write_texture/readback-reupload=0
same-generation/query-head/candidate copies=0
write-after-seal and stale-generation access=0
production and hidden texture consumers=0
active production path unchanged
all negative controls pass
Rust artifact and manifest emitted
```

## 19. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2B_NATIVE_KV_TENSOR_TEXTURE_RESIDENCY_AND_IMMUTABLE_PAGE_TABLE_SEALED
```

This authorizes R7-R2C only. It does not promote texture-backed production attention.

Representative HOLD outcomes:

```text
HOLD_..._R7_R2B_CANONICAL_TEXTURE_FORMAT_OR_USAGE_UNSUPPORTED
HOLD_..._R7_R2B_TEXTURE_RESIDENCY_OWNER_AMBIGUOUS
HOLD_..._R7_R2B_IMMUTABLE_PHYSICAL_PAGE_TABLE_INVALID
HOLD_..._R7_R2B_HOST_MATERIALIZATION_OR_UPLOAD_DETECTED
HOLD_..._R7_R2B_IMMUTABLE_PAGE_REBAKE_DETECTED
HOLD_..._R7_R2B_TEXTURE_RESIDENCY_ESCAPED_INTO_ACTIVE_PRODUCTION_PATH
```

## 20. Next revision

```text
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C
Hybrid Buffer-Q / Immutable Texture-KV Binding /
Query-Head and KV-Head Coordinate Authority Split /
Exact Integer TextureLoad /
Buffer-Texture Raw Value and Attention Numerical Parity Seal
```
