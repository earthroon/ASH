# ASH-TCU-REPLACE-04-R2-R1

## Active Authorization Anchor Schema Version Rebind
## ShadowEntryPreparation Variant Contract Seal
## ActiveShadowEntry Scope Versioning
## Legacy V1 Reader Compatibility Boundary
## Anchor Digest Domain Separation
## REPLACE-05 Readiness Revalidation
## No Runtime Snapshot Mutation / No Active Route Mutation / No Production Replacement

### Parent binding

```text
parent_patch_id=ASH-TCU-REPLACE-04-R2
parent_schema=ash.tcu.replace.04.r2.active_edge_audit.runtime_artifact.v1
parent_semantic_digest=977ba4e390f26df3546eb11bf035c009e7d119de139e187138ee3f22740ddd97
parent_execution_digest=33767752832207db3ba67e4531bd5d78b1553f72ee2c6cc6be1a324fe657d1e0
parent_spec_commit=82edeec4573e316a1376a28d821930023f31e962
active_root_digest=f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
active_root_mode=disabled
```

The parent R2 artifact serialized `shadow_entry_preparation` and `active_shadow_entry` under `ash.tcu.replace.04.authorization_anchor.v1`. R2-R1 treats this as a blocking schema/variant contract mismatch.

### Frozen V1 contract

V1 schema remains `ash.tcu.replace.04.authorization_anchor.v1`.

V1 kinds are limited to:

```text
candidate_preparation
apply_preparation
canary_preparation
production_preparation
```

V1 scopes are limited to:

```text
candidate
route
```

V1 must reject `shadow_entry_preparation`, `active_shadow_entry`, unknown kind, unknown scope, missing schema, and unknown schema. Existing valid V1 candidate and route anchors must retain their established semantic digests.

### V2 contract

Introduce `ash.tcu.replace.04.authorization_anchor.v2`.

V2 adds:

```text
authorization_kind=shadow_entry_preparation
authorization_scope.kind=active_shadow_entry
```

`ShadowEntryPreparation` is valid only with `ActiveShadowEntry`, active composition-root authority, Disabled source mode, ShadowOnly target mode, and dry-run-only restrictions. It must not grant route selection, output ownership, default-route mutation, or production replacement.

### Schema-first dispatch

Required order:

```text
1. read top-level schema
2. exact-match schema identifier
3. decode the matching versioned wire DTO
4. validate version-specific kind/scope vocabulary
5. validate semantic digest
6. convert to canonical validated semantics
```

Forbidden:

```text
latest-type-first decoding
serde untagged version guessing
unknown-schema fallback
V2-to-V1 fallback
silent V1-to-V2 upgrade
silent V2-to-V1 downgrade
```

Required counts:

```text
schema_dispatch_owner_count=1
unknown_schema_fallback_count=0
version_guessing_count=0
untagged_deserialization_count=0
v2_to_v1_fallback_count=0
```

### Digest domains

V1 digest behavior is preserved exactly. V2 uses a distinct domain:

```text
ash.tcu.replace.authorization-anchor.digest.v2
```

Required:

```text
legacy_v1_digest_regression_mismatch_count=0
cross_version_equal_digest_count=0
cross_version_anchor_replay_acceptance_count=0
```

The repaired V2 anchor digest must differ from the parent V1-labeled active anchor digest `4d6e855de54d207475d961f6a5df73ad4bc486dd9a521ec42b9fac76bdf83661`.

### Migration boundary

Provide explicit V1-to-V2 migration that preserves common semantics, changes schema, recomputes the V2 digest, emits a migration receipt, and never fabricates `ActiveShadowEntry`. No generic V2-to-V1 migration API may exist.

### Active authorization reissue

Reissue the active anchor as V2 with:

```text
composition_root_id=repository_default_replacement_context
source_snapshot_digest=f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
source_mode=disabled
authorized_target_mode=shadow_only
dry_run_only=true
```

Canonical validation status is `validation_executed_and_matched`. Legacy `evidence_status=executed_and_matched` may remain only as a labeled compatibility projection and must not enter readiness logic.

### Transaction and receipt reissue

Because the transaction binds `authorization_anchor_digest`, the active transaction and dry-run receipt must be reissued.

Preserve:

```text
authority_domain=active_composition_root
runtime_snapshot_mode=disabled
logical_source_mode=disabled
proposed_target_mode=shadow_only
effective_runtime_mode=disabled
prior_transaction_digest=null
store_eligible=true
apply_eligible=false
```

Required:

```text
reissued_transaction.authorization_anchor_digest=repaired_v2_anchor_digest
reissued_transaction_digest!=f944fd218374b5d8a4ad92a20719e0cd3edbc148638ac48cc0fb12c7868b3561
reissued_receipt_digest!=d2e30a9625b7ea4804979ad27b036cd1a89f61400329cda436a5c424babe8714
parent_anchor_status=superseded_by_authorization_schema_rebind
parent_transaction_status=superseded_by_authorization_schema_rebind
parent_receipt_status=superseded_by_authorization_schema_rebind
```

### REPLACE-05 readiness

Parent readiness is not inherited directly. Evaluation starts false and is recomputed after V1 compatibility, V2 validation, schema dispatch, digest separation, replay rejection, anchor/transaction/receipt reissue, and safety checks.

Final allowed readiness:

```text
active_composition_root_transition_binding_ready=true
prepared_transition_store_readiness=true
active_transition_apply_readiness=false
active_route_ownership_readiness=false
repository_ready_for_replace_05=true
replace_05_readiness_scope=prepared_transition_store_and_single_use_consumption_contract_only
```

No apply, activation, route ownership, or production readiness may be inferred.

### Safety

All of the following remain zero:

```text
base_graph_change_count
active_eligibility_change_count
runtime_snapshot_mutation_count
runtime_context_replacement_count
active_route_mutation_count
default_route_mutation_count
registry_mutation_count
route_epoch_increment_count
route_select_permit_count
output_ownership_permit_count
default_route_change_permit_count
production_replacement_permit_count
production_replacement_execution_count
gpu_command_submission_count
performance_claim_count
```

Output parity is not executed:

```text
executed_output_parity=false
executed_output_parity_status=not_executed_static_no_change_evidence_only
```

### Runtime artifact

```text
schema=ash.tcu.replace.04.r2.r1.authorization_schema_rebind.runtime_artifact.v1
path=workspace/runtime/tensorcube/ash_tcu_replace_04_r2_r1_authorization_schema_rebind_runtime_artifact.json
```

### PASS marker

```text
PASS_ASH_TCU_REPLACE_04_R2_R1_ACTIVE_AUTHORIZATION_ANCHOR_SCHEMA_REBOUND_TO_V2_SHADOW_ENTRY_PREPARATION_VARIANT_CONTRACT_SEALED_ACTIVE_SHADOW_ENTRY_SCOPE_VERSIONED_LEGACY_V1_READER_COMPATIBILITY_BOUNDARY_PROVEN_EXPLICIT_SCHEMA_DISPATCH_ESTABLISHED_NO_SILENT_VERSION_FALLBACK_ANCHOR_DIGEST_DOMAINS_SEPARATED_ACTIVE_TRANSACTION_AND_DRY_RUN_RECEIPT_REISSUED_REPLACE_05_STORE_ONLY_READINESS_REVALIDATED_NO_RUNTIME_SNAPSHOT_MUTATION_NO_ACTIVE_ROUTE_MUTATION_NO_PRODUCTION_REPLACEMENT
```

Recommended next patch is ASH-TCU-REPLACE-05 Prepared Transition Store / Single-Use Transaction Consumption Contract / Authorization Freshness and Replay Gate / Rollback Precondition Revalidation / Active-Domain Dry-Run Transaction Persistence / No Apply Execution / No Route Ownership / No Default Route Mutation / No Production Replacement Seal.
