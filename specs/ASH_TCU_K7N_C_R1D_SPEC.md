# ASH-TCU-K7N-C-R1D SPEC

## Title

Executed Tamper Counterexample Suite / Proposal Prepared Transaction Commit Authority Registry Policy Provenance Evidence Digest Tamper / Single-Fault Isolated Runtime Context / Exact Rejection Classification / No Authoritative Registry Mutation Seal

## Patch ID

```txt
ASH-TCU-K7N-C-R1D
```

## Status Target

```txt
PASS_ASH_TCU_K7N_C_R1D_EXECUTED_TAMPER_COUNTEREXAMPLE_SUITE_EXACT_REJECTION_NO_AUTHORITATIVE_REGISTRY_MUTATION_SEAL
```

## Parent

```txt
ASH-TCU-K7N-C-R1C
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_C_R1C_EXPLICIT_COMMIT_AUTHORITY_MUTATION_POLICY_SSOT_NO_HIDDEN_BYPASS_NO_ROUTE_STATE_CHANGE_SEAL
```

Required prior verdict:

```txt
explicit_commit_authority_only_policy_installed_and_all_registry_mutations_bound_to_policy_evaluator
```

## Purpose

R1D executes a single-fault tamper suite against the real TensorCube route-control artifact graph. The untouched canonical graph must validate first. Every case mutates exactly one semantic field, executes a real semantic validator, returns the exact expected rejection class, and leaves both the authoritative Registry v4 and the isolated case registry unchanged.

The suite covers proposal, prepared transaction, predicted state, capability evidence, commit authority, policy state, Registry v4, Binding v2 provenance, MutationRecord v3, committed transaction, RuntimeRouteMutation evidence, rebind chain, and replay identity.

## Canonical Bundle

Required bundle schema:

```txt
ash_tensorcube_route_integrity_bundle_v1
```

Required inputs:

```txt
K7N-B prepared transaction
K7N-C committed transaction
K7N-C RuntimeRouteMutation evidence
R1A registry v2 and evidence rebind
R1B registry v3, provenance migration and evidence rebind
R1C registry v4, policy state, policy transition and authority policy rebind
```

The canonical bundle validates registry, policy, provenance, mutation record, prepared transaction, commit, evidence, rebind, capability and identity consistency before any tamper case executes.

Required bundle digest domain:

```txt
ash.tensorcube.route.integrity_bundle.v1
```

## Single-Fault Rule

Every case must change exactly one declared semantic field. Recomputing downstream digests, changing multiple IDs together, deleting an artifact, malformed JSON, and unrelated object replacement are forbidden.

Required per case:

```txt
single_fault_count = 1
untargeted_mismatch_count = 0
executed = true
rejected = true
exact_rejection_match = true
authoritative_registry_unchanged = true
isolated_registry_unchanged = true
panic = false
```

## Case Registry SSOT

A single static case registry owns case IDs, groups, field paths, tamper kinds and exact expected rejection reasons. Registered count, group counts, reports and PASS markers derive from that registry. No second manually maintained case list is allowed.

Required groups and counts:

```txt
proposal = 8
prepared_transaction = 8
capability = 4
authority = 12
registry_policy = 8
provenance_mutation = 10
commit_evidence = 10
rebind_replay = 6
total = 66
```

## Required Case Matrix

### Proposal

```txt
proposal_digest -> ProposalDigestMismatch
proposal_id -> ProposalIdentityMismatch
registry_instance_id -> RegistryInstanceMismatch
expected_epoch -> StaleEpoch
expected_registry_digest -> StaleRegistryDigest
route_before -> RouteBeforeMismatch
route_after -> TargetRouteMismatch
target_slot -> TargetSlotMismatch
```

### Prepared transaction

```txt
transaction_digest -> PreparedTransactionDigestMismatch
transaction_id -> TransactionIdentityMismatch
stage -> PreparedStageInvalid
predicted_epoch_after -> PredictedEpochMismatch
predicted_registry_digest_after -> PredictedRegistryDigestMismatch
predicted default binding -> PredictedBindingMismatch
before snapshot digest -> BeforeSnapshotIntegrityFailure
transition payload digest -> TransitionPayloadDigestMismatch
```

### Capability

```txt
capability execution ID -> CapabilityExecutionIdentityMismatch
capability dispatch digest -> CapabilityDispatchDigestMismatch
capability readback digest -> CapabilityReadbackDigestMismatch
catalog capability reference -> CatalogCapabilityEvidenceMismatch
```

### Authority

```txt
authority ID -> AuthorityIdentityMismatch
authority digest -> AuthorityDigestMismatch
registry instance -> AuthorityRegistryMismatch
transaction ID -> AuthorityTransactionMismatch
proposal ID -> AuthorityProposalMismatch
slot -> AuthoritySlotMismatch
consumed -> AuthorityAlreadyConsumed
one-shot -> AuthorityNotOneShot
operator explicit -> OperatorCommitNotExplicit
required policy -> AuthorityPolicyMismatch
policy revision -> AuthorityPolicyRevisionMismatch
policy digest -> AuthorityPolicyDigestMismatch
```

### Registry and policy

```txt
current registry digest -> RegistryDigestMismatch
registry instance -> RegistryInstanceMismatch
registry epoch -> RegistryEpochMismatch
active policy -> AuthorityPolicyMismatch
policy digest -> PolicyDigestMismatch
policy revision -> PolicyRevisionMismatch
policy registry instance -> PolicyRegistryInstanceMismatch
Default binding route -> BindingRouteMismatch
```

### Provenance and mutation record

```txt
provenance digest -> BindingProvenanceDigestMismatch
effective author -> EffectiveBindingAuthorityMismatch
commit executor -> CommitExecutionProvenanceMismatch
prediction origin -> PredictionOriginMismatch
provenance commit ID -> CommitIdentityMismatch
provenance runtime evidence ID -> RuntimeEvidenceIdentityMismatch
mutation record digest -> MutationRecordDigestMismatch
mutation authority ID -> AuthorityIdentityMismatch
mutation commit ID -> CommitIdentityMismatch
mutation runtime evidence ID -> RuntimeEvidenceIdentityMismatch
```

### Commit and evidence

```txt
commit digest -> CommitDigestMismatch
commit ID -> CommitIdentityMismatch
commit registry digest after -> CommittedRegistryDigestMismatch
commit epoch after -> CommittedEpochMismatch
commit runtime evidence ID -> RuntimeEvidenceIdentityMismatch
runtime evidence ID -> RuntimeEvidenceIdentityMismatch
runtime evidence registry hash -> RuntimeEvidenceRegistryDigestMismatch
runtime evidence epoch -> RuntimeEvidenceEpochMismatch
runtime evidence authority -> RuntimeEvidenceAuthorityMismatch
runtime evidence claim -> RuntimeEvidenceClaimMismatch
```

### Rebind and replay

```txt
R1A rebind v2 digest -> EvidenceRebindDigestMismatch
R1B rebind v3 digest -> EvidenceRebindDigestMismatch
R1C authority rebind policy digest -> AuthorityPolicyRebindMismatch
rebind mutation ID -> MutationIdentityMismatch
rebind commit ID -> CommitIdentityMismatch
canonical committed transaction replay -> TransactionAlreadyCommitted
```

## Isolation And Atomicity

Each case clones the canonical bundle and registry. The authoritative registry is never passed as mutable input. Before and after every case, canonical bytes and semantic invariants are compared.

A rejected case must not change route epoch, bindings, mutation ledger, rollback stack, policy state, or authority consumption state.

## Exact Rejection

A case passes only when actual rejection equals the expected stable `TensorCubeTamperRejectionReason`. Any-error acceptance, panic, parse failure, missing execution, generic wildcard mapping and silent Burn fallback are forbidden.

## Prior Artifact Integrity

R1D hashes protected prior artifacts before and after execution. Required protected-artifact rewrite count is zero.

## No-State-Change Guards

R1D must prove:

```txt
new route mutation = false
new transaction commit = false
new RuntimeRouteMutation = false
runtime consumer binding = false
runtime output change = false
rollback execution = false
weight/checkpoint mutation = false
performance claim = false
```

Registry remains `ash_tensorcube_route_registry_v4`.

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_c_r1d_tamper_suite_audit -- --repo-root <repo> --require-r1c-pass --load-canonical-integrity-bundle --validate-canonical-bundle --enforce-single-fault-injection --execute-proposal-tamper-cases --execute-prepared-transaction-tamper-cases --execute-capability-tamper-cases --execute-authority-tamper-cases --execute-registry-policy-tamper-cases --execute-provenance-mutation-tamper-cases --execute-commit-evidence-tamper-cases --execute-rebind-replay-tamper-cases --require-exact-rejection-class --verify-isolated-failure-atomicity --verify-authoritative-registry-unchanged --verify-prior-artifacts-not-rewritten --no-route-mutation --no-runtime-output-claim --no-rollback-execution --no-weight-mutation --no-performance-claim
```

## Acceptance

```txt
canonical graph failure count = 0
registered cases = 66
executed cases = 66
rejected cases = 66
unexpected allow count = 0
wrong rejection class count = 0
panic count = 0
single-fault violation count = 0
authoritative registry mutation count = 0
isolated failed-case mutation count = 0
protected artifact rewrite count = 0
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_C_R1D_PRIOR_R1C_RECEIPT
PASS_ASH_TCU_K7N_C_R1D_CANONICAL_INTEGRITY_BUNDLE
PASS_ASH_TCU_K7N_C_R1D_CANONICAL_BUNDLE_VALIDATION
PASS_ASH_TCU_K7N_C_R1D_SINGLE_FAULT_INJECTION
PASS_ASH_TCU_K7N_C_R1D_PROPOSAL_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_PREPARED_TRANSACTION_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_CAPABILITY_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_AUTHORITY_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_REGISTRY_POLICY_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_PROVENANCE_MUTATION_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_COMMIT_EVIDENCE_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_REBIND_REPLAY_TAMPER_CASES
PASS_ASH_TCU_K7N_C_R1D_EXACT_REJECTION_CLASSIFICATION
PASS_ASH_TCU_K7N_C_R1D_ALL_REGISTERED_CASES_EXECUTED
PASS_ASH_TCU_K7N_C_R1D_NO_UNEXPECTED_ALLOW
PASS_ASH_TCU_K7N_C_R1D_NO_WRONG_REJECTION_CLASS
PASS_ASH_TCU_K7N_C_R1D_NO_COUNTEREXAMPLE_PANIC
PASS_ASH_TCU_K7N_C_R1D_ISOLATED_FAILURE_ATOMICITY
PASS_ASH_TCU_K7N_C_R1D_AUTHORITATIVE_REGISTRY_UNCHANGED
PASS_ASH_TCU_K7N_C_R1D_PRIOR_ARTIFACTS_NOT_REWRITTEN
PASS_ASH_TCU_K7N_C_R1D_NO_ROUTE_MUTATION
PASS_ASH_TCU_K7N_C_R1D_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_C_R1D_NO_ROLLBACK_EXECUTION
PASS_ASH_TCU_K7N_C_R1D_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_C_R1D_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_C_R1D_EXECUTED_TAMPER_COUNTEREXAMPLE_SUITE_EXACT_REJECTION_NO_AUTHORITATIVE_REGISTRY_MUTATION_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

All case counts, group counts, artifact identities, digests and rejection results must be derived from actual runtime artifacts and the case-registry SSOT.

## Recommended Next Patch

```txt
ASH-TCU-K7N-C-R1E
Commit Receipt Self-Validation And Rebind Audit / Commit Proposal Authority Policy Registry Evidence Full Graph Digest / Orphan-Free Receipt Closure / No Route State Change Seal
```

## Final Seal

R1D executes every registered single-fault tamper case against the actual route-control artifact graph. Each case is rejected with the exact expected reason, without panic, fallback, partial mutation, prior-artifact rewrite, or authoritative registry state change.