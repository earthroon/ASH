# ASH-TCU-REPLACE-04-R1

## Active Composition-Root Snapshot Binding / Dry-Run Fixture Authority Isolation / Runtime Snapshot Mode vs Logical Transaction Source State Separation / Transaction Source Snapshot Digest Truth Repair / Prior Prepared Transaction State Ownership / Apply-Preparation Chain Provenance Binding / REPLACE-05 Readiness Reblock / No Active Route Mutation / No Production Replacement Seal

## 0. Metadata

- Patch: `ASH-TCU-REPLACE-04-R1`
- Parent: `ASH-TCU-REPLACE-04`
- Parent schema: `ash.tcu.replace.04.transition_transaction_audit.runtime_artifact.v1`
- Parent semantic digest: `a182f14b60d9bb2433487f0382f91a4b295e6167bfb86a6e9991337edef56c00`
- Parent execution digest: `cda319206c297925466a77fe57308c74fd7637c8c92ca69b488cc427215560a3`
- Parent spec commit: `53edcb94caa1a2750b4b27fd2aa0f235c0a0e664`
- R1 schema: `ash.tcu.replace.04.r1.snapshot_binding_repair.runtime_artifact.v1`
- R1 artifact: `workspace/runtime/tensorcube/ash_tcu_replace_04_r1_snapshot_binding_repair_runtime_artifact.json`
- Audit binary: `ash_tcu_replace_04_r1_snapshot_binding_audit`

## 1. Defect

The parent artifact proves deterministic transition mechanics on a ShadowOnly fixture snapshot, but the repository composition-root snapshot is a different Disabled snapshot.

```text
repository root digest = f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
fixture digest         = 654e701cb625cc364b76d3efd498ad203881d29603d27529907e26edf533324e
```

The parent candidate and apply transactions use the fixture digest. Therefore they are valid fixture evidence, not active runtime readiness evidence. The parent `repository_ready_for_replace_05=true` is over-promoted and must be reblocked.

The apply transaction also conflates two states:

```text
backing snapshot mode = shadow_only
logical source mode   = candidate_prepared
effective mode        = shadow_only
```

R1 separates those owners explicitly.

## 2. Authority domains

Introduce:

```rust
pub enum TensorCubeReplacementAuthorityDomain {
    ActiveCompositionRoot,
    AuditFixture,
}
```

Every canonical transaction and receipt must state its authority domain. No domain may be inferred from a digest, transaction ID or mode.

### ActiveCompositionRoot

Only the snapshot owned by `repository_default_replacement_context()` belongs to this domain. Active-domain evidence may contribute to repository readiness.

### AuditFixture

Synthetic snapshots used for graph tests, anchor tests, dry-run construction, transaction chaining, digest determinism and negative fixtures belong to this domain. Fixture evidence may prove mechanics but must never satisfy active readiness.

Required:

```text
fixture_evidence_used_as_active_authority_count = 0
fixture_transaction_count_used_in_promotion_formula = 0
fixture_receipt_count_used_in_promotion_formula = 0
```

## 3. Active snapshot binding

Create one immutable active binding containing:

- composition-root ID,
- runtime-context schema,
- snapshot digest,
- snapshot mode read directly from the snapshot,
- authority domain,
- deterministic semantic digest.

Required current values:

```text
authority_domain = active_composition_root
snapshot_digest = f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
snapshot_mode = disabled
binding_count = 1
snapshot_instance_count = 1
distinct_snapshot_digest_count = 1
```

A fixture snapshot may not substitute for the active root even if a future digest happens to match.

## 4. Fixture snapshot binding

Create an immutable fixture binding containing fixture ID, purpose, digest, mode, authority domain, promotion eligibility and semantic digest.

Required current fixture:

```text
authority_domain = audit_fixture
snapshot_digest = 654e701cb625cc364b76d3efd498ad203881d29603d27529907e26edf533324e
snapshot_mode = shadow_only
eligible_for_repository_promotion = false
```

## 5. Canonical transaction state

Retire `source_snapshot_digest`, `source_mode` and `effective_mode` as internal state owners. They may remain only as compatibility getters.

Canonical fields:

```text
authority_domain
runtime_snapshot_digest
runtime_snapshot_mode
logical_source_mode
proposed_target_mode
effective_runtime_mode
prior_transaction_digest
logical_source_state_digest
```

Compatibility projection:

```text
source_snapshot_digest -> runtime_snapshot_digest
source_mode -> logical_source_mode
effective_mode -> effective_runtime_mode
```

Compatibility values must not participate in readiness.

## 6. Runtime snapshot truth

`runtime_snapshot_digest` identifies the actual backing snapshot. `runtime_snapshot_mode` must equal the mode encoded by that snapshot.

Required:

```text
runtime_snapshot_digest_mismatch_count = 0
runtime_snapshot_mode_mismatch_count = 0
```

## 7. Logical source state

`logical_source_mode` identifies the prepared transaction-chain state from which the current step begins. It may differ from the runtime snapshot mode only when a valid prior prepared transaction proves that state.

The prior transaction must have:

- the same authority domain,
- the same runtime snapshot digest and mode,
- the same candidate identity,
- the same route identity,
- `prepared_dry_run_only` disposition,
- proposed target equal to the current logical source mode.

A free-floating logical CandidatePrepared state is forbidden.

The logical-source-state digest must include domain, runtime digest, runtime mode, logical mode, prior digest, candidate and route identities. Physical paths, timestamps, PIDs, host names and JSON formatting must be excluded.

## 8. Candidate fixture transaction

Required:

```text
authority_domain = audit_fixture
runtime_snapshot_mode = shadow_only
logical_source_mode = shadow_only
proposed_target_mode = candidate_prepared
effective_runtime_mode = shadow_only
prior_transaction_digest = null
```

## 9. Apply fixture transaction

Required:

```text
authority_domain = audit_fixture
runtime_snapshot_mode = shadow_only
logical_source_mode = candidate_prepared
proposed_target_mode = apply_authorized
effective_runtime_mode = shadow_only
prior_transaction_digest = candidate transaction semantic digest
```

The prior candidate transaction is the only owner of the logical CandidatePrepared state. The active runtime snapshot remains unchanged.

## 10. Parent reclassification

The parent candidate and apply transactions are reclassified as AuditFixture evidence because their source digest equals the fixture digest rather than the composition-root digest.

Preserved parent claims:

- graph edge count 11,
- dry-run-preparable edge count 2,
- executable edge count 0,
- deterministic transaction and receipt digests,
- anchor validation,
- valid fixture chain,
- zero runtime mutation.

Retracted parent claim:

```text
repository_ready_for_replace_05 = true
```

## 11. Readiness separation

Introduce:

```text
fixture_transition_mechanics_ready
active_composition_root_transition_binding_ready
repository_ready_for_replace_05
```

Expected current values:

```text
fixture_transition_mechanics_ready = true
active_composition_root_transition_binding_ready = false
repository_ready_for_replace_05 = false
```

A successful R1 patch therefore has `pass=true` while keeping the next stage blocked.

## 12. Corrected readiness formula

`repository_ready_for_replace_05` requires all of:

- valid parent binding,
- unchanged graph and zero executable edges,
- fixture mechanics pass,
- exactly one active composition-root binding,
- an active-domain prepared transaction and valid active-domain chain,
- zero fixture evidence in the promotion formula,
- zero snapshot-mode or prior-provenance mismatches,
- zero effective runtime mode mutation,
- zero runtime-context replacement,
- zero route, registry or epoch mutation,
- zero production replacement execution.

Because the current repository has no active-domain prepared transaction, readiness must be false.

## 13. Exact parent paths

The audit must use exact JSON pointers:

```text
/patch_id
/schema
/semantic_inventory_digest
/execution_artifact_digest
/github_spec_commit
/runtime_snapshot_preservation/repository_composition_root_snapshot_digest_before
/runtime_snapshot_preservation/repository_composition_root_snapshot_digest_after
/runtime_snapshot_preservation/dry_run_fixture_snapshot_digest_before
/runtime_snapshot_preservation/dry_run_fixture_snapshot_digest_after
/prepared_transactions/transactions
/transition_graph_inventory
/verdict/repository_ready_for_replace_05
```

Recursive first-match lookup is forbidden.

## 14. Required metrics

```text
active_composition_root_binding_count = 1
active_composition_root_snapshot_instance_count = 1
active_composition_root_distinct_snapshot_digest_count = 1
fixture_snapshot_binding_count = 1
active_domain_transaction_count = 0
fixture_domain_transaction_count = 2
transaction_count = 2
canonical_transaction_field_complete_count = 2
runtime_snapshot_mode_mismatch_count = 0
logical_source_mode_unproven_count = 0
prior_transaction_required_count = 1
prior_transaction_present_count = 1
prior_transaction_valid_count = 1
prior_transaction_mismatch_count = 0
fixture_transition_mechanics_ready = true
active_composition_root_transition_binding_ready = false
repository_ready_for_replace_05 = false
```

## 15. Safety invariants

```text
transition_graph_semantic_change_count = 0
executable_transition_edge_count = 0
policy_snapshot_mutation_count = 0
runtime_context_replacement_count = 0
active_route_mutation_count = 0
default_route_mutation_count = 0
registry_mutation_count = 0
route_epoch_increment_count = 0
route_select_permit_count = 0
output_ownership_permit_count = 0
default_route_change_permit_count = 0
production_replacement_permit_count = 0
production_replacement_execution_count = 0
gpu_command_submission_count = 0
performance_claim_count = 0
```

Executed decode/training parity is not required. When not run, the artifact must state `not_executed_static_no_change_evidence_only` rather than claiming executed equality.

## 16. Required receipts

```text
ash_tcu_replace_04_r1_parent_binding_receipt.json
ash_tcu_replace_04_r1_active_composition_root_binding_receipt.json
ash_tcu_replace_04_r1_fixture_snapshot_binding_receipt.json
ash_tcu_replace_04_r1_parent_transaction_reclassification_receipt.json
ash_tcu_replace_04_r1_canonical_transaction_state_inventory.json
ash_tcu_replace_04_r1_candidate_provenance_receipt.json
ash_tcu_replace_04_r1_apply_chain_provenance_receipt.json
ash_tcu_replace_04_r1_authority_domain_isolation_audit.json
ash_tcu_replace_04_r1_fixture_promotion_leakage_audit.json
ash_tcu_replace_04_r1_runtime_snapshot_mode_truth_audit.json
ash_tcu_replace_04_r1_logical_source_state_truth_audit.json
ash_tcu_replace_04_r1_readiness_reblock_receipt.json
ash_tcu_replace_04_r1_no_runtime_mutation_guard.json
ash_tcu_replace_04_r1_no_production_replacement_guard.json
ash_tcu_replace_04_r1_output_parity_status.json
ash_tcu_replace_04_r1_static_checks.json
ash_tcu_replace_04_r1_verdict.json
```

## 17. Required tests

At minimum:

- active binding uses repository context,
- active digest and mode are exact,
- fixture domain is explicit and promotion-ineligible,
- candidate canonical fields are truthful,
- apply canonical fields are truthful,
- apply requires a valid prior transaction,
- wrong prior domain, snapshot, candidate, route or target fails closed,
- fixture evidence cannot open REPLACE-05,
- physical parent path does not affect digests,
- graph remains unchanged and executable-edge count remains zero.

## 18. PASS / HOLD

PASS:

```text
PASS_ASH_TCU_REPLACE_04_R1_ACTIVE_COMPOSITION_ROOT_SNAPSHOT_BOUND_DRY_RUN_FIXTURE_AUTHORITY_ISOLATED_RUNTIME_SNAPSHOT_MODE_AND_LOGICAL_SOURCE_STATE_SEPARATED_TRANSACTION_SOURCE_SNAPSHOT_DIGEST_TRUTH_REPAIRED_PRIOR_PREPARED_TRANSACTION_STATE_OWNERSHIP_BOUND_APPLY_PREPARATION_CHAIN_PROVENANCE_PROVEN_REPLACE_05_READINESS_REBLOCKED_NO_ACTIVE_ROUTE_MUTATION_NO_PRODUCTION_REPLACEMENT
```

HOLD:

```text
HOLD_ASH_TCU_REPLACE_04_R1_SNAPSHOT_AUTHORITY_TRANSACTION_PROVENANCE_OR_READINESS_REBLOCK_INCOMPLETE
```

## 19. Next patch

After R1 passes, recommend:

```text
ASH-TCU-REPLACE-04-R2
Active Composition-Root Eligible Edge Audit /
Disabled-to-Shadow Dry-Run Preparation Contract /
Repository Snapshot-Bound Transition Request /
Active-Domain Authorization and Rollback Evidence /
No Runtime Snapshot Mutation /
No Active Route Mutation /
No Production Replacement Seal
```

R1 must not recommend REPLACE-05 directly.
