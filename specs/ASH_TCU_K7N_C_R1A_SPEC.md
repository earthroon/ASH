# ASH-TCU-K7N-C-R1A SPEC

## Title

Registry Digest Domain Separation / Non-Recursive Mutation Ledger Transition Digest / Canonical Current Registry Digest SSOT / K7N-B Predicted K7N-C Actual Parity Repair Seal

## Patch ID

```txt
ASH-TCU-K7N-C-R1A
```

## Status Target

```txt
PASS_ASH_TCU_K7N_C_R1A_REGISTRY_DIGEST_DOMAIN_SEPARATION_NON_RECURSIVE_LEDGER_TRANSITION_DIGEST_SEAL
```

## Parent

```txt
ASH-TCU-K7N-C
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_C_PREPARED_TRANSACTION_COMMIT_RUNTIME_CAS_DEFAULT_ROUTE_ADOPTION_NO_USER_VISIBLE_NO_PRODUCTION_SEAL
```

Required prior verdict:

```txt
prepared_default_route_transaction_committed_by_runtime_cas_epoch_and_digest_transition_verified
```

## Purpose

K7N-C-R1A removes the recursive digest dependency created when a mutation-ledger record stores `registry_digest_after` while that ledger record is itself part of the final registry digest input.

The final `current_registry_digest` becomes the sole canonical digest of the complete registry state. The mutation ledger no longer stores a value that claims to equal the digest of the registry containing that same ledger. Instead it stores a non-recursive `transition_payload_digest` and a sealed `mutation_record_digest`.

The original K7N-C receipts and RuntimeRouteMutation evidence must not be rewritten. R1A creates an explicit registry-v1 to registry-v2 migration, preserves registry identity and route state, and writes a derived digest-rebind receipt.

## Confirmed Legacy Condition

The K7N-C committed registry contains:

```txt
current_registry_digest
mutation_ledger[].registry_digest_before
mutation_ledger[].registry_digest_after
```

`mutation_ledger[].registry_digest_after` differs from the final `current_registry_digest`. Fixed-count rehashing does not resolve the semantic recursion and is forbidden.

## Digest SSOT

Required digest domains:

```txt
ash.tensorcube.registry.snapshot.v1
ash.tensorcube.registry.transition.v1
ash.tensorcube.registry.mutation_record.v1
ash.tensorcube.registry.current.v1
```

All digests use canonical UTF-8 JSON, recursively sorted object keys, stable enum and array ordering, SHA-256, lowercase hexadecimal output, and explicit length framing:

```txt
domain_length_u32_le
domain_utf8
payload_length_u64_le
canonical_payload_utf8
```

## Transition Payload

`TensorCubeRouteTransitionPayload` contains only facts known before final ledger insertion:

```txt
transaction ID
proposal ID
registry instance ID
slot
route before / after
epoch before / after
registry digest before
binding digest before / after
rollback snapshot digest
capability execution / dispatch / readback references
```

It must not contain the final registry digest, its own digest, a mutation-record digest, or commit digest.

## Mutation Record v2

Required schema:

```txt
ash_tensorcube_route_mutation_record_v2
```

Required fields:

```txt
mutation ID
transaction ID
proposal ID
slot
route before / after
epoch before / after
registry digest before
transition payload digest
mutation record digest
evidence ID
```

The v1 field `registry_digest_after` must not exist in the v2 record, even as a null alias.

## Registry v2

Required schema:

```txt
ash_tensorcube_route_registry_v2
```

The final registry digest covers registry schema, registry instance, epoch, catalog, bindings, rollback stack, v2 mutation ledger, mutation policy, and genesis digest. It excludes only its own digest field and non-canonical diagnostics.

Required calculation order:

```txt
1. validate immutable before registry
2. build transition payload
3. calculate transition payload digest
4. build and seal mutation record v2
5. append sealed record to the staged v2 ledger
6. preserve rollback snapshot and route bindings
7. calculate final current registry digest exactly once
8. validate the complete v2 registry
```

Forbidden:

```txt
rehash twice
rehash for a fixed iteration count
rehash until repetition
copy an intermediate digest into the ledger
```

## Explicit Migration

R1A must explicitly migrate v1 to v2. Silent serde defaults, hidden field aliases, and guessed legacy semantics are forbidden.

Migration preconditions:

```txt
K7N-C status and verdict valid
registry instance present
legacy epoch = 1
Default = TensorCube candidate
UserVisible = Burn baseline
Production = Burn baseline
mutation ledger count = 1
rollback stack count = 1
committed transaction and RuntimeRouteMutation evidence present
```

Migration preserves:

```txt
registry instance ID
epoch
catalog
all four bindings
rollback stack logical content
mutation identity
transaction identity
proposal identity
logical mutation count
```

Migration may change only registry schema, mutation-record schema, digest fields, and final canonical digest.

The original K7N-C receipt and evidence must remain byte-identical.

## Prediction and Actual Parity

K7N-B prepared state and K7N-C committed state must be reconstructed through the same shared digest core.

Required:

```txt
predicted transition payload = actual transition payload
predicted transition digest = actual transition digest
predicted mutation record v2 = actual mutation record v2
predicted mutation-record digest = actual mutation-record digest
```

The v2 final registry digest is calculated from the migrated actual state after all child records are sealed.

## Evidence Rebind

R1A creates a derived receipt binding:

```txt
existing RuntimeRouteMutation evidence ID
legacy v1 registry digest
new v2 registry digest
schema migration ID
same registry instance
same epoch
same mutation ID
```

This is not a second route mutation.

## No-State-Change Guards

R1A must prove:

```txt
Candidate unchanged
Default unchanged
UserVisible unchanged
Production unchanged
epoch remains 1
logical mutation count remains 1
rollback count remains 1
no new route transaction committed
no runtime output change
no rollback execution
no weight/checkpoint mutation
no performance claim
```

## Main Implementation

```txt
crates/burn_webgpu_backend/src/tensorcube_digest_domain.rs
crates/burn_webgpu_backend/src/tensorcube_canonical_digest.rs
crates/burn_webgpu_backend/src/tensorcube_route_transition_payload.rs
crates/burn_webgpu_backend/src/tensorcube_route_registry_digest.rs
crates/burn_webgpu_backend/src/tensorcube_route_mutation_record_v2.rs
crates/burn_webgpu_backend/src/tensorcube_route_registry_v2.rs
crates/burn_webgpu_backend/src/tensorcube_registry_schema_migration_record.rs
crates/burn_webgpu_backend/src/tensorcube_registry_v1_to_v2_migration.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_c_r1a_*.rs
crates/orchestrator_local/src/ash_tcu_k7n_c_r1a_digest_semantics_repair_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_c_r1a_digest_semantics_repair_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_c_r1a_digest_semantics_repair_audit -- --repo-root <repo> --require-k7n-c-pass --diagnose-legacy-recursive-digest --migrate-registry-v1-to-v2 --create-transition-payload-digest --create-mutation-record-digest --recalculate-current-registry-digest --verify-non-recursive-digest-domains --verify-k7n-b-predicted-k7n-c-actual-parity --write-schema-migration-receipt --write-evidence-digest-rebind --preserve-registry-instance --preserve-route-bindings --preserve-epoch --no-route-mutation --no-runtime-output-claim --no-rollback-execution --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_C_R1A_PRIOR_K7N_C_RECEIPT
PASS_ASH_TCU_K7N_C_R1A_LEGACY_RECURSIVE_DIGEST_DIAGNOSIS
PASS_ASH_TCU_K7N_C_R1A_CANONICAL_DIGEST_HELPER
PASS_ASH_TCU_K7N_C_R1A_DIGEST_DOMAIN_SEPARATION
PASS_ASH_TCU_K7N_C_R1A_TRANSITION_PAYLOAD_DIGEST
PASS_ASH_TCU_K7N_C_R1A_MUTATION_RECORD_V2
PASS_ASH_TCU_K7N_C_R1A_MUTATION_RECORD_DIGEST
PASS_ASH_TCU_K7N_C_R1A_REGISTRY_V1_TO_V2_MIGRATION
PASS_ASH_TCU_K7N_C_R1A_REGISTRY_INSTANCE_PRESERVED
PASS_ASH_TCU_K7N_C_R1A_ROUTE_BINDINGS_PRESERVED
PASS_ASH_TCU_K7N_C_R1A_EPOCH_PRESERVED
PASS_ASH_TCU_K7N_C_R1A_NON_RECURSIVE_CURRENT_REGISTRY_DIGEST
PASS_ASH_TCU_K7N_C_R1A_K7N_B_PREDICTED_K7N_C_ACTUAL_PARITY
PASS_ASH_TCU_K7N_C_R1A_EVIDENCE_DIGEST_REBIND
PASS_ASH_TCU_K7N_C_R1A_LEGACY_RECEIPT_NOT_REWRITTEN
PASS_ASH_TCU_K7N_C_R1A_NO_FIXED_ITERATION_REHASH
PASS_ASH_TCU_K7N_C_R1A_NO_ROUTE_MUTATION
PASS_ASH_TCU_K7N_C_R1A_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_C_R1A_NO_ROLLBACK_EXECUTION
PASS_ASH_TCU_K7N_C_R1A_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_C_R1A_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_C_R1A_REGISTRY_DIGEST_DOMAIN_SEPARATION_NON_RECURSIVE_LEDGER_TRANSITION_DIGEST_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

All IDs and digest values must be derived from actual K7N-B and K7N-C runtime artifacts. No example digest may be hardcoded.

## Recommended Next Patch

```txt
ASH-TCU-K7N-C-R1B
Prediction Origin And Commit Provenance Split / Prepared-By Commit-Executed-By Registry Metadata / No Route State Change Seal
```

## Final Seal

R1A installs a non-recursive digest model. The ledger proves the transition and record; the final registry digest proves the complete registry containing that sealed ledger. Registry identity, epoch, route bindings, rollback history, and logical mutation history are preserved without rewriting original evidence.