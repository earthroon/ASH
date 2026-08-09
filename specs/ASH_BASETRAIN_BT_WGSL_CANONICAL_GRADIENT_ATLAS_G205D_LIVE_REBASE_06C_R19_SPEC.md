# ASH-BASETRAIN-BT-WGSL-CANONICAL-GRADIENT-ATLAS-G205D-LIVE-REBASE-06C-R19

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-CANONICAL-GRADIENT-ATLAS-G205D-LIVE-REBASE-06C-R19`
- Build revision: `bt-wgsl-canonical-gradient-atlas-g205d-live-rebase-06c-r19`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-STRUCTURAL-FACTOR-HEAD-RESIDUAL-BACKWARD-06C-R18`
- Correctness ancestor: `ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-PERFORMANCE-AUTHORITY-REPAIR-06C-R16-R1`
- Next consumer: R20 device-local G205D gradient accumulation
- Proof ledger: `HOLD`

## SSOT

R19 does not calculate new model gradients. It inventories the already-admitted selected-layer parameter gradients from R14 through R18 into a zero-copy descriptor atlas keyed by canonical parameter identity, retires historical duplicate gradient authorities, replaces G205D's fixed Q/K/V host-vector production assumption with a live GPU gradient-segment descriptor contract, and hands the resulting 27-parameter, 44-lease selected-layer gradient set to R20 without accumulation, normalization, clipping, optimizer evaluation, weight mutation, checkpoint writes, or final-loss promotion.

`dInputHiddenComplete` remains a backward carrier and is explicitly excluded from the parameter-gradient atlas.

## R18 physical parent

Required parent evidence:

```text
r18_physical_parent=1
complete_selected_layer_dinput_authority=1
canonical_shared_factor_dw_tiles=6
horizon_head_dw_tiles=4
production_gradient_payload_readback=0
reproducibility_match=1
r19_handoff_ready=1
```

R19 additionally requires the R16-R1 TensorCube backward correctness authority to remain valid. Performance qualification is not a mathematical dependency.

## Selected-layer scope

R19 scope is exactly one selected decoder layer plus its four-horizon structural branch.

R19 does not claim gradients for:

- token embeddings
- final model RMSNorm
- LM head
- any bias parameter
- any other decoder layer

`canonical_selected_layer_gradient_authority=true` is permitted after R19 closes. `full_model_gradient_authority` remains false.

## Canonical parameter registry

Exactly 27 entries, in this immutable order.

### Base parameters, 9

```text
00 input_layernorm
01 self_attn_q_proj
02 self_attn_k_proj
03 self_attn_v_proj
04 self_attn_o_proj
05 post_attention_layernorm
06 mlp_gate_proj
07 mlp_up_proj
08 mlp_down_proj
```

### Structural parameters, 18

```text
09 structural_deltaq_h1
10 structural_deltaq_h2
11 structural_deltaq_h3
12 structural_deltaq_h4
13 structural_gate_h1
14 structural_gate_h2
15 structural_gate_h3
16 structural_gate_h4
17 structural_factor_hangul_presence
18 structural_factor_hangul_count
19 structural_factor_hangul_descriptor
20 structural_factor_cji18
21 structural_factor_qwlocal12
22 structural_factor_qwedge10
23 structural_horizon_head_h1
24 structural_horizon_head_h2
25 structural_horizon_head_h3
26 structural_horizon_head_h4
```

Every entry binds semantic identity, exact parameter-version identity, selected-layer identity, shape, dtype, source revision, source authority digest, finite/completion authority, and gradient-segment lineage.

All 27 entries must bind the same selected layer. R14/R15/R16/R17/R18 source outputs must also agree on that layer.

## Canonical source map

```text
input_layernorm                  -> R15
self_attn_q_proj                 -> R16
self_attn_k_proj                 -> R16
self_attn_v_proj                 -> R16
self_attn_o_proj                 -> R16
post_attention_layernorm         -> R14
mlp_gate_proj                    -> R16
mlp_up_proj                      -> R16
mlp_down_proj                    -> R16
structural_deltaq_h1..h4         -> R17
structural_gate_h1..h4           -> R17
structural_factor_* x6           -> R18
structural_horizon_head_h1..h4   -> R18
```

Historical superseded payloads may remain resident for audit but have no R19 canonical authority:

- R13 FFN dW is superseded by R16
- R13 OProj candidate is retired
- R14 OProj dW is superseded by R16
- R15 Q/K/V dW is superseded by R16

No heuristic such as newest-vector-position or newest-string revision is permitted. The source map above is explicit SSOT.

## Exact shapes

```text
input_layernorm              [2048]
self_attn_q_proj             [2048,2048]
self_attn_k_proj             [256,2048]
self_attn_v_proj             [256,2048]
self_attn_o_proj             [2048,2048]
post_attention_layernorm     [2048]
mlp_gate_proj                [5632,2048]
mlp_up_proj                  [5632,2048]
mlp_down_proj                [2048,5632]
DeltaQ H1-H4                 [2048,256]
Structural Gate H1-H4        [1,256]
Factor presence              [256,9]
Factor count                 [256,10]
Factor descriptor            [256,144]
Factor cji18                 [256,162]
Factor qwlocal12             [256,108]
Factor qwedge10              [256,90]
Horizon Head H1-H4           [523,2048]
```

Gradient dtype is F32 for all 27 entries.

## Gradient payload inventory

Base linear tiles:

```text
Q      2
K      1
V      1
OProj  2
Gate   6
Up     6
Down   2
-------
       20
```

Structural linear tiles:

```text
DeltaQ          8
Structural Gate 4
Factors         6
Horizon Heads   4
-----------------
                22
```

Therefore:

```text
linear dW tiles         = 42
RMSNorm dgamma vectors  = 2
GPU gradient leases     = 44
```

The two RMSNorm vectors remain `FULL_VECTOR` segments and are not disguised as fake matrix tiles.

## Logical scalar span

```text
base parameter scalars       = 44,044,288
structural parameter scalars =  6,516,480
total                        = 50,560,768 F32 scalars
logical F32 bytes            = 202,243,072
```

This 202,243,072-byte number is a logical descriptor span only. R19 must not allocate a contiguous 202MB gradient buffer.

## Descriptor-only canonical atlas

R19 introduces a descriptor-only runtime atlas equivalent to:

```text
R19CanonicalGradientAtlasV1 {
    selected_layer,
    parameter_entries[27],
    gradient_segments[44],
    parameter_registry_digest,
    selected_parameter_set_digest,
    atlas_digest,
}
```

The atlas owns/references existing gradient leases. It does not concatenate their contents.

Required:

```text
descriptor_atlas_authority=1
mega_gradient_buffer=0
gradient_payload_copy=0
host_gradient_concat=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
```

## Gradient segment classes

Only two segment classes are canonical:

```text
ROW_TILE
FULL_VECTOR
```

A row tile binds output-row range, input width, element count and existing lease lineage. A full vector binds element range `[0,N)` and an existing lease lineage.

For every matrix parameter, row tiles sorted by `output_row_start` must exactly cover `[0,out_rows)` with zero gaps and zero overlaps.

For both norm parameters, the vector must exactly cover 2048 elements.

## Parameter identity and version binding

Semantic identity answers which model parameter the entry represents.

Version identity answers which exact selected-layer resident/generated parameter instance produced the gradient.

Base parameter version binding uses selected-layer weight generation, weight pointer digest, decoder-block identity digest, role and shape.

Structural parameter version binding uses retained structural forward-tape identities:

- DeltaQ weight identity
- Gate weight identity
- shared Factor weight identity
- Horizon Head weight identity

No semantic/version identity collapse is allowed.

## Gradient-weight alias authority

Structural parameters retain exact weight leases, so R19 directly verifies that every structural gradient lease buffer is not the corresponding weight buffer.

For base parameters, the current R14-R16 output packets do not expose every corresponding weight lease at R19 scope. R19 therefore does not fabricate those leases or reopen the checkpoint. It explicitly inherits the upstream fail-closed/no-alias completion authority from the canonical source receipt. This inheritance is recorded per entry as receipt-backed authority.

Required final count:

```text
gradient_weight_alias_count=0
```

## Receipt-backed finite/completion authority

R19 must not rescan 50,560,768 production gradient scalars on the CPU.

Each canonical entry inherits finite and completion authority from its canonical producing revision. Missing finite/completion evidence is a hard error.

No host payload digest is used to establish gradient identity.

## Gradient lease lineage

Each segment binds metadata-derived lease lineage, including shape/length, active seam/primitive/stream identity and buffer range metadata. Pointer addresses are not portable semantic identities.

The atlas digest is constructed from deterministic descriptor metadata only, ordered by:

```text
parameter registry ordinal
-> local gradient segment ordinal
```

## `dInputHiddenComplete` boundary

R18's `dInputHiddenComplete` is preserved in `BaseTrainR19LayerOutput`, but:

```text
complete_dinput_parameter_entry_count=0
```

It is a carrier for future previous-layer reverse propagation, not a parameter gradient.

## Gradient ownership vs forward tape ownership

The final R19 atlas references exactly 44 canonical gradient leases.

R18's 54 forward/tape owner pins are a different lifetime domain and are not reinterpreted as R19 gradient ownership.

Required:

```text
gradient_lease_reference_count=44
forward_owner_pin_extension=0
```

For double-build reproducibility, the first temporary atlas is dropped immediately after digest comparison so the authoritative R19 atlas remains the sole R19-owned 44-lease descriptor set.

## G205D historical production assumptions retired

Historical G205D is fixed to Q/K/V selected groups and uses host `&[f32]` gradient bundles. Those paths remain historical probes only.

R19 publishes:

```text
BASETRAIN_G205D_FIXED_QKV_PRODUCTION_AUTHORITY=false
BASETRAIN_G205D_HOST_VECTOR_PRODUCTION_AUTHORITY=false
```

No R19 production payload may be materialized into the historical host-vector ABI.

## G205D live GPU descriptor rebase

R19 introduces a metadata-only production descriptor equivalent to:

```text
R19G205DLiveGradientBundleDescriptorV1 {
    selected_layer,
    selected_parameter_set_digest,
    parameter_count=27,
    gradient_segment_count=44,
    logical_scalar_count=50_560_768,
    atlas_digest,
    source_backward_revision,
    source_batch_lineage,
    gradient_dtype=f32,
    gradient_segments[44],
    final_loss_authority=false,
    bundle_digest,
}
```

The descriptor contains no gradient payload bytes.

## No R20 work in R19

R19 intentionally does not define or execute:

- accumulation-window admission
- microbatch ordinal accumulation
- loss-scale policy
- mean reduction
- global norm
- gradient clipping
- optimizer candidate
- optimizer state reads/writes
- weight delta materialization
- weight mutation

Required:

```text
g205d_accumulation_window_admission=0
loss_scale_assumption=0
g205d_accumulation_dispatch=0
global_norm_dispatch=0
gradient_clip_dispatch=0
optimizer_candidate=0
weight_mutation=0
```

R20 exclusively owns these authorities.

## Current gradient origin

The selected-layer gradients still originate from the deterministic upstream backward fixture chain.

R19 must preserve:

```text
final_loss_authority=0
gradient_origin_deterministic_fixture=1
```

The descriptor atlas does not relabel fixture-derived gradients as real final-loss training gradients.

## Negative canaries

R19 includes four descriptor-only negative canaries:

1. remove one of 27 canonical entries -> reject
2. duplicate one canonical semantic identity -> reject
3. create overlapping Q row tiles -> reject
4. replace a parameter version identity with stale lineage -> reject

All four must be observed rejected before final publication.

## Double-build reproducibility

Build the complete atlas twice from unchanged R18 state.

Required exact matches:

- parameter registry digest
- selected parameter-set digest
- atlas digest
- segment order

No payload copying is introduced by the second descriptor build.

## R19 output

```text
BaseTrainR19LayerOutput {
    layer_index,
    d_input_hidden_complete,
    canonical_gradient_atlas,
    g205d_live_gradient_bundle_descriptor,
    canonical_selected_layer_gradient_authority=true,
    full_model_gradient_authority=false,
    final_loss_authority=false,
    r20_handoff_ready=true,
}
```

## R20 handoff

R20 receives:

```text
27 canonical parameter identities
44 existing GPU gradient segment references
50,560,768 logical F32 scalars
selected parameter-set digest
atlas digest
source batch lineage
gradient origin class
```

R20 will own device-local transactional accumulation and related numerical policy.

## Required receipts

```text
r19_parent_r18_receipt.json
r19_scope_receipt.json
r19_parameter_registry_receipt.json
r19_parameter_identity_receipt.json
r19_base_gradient_source_receipt.json
r19_structural_gradient_source_receipt.json
r19_historical_gradient_dedup_receipt.json
r19_linear_tile_coverage_receipt.json
r19_rms_vector_coverage_receipt.json
r19_gradient_weight_alias_receipt.json
r19_gradient_lease_inventory_receipt.json
r19_descriptor_atlas_receipt.json
r19_atlas_digest_receipt.json
r19_g205d_fixed_qkv_retirement_receipt.json
r19_g205d_host_vector_retirement_receipt.json
r19_g205d_live_descriptor_rebase_receipt.json
r19_negative_canary_receipt.json
r19_reproducibility_receipt.json
r19_r20_handoff_receipt.json
bt_wgsl_canonical_gradient_atlas_g205d_live_rebase_06c_r19_final.json
```

## Receipt atlas

Eight deterministic parallel/streaming waves:

```text
Wave 0 R18 parent / scope / complete dInput
Wave 1 27-entry registry / identities
Wave 2 base sources / historical dedup
Wave 3 structural sources / source digests
Wave 4 coverage / leases / descriptor atlas
Wave 5 G205D retirement / live descriptor / R20 deferrals
Wave 6 negative canaries / reproducibility
Wave 7 R20 boundary / PASS / proof ledger
```

Required:

```text
receipt_atlas_waves=8
parallel_receipt_lane_build=1
streaming_receipt_merge=1
deterministic_receipt_merge=1
monolithic_final_json=0
```

## CLI gates

Exactly 70 R19 gates are required exactly once in runtime validation, short args, full args and resolved-args repair input:

```text
--require-bt-wgsl-r19-r18-physical-parent
--require-bt-wgsl-r19-complete-dinput-parent
--require-bt-wgsl-r19-r16r1-correctness-authority-preserved
--require-bt-wgsl-r19-selected-layer-scope
--require-bt-wgsl-r19-parameter-registry-27
--require-bt-wgsl-r19-base-parameter-registry-9
--require-bt-wgsl-r19-structural-parameter-registry-18
--require-bt-wgsl-r19-base-registry-order
--require-bt-wgsl-r19-structural-registry-order
--require-bt-wgsl-r19-parameter-semantic-identity
--require-bt-wgsl-r19-parameter-version-binding
--require-bt-wgsl-r19-weight-layout-binding
--require-bt-wgsl-r19-gradient-dtype-f32
--require-bt-wgsl-r19-linear-gradient-tiles-42
--require-bt-wgsl-r19-rms-gradient-vectors-2
--require-bt-wgsl-r19-gradient-payload-leases-44
--require-bt-wgsl-r19-logical-scalar-count-50560768
--require-bt-wgsl-r19-base-linear-r16-authority
--require-bt-wgsl-r19-post-rms-r14-authority
--require-bt-wgsl-r19-input-rms-r15-authority
--require-bt-wgsl-r19-deltaq-gate-r17-authority
--require-bt-wgsl-r19-factor-head-r18-authority
--require-bt-wgsl-r19-zero-historical-gradient-duplication
--require-bt-wgsl-r19-r13-oproj-candidate-retired
--require-bt-wgsl-r19-r15-qkv-gradient-superseded
--require-bt-wgsl-r19-r13-ffn-gradient-superseded
--require-bt-wgsl-r19-linear-tile-exact-coverage
--require-bt-wgsl-r19-zero-tile-gap
--require-bt-wgsl-r19-zero-tile-overlap
--require-bt-wgsl-r19-rms-vector-exact-coverage
--require-bt-wgsl-r19-zero-gradient-weight-alias
--require-bt-wgsl-r19-descriptor-atlas-authority
--require-bt-wgsl-r19-zero-mega-gradient-buffer
--require-bt-wgsl-r19-zero-gradient-payload-copy
--require-bt-wgsl-r19-zero-host-concat
--require-bt-wgsl-r19-zero-gradient-payload-readback
--require-bt-wgsl-r19-receipt-backed-finite-authority
--require-bt-wgsl-r19-source-authority-digest-binding
--require-bt-wgsl-r19-gradient-lease-lineage-binding
--require-bt-wgsl-r19-atlas-deterministic-digest
--require-bt-wgsl-r19-double-build-reproducibility
--require-bt-wgsl-r19-g205d-fixed-qkv-set-retired
--require-bt-wgsl-r19-g205d-host-vector-bundle-retired
--require-bt-wgsl-r19-g205d-live-descriptor-rebase
--require-bt-wgsl-r19-g205d-selected-set-digest-27
--require-bt-wgsl-r19-zero-g205d-accumulation-window-admission
--require-bt-wgsl-r19-zero-loss-scale-assumption
--require-bt-wgsl-r19-zero-g205d-accumulation-dispatch
--require-bt-wgsl-r19-zero-global-norm-dispatch
--require-bt-wgsl-r19-zero-gradient-clip-dispatch
--require-bt-wgsl-r19-zero-optimizer-candidate
--require-bt-wgsl-r19-zero-weight-mutation
--require-bt-wgsl-r19-zero-checkpoint-write
--require-bt-wgsl-r19-final-loss-authority-deferred
--require-bt-wgsl-r19-deterministic-fixture-lineage-preserved
--require-bt-wgsl-r19-zero-full-model-gradient-claim
--require-bt-wgsl-r19-zero-embedding-gradient-entry
--require-bt-wgsl-r19-zero-final-norm-gradient-entry
--require-bt-wgsl-r19-zero-lm-head-gradient-entry
--require-bt-wgsl-r19-zero-bias-gradient-entry
--require-bt-wgsl-r19-complete-dinput-not-parameter-gradient
--require-bt-wgsl-r19-gradient-lease-ownership
--require-bt-wgsl-r19-zero-forward-owner-pin-extension
--require-bt-wgsl-r19-missing-entry-negative-canary
--require-bt-wgsl-r19-duplicate-entry-negative-canary
--require-bt-wgsl-r19-overlap-negative-canary
--require-bt-wgsl-r19-stale-lineage-negative-canary
--require-bt-wgsl-r19-atlas-wave-streaming-receipt
--require-bt-wgsl-r19-zero-monolithic-final-json
--require-bt-wgsl-r19-r20-handoff-ready
```

## Expected physical summary

```text
r18_physical_parent=1
complete_dinput_parent=1
selected_layer_count=1
canonical_parameter_count=27
base_parameter_count=9
structural_parameter_count=18
linear_gradient_tile_count=42
rms_gradient_vector_count=2
gradient_payload_lease_count=44
logical_gradient_scalar_count=50560768
logical_gradient_f32_bytes=202243072
base_linear_r16_authority=1
post_rms_r14_authority=1
input_rms_r15_authority=1
deltaq_gate_r17_authority=1
factor_head_r18_authority=1
historical_gradient_duplicate_authority=0
tile_gap=0
tile_overlap=0
gradient_weight_alias=0
descriptor_atlas_authority=1
mega_gradient_buffer=0
gradient_payload_copy=0
host_gradient_concat=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
receipt_backed_finite_authority=1
atlas_digest_reproducible=1
g205d_fixed_qkv_production_authority=0
g205d_host_vector_production_authority=0
g205d_live_descriptor_rebase=1
g205d_selected_parameter_count=27
g205d_accumulation_window_admission=0
loss_scale_assumption=0
g205d_accumulation_dispatch=0
global_norm_dispatch=0
gradient_clip_dispatch=0
optimizer_candidate=0
weight_mutation=0
checkpoint_write=0
final_loss_authority=0
gradient_origin_deterministic_fixture=1
full_model_gradient_authority=0
embedding_gradient_entry_count=0
final_norm_gradient_entry_count=0
lm_head_gradient_entry_count=0
bias_gradient_entry_count=0
complete_dinput_parameter_entry_count=0
gradient_lease_reference_count=44
forward_owner_pin_extension=0
negative_canaries=4
reproducibility_runs=2
reproducibility_match=1
r20_handoff_ready=1
receipt_atlas_waves=8
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_CANONICAL_GRADIENT_ATLAS_G205D_LIVE_REBASE_06C_R19
```

The expanded runtime token additionally seals R18 physical parentage, 27 canonical identities, 44 lease coverage, historical-gradient retirement, descriptor-only zero-copy authority, G205D live descriptor rebase, deferred accumulation/optimizer boundaries, negative canaries, reproducibility, R20 handoff, streaming receipt atlas and proof-ledger HOLD.
