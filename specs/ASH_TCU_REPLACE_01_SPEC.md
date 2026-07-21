# ASH-TCU-REPLACE-01

# Legacy Replacement Boolean Ownership Audit /
# Router Parity Telemetry Timing Preflight Authority Inventory /
# Requested Admitted Selected Dispatched Completed Output-Owned State Separation /
# No Runtime Behavior Change /
# No Replacement Enablement /
# No Production Promotion Seal

---

## 0. Patch Metadata

- **Patch ID**

  `ASH-TCU-REPLACE-01_LEGACY_REPLACEMENT_BOOLEAN_OWNERSHIP_AUDIT_ROUTER_PARITY_TELEMETRY_TIMING_PREFLIGHT_AUTHORITY_INVENTORY_REQUESTED_ADMITTED_SELECTED_DISPATCHED_COMPLETED_OUTPUT_OWNED_STATE_SEPARATION_NO_RUNTIME_BEHAVIOR_CHANGE_NO_REPLACEMENT_ENABLEMENT_NO_PRODUCTION_PROMOTION_SEAL`

- **Short ID**

  `ASH-TCU-REPLACE-01`

- **Parent code snapshot**

  `ASH-TRUTH-AUDIT-01-R3-R4`

- **Recommended semantic prerequisite**

  `ASH-TRUTH-AUDIT-01-R3-R5`

- **Next patch**

  `ASH-TCU-REPLACE-02_TENSORCUBE_REPLACEMENT_MODE_SSOT_IMMUTABLE_POLICY_SNAPSHOT_LEGACY_BOOLEAN_DERIVATION_SEAL`

- **Patch class**

  `static source authority audit, state vocabulary separation and baseline ownership receipt`

- **Runtime binary**

  `crates/orchestrator_local/src/bin/ash_tcu_replace_01_legacy_replacement_boolean_ownership_audit.rs`

- **Cargo feature**

  `orchestrator_tcu_audit_bins`

- **Runtime artifact schema**

  `ash.tcu.replace.01.ownership_audit.runtime_artifact.v1`

- **Primary runtime artifact**

  `workspace/runtime/tensorcube/ash_tcu_replace_01_ownership_audit_runtime_artifact.json`

- **Local manifest**

  `artifacts/ASH_TCU_REPLACE_01_LOCAL_MANIFEST.json`

- **Runtime execution**: forbidden
- **GPU adapter acquisition**: forbidden
- **Command submission**: forbidden
- **Route mutation**: forbidden
- **Replacement enablement**: forbidden
- **Default-route adoption**: forbidden
- **Production replacement**: forbidden
- **Performance claim**: forbidden
- **Model weight mutation**: forbidden
- **Optimizer state mutation**: forbidden

---

## 1. Purpose

This patch creates the first authoritative inventory of every source surface that currently declares, initializes, copies, validates, rejects, projects, asserts or claims TensorCube replacement state.

The patch must answer six distinct questions without collapsing them into one legacy boolean:

```text
Was TensorCube replacement requested?
Was the request admitted?
Was a TensorCube route selected?
Was that route actually dispatched?
Did that dispatch complete?
Did TensorCube output become downstream output authority?
```

It must separately inventory the independent governance axes:

```text
Was default-route mutation allowed?
Was production replacement allowed?
Was production replacement executed?
Was a performance claim allowed?
```

The patch establishes evidence for the following architectural conclusion:

```text
tensorcube_matmul_replacement_enabled
is not currently a reliable SSOT for execution state.
```

The same name may represent a default, a prohibition, a copied report field, a contract-leak sentinel, a test expectation, a policy input or a projected result. This patch identifies those roles. It does not repair them.

---

## 2. Required Scope

Required Rust roots:

```text
crates/burn_webgpu_backend/src
crates/burn_webgpu_backend/tests
crates/base_train/src
crates/orchestrator_local/src
crates/model_core/src
crates/lora_train/src
```

Required primary surfaces:

```text
crates/burn_webgpu_backend/src/qwave_atlas_backend_router.rs
crates/burn_webgpu_backend/src/qwave_atlas_parity.rs
crates/burn_webgpu_backend/src/qwave_atlas_telemetry.rs
crates/burn_webgpu_backend/src/qwave_atlas_timing_probe.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g209t0_tensorcube_tensorcore_shadow_preflight.rs
```

Required extended mutation-chain surfaces, when present:

```text
qwave_backend_switch_dryrun.rs
qwave_backend_apply_candidate.rs
qwave_backend_apply_sandbox.rs
qwave_backend_rollback_ledger.rs
qwave_backend_recovery_candidate.rs
qwave_backend_apply_preflight.rs
qwave_backend_shadow_commit.rs
```

Required symbol families:

```text
tensorcube_matmul_replacement_enabled
matmul_replacement_enabled
tensorcube_production_replacement_enabled
production_replacement_allowed
production_replacement_executed
production_default_change_allowed
production_default_changed
direct_replacement_allowed
runtime_apply_allowed
backend_policy_mutation_allowed
shadow_route_opened
tensorcube_shadow_route_opened
default_route_adopted
route_adoption
performance_claim_allowed
performance_claim
```

The scanner must additionally inspect identifiers combining TensorCube, replacement, production, promotion, adoption, route, dispatch, completion, output and claim semantics. Unknown matches may not be silently discarded.

---

## 3. Explicit Non-Goals

This patch must not:

```text
create TensorcubeReplacementMode
change a runtime configuration default
change false to true
read an enablement environment variable
create an experiment token
admit a TensorCube route
select a TensorCube route
dispatch TensorCube work
change default-route pointers
increment a route epoch
transfer output authority
permit production replacement
permit performance claims
repair timing validity
measure or promote 3.04x
```

---

## 4. Canonical Lifecycle Vocabulary

Introduce audit-only vocabulary:

```rust
enum ReplacementLifecycleState {
    Requested,
    Admitted,
    Selected,
    Dispatched,
    Completed,
    OutputOwned,
}
```

This enum belongs only to the audit binary or audit-support code. It must not become runtime policy in this patch.

### 4.1 Requested

An external or internal intent asks for TensorCube replacement or route use. Evidence may include CLI arguments, environment values, configuration fields, operator artifacts or API arguments.

Requested does not imply admission, selection, dispatch, completion or output ownership.

### 4.2 Admitted

A policy authority accepts the request for a defined scope. Evidence must identify authority, mode, predicates, reason and receipt. A config boolean without an admission receipt is not admitted-state proof.

### 4.3 Selected

A route or implementation is chosen from eligible candidates. Candidate ranking and nomination are not selection.

### 4.4 Dispatched

A command using the TensorCube implementation is submitted to the GPU queue. A route declaration, dispatch function declaration, telemetry type or enabled boolean does not prove dispatch.

### 4.5 Completed

Submitted TensorCube work reaches a verified completion boundary. Submission alone is not completion.

### 4.6 Output-Owned

TensorCube-produced output becomes the authoritative downstream tensor. A shadow comparison may be dispatched and completed while baseline output remains authoritative.

---

## 5. Orthogonal Governance Axes

The lifecycle states remain separate from:

```rust
struct ReplacementGovernanceAxes {
    default_route_change_allowed: bool,
    default_route_changed: bool,
    production_replacement_allowed: bool,
    production_replacement_executed: bool,
    performance_claim_allowed: bool,
    user_visible_execution_allowed: bool,
}
```

Completion does not imply production replacement. Output ownership does not imply performance-claim permission.

---

## 6. Occurrence Classification

Every matched occurrence receives one primary role:

```rust
enum ReplacementOccurrenceRole {
    StructFieldDeclaration,
    FunctionArgument,
    LocalBinding,
    LiteralDefault,
    ConfigInitializer,
    DirectAssignment,
    DerivedAssignment,
    BooleanComposition,
    AdmissionGuard,
    MutationGuard,
    ContractLeakGuard,
    NoExecutionGuard,
    NoPromotionGuard,
    NoPerformanceClaimGuard,
    CandidateRankInput,
    CandidateSelectionInput,
    RouteRegistryRead,
    RouteRegistryWrite,
    RouteMutationAttempt,
    DispatchRequest,
    DispatchSubmissionWitness,
    CompletionWitness,
    OutputSelection,
    OutputOwnershipWitness,
    ReportProjection,
    ManifestProjection,
    PriorReceiptRead,
    TestAssertion,
    CommentOrDiagnosticOnly,
    Unclassified,
}
```

Each occurrence also receives one authority class:

```rust
enum ReplacementAuthorityClass {
    None,
    InputAuthority,
    PolicyAuthority,
    AdmissionAuthority,
    SelectionAuthority,
    DispatchAuthority,
    CompletionAuthority,
    OutputAuthority,
    RouteRegistryAuthority,
    ProductionPromotionAuthority,
    PerformanceClaimAuthority,
    ObservationOnly,
    ProjectionOnly,
    TestOnly,
    Unknown,
}
```

Primary role and authority are independent. A report projection is `ReportProjection / ProjectionOnly`, not a writer.

---

## 7. Access Semantics

Each finding records:

```rust
struct ReplacementAccessSemantics {
    reads_state: bool,
    writes_state: bool,
    derives_state: bool,
    copies_state: bool,
    validates_state: bool,
    rejects_state: bool,
    asserts_state: bool,
    mutates_runtime: bool,
}
```

A copied report field does not increase authority-writer count. A validation string does not become runtime authority.

---

## 8. Finding Schema

```rust
struct ReplacementOwnershipFinding {
    finding_id: String,
    file_path: String,
    line_start: usize,
    line_end: usize,
    symbol: String,
    source_excerpt_digest: String,
    occurrence_role: ReplacementOccurrenceRole,
    authority_class: ReplacementAuthorityClass,
    lifecycle_states: Vec<ReplacementLifecycleState>,
    governance_axes: Vec<String>,
    access: ReplacementAccessSemantics,
    literal_bool: Option<bool>,
    referenced_symbols: Vec<String>,
    patch_or_stage_id: Option<String>,
    diagnostic_text: Option<String>,
    classification_confidence: String,
    classification_reason: String,
}
```

Finding IDs must be stable and derived from normalized path, location, symbol and normalized source excerpt.

---

## 9. Scanner Contract

Required order:

```text
physical source
→ preserve line positions
→ identify comments and strings
→ parse the Rust source structurally
→ identify declarations and expressions
→ identify exact symbol occurrences
→ classify syntactic role
→ assign authority semantics
→ assign lifecycle relevance
```

Forbidden:

```text
symbol contains "enabled"
→ assume runtime writer
```

If a required Rust source cannot be structurally parsed, it enters `parse_failure`; the scanner must not silently fall back to keyword-only PASS. Required metric:

```text
source_parse_failure_count=0
```

Comments and diagnostic strings are inventoried as `CommentOrDiagnosticOnly / None`. Test assertions are `TestAssertion / TestOnly`. Report copies are `ReportProjection / ProjectionOnly`.

---

## 10. Primary Surface Semantics

### Router

The QWave router is candidate recommendation and prohibition authority. It is not dispatch or output-ownership proof.

### Parity

Parity is a correctness witness, execution-evidence consumer and contract-leak guard. It is not route-selection authority.

### Telemetry

Telemetry observes execution. It does not authorize execution.

### Timing

Timing provides advisory measurement evidence. It does not prove route adoption, production replacement, output ownership or performance-claim eligibility.

### Preflight

Preflight declares capabilities, route availability and prohibitions. A preflight-opened surface is not admission, selection, dispatch, completion or output ownership.

---

## 11. Authority Conflict

A conflict exists when two independent writers claim the same state without a declared SSOT relationship.

Duplicated projections, duplicated guards and duplicated tests are not automatically conflicts. Competing write or decision authority is a conflict.

```rust
struct ReplacementAuthorityConflict {
    conflict_id: String,
    symbol_family: String,
    authority_a: String,
    authority_b: String,
    conflict_kind: String,
    shared_state: String,
    root_files: Vec<String>,
    blocking: bool,
    explanation: String,
}
```

---

## 12. Unknown Policy

Any occurrence that cannot be safely assigned becomes:

```text
role=Unclassified
authority=Unknown
```

PASS requires:

```text
unclassified_occurrence_count=0
```

Unknown findings may not be suppressed because they are outside the primary files.

---

## 13. Runtime Artifact Layout

```json
{
  "schema": "ash.tcu.replace.01.ownership_audit.runtime_artifact.v1",
  "patch_id": "ASH-TCU-REPLACE-01",
  "source_snapshot": {},
  "scan_scope": {},
  "symbol_family_summary": {},
  "primary_surface_inventory": [],
  "extended_surface_inventory": [],
  "lifecycle_state_inventory": {
    "requested": {},
    "admitted": {},
    "selected": {},
    "dispatched": {},
    "completed": {},
    "output_owned": {}
  },
  "governance_axis_inventory": {
    "default_route": {},
    "production_replacement": {},
    "performance_claim": {}
  },
  "authority_summary": {},
  "authority_conflicts": [],
  "unclassified_findings": [],
  "no_runtime_behavior_change_guard": {},
  "predicates": [],
  "verdict": {}
}
```

---

## 14. Rust-Generated Outputs

The Rust binary must create all receipts and the manifest at runtime:

```text
workspace/runtime/tensorcube/ash_tcu_replace_01_ownership_audit_runtime_artifact.json
workspace/runtime/tensorcube/ash_tcu_replace_01_symbol_occurrence_inventory.json
workspace/runtime/tensorcube/ash_tcu_replace_01_primary_authority_surface_inventory.json
workspace/runtime/tensorcube/ash_tcu_replace_01_extended_qwave_mutation_chain_inventory.json
workspace/runtime/tensorcube/ash_tcu_replace_01_route_registry_authority_inventory.json
workspace/runtime/tensorcube/ash_tcu_replace_01_lifecycle_state_separation_receipt.json
workspace/runtime/tensorcube/ash_tcu_replace_01_governance_axis_separation_receipt.json
workspace/runtime/tensorcube/ash_tcu_replace_01_authority_conflict_receipt.json
workspace/runtime/tensorcube/ash_tcu_replace_01_unclassified_occurrence_receipt.json
workspace/runtime/tensorcube/ash_tcu_replace_01_no_runtime_behavior_change_guard.json
workspace/runtime/tensorcube/ash_tcu_replace_01_no_replacement_enablement_guard.json
workspace/runtime/tensorcube/ash_tcu_replace_01_no_production_promotion_guard.json
workspace/runtime/tensorcube/ash_tcu_replace_01_no_performance_claim_guard.json
workspace/runtime/tensorcube/ash_tcu_replace_01_static_checks.json
workspace/runtime/tensorcube/ash_tcu_replace_01_verdict.json
artifacts/ASH_TCU_REPLACE_01_LOCAL_MANIFEST.json
```

The baked ZIP must not contain the specification, generated runtime artifacts or generated manifest.

---

## 15. Allowed Changes

Allowed:

```text
new audit binary
Cargo.toml bin registration
audit-only tests
```

Conditionally allowed:

```text
small audit-only shared module under orchestrator_local
```

Forbidden:

```text
burn_webgpu_backend runtime behavior modifications
base_train route modifications
model_core route modifications
lora_train decode route modifications
route registry mutation-policy modifications
QWave config default changes
```

---

## 16. No Runtime Behavior Change Guard

Required receipt:

```json
{
  "gpu_adapter_requested": false,
  "gpu_device_requested": false,
  "command_encoder_created": false,
  "command_submitted": false,
  "route_registry_mutated": false,
  "route_epoch_incremented": false,
  "default_route_changed": false,
  "model_output_changed": false,
  "training_output_changed": false,
  "decode_output_changed": false,
  "model_weights_mutated": false,
  "optimizer_state_mutated": false
}
```

---

## 17. No Replacement Enablement Guard

Required:

```text
no existing false replacement default changed to true
no new runtime enable flag introduced
no replacement environment variable introduced
no replacement CLI enable argument introduced
no admitted replacement policy introduced
```

The audit-only lifecycle vocabulary must not be wired into runtime configuration.

---

## 18. No Production Promotion Guard

Required:

```text
production_replacement_allowed=false
production_replacement_executed=false
production_default_changed=false
default_route_adoption_executed=false
user_visible_activation_executed=false
```

---

## 19. No Performance Claim Guard

Required:

```text
performance_claim_allowed=false
operator_speedup_claim_allowed=false
decode_speedup_claim_allowed=false
training_speedup_claim_allowed=false
```

The audit may report numeric values as observations but must not promote them into claims.

---

## 20. Blocking Predicates

```text
TCU_REPLACE_01_REQUIRED_PRIMARY_SURFACES_PRESENT
TCU_REPLACE_01_ALL_MATCHED_OCCURRENCES_CLASSIFIED
TCU_REPLACE_01_ALL_REQUIRED_RUST_SOURCES_PARSED
TCU_REPLACE_01_ALL_PRIMARY_FINDINGS_HAVE_AUTHORITY_CLASS
TCU_REPLACE_01_REQUESTED_ADMITTED_SELECTED_DISPATCHED_COMPLETED_OUTPUT_OWNED_SEPARATED
TCU_REPLACE_01_PRODUCTION_AND_PERFORMANCE_AXES_NOT_DERIVED_FROM_EXECUTION
TCU_REPLACE_01_REPORT_AND_MANIFEST_PROJECTIONS_NOT_AUTHORITY_WRITERS
TCU_REPLACE_01_TEST_ASSERTIONS_NOT_RUNTIME_AUTHORITY
TCU_REPLACE_01_NO_RUNTIME_BEHAVIOR_CHANGE
TCU_REPLACE_01_NO_REPLACEMENT_ENABLEMENT
TCU_REPLACE_01_NO_PRODUCTION_PROMOTION
TCU_REPLACE_01_NO_PERFORMANCE_CLAIM
TCU_REPLACE_01_INVENTORY_ORDER_AND_DIGEST_DETERMINISTIC
TCU_REPLACE_01_ALL_BLOCKING_PREDICATES_PASS
```

---

## 21. Determinism

All findings must be sorted by normalized file path, line start, line end, symbol, role and authority. Canonical JSON must be deterministic. Repeated runs against the same tree must produce identical semantic digests; timestamps are excluded from semantic digests.

---

## 22. Required Tests

```text
classifies_struct_field_declaration
classifies_false_config_initializer
classifies_contract_leak_guard
classifies_report_projection
classifies_test_assertion
classifies_boolean_composition
classifies_route_registry_read
classifies_route_registry_write
classifies_dispatch_submission
classifies_completion_witness
classifies_output_selection
diagnostic_string_is_not_runtime_authority
comment_occurrence_is_not_runtime_authority
unknown_occurrence_fails_closed
primary_router_surface_found
primary_parity_surface_found
primary_telemetry_surface_found
primary_timing_surface_found
primary_preflight_surface_found
all_replacement_symbols_inventory_nonempty
all_primary_occurrences_classified
no_runtime_gpu_call_from_audit
no_route_registry_mutation_from_audit
no_false_to_true_runtime_change
deterministic_artifact_digest
```

---

## 23. Runtime Command

```powershell
cargo run `
  --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_replace_01_legacy_replacement_boolean_ownership_audit `
  -- `
  --repo-root . `
  --out-dir workspace/runtime/tensorcube `
  --fail-on-unclassified true `
  --require-no-runtime-behavior-change true `
  --require-no-replacement-enablement true `
  --require-no-production-promotion true
```

---

## 24. Failure IDs

```text
FAIL_TCU_REPLACE_01_REQUIRED_PRIMARY_SURFACE_MISSING
FAIL_TCU_REPLACE_01_SOURCE_PARSE_FAILURE
FAIL_TCU_REPLACE_01_UNCLASSIFIED_OCCURRENCE
FAIL_TCU_REPLACE_01_AUTHORITY_CLASS_MISSING
FAIL_TCU_REPLACE_01_LIFECYCLE_STATE_COLLAPSED
FAIL_TCU_REPLACE_01_GOVERNANCE_AXIS_COLLAPSED
FAIL_TCU_REPLACE_01_PROJECTION_MISCLASSIFIED_AS_WRITER
FAIL_TCU_REPLACE_01_TEST_MISCLASSIFIED_AS_AUTHORITY
FAIL_TCU_REPLACE_01_CONFLICTING_STATE_WRITERS
FAIL_TCU_REPLACE_01_RUNTIME_BEHAVIOR_CHANGED
FAIL_TCU_REPLACE_01_REPLACEMENT_ENABLED
FAIL_TCU_REPLACE_01_PRODUCTION_PROMOTION_DETECTED
FAIL_TCU_REPLACE_01_PERFORMANCE_CLAIM_DETECTED
FAIL_TCU_REPLACE_01_NONDETERMINISTIC_INVENTORY
```

---

## 25. Expected PASS State

```text
required_primary_surface_count >= 5
required_primary_surface_missing_count=0
matched_occurrence_count > 0
classified_occurrence_count=matched_occurrence_count
unclassified_occurrence_count=0
source_parse_failure_count=0
requested_state_inventory_created=true
admitted_state_inventory_created=true
selected_state_inventory_created=true
dispatched_state_inventory_created=true
completed_state_inventory_created=true
output_owned_state_inventory_created=true
lifecycle_state_collapse_count=0
governance_axis_collapse_count=0
runtime_behavior_changed=false
replacement_enabled_by_patch=false
default_route_changed_by_patch=false
production_replacement_executed_by_patch=false
performance_claim_allowed_by_patch=false
```

---

## 26. Expected Semantic Outcome

The expected conclusion is not that TensorCube replacement is ready. The expected conclusion is:

```text
The repository contains multiple legacy boolean declarations,
guards, projections, tests and staged governance surfaces.

Their ownership roles are now completely inventoried.

Requested, admitted, selected, dispatched, completed and
output-owned states are semantically distinct.

No current field is promoted into the new runtime SSOT.

No replacement behavior changed.
```

---

## 27. Promotion Boundary

`ASH-TCU-REPLACE-02` may begin only when:

```text
all occurrences are classified
all primary authority surfaces are present
no unknown writer remains
no runtime behavior changed
no replacement was enabled
```

If unknown writers remain, REPLACE-02 is blocked.

REPLACE-02 must bind:

```text
ash_tcu_replace_01_ownership_audit_runtime_artifact.json
parent_ownership_inventory_digest
```

---

## 28. Final Seal

This patch passes only when the repository can state with source-backed evidence:

```text
Every legacy replacement-related boolean occurrence is known.
Every occurrence has a syntactic role.
Every primary occurrence has an authority classification.
Requested, admitted, selected, dispatched, completed and output-owned
are no longer treated as interchangeable words.
Production promotion and performance claims remain independent.
No runtime route was changed.
No TensorCube replacement was enabled.
No production promotion occurred.
```

Canonical verdict:

```text
PASS_ASH_TCU_REPLACE_01_LEGACY_REPLACEMENT_BOOLEAN_OWNERSHIP_AUDIT_COMPLETE_LIFECYCLE_STATE_SEPARATION_COMPLETE_NO_RUNTIME_BEHAVIOR_CHANGE_NO_REPLACEMENT_ENABLEMENT_NO_PRODUCTION_PROMOTION
```
