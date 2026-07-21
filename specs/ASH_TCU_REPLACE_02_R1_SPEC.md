# ASH-TCU-REPLACE-02-R1

## Parent Artifact Explicit JSON Path Binding / Recursive First-Match Key Lookup Retirement / R1 Ancestor Digest Shadowing Prevention / Semantic Closure Digest Exact Ownership / Verdict Readiness Exact Ownership / Parent Binding Diagnostic Actual-vs-Expected Materialization / No Policy Semantic Change / No Runtime Behavior Change / No Replacement Enablement Seal

## 0. Patch metadata

- Patch ID: `ASH-TCU-REPLACE-02-R1`
- Parent implementation: `ASH-TCU-REPLACE-02`
- Upstream audit parent: `ASH-TCU-REPLACE-01-R2`
- Parent schema: `ash.tcu.replace.01.r2.ownership_audit.runtime_artifact.v1`
- Expected parent semantic digest: `7cd333f938c4908e52e3ddf9fcd8e41d7c518bd6dbdd5a5be72fe1e0fca52f9d`
- Expected route replacement allowlist digest: `6ec309aa7fb71f1ce0c96747ed50b9528c531eb8a9183499cb5532a8199c6375`
- Required parent readiness: `repository_ready_for_replace_02=true`
- Runtime schema: `ash.tcu.replace.02.r1.parent_binding_repair.runtime_artifact.v1`
- Modified binary: `crates/orchestrator_local/src/bin/ash_tcu_replace_02_policy_snapshot_audit.rs`
- Policy semantic change: forbidden
- Runtime route change: forbidden
- Replacement enablement: forbidden
- Production promotion: forbidden

## 1. Defect

The parent R2 artifact contains repeated key names at different lineage levels. In particular:

- `/parent_lineage/semantic_inventory_digest` owns the historical R1 digest.
- `/semantic_digest_closure/semantic_inventory_digest` owns the current R2 digest.
- `/verdict/semantic_inventory_digest` reports the current digest as verdict evidence.

The original REPLACE-02 audit used recursive first-match lookup. Its result depended on traversal order and could bind the historical R1 digest instead of the current R2 closure digest.

This is a parent artifact path-ownership defect. It is not parent artifact corruption, policy semantic failure, compatibility parity failure, runtime behavior change, or replacement enablement.

## 2. Required authority paths

The following immutable path registry is the only authority for parent binding:

| Binding field | JSON pointer | Ownership |
|---|---|---|
| patch ID | `/patch_id` | top-level artifact identity |
| runtime schema | `/schema` | top-level artifact identity |
| semantic inventory digest | `/semantic_digest_closure/semantic_inventory_digest` | current semantic closure |
| route replacement allowlist digest | `/semantic_digest_closure/route_replacement_allowlist_digest` | current semantic closure |
| REPLACE-02 readiness | `/verdict/repository_ready_for_replace_02` | final verdict |

No alias, ancestor path, key-name search, value-coincidence search, first-match search, or last-match search may supply an authority-bearing value.

## 3. Validation order

The audit must execute in this order:

1. Parse the parent JSON.
2. Read `/patch_id` and `/schema` using exact JSON pointers.
3. Validate patch ID and schema.
4. Select the schema-specific path registry.
5. Read semantic closure digest and allowlist digest from exact closure paths.
6. Read readiness from the exact verdict path.
7. Materialize actual-vs-expected comparisons.
8. Construct `ParentReplacementAuditBinding` only after every comparison passes.
9. Continue the unchanged REPLACE-02 policy, projection, and writer-retirement audit.

Unknown parent schemas fail closed. They must never trigger recursive fallback.

## 4. Recursive lookup retirement

The following functions must not control parent acceptance:

- `find_first_string`
- `find_first_bool`
- `find_first_value`
- `find_last_string`
- any search selecting a value because it equals the expected digest

Required metrics:

```text
recursive_parent_key_lookup_call_count=0
authority_first_match_lookup_count=0
authority_last_match_lookup_count=0
authority_value_search_lookup_count=0
```

A recursive traversal may remain only as diagnostic enumeration of all same-named occurrences. Such traversal must receive the already-fixed selected authority path and may not choose authority.

## 5. Strict path and type readers

Authority reads must use `serde_json::Value::pointer` with the registry pointer.

Missing paths fail with:

```text
FAIL_TCU_REPLACE_02_R1_PARENT_REQUIRED_PATH_MISSING
```

Wrong JSON types fail with:

```text
FAIL_TCU_REPLACE_02_R1_PARENT_FIELD_TYPE_MISMATCH
```

Forbidden coercions include:

- `"true"` to `true`
- `1` to `true`
- `null` to `false`
- number or boolean to string
- absent value to an empty string or default boolean

## 6. Ancestor shadowing prevention

The audit must enumerate all occurrences of:

- `semantic_inventory_digest`
- `route_replacement_allowlist_digest`
- `repository_ready_for_replace_02`

Each occurrence receipt contains:

- full JSON pointer
- value
- selected flag

Required invariants:

```text
semantic_digest_selected_authority_count=1
allowlist_digest_selected_authority_count=1
readiness_selected_authority_count=1
ancestor_digest_selected_as_current_count=0
historical_readiness_selected_as_current_count=0
```

Multiple same-named fields at different owned paths are not automatically corruption. The selected authority must nevertheless be exactly one.

## 7. Diagnostics

Every comparison record must include:

- field ID
- JSON pointer
- ownership class
- actual value
- expected value
- matched flag
- failure ID when mismatched

A semantic mismatch must report:

```text
FAIL_TCU_REPLACE_02_R1_PARENT_SEMANTIC_DIGEST_MISMATCH:
field=SemanticInventoryDigest
path=/semantic_digest_closure/semantic_inventory_digest
actual=<actual>
expected=7cd333f938c4908e52e3ddf9fcd8e41d7c518bd6dbdd5a5be72fe1e0fca52f9d
ownership=SemanticDigestClosure
```

Equivalent materialization is required for patch ID, schema, allowlist digest, readiness, missing path, and wrong type failures.

## 8. Policy semantic preservation

R1 must not change:

- `TensorCubeReplacementMode`
- `TensorCubeReplacementPolicySource`
- `TensorCubeReplacementPolicyScope`
- `TensorCubeReplacementPolicySnapshot`
- `LegacyReplacementBooleanMatrix`
- `LegacyReplacementBooleanView`
- strict legacy matrix import semantics
- compatibility projection semantics
- snapshot digest algorithm
- migrated Q-wave consumer behavior

The code bake must modify only the REPLACE-02 audit binary unless compile metadata requires a narrow mechanical update.

Required metrics:

```text
policy_module_semantic_change_count=0
projection_semantic_change_count=0
legacy_matrix_semantic_change_count=0
snapshot_digest_algorithm_change_count=0
```

## 9. Safety invariants

```text
runtime_route_mutation_count=0
registry_mutation_count=0
route_epoch_increment_count=0
default_route_change_count=0
replacement_enablement_count=0
production_replacement_execution_count=0
promotion_token_consumption_count=0
gpu_command_submission_count=0
model_output_change_count=0
training_output_change_count=0
performance_claim_count=0
```

## 10. Runtime outputs

```text
workspace/runtime/tensorcube/
  ash_tcu_replace_02_r1_parent_binding_repair_runtime_artifact.json
  ash_tcu_replace_02_r1_parent_binding_receipt.json
  ash_tcu_replace_02_r1_parent_path_registry.json
  ash_tcu_replace_02_r1_parent_field_read_receipt.json
  ash_tcu_replace_02_r1_parent_binding_comparison_receipt.json
  ash_tcu_replace_02_r1_semantic_digest_shadowing_receipt.json
  ash_tcu_replace_02_r1_allowlist_digest_shadowing_receipt.json
  ash_tcu_replace_02_r1_readiness_shadowing_receipt.json
  ash_tcu_replace_02_r1_recursive_lookup_retirement_receipt.json
  ash_tcu_replace_02_r1_policy_semantic_preservation_receipt.json
  ash_tcu_replace_02_r1_no_runtime_behavior_change_guard.json
  ash_tcu_replace_02_r1_no_replacement_enablement_guard.json
  ash_tcu_replace_02_r1_no_production_promotion_guard.json
  ash_tcu_replace_02_r1_static_checks.json
  ash_tcu_replace_02_r1_verdict.json

artifacts/
  ASH_TCU_REPLACE_02_R1_LOCAL_MANIFEST.json
```

## 11. Required metrics

### Path registry

```text
parent_path_spec_count=5
parent_path_spec_unique_pointer_count=5
parent_path_spec_unique_field_count=5
missing_parent_path_spec_count=0
duplicate_parent_json_pointer_count=0
duplicate_parent_field_id_count=0
```

### Field reads

```text
parent_required_field_count=5
parent_required_field_read_success_count=5
parent_required_field_missing_count=0
parent_required_field_type_mismatch_count=0
```

### Comparisons

```text
parent_binding_comparison_count=5
parent_binding_match_count=5
parent_binding_mismatch_count=0
parent_patch_id_mismatch_count=0
parent_schema_mismatch_count=0
parent_semantic_digest_mismatch_count=0
parent_allowlist_digest_mismatch_count=0
parent_readiness_mismatch_count=0
```

## 12. Blocking predicates

```text
TCU_REPLACE_02_R1_PARENT_PATH_REGISTRY_COMPLETE
TCU_REPLACE_02_R1_PARENT_PATH_REGISTRY_UNIQUE
TCU_REPLACE_02_R1_TOP_LEVEL_IDENTITY_PATHS_EXACT
TCU_REPLACE_02_R1_SEMANTIC_CLOSURE_PATH_EXACT
TCU_REPLACE_02_R1_ALLOWLIST_CLOSURE_PATH_EXACT
TCU_REPLACE_02_R1_VERDICT_READINESS_PATH_EXACT
TCU_REPLACE_02_R1_RECURSIVE_PARENT_LOOKUP_RETIRED
TCU_REPLACE_02_R1_CURRENT_R2_DIGEST_SELECTED_ONCE
TCU_REPLACE_02_R1_R1_ANCESTOR_DIGEST_NOT_SELECTED
TCU_REPLACE_02_R1_CURRENT_VERDICT_READINESS_SELECTED_ONCE
TCU_REPLACE_02_R1_HISTORICAL_READINESS_NOT_SELECTED
TCU_REPLACE_02_R1_ACTUAL_EXPECTED_DIAGNOSTICS_COMPLETE
TCU_REPLACE_02_R1_NO_POLICY_MODE_SEMANTIC_CHANGE
TCU_REPLACE_02_R1_NO_LEGACY_MATRIX_SEMANTIC_CHANGE
TCU_REPLACE_02_R1_NO_PROJECTION_SEMANTIC_CHANGE
TCU_REPLACE_02_R1_NO_SNAPSHOT_DIGEST_ALGORITHM_CHANGE
TCU_REPLACE_02_R1_NO_RUNTIME_BEHAVIOR_CHANGE
TCU_REPLACE_02_R1_NO_REPLACEMENT_ENABLEMENT
TCU_REPLACE_02_R1_NO_DEFAULT_ROUTE_CHANGE
TCU_REPLACE_02_R1_NO_REGISTRY_MUTATION
TCU_REPLACE_02_R1_NO_PRODUCTION_PROMOTION
TCU_REPLACE_02_R1_NO_GPU_COMMAND_SUBMISSION
TCU_REPLACE_02_R1_NO_PERFORMANCE_CLAIM
```

## 13. Required tests

```text
top_level_patch_id_is_selected
top_level_schema_is_selected
ancestor_digest_does_not_shadow_current_digest
current_digest_selected_by_exact_pointer
verdict_readiness_is_selected
object_key_order_does_not_change_selection
ancestor_block_before_closure_does_not_change_selection
ancestor_block_after_closure_does_not_change_selection
missing_exact_digest_path_does_not_use_ancestor_digest
missing_exact_allowlist_path_does_not_use_alias
missing_verdict_readiness_does_not_use_historical_readiness
wrong_readiness_type_fails_closed
null_digest_fails_type_check
diagnostic_inventory_reports_selected_and_shadowing_occurrences
digest_mismatch_prints_actual_expected_path_and_ownership
```

The actual user parent artifact must pass despite containing the historical R1 digest before the current R2 closure digest.

## 14. Readiness

```text
repository_ready_for_replace_03 =
    original_replace_02_readiness
    && exact_path_binding_pass
    && recursive_lookup_retired
    && ancestor_shadowing_prevented
    && policy_semantic_preservation_pass
```

R1 repairs audit acceptance only. It does not independently create REPLACE-03 readiness.

## 15. PASS and HOLD

PASS:

```text
PASS_ASH_TCU_REPLACE_02_R1_PARENT_ARTIFACT_EXPLICIT_JSON_PATHS_BOUND_RECURSIVE_FIRST_MATCH_AUTHORITY_LOOKUP_RETIRED_R1_ANCESTOR_DIGEST_SHADOWING_PREVENTED_SEMANTIC_CLOSURE_DIGEST_EXACTLY_OWNED_VERDICT_READINESS_EXACTLY_OWNED_PARENT_BINDING_ACTUAL_EXPECTED_DIAGNOSTICS_MATERIALIZED_NO_POLICY_SEMANTIC_CHANGE_NO_RUNTIME_BEHAVIOR_CHANGE_NO_REPLACEMENT_ENABLEMENT
```

HOLD:

```text
HOLD_ASH_TCU_REPLACE_02_R1_PARENT_ARTIFACT_PATH_OWNERSHIP_OR_POLICY_PRESERVATION_INCOMPLETE
```

## 16. Final seal

REPLACE-02-R1 passes only when parent authority is selected by exact schema-owned JSON paths, the historical R1 digest cannot shadow the current R2 closure digest, historical readiness cannot shadow final verdict readiness, every mismatch exposes path and actual-vs-expected values, policy semantics remain unchanged, and no runtime behavior or replacement state changes.
