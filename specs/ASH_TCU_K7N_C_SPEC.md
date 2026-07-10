# ASH-TCU-K7N-C SPEC

## Title

Prepared Transaction Commit And Receipt-to-Registry Rebind / Runtime-Owned Compare-And-Swap Mutation / Default Slot Adoption / Epoch Increment And Registry Digest Transition / Rollback Snapshot Push / No User-Visible Or Production Adoption Seal

## Patch ID

```txt
ASH-TCU-K7N-C
```

## Status Target

```txt
PASS_ASH_TCU_K7N_C_PREPARED_TRANSACTION_COMMIT_RUNTIME_CAS_DEFAULT_ROUTE_ADOPTION_NO_USER_VISIBLE_NO_PRODUCTION_SEAL
```

## Parent

```txt
ASH-TCU-K7N-B
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_B_ROUTE_EPOCH_HASH_PREPARED_TRANSACTION_NO_LIVE_COMMIT_NO_ROUTE_ADOPTION_SEAL
```

Required prior verdict:

```txt
route_transaction_prepared_with_epoch_hash_cas_preconditions_no_live_commit
```

## Purpose

K7N-C commits one K7N-B prepared transaction into the runtime-owned TensorCube route registry. It validates the prepared receipt and explicit one-shot authority, reacquires the live registry under a write lock, revalidates registry instance, epoch, digest, route-before, target capability, and replay state, constructs the complete after-state on a detached staged registry, verifies predicted-to-actual parity, and replaces the live registry through one final assignment.

K7N-C mutates only the Default binding. Candidate, UserVisible, and Production bindings remain unchanged. It does not bind the registry to runtime decode output, change assistant output, execute rollback, mutate model weights, or promote performance or production-readiness claims.

## State Ownership

The live registry remains owned by:

```txt
TensorCubeRuntimeContext
└── Arc<RwLock<TensorCubeRouteRegistry>>
```

The prepared transaction owns the expected registry instance, epoch, digest, route-before, route-after, predicted epoch, predicted bindings, and predicted digest.

The commit authority owns permission to commit one exact transaction to the Default slot. The orchestrator supplies explicit approval but must not directly edit registry fields.

## SSOT

```txt
crates/burn_webgpu_backend/src/tensorcube_route_commit_authority.rs
crates/burn_webgpu_backend/src/tensorcube_route_transaction_committer.rs
crates/burn_webgpu_backend/src/tensorcube_committed_route_transaction.rs
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_route_transaction_commit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_committed_route_registry_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_runtime_route_mutation_evidence_latest.json
```

Commit schema:

```txt
ash_tensorcube_route_commit_v1
```

## Explicit Commit Authority

The audit requires:

```txt
--operator-explicit-commit
--commit-prepared-transaction
```

The authority must bind:

```txt
registry instance ID
transaction ID
proposal ID
allowed slot = Default
operator explicit commit = true
one shot = true
consumed before commit = false
```

A prepared receipt alone is not commit authority.

## Prepared Transaction Validation

Before the write lock, K7N-C validates:

```txt
transaction schema version
stage = Prepared
proposal prepare-only = true
proposal operator-explicit = true
live commit executed = false
proposal ID and digest
transaction ID and digest
registry instance consistency
epoch-before consistency
registry-digest-before consistency
route-before and route-after consistency
predicted epoch = epoch-before + 1
predicted registry digest present and different from before
target slot = Default
candidate capability evidence present
```

Any failure prevents mutation.

## Commit-Time CAS Boundary

Under the live registry write lock, K7N-C must revalidate:

```txt
live registry instance ID = prepared registry instance ID
live epoch = prepared epoch-before
live registry digest = prepared registry-digest-before
live Default route = prepared route-before
target route exists in live catalog
target capability references match the prepared proposal
transaction ID is absent from the live mutation ledger
authority registry, transaction, proposal, and slot match
authority is explicit, one-shot, and unconsumed
```

Pre-lock validation is not sufficient.

## Atomic Staged Mutation

Required sequence:

```txt
1. acquire live write lock
2. validate all CAS conditions
3. clone live registry into staged registry
4. apply the prepared mutation only to staged state
5. recalculate staged digests
6. verify staged state equals K7N-B predicted state
7. materialize commit and evidence payloads in memory
8. replace live registry with one assignment
9. mark authority consumed
10. release write lock
```

The final mutation boundary is:

```rust
*live_registry_guard = staged_registry;
```

Any failure before this assignment leaves the live registry unchanged and authority unconsumed.

## Predicted-State Compatibility Rule

K7N-B calculated its predicted registry digest over the complete predicted registry payload, including binding metadata, rollback snapshot, and mutation-ledger fields. K7N-C must reproduce that exact payload to satisfy predicted-to-actual digest parity.

Therefore the registry-internal binding and ledger payload committed by K7N-C must remain byte-equivalent to the K7N-B predicted state. K7N-C must not rewrite those fields merely to rename the committing patch.

K7N-C-specific truth is recorded separately in:

```txt
commit authority
commit ID and commit digest
atomic swap receipt
RuntimeRouteMutation evidence
K7N-C commit receipt
```

This preserves both authorities:

```txt
K7N-B owns the predicted registry payload
K7N-C owns the actual commit event and runtime mutation evidence
```

## Required Transition

For the canonical transaction:

```txt
epoch before = 0
epoch after = 1
Default before = burn_baseline
Default after = ash_tcu_k6p_row_major_emit_candidate_v1
Candidate unchanged
UserVisible unchanged at burn_baseline
Production unchanged at burn_baseline
rollback stack count 0 -> 1
mutation ledger count 0 -> 1
```

The catalog and candidate lifecycle remain unchanged.

## Predicted-to-Actual Parity

K7N-C must prove:

```txt
actual registry instance = prepared registry instance
actual epoch after = predicted epoch after
actual Candidate binding = predicted Candidate binding
actual Default binding = predicted Default binding
actual UserVisible binding = predicted UserVisible binding
actual Production binding = predicted Production binding
actual catalog digest = predicted catalog digest
actual bindings digest = predicted bindings digest
actual registry digest = predicted registry digest
```

A digest mismatch fails closed before atomic replacement.

## Runtime Mutation Evidence

K7N-C emits a K7M-A evidence record for:

```txt
claim_name = default_route_mutated
evidence_class = RuntimeRouteMutation
authority = RuntimeMutated
claim_value = true
source registry epoch = 1
source registry hash = committed registry digest
```

The evidence must pass `validate_protected_claim(DefaultRouteMutated, ...)`.

K7N-C must not satisfy UserVisibleRouteMutated, ProductionRouteMutated, RuntimeDecodeOutputChanged, AssistantMessageOutputChanged, or ActualRollbackExecuted.

## Replay Rejection

After commit, attempting the same transaction again must be rejected explicitly. The committed registry must remain at epoch one with one ledger entry and one rollback snapshot.

An already-present transaction identity in the mutation ledger must be classified as `TransactionAlreadyCommitted`; it must not be silently reduced to a generic stale-epoch result.

## Tamper Rejection

Before the authoritative commit, isolated contexts must reject tampered proposal digest, transaction digest, predicted digest, registry instance, epoch-before, route-before, capability references, authority transaction ID, authority slot, consumed authority, and missing explicit commit approval.

Counterexamples must not modify the authoritative live registry.

## Guards

K7N-C must prove:

```txt
Default binding mutated = true
Candidate binding mutated = false
UserVisible binding mutated = false
Production binding mutated = false
runtime route mutation evidence created = true
runtime decode output changed = false
assistant message output changed = false
rollback snapshot pushed = true
rollback execution = false
model/optimizer/checkpoint mutation = false
performance claim = false
production-readiness claim = false
```

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_route_commit_authority.rs
crates/burn_webgpu_backend/src/tensorcube_committed_route_mutation_record.rs
crates/burn_webgpu_backend/src/tensorcube_runtime_route_mutation_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_committed_route_transaction.rs
crates/burn_webgpu_backend/src/tensorcube_route_commit_error.rs
crates/burn_webgpu_backend/src/tensorcube_route_transaction_committer.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_c_*.rs
crates/orchestrator_local/src/ash_tcu_k7n_c_prepared_transaction_commit_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_c_prepared_transaction_commit_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_c_prepared_transaction_commit_audit -- --repo-root <repo> --require-k7n-b-pass --load-prepared-transaction --operator-explicit-commit --commit-prepared-transaction --require-default-slot-only --validate-authority --validate-prepared-transaction --validate-write-lock-cas --create-staged-registry --push-rollback-snapshot --append-mutation-ledger --verify-predicted-actual-parity --atomic-swap-live-registry --emit-runtime-route-mutation-evidence --validate-replay-rejection --validate-tampered-transaction-rejection --no-user-visible-adoption --no-production-adoption --no-candidate-slot-mutation --no-runtime-output-claim --no-rollback-execution --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_C_PRIOR_K7N_B_RECEIPT
PASS_ASH_TCU_K7N_C_COMMIT_AUTHORITY
PASS_ASH_TCU_K7N_C_PREPARED_TRANSACTION_VALIDATION
PASS_ASH_TCU_K7N_C_WRITE_LOCK_CAS_VALIDATION
PASS_ASH_TCU_K7N_C_STAGED_REGISTRY
PASS_ASH_TCU_K7N_C_BEFORE_SNAPSHOT
PASS_ASH_TCU_K7N_C_ROLLBACK_SNAPSHOT_PUSH
PASS_ASH_TCU_K7N_C_MUTATION_LEDGER_APPEND
PASS_ASH_TCU_K7N_C_EPOCH_INCREMENT
PASS_ASH_TCU_K7N_C_DEFAULT_BINDING_MUTATION
PASS_ASH_TCU_K7N_C_PREDICTED_ACTUAL_PARITY
PASS_ASH_TCU_K7N_C_ATOMIC_REGISTRY_SWAP
PASS_ASH_TCU_K7N_C_RUNTIME_ROUTE_MUTATION_EVIDENCE
PASS_ASH_TCU_K7N_C_REPLAY_REJECTED
PASS_ASH_TCU_K7N_C_TAMPERED_TRANSACTION_REJECTED
PASS_ASH_TCU_K7N_C_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K7N_C_NO_PRODUCTION_ADOPTION
PASS_ASH_TCU_K7N_C_NO_CANDIDATE_SLOT_MUTATION
PASS_ASH_TCU_K7N_C_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_C_NO_ROLLBACK_EXECUTION
PASS_ASH_TCU_K7N_C_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_C_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_C_PREPARED_TRANSACTION_COMMIT_RUNTIME_CAS_DEFAULT_ROUTE_ADOPTION_NO_USER_VISIBLE_NO_PRODUCTION_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

All IDs, digests, epochs, bindings, evidence references, and state transitions must be derived from the actual K7N-B prepared receipt and actual runtime registry.

## Recommended Next Patch

```txt
ASH-TCU-K7N-D
Default Route Consumer Binding / Registry Epoch And Digest Snapshot Read / Runtime Decode Selection Dry-Run / Candidate And Burn Dual Execution Comparison / No User-Visible Or Production Output Change Seal
```

## Final Seal

K7N-C performs one explicitly authorized compare-and-swap commit against the runtime-owned registry. It reproduces the K7N-B predicted after-state exactly, atomically replaces live state, increments the epoch once, pushes one rollback snapshot, appends one mutation record, emits RuntimeRouteMutation evidence for DefaultRouteMutated, rejects replay and tampering, and leaves Candidate, UserVisible, Production, runtime output, rollback execution, weights, and performance claims untouched.