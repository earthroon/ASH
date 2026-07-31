# ASH-ATTN-HEADWISE-TEXTURE-05-R2.1

## Eligibility Predicate Decomposition /
## Hold-Before-Bail Artifact /
## Latency Percentile Disclosure /
## Worst Commit Geometry Localization /
## Generic Error Ordering Correction /
## Canonical Promotion Artifact Non-Admission /
## No Runtime Semantics Mutation /
## BufferAtlas Authority Preservation Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R2.1`  
> Build revision: `HEADWISE-TEXTURE-05-R2.1-eligibility-failure-localization-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-05-R2`  
> Parent state: `HOLD - Texture05SustainedSoakNotEligible`  
> Production executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1` unchanged  
> Output authority: `HeadwiseFullActive` unchanged

---

# 0. Purpose

The R2 gate exits on the aggregate `promotion_eligible` boolean before detailed evidence is written. R2.1 decomposes that decision into deterministic leaf predicates, records diagnostics before returning, and replaces the opaque error with a typed HOLD containing the exact failed predicates.

Canonical flow:

```text
supervisor evidence
  -> sustained soak receipt
  -> nine leaf predicates
  -> p50 / p95 / p99 / max disclosure
  -> worst five commit ranking
  -> eligibility breakdown receipt
  -> gate disposition receipt
  -> atomic artifact write
  -> readback digest verification
  -> Promote or typed HOLD
```

A HOLD remains a HOLD. This patch does not change thresholds, workload geometry, runtime authority, queue ordering, shaders, or candidate output semantics.

---

# 1. Scope

## In scope

```text
Promotion predicate decomposition
Deterministic false-predicate ordering
p50 / p95 / p99 / max latency disclosure
Exact route / generation / seq_q / seq_kv attribution
Worst five commit ranking
Diagnostic write before non-zero HOLD exit
Atomic write and readback SHA-256 verification
Canonical promotion artifact non-admission on HOLD
Existing Promote path preservation
```

## Out of scope

```text
Persistent atlas slot reuse
Incremental texture append adoption
Snapshot or scratch pooling
Fence-aware retirement
Allocator or DX12 heap telemetry
Latency or residency budget changes
Coverage matrix changes
Q/K/V source changes
Candidate output promotion
TensorCube texture consumption
```

---

# 2. Decision SSOT

```rust
pub struct HeadwiseTextureEligibilityBreakdownReceipt {
    pub predicate_results: Vec<HeadwiseTextureEligibilityPredicateResult>,
    pub false_predicate_ids: Vec<HeadwiseTextureEligibilityPredicateId>,
    pub first_false_predicate: Option<HeadwiseTextureEligibilityPredicateId>,
    pub latency_p50_ns: u64,
    pub latency_p95_ns: u64,
    pub latency_p99_ns: u64,
    pub latency_max_ns: u64,
    pub worst_commits: Vec<HeadwiseTextureWorstCommitRecord>,
    pub disposition: HeadwiseTextureGateDisposition,
    pub canonical_promotion_artifact_write_admitted: bool,
    pub receipt_digest: String,
}
```

Compatibility invariant:

```text
soak_receipt.promotion_eligible
==
(disposition == Promote)
```

Mismatch fails closed with `Texture05R21EligibilityDecisionParityMismatch`.

---

# 3. Canonical predicate order

```rust
pub enum HeadwiseTextureEligibilityPredicateId {
    CoverageComplete,
    HealthyCommitCount,
    MaximumHealthyStreak,
    LatencyP95WithinBudget,
    LatencyP99WithinBudget,
    ResidencyAllSamplesWithinBudget,
    ResidencyPlateauWithinBudget,
    ShadowDisableReceiptPresent,
    BufferAtlasContinuityPass,
}
```

Enum declaration order is authoritative. Hash-map order, discovery order, JSON key order, and lexical sorting are forbidden.

```text
false predicate count == 0  -> Promote
false predicate count > 0   -> Hold
```

Typed HOLD:

```text
Texture05EligibilityHold:<Reason1>,<Reason2>,...
```

---

# 4. Timing observation authority

Each healthy commit preserves one exact timing observation binding:

```text
commit ordinal
committed generation
route
coverage key
batch / Q head / KV head geometry
exact seq_q / seq_kv
head dimension / page tokens
total shadow GPU ns
timing receipt digest
live shadow receipt digest
observation digest
```

Required parity:

```text
timing observation count == timing receipt count
observation generation == timing generation
observation duration == timing duration
observation timing digest == timing receipt digest
coverage key == classify(route, seq_q, seq_kv)
```

Worst commit ordering:

```text
total_shadow_gpu_ns descending
commit_ordinal ascending for ties
committed_generation ascending for remaining ties
```

Ranked count is `min(sample_count, 5)`. Percentiles use the existing nearest-rank implementation.

---

# 5. HOLD-before-bail ordering

Forbidden:

```rust
ensure!(soak_receipt.promotion_eligible, "Texture05SustainedSoakNotEligible");
```

Required semantic order:

```text
seal
  -> evaluate eligibility
  -> build ten diagnostic payloads
  -> atomically write and readback verify
  -> write artifact_write_receipt as the eleventh artifact
  -> verify canonical promotion paths
  -> branch on disposition
```

On HOLD:

```text
canonical Texture-05 runtime artifact write       0
canonical Texture-05 local manifest write         0
candidate readiness promotion                      forbidden
existing canonical files                           byte-identical
process exit                                       non-zero
```

On Promote, existing canonical runtime and manifest paths and PASS semantics remain unchanged.

---

# 6. Diagnostic outputs

```text
workspace/runtime/attention/headwise/texture/05/diagnostic/
  eligibility_breakdown.json
  latency_ranked_commits.json
  gate_disposition_receipt.json
  artifact_write_receipt.json
```

Required eleven-artifact set:

```text
coverage_matrix
latency_summary
residency_summary
quarantine_ledger
shadow_disable_receipt
bufferatlas_continuity_receipt
sustained_soak_receipt
eligibility_breakdown
latency_ranked_commits
gate_disposition_receipt
artifact_write_receipt
```

Every entry binds semantic ID, path, byte count, SHA-256, and readback verification state. Writes use a temporary sibling file followed by atomic rename.

---

# 7. Runtime authority preservation

Required zero counters:

```text
new GPU buffers
new GPU textures
new GPU query sets
new queue submissions
payload readbacks
host uploads
host repacks
CPU payload materializations
candidate output commits
candidate downstream consumers
route authority mutations
output authority mutations
physical executor switches
TensorCube texture consumers
```

R2.1 adds CPU metadata and JSON output only.

---

# 8. Dedicated verification gate

New binary:

```text
ash_attn_headwise_texture_05_r2_1_gate
```

It verifies:

```text
CLI registry exactness
nine predicate order and cardinality
Promote synthetic fixture
localized HOLD synthetic fixture
nearest-rank percentile disclosure
worst-five deterministic ordering
atomic artifact write and readback verification
canonical promotion path non-mutation on HOLD
production source no longer contains the generic early ensure
original 5 s / 10 s thresholds remain unchanged
original representative sequence sets remain unchanged
```

The verification binary writes through Rust:

```text
workspace/runtime/attention/headwise/texture/05/r2_1/
  ash_attn_headwise_texture_05_r2_1_runtime_artifact.json
  ash_attn_headwise_texture_05_r2_1_local_manifest.json
```

These are execution products and are excluded from the code ZIP.

---

# 9. Gate contract

```text
predicate leaf count                   9
ranked worst commit limit              5
required diagnostic artifacts         11
positive cases                        32 minimum
negative controls                     36 minimum
canonical promotion writes on HOLD     0
new GPU buffers                        0
new GPU textures                       0
new GPU query sets                     0
new queue submissions                  0
new payload readbacks                  0
candidate output commits               0
route authority mutations              0
output authority mutations             0
physical executor switches             0
TensorCube texture consumers           0
```

R2.1 PASS proves localization integrity only. It does not claim `SustainedShadowSoakBound` unless the original Texture-05 gate independently returns Promote.

---

# 10. Direct execution

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r2_1_gate -- "@specs/cli/ash_attn_headwise_texture_05_r2_1.args"
```

Original Texture-05 rerun:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected revision:

```text
HEADWISE-TEXTURE-05-R2.1-eligibility-failure-localization-v1
```

PASS token:

```text
PROMOTE_ASH_ATTN_HEADWISE_TEXTURE_05_R2_1_ELIGIBILITY_PREDICATE_DECOMPOSITION_HOLD_BEFORE_BAIL_ARTIFACT_LATENCY_PERCENTILE_DISCLOSURE_WORST_COMMIT_GEOMETRY_LOCALIZATION_GENERIC_ERROR_ORDERING_CORRECTION_CANONICAL_PROMOTION_ARTIFACT_NON_ADMISSION_NO_RUNTIME_SEMANTICS_MUTATION_BUFFERATLAS_AUTHORITY_PRESERVATION_SEALED
```

---

# 11. Completion state

```text
Texture-05 implementation
  EligibilityFailureLocalized

Texture-05 performance state
  Promote or Hold, determined by the original gate rerun

BufferAtlasV1
  ProductionActive
  UninterruptedAuthority

KvTextureGqa4V1
  LiveShadowParityBound
  ProductionOutputCommitForbidden
```

R3 consumes the R2.1 eligibility breakdown receipt digest as parent failure evidence.