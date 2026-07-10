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

K7N-B adds a prepare-only transaction planner over the runtime-owned registry from K7N-A. It captures the authoritative before snapshot, validates compare-and-swap preconditions, validates target capability evidence, calculates a detached predicted-after registry state, and emits a prepared transaction receipt.

K7N-B must not acquire live mutation authority, commit a proposal, change any live route binding, increment the live epoch, append the live mutation ledger, push the live rollback stack, emit RuntimeRouteMutation evidence, adopt a default or user-visible route, replace production, change runtime output, execute rollback, mutate weights, or promote performance claims.

## Transaction Boundary

K7N-B implements only:

```txt
proposal
preparation
rejection
```

K7N-B does not implement commit or rollback. A predicted-after snapshot is detached planning state, not live runtime state.

## State Ownership

The live registry remains owned by `TensorCubeRuntimeContext` through `Arc<RwLock<TensorCubeRouteRegistry>>`.

The planner owns immutable proposals, before snapshots, validated preconditions, detached predicted-after state, prepared receipts, and rejection receipts.

The orchestrator owns explicit CLI input and output paths only.

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

## Canonical Audit Proposal

```txt
target_slot = default
route_before = burn_baseline
route_after = ash_tcu_k6p_row_major_emit_candidate_v1
operator_explicit = true
prepare_only = true
```

The live default route must remain `burn_baseline` throughout K7N-B.

Production-slot proposals must be rejected.

## Proposal Preconditions

The planner must validate:

```txt
registry instance ID matches
expected epoch matches live epoch
expected registry digest matches live digest
target slot exists
route-before matches current binding
route-after exists in catalog
route-after differs from route-before
target lifecycle is eligible
operator request is explicit
proposal is prepare-only
production slot is not targeted
proposal digest is valid
candidate capability evidence matches catalog entry
```

A non-Burn target must be `CapabilityProven` or `EligibleForReview`. A Burn baseline target may be `Registered`.

## Compare-And-Swap Boundary

Future commit authority is modeled by the conjunction of:

```txt
registry instance ID
expected epoch
expected registry digest
route-before binding
```

Matching only epoch or only digest is insufficient.

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

The planner must use read-only access to the live registry.

## Detached Predicted After State

The planner must clone the live registry into detached state, change only the proposed slot, increment the detached epoch exactly once, push the before snapshot to the detached rollback stack, append one detached predicted mutation record, recalculate digests, and leave the live registry untouched.

For the canonical proposal:

```txt
predicted candidate = ash_tcu_k6p_row_major_emit_candidate_v1
predicted default = ash_tcu_k6p_row_major_emit_candidate_v1
predicted user-visible = burn_baseline
predicted production = burn_baseline
predicted epoch = 1
```

Live bindings and live epoch remain unchanged.

## Required Rejection Tests

K7N-B must reject while preserving live state:

```txt
stale epoch
stale registry digest
registry instance mismatch
route-before mismatch
unknown route
same-route no-op
production proposal
candidate capability mismatch
operator request not explicit
prepare-only false
```

## Live Registry Immutability

Before and after preparation and all rejection tests, K7N-B must prove:

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

If the live digest moves during preparation, preparation fails.

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
crates/burn_webgpu_backend/src/tensorcube_k7n_b_*.rs
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

All IDs, epochs, routes, capability references, and digests must come from the actual registry and preparation event.

## Recommended Next Patch

```txt
ASH-TCU-K7N-C
Prepared Transaction Commit And Receipt-to-Registry Rebind / Runtime-Owned Compare-And-Swap Mutation / Epoch Increment And Registry Digest Transition / Default Slot Only / Rollback Snapshot Push / No User-Visible Or Production Adoption Seal
```

## Final Seal

K7N-B binds an explicit prepare-only proposal to the runtime-owned registry instance, epoch, digest, current binding, and target capability evidence. It calculates a detached predicted-after state, rejects stale and invalid proposals, and leaves all live registry state unchanged.