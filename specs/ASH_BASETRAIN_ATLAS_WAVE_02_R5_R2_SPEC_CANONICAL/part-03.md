Current validation requires both:

```text
hidden_size == num_heads * head_dim
hidden_size == num_kv_heads * head_dim
```

and requires Q, K and V all to have shape:

```text
[hidden_size, hidden_size]
```

This forces `num_kv_heads == num_heads` and therefore proves only MHA.

A GQA model requires:

```text
Q rows = num_heads * head_dim
K rows = num_kv_heads * head_dim
V rows = num_kv_heads * head_dim
```

R5 production admission remains blocked until this is explicit.

## 15.3 RoPE convention is unbound

The current CPU and GPU implementations can agree with each other while both disagree with the checkpoint architecture.

Required future authority:

```text
checkpoint architecture/config digest
  -> RopePairingConvention
  -> CPU independent reference
  -> GPU implementation
```

At minimum:

```rust
pub enum RopePairingConvention {
    SplitHalf,
    Interleaved,
}
```

must become an explicit model-bound value.

---

# 16. Mandatory successor order

The prior plan that placed physical counters immediately after lineage is superseded.

The corrected order is:

```text
R5-R2  overlay lineage and stale receipt closure
  ->
R5-R3  checkpoint/header -> ModelSpec -> Params tensor geometry authority
  ->
R5-R4  GQA projection shape and KV stride closure
  ->
R5-R5  RoPE convention and independent external reference
  ->
R5-R6  physical runtime event counters
  ->
R5-R7  failure-recordable proof ledger
  ->
R5-R8  distinct negative mutation matrix
  ->
R5-R9  repository-wide WGSL inventory and legacy quarantine
  ->
R5-R10 artifact publication and repair-script purity
  ->
R5-R11 evidence requalification
  ->
AW-02-R6 Headwise training adapter
```

R5-R2 PASS must not unlock R6.

---

# 17. Next patch definitions

## 17.1 Immediate next patch

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3

Checkpoint Model Geometry Authority /
Header·Config To ModelSpec Binding /
ModelSpec-Derived Params /
Projection Shape Derivation /
Fixture Profile Explicit Isolation /
No Independent Geometry Literal /
No Production Admission Seal
```

## 17.2 Following patch

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4

GQA Query·KV Head Geometry /
Independent Q·K·V Projection Shapes /
KV Buffer Stride /
Q-Head To KV-Head Mapping /
TinyLlama Physical Profile /
No Dormant GQA Path Seal
```

## 17.3 Following patch

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5

RoPE Pairing Convention Authority /
Checkpoint Config Digest Binding /
Split-Half·Interleaved Explicit Enum /
Independent External Reference Vector /
No Self-Mirroring Parity Seal
```

---

# 18. R5-R2 admission decision

R5-R2 may emit PASS only for the following proposition:

```text
The immutable R5 and R5-R1 package lineage has been fully rehashed,
the exact R5-R1 changed-file set has been sealed,
stale receipt entries have been classified without rewriting history,
and the prior physical PASS has been separated from evidence admission.
```

It may not emit PASS for:

```text
production model geometry
GQA
RoPE convention
runtime-derived counters
proof-ledger completeness
no receipt overclaim requalification
R6 readiness
```

---

# 19. Expected PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R2_R5_R1_OVERLAY_LINEAGE_RECEIPT_IMMUTABLE_PARENT_ZIP_DIGEST_CHANGED_FILE_EXACT_SET_FULL_PACKAGE_SHA_RECALCULATION_PHYSICAL_PASS_EVIDENCE_RECLASSIFICATION_STALE_RECEIPT_REJECTION_NO_IN_PLACE_RECEIPT_MUTATION_LINEAGE_ONLY_R6_BLOCKED_SEALED
```

Required accompanying state:

```text
lineageAdmission = PASS
physicalExecution = PASS_OBSERVED
proofLedgerAdmission = HOLD
productionModelGeometry = UNPROVEN
GqaGeometry = UNPROVEN
RopeConvention = UNPROVEN
noReceiptOverclaimClaim = REVOKED_PENDING_REQUALIFICATION
r6Admission = BLOCKED
```

---

# 20. Completion state

After R5-R2 PASS:

```text
R5 physical execution
  PASS_OBSERVED

R5-R1 package lineage
  EXACT_REHASHED
  CHILD_RECEIPT_PUBLISHED

R5 parent receipt
  IMMUTABLE
  HISTORICAL
  STALE_FINDINGS_RETAINED

R5 evidence package
  HOLD

R5 production-model authority
  BLOCKED

R6 Headwise admission
  BLOCKED

Next authority patch
  ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3
```

R5-R2 closes the bookkeeping spine only.

The model-execution spine begins with R5-R3.
