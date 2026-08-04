
Headwise adoption remains the responsibility of `ASH-BASETRAIN-ATLAS-WAVE-02-R6`.

---

# 22. No full-model admission

The selected-layer forward stops at attention context.

Required zero counters:

```text
o_projection_dispatch_count        0
attention_residual_dispatch_count  0
post_attention_norm_dispatch_count 0
mlp_dispatch_count                 0
layer_output_publish_count         0
next_layer_dispatch_count          0
final_norm_dispatch_count          0
lm_head_dispatch_count             0
logits_publish_count               0
loss_dispatch_count                0
backward_dispatch_count            0
optimizer_step_count               0
full_model_dispatch_count          0
```

Required state:

```text
executed_layer_count      1
full_model_admission      BLOCKED
production_admission      BLOCKED
proof_ledger_admission    HOLD
r6_admission              BLOCKED
```

---

# 23. Physical gate artifacts

The gate must write a versioned runtime directory such as:

```text
workspace/runtime/basetrain/atlas_wave/02/r5_r7/selected-layer-real-forward-v1/
```

Required artifacts:

```text
00_parent_r5_r6_authority_import.json
01_parent_r5_r5_rope_authority_import.json
02_selected_layer_tensor_selection_receipt.json
03_bf16_f16_decode_authority_receipt.json
04_resident_tensor_lease_set_receipt.json
05_token_fixture_authority_receipt.json
06_actual_embedding_forward_receipt.json
07_actual_rmsnorm_forward_receipt.json
08_actual_qkv_forward_receipt.json
09_external_neox_rope_live_receipt.json
10_production_gqa_attention_receipt.json
11_cpu_f64_selected_surface_reference_receipt.json
12_gpu_cpu_selected_surface_parity_receipt.json
13_resident_lease_provenance_receipt.json
14_no_headwise_output_authority_receipt.json
15_no_full_model_admission_receipt.json
16_negative_counterfactual_ledger.json
17_selected_layer_forward_authority.json
ash_basetrain_atlas_wave_02_r5_r7_local_manifest.json
```

Every artifact must contain:

```text
schemaVersion
patchId
buildRevision
checkpointSetDigest
selectedLayer
selectedSurfaceId
receiptKind
payload
productionAdmission
proofLedgerAdmission
r6Admission
fullModelAdmission
pass
receiptDigest
```

---

# 24. Required negative counterfactual ledger

The physical gate must execute or structurally reject at least the following counterfactuals.

## 24.1 Parent identity

```text
wrong R5-R6 manifest digest
wrong checkpointSetDigest
wrong inventoryDigest
wrong R5-R5 rope authority digest
parent production admission unexpectedly enabled
```

## 24.2 Tensor selection

```text
wrong selected layer
missing Q tensor
K/V swap
shape-compatible tensor substitution
suffix-only key match
planned registry used as payload truth
```

## 24.3 Payload range

```text
absolute range start shifted by 2 bytes
absolute range end truncated
shard SHA mismatch
range escape outside shard
short read
whole-file silent fallback
```

## 24.4 Decode

```text
BF16 decoded as F16
F16 decoded as BF16
byte-swapped half
chunk reorder
zero-filled missing chunk
NaN or Inf source payload
full host tensor materialization
```

## 24.5 Residency

```text
mixed runtime holder
mixed device epoch
mixed queue epoch
mixed source weight generation
mixed atlas residency generation
mixed slot index
hardcoded layer0 group for nonzero selected layer
lease dropped before submission completion
checkpoint reopened during forward
weight rewritten during forward
```

## 24.6 Numerical convention

```text
adjacent RoPE instead of NeoX half-split
hardcoded rope_theta
wrong position IDs
MHA mapping instead of GQA
round-robin KV mapping
wrong attention scale
causal mask disabled
padding mask disabled
```

## 24.7 Authority expansion

```text
Headwise dispatch count nonzero
TensorCube dispatch count nonzero
O projection dispatch count nonzero
MLP dispatch count nonzero
next layer dispatch count nonzero
full-model admission claimed
production admission claimed
proof-ledger promotion claimed
```

Every negative case must record:

```text
counterfactual ID
mutation or substituted authority
expected rejection code
observed rejection code
pass
```

---

# 25. Failure taxonomy

Canonical error prefixes:

```text
AW02R5R7ParentR5R6*
AW02R5R7ParentR5R5*
AW02R5R7CheckpointSet*
AW02R5R7TensorSelection*
AW02R5R7TensorRange*
AW02R5R7Decode*
AW02R5R7ResidentLease*
AW02R5R7RuntimeLineage*
AW02R5R7TokenFixture*
AW02R5R7Embedding*
AW02R5R7RmsNorm*
AW02R5R7Qkv*
AW02R5R7Rope*
AW02R5R7Gqa*
AW02R5R7CpuReference*
AW02R5R7Parity*
AW02R5R7HeadwiseAuthority*
AW02R5R7FullModelAuthority*
```

Representative failures:

```text
AW02R5R7CheckpointSetDigestMismatch
AW02R5R7SelectedLayerOutOfRange
AW02R5R7SelectedTensorIdentityMismatch
AW02R5R7TensorRangeOutsideShard
AW02R5R7SourceDtypeUnsupported
AW02R5R7DecodeRuleMismatch
AW02R5R7DecodeNonFiniteValue
AW02R5R7HostFullTensorMaterializationObserved
AW02R5R7MixedResidentLineage
AW02R5R7CheckpointReopenedDuringForward
AW02R5R7LegacyAdjacentRopeActive
AW02R5R7RopePairingLayoutMismatch
AW02R5R7GqaHeadMappingMismatch
AW02R5R7PaddingExactZeroFailed
AW02R5R7SelectedSurfaceParityFailed
AW02R5R7HeadwiseDispatchObserved
AW02R5R7FullModelDispatchObserved
```

---

# 26. CLI and fixtures

Canonical args file:

```text
specs/cli/ash_basetrain_atlas_wave_02_r5_r7.args
```

Recommended arguments:

```text
--repo-root
.

--prior-r5-r6-local-manifest
workspace/runtime/basetrain/atlas_wave/02/r5_r6/checkpoint-tensor-set-authority-v1/ash_basetrain_atlas_wave_02_r5_r6_local_manifest.json

--prior-r5-r6-checkpoint-authority
workspace/runtime/basetrain/atlas_wave/02/r5_r6/checkpoint-tensor-set-authority-v1/09_checkpoint_tensor_set_authority.json

--prior-r5-r5-local-manifest
workspace/runtime/basetrain/atlas_wave/02/r5_r5/external-rope-convention-v1/ash_basetrain_atlas_wave_02_r5_r5_local_manifest.json

--selected-layer
0

--batch-size
1

--seq-len
4

--token-ids
1,328,329,336

--row-valid-lengths
4

--position-ids
0,1,2,3

--atlas-source-page-bytes
4194304

--atlas-pages-per-wave
4

--atlas-parallel-workers
4

--runtime-output-dir
