# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C

## Hybrid Buffer-Q / Immutable Texture-KV Binding / Query-Head and KV-Head Coordinate Authority Split / Exact Integer TextureLoad / Buffer-Texture Raw Value and Attention Numerical Parity Seal

## 0. Document state

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
PATCH_CLASS=hybrid-binding,coordinate-authority,texture-consumer,raw-value-parity,attention-numerical-parity,shadow-validation
DEFAULT_VERDICT=HOLD
RUNTIME_ARTIFACT_AUTHORITY=Rust-only
MANIFEST_AUTHORITY=Rust-only
PRODUCTION_ROUTE_MUTATION=forbidden
PREBAKED_RUNTIME_EVIDENCE=forbidden
```

R7-R2C connects the R7-R2B immutable K/V texture residency to a real shadow attention consumer. Q remains the existing same-device storage buffer. K and V are read from distinct immutable RGBA4 tensor textures. The revision proves exact coordinate authority, exact integer texture fetch, raw buffer-texture parity, and attention numerical parity while keeping the production route unchanged.

## 1. Parent requirements

R7-R2C requires the promoted R7-R2B artifact and manifest. The parent must report successful texture capability, immutable page-table ownership, same-device GPU population, zero host upload, zero same-generation rebake, consumer isolation, and active-path parity.

R7-R2C must not introduce a new Device, Queue, dispatcher, global pipeline cache, output ABI authority, route authority, or independent GQA mapping authority.

## 2. Component revisions

```text
backend_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
model_core_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R6-R1
active_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
active_route_policy_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7
texture_residency_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2B
hybrid_texture_binding_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C
cli_contract_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2C
```

Cross-component revision equality is forbidden.

## 3. Canonical hybrid binding

```text
Q=same-device read-only storage buffer
K=R7-R2B immutable texture_2d_array<f32>
V=R7-R2B immutable texture_2d_array<f32>
page table=read-only storage buffer
reference output=dedicated native shadow scratch
candidate output=dedicated native shadow scratch
parity decision=device-native compact decision buffer
```

The K/V payload path must have zero sampler bindings. Existing sampled math LUT policy remains a separate domain and must not be confused with tensor-payload texture policy.

## 4. Canonical shape and validation matrix

```text
batch=1
q_heads=32
kv_heads=4
query_heads_per_kv=8
head_dim=64
page_tokens=128
sealed logical pages=3

validation shapes:
seq_q=1, seq_kv=128
seq_q=2, seq_kv=256
seq_q=8, seq_kv=384
```

The three shapes must execute independently and produce separate parity receipts.

## 5. Query-head and KV-head authority

The authoritative mapping is:

```text
kv_head=query_head/query_heads_per_kv
```

Required boundary cases:

```text
q_head 0  -> kv_head 0
q_head 7  -> kv_head 0
q_head 8  -> kv_head 1
q_head 15 -> kv_head 1
q_head 16 -> kv_head 2
q_head 23 -> kv_head 2
q_head 24 -> kv_head 3
q_head 31 -> kv_head 3
```

The mapping must be derived from runtime metadata. A texture-specific hard-coded GQA map is forbidden.

## 6. Page and texture coordinate authority

```text
logical_page=kv_position/page_tokens
token_in_page=kv_position%page_tokens
physical_page=physical_page_lut[logical_page]
array_layer=physical_page*layers_per_physical_page+batch*kv_head_count+kv_head
texel_x=dimension/4
rgba_lane=dimension%4
texel_y=token_in_page
mip=0
```

The physical page must be sealed, generation-valid, and layout-digest-compatible. Stale generation, stale view, non-sealed page, valid-token overflow, or reconstructed linear fallback addressing must fail closed.

## 7. Exact tensor fetch policy

K/V payload fetch must use only:

```wgsl
textureLoad(texture, vec2<i32>(dimension_group, token_in_page), array_layer, 0)
```

Forbidden on K/V payload:

- `textureSample` or `textureSampleLevel`;
- sampler arguments;
- normalized or fractional coordinates;
- filtering;
- nonzero mip levels;
- sRGB formats;
- partial RGBA fetch or alpha metadata semantics.

All R, G, B, and A lanes are tensor payload and must be consumed.

## 8. Raw buffer-texture parity

The reference surface is the same-device K/V source buffer used by the residency population path. The candidate surface is the immutable K/V texture.

The GPU raw-parity comparator must cover all sealed logical pages, all batches, all KV heads, all valid tokens, all dimensions, and all RGBA lanes.

For the rgba32float baseline, finite values require bitwise equality. `+0.0` and `-0.0` are distinct. Tensor payload readback is forbidden. Only compact mismatch counters and first-fault coordinates may be read back.

Required results:

```text
raw_k_bit_mismatch_count=0
raw_v_bit_mismatch_count=0
payload_readback_count=0
```

## 9. Attention reference and candidate

Reference:

```text
same-device Q buffer
same-device K/V source buffers
operation-order-preserving attention
```

Candidate:

```text
same-device Q buffer
immutable K/V texture views
R7-R2B physical page LUT
exact integer textureLoad
same operation order
```

Reference and candidate must share scale, causal visibility, Q identity, logical K/V values, GQA mapping, output shape, and arithmetic order.

## 10. Arithmetic order

R7-R2C changes only the K/V load surface and coordinate resolution. It must not introduce cluster grouping, subgroup reduction, shared-memory KV tiling, softmax-strategy changes, score-reduction reordering, V-accumulation reordering, fast-math policy changes, or tolerance widening.

For incremental visibility:

```text
visible_kv_count=seq_kv-seq_q+q_position+1
```

Reference and candidate must use the same visibility rule.

## 11. Attention parity stages

The gate records bitwise parity for:

```text
score
row maximum
denominator
normalized probability
final attention output
```

Required counters:

```text
score_bit_mismatch_count=0
row_max_bit_mismatch_count=0
denominator_bit_mismatch_count=0
probability_bit_mismatch_count=0
output_bit_mismatch_count=0
```

No silent epsilon or tolerance policy is allowed. If identical logical inputs and preserved arithmetic order do not produce bitwise parity, the verdict is HOLD and a separate tolerance-policy revision is required.

## 12. GPU comparison and readback policy

Reference and candidate tensors remain GPU-resident. The comparator executes on GPU and emits only compact atomic mismatch counters and first-fault linear indices.

Allowed readback:

```text
compact decision token
aggregate mismatch counts
first-fault index
```

Forbidden readback:

```text
Q tensor
K tensor
V tensor
score matrix
probability matrix
attention output tensor
```

## 13. Generation lock

During one validation run, the following identities are immutable:

```text
residency generation
page-table generation
layout digest
K texture view identity
V texture view identity
```

Required zero counters:

```text
mid_validation_generation_switch_count
stale_page_table_binding_count
stale_texture_view_binding_count
page_retirement_during_validation_count
```

## 14. Shadow isolation

The candidate writes only to dedicated shadow scratch. It must never commit into production output, production guard, O-projection, residual, decode output, route probes, or performance promotion surfaces.

Required zero counters:

```text
candidate_output_commit_count
production_consumer_count
hidden_texture_consumer_count
active_route_mutation_count
```

## 15. Active-path protection

Before and after snapshots must prove unchanged identity for:

- active Headwise dispatcher source;
- active buffer attention shader;
- production route identity;
- output ABI identity;
- parent artifact and manifest bindings.

R7-R2C does not promote a production texture route.

## 16. CLI extension

R7-R2B strict CLI is extended with:

```text
--hybrid-texture-binding-policy buffer-q-immutable-texture-kv-v1
--hybrid-texture-coordinate-policy split-qhead-kvhead-page-lut-v1
--hybrid-texture-fetch-policy exact-integer-textureload-v1
--hybrid-texture-parity-policy gpu-bitwise-f32-v1
--hybrid-texture-validation-surface shadow-only-v1
--hybrid-texture-page-generation-policy locked-per-validation-v1
--hybrid-texture-reference-policy active-buffer-headwise-v1
--hybrid-texture-arithmetic-policy operation-order-preserving-v1
--hybrid-texture-output-policy dedicated-native-shadow-scratch-v1
--hybrid-texture-decision-policy device-native-compact-token-v1
```

Required booleans:

```text
--require-hybrid-q-buffer-identity true
--require-hybrid-k-texture-identity true
--require-hybrid-v-texture-identity true
--require-hybrid-qhead-kvhead-map-exact true
--require-hybrid-page-table-generation-lock true
--require-hybrid-integer-textureload true
--require-hybrid-kv-sampler-zero true
--require-hybrid-kv-normalized-coordinate-zero true
--require-hybrid-kv-filtering-zero true
--require-hybrid-kv-mipmap-zero true
--require-hybrid-rgba4-full-consumption true
--require-hybrid-raw-bitwise-parity true
--require-hybrid-score-bitwise-parity true
--require-hybrid-softmax-bitwise-parity true
--require-hybrid-output-bitwise-parity true
--require-hybrid-payload-readback-zero true
--require-hybrid-production-consumer-zero true
--require-hybrid-active-route-unchanged true
--require-hybrid-candidate-output-commit-zero true
--require-hybrid-first-fault-capture true
```

Unknown, duplicate, missing, adhered, silently defaulted, or last-write-wins CLI keys remain forbidden.

## 17. Negative controls

At least 100 executed controls are required, ten each for:

```text
BND binding
GQA mapping
CRD page coordinates
TEX texture access
RAW raw parity
ATT attention parity
ISO consumer isolation
GEN generation lock
RDB readback prohibition
ACT active-path protection
```

Expected count must be derived from the registry.

## 18. Runtime outputs

Rust emits binding, parameter ABI, coordinate authority, raw K/V parity, per-shape attention parity, generation lock, shadow isolation, payload-readback-zero, active-path snapshots, negative-control outcomes, CLI receipts, runtime artifact, local manifest, and verdict.

The code ZIP must not contain specs, scripts, manifest, artifact, receipt, verdict, runtime JSON, or run-command files. Runtime evidence is generated only by Rust execution.

## 19. PASS requirements

```text
R7-R2B parent binding pass
Q buffer identity pass
K texture identity pass
V texture identity pass
GQA mapping pass
page-coordinate authority pass
exact integer textureLoad pass
K/V sampler count=0
normalized-coordinate count=0
filtering count=0
nonzero-mip count=0
RGBA4 full consumption pass
raw K/V mismatch count=0
score mismatch count=0
row-max mismatch count=0
denominator mismatch count=0
probability mismatch count=0
output mismatch count=0
payload readback count=0
candidate output commit count=0
hidden production consumer count=0
generation lock pass
active production path unchanged
all negative controls pass
Rust artifact and manifest emitted
```

## 20. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2C_HYBRID_BUFFER_Q_IMMUTABLE_TEXTURE_KV_BINDING_AND_NUMERICAL_PARITY_SEALED
```

Representative HOLD outcomes:

```text
HOLD_..._R7_R2C_HYBRID_BUFFER_TEXTURE_BINDING_INVALID
HOLD_..._R7_R2C_QUERY_HEAD_KV_HEAD_OR_PAGE_COORDINATE_AUTHORITY_INVALID
HOLD_..._R7_R2C_BUFFER_TEXTURE_RAW_VALUE_PARITY_INCOMPLETE
HOLD_..._R7_R2C_ATTENTION_BITWISE_PARITY_INCOMPLETE
HOLD_..._R7_R2C_TEXTURE_PAGE_GENERATION_CHANGED_DURING_VALIDATION
HOLD_..._R7_R2C_SHADOW_TEXTURE_CONSUMER_ESCAPED_INTO_PRODUCTION_PATH
```

## 21. Fail-closed rules

The gate must not silently replace a failed texture candidate with a buffer candidate, reconstruct page addresses after a page-table failure, use modulo GQA fallback, widen tolerance after parity failure, perform CPU tensor parity, or commit candidate output into production.

## 22. Rollback

Rollback removes the R7-R2C hybrid candidate, parity comparators, shadow scratch, and CLI extension while preserving R7-R2B residency, immutable K/V textures, page table, and the active R7 buffer route.

## 23. Next revision

```text
ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2D
RGBA Texture GQA4 Parallel Cluster Kernel /
Shared KV Tile Population /
Four Query-Head Concurrent Consumption /
Kernel-Only Numerical and Structural Validation Seal
```

## 24. Final seal statement

The existing same-device Q buffer was bound with immutable K and V RGBA4 tensor textures. Query-head, KV-head, logical-page, physical-page, array-layer, texel, and RGBA-lane coordinates were resolved through one explicit authority chain. K/V payloads were fetched only through exact integer textureLoad. Raw buffer-texture values and operation-order-preserving attention surfaces were compared on GPU without tensor payload readback. The hybrid candidate remained shadow-only and did not alter the active production path.
