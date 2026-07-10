# ASH-TCU-K7N-B SPEC

## Title

Route Epoch And Hash Prepared Transaction Receipt / Runtime-Owned Mutation Proposal Validation / Compare-And-Swap Preconditions / Predicted After Snapshot / No Live Commit No Route Adoption Seal

## Patch ID

```txt
ASH-TCU-K7N-B
```

## Status Target

```txt
PASS_ASH_TCU_K7N_B_ROUTE_EPOCH_HASH_PREPARED_TRANSACTION_NO_LIVE_COMMIT_NO_ROUTE_ADOPTION_SEAL
```

## Parent

```txt
ASH-TCU-K7N-A
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_A_CENTRAL_ROUTE_REGISTRY_SSOT_EXPLICIT_BOOTSTRAP_NO_ROUTE_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

Required prior verdict:

```txt
central_runtime_owned_route_registry_created_at_genesis_epoch_zero_no_route_adoption
```

## Purpose

K7N-B adds a prepare-only route transaction planner over the runtime-owned registry created in K7N-A. It captures the live before snapshot, validates compare-and-swap preconditions, validates target capability evidence, calculates a detached predicted-after registry state, and emits a prepared transaction receipt.

K7N-B must not acquire live mutation authority, commit the proposal, change any live route binding, increment the live epoch, append the live mutation ledger, push the live rollback stack, emit `RuntimeRouteMutation` evidence, adopt a default or user-visible route, replace production, change runtime output, execute rollback, mutate weights, or promote performance claims.

## Transaction Boundary

K7N-B implements only:

```txt
proposal
preparation
rejection
```

K7N-B does not implement:

```txt
commit
rollback
```

A prepared transaction is not a route mutation. A predicted-after snapshot is detached planning state, not live runtime state.

## State Ownership

The runtime registry remains the owner of live catalog, bindings, epoch, digest, rollback stack, and mutation ledger.

The transaction planner owns immutable proposals, before snapshots, validated preconditions, detached predicted-after state, prepared receipts, and rejection receipts.

The orchestrator owns explicit CLI input and receipt output only. It must not duplicate or own the live registry.

## SSOT

```txt
crates/burn_webgpu_backend/src/tensorcube_route_mutation_proposal.rs
crates/burn_webgpu_backend/src/tensorcube_route_transaction_planner.rs
crates/burn_webgpu_backend/src/tensorcube_prepared_route_transaction.rs
workspace/runtime/tensorcube/ash_tensorcube_k7n_b_prepared_route_transaction_latest.json
```

Transaction schema:

```txt
ash_tensorcube_route_transaction_v1
```

## Transaction Stage

```rust
pub enum TensorCubeRouteTransactionStage {
    Proposed,
    Prepared,
    Rejected,
    Committed,
    RolledBack,
}
```

K7N-B may produce only `Proposed`, `Prepared`, and `Rejected`.

## Mutation Proposal

```rust
pub struct TensorCubeRouteMutationProposal {
    pub transaction_schema_version: String,
    pub proposal_id: String,
    pub proposal_digest: String,
    pub registry_instance_id: String,
    pub expected_epoch: u64,
    pub expected_registry_digest: String,
    pub target_slot: TensorCubeRouteSlot,
    pub route_before: TensorCubeRouteId,
    pub route_after: TensorCubeRouteId,
    pub requested_by_patch: String,
    pub request_reason: String,
    pub operator_explicit: bool,
    pub prepare_only: bool,
    pub capability_execution_id: Option<String>,
    pub capability_dispatch_digest: Option<String>,
    pub capability_readback_digest: Option<String>,
}
```

The proposal ID must be unique per request. The proposal digest must be deterministic for normalized proposal content and must not depend on timestamps or random nonces.

Required:

```txt
operator_explicit = true
prepare_only = true
```

Implicit proposals from legacy receipts, annotations, environment variables, fallback constants, catalog ordering, or candidate binding alone are forbidden.

## Canonical Audit Proposal

```txt
target_slot = default
route_before = burn_baseline
route_after = ash_tcu_k6p_row_major_emit_candidate_v1
```

The live default route must remain `burn_baseline` through K7N-B.

Production-slot proposals must be rejected with `ProductionProposalForbidden`.

## Preconditions

The planner must validate:

```txt
registry instance ID matches
expected epoch matches live epoch
expected registry digest matches live digest
target slot exists
route-before matches current binding
route-after exists in the catalog
route-after differs from route-before
target lifecycle is eligible
operator request is explicit
proposal is prepare-only
production slot is not targeted
proposal digest is valid
candidate capability evidence matches the target catalog entry
```

A non-Burn target must be `CapabilityProven` or `EligibleForReview`. A Burn baseline target may be `Registered`.

## Planner API

```rust
pub struct TensorCubeRouteTransactionPlanner;

impl TensorCubeRouteTransactionPlanner {
    pub fn prepare(
        runtime: &TensorCubeRuntimeContext,
        proposal: &TensorCubeRouteMutationProposal,
    ) -> Result<TensorCubePreparedRouteTransaction, TensorCubeRouteTransactionError>;
}
```

The planner must use a read lock for live-state capture and must not acquire a live write lock.

## Prepared Transaction

```rust
pub struct TensorCubePreparedRouteTransaction {
    pub transaction_schema_version: String,
    pub transaction_id: String,
    pub transaction_digest: String,
    pub stage: TensorCubeRouteTransactionStage,
    pub proposal: TensorCubeRouteMutationProposal,
    pub registry_instance_id: String,
    pub before_snapshot: TensorCubeRouteSnapshot,
    pub predicted_after_snapshot: TensorCubeRouteSnapshot,
    pub epoch_before: u64,
    pub predicted_epoch_after: u64,
    pub registry_digest_before: String,
    pub predicted_registry_digest_after: String,
    pub route_before: TensorCubeRouteId,
    pub route_after: TensorCubeRouteId,
    pub preconditions_valid: bool,
    pub live_commit_executed: bool,
    pub live_registry_digest_after_preparation: String,
    pub live_epoch_after_preparation: u64,
}
```

Required:

```txt
stage = prepared
preconditions_valid = true
live_commit_executed = false
predicted_epoch_after = epoch_before + 1
```

## Predicted After State

The planner must operate on detached cloned state. It must change only the proposed slot, increment the detached epoch exactly once, push the before snapshot onto the detached rollback stack, append exactly one detached predicted mutation record, recalculate digests, and leave the live registry untouched.

For the canonical default proposal:

```txt
predicted candidate = ash_tcu_k6p_row_major_emit_candidate_v1
predicted default = ash_tcu_k6p_row_major_emit_candidate_v1
predicted user-visible = burn_baseline
predicted production = burn_baseline
```

Live bindings remain unchanged.

## CAS Boundary

Future commit authority is modeled by the conjunction of:

```txt
registry instance ID
expected epoch
expected registry digest
route-before binding
```

Matching only epoch or only digest is insufficient.

## Required Rejection Tests

K7N-B must reject and preserve live state for:

```txt
stale epoch
stale registry digest
registry instance mismatch
route-before mismatch
unknown route
same-route no-op
production proposal
candidate capability evidence mismatch
operator request not explicit
prepare-only false
```

## Error Type

```rust
pub enum TensorCubeRouteTransactionError {
    TransactionSchemaMismatch,
    MissingProposalId,
    MissingProposalDigest,
    OperatorRequestNotExplicit,
    PrepareOnlyRequired,
    RegistryLockPoisoned,
    RegistryInstanceMismatch,
    StaleEpoch,
    StaleRegistryDigest,
    MissingTargetSlot,
    RouteBeforeMismatch,
    TargetRouteNotInCatalog,
    TargetRouteLifecycleInvalid,
    CandidateCapabilityEvidenceMissing,
    CandidateCapabilityEvidenceMismatch,
    NoOpProposal,
    ProductionProposalForbidden,
    BeforeSnapshotIntegrityFailure,
    PredictedAfterSnapshotIntegrityFailure,
    PredictedEpochInvalid,
    PredictedDigestInvalid,
    LiveRegistryChangedDuringPreparation,
}
```

## Live Registry Immutability

Before and after all preparation and rejection tests, K7N-B must prove:

```txt
registry instance ID unchanged
live epoch unchanged
live registry digest unchanged
live catalog unchanged
live bindings unchanged
live mutation ledger unchanged
live rollback stack unchanged
mutation_enabled remains false
```

If the live digest moves during preparation, the planner must fail with `LiveRegistryChangedDuringPreparation`.

## Evidence Classification

```txt
route mutation proposed -> DeclaredIntent / IntentOnly
preconditions validated -> DerivedReceipt / DerivedOnly
predicted route state calculated -> DerivedReceipt / DerivedOnly
runtime route mutation committed -> false
```

K7N-B must not emit `RuntimeRouteMutation / RuntimeMutated` evidence.

## Guards

K7N-B must prove:

```txt
live commit requested = false
live commit executed = false
live write lock acquired = false
live binding changed = false
live epoch incremented = false
live registry digest changed = false
live mutation ledger appended = false
live rollback stack pushed = false
route adoption = false
production replacement = false
runtime output claim = false
rollback execution = false
weight mutation = false
performance claim = false
```

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_route_transaction_stage.rs
crates/burn_webgpu_backend/src/tensorcube_route_mutation_proposal.rs
crates/burn_webgpu_backend/src/tensorcube_predicted_route_mutation.rs
crates/burn_webgpu_backend/src/tensorcube_prepared_route_transaction.rs
crates/burn_webgpu_backend/src/tensorcube_route_transaction_error.rs
crates/burn_webgpu_backend/src/tensorcube_route_transaction_planner.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_prior_k7n_a_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_mutation_proposal.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_before_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_precondition_validation.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_predicted_after_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_transaction_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_stale_epoch_rejection.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_stale_digest_rejection.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_route_before_mismatch_rejection.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_unknown_route_rejection.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_noop_rejection.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_live_registry_immutability.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_no_live_commit_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_no_route_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_no_runtime_output_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_b_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7n_b_route_epoch_hash_transaction_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_b_route_epoch_hash_transaction_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_b_route_epoch_hash_transaction_audit -- --repo-root <repo> --require-k7n-a-pass --proposal-slot default --proposal-route-before burn_baseline --proposal-route-after ash_tcu_k6p_row_major_emit_candidate_v1 --proposal-reason k7n_b_prepare_only_default_candidate_transaction --operator-explicit --prepare-only --validate-registry-instance --validate-expected-epoch --validate-expected-registry-digest --validate-route-before --validate-target-capability --create-before-snapshot --create-predicted-after-snapshot --validate-stale-epoch-rejection --validate-stale-digest-rejection --validate-route-before-mismatch-rejection --validate-unknown-route-rejection --validate-noop-rejection --validate-production-proposal-rejection --verify-live-registry-unchanged --no-live-commit --no-route-adoption --no-production-replacement --no-runtime-output-claim --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_B_PRIOR_K7N_A_RECEIPT
PASS_ASH_TCU_K7N_B_MUTATION_PROPOSAL
PASS_ASH_TCU_K7N_B_REGISTRY_INSTANCE_PRECONDITION
PASS_ASH_TCU_K7N_B_EPOCH_PRECONDITION
PASS_ASH_TCU_K7N_B_REGISTRY_DIGEST_PRECONDITION
PASS_ASH_TCU_K7N_B_ROUTE_BEFORE_PRECONDITION
PASS_ASH_TCU_K7N_B_TARGET_CAPABILITY_PRECONDITION
PASS_ASH_TCU_K7N_B_BEFORE_SNAPSHOT
PASS_ASH_TCU_K7N_B_PREDICTED_AFTER_SNAPSHOT
PASS_ASH_TCU_K7N_B_TRANSACTION_DIGEST
PASS_ASH_TCU_K7N_B_STALE_EPOCH_REJECTED
PASS_ASH_TCU_K7N_B_STALE_DIGEST_REJECTED
PASS_ASH_TCU_K7N_B_ROUTE_BEFORE_MISMATCH_REJECTED
PASS_ASH_TCU_K7N_B_UNKNOWN_ROUTE_REJECTED
PASS_ASH_TCU_K7N_B_NOOP_REJECTED
PASS_ASH_TCU_K7N_B_PRODUCTION_PROPOSAL_REJECTED
PASS_ASH_TCU_K7N_B_LIVE_REGISTRY_IMMUTABILITY
PASS_ASH_TCU_K7N_B_NO_LIVE_COMMIT
PASS_ASH_TCU_K7N_B_NO_ROUTE_ADOPTION
PASS_ASH_TCU_K7N_B_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7N_B_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_B_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_B_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_B_ROUTE_EPOCH_HASH_PREPARED_TRANSACTION_NO_LIVE_COMMIT_NO_ROUTE_ADOPTION_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

All identifiers, routes, epochs, digests, and capability references must come from the actual K7N-A registry and actual preparation event.

## Recommended Next Patch

```txt
ASH-TCU-K7N-C
Prepared Transaction Commit And Receipt-to-Registry Rebind / Runtime-Owned Compare-And-Swap Mutation / Epoch Increment And Registry Digest Transition / Default Slot Only / Rollback Snapshot Push / No User-Visible Or Production Adoption Seal
```

## Final Seal

K7N-B prepares a route transaction against the runtime-owned registry using registry instance, epoch, digest, route-before, target capability, and explicit operator intent. It calculates a detached predicted-after state and rejects stale or invalid proposals. It does not commit, mutate live state, adopt a route, replace production, change runtime output, execute rollback, mutate weights, or promote performance claims.
