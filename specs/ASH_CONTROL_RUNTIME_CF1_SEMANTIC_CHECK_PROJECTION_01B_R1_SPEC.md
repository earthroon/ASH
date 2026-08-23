# ASH-CONTROL-RUNTIME-CF1-SEMANTIC-CHECK-PROJECTION-01B-R1

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-CHECK-PROJECTION-01B-R1
Parent: ASH-CONTROL-RUNTIME-CF1-TYPED-VALIDATION-GRAPH-01B
Role: Rust-native independent semantic projection of legacy CF1 static validators
Production authority: false
CF1 compile receipt producer migration: false
104 structural-gate authority migration: false
Cargo compile authority migration: false
Python retirement: false
PowerShell retirement: false
Training math change: none
Optimizer change: none
Checkpoint change: none
Inference route change: none
```

## Authority declaration

```text
Frozen-Disposition Replay Retirement /
Rust-Native Semantic Evaluation /
80 Active Validator Semantic Programs /
1 Declared-Inactive Validator Preserved /

Legacy Validator Source Provenance Binding /
No Target-Source Hash Outcome Authority /

Typed Semantic Checks /
Per-Check Identity /
Per-Check Receipt /
Per-Validator Semantic Receipt /

Expected Legacy Disposition Comparison Only /
No Expected-Disposition As Evaluation Input /

Known 15C-R1 Failure Preserved /
Three Scheduler-Hash Failures Independently Reproduced /

No Python Runtime /
No Python Subprocess /
No PowerShell Subprocess /
No Cargo Subprocess In Semantic Route /

No CF1 Compile Receipt V2 Mutation /
No 104 Structural Gate Authority Migration /
No Cargo Compile Authority Migration /
No Production Receipt Migration /
No Production Authority Claim
```

## 1. Parent truth

01B established the exact legacy registry:

```text
Declared validators            = 81
Active validators              = 80
Declared inactive              = 1
Production                     = 75
Historical Preservation        = 1
Operational Recovery           = 1
Runtime Qualification          = 3
Parent validator subset        = 6
```

01B uses `FrozenSourceBound` replay. Source identity is verified and the remembered legacy PASS/FAIL is replayed. That is migration evidence, not an independently executable replacement for the Python validators.

## 2. R1 authority transition

R1 changes the flow to:

```text
current repository source
    -> Rust semantic evaluator
    -> typed check results
    -> Rust validator disposition
    -> compare with expected legacy disposition
```

The expected legacy disposition is oracle metadata only.

Mandatory invariant:

```text
changing expectedLegacyDisposition alone
    does not change semanticDisposition
    may change legacyParityMatch
```

Any code path that derives semantic PASS/FAIL from `expected_legacy_disposition` is forbidden.

## 3. Normative R1 closure

Final R1 closure requires:

```text
ActiveValidatorCount             = 80
SemanticProjectedCount           = 80
FrozenSourceBoundActiveCount     = 0
DeclaredInactiveCount            = 1
UnsupportedCheckCount            = 0
TranslationStaleCount            = 0
```

An active validator without a complete semantic program must fail closed as `SemanticProjectionIncomplete`. It must never inherit the legacy result.

## 4. Provenance versus target authority

The legacy validator itself remains SHA256-bound as translation provenance:

```text
legacyPath
legacySourceSha256
translationRevision
semanticProgramDigest
```

If the Python validator changes, the Rust projection is stale.

Target source files are different. A Rust/WGSL/JSON/source target changing must cause semantic re-evaluation of its new contents. R1 must not reject a target change merely because its old 01B input SHA changed.

```text
legacy validator source changed -> SemanticTranslationStale
target source changed           -> evaluate changed target source
```

## 5. Typed semantic families

The semantic layer must be capable of representing the actual legacy checks with explicit typed identities. Minimum families include:

```text
PathExists / PathAbsent / Utf8Readable
TextContains / TextAbsent
TextContainsAll / TextContainsNone
ExactOccurrenceCount / TokenOrder
SectionContains / SectionAbsent
SectionExactOccurrenceCount / SectionTokenOrder
BalancedBraceSection
RegexSearch / RegexFindAll / RegexSplit / RegexCount
JsonParse / JsonFieldExists / JsonFieldEquals
JsonArrayLength / JsonSetEquals / JsonSequenceEquals
FileSha256 / FileSha256Equals / DigestFanoutContains
StringSetEquals / SortedSequenceEquals / UniqueCount
RepositoryFileQuery / SourceMentionPathSetEquals
PythonSourceSyntax
RegistryProjection
TypedCustomSemantic
```

Anonymous closure-based validator authority is forbidden. Complex checks receive named custom semantic IDs.

R1 must neither strengthen nor weaken legacy checks during migration. Section-local checks stay section-local; ordering/hash checks remain ordering/hash checks; simple text checks are not silently replaced by stronger AST policy.

## 6. Per-check identity

Each projected clause records:

```text
checkId
semantic disposition
detail
```

Legacy names such as `identity:<token>`, `scheduler-hash:<validator>`, and other explicit check labels are preserved where available.

All checks inside one validator are evaluated. Legacy fail-fast applies between validators, not inside a validator.

## 7. Current legacy baseline

R1 does not repair the existing legacy failure.

Current full-matrix truth:

```text
79 PASS
1 FAIL
first failure ordinal = 56
```

The failing validator is:

```text
tools/validate_ash_bp_dk_fusion_legacy_restart_barrier_transaction_marker_classification_15c_r1_static.py
```

Current 15C-R1 result:

```text
105 checks
102 PASS
3 FAIL
```

All three failures are scheduler digest fanout failures for validators 16, 17, and 18.

## 8. 15C-R1 independent semantic projection

The Rust evaluator independently recomputes 15C-R1 from current source, including:

```text
path existence
patch identity
writer staging schema
classifier presence/retirement
pending marker semantics
commit lineage
active/historical section semantics
classifier read-only boundary
shared barrier authority
parent semantics
15/15A/15B adoption state
activation-source SHA fanout
scheduler-source SHA fanout
CF1 declaration and ordering
```

Required current result:

```text
checkCount = 105
failedCheckCount = 3
failed check IDs all start with scheduler-hash:
semanticDisposition = Failed
legacyParityMatch = true
```

R1 must not update downstream expected scheduler hashes simply to make the result green. That is a separate repair authority.

## 9. Process isolation

The semantic route itself performs no subprocess work:

```text
pythonProcessSpawnCount      = 0
powershellProcessSpawnCount  = 0
cargoProcessSpawnCount       = 0
```

No CPython embedding, Python process, PowerShell wrapper, or Cargo command is part of semantic evaluation.

Where legacy validators use Python syntax checks, final R1 projection must use a pure-Rust parse-only implementation. Registry-module users require explicit typed projections of only the fields/relations they consume. Arbitrary Python execution is forbidden.

## 10. Execution modes

The semantic route supports:

```text
LegacyFailFast
DiagnosticFullMatrix
```

After final 80-program projection, current expected full matrix is:

```text
79 semantic PASS
1 semantic FAIL
first failure ordinal 56
validator disposition parity mismatch = 0
```

Expected legacy fail-fast after final projection:

```text
56 PASS
1 FAIL
23 NotExecutedFailFast
first failure ordinal 56
```

## 11. Semantic route

```text
ash_control_runtime cf1-semantic-shadow
    --repo-root <path>
    [--receipt <path>]
    [--mode legacy-fail-fast|diagnostic-full-matrix]
```

The route publishes:

```text
ash.control_runtime.cf1.semantic_validation_shadow.v1
```

It is separate from the CF1 V2 compile receipt and the 01B frozen static-shadow receipt.

## 12. Semantic node receipt

Each node records at minimum:

```text
validatorId
executionOrdinal
legacyPath
legacySourceSha256
translationRevision
semanticProgramDigest
semanticDisposition
expectedLegacyDisposition
legacyParityMatch
checkCount
passedCheckCount
failedCheckCount
unsupportedCheckCount
checks[]
receiptHash
```

Semantic disposition is calculated before legacy comparison.

## 13. Whole semantic receipt

The whole receipt records:

```text
schema
patchId
executionMode
registryDigest

declaredValidatorCount
activeValidatorCount
declaredInactiveCount
semanticProjectedCount
frozenSourceBoundActiveCount

semanticPassCount
semanticFailCount
semanticIncompleteCount
translationStaleCount
notExecutedFailFastCount

firstFailureValidatorId
firstFailureOrdinal
legacyParityMatchCount
legacyParityMismatchCount

pythonProcessSpawnCount
powershellProcessSpawnCount
cargoProcessSpawnCount
semanticProjectionClosed
productionAuthorityClaimed
nodeReceipts
receiptHash
```

## 14. Semantic failure versus authority failure

Normal validator semantic failures include missing/forbidden tokens and digest mismatch. They are evidence, not engine crashes.

Authority failures are distinct:

```text
SemanticProjectionIncomplete
SemanticTranslationStale
SemanticUnsupported
SemanticEvaluationFailed
RegistryProjectionStale
PythonSyntaxProjectionMismatch
```

The existing ordinal-56 state is:

```text
engine failure = false
semantic validator failure = true
legacy parity match = true
```

## 15. No silent partial promotion

Until all 80 active validators are independently projected:

```text
semanticProjectionClosed = false
productionAuthorityClaimed = false
```

An unprojected node is never converted to PASS using its historical result.

## 16. Required independence tests

```text
semantic_result_does_not_depend_on_expected_legacy_disposition
changing_expected_legacy_disposition_changes_only_parity_comparison
target_source_drift_triggers_semantic_evaluation_not_frozen_binding_rejection
legacy_validator_source_drift_marks_translation_stale
all_80_active_validators_are_semantic_projected
no_active_validator_remains_frozen_source_bound
inactive_validator_has_no_semantic_program
```

Current-baseline tests after final closure:

```text
semantic_full_matrix_reproduces_79_pass_1_fail
semantic_first_failure_is_ordinal_56
semantic_15c_r1_has_105_checks
semantic_15c_r1_has_exactly_three_failed_scheduler_hash_checks
semantic_fail_fast_reproduces_56_pass_1_fail_23_not_executed
```

## 17. Authority boundaries preserved

R1 does not move:

```text
104 structural-gate physical authority
cargo fmt/check/test/build authority
PowerShell SourceTreeDigest authority
CF1 V2 production receipt writer
production binary admission
```

A legacy validator may inspect an `.args` file as part of its own semantics. That is not the same as adopting the 104 structural gates as Rust physical authority.

## 18. Bake policy

Exclude from baked source ZIP:

```text
artifacts/
artifact/
target/
__pycache__/
*.pyc
*.pyo
*.sha256
runtime-generated receipts
runtime-generated failure reports
runtime-generated manifests
```

Source contracts such as Cargo files, `.args` contracts, JSON profiles, Rust semantic implementation, and retained legacy validators remain source material.

The specification itself is committed to GitHub and need not be embedded in the baked source ZIP.

## 19. Current implementation bake status

The first 01B-R1 bake deliberately does not fake final 80-program closure.

Implemented independent semantic program:

```text
ordinal 56 / 15C-R1
105 independent Rust checks
current result: 102 PASS / 3 FAIL
legacy failure identity parity preserved
```

Remaining active validators:

```text
79 SemanticProjectionIncomplete
```

Therefore current implementation truth is:

```text
SemanticProjectedCount = 1
FrozenSourceBoundActiveCount = 79
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

This HOLD is intentional. Replaying the 79 remembered PASS results would violate the purpose of R1.

## 20. Physical toolchain qualification

When a Rust toolchain is available, intended closure includes:

```text
cargo fmt --check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo test --manifest-path crates/ash_control_runtime/Cargo.toml
```

A bake environment without Cargo/rustc/rustfmt must not claim those gates passed.

## 21. Final R1 promotion gates

```text
PASS_CONTROL01B_R1_SEMANTIC_PROGRAM_80
PASS_CONTROL01B_R1_NO_ACTIVE_FROZEN_REPLAY
PASS_CONTROL01B_R1_EXPECTED_DISPOSITION_NOT_EVALUATION_INPUT
PASS_CONTROL01B_R1_TARGET_SOURCE_HASH_AUTHORITY_RETIRED
PASS_CONTROL01B_R1_LEGACY_VALIDATOR_REVISION_BINDING_PRESERVED
PASS_CONTROL01B_R1_PER_CHECK_IDENTITY
PASS_CONTROL01B_R1_PER_CHECK_RECEIPT
PASS_CONTROL01B_R1_FULL_MATRIX_79_1_PARITY
PASS_CONTROL01B_R1_FAIL_FAST_56_1_23_PARITY
PASS_CONTROL01B_R1_FIRST_FAILURE_ORDINAL_56
PASS_CONTROL01B_R1_15C_R1_THREE_SCHEDULER_HASH_FAILURES
PASS_CONTROL01B_R1_NO_PYTHON_PROCESS
PASS_CONTROL01B_R1_NO_POWERSHELL_PROCESS
PASS_CONTROL01B_R1_NO_CARGO_PROCESS
PASS_CONTROL01B_R1_CF1_V2_UNCHANGED
PASS_CONTROL01B_R1_NO_104_GATE_AUTHORITY_MIGRATION
PASS_CONTROL01B_R1_NO_COMPILE_AUTHORITY_MIGRATION
PASS_CONTROL01B_R1_NO_PRODUCTION_AUTHORITY
PASS_CONTROL01B_R1_NO_TRAINING_MATH_CHANGE
PASS_CONTROL01B_R1_NO_OPTIMIZER_CHANGE
PASS_CONTROL01B_R1_NO_CHECKPOINT_CHANGE
PASS_CONTROL01B_R1_NO_RUNTIME_ROUTE_CHANGE
```

The current staged bake establishes the semantic route and 15C-R1 pilot but does not claim the final `SEMANTIC_PROGRAM_80` gate.

## 22. Next revision after semantic closure

After all 80 semantic programs are independently projected:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-MUTATION-PARITY-01B-R2
```

R2 mutates source fixtures and proves that legacy Python and Rust identify the same failing validator and, where observable, the same check. Only after mutation parity should the existing 15C-R1 scheduler-hash baseline be repaired and the separate 104 structural-gate authority migration begin.
