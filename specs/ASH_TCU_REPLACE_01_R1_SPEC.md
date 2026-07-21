# ASH-TCU-REPLACE-01-R1

# Audit Self-Scan Exclusion /
# Audit-Generated Vocabulary and Diagnostic Surface Isolation /
# Projection and Comment Writer Counter Semantics Repair /
# Primitive Authority Writer Edge Graph /
# Same-State Same-Scope Conflict Derivation /
# Semantic Inventory Digest Reissue /
# Premature REPLACE-02 Readiness Retirement /
# No Runtime Behavior Change /
# No Replacement Enablement Seal

---

## 0. Patch Metadata

- **Patch ID**

  `ASH-TCU-REPLACE-01-R1_AUDIT_SELF_SCAN_EXCLUSION_AUDIT_GENERATED_VOCABULARY_DIAGNOSTIC_SURFACE_ISOLATION_PROJECTION_COMMENT_WRITER_COUNTER_SEMANTICS_REPAIR_PRIMITIVE_AUTHORITY_WRITER_EDGE_GRAPH_SAME_STATE_SAME_SCOPE_CONFLICT_DERIVATION_SEMANTIC_INVENTORY_DIGEST_REISSUE_PREMATURE_REPLACE_02_READINESS_RETIREMENT_NO_RUNTIME_BEHAVIOR_CHANGE_NO_REPLACEMENT_ENABLEMENT_SEAL`

- **Short ID**: `ASH-TCU-REPLACE-01-R1`
- **Parent**: `ASH-TCU-REPLACE-01`
- **Parent semantic digest**: `6e349b21616d0d9db8ef212f14c2b6b76693684d9ae8074da4819a81e2d45f30`
- **Parent digest disposition**: `historical_only / superseded / promotion_authority_forbidden`
- **Runtime binary**: `crates/orchestrator_local/src/bin/ash_tcu_replace_01_legacy_replacement_boolean_ownership_audit.rs`
- **Runtime schema**: `ash.tcu.replace.01.r1.ownership_audit.runtime_artifact.v1`
- **Primary artifact**: `workspace/runtime/tensorcube/ash_tcu_replace_01_r1_ownership_audit_runtime_artifact.json`
- **Manifest**: `artifacts/ASH_TCU_REPLACE_01_R1_LOCAL_MANIFEST.json`
- **Patch class**: `audit truth repair, scope isolation, writer semantics repair, primitive conflict graph derivation and readiness revocation`

Forbidden in this patch:

```text
GPU adapter or device acquisition
GPU command submission
route mutation
replacement enablement
default-route adoption
production promotion
performance claim
model or optimizer mutation
```

---

## 1. Purpose

The parent audit preserved runtime safety but is not eligible to become the parent SSOT for REPLACE-02 because:

```text
the audit binary scanned its own generated vocabulary
projection and comment surfaces inflated writer semantics
zero-conflict output lacked primitive edge-pair evidence
repository_ready_for_replace_02 became true before those defects were closed
```

R1 preserves the parent safety truth and reissues the ownership digest from uncontaminated subject evidence.

---

## 2. Confirmed Parent State

```text
scanned_rust_file_count=5197
matched_occurrence_count=10144
unclassified_occurrence_count=0
source_parse_failure_count=0
blocking_authority_conflict_count=0
runtime_behavior_changed=false
replacement_enabled_by_patch=false
production_replacement_executed_by_patch=false
performance_claim_allowed_by_patch=false
repository_ready_for_replace_02=true
semantic_inventory_digest=6e349b21616d0d9db8ef212f14c2b6b76693684d9ae8074da4819a81e2d45f30
```

Safety fields remain valid. Parent readiness and digest promotion authority are retired.

---

## 3. Self-Scan Exclusion

The audit implementation must be excluded before file read, parsing, symbol matching, occurrence counting, classification and semantic digest input.

Exact exclusion:

```text
crates/orchestrator_local/src/bin/ash_tcu_replace_01_legacy_replacement_boolean_ownership_audit.rs
```

Future helper prefix:

```text
crates/orchestrator_local/src/bin/ash_tcu_replace_01_r1_*.rs
```

Forbidden:

```text
scan first
remove findings later
```

Required receipt:

```json
{
  "audit_implementation_excluded_before_read": true,
  "self_scan_occurrence_count": 0,
  "self_scan_digest_input_count": 0,
  "pass": true
}
```

---

## 4. Generated Surface Isolation

Audit-only vocabulary, JSON keys, predicate IDs, failure IDs, verdict strings and diagnostics must not become subject evidence.

Required:

```text
generated_vocabulary_subject_occurrence_count=0
generated_diagnostic_subject_occurrence_count=0
generated_schema_field_subject_occurrence_count=0
```

Subject-source comments and strings may remain diagnostic findings but never writers.

---

## 5. Writer Semantic Classes

```rust
enum WriterSemanticClass {
    NoWrite,
    ConstructionWrite,
    ProjectionCopy,
    DerivedLocalWrite,
    ConfigurationWrite,
    PolicyDecisionWrite,
    RegistryMutationWrite,
    RuntimeStateWrite,
    OutputAuthorityWrite,
    PromotionAuthorityWrite,
}
```

`writes_state=true` is allowed only for an actual assignment or mutation in the finding's semantic domain.

```text
struct field declaration   -> false
comment                    -> false
diagnostic string          -> false
report projection          -> false
test assertion             -> false
read-only guard            -> false
config initializer         -> true
local derived assignment   -> true
route registry mutation    -> true
output authority selection -> true
```

The presence of `symbol=` inside comments, strings, projections, tests or guards must never override the classified role.

---

## 6. Writer Counter Contract

```text
writer_count = count(access.writes_state=true)
```

```text
runtime_writer_count = count(
  writes_state=true
  AND writer_semantic_class IN {
    RegistryMutationWrite,
    RuntimeStateWrite,
    OutputAuthorityWrite,
    PromotionAuthorityWrite
  }
)
```

Required counters:

```text
construction_writer_count
derived_local_writer_count
configuration_writer_count
runtime_writer_count
projection_count
comment_count
test_count
comment_writer_count
projection_runtime_writer_count
test_runtime_writer_count
guard_writer_count
```

Required invariants:

```text
comment_writer_count=0
projection_runtime_writer_count=0
test_runtime_writer_count=0
guard_writer_count=0

writer_count
=
construction_writer_count
+ derived_local_writer_count
+ configuration_writer_count
+ runtime_writer_count
```

---

## 7. G209T0 Regression Fixture

Required fixture:

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g209t0_tensorcube_tensorcore_shadow_preflight.rs
```

When its matching occurrences remain comment and projection only:

```text
writer_count=0
runtime_writer_count=0
comment_writer_count=0
projection_runtime_writer_count=0
```

---

## 8. Primitive Authority Writer Graph

Every actual writer edge must resolve to:

```rust
struct CanonicalStateKey {
    domain: String,
    subsystem: String,
    state_name: String,
    subject_identity: Option<String>,
}

struct AuthorityScope {
    kind: String,
    identity: String,
    parent_identity: Option<String>,
}

struct PrimitiveAuthorityWriterEdge {
    edge_id: String,
    canonical_state_key: CanonicalStateKey,
    scope: AuthorityScope,
    authority_root_id: String,
    source_file: String,
    source_line_start: usize,
    source_line_end: usize,
    source_symbol: String,
    writer_semantic_class: WriterSemanticClass,
    authority_class: ReplacementAuthorityClass,
    write_operation: String,
    value_expression_digest: String,
    mutates_runtime: bool,
    promotion_relevant: bool,
}
```

Canonical state examples:

```text
tensorcube.route.replacement_enabled
tensorcube.route.requested
tensorcube.route.admitted
tensorcube.route.selected_route
tensorcube.route.dispatch_started
tensorcube.route.dispatch_completed
tensorcube.route.output_owner
tensorcube.governance.default_route_changed
tensorcube.governance.production_replacement_allowed
tensorcube.governance.production_replacement_executed
tensorcube.governance.performance_claim_allowed
tensorcube.governance.performance_claim_execution
```

Authority scope kinds include:

```text
test
report
artifact
route_registry
decode_run
training_run
benchmark_run
shadow_run
source_module
```

Authority roots include:

```text
configuration_loader
policy_resolver
admission_gate
route_selector
dispatch_owner
completion_witness
output_selector
route_registry
promotion_gate
performance_claim_gate
```

---

## 9. Same-State Same-Scope Conflict Derivation

A blocking conflict requires:

```text
same canonical state key
AND same authority scope
AND runtime-relevant writer classes
AND independent authority roots
AND no declared SSOT delegation relationship
```

A writer count greater than one does not itself prove conflict.

Required metrics:

```text
primitive_writer_edge_count
runtime_writer_edge_count
candidate_edge_pair_count
same_state_pair_count
same_state_same_scope_pair_count
independent_root_pair_count
compatible_pair_count
conflict_pair_count
unresolved_pair_count
```

Required:

```text
unresolved_pair_count=0
```

Every non-conflicting same-state pair must carry an exclusion reason such as:

```text
non_runtime_writer_class
non_overlapping_scope
same_authority_root
projection_only
observation_only
test_only
artifact_only
parent_child_authority_relation
```

---

## 10. Parent Readiness Retirement

The parent result `repository_ready_for_replace_02=true` is historical only.

```json
{
  "parent_patch_id": "ASH-TCU-REPLACE-01",
  "parent_ready_value": true,
  "parent_readiness_authority_valid": false,
  "parent_digest_disposition": [
    "historical_only",
    "superseded",
    "promotion_authority_forbidden"
  ],
  "pass": true
}
```

R1 readiness defaults to false and becomes true only from the complete repaired predicate conjunction.

---

## 11. Semantic Digest Reissue

R1 must issue a deterministic digest over:

```text
subject findings
writer semantics
lifecycle and governance inventories
canonical state keys
authority roots
primitive writer edges
conflict metrics
conflict and non-conflict receipts
```

Exclude:

```text
audit implementation source
audit-generated vocabulary
wall-clock timestamps
absolute local paths
output directory
JSON whitespace
parent digest lineage metadata
```

Required:

```text
r1_semantic_inventory_digest
!=
6e349b21616d0d9db8ef212f14c2b6b76693684d9ae8074da4819a81e2d45f30
```

REPLACE-02 may bind only the R1 digest.

---

## 12. Required Output Files

```text
workspace/runtime/tensorcube/
  ash_tcu_replace_01_r1_ownership_audit_runtime_artifact.json
  ash_tcu_replace_01_r1_self_scan_exclusion_receipt.json
  ash_tcu_replace_01_r1_generated_surface_isolation_receipt.json
  ash_tcu_replace_01_r1_writer_counter_semantics_receipt.json
  ash_tcu_replace_01_r1_primary_surface_counter_delta.json
  ash_tcu_replace_01_r1_canonical_state_key_registry.json
  ash_tcu_replace_01_r1_authority_root_registry.json
  ash_tcu_replace_01_r1_authority_root_relation_registry.json
  ash_tcu_replace_01_r1_primitive_writer_edge_graph.json
  ash_tcu_replace_01_r1_authority_conflict_derivation_receipt.json
  ash_tcu_replace_01_r1_authority_conflict_receipt.json
  ash_tcu_replace_01_r1_non_conflict_exclusion_receipt.json
  ash_tcu_replace_01_r1_parent_readiness_retirement_receipt.json
  ash_tcu_replace_01_r1_semantic_digest_reissue_receipt.json
  ash_tcu_replace_01_r1_parent_to_r1_delta_receipt.json
  ash_tcu_replace_01_r1_no_runtime_behavior_change_guard.json
  ash_tcu_replace_01_r1_no_replacement_enablement_guard.json
  ash_tcu_replace_01_r1_no_production_promotion_guard.json
  ash_tcu_replace_01_r1_no_performance_claim_guard.json
  ash_tcu_replace_01_r1_static_checks.json
  ash_tcu_replace_01_r1_verdict.json

artifacts/
  ASH_TCU_REPLACE_01_R1_LOCAL_MANIFEST.json
```

Artifacts and manifest are generated by Rust at runtime and are forbidden in the baked code ZIP.

---

## 13. Blocking Predicates

```text
TCU_REPLACE_01_R1_AUDIT_SELF_SCAN_EXCLUDED
TCU_REPLACE_01_R1_AUDIT_GENERATED_VOCABULARY_ISOLATED
TCU_REPLACE_01_R1_COMMENT_WRITER_COUNT_ZERO
TCU_REPLACE_01_R1_PROJECTION_RUNTIME_WRITER_COUNT_ZERO
TCU_REPLACE_01_R1_TEST_RUNTIME_WRITER_COUNT_ZERO
TCU_REPLACE_01_R1_READ_ONLY_GUARDS_NOT_WRITERS
TCU_REPLACE_01_R1_WRITER_COUNTER_DERIVATION_VALID
TCU_REPLACE_01_R1_REQUIRED_PRIMARY_SURFACES_PRESENT
TCU_REPLACE_01_R1_ALL_MATCHED_OCCURRENCES_CLASSIFIED
TCU_REPLACE_01_R1_ALL_REQUIRED_RUST_SOURCES_PARSED
TCU_REPLACE_01_R1_ALL_PRIMARY_FINDINGS_HAVE_AUTHORITY_CLASS
TCU_REPLACE_01_R1_PRIMITIVE_AUTHORITY_WRITER_EDGE_GRAPH_COMPLETE
TCU_REPLACE_01_R1_SAME_STATE_SAME_SCOPE_CONFLICT_DERIVATION_COMPLETE
TCU_REPLACE_01_R1_BLOCKING_AUTHORITY_CONFLICT_COUNT_ZERO
TCU_REPLACE_01_R1_PREMATURE_PARENT_REPLACE_02_READINESS_RETIRED
TCU_REPLACE_01_R1_PARENT_SEMANTIC_DIGEST_PROMOTION_AUTHORITY_RETIRED
TCU_REPLACE_01_R1_SEMANTIC_INVENTORY_DIGEST_REISSUED
TCU_REPLACE_01_R1_REISSUED_DIGEST_DIFFERS_FROM_PARENT
TCU_REPLACE_01_R1_NO_RUNTIME_BEHAVIOR_CHANGE
TCU_REPLACE_01_R1_NO_REPLACEMENT_ENABLEMENT
TCU_REPLACE_01_R1_NO_PRODUCTION_PROMOTION
TCU_REPLACE_01_R1_NO_PERFORMANCE_CLAIM
TCU_REPLACE_01_R1_ALL_BLOCKING_PREDICATES_PASS
```

---

## 14. No Runtime Behavior Change

```json
{
  "audit_binary_imports_wgpu": false,
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
  "optimizer_state_mutated": false,
  "pass": true
}
```

---

## 15. No Replacement, Production or Performance Promotion

```text
existing_false_replacement_default_changed_to_true=false
runtime_enable_flag_introduced=false
replacement_environment_variable_introduced=false
replacement_cli_enable_argument_introduced=false
admitted_replacement_policy_introduced=false
replacement_enabled_by_patch=false

default_route_adoption_executed=false
production_default_changed=false
production_replacement_allowed=false
production_replacement_executed=false
promotion_token_created=false
promotion_token_consumed=false
user_visible_activation_executed=false

performance_claim_allowed=false
operator_speedup_claim_allowed=false
decode_speedup_claim_allowed=false
training_speedup_claim_allowed=false
speedup_3_04_promoted=false
```

---

## 16. Runtime Command

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

## 17. Expected PASS State

```text
self_scan_occurrence_count=0
self_scan_digest_input_count=0
generated_vocabulary_subject_occurrence_count=0
generated_diagnostic_subject_occurrence_count=0
comment_writer_count=0
projection_runtime_writer_count=0
test_runtime_writer_count=0
guard_writer_count=0
unclassified_occurrence_count=0
source_parse_failure_count=0
unresolved_conflict_pair_count=0
blocking_authority_conflict_count=0
runtime_behavior_changed=false
replacement_enabled_by_patch=false
production_replacement_executed_by_patch=false
performance_claim_allowed_by_patch=false
```

---

## 18. REPLACE-02 Boundary

REPLACE-02 may begin only when:

```text
repository_ready_for_replace_02=true
new R1 semantic digest exists
primitive writer graph is complete
unresolved conflict pair count is zero
blocking conflict count is zero
parent readiness retirement receipt exists
parent digest retirement receipt exists
```

The parent digest `6e349b...` is forbidden as a REPLACE-02 authority parent.

---

## 19. Final Verdict

PASS marker:

```text
PASS_ASH_TCU_REPLACE_01_R1_AUDIT_SELF_SCAN_EXCLUDED_GENERATED_SURFACES_ISOLATED_WRITER_COUNTER_SEMANTICS_REPAIRED_PRIMITIVE_AUTHORITY_WRITER_EDGE_GRAPH_COMPLETE_SAME_STATE_SAME_SCOPE_CONFLICT_DERIVATION_COMPLETE_SEMANTIC_INVENTORY_DIGEST_REISSUED_PARENT_REPLACE_02_READINESS_RETIRED_NO_RUNTIME_BEHAVIOR_CHANGE_NO_REPLACEMENT_ENABLEMENT
```

HOLD marker:

```text
HOLD_ASH_TCU_REPLACE_01_R1_REPLACE_02_READINESS_NOT_PROVEN
```

---

## 20. Final Seal

```text
The ownership audit does not audit itself.
Audit-generated vocabulary does not become runtime evidence.
Comments, projections, tests and read-only guards do not inflate writer counts.
Every actual writer is represented by a canonical state, scope and authority-root edge.
Zero conflicts are claimed only after primitive edge-pair evaluation.
The parent digest remains historical only.
The parent REPLACE-02 readiness result is retired.
A new deterministic semantic inventory digest is issued.
No runtime behavior changed.
No TensorCube replacement was enabled.
No production promotion or performance claim occurred.
```