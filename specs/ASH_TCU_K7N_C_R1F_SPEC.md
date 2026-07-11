# ASH-TCU-K7N-C-R1F SPEC

## Title

Unit Test Matrix And Truth Repair Final Seal / Digest Provenance Policy Tamper Closure Regression Suite / Deterministic Receipt Replay / Isolated Commit Atomicity / K7N-C-R1 Final Acceptance / No Runtime Consumer Binding Seal

## Patch ID

```txt
ASH-TCU-K7N-C-R1F
```

## Status Target

```txt
PASS_ASH_TCU_K7N_C_R1F_UNIT_TEST_MATRIX_TRUTH_REPAIR_FINAL_SEAL_NO_RUNTIME_CONSUMER_BINDING
```

## Parent

```txt
ASH-TCU-K7N-C-R1E
```

Required prior status:

```txt
PASS_ASH_TCU_K7N_C_R1E_COMMIT_RECEIPT_SELF_VALIDATION_FULL_REBIND_ORPHAN_FREE_GRAPH_CLOSURE_NO_ROUTE_STATE_CHANGE_SEAL
```

Required prior verdict:

```txt
legacy_and_canonical_commit_receipts_self_validated_and_full_receipt_graph_closed_without_orphans
```

## Purpose

K7N-C-R1F converts the completed K7N-C truth-repair chain into one deterministic executable regression contract.

It binds and tests:

```txt
R1A
  registry digest domain separation
  canonical JSON and non-recursive digest semantics
  predicted/actual digest parity

R1B
  prediction, preparation and commit provenance separation
  binding authority lineage and identity closure

R1C
  typed mutation-policy SSOT
  explicit commit authority policy gate
  pre-lock and under-lock policy checks

R1D
  66 single-fault tamper counterexamples
  exact rejection classification
  isolated failure atomicity

R1E
  legacy commit digest reproduction
  canonical commit receipt v2
  Registry v1 to v4 rebind closure
  orphan-free receipt graph and closure root
```

R1F is the final acceptance patch for K7N-C-R1. It does not bind a decoder, attention, FFN, matmul, LM-head, sampler, training, inference, or output-publication consumer.

## Scope Boundary

R1F may create test definitions, execution receipts, invariant coverage, determinism receipts, detached concurrency receipts, runtime-consumer audits, and a final acceptance seal.

R1F must not create:

```txt
Registry v5
Binding v3
MutationRecord v4
Commit receipt v3
new route mutation
new RuntimeRouteMutation evidence
runtime consumer selection
UserVisible or Production promotion
weight mutation
performance promotion
```

Registry authority remains:

```txt
ash_tensorcube_route_registry_v4
```

## Test Registry SSOT

All mandatory tests are owned by one static registry:

```rust
pub const K7N_C_R1F_TEST_MATRIX:
    &[TensorCubeTruthRepairTestDefinition] = &[
        // all mandatory tests
    ];
```

The registry is the sole source of:

```txt
test IDs
test names
group counts
owner patch
invariant coverage
execution kind
expected outcome
registered test count
report rows
PASS eligibility
```

No second manually maintained test list is allowed.

Required:

```txt
registered test count = 72
duplicate test ID count = 0
duplicate test name count = 0
```

## Test Matrix

```txt
R1A Digest Semantics       8
R1B Provenance             8
R1C Mutation Policy       12
R1D Tamper Binding        10
R1E Receipt Closure       12
Serialization Determinism  8
Commit Atomicity           6
Final State Guards         8
────────────────────────────
Total                      72
```

The total and group counts must be calculated from the registry SSOT.

## R1A Digest Semantics Group

Required tests:

```txt
R1F-A01 Canonical JSON Stable
R1F-A02 Digest Domain Separation
R1F-A03 Transition Digest Non-Recursive
R1F-A04 Mutation Record Non-Recursive
R1F-A05 Registry Digest Single Final Pass
R1F-A06 Registry v1 to v2 State Preservation
R1F-A07 K7N-B Predicted / K7N-C Actual Digest Parity
R1F-A08 Legacy Receipt Immutability
```

The same semantic payload must hash differently under distinct digest domains. Transition, mutation-record, registry, commit, and graph digests must exclude their own output fields and downstream final digests.

## R1B Provenance Group

Required tests:

```txt
R1F-B01 Legacy bound_by_patch Field Removed
R1F-B02 Generic evidence_id Field Removed
R1F-B03 Prediction Origin = ASH-TCU-K7N-B
R1F-B04 Prepared By = ASH-TCU-K7N-B
R1F-B05 Commit Executed By = ASH-TCU-K7N-C
R1F-B06 Effective Binding Author = ASH-TCU-K7N-C
R1F-B07 Prediction Evidence / Runtime Evidence Split
R1F-B08 Identity Graph Complete And Orphan-Free
```

Required identity closure:

```txt
proposal
transaction
authority
commit
mutation
RuntimeRouteMutation evidence
```

Mismatch and orphan counts must be zero.

## R1C Mutation Policy Group

Required tests:

```txt
R1F-C01 Policy Enum Round Trip
R1F-C02 Registry v4 Active Policy
R1F-C03 Policy Digest Validation
R1F-C04 Disabled Rejects Explicit Authority
R1F-C05 Explicit Policy Rejects Missing Authority
R1F-C06 Explicit Policy Accepts Exact Authority
R1F-C07 Runtime Actor Rejected Under Explicit Policy
R1F-C08 Authority Policy Revision Mismatch
R1F-C09 Authority Policy Digest Mismatch
R1F-C10 Pre-Lock Policy Check Present
R1F-C11 Under-Lock Policy Revalidation Present
R1F-C12 No Hidden Mutation Entrypoint
```

Required active policy:

```txt
explicit_commit_authority_only
```

Exact rejection classes must be checked. A generic error does not pass.

## R1D Tamper Receipt Binding Group

R1F does not replace or rerun the R1D 66-case suite. It binds its authoritative receipts.

Required tests:

```txt
R1F-D01 Registered Cases = 66
R1F-D02 Executed Cases = Registered Cases
R1F-D03 Rejected Cases = Registered Cases
R1F-D04 Wrong Rejection Class Count = 0
R1F-D05 Unexpected Allow Count = 0
R1F-D06 Panic Count = 0
R1F-D07 Single-Fault Violation Count = 0
R1F-D08 Authoritative Registry Mutation Count = 0
R1F-D09 Isolated Failed-Case Mutation Count = 0
R1F-D10 Integrity Bundle / Case Registry / Verdict Digest Binding
```

## R1E Receipt Closure Group

Required tests:

```txt
R1F-E01 Legacy Commit Digest Reproduction
R1F-E02 Canonical Commit v2 Digest
R1F-E03 Commit-State / Current-State Separation
R1F-E04 Registry v1 to v2 Chain
R1F-E05 Registry v2 to v3 Chain
R1F-E06 Registry v3 to v4 Chain
R1F-E07 Binding Provenance Closure
R1F-E08 MutationRecord v3 Closure
R1F-E09 Receipt Graph Node Closure
R1F-E10 Receipt Graph Edge Closure
R1F-E11 Receipt Graph Acyclic
R1F-E12 Closure Root Validation
```

The historical commit-state Registry v1 digest and current Registry v4 digest are expected to differ. This difference is semantic separation, not failure.

## Serialization Determinism Group

Required tests:

```txt
R1F-F01 Registry v4 JSON Round Trip
R1F-F02 Commit v2 Round Trip
R1F-F03 Receipt Graph Round Trip
R1F-F04 Validation Envelope Round Trip
R1F-F05 Closure Root Round Trip
R1F-F06 Same-Input Replay Digest
R1F-F07 Filesystem Discovery Order Independence
R1F-F08 Host Metadata Exclusion
```

Canonical digests must not include:

```txt
absolute repository path
Windows drive letter
audit timestamp
cargo target path
host name
user name
CPU model
GPU model
```

## Commit Atomicity Group

All commit probes use detached isolated state. The authoritative Registry v4 must never be passed as mutable input.

Required tests:

```txt
R1F-G01 Rejected Commit Leaves State Unchanged
R1F-G02 Policy Change Between Checks Is Rejected
R1F-G03 Concurrent One-Shot Authority Has Exactly One Winner
R1F-G04 No Partial Ledger Append
R1F-G05 No Partial Rollback Push
R1F-G06 Atomic Registry Swap
```

Concurrent one-shot requirements:

```txt
successful commit count = 1
rejected commit count = 1
final epoch delta = 1
final ledger delta = 1
final rollback delta = 1
partial mutation count = 0
```

## Final State Guard Group

Required tests:

```txt
R1F-H01 Registry Schema Remains v4
R1F-H02 Registry Instance Unchanged
R1F-H03 Route Epoch Remains 1
R1F-H04 Route Bindings Unchanged
R1F-H05 Mutation And Rollback History Unchanged
R1F-H06 Runtime Consumer Unbound
R1F-H07 Protected Artifacts Unchanged
R1F-H08 No Promotion Claims
```

Required route state:

```txt
Candidate = ash_tcu_k6p_row_major_emit_candidate_v1
Default = ash_tcu_k6p_row_major_emit_candidate_v1
UserVisible = burn_baseline
Production = burn_baseline
mutation count = 1
rollback count = 1
```

## Runtime Consumer Binding Audit

R1F must scan route-reader and registry references across decoder, attention, FFN, matmul, LM-head, sampler, training, inference, and output-publication domains.

References must be classified as:

```txt
control-plane declaration
audit-only read
test-only read
detached migration
actual runtime consumer
```

Required:

```txt
actual runtime consumer count = 0
unclassified consumer reference count = 0
runtime consumer bound = false
```

This audit becomes the baseline for K7N-D0.

## Truth-Repair Invariant Coverage

Every registered test binds one truth-repair invariant. Every invariant must have executable test coverage and authoritative receipt coverage.

Required:

```txt
uncovered invariant count = 0
ambiguous invariant owner count = 0
```

Canonical invariant owners are explicit for R1A, R1B, R1C, R1D, R1E, and R1F. Test ownership and invariant ownership must not be silently inferred from file names.

## Failure Atomicity

Every rejected isolated mutation must preserve:

```txt
registry bytes
registry digest
epoch
bindings
mutation ledger
rollback stack
policy state
authority consumption state
```

A rejected test that partially mutates isolated state fails R1F.

## Protected Artifact Guard

R1F hashes protected R1A through R1E receipts before and after the complete matrix.

Protected files include the K7N-B prepared transaction, K7N-C commit and RuntimeRouteMutation evidence, R1A to R1C migration and rebind receipts, R1D integrity/tamper receipts, and R1E commit-v2/graph/envelope/closure-root receipts.

Required:

```txt
protected artifact rewrite count = 0
authoritative Registry v4 byte equality = true
```

R1F writes only under R1F runtime and artifact paths.

## Panic And Skip Policy

Every mandatory test executes through an explicit result boundary.

Required:

```txt
skipped = 0
panicked = 0
```

A panic, missing input, compile-only result, generic error, or skipped mandatory test cannot satisfy an expected outcome.

## Required Implementation

```txt
crates/burn_webgpu_backend/src/tensorcube_k7n_c_r1f_truth_repair.rs
crates/burn_webgpu_backend/src/tensorcube_truth_repair_*.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_c_r1f_*.rs
crates/orchestrator_local/src/ash_tcu_k7n_c_r1f_truth_repair_final_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_c_r1f_truth_repair_final_audit.rs
```

Required focused tests:

```txt
ash_tcu_k7n_c_r1f_test_registry.rs
ash_tcu_k7n_c_r1f_r1a_digest_matrix.rs
ash_tcu_k7n_c_r1f_r1b_provenance_matrix.rs
ash_tcu_k7n_c_r1f_r1c_policy_matrix.rs
ash_tcu_k7n_c_r1f_r1d_receipt_binding.rs
ash_tcu_k7n_c_r1f_r1e_closure_matrix.rs
ash_tcu_k7n_c_r1f_serialization_determinism.rs
ash_tcu_k7n_c_r1f_concurrent_one_shot_authority.rs
ash_tcu_k7n_c_r1f_failure_atomicity.rs
ash_tcu_k7n_c_r1f_runtime_consumer_unbound.rs
ash_tcu_k7n_c_r1f_protected_artifacts_immutable.rs
ash_tcu_k7n_c_r1f_final_seal.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_c_r1f_truth_repair_final_audit -- `
  --repo-root <repo> `
  --require-r1e-pass `
  --load-r1a-r1e-authoritative-receipts `
  --build-test-registry `
  --require-72-registered-tests `
  --execute-r1a-digest-tests `
  --execute-r1b-provenance-tests `
  --execute-r1c-policy-tests `
  --validate-r1d-tamper-receipt `
  --execute-r1e-closure-tests `
  --execute-serialization-determinism-tests `
  --execute-isolated-commit-atomicity-tests `
  --audit-runtime-consumer-binding `
  --require-all-tests-executed `
  --require-all-tests-passed `
  --require-no-test-panic `
  --require-no-test-skip `
  --require-no-uncovered-invariants `
  --verify-authoritative-registry-unchanged `
  --verify-prior-artifacts-not-rewritten `
  --write-test-registry-receipt `
  --write-test-results `
  --write-invariant-coverage `
  --write-final-seal `
  --no-route-mutation `
  --no-runtime-consumer-binding `
  --no-runtime-output-claim `
  --no-rollback-execution `
  --no-weight-mutation `
  --no-performance-claim
```

## Required Runtime Outputs

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_report_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_prior_receipt_binding_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_test_registry_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_test_results_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_test_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_group_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_invariant_coverage_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_determinism_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_concurrency_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_runtime_consumer_audit_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_protected_artifact_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_final_seal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7n_c_r1f_verdict_latest.json
artifacts/ASH_TCU_K7N_C_R1F_LOCAL_MANIFEST.json
```

## Required Final Values

```txt
registered = 72
executed = 72
passed = 72
failed = 0
skipped = 0
panicked = 0
exact outcome mismatch = 0

uncovered invariant count = 0
ambiguous invariant owner count = 0

concurrent one-shot success = 1
concurrent one-shot rejection = 1
partial mutation count = 0

actual runtime consumer count = 0
unclassified consumer reference count = 0

authoritative registry mutation count = 0
protected artifact rewrite count = 0
```

## PASS Markers

```txt
PASS_ASH_TCU_K7N_C_R1F_PRIOR_R1E_RECEIPT
PASS_ASH_TCU_K7N_C_R1F_R1A_R1E_CHAIN_BINDING
PASS_ASH_TCU_K7N_C_R1F_TEST_REGISTRY_SSOT
PASS_ASH_TCU_K7N_C_R1F_72_TESTS_REGISTERED
PASS_ASH_TCU_K7N_C_R1F_ALL_TESTS_EXECUTED
PASS_ASH_TCU_K7N_C_R1F_ALL_TESTS_PASSED
PASS_ASH_TCU_K7N_C_R1F_NO_TEST_SKIP
PASS_ASH_TCU_K7N_C_R1F_NO_TEST_PANIC
PASS_ASH_TCU_K7N_C_R1F_EXACT_OUTCOME_MATCH
PASS_ASH_TCU_K7N_C_R1F_R1A_DIGEST_SEMANTICS_MATRIX
PASS_ASH_TCU_K7N_C_R1F_R1B_PROVENANCE_MATRIX
PASS_ASH_TCU_K7N_C_R1F_R1C_POLICY_MATRIX
PASS_ASH_TCU_K7N_C_R1F_R1D_TAMPER_RECEIPT_BINDING
PASS_ASH_TCU_K7N_C_R1F_R1E_RECEIPT_CLOSURE_MATRIX
PASS_ASH_TCU_K7N_C_R1F_CANONICAL_SERIALIZATION_DETERMINISM
PASS_ASH_TCU_K7N_C_R1F_SAME_INPUT_REPLAY_DETERMINISM
PASS_ASH_TCU_K7N_C_R1F_FILESYSTEM_ORDER_INDEPENDENCE
PASS_ASH_TCU_K7N_C_R1F_HOST_METADATA_EXCLUDED
PASS_ASH_TCU_K7N_C_R1F_REJECTED_COMMIT_ATOMICITY
PASS_ASH_TCU_K7N_C_R1F_POLICY_CHANGE_DURING_COMMIT_REJECTED
PASS_ASH_TCU_K7N_C_R1F_CONCURRENT_ONE_SHOT_EXACTLY_ONE_COMMIT
PASS_ASH_TCU_K7N_C_R1F_NO_PARTIAL_LEDGER_APPEND
PASS_ASH_TCU_K7N_C_R1F_NO_PARTIAL_ROLLBACK_PUSH
PASS_ASH_TCU_K7N_C_R1F_ATOMIC_REGISTRY_SWAP
PASS_ASH_TCU_K7N_C_R1F_INVARIANT_COVERAGE_COMPLETE
PASS_ASH_TCU_K7N_C_R1F_NO_AMBIGUOUS_INVARIANT_OWNER
PASS_ASH_TCU_K7N_C_R1F_RUNTIME_CONSUMER_AUDIT
PASS_ASH_TCU_K7N_C_R1F_NO_RUNTIME_CONSUMER_BOUND
PASS_ASH_TCU_K7N_C_R1F_AUTHORITATIVE_REGISTRY_UNCHANGED
PASS_ASH_TCU_K7N_C_R1F_PRIOR_ARTIFACTS_NOT_REWRITTEN
PASS_ASH_TCU_K7N_C_R1F_NO_ROUTE_MUTATION
PASS_ASH_TCU_K7N_C_R1F_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7N_C_R1F_NO_ROLLBACK_EXECUTION
PASS_ASH_TCU_K7N_C_R1F_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7N_C_R1F_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7N_C_R1F_TRUTH_REPAIR_FINAL_SEAL
PASS_ASH_TCU_K7N_C_R1F_UNIT_TEST_MATRIX_TRUTH_REPAIR_FINAL_SEAL_NO_RUNTIME_CONSUMER_BINDING
```

## Acceptance Criteria

R1F is accepted only if:

1. R1E prior status, verdict, closure root, and protected artifact guards validate.
2. All required R1A through R1E receipts exist and status mismatch count is zero.
3. One registry owns exactly 72 unique mandatory tests.
4. Every test executes and passes with its exact expected outcome.
5. No mandatory test is skipped or panics.
6. All truth-repair invariants have executable and receipt-backed coverage.
7. Serialization and same-input replay are deterministic.
8. Filesystem discovery order and host metadata do not affect canonical digests.
9. Rejected isolated commits leave no partial state.
10. Concurrent one-shot authority produces exactly one winner and one explicit rejection.
11. Registry schema, instance, epoch, bindings, mutation ledger, rollback stack, and policy state remain unchanged.
12. Runtime consumer and unclassified consumer-reference counts are zero.
13. The authoritative Registry v4 and protected prior artifacts remain byte-identical.
14. No new route mutation, RuntimeRouteMutation evidence, runtime output change, rollback, weight mutation, performance claim, or production promotion occurs.
15. The final seal digest validates and K7N-C-R1 is declared complete.

## Recommended Next Patch

```txt
ASH-TCU-K7N-D0
Runtime Consumer Owner Audit / Decoder Attention FFN Matmul LM-Head Sampler Consumer Inventory / Route Read Authority And State Ownership Map / No Execution Path Change Seal
```

## Final Seal

R1F converts the K7N-C truth-repair chain into an executable regression baseline.

R1A digest semantics remain non-recursive. R1B provenance remains separated. R1C policy remains explicit and authority-bound. R1D tamper rejection remains complete and exact. R1E receipt closure remains deterministic and orphan-free.

All 72 mandatory tests execute and pass. Every invariant is covered. Detached concurrency preserves one-shot atomicity. The authoritative Registry v4 and protected receipts remain unchanged. No runtime consumer is bound.

K7N-C-R1 is complete and ready for K7N-D0 runtime-consumer ownership audit.