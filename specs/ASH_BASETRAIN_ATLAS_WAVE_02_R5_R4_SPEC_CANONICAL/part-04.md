| RMSNorm | `T × H` | `T × H` | bounded float |
| Q | `T × QW` | `T × QW` | bounded float |
| K | `T × KW` | `T × KW` | bounded float |
| V | `T × KW` | `T × KW` | bounded float |
| Q_RoPE | `T × QW` | `T × QW` | bounded float |
| K_RoPE | `T × KW` | `T × KW` | bounded float |
| Context | `T × H` | `T × H` | bounded float |

Existing tolerance values may be retained only after cardinality correction and physical GPU observation.

Every parity receipt must record failures before final admission.

R5-R4 does not requalify the global R5 proof ledger. Its parity records are R5-R4-specific physical evidence.

---

# 18. Padding exact-zero validation

Padding validation must accept a logical width per surface.

Required width map:

```text
Q         QW
K         KW
V         KW
Q_RoPE    QW
K_RoPE    KW
Context   H
```

For every padded token and every logical lane:

```text
value.to_bits() == 0x00000000
```

The validator must not assume every surface length equals `T × H`.

Required receipt fields:

```text
surface_id
logical_width
padded_token_count
checked_scalar_count
negative_zero_count
nonzero_count
first_violation
pass
```

---

# 19. Live handoff geometry

The R5-R4 live handoff must preserve unequal Q/K/V buffer geometry.

Required handoff metadata:

```rust
pub struct BaseTrainAtlasWave02R5R4LiveGeometryReceipt {
    pub geometry_digest: String,
    pub q_shape: [u32; 3],
    pub k_shape: [u32; 3],
    pub v_shape: [u32; 3],
    pub context_shape: [u32; 3],
    pub q_stride: u32,
    pub kv_stride: u32,
    pub q_heads_per_kv: u32,
    pub mapping_digest: String,
    pub q_logical_bytes: u64,
    pub k_logical_bytes: u64,
    pub v_logical_bytes: u64,
    pub runtime_holder_id: String,
    pub device_epoch: u64,
    pub queue_epoch: u64,
    pub source_weight_generation: u64,
    pub atlas_residency_generation: u64,
    pub receipt_digest: String,
}
```

Required shapes for the fixture:

```text
Q       [2, 4, 16]
K       [2, 4, 8]
V       [2, 4, 8]
Context [2, 4, 16]
```

The live buffer lease must not infer K/V size from Q size.

TensorCube Stage10 remains blocked in R5-R4.

---

# 20. New receipts

R5-R4 must publish at least these artifacts under its own runtime directory:

```text
workspace/runtime/basetrain/atlas_wave/02/r5_r4/
```

Required artifacts:

```text
00_parent_r5_r3_physical_pass_import.json
01_gqa_fixture_profile_receipt.json
02_gqa_model_spec_source_receipt.json
03_gqa_header_geometry_receipt.json
04_gqa_geometry_authority_receipt.json
05_q_to_kv_mapping_receipt.json
06_resident_qkv_shape_receipt.json
07_gpu_buffer_cardinality_receipt.json
08_dispatch_geometry_receipt.json
09_qkv_projection_receipt.json
10_rope_unequal_width_receipt.json
11_attention_mapping_receipt.json
12_cpu_f64_gqa_reference_receipt.json
13_stage_parity_receipt.json
14_mapping_counterfactual_rejection_receipt.json
15_padding_exact_zero_receipt.json
16_live_handoff_geometry_receipt.json
17_mutation_firewall_receipt.json
18_admission_manifest.json
```

Artifact count must be derived from the physically published set.

---

# 21. Receipt requirements

Every R5-R4 receipt must include:

```text
schemaVersion
patchId
buildRevision
parentGeometryDigest
profileDigest
checkpointIdentityDigest
checkpointHeaderDigest
modelSpecDigest
runtimeHolderId
deviceEpoch
queueEpoch
sourceWeightGeneration
atlasResidencyGeneration
executorCallsiteId
fallbackCount
pass
receiptDigest
```

Receipts concerning a GPU stage must additionally include:

```text
shaderModuleDigest
pipelineIdentityDigest
bindGroupLayoutDigest
inputBufferIdentityDigests
residentWeightAddressDigests
outputBufferIdentityDigests
logicalScalarCounts
logicalByteCounts
dispatchDimensions
queueSubmissionSerial
readbackByteCount
```

Empty input identity arrays are not admitted for QKV, RoPE, or attention.

---

# 22. Physical positive controls

R5-R4 must execute and record these positive assertions.

```text
POS-GQA-001 profile kind is SyntheticGqaFixture
POS-GQA-002 query head count is 4
POS-GQA-003 KV head count is 2
POS-GQA-004 Q/KV head counts are unequal
POS-GQA-005 q_heads_per_kv is 2
POS-GQA-006 Q projection width is 16
POS-GQA-007 KV projection width is 8
POS-GQA-008 Q resident shape is [16,16]
POS-GQA-009 K resident shape is [8,16]
POS-GQA-010 V resident shape is [8,16]
POS-GQA-011 Q output bytes are 512
POS-GQA-012 K output bytes are 256
POS-GQA-013 V output bytes are 256
POS-GQA-014 Q_RoPE bytes are 512
POS-GQA-015 K_RoPE bytes are 256
POS-GQA-016 mapping table is [0,0,1,1]
POS-GQA-017 Q/K/V projection parity passes
POS-GQA-018 Q/K RoPE parity passes
POS-GQA-019 context parity passes
POS-GQA-020 modulo counterfactual is rejected
POS-GQA-021 changed mapping heads are exactly {1,2}
POS-GQA-022 padded Q/K/V/context are positive zero
POS-GQA-023 live handoff preserves Q/KV unequal widths
POS-GQA-024 host K/V expansion count is zero
POS-GQA-025 TensorCube Stage10 dispatch count is zero
POS-GQA-026 loss dispatch count is zero
POS-GQA-027 backward dispatch count is zero
POS-GQA-028 optimizer dispatch count is zero
POS-GQA-029 production admission is false
POS-GQA-030 RoPE external convention remains unbound
```

These are R5-R4-specific assertions. They do not count toward requalification of the stale global R5 proof ledger.

---

# 23. Negative controls

R5-R4 must include distinct negative mutations that exercise the physical GQA boundary.

## 23.1 Geometry mutations

```text
NEG-GQA-GEOM-001 num_key_value_heads = 0
