# ASH-TCU-REPLACE-04

## Canonical Replacement Transition Transaction / Mode Transition Graph / Authorization and Rollback Anchor Binding / Candidate-to-Apply Prepared Transaction / Dry-Run Transition Receipt / Proposed-vs-Effective Mode Separation / No Active Route Mutation / No Production Replacement Seal

## 0. Metadata

- Parent: `ASH-TCU-REPLACE-03`
- Parent schema: `ash.tcu.replace.03.consumer_rebind_audit.runtime_artifact.v1`
- Parent semantic digest: `bb29fc458f19e75867d0476e0cd7c4da8eddc5805462bac8fee7a8bee45877d7`
- Parent execution digest: `82f7e0757e9b927fcf416a713e3df57ef3c61ce967baea682908763011450adb`
- Parent spec commit: `7966166d32738b193786849d80efa8e1f9f36726`
- Parent composition-root snapshot digest: `f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692`
- Parent readiness: `repository_ready_for_replace_04=true`
- Transition schema: `ash.tcu.replace.04.transition_transaction.v1`
- Graph schema: `ash.tcu.replace.04.mode_transition_graph.v1`
- Authorization schema: `ash.tcu.replace.04.authorization_anchor.v1`
- Rollback schema: `ash.tcu.replace.04.rollback_anchor.v1`
- Dry-run receipt schema: `ash.tcu.replace.04.dry_run_transition_receipt.v1`
- Runtime artifact schema: `ash.tcu.replace.04.transition_transaction_audit.runtime_artifact.v1`

Primary implementation:

```text
crates/burn_webgpu_backend/src/tensorcube_replacement_transition.rs
```

Audit binary:

```text
crates/orchestrator_local/src/bin/ash_tcu_replace_04_transition_transaction_audit.rs
```

## 1. Purpose

REPLACE-04 establishes a canonical representation for a future replacement-mode transition. It may describe, validate, hash, reject, and receipt a proposed transition. It may not apply, commit, activate, execute, or install that transition.

The canonical flow is:

```text
immutable active snapshot
→ explicit transition request
→ explicit graph edge
→ authorization anchor validation
→ rollback anchor validation
→ immutable prepared dry-run transaction
→ deterministic dry-run receipt
```

Blocking invariant:

```text
proposed_target_mode != effective_runtime_mode
```

For every prepared transaction:

```text
effective_runtime_mode_after = effective_runtime_mode_before
```

## 2. Parent Binding

The parent is read only through exact JSON pointers:

```text
/patch_id
/schema
/semantic_inventory_digest
/execution_artifact_digest
/github_spec_commit
/verdict/repository_ready_for_replace_04
/runtime_snapshot_composition_root/snapshot_semantic_digest
/runtime_snapshot_composition_root/runtime_policy_composition_root_count
/runtime_snapshot_composition_root/runtime_policy_snapshot_instance_count
/guard_evaluation_inventory/route_select_permit_count
/guard_evaluation_inventory/output_ownership_permit_count
/guard_evaluation_inventory/default_route_change_permit_count
/guard_evaluation_inventory/production_replacement_permit_count
```

Required parent state:

```text
patch_id = ASH-TCU-REPLACE-03
schema = ash.tcu.replace.03.consumer_rebind_audit.runtime_artifact.v1
semantic digest = bb29fc458f19e75867d0476e0cd7c4da8eddc5805462bac8fee7a8bee45877d7
execution digest = 82f7e0757e9b927fcf416a713e3df57ef3c61ce967baea682908763011450adb
spec commit = 7966166d32738b193786849d80efa8e1f9f36726
composition-root snapshot digest = f6cc60a0d7c726183ac8e257443d25db3e42480271dc88fb0a237706b2d3f692
composition root count = 1
snapshot instance count = 1
all dangerous permit counts = 0
repository_ready_for_replace_04 = true
```

Recursive key-name search, alias fallback, and expected-value search are forbidden.

## 3. Transition Graph SSOT

One explicit registry owns all legal edges.

Required forward edges:

```text
Disabled → ShadowOnly
ShadowOnly → CandidatePrepared
CandidatePrepared → ApplyAuthorized
ApplyAuthorized → InternalCanary
InternalCanary → UserVisibleCanary
UserVisibleCanary → ProductionReplacement
```

Required rollback edges:

```text
CandidatePrepared → ShadowOnly
ApplyAuthorized → CandidatePrepared
InternalCanary → ApplyAuthorized
UserVisibleCanary → InternalCanary
ProductionReplacement → UserVisibleCanary
```

No transition may be inferred from enum ordinals.

REPLACE-04 dry-run allowlist:

```text
ShadowOnly → CandidatePrepared
CandidatePrepared → ApplyAuthorized
```

Every edge must report `executable_by_replace_04=false`.

Required graph metrics:

```text
transition_graph_owner_count = 1
mode_count = 7
intent_count = 6
edge_count = 11
required_forward_edge_count = 6
required_rollback_edge_count = 5
missing_required_edge_count = 0
duplicate_edge_count = 0
conflicting_edge_count = 0
dry_run_preparable_edge_count = 2
executable_transition_edge_count = 0
```

## 4. Transition Vocabulary

Intents:

```text
PrepareCandidate
PrepareApplyAuthorization
PrepareInternalCanary
PrepareUserVisibleCanary
PrepareProductionReplacement
PrepareRollback
```

Phases:

```text
Drafted
GraphValidated
AnchorsValidated
DryRunEvaluated
Prepared
Rejected
```

`Applied`, `Committed`, `Activated`, `Promoted`, and `ProductionActive` do not exist in REPLACE-04.

## 5. Authorization Anchor

The authorization anchor binds:

```text
authorization ID
authorization kind
source snapshot digest
logical source mode
proposed target mode
candidate identity
route identity
authorization scope
evidence digest
semantic digest
```

Runtime-constructible authorization kinds:

```text
CandidatePreparation
ApplyPreparation
```

A deserialized anchor is evidence only. It must be revalidated for schema, digest, source snapshot, modes, identities, and edge ownership before use.

## 6. Rollback Anchor

The rollback anchor binds:

```text
source snapshot digest
logical source mode
rollback target mode
candidate identity
route identity
route registry digest
default route identity
active route identity
route epoch
rollback evidence digest
semantic digest
```

When route registry, active route, default route, or epoch are not materially measured, the anchor records:

```text
evidence_status = not_materialized
```

Missing evidence must never be replaced with invented values.

## 7. Canonical Transaction

The immutable transaction contains:

```text
transaction ID
transaction version
root source snapshot digest
logical source mode
proposed target mode
effective active mode
intent
phase
disposition
candidate identity
route identity
authorization anchor digest
rollback anchor digest
transition edge digest
optional prior transaction digest
construction input digest
semantic digest
```

No apply, commit, activate, execute, snapshot replacement, or effective-mode setter API may exist.

## 8. Staged Source Chain

The apply-preparation transaction must not construct or install an active CandidatePrepared snapshot.

Candidate preparation:

```text
active fixture snapshot mode = ShadowOnly
logical source mode = ShadowOnly
proposed target mode = CandidatePrepared
effective mode = ShadowOnly
```

Apply preparation:

```text
active fixture snapshot mode = ShadowOnly
prior transaction proposed mode = CandidatePrepared
logical source mode = CandidatePrepared
proposed target mode = ApplyAuthorized
effective mode = ShadowOnly
```

The apply transaction binds the candidate transaction semantic digest as `prior_transaction_digest`.

This proves transaction composition without mutating the active snapshot.

## 9. Candidate and Apply Transactions

Candidate transaction requirements:

```text
edge = ShadowOnly → CandidatePrepared
intent = PrepareCandidate
authorization kind = CandidatePreparation
rollback target = ShadowOnly
disposition = PreparedDryRunOnly
```

Apply transaction requirements:

```text
edge = CandidatePrepared → ApplyAuthorized
intent = PrepareApplyAuthorization
authorization kind = ApplyPreparation
rollback target = CandidatePrepared
prior transaction digest = candidate transaction digest
disposition = PreparedDryRunOnly
```

Neither transaction authorizes route selection, output ownership, default-route mutation, or production execution.

## 10. Dry-Run Receipt

Each receipt records:

```text
transaction digest
source snapshot digest
logical source mode
proposed target mode
effective mode before and after
graph validity
authorization validity
rollback validity
identity parity
runtime snapshot preservation
active-route evidence status
default-route evidence status
registry evidence status
route-epoch evidence status
disposition
failure reasons
semantic digest
```

A receipt passes only when graph, anchors, identities, root snapshot, and effective-mode preservation all pass.

Receipts are evidence only and cannot be reused as execution authority.

## 11. Digest Determinism

The construction input digest includes schema, version, root snapshot digest, logical source mode, proposed target mode, effective mode, intent, identities, anchor digests, edge digest, and prior transaction digest.

Excluded inputs:

```text
absolute path
physical parent filename
timestamp
PID
thread ID
memory address
JSON whitespace
output directory
Cargo profile
host name
```

Required:

```text
same semantic inputs → same transaction digest
same semantic inputs → same receipt digest
different physical parent paths → same final semantic digest
```

## 12. Negative Fixtures

At least these failures are required:

```text
ShadowOnly → ApplyAuthorized skip edge
candidate identity mismatch
rollback route identity mismatch
```

Required counts:

```text
transaction construction attempts >= 5
transaction construction successes = 2
transaction construction rejections >= 3
authorization mismatch count >= 1
rollback mismatch count >= 1
accepted anchor without revalidation count = 0
```

## 13. Runtime Boundary

Allowed:

```text
transition module exports
audit-only construction
unit tests
receipt serialization
static inventories
```

Forbidden:

```text
Q-wave consumer transaction inputs
runtime transaction execution
runtime snapshot replacement
active route mutation
default route mutation
route registry mutation
route epoch increment
production replacement
GPU submission
```

Required:

```text
runtime_consumer_transition_transaction_input_count = 0
```

## 14. Safety Metrics

All must equal zero:

```text
policy_snapshot_mutation_count
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
promotion_token_consumption_count
gpu_adapter_request_count
gpu_device_request_count
gpu_command_submission_count
shader_change_count
performance_claim_count
```

## 15. Output-Parity Honesty

REPLACE-04 does not require decode or training execution. When not executed:

```text
executed_output_parity = false
executed_output_parity_status = not_executed_static_no_change_evidence_only
```

Static no-mutation evidence must not be represented as executed output equality.

## 16. Required Tests

```text
graph contains 11 explicit edges
dry-run allowlist contains exactly 2 edges
all edges are non-executable
forbidden skip edge is rejected
candidate dry-run keeps effective mode ShadowOnly
apply dry-run chains from candidate transaction
apply dry-run keeps effective mode ShadowOnly
candidate mismatch fails closed
same inputs produce same transaction digest
same inputs produce same receipt digest
parent constants remain exact
fixture snapshot remains unchanged
```

## 17. Readiness for REPLACE-05

`repository_ready_for_replace_05=true` only when parent binding, graph integrity, both positive transactions, all negative fixtures, anchor validation, digest determinism, snapshot preservation, zero mutation counts, zero dangerous permits, zero production execution, zero GPU submission, and zero performance claims all pass.

Recommended next patch:

```text
ASH-TCU-REPLACE-05

Prepared Transition Store /
Single-Use Transaction Consumption Contract /
Authorization Freshness and Replay Gate /
Rollback Precondition Revalidation /
Apply Sandbox Without Route Ownership /
No Default Route Mutation /
No Production Replacement Seal
```

## 18. PASS Marker

```text
PASS_ASH_TCU_REPLACE_04_
CANONICAL_REPLACEMENT_TRANSITION_TRANSACTION_ESTABLISHED_
MODE_TRANSITION_GRAPH_SEALED_
AUTHORIZATION_AND_ROLLBACK_ANCHORS_BOUND_
CANDIDATE_TO_APPLY_PREPARED_TRANSACTION_PROVEN_
DRY_RUN_TRANSITION_RECEIPTS_DETERMINISTIC_
PROPOSED_AND_EFFECTIVE_MODES_SEPARATED_
NO_ACTIVE_ROUTE_MUTATION_
NO_PRODUCTION_REPLACEMENT
```

## 19. HOLD Marker

```text
HOLD_ASH_TCU_REPLACE_04_
TRANSITION_GRAPH_TRANSACTION_ANCHOR_OR_DRY_RUN_SAFETY_INCOMPLETE
```

## 20. Final Seal

REPLACE-04 passes only when one explicit graph owns every legal edge; no ordinal logic infers transitions; only two edges are dry-run preparable; no edge is executable; authorization and rollback anchors are immutable, digest-bound, identity-bound, and revalidated; candidate and apply transactions are chained deterministically; the proposed target changes while the effective mode does not; the composition-root snapshot is not replaced; no apply or commit API exists; no Q-wave consumer accepts a transaction; no route, registry, epoch, output ownership, production path, GPU behavior, or benchmark claim changes.