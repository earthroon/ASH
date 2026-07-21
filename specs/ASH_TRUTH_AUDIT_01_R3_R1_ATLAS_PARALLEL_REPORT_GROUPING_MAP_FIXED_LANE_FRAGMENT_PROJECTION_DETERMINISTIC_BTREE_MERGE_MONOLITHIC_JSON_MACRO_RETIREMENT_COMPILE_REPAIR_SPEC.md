# ASH-TRUTH-AUDIT-01-R3-R1

## Atlas Parallel Report Grouping Map / Fixed-Lane Fragment Projection / Deterministic BTree Merge / Monolithic JSON Macro Retirement Compile Repair

## 0. Metadata

- Patch ID: `ASH-TRUTH-AUDIT-01-R3-R1`
- Parent: `ASH-TRUTH-AUDIT-01-R3`
- Runtime schema: `ash.truth_audit.01.r3.runtime_artifact.v1`
- Runtime artifact: `workspace/runtime/truth_audit/ash_truth_audit_01_r3_runtime_artifact.json`
- Failure class: compile-time `serde_json::json!` macro recursion overflow
- Evidence policy changes: forbidden
- Repository predicate changes: forbidden
- Automatic PASS or evidence promotion: forbidden

## 1. Confirmed failure

The R3 binary fails while expanding one monolithic top-level report expression:

```text
error: recursion limit reached while expanding `$crate::json_internal!`
crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
```

The failure occurs before runtime. It is not a recursive claim graph, file-system traversal, verifier loop, or digest operation.

## 2. Forbidden repair

The canonical repair must not add:

```rust
#![recursion_limit = "256"]
```

Increasing the macro recursion limit preserves the ownership defect and makes future report growth dependent on compiler configuration.

## 3. Repair objective

Replace the monolithic report macro with:

```text
completed audit computation
-> immutable AuditSnapshot
-> eleven Atlas report groups
-> four fixed parallel lanes
-> owned BTreeMap fragments
-> group and field ownership validation
-> deterministic sequential merge
-> existing fixed-width digest seal
-> existing atomic artifact promotion
```

## 4. SSOT boundary

Audit state is computed before report projection. The report is a projection and may not become the location where claims, predicates, HOLD reasons, verifier states, or the final verdict are recalculated.

Required authority chain:

```text
RepositoryAuditState
-> AuditSnapshot
-> ReportAtlasFragment set
-> merged serde_json::Value
-> sealed persisted bytes
```

## 5. Immutable AuditSnapshot

The snapshot owns the final values needed by the report:

```text
identity
verdict
repository policy
predicate counts and receipts
claim counts and receipts
verifier receipts
HOLD reasons
closure roadmap
aggregate evidence counts
LoRA and Decode physical-proof states
input and output artifact paths
```

All Atlas workers borrow the snapshot immutably.

## 6. Atlas groups

The report has exactly eleven groups:

```text
A00_IDENTITY
A01_VERDICT
A02_POLICY
A03_PREDICATES
A04_CLAIMS
A05_VERIFIERS
A06_HOLD_ROADMAP
A07_AGGREGATES
A08_PHYSICAL_PROOFS
A09_INPUT_PATHS
A10_SEAL
```

Each top-level report field has exactly one owner.

## 7. Fixed lanes

The report uses four fixed lanes:

```text
LANE_0_CORE
  A00_IDENTITY
  A01_VERDICT
  A09_INPUT_PATHS

LANE_1_GOVERNANCE
  A02_POLICY
  A03_PREDICATES

LANE_2_EVIDENCE
  A04_CLAIMS
  A05_VERIFIERS
  A07_AGGREGATES
  A08_PHYSICAL_PROOFS

LANE_3_CLOSURE
  A06_HOLD_ROADMAP
  A10_SEAL
```

Lane assignment is static SSOT. Thread scheduling and completion order do not affect ownership or merge order.

## 8. Group fragment contract

```rust
struct ReportAtlasFragment {
    group_id: ReportAtlasGroupId,
    lane_id: ReportAtlasLaneId,
    fields: BTreeMap<String, serde_json::Value>,
}
```

A lane returns owned fragments. It does not mutate a shared root map, write files, or seal the artifact.

## 9. No shared mutable report

Forbidden:

```rust
Arc<Mutex<serde_json::Map<String, Value>>>
```

Each lane builds private fragments. One sequential merger owns the final root map.

## 10. Typed repository policy

The large policy `json!` block is retired and replaced with a serializable typed receipt:

```rust
struct RepositoryPolicyReceipt {
    policy_id: String,
    required_claim_ids: Vec<String>,
    optional_claim_ids: Vec<String>,
    allowed_terminal_evidence_classes_by_claim:
        BTreeMap<String, Vec<String>>,
    required_repository_predicate_ids: Vec<String>,
    require_semantic_classifier_pass: bool,
    require_no_unknown_required_claims: bool,
    require_no_confirmed_false_required_claims: bool,
    require_lora_min1_physical_proof: bool,
    require_decode_min1_physical_proof: bool,
    aggregate_counts_are_policy_thresholds: bool,
}
```

Nested typed receipts are converted with `serde_json::to_value` rather than another large macro.

## 11. Field ownership

### A00_IDENTITY

```text
schema
patch_id
created_at_ms
```

### A01_VERDICT

```text
verdict
repository_verdict_state
semantic_classifier_pass
repository_truth_audit_pass
all_truth_checks_pass
```

### A02_POLICY

```text
repository_policy
```

### A03_PREDICATES

```text
repository_predicate_count
repository_predicate_pass_count
repository_predicate_fail_count
repository_predicate_unavailable_count
repository_failed_predicate_ids
repository_blocking_fail_count
repository_blocking_failed_predicate_ids
repository_predicate_receipt
```

### A04_CLAIMS

```text
required_claim_count
required_claim_pass_count
required_claim_hold_count
required_claim_fail_count
required_claim_unavailable_count
required_claim_contradicted_count
lineage_only_required_claim_count
structural_only_required_claim_count
promotion_eligible_claim_count
promotion_blocked_claim_count
claim_evidence_receipt
```

### A05_VERIFIERS

```text
verifier_receipt
```

### A06_HOLD_ROADMAP

```text
repository_hold_reason_count
repository_hold_reason_ids
repository_hold_reasons
repository_closure_roadmap
```

### A07_AGGREGATES

```text
direct_performed_claim_count
direct_verified_passthrough_count
computed_invariant_count
independent_verifier_invocation_count
runtime_observation_count
independent_comparator_count
negative_fixture_mutation_count
unknown_requires_review_count
confirmed_false_verification_count
lineage_only_verification_count
structural_invariant_count
independent_physical_verification_count
direct_performed_claim_repair_pass
```

### A08_PHYSICAL_PROOFS

```text
lora_min1_artifact_state
lora_min1_gate_pass
lora_min1_predicate_count
lora_min1_predicate_pass_count
lora_min1_predicate_fail_count
lora_min1_failed_predicate_ids
lora_min1_physical_proof_pass
decode_min1_physical_proof_pass
lora_min1_acceptance_receipt
```

### A09_INPUT_PATHS

```text
lora_min1_artifact
decode_min1_artifact
runtime_artifact
```

### A10_SEAL

```text
artifact_digest
```

The complete registry contains 59 unique top-level fields.

## 12. Parallel projection

`build_report_atlas_parallel` uses `std::thread::scope` and exactly four lane workers.

Each lane:

```text
receives &AuditSnapshot
builds assigned groups sequentially
returns Vec<ReportAtlasFragment>
performs no shared mutation
```

No new runtime dependency is introduced solely for report projection.

## 13. Deterministic merge

Fragments are stored in:

```rust
BTreeMap<ReportAtlasGroupId, ReportAtlasFragment>
```

Merge order is:

```text
ReportAtlasGroupId order
then fragment field-name BTreeMap order
```

Thread completion order is not authority.

## 14. Validation gates

Before merge, validation requires:

```text
group_count=11
lane_count=4
each group present exactly once
each group assigned to its registered lane
actual field set == registered field set
no field owned by two groups
no unregistered field emitted
```

Failure IDs include:

```text
REPORT_ATLAS_GROUP_COUNT_MISMATCH
REPORT_ATLAS_GROUP_MISSING
REPORT_ATLAS_DUPLICATE_GROUP
REPORT_ATLAS_LANE_OWNERSHIP_MISMATCH
REPORT_ATLAS_REQUIRED_FIELD_MISSING
REPORT_ATLAS_UNREGISTERED_FIELD_EMITTED
REPORT_ATLAS_DUPLICATE_FIELD_OWNER
```

No partial report is sealed or persisted.

## 15. Runtime diagnostics

R3 prints:

```text
report_atlas_group_count
report_atlas_lane_count
report_atlas_field_count
report_atlas_duplicate_field_count
report_atlas_missing_required_field_count
report_atlas_validation_pass
```

Expected:

```text
report_atlas_group_count=11
report_atlas_lane_count=4
report_atlas_field_count=59
report_atlas_duplicate_field_count=0
report_atlas_missing_required_field_count=0
report_atlas_validation_pass=true
```

## 16. Artifact integrity preservation

The existing R3 artifact seal remains authoritative:

```text
artifact_digest fixed-width placeholder
one pretty serialization
canonical digest computation
fixed-width digest byte patch
JSON reparse verification
temporary byte parity
temporary digest parity
atomic promotion
previous artifact restoration on failure
```

Atlas projection does not change the digest algorithm or promotion protocol.

## 17. Behavioral parity

The repair preserves:

```text
claim IDs
verifier IDs
predicate IDs
HOLD reason IDs
roadmap task IDs
repository policy semantics
repository verdict formula
LoRA and Decode accepted physical proofs
aggregate evidence counts
CLI flags
runtime artifact schema
```

The expected first runtime verdict remains `HoldExplained`, not fabricated PASS.

## 18. Expected runtime verdict

```text
HOLD_ASH_TRUTH_AUDIT_01_R3
verdict=hold
repository_verdict_state=HoldExplained
repository_truth_audit_pass=false
repository_hold_reason_ids=["HOLD_VERIFIER_RESULT_MISSING"]
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
```

Runtime evidence remains the SSOT for exact counts.

## 19. Static tests

Required:

```text
monolithic top-level report json macro absent
monolithic policy json macro absent
recursion_limit attribute absent
Atlas group variants=11
fixed lane count=4
field registry count=59
global field owners unique
lane partition covers every group once
Arc<Mutex<Map>> absent
```

## 20. Negative tests

```text
missing group fails closed
duplicate group fails closed
wrong lane ownership fails closed
missing required field fails closed
unregistered field fails closed
duplicate field owner fails closed
lane panic becomes a stage-specific error
thread completion permutation does not change semantic report
```

## 21. Implementation scope

Only:

```text
crates/lora_train/src/bin/ash_truth_audit_01_r3.rs
```

R2, LoRA MIN1, Decode MIN1, optimizer, comparator, and physical-proof code remain unchanged.

## 22. Compile command

```powershell
cargo check -p lora_train --bin ash_truth_audit_01_r3
```

## 23. Release build command

```powershell
cargo build --release -p lora_train --bin ash_truth_audit_01_r3
```

## 24. Runtime command

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r3 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-repository-predicate-receipt --print-claim-promotion-receipt --print-verifier-receipt --print-repository-hold-roadmap
```

## 25. PASS conditions

```text
R3 compiles without recursion-limit increase
AuditSnapshot is report projection SSOT
eleven groups have explicit field ownership
four scoped lane workers return owned fragments
no shared mutable root map exists
all fragments use BTreeMap
duplicate and missing fields fail closed
merge is sequential and deterministic
59 original report fields are preserved
artifact seal and promotion remain unchanged
runtime reaches HoldExplained or evidence-derived Pass
```

## 26. FAIL conditions

```text
recursion_limit is raised instead of restructuring
monolithic report json macro remains
monolithic policy json macro remains
parallel lanes mutate a shared map
later groups silently overwrite fields
completion order changes output semantics
partial Atlas output is sealed
repository policy changes to obtain PASS
LoRA or Decode physical proof is reopened
```

## 27. Canonical seal

```text
The audit computes once.
The snapshot freezes once.
The Atlas projects through fixed groups.
The lanes may run in parallel.
The merger remains sequential and deterministic.

A field has one owner.
A group has one lane.
A fragment has one identity.
A root map has one merger.

No giant json macro.
No recursion-limit camouflage.
No shared mutable report.
No completion-order authority.
No silent field overwrite.
No partial artifact promotion.

Eleven groups.
Four lanes.
Fifty-nine owned fields.
One frozen snapshot.
One deterministic report.
```