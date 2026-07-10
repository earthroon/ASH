# ASH-TCU-K7M-B SPEC

## Title

Legacy Receipt Truth Reclassification / K6ZV Through K7L Evidence Authority Annotation / Read-Only Sidecar Overlay / No Legacy Value Rewrite No Runtime Mutation Seal

## Patch ID

```txt
ASH-TCU-K7M-B
```

## Status Target

```txt
PASS_ASH_TCU_K7M_B_LEGACY_RECEIPT_TRUTH_RECLASSIFICATION_NO_LEGACY_VALUE_REWRITE_NO_RUNTIME_MUTATION_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7M-A
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7M_A_EVIDENCE_CLASS_SSOT_NO_LEGACY_REWRITE_NO_RUNTIME_MUTATION_SEAL
```

## Required Prior Verdict

```txt
tensorcube_evidence_class_ssot_created_no_legacy_rewrite_no_runtime_mutation
```

## Purpose

K7M-B applies the K7M-A evidence vocabulary to the legacy TensorCube receipt chain from K6ZV through K7L.

K7M-B reads legacy receipts, extracts claims, identifies claim origin, assigns evidence class and authority, evaluates protected claims, writes per-receipt annotation sidecars, and writes a canonical reclassification index.

K7M-B must not rewrite legacy receipt files, change legacy boolean values, change legacy PASS or verdict markers, delete legacy files, execute GPU work, mutate runtime routes, execute rollback, create tokens, or mutate weights.

Legacy receipts remain immutable historical records. Annotation sidecars are the current evidence interpretation layer. The reclassification index is the canonical lookup SSOT.

## Current K7M-A Baseline

```txt
evidence_schema_version = ash_tensorcube_evidence_schema_v1
evidence_class_count = 8
evidence_authority_count = 7
protected_claim_count = 10
authority_mapping_complete = true
protected_claim_policy_complete = true
positive_fixture_count = 8
positive_fixture_fail_count = 0
negative_fixture_count = 11
negative_fixture_unexpected_pass_count = 0
legacy_receipt_file_count = 252
legacy_receipt_reclassification_required_next = true
legacy_receipt_rewrite_executed = false
gpu_dispatch_executed_by_k7m_a = false
gpu_readback_executed_by_k7m_a = false
runtime route mutations = false
rollback execution = false
weight mutations = false
```

## Scope

Included patch range:

```txt
ASH-TCU-K6ZV through ASH-TCU-K7L
```

Included receipt kinds:

```txt
runtime receipts
static checks receipts
verdict receipts
local manifests
route mutation receipts
activation receipts
GPU dispatch receipts
readback receipts
parity receipts
rollback receipts
operator token receipts
health and canary receipts
```

Excluded:

```txt
source code rewrite
legacy JSON rewrite
new GPU execution
new parity execution
route registry mutation
production promotion
actual rollback
weight mutation
```

## SSOT

### Reclassification Index Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_legacy_truth_reclassification_index_latest.json
```

### Annotation Registry Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_legacy_annotation_registry_latest.json
```

### Per-Receipt Annotation Directory

```txt
workspace/runtime/tensorcube/k7m_b_legacy_annotations/
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_prior_k7m_a_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_legacy_receipt_discovery_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_claim_extraction_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_reclassification_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_reclassification_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_protected_claim_downgrade_report_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_unresolved_claim_report_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_annotation_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_no_legacy_value_rewrite_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_no_runtime_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_b_verdict_latest.json
artifacts/ASH_TCU_K7M_B_LOCAL_MANIFEST.json
```

## State Ownership

K7M-B owns legacy receipt discovery, legacy claim extraction, claim origin inference, reclassification policy, per-claim annotations, per-receipt sidecars, protected claim downgrade report, unresolved claim report, annotation integrity verification, and canonical reclassification index.

K7M-B does not own legacy receipt content, legacy PASS markers, actual GPU execution or measurement, CPU/Burn parity execution, runtime route registries, tokens, actual rollback, model weights, optimizer state, or checkpoints.

## Legacy Receipt Identity

```rust
#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct TensorCubeLegacyReceiptIdentity {
    pub receipt_id: String,
    pub patch_id: String,
    pub receipt_path: String,
    pub receipt_sha256: String,
    pub receipt_status: Option<String>,
    pub receipt_verdict: Option<String>,
}
```

The receipt hash must be computed before annotation. Annotation must refer to the hash. K7M-B must never write back into the hashed legacy file.

## Claim Origin

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TensorCubeLegacyClaimOrigin {
    StaticLiteral,
    CliFlag,
    DerivedFromPriorReceipt,
    ConstructedByAudit,
    RuntimeExecutionReceipt,
    RuntimeMeasurementReceipt,
    RuntimeComparisonReceipt,
    RuntimeRegistryReceipt,
    Unknown,
}
```

## Classification Confidence

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TensorCubeClassificationConfidence {
    Exact,
    High,
    Medium,
    Low,
    Unresolved,
}
```

## Claim Annotation

```rust
#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct TensorCubeLegacyClaimAnnotation {
    pub annotation_id: String,
    pub legacy_receipt_id: String,
    pub legacy_receipt_path: String,
    pub legacy_receipt_sha256: String,
    pub patch_id: String,
    pub claim_json_pointer: String,
    pub claim_name: String,
    pub claim_value: serde_json::Value,
    pub claim_origin: TensorCubeLegacyClaimOrigin,
    pub assigned_evidence_class: TensorCubeEvidenceClass,
    pub assigned_authority: TensorCubeEvidenceAuthority,
    pub original_claim_preserved: bool,
    pub classification_reason: String,
    pub classification_confidence: TensorCubeClassificationConfidence,
    pub protected_claim: Option<TensorCubeProtectedClaim>,
    pub protected_claim_policy_satisfied: bool,
    pub source_execution_id: Option<String>,
    pub source_receipt_ids: Vec<String>,
    pub source_dispatch_digest: Option<String>,
    pub source_readback_digest: Option<String>,
    pub source_registry_epoch: Option<u64>,
    pub source_registry_hash: Option<String>,
    pub unresolved_runtime_owner: bool,
    pub requires_k7m_c_execution_binding: bool,
    pub evidence_schema_version: String,
}
```

## Reclassification Policy

### Static literal or policy field

```txt
origin = StaticLiteral
evidence_class = StaticContract
authority = ContractOnly
```

### CLI flag or requested action

```txt
origin = CliFlag
evidence_class = DeclaredIntent
authority = IntentOnly
```

### Prior receipt status or copied field

```txt
origin = DerivedFromPriorReceipt
evidence_class = DerivedReceipt
authority = DerivedOnly
source_receipt_ids is not empty
```

### Audit-constructed claim without execution evidence

```txt
origin = ConstructedByAudit
evidence_class = DerivedReceipt
authority = DerivedOnly
protected_claim_policy_satisfied = false
requires_k7m_c_execution_binding = true
```

### GPU execution receipt with valid source evidence

```txt
origin = RuntimeExecutionReceipt
evidence_class = ExecutedGpu
authority = Executed
source_execution_id is present
source_dispatch_digest is present
```

### GPU readback receipt with valid source evidence

```txt
origin = RuntimeMeasurementReceipt
evidence_class = MeasuredReadback
authority = Measured
source_execution_id is present
source_readback_digest is present
```

### CPU/Burn comparison receipt with measured source

```txt
origin = RuntimeComparisonReceipt
evidence_class = ComparedAgainstCpu or ComparedAgainstBurn
authority = Compared
```

### Route mutation receipt with epoch and hash

```txt
origin = RuntimeRegistryReceipt
evidence_class = RuntimeRouteMutation
authority = RuntimeMutated
source_registry_epoch is present
source_registry_hash is present
```

### Unknown or insufficient origin

```txt
origin = Unknown
evidence_class = DerivedReceipt
authority = DerivedOnly
classification_confidence = Unresolved
protected_claim_policy_satisfied = false
```

Unknown claims must never be silently upgraded.

## Protected Claims

K7M-B must inspect:

```txt
native_wgpu_dispatch_executed
gpu_output_measured
cpu_parity_passed
burn_parity_passed
default_route_mutated
user_visible_route_mutated
production_route_mutated
runtime_decode_output_changed
assistant_message_output_changed
actual_rollback_executed
```

If a protected claim lacks required evidence, the original value remains unchanged while its annotation authority is downgraded and `requires_k7m_c_execution_binding=true`.

`runtime_decode_output_changed` and `assistant_message_output_changed` remain DerivedOnly and unresolved unless accepted runtime owner evidence exists.

## Discovery

K7M-B must discover receipts by known patch range, known runtime receipt directories, known artifact manifest paths, patch_id fields, and status/verdict markers. Arbitrary unrelated JSON files must not be classified.

Discovery receipt:

```txt
legacy_receipt_discovery_created = true
legacy_receipt_file_count_expected_min = 252
legacy_receipt_file_count_discovered >= 252
legacy_receipt_hash_count = legacy_receipt_file_count_discovered
legacy_receipt_unreadable_count = 0
legacy_receipt_duplicate_identity_count = 0
legacy_receipt_out_of_scope_count = 0
```

## Claim Extraction

K7M-B must extract boolean claims, status/verdict markers, route identifiers, execution identifiers, dispatch/readback digests, registry epochs/hashes, and source receipt references.

```txt
claim_extraction_created = true
legacy_receipt_count_scanned = discovered count
claim_count_total > 0
protected_claim_occurrence_count > 0
claim_extraction_failure_count = 0
```

## Annotation Sidecar

Each annotation file uses:

```txt
annotation_schema = ash_tensorcube_legacy_truth_annotation_v1
evidence_schema_version = ash_tensorcube_evidence_schema_v1
```

It contains immutable receipt identity, claims, and summary counts per evidence class, unresolved count, and protected claim policy failure count.

## Canonical Reclassification Index

The index contains receipt identity/hash, annotation path/hash, claim count, highest authority, protected claim count, policy failure count, unresolved count, and K7M-C binding requirement.

The index must be deterministic and sorted by patch_id, receipt_path, and claim_json_pointer.

## Annotation Integrity

```txt
annotation_integrity_created = true
all_annotation_receipt_hashes_match = true
all_annotation_files_parse = true
all_claim_json_pointers_resolve = true
all_original_claim_values_match = true
all_class_authority_pairs_valid = true
all_protected_claim_policies_evaluated = true
annotation_duplicate_id_count = 0
annotation_orphan_count = 0
annotation_integrity_failure_count = 0
```

## No Legacy Value Rewrite Guard

K7M-B must compute before/after hashes for every legacy receipt.

```txt
no_legacy_value_rewrite_guard_created = true
legacy_receipt_hash_before_count = discovered count
legacy_receipt_hash_after_count = discovered count
legacy_receipt_hash_mismatch_count = 0
legacy_receipt_files_written = false
legacy_receipt_files_deleted = false
legacy_receipt_values_changed = false
legacy_pass_markers_changed = false
legacy_verdict_markers_changed = false
```

## No Runtime Mutation Guard

```txt
no_runtime_mutation_guard_created = true
gpu_dispatch_executed_by_k7m_b = false
gpu_readback_executed_by_k7m_b = false
cpu_parity_executed_by_k7m_b = false
burn_parity_executed_by_k7m_b = false
default_route_registry_mutated_by_k7m_b = false
user_visible_route_registry_mutated_by_k7m_b = false
production_route_registry_mutated_by_k7m_b = false
runtime_decode_output_changed_by_k7m_b = false
assistant_message_output_changed_by_k7m_b = false
activation_token_created_by_k7m_b = false
rollback_token_created_by_k7m_b = false
rollback_execution_started_by_k7m_b = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
```

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_legacy_claim_origin.rs
crates/burn_webgpu_backend/src/tensorcube_classification_confidence.rs
crates/burn_webgpu_backend/src/tensorcube_legacy_receipt_identity.rs
crates/burn_webgpu_backend/src/tensorcube_legacy_claim_annotation.rs
crates/burn_webgpu_backend/src/tensorcube_legacy_reclassification_policy.rs
crates/burn_webgpu_backend/src/tensorcube_legacy_annotation_index.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_prior_k7m_a_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_legacy_receipt_discovery.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_claim_extraction.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_reclassification_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_reclassification_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_protected_claim_downgrade_report.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_unresolved_claim_report.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_annotation_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_no_legacy_value_rewrite_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_no_runtime_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_b_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7m_b_legacy_truth_reclassification_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7m_b_legacy_truth_reclassification_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7m_b_legacy_truth_reclassification_audit -- --repo-root <repo> --require-k7m-a-pass --discover-legacy-receipts --extract-legacy-claims --apply-read-only-reclassification --write-annotation-sidecars --write-reclassification-index --write-protected-claim-downgrade-report --write-unresolved-claim-report --verify-annotation-integrity --no-legacy-value-rewrite --no-runtime-mutation
```

## PASS Markers

```txt
PASS_ASH_TCU_K7M_B_PRIOR_K7M_A_RECEIPT
PASS_ASH_TCU_K7M_B_LEGACY_RECEIPT_DISCOVERY
PASS_ASH_TCU_K7M_B_LEGACY_CLAIM_EXTRACTION
PASS_ASH_TCU_K7M_B_RECLASSIFICATION_POLICY
PASS_ASH_TCU_K7M_B_READ_ONLY_RECLASSIFICATION_EXECUTION
PASS_ASH_TCU_K7M_B_PROTECTED_CLAIM_DOWNGRADE_REPORT
PASS_ASH_TCU_K7M_B_UNRESOLVED_CLAIM_REPORT
PASS_ASH_TCU_K7M_B_ANNOTATION_INTEGRITY
PASS_ASH_TCU_K7M_B_NO_LEGACY_VALUE_REWRITE
PASS_ASH_TCU_K7M_B_NO_RUNTIME_MUTATION
PASS_ASH_TCU_K7M_B_LEGACY_RECEIPT_TRUTH_RECLASSIFICATION_NO_LEGACY_VALUE_REWRITE_NO_RUNTIME_MUTATION_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7M_B_MISSING_K7M_A_PRIOR_VERDICT
FAIL_ASH_TCU_K7M_B_K7M_A_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7M_B_EVIDENCE_SCHEMA_VERSION_MISMATCH
FAIL_ASH_TCU_K7M_B_LEGACY_RECEIPT_DISCOVERY_FAILED
FAIL_ASH_TCU_K7M_B_LEGACY_RECEIPT_UNREADABLE
FAIL_ASH_TCU_K7M_B_LEGACY_RECEIPT_IDENTITY_DUPLICATE
FAIL_ASH_TCU_K7M_B_LEGACY_RECEIPT_HASH_MISSING
FAIL_ASH_TCU_K7M_B_CLAIM_EXTRACTION_FAILED
FAIL_ASH_TCU_K7M_B_PROTECTED_CLAIM_NOT_EVALUATED
FAIL_ASH_TCU_K7M_B_INVALID_CLASS_AUTHORITY_PAIR
FAIL_ASH_TCU_K7M_B_DECLARED_INTENT_UPGRADED_TO_EXECUTION
FAIL_ASH_TCU_K7M_B_DERIVED_RECEIPT_UPGRADED_TO_MEASUREMENT
FAIL_ASH_TCU_K7M_B_AUDIT_CONSTRUCTED_ROUTE_MUTATION_ACCEPTED
FAIL_ASH_TCU_K7M_B_RUNTIME_OUTPUT_OWNER_FALSELY_RESOLVED
FAIL_ASH_TCU_K7M_B_UNKNOWN_CLAIM_SILENTLY_UPGRADED
FAIL_ASH_TCU_K7M_B_ANNOTATION_SIDECAR_MISSING
FAIL_ASH_TCU_K7M_B_ANNOTATION_RECEIPT_HASH_MISMATCH
FAIL_ASH_TCU_K7M_B_ANNOTATION_CLAIM_POINTER_INVALID
FAIL_ASH_TCU_K7M_B_ANNOTATION_ORIGINAL_VALUE_MISMATCH
FAIL_ASH_TCU_K7M_B_ANNOTATION_INTEGRITY_FAILED
FAIL_ASH_TCU_K7M_B_LEGACY_RECEIPT_REWRITTEN
FAIL_ASH_TCU_K7M_B_LEGACY_RECEIPT_DELETED
FAIL_ASH_TCU_K7M_B_LEGACY_VALUE_CHANGED
FAIL_ASH_TCU_K7M_B_LEGACY_PASS_MARKER_CHANGED
FAIL_ASH_TCU_K7M_B_LEGACY_VERDICT_CHANGED
FAIL_ASH_TCU_K7M_B_GPU_EXECUTION_STARTED
FAIL_ASH_TCU_K7M_B_GPU_READBACK_STARTED
FAIL_ASH_TCU_K7M_B_RUNTIME_ROUTE_MUTATED
FAIL_ASH_TCU_K7M_B_ROLLBACK_EXECUTION_STARTED
FAIL_ASH_TCU_K7M_B_WEIGHT_MUTATION_DETECTED
```

## Static Checks

Static checks must use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

They must verify prior K7M-A pass, schema v1, at least 252 receipts discovered, no unreadable or duplicate receipts, nonzero extracted claims and protected claims, no extraction failures, read-only reclassification executed, sidecar count equals receipt count, annotation integrity passes, legacy hashes match, no silent evidence upgrades, no GPU execution, no route mutation, no rollback, and no weight mutation.

## Recommended Next Patch

```txt
ASH-TCU-K7M-C
Execution Evidence Binding / Actual Queue Submit Dispatch Readback And Comparison Evidence / No Route Mutation No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7M-B does not rewrite history.

It creates a read-only evidence interpretation layer over K6ZV through K7L. Legacy values, PASS markers, and verdicts remain intact. Claims supported only by CLI intent, static construction, or prior receipt derivation are not treated as equivalent to measured GPU execution or actual runtime route mutation.
```
