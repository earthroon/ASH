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
workspace/runtime/basetrain/atlas_wave/02/r5_r7/selected-layer-real-forward-v1
```

The gate may receive the same checkpoint/config/CAS inputs used by R5-R6 only to deterministically reconstruct the authority. The reconstructed checkpointSetDigest and authorityDigest must exactly equal the parent R5-R6 local manifest. Tensor keys and shard paths still come only from that reconstructed authority; independent tensor or shard overrides are forbidden.

---

# 27. Required implementation units

## base_train crate

```text
base_train_atlas_wave_02_r5_r7_selected_layer_forward_authority.rs
base_train_atlas_wave_02_r5_r7_cpu_f64_reference.rs
```

Required public APIs:

```rust
pub fn import_base_train_atlas_wave_02_r5_r6_checkpoint_authority(...)
    -> Result<BaseTrainAtlasWave02R5CheckpointTensorSetAuthority>;

pub fn select_base_train_atlas_wave_02_r5_r7_tensors(...)
    -> Result<BaseTrainAtlasWave02R5R7SelectedTensorSet>;

pub fn build_base_train_atlas_wave_02_r5_r7_cpu_f64_reference(...)
    -> Result<BaseTrainAtlasWave02R5R7CpuF64Reference>;

pub fn compare_base_train_atlas_wave_02_r5_r7_selected_surface(...)
    -> Result<BaseTrainAtlasWave02R5R7ParityReceipt>;
```

## burn_webgpu_backend crate

```text
base_train_atlas_wave_02_r5_r7_checkpoint_residency.rs
