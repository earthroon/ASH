# ASH-TCU-K7N-C-R1C SPEC

## Title

Explicit Commit Authority Mutation Policy SSOT / Disabled ExplicitCommitAuthorityOnly RuntimeManaged Typed Policy / Committer Policy Gate / No Hidden Mutation Bypass / Registry v3 to v4 Policy Migration / No Route State Change Seal

## Patch ID

```txt
ASH-TCU-K7N-C-R1C
```

## Status Target

```txt
PASS_ASH_TCU_K7N_C_R1C_EXPLICIT_COMMIT_AUTHORITY_MUTATION_POLICY_SSOT_NO_HIDDEN_BYPASS_NO_ROUTE_STATE_CHANGE_SEAL
```

## Parent

```txt
ASH-TCU-K7N-C-R1B
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_C_R1B_PREDICTION_COMMIT_PROVENANCE_SPLIT_BINDING_AUTHORITY_LINEAGE_NO_ROUTE_STATE_CHANGE_SEAL
```

Required prior verdict:

```txt
prediction_preparation_commit_and_effective_binding_authority_provenance_separated
```

## Purpose

K7N-C-R1C replaces the ambiguous Registry v3 string policy `disabled` with a typed mutation-policy SSOT. The historical K7N-C commit used explicit one-shot commit authority, write-lock CAS, staged mutation, and atomic swap. Therefore the effective historical policy was `ExplicitCommitAuthorityOnly`, even though the registry metadata recorded `Disabled`.

R1C introduces a typed policy enum, policy-state digest, policy evaluator, policy-bound commit authority v2, mandatory pre-lock and under-lock policy checks, executed counterexamples, and mutation-entrypoint audit. Registry identity, route epoch, routes, rollback history, logical mutation history, runtime output, model state, and performance authority remain unchanged.

## Mutation Policy

Required enum:

```rust
pub enum TensorCubeRegistryMutationPolicy {
    Disabled,
    ExplicitCommitAuthorityOnly,
    RuntimeManaged,
}
```

Semantics:

```txt
Disabled
  all mutation classes rejected

ExplicitCommitAuthorityOnly
  exactly one valid explicit one-shot commit authority required
  runtime actor absent

RuntimeManaged
  valid registered runtime actor required
  defined but not activated or exercised by R1C
```

## Required Active Policy

After migration:

```txt
active policy = ExplicitCommitAuthorityOnly
previous policy = Disabled
policy revision = 1
explicit authority required = true
runtime actor required = false
route epoch remains 1
route state changed = false
```

## Policy State

Required schema:

```txt
ash_tensorcube_registry_mutation_policy_v1
```

Required fields:

```txt
active policy
policy revision
activated-by patch
activation reason
previous policy
explicit-authority-required
runtime-actor-required
route epoch at activation
registry instance ID
policy digest
```

Required digest domain:

```txt
ash.tensorcube.registry.mutation_policy.v1
```

## Registry v4

Migrate:

```txt
ash_tensorcube_route_registry_v3
→ ash_tensorcube_route_registry_v4
```

Registry v4 contains the Registry v3 catalog, Binding v2 records, rollback stack, MutationRecord v3 ledger, typed mutation-policy state, genesis digest, and current registry digest.

Required current-registry digest domain:

```txt
ash.tensorcube.registry.current.v3
```

The Registry v3 string field `mutation_policy = "disabled"` must not survive in Registry v4.

## Policy Evaluator

All mutation permission decisions belong to:

```txt
TensorCubeRegistryMutationPolicyEvaluator
```

The evaluator validates policy schema/digest/revision, registry identity, slot, authority kind, explicit authority presence and validity, runtime actor presence, transaction identity, proposal identity, and authority consumption state.

Required authority kind:

```txt
ExplicitCommitAuthority
RuntimeManagedActor
```

## Commit Authority v2

Required schema:

```txt
ash_tensorcube_route_commit_authority_v2
```

Required additions:

```txt
policy schema version
required policy
policy revision
policy digest
```

Required policy:

```txt
ExplicitCommitAuthorityOnly
```

Historical v1 authority remains available for replay only. R1C creates a non-reactivating policy rebind showing the historical K7N-C authority was compatible with the newly explicit policy.

## Committer Policy Gate

Every route mutation committer must:

```txt
1. validate authority structure
2. read active policy
3. evaluate policy before write lock
4. reject unless decision is Allow
5. acquire write lock
6. revalidate policy revision and digest under lock
7. run normal CAS validation
8. construct staged registry
9. perform one atomic swap
```

A policy change between checks must produce `MutationPolicyChangedDuringCommit`.

No audit, test, environment variable, debug build, orchestrator, migration helper, or direct write-lock path may bypass the evaluator.

## Mutation Entrypoint Audit

R1C must inspect relevant source files for mutable registry operations such as write-lock acquisition, binding insertion, mutation-ledger push, rollback push, epoch assignment, and registry-digest assignment.

Each observed call site must be classified as:

```txt
canonical committer path
schema migration on detached state
historical test path
forbidden hidden mutation path
```

Required:

```txt
unclassified mutable call-site count = 0
forbidden bypass count = 0
```

Observed counts must come from actual source inspection.

## Executed Counterexamples

R1C must execute isolated counterexamples for Disabled/no authority, Disabled/valid explicit authority, Explicit-only/no authority, registry/transaction/proposal/slot mismatch, consumed or non-one-shot authority, policy revision or digest mismatch, runtime actor under explicit-only, RuntimeManaged without or with unknown actor, and policy change between pre-lock and under-lock validation.

Flag presence alone is insufficient. Every case must execute and return the expected specific error without mutating the authoritative registry.

## Historical Interpretation

Required diagnosis:

```txt
recorded policy = Disabled
effective historical policy = ExplicitCommitAuthorityOnly
historical policy metadata incomplete = true
historical commit authority valid = true
historical commit bypass = false
```

R1C must not relabel the K7N-C commit as unauthorized.

## No State Change

R1C must preserve registry instance ID, route epoch 1, all four route bindings, Binding v2 provenance, rollback stack, MutationRecord v3 ledger, logical mutation count 1, and genesis digest. R1C may change only registry schema, policy representation, policy revision, policy digest, and current registry digest.

No route mutation, new transaction, new RuntimeRouteMutation evidence, runtime output change, rollback execution, weight/checkpoint mutation, or performance claim is allowed.

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7n_c_r1c_mutation_policy_audit -- --repo-root <repo> --require-r1b-pass --diagnose-legacy-disabled-policy --migrate-registry-v3-to-v4 --activate-explicit-commit-authority-only --create-policy-state --create-authority-policy-rebind --validate-policy-digest --validate-policy-revision --audit-mutation-entrypoints --validate-no-hidden-bypass --execute-policy-counterexamples --preserve-registry-instance --preserve-route-state --preserve-route-epoch --preserve-mutation-history --no-route-mutation --no-runtime-output-claim --no-rollback-execution --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_C_R1C_PRIOR_R1B_RECEIPT
PASS_ASH_TCU_K7N_C_R1C_LEGACY_POLICY_DIAGNOSIS
PASS_ASH_TCU_K7N_C_R1C_MUTATION_POLICY_ENUM
PASS_ASH_TCU_K7N_C_R1C_MUTATION_POLICY_STATE
PASS_ASH_TCU_K7N_C_R1C_POLICY_DIGEST
PASS_ASH_TCU_K7N_C_R1C_POLICY_TRANSITION
PASS_ASH_TCU_K7N_C_R1C_EXPLICIT_COMMIT_AUTHORITY_ONLY_ACTIVE
PASS_ASH_TCU_K7N_C_R1C_COMMIT_AUTHORITY_V2
PASS_ASH_TCU_K7N_C_R1C_AUTHORITY_POLICY_REBIND
PASS_ASH_TCU_K7N_C_R1C_POLICY_EVALUATOR
PASS_ASH_TCU_K7N_C_R1C_PRE_LOCK_POLICY_VALIDATION
PASS_ASH_TCU_K7N_C_R1C_UNDER_LOCK_POLICY_REVALIDATION
PASS_ASH_TCU_K7N_C_R1C_MUTATION_ENTRYPOINT_AUDIT
PASS_ASH_TCU_K7N_C_R1C_POLICY_COUNTEREXAMPLES_EXECUTED
PASS_ASH_TCU_K7N_C_R1C_NO_HIDDEN_MUTATION_BYPASS
PASS_ASH_TCU_K7N_C_R1C_REGISTRY_V3_TO_V4_MIGRATION
PASS_ASH_TCU_K7N_C_R1C_REGISTRY_INSTANCE_PRESERVED
PASS_ASH_TCU_K7N_C_R1C_ROUTE_STATE_PRESERVED
PASS_ASH_TCU_K7N_C_R1C_ROUTE_EPOCH_PRESERVED
PASS_ASH_TCU_K7N_C_R1C_MUTATION_HISTORY_PRESERVED
PASS_ASH_TCU_K7N_C_R1C_NO_ROUTE_MUTATION
PASS_ASH_TCU_K7N_C_R1C_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_C_R1C_NO_ROLLBACK_EXECUTION
PASS_ASH_TCU_K7N_C_R1C_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_C_R1C_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_C_R1C_EXPLICIT_COMMIT_AUTHORITY_MUTATION_POLICY_SSOT_NO_HIDDEN_BYPASS_NO_ROUTE_STATE_CHANGE_SEAL
```

## Static Checks

Use `static_json_grouping = atlas_parallel_grouped_static_checks_v1`. All IDs, policy values, digests, call-site counts, and counterexample counts must come from actual runtime artifacts and source inspection.

## Recommended Next Patch

```txt
ASH-TCU-K7N-C-R1D
Executed Tamper Counterexample Suite / Proposal Transaction Authority Registry Policy Digest Tamper / Isolated Runtime Context / No Authoritative Registry Mutation Seal
```

## Final Seal

R1C installs `ExplicitCommitAuthorityOnly` as the typed mutation-policy SSOT. Every route mutation must pass the policy evaluator before and under the write lock. The historical K7N-C commit remains authorized, while hidden bypasses are rejected. Registry identity, route epoch, route state, rollback history, mutation history, runtime output, model state, and performance authority remain unchanged.