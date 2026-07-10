# ASH-TCU-K7M-A SPEC

## Title

TensorCube Evidence Class SSOT / Measured Declared Derived Evidence Separation / Protected Execution And Mutation Claims / No Legacy Receipt Rewrite No Runtime Mutation Seal

## Patch ID

```txt
ASH-TCU-K7M-A
```

## Status Target

```txt
PASS_ASH_TCU_K7M_A_EVIDENCE_CLASS_SSOT_NO_LEGACY_REWRITE_NO_RUNTIME_MUTATION_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7L
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7L_USER_VISIBLE_ROLLBACK_REHEARSAL_NO_ACTUAL_ROLLBACK_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
user_visible_rollback_rehearsal_passed_no_actual_rollback
```

## Purpose

`ASH-TCU-K7M-A` establishes a single source of truth for TensorCube evidence semantics.

Previous TensorCube patches contain several different kinds of claims: static contract checks, operator intent, derived receipt state, actual GPU execution, measured GPU readback, CPU parity comparison, Burn parity comparison, and runtime route mutation.

These claims must no longer share the same semantic authority merely because they are represented as boolean fields.

K7M-A introduces a typed evidence classification layer that distinguishes what was declared, what was derived, what was executed, what was measured, what was compared, and what was actually mutated.

K7M-A does not rewrite K6ZV through K7L receipts, reinterpret old PASS markers, execute a GPU kernel, mutate route registries, create or consume activation or rollback tokens, replace production, or mutate model weights.

Legacy receipt reclassification belongs to `ASH-TCU-K7M-B`.

Actual dispatch evidence binding belongs to `ASH-TCU-K7M-C`.

## SSOT

### Evidence Schema Owner

```txt
crates/burn_webgpu_backend/src/tensorcube_evidence_class.rs
```

### Evidence Record Owner

```txt
crates/burn_webgpu_backend/src/tensorcube_evidence_record.rs
```

### Evidence Authority Policy Owner

```txt
crates/burn_webgpu_backend/src/tensorcube_evidence_authority_policy.rs
```

### Runtime Receipt Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_evidence_class_ssot_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_prior_k7l_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_evidence_schema_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_evidence_authority_matrix_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_protected_claim_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_schema_validation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_legacy_receipt_inventory_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_no_legacy_rewrite_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_no_runtime_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_a_verdict_latest.json
artifacts/ASH_TCU_K7M_A_LOCAL_MANIFEST.json
```

## State Ownership

K7M-A owns the TensorCube evidence class definition, evidence record definition, authority levels, protected claim policy, schema validation, new-receipt metadata contract, legacy receipt read-only inventory, no-legacy-rewrite guard, and no-runtime-mutation guard.

K7M-A does not own legacy receipt reclassification, legacy PASS replacement, GPU dispatch, queue submission, readback, CPU or Burn parity execution, runtime route mutation, route replacement, token creation, rollback execution, weight mutation, optimizer mutation, safetensors mutation, or checkpoint finalization.

## Evidence Class Definition

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TensorCubeEvidenceClass {
    StaticContract,
    DeclaredIntent,
    DerivedReceipt,
    ExecutedGpu,
    MeasuredReadback,
    ComparedAgainstCpu,
    ComparedAgainstBurn,
    RuntimeRouteMutation,
}
```

## Evidence Authority Definition

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum TensorCubeEvidenceAuthority {
    ContractOnly,
    IntentOnly,
    DerivedOnly,
    Executed,
    Measured,
    Compared,
    RuntimeMutated,
}
```

## Authority Mapping

```txt
StaticContract       -> ContractOnly
DeclaredIntent       -> IntentOnly
DerivedReceipt       -> DerivedOnly
ExecutedGpu          -> Executed
MeasuredReadback     -> Measured
ComparedAgainstCpu   -> Compared
ComparedAgainstBurn  -> Compared
RuntimeRouteMutation -> RuntimeMutated
```

The mapping must be centralized. Call sites must not define alternative authority ordering.

## Evidence Record

```rust
#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct TensorCubeEvidenceRecord {
    pub evidence_id: String,
    pub patch_id: String,
    pub claim_name: String,
    pub evidence_class: TensorCubeEvidenceClass,
    pub authority: TensorCubeEvidenceAuthority,
    pub is_measured: bool,
    pub is_declared_only: bool,
    pub is_derived: bool,
    pub is_runtime_mutation: bool,
    pub source_execution_id: Option<String>,
    pub source_receipt_ids: Vec<String>,
    pub source_dispatch_digest: Option<String>,
    pub source_readback_digest: Option<String>,
    pub source_registry_epoch: Option<u64>,
    pub source_registry_hash: Option<String>,
    pub claim_value: serde_json::Value,
    pub evidence_schema_version: String,
}
```

## Evidence Schema Version

```txt
ash_tensorcube_evidence_schema_v1
```

Every K7M-A or later TensorCube receipt must expose this schema version.

## Canonical Evidence Rules

### Static contract

```txt
evidence_class = static_contract
is_measured = false
is_declared_only = false
is_derived = false
is_runtime_mutation = false
```

### Declared intent

```txt
evidence_class = declared_intent
is_measured = false
is_declared_only = true
is_derived = false
is_runtime_mutation = false
```

### Derived receipt

```txt
evidence_class = derived_receipt
is_measured = false
is_declared_only = false
is_derived = true
is_runtime_mutation = false
source_receipt_ids is not empty
```

### Executed GPU

```txt
evidence_class = executed_gpu
is_measured = false
is_declared_only = false
is_derived = false
is_runtime_mutation = false
source_execution_id is present
source_dispatch_digest is present
```

### Measured readback

```txt
evidence_class = measured_readback
is_measured = true
is_declared_only = false
is_derived = false
is_runtime_mutation = false
source_execution_id is present
source_readback_digest is present
```

### Compared evidence

```txt
evidence_class = compared_against_cpu or compared_against_burn
is_measured = true
is_declared_only = false
is_derived = false
is_runtime_mutation = false
source_execution_id is present
source_readback_digest is present
```

### Runtime route mutation

```txt
evidence_class = runtime_route_mutation
is_measured = false
is_declared_only = false
is_derived = false
is_runtime_mutation = true
source_registry_epoch is present
source_registry_hash is present
```

## Protected Claims

```rust
pub enum TensorCubeProtectedClaim {
    NativeWgpuDispatchExecuted,
    GpuOutputMeasured,
    CpuParityPassed,
    BurnParityPassed,
    DefaultRouteMutated,
    UserVisibleRouteMutated,
    ProductionRouteMutated,
    RuntimeDecodeOutputChanged,
    AssistantMessageOutputChanged,
    ActualRollbackExecuted,
}
```

## Minimum Evidence Class Per Protected Claim

```txt
native_wgpu_dispatch_executed -> ExecutedGpu or higher
gpu_output_measured -> MeasuredReadback or higher
cpu_parity_passed -> ComparedAgainstCpu
burn_parity_passed -> ComparedAgainstBurn
default_route_mutated -> RuntimeRouteMutation
user_visible_route_mutated -> RuntimeRouteMutation
production_route_mutated -> RuntimeRouteMutation
actual_rollback_executed -> RuntimeRouteMutation
```

`runtime_decode_output_changed` and `assistant_message_output_changed` remain protected but unresolved until their runtime owners are defined.

## Protected Claim Validation API

```rust
pub fn validate_protected_claim(
    claim: TensorCubeProtectedClaim,
    evidence: &TensorCubeEvidenceRecord,
) -> Result<(), TensorCubeEvidenceError>;
```

## Error Type

```rust
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum TensorCubeEvidenceError {
    MissingEvidenceId,
    MissingPatchId,
    MissingClaimName,
    MissingSchemaVersion,
    SchemaVersionMismatch,
    InvalidAuthorityForClass,
    InvalidBooleanCombination,
    MissingSourceExecutionId,
    MissingSourceReceiptIds,
    MissingDispatchDigest,
    MissingReadbackDigest,
    MissingRegistryEpoch,
    MissingRegistryHash,
    DeclaredIntentUsedAsExecution,
    DerivedReceiptUsedAsMeasurement,
    StaticContractUsedAsExecution,
    NonMutationEvidenceUsedAsRouteMutation,
    ProtectedClaimAuthorityTooLow,
}
```

## Evidence Authority Matrix Receipt

```txt
evidence_authority_matrix_created = true
evidence_schema_version = ash_tensorcube_evidence_schema_v1
evidence_class_count = 8
evidence_authority_count = 7
protected_claim_count = 10
authority_mapping_complete = true
protected_claim_policy_complete = true
```

## Schema Validation Fixtures

Positive fixtures:

```txt
valid_static_contract
valid_declared_intent
valid_derived_receipt
valid_executed_gpu
valid_measured_readback
valid_cpu_comparison
valid_burn_comparison
valid_runtime_route_mutation
```

Negative fixtures:

```txt
declared_intent_claims_gpu_execution
derived_receipt_claims_gpu_measurement
static_contract_claims_route_mutation
executed_gpu_missing_execution_id
executed_gpu_missing_dispatch_digest
measured_readback_missing_readback_digest
derived_receipt_missing_source_receipt
runtime_mutation_missing_epoch
runtime_mutation_missing_registry_hash
cpu_parity_uses_measured_readback_class
burn_parity_uses_derived_receipt_class
```

## Legacy Receipt Boundary

K7M-A may read K6ZV through K7L receipts to enumerate legacy claim names. It must not rewrite, delete, change PASS markers, change values, silently attach measured authority, or silently downgrade existing receipt files.

It must produce a read-only inventory:

```txt
legacy_receipt_inventory_created = true
legacy_receipt_rewrite_executed = false
legacy_receipt_reclassification_executed = false
legacy_receipt_reclassification_required_next = true
recommended_next_patch = ASH-TCU-K7M-B
```

## No Legacy Rewrite Guard

```txt
no_legacy_rewrite_guard_created = true
legacy_receipt_files_written = false
legacy_receipt_files_deleted = false
legacy_receipt_pass_markers_changed = false
legacy_receipt_values_changed = false
legacy_receipt_reclassification_executed = false
```

## No Runtime Mutation Guard

```txt
no_runtime_mutation_guard_created = true
gpu_dispatch_executed_by_k7m_a = false
gpu_readback_executed_by_k7m_a = false
default_route_registry_mutated_by_k7m_a = false
user_visible_route_registry_mutated_by_k7m_a = false
production_route_registry_mutated_by_k7m_a = false
runtime_decode_output_changed_by_k7m_a = false
assistant_message_output_changed_by_k7m_a = false
rollback_execution_started_by_k7m_a = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
```

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_evidence_class.rs
crates/burn_webgpu_backend/src/tensorcube_evidence_record.rs
crates/burn_webgpu_backend/src/tensorcube_evidence_authority_policy.rs
crates/burn_webgpu_backend/src/tensorcube_protected_claim.rs
crates/burn_webgpu_backend/src/tensorcube_evidence_error.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_prior_k7l_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_evidence_schema.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_evidence_authority_matrix.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_protected_claim_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_schema_validation.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_legacy_receipt_inventory.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_no_legacy_rewrite_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_no_runtime_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_a_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7m_a_evidence_class_ssot_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7m_a_evidence_class_ssot_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7m_a_evidence_class_ssot_audit -- --repo-root <repo> --require-k7l-pass --create-evidence-schema --create-evidence-authority-matrix --create-protected-claim-policy --validate-positive-evidence-fixtures --validate-negative-evidence-fixtures --inventory-legacy-receipts-read-only --no-legacy-rewrite --no-runtime-mutation
```

## PASS Markers

```txt
PASS_ASH_TCU_K7M_A_PRIOR_K7L_RECEIPT
PASS_ASH_TCU_K7M_A_EVIDENCE_SCHEMA
PASS_ASH_TCU_K7M_A_EVIDENCE_AUTHORITY_MATRIX
PASS_ASH_TCU_K7M_A_PROTECTED_CLAIM_POLICY
PASS_ASH_TCU_K7M_A_POSITIVE_SCHEMA_FIXTURES
PASS_ASH_TCU_K7M_A_NEGATIVE_SCHEMA_FIXTURES
PASS_ASH_TCU_K7M_A_LEGACY_RECEIPT_READ_ONLY_INVENTORY
PASS_ASH_TCU_K7M_A_NO_LEGACY_REWRITE
PASS_ASH_TCU_K7M_A_NO_RUNTIME_MUTATION
PASS_ASH_TCU_K7M_A_EVIDENCE_CLASS_SSOT_NO_LEGACY_REWRITE_NO_RUNTIME_MUTATION_SEAL
```

## Static Checks

K7M-A static checks must use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

They must verify prior K7L pass, evidence schema creation, class and authority counts, policy completeness, fixture results, read-only legacy inventory, no legacy rewrite, no GPU execution, no route mutation, no rollback, and no weight or checkpoint mutation.

## Recommended Next Patch

```txt
ASH-TCU-K7M-B
Legacy Receipt Truth Reclassification / K6ZV Through K7L Evidence Authority Annotation / No Legacy Value Rewrite No Runtime Mutation Seal
```

## Final Seal

```txt
ASH-TCU-K7M-A does not claim new TensorCube execution.

ASH-TCU-K7M-A only creates the evidence vocabulary and authority policy required to distinguish declared intent, derived receipt state, actual GPU execution, measured output, parity comparison, and actual runtime route mutation without rewriting legacy receipts, changing existing PASS markers, executing GPU work, mutating runtime routes, executing rollback, replacing production, or mutating weights.
```
