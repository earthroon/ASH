Count equality alone is insufficient.

---

# 4. Lineage model

R5-R2 must model the package chain as immutable nodes.

```text
R4 full body
  -> R5 overlay
  -> R5 full body
  -> R5-R1 overlay
  -> R5-R1 full body
  -> R5-R2 evidence overlay
  -> R5-R2 full body
```

Each edge must carry:

```text
parent artifact name
parent artifact SHA-256
child overlay name
child overlay SHA-256
child full-body name
child full-body SHA-256
exact changed-file set digest
full package tree digest
```

No edge may be inferred only from a filename.

No receipt may refer to “latest R5 body”.

All lineage identifiers must be immutable digest identities.

---

# 5. New R5-R1 overlay receipt

R5-R2 must add, not replace:

```text
ASH_BASETRAIN_ATLAS_WAVE_02_R5_R1_OVERLAY_RECEIPT.json
ASH_BASETRAIN_ATLAS_WAVE_02_R5_R1_STATIC_CHECKS.txt
```

The existing R5 receipt remains byte-identical.

## 5.1 Required receipt schema

```json
{
  "schemaVersion": "ash.basetrain.atlas_wave.02.r5.r1.overlay_lineage_receipt.v1",
  "patchId": "ASH-BASETRAIN-ATLAS-WAVE-02-R5-R1",
  "receiptProducerPatchId": "ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2",
  "parentPatchId": "ASH-BASETRAIN-ATLAS-WAVE-02-R5",
  "parentBodyArtifact": "...R5...code_baked.zip",
  "parentBodySha256": "d97aa659...",
  "overlayArtifact": "...R5-R1...overlay_baked.zip",
  "overlaySha256": "0812c3a6...",
  "childBodyArtifact": "...R5-R1...code_baked.zip",
  "childBodySha256": "efb5a6e5...",
  "changedFileCount": 3,
  "changedFiles": [],
  "changedFileSetDigest": "<derived>",
  "parentTreeFileCount": "<derived>",
  "childTreeFileCount": "<derived>",
  "childTreeManifestDigest": "<derived>",
  "inheritedStaleReceiptCount": 1,
  "childDeltaStaleReceiptCount": 2,
  "staleReceiptFindings": [],
  "physicalPassObservation": {},
  "evidenceAdmission": "HOLD",
  "pass": true,
  "passScope": "R5_R1_OVERLAY_LINEAGE_ONLY"
}
```

All counts and digests marked `<derived>` must be calculated from enumerated files at receipt-generation time.

Literal final values are forbidden.

## 5.2 Canonical serialization

The receipt must use deterministic canonical JSON.

Required:

```text
UTF-8
no BOM
stable object key ordering
stable changed-file ordering by normalized path
LF line endings
no timestamps inside digest authority
```

Human-readable timestamps may exist outside the canonical digest view.

---

# 6. Full package SHA recalculation

R5-R2 must hash every regular file in the R5-R1 full body.

A partial 27-entry recheck is insufficient.

## 6.1 Path normalization

Each package path must be normalized as:

```text
UTF-8 repository-relative path
forward slash separator
no leading ./
no duplicate separator
no parent traversal
case preserved
```

## 6.2 File manifest entry

```rust
pub struct PackageFileDigestEntry {
    pub normalized_path: String,
    pub byte_len: u64,
    pub sha256: String,
}
```

## 6.3 Full-tree digest

The canonical tree digest input must be equivalent to:

```text
for each entry ordered lexicographically by normalized_path:
    path_byte_len as fixed-width integer
    path bytes
    file_byte_len as fixed-width integer
    raw 32-byte SHA-256
```

The tree digest must not hash pretty-printed JSON text as its primary authority.

A JSON representation may be emitted as evidence after the binary canonical view is sealed.

## 6.4 Required outputs

```text
ASH_BASETRAIN_ATLAS_WAVE_02_R5_R1_FULL_PACKAGE_MANIFEST.json
ASH_BASETRAIN_ATLAS_WAVE_02_R5_R1_FULL_PACKAGE_MANIFEST.sha256
```

Required checks:

```text
all regular files enumerated
symlink count recorded
unsupported file type count == 0
path collision after normalization == 0
file hash read failure count == 0
tree digest recomputation equality == true
```

---

# 7. Stale receipt rejection

R5-R2 must distinguish three conditions.

```rust
pub enum ReceiptDigestDisposition {
    ExactCurrent,
    ExpectedParentValueChangedByDeclaredChildDelta,
    InheritedParentReceiptStale,
    UndeclaredChildMutation,
    MissingFile,
}
```

## 7.1 Exact current

The declared digest equals the current child-body file digest.

## 7.2 Expected parent value changed by declared child delta

The old receipt correctly describes the parent file, and the child overlay explicitly modifies that path.

This is not corruption, but it requires a child receipt.

## 7.3 Inherited parent receipt stale

The declared digest does not match the immutable parent body from which the child started.

This is a pre-existing lineage defect.

## 7.4 Undeclared child mutation

The child-body digest differs from the parent-body digest but the path is absent from the child overlay receipt.

This is a hard failure.

Required final admission:

```text
ExactCurrent allowed
ExpectedParentValueChangedByDeclaredChildDelta allowed only with new child receipt
InheritedParentReceiptStale retained as blocker and explicitly counted
UndeclaredChildMutation forbidden
MissingFile forbidden
```

R5-R2 lineage PASS does not erase inherited stale findings.

It records and seals them.

---

# 8. Physical PASS evidence reclassification

The following externally observed token is retained as an execution observation:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_WGPU26_WGSL_ABI_AUDIT_SAME_PROCESS_AW01_LIVE_RESIDENCY_ADOPTION_NO_HOST_WEIGHT_REUPLOAD_EXPLICIT_POSITION_ROPE_PARAMETER_BINDING_EMBEDDING_RMSNORM_QKV_ROPE_STAGE_SPLIT_CANONICAL_GPU_ORACLE_NAMING_SEPARATION_CPU_F64_FULL_NUMERICAL_PARITY_PADDING_QKV_CONTEXT_EXACT_ZERO_EXECUTED_POSITIVE_NEGATIVE_CONTROL_COUNTING_TENSORCUBE_LIVE_LEASE_HANDOFF_NO_RECEIPT_OVERCLAIM_NO_STAGE10_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER_NO_DELTA_NO_WEIGHT_WRITE_NO_CURSOR_WRITE_NO_POINTER_SWAP_NO_CHECKPOINT_WRITE_NO_ROUTE_PROMOTION_NO_DECODE_MUTATION_SEALED
```

R5-R2 must not discard the fact that the executable ran and reached this token.

It must split the token’s claims into separate dispositions.

## 8.1 Retained physical observations

```text
process exited successfully
native WGPU bootstrap succeeded
requested WGPU features were admitted
subgroup size 32 was observed
five canonical R5 shader stages executed
same-process AW-01 residency path executed
CPU-reference comparison code returned admission
padding-zero checks returned admission
TensorCube Stage10 remained sealed
loss, backward, optimizer and weight write remained sealed
```

These are retained as `PhysicalExecutionObserved`.

## 8.2 Claims placed on HOLD

```text
EXECUTED_POSITIVE_NEGATIVE_CONTROL_COUNTING
NO_RECEIPT_OVERCLAIM
repository-wide WGSL ABI cleanliness
