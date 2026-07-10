# ASH-TCU-K7N-C-R1B SPEC

## Title

Prediction Origin And Commit Provenance Split / Binding Authority Lineage Registry / Prepared-By Commit-Executed-By Evidence Separation / Registry v2 to v3 Metadata Migration / No Route State Change Seal

## Patch ID

```txt
ASH-TCU-K7N-C-R1B
```

## Status Target

```txt
PASS_ASH_TCU_K7N_C_R1B_PREDICTION_COMMIT_PROVENANCE_SPLIT_BINDING_AUTHORITY_LINEAGE_NO_ROUTE_STATE_CHANGE_SEAL
```

## Parent

```txt
ASH-TCU-K7N-C-R1A
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_C_R1A_REGISTRY_DIGEST_DOMAIN_SEPARATION_NON_RECURSIVE_LEDGER_TRANSITION_DIGEST_SEAL
```

Required prior verdict:

```txt
registry_digest_domains_separated_and_mutation_ledger_self_reference_removed
```

## Purpose

K7N-C-R1B separates bootstrap origin, prediction origin, preparation owner, commit executor, effective binding authority, prediction evidence, and runtime mutation evidence. It migrates the registry from v2 to v3 without changing route IDs, route slots, epoch, catalog, rollback history, logical mutation history, runtime output, or model state.

The existing Default binding has `bound_by_patch = ASH-TCU-K7N-B-PREDICTED`, which identifies prediction rather than the actual K7N-C commit. The existing mutation record also has a generic `evidence_id` that points to the proposal identity instead of the K7N-C RuntimeRouteMutation evidence. R1B replaces both ambiguous fields with typed provenance.

## Provenance Roles

Required distinct roles:

```txt
bootstrap_origin_patch
prediction_origin_patch
prepared_by_patch
commit_executed_by_patch
effective_binding_author_patch
```

Required Default binding values:

```txt
bootstrap_origin_patch = ASH-TCU-K7N-A
prediction_origin_patch = ASH-TCU-K7N-B
prepared_by_patch = ASH-TCU-K7N-B
commit_executed_by_patch = ASH-TCU-K7N-C
effective_binding_author_patch = ASH-TCU-K7N-C
```

Candidate, UserVisible, and Production remain bootstrap-owned by K7N-A.

## Binding Provenance Schema

Required schema version:

```txt
ash_tensorcube_route_binding_provenance_v1
```

Required fields:

```txt
slot
effective route ID
effective epoch
binding source
bootstrap origin patch
prediction origin patch
prepared-by patch
commit-executed-by patch
effective binding author patch
proposal ID
transaction ID
authority ID
commit ID
mutation ID
prediction evidence ID
runtime mutation evidence ID
provenance digest
```

## Binding v2

Required schema:

```txt
ash_tensorcube_route_binding_v2
```

Binding v2 must contain slot, route ID, source, epoch, explicit operator input, and a typed provenance object.

The v1 fields below must not exist in Binding v2:

```txt
bound_by_patch
runtime_mutation_evidence_id
```

Historical v1 structs may remain for explicit migration only.

## Mutation Record v3

Required schema:

```txt
ash_tensorcube_route_mutation_record_v3
```

Required fields:

```txt
mutation ID
proposal ID
transaction ID
authority ID
commit ID
slot
route before / after
epoch before / after
registry digest before
transition payload digest
prediction evidence ID
runtime mutation evidence ID
predicted-by patch
prepared-by patch
committed-by patch
mutation-record digest
```

The generic v2 field `evidence_id` must not exist in v3.

## Registry v3

Required registry schema:

```txt
ash_tensorcube_route_registry_v3
```

Registry v3 contains Binding v2 records, MutationRecord v3 records, catalog, rollback stack, mutation policy, genesis digest, and a v3 current registry digest.

Required current-registry digest domain:

```txt
ash.tensorcube.registry.current.v2
```

Required binding provenance digest domain:

```txt
ash.tensorcube.registry.binding_provenance.v1
```

Required mutation-record digest domain:

```txt
ash.tensorcube.registry.mutation_record.v2
```

## Explicit v2 to v3 Migration

Migration input authority must come from:

```txt
K7N-A bootstrap/genesis evidence
K7N-B prepared transaction
K7N-C committed transaction
K7N-C RuntimeRouteMutation evidence
R1A registry v2 migration record
R1A evidence digest-rebind receipt
```

The migration must not infer commit provenance from route names, catalog ordering, or patch constants alone.

Migration preserves:

```txt
registry instance ID
epoch
catalog
all four effective route IDs
binding sources and binding epochs
rollback stack logical content
mutation count
proposal / transaction / mutation identities
route before / route after
```

Migration may change only schema versions, metadata shape, evidence fields, provenance digests, mutation-record digest, and current registry digest.

## Identity Graph

Required identity equality:

```txt
binding.proposal_id = prepared.proposal_id = committed.proposal_id = mutation.proposal_id
binding.transaction_id = prepared.transaction_id = committed.transaction_id = mutation.transaction_id
binding.authority_id = committed.authority_id = mutation.authority_id
binding.commit_id = committed.commit_id = mutation.commit_id
binding.mutation_id = committed.mutation_id = mutation.mutation_id
binding.runtime_mutation_evidence_id = mutation.runtime_mutation_evidence_id = RuntimeRouteMutation.evidence_id
```

No orphan identity is allowed.

Prediction evidence identity and RuntimeRouteMutation evidence identity must be distinct typed fields.

## No Route State Change

R1B must prove:

```txt
Candidate unchanged
Default unchanged
UserVisible unchanged
Production unchanged
epoch remains 1
logical mutation count remains 1
rollback count remains 1
no route transaction committed
no runtime output change
no rollback execution
no model/optimizer/checkpoint mutation
no performance claim
```

## Evidence Rebind

R1B creates a derived provenance rebind receipt linking:

```txt
existing K7N-C RuntimeRouteMutation evidence ID
R1A registry v2 digest
R1B registry v3 digest
R1A schema migration ID
R1B provenance migration ID
same registry instance
same epoch
same mutation ID
same commit ID
```

This is not a second RuntimeRouteMutation event.

## Main Implementation

```txt
crates/burn_webgpu_backend/src/tensorcube_route_binding_provenance.rs
crates/burn_webgpu_backend/src/tensorcube_route_binding_v2.rs
crates/burn_webgpu_backend/src/tensorcube_route_mutation_record_v3.rs
crates/burn_webgpu_backend/src/tensorcube_route_registry_v3.rs
crates/burn_webgpu_backend/src/tensorcube_binding_provenance_migration_record.rs
crates/burn_webgpu_backend/src/tensorcube_registry_v2_to_v3_provenance_migration.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_c_r1b_*.rs
crates/orchestrator_local/src/ash_tcu_k7n_c_r1b_provenance_split_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_c_r1b_provenance_split_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_c_r1b_provenance_split_audit -- --repo-root <repo> --require-r1a-pass --diagnose-legacy-bound-by-patch --diagnose-legacy-generic-evidence-id --migrate-registry-v2-to-v3 --create-binding-provenance --split-prediction-and-commit-authority --create-mutation-record-v3 --validate-identity-graph --recalculate-registry-v3-digest --write-provenance-migration-receipt --write-evidence-provenance-rebind --preserve-registry-instance --preserve-route-state --preserve-epoch --preserve-mutation-history --no-route-mutation --no-runtime-output-claim --no-rollback-execution --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_C_R1B_PRIOR_R1A_RECEIPT
PASS_ASH_TCU_K7N_C_R1B_LEGACY_BOUND_BY_PATCH_DIAGNOSIS
PASS_ASH_TCU_K7N_C_R1B_LEGACY_GENERIC_EVIDENCE_ID_DIAGNOSIS
PASS_ASH_TCU_K7N_C_R1B_BINDING_PROVENANCE_SCHEMA
PASS_ASH_TCU_K7N_C_R1B_BINDING_SCHEMA_V2
PASS_ASH_TCU_K7N_C_R1B_MUTATION_RECORD_V3
PASS_ASH_TCU_K7N_C_R1B_PREDICTION_ORIGIN
PASS_ASH_TCU_K7N_C_R1B_PREPARED_BY_ORIGIN
PASS_ASH_TCU_K7N_C_R1B_COMMIT_EXECUTION_ORIGIN
PASS_ASH_TCU_K7N_C_R1B_EFFECTIVE_BINDING_AUTHORITY
PASS_ASH_TCU_K7N_C_R1B_PREDICTION_EVIDENCE_SPLIT
PASS_ASH_TCU_K7N_C_R1B_RUNTIME_MUTATION_EVIDENCE_SPLIT
PASS_ASH_TCU_K7N_C_R1B_IDENTITY_GRAPH
PASS_ASH_TCU_K7N_C_R1B_REGISTRY_V2_TO_V3_MIGRATION
PASS_ASH_TCU_K7N_C_R1B_REGISTRY_INSTANCE_PRESERVED
PASS_ASH_TCU_K7N_C_R1B_ROUTE_STATE_PRESERVED
PASS_ASH_TCU_K7N_C_R1B_EPOCH_PRESERVED
PASS_ASH_TCU_K7N_C_R1B_MUTATION_HISTORY_PRESERVED
PASS_ASH_TCU_K7N_C_R1B_EVIDENCE_PROVENANCE_REBIND
PASS_ASH_TCU_K7N_C_R1B_ORIGINAL_RECEIPTS_NOT_REWRITTEN
PASS_ASH_TCU_K7N_C_R1B_NO_ROUTE_MUTATION
PASS_ASH_TCU_K7N_C_R1B_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_C_R1B_NO_ROLLBACK_EXECUTION
PASS_ASH_TCU_K7N_C_R1B_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_C_R1B_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_C_R1B_PREDICTION_COMMIT_PROVENANCE_SPLIT_BINDING_AUTHORITY_LINEAGE_NO_ROUTE_STATE_CHANGE_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

All IDs, provenance values, and digests must be read from actual K7N-A/B/C and R1A runtime artifacts. Example IDs must not be hardcoded.

## Recommended Next Patch

```txt
ASH-TCU-K7N-C-R1C
Explicit Commit Authority Mutation Policy SSOT / Disabled ExplicitCommitAuthorityOnly RuntimeManaged / No Hidden Commit Bypass / No Route State Change Seal
```

## Final Seal

R1B separates prediction, preparation, commit execution, and effective binding authority. K7N-B remains the owner of the prepared prediction, K7N-C remains the owner of the actual runtime commit, and K7N-A remains the origin of unchanged bootstrap bindings. Registry identity, epoch, route state, mutation history, rollback history, runtime output, model state, and performance authority remain unchanged.