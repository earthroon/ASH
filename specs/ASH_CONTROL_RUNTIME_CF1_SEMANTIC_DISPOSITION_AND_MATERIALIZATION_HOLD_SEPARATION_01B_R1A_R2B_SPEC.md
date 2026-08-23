# ASH-CONTROL-RUNTIME-CF1-SEMANTIC-DISPOSITION-AND-MATERIALIZATION-HOLD-SEPARATION-01B-R1A-R2B

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-DISPOSITION-AND-MATERIALIZATION-HOLD-SEPARATION-01B-R1A-R2B
Parent: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-CAPABILITY-MATRIX-AND-BATCH-MATERIALIZATION-01B-R1A-R2A
Role: semantic-result / materialization-hold / workflow-disposition axis separation
Coverage expansion: forbidden
Production authority: false
Core registry mutation: forbidden
R2A capability-matrix mutation: forbidden
104 structural-gate migration: false
Cargo compile authority migration: false
CF1 V2 producer migration: false
```

## Authority declaration

```text
Semantic Disposition Axis Separation /
Materialization Hold Axis Separation /
Workflow Disposition Axis Separation /
No Generic First-Failure Collapse /
No Incomplete-As-Semantic-Failure /
No Stale-As-Semantic-Failure /
No Unsupported-As-Semantic-Failure /
Core Materialization State SSOT Reuse /
Registry Inventory Counts /
Observed Execution Counts /
Diagnostic Full-Matrix Truth /
Legacy Fail-Fast Truth /
No Fake Semantic Check For Frozen /
No Frozen PASS Replay /
No Expected-Disposition Evaluation Input /
Ordinal 56 Semantic Failure Preservation /
Ordinal 0 Materialization Hold Preservation /
26 SemanticProjected /
54 Frozen Preserved /
No Coverage Expansion /
CONTROL-02 Authority Architecture Preservation /
R2A Capability Matrix Preservation /
Legacy Oracle 79 PASS / 1 FAIL Preserved /
15C-R1 105 / 102 / 3 Preserved /
No Production Authority Claim
```

## 1. Parent physical truth

Parent R2A physical runtime:

```text
previousProjectedCount = 25
newlyProjectedCount = 1
finalProjectedCount = 26
finalFrozenCount = 54
unclassifiedFrozenCount = 0
productionAuthorityClaimed = false
```

Pre-R2B diagnostic semantic shadow:

```text
semanticProjectedCount = 26
frozenSourceBoundActiveCount = 54
semanticIncompleteCount = 54
firstFailureOrdinal = 0
semanticProjectionClosed = false
```

`firstFailureOrdinal = 0` was ambiguous. Ordinal 0 is FrozenSourceBound, while the known executable semantic failure is ordinal 56.

## 2. Three independent axes

R2B separates:

```text
Can this validator execute?       -> Core materialization state
Did an executed program pass?     -> semantic execution state
Can the workflow continue?        -> workflow disposition
```

Core materialization remains the single SSOT via `ash_core::Cf1MaterializationState`:

```text
DeclaredInactive
FrozenSourceBound
SemanticProjected
TranslationStale
ProjectionIncomplete
Unsupported
```

No duplicate materialization enum is introduced in control-runtime.

## 3. Semantic execution state

Canonical control-runtime semantic types:

```text
Cf1SemanticDisposition
  Passed
  Failed

Cf1SemanticExecutionState
  NotExecutable
  NotExecutedFailFast
  Executed(Passed | Failed)
  DeclaredInactive
```

Legal examples:

```text
SemanticProjected + Executed(Passed)
SemanticProjected + Executed(Failed)
FrozenSourceBound + NotExecutable
TranslationStale + NotExecutable
Executable-but-skipped + NotExecutedFailFast
```

Frozen/Stale/Unsupported are not semantic failures.

## 4. Workflow disposition

```text
Completed
HeldMaterializationIncomplete
HeldTranslationStale
HeldUnsupportedProjection
FailedSemanticValidation
FailedInfrastructure
```

Workflow disposition is process/control-plane outcome and never erases individual observations.

## 5. No fake semantic checks for non-executable nodes

Frozen or stale validators no longer synthesize Unsupported/Failed semantic checks.

They report:

```text
semanticExecutionState = NotExecutable
checkCount = 0
passedCheckCount = 0
failedCheckCount = 0
unsupportedCheckCount = 0
checks = []
```

The reason is recorded separately as materialization evidence.

If an admitted program unexpectedly produces Unsupported checks, it becomes:

```text
materializationState = ProjectionIncomplete
semanticExecutionState = NotExecutable
```

rather than semantic Failed.

## 6. Registry inventory vs observed execution

Registry fields:

```text
registrySemanticProjectedCount
registryFrozenSourceBoundCount
registryTranslationStaleCount
registryProjectionIncompleteCount
registryUnsupportedCount
```

Observed fields:

```text
observedSemanticPassCount
observedSemanticFailureCount
observedFrozenHoldCount
observedTranslationStaleHoldCount
observedProjectionIncompleteHoldCount
observedUnsupportedHoldCount
notExecutedCount
```

This prevents `54 Frozen in registry` from being confused with `1 Frozen actually visited before fail-fast stopped`.

## 7. Independent first ordinals

The semantic v2 receipt retires generic semantic-route `firstFailureOrdinal` authority.

Canonical fields:

```text
firstSemanticFailureOrdinal
firstMaterializationHoldOrdinal
firstFrozenSourceBoundOrdinal
firstTranslationStaleOrdinal
firstProjectionIncompleteOrdinal
firstUnsupportedProjectionOrdinal
firstInfrastructureFailureOrdinal
```

First ordinals are category-local minima by execution ordinal.

## 8. Diagnostic Full-Matrix target

For the current 26/54 tree:

```text
workflowMode = DiagnosticFullMatrix
registrySemanticProjectedCount = 26
registryFrozenSourceBoundCount = 54
observedSemanticPassCount = 25
observedSemanticFailureCount = 1
observedFrozenHoldCount = 54
observedTranslationStaleHoldCount = 0
observedProjectionIncompleteHoldCount = 0
observedUnsupportedHoldCount = 0
notExecutedCount = 0
firstSemanticFailureOrdinal = 56
firstMaterializationHoldOrdinal = 0
firstFrozenSourceBoundOrdinal = 0
firstTranslationStaleOrdinal = null
workflowDisposition = HeldMaterializationIncomplete
semanticProjectionClosed = false
productionAuthorityClaimed = false
```

This is the primary R2B runtime regression gate.

## 9. Legacy Fail-Fast target

Ordinal 0 is FrozenSourceBound, therefore fail-fast stops before an executable semantic validator is observed:

```text
workflowMode = LegacyFailFast
registrySemanticProjectedCount = 26
registryFrozenSourceBoundCount = 54
observedSemanticPassCount = 0
observedSemanticFailureCount = 0
observedFrozenHoldCount = 1
notExecutedCount = 79
firstSemanticFailureOrdinal = null
firstMaterializationHoldOrdinal = 0
firstFrozenSourceBoundOrdinal = 0
workflowDisposition = HeldMaterializationIncomplete
semanticProjectionClosed = false
productionAuthorityClaimed = false
```

Ordinal 56 must not be claimed as observed in fail-fast because it was not executed.

## 10. Skipped-node evidence

Fail-fast still emits node observations for skipped active validators.

The receipt preserves the Executable Registry materialization state but sets:

```text
semanticExecutionState = NotExecutedFailFast
```

Skipped nodes are not source-probed and do not create runtime stale/semantic evidence.

## 11. Projection closure semantics

`SemanticProjectionClosed` means all active validators have current executable semantic materializations.

It does not mean all semantic validators pass.

A future valid state may therefore be:

```text
SemanticProjectionClosed = true
ObservedSemanticFailureCount = 1
FirstSemanticFailureOrdinal = 56
```

## 12. Ownership

```text
Core         -> canonical membership and materialization vocabulary
Factory      -> program materialization
Device       -> primitive semantic execution
Manager      -> one-validator lifecycle and semantic aggregation
Orchestrator -> workflow, fail-fast, category counts, independent first ordinals
Receipt      -> immutable observation only
```

No receipt-side re-interpretation of failure categories is allowed.

## 13. Schema promotion

```text
schema = ash.control_runtime.cf1.semantic_validation_shadow.r2b.v2
patchId = ASH-CONTROL-RUNTIME-CF1-SEMANTIC-DISPOSITION-AND-MATERIALIZATION-HOLD-SEPARATION-01B-R1A-R2B
```

The ambiguous semantic-route v1 `firstFailureOrdinal` field is not canonical in v2.

The older CF1 static-shadow route is a separate subsystem and is not redefined by R2B.

## 14. CLI output

`cf1-semantic-shadow` keeps the command surface and prints separated truth:

```text
ASH_CONTROL_RUNTIME_R2B_SEMANTIC_PROJECTION_CLOSED=...
receiptHash=...
workflowMode=...
registrySemanticProjectedCount=...
registryFrozenSourceBoundCount=...
observedSemanticPassCount=...
observedSemanticFailureCount=...
observedFrozenHoldCount=...
observedTranslationStaleHoldCount=...
observedProjectionIncompleteHoldCount=...
observedUnsupportedHoldCount=...
notExecutedCount=...
firstSemanticFailureOrdinal=...
firstMaterializationHoldOrdinal=...
firstTranslationStaleOrdinal=...
workflowDisposition=...
productionAuthorityClaimed=false
```

The process remains nonzero while semantic projection is incomplete.

## 15. Coverage preservation

R2B performs no Factory coverage expansion:

```text
SemanticProjected = 26
FrozenSourceBound = 54
DeclaredInactive = 1
CoverageExpansionCount = 0
```

No generated semantic program is changed.

Preserved program source SHA256:

```text
generated.rs       e7f2cc33388bec593647dc896cc51ca2026fb0e23378fc043eb23cf5851e7f74
generated_r1ar1.rs c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f
generated_r1ar2.rs 13c3bc10ca9dd7e41b8c403cf710ae5ffbc31d0f8499ce40cbdef0c83deb37cc
generated_r2a.rs   af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

## 16. Core and workspace preservation

```text
crates/ash_core/src/cf1_control_authority.rs
SHA256 = 14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6

Cargo.toml
SHA256 = 4beccf28819d5d7c0b5505342c090824c40a25eb7d5a6994a0f04422a999ca16
```

Both are byte-identical to the workspace/unicode-fixed parent.

## 17. Legacy oracle regression

All 80 active legacy validators were rerun after R2B source changes:

```text
ordinals 00..39 = 40 PASS / 0 FAIL
ordinals 40..79 = 39 PASS / 1 FAIL
TOTAL = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

15C-R1 remains:

```text
105 checks
102 PASS
3 scheduler-hash FAIL
```

The same validators 16, 17, and 18 remain the three scheduler-hash failures.

PowerShell producer remains byte-identical:

```text
05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## 18. Changed source surface

Exactly four source files change:

```text
crates/ash_control_runtime/src/cf1/semantic_contract.rs
crates/ash_control_runtime/src/manager/semantic_validation.rs
crates/ash_control_runtime/src/orchestrator/cf1.rs
crates/ash_control_runtime/src/main.rs
```

Core, Factory, Device, capability matrix, generated programs, legacy validators, and training sources are unchanged.

## 19. Static qualification

Bake environment has no usable Cargo/Rust toolchain, therefore physical R2B Rust compile/test PASS is not claimed here.

Static checks:

```text
changed-source delimiter sanity = PASS
invalid Rust \uXXXX escape count = 0
old semantic-route Cf1SemanticValidatorDisposition refs = 0
old semantic-route first_failure_ordinal refs = 0
old semantic-route semantic_incomplete_count refs = 0
forbidden baked artifacts = 0
```

## 20. Physical qualification

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime
```

Diagnostic runtime:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode diagnostic-full-matrix
```

Fail-fast runtime:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode legacy-fail-fast
```

Both remain fail-closed/nonzero while 54 Frozen nodes remain. Their receipts must match sections 8 and 9.

## 21. Mandatory gates

```text
PASS_R2B_CORE_REGISTRY_UNCHANGED
PASS_R2B_EXECUTABLE_REGISTRY_26_54_PRESERVED
PASS_R2B_CAPABILITY_MATRIX_UNCHANGED
PASS_R2B_GENERATED_PROGRAMS_UNCHANGED
PASS_R2B_MATERIALIZATION_AXIS_SEPARATED
PASS_R2B_SEMANTIC_DISPOSITION_AXIS_SEPARATED
PASS_R2B_WORKFLOW_DISPOSITION_AXIS_SEPARATED
PASS_R2B_NO_INCOMPLETE_AS_SEMANTIC_FAILURE
PASS_R2B_NO_STALE_AS_SEMANTIC_FAILURE
PASS_R2B_NO_UNSUPPORTED_AS_SEMANTIC_FAILURE
PASS_R2B_NO_FAKE_FROZEN_SEMANTIC_CHECK
PASS_R2B_FIRST_SEMANTIC_FAILURE_ORDINAL_INDEPENDENT
PASS_R2B_FIRST_MATERIALIZATION_HOLD_ORDINAL_INDEPENDENT
PASS_R2B_DIAGNOSTIC_25_PASS_1_FAIL_54_HOLD
PASS_R2B_DIAGNOSTIC_FIRST_SEMANTIC_FAILURE_56
PASS_R2B_DIAGNOSTIC_FIRST_MATERIALIZATION_HOLD_0
PASS_R2B_DIAGNOSTIC_NOT_EXECUTED_ZERO
PASS_R2B_FAILFAST_FIRST_MATERIALIZATION_HOLD_0
PASS_R2B_FAILFAST_SEMANTIC_FAILURE_NONE
PASS_R2B_FAILFAST_NOT_EXECUTED_79
PASS_R2B_15C_105_102_3
PASS_R2B_LEGACY_ORACLE_79_1
PASS_R2B_EXPECTED_DISPOSITION_NOT_EVALUATION_INPUT
PASS_R2B_NO_FROZEN_PASS_REPLAY
PASS_R2B_NO_COVERAGE_EXPANSION
PASS_R2B_CF1_V2_UNCHANGED
PASS_R2B_NO_104_GATE_MIGRATION
PASS_R2B_NO_CARGO_AUTHORITY_MIGRATION
PASS_R2B_NO_PRODUCTION_AUTHORITY
```

## 22. Promotion blockers

```text
RegistrySemanticProjectedCount != 26
RegistryFrozenSourceBoundCount != 54
Diagnostic ObservedSemanticPassCount != 25
Diagnostic ObservedSemanticFailureCount != 1
Diagnostic ObservedFrozenHoldCount != 54
Diagnostic FirstSemanticFailureOrdinal != 56
Diagnostic FirstMaterializationHoldOrdinal != 0
Diagnostic NotExecutedCount != 0
FailFast ObservedFrozenHoldCount != 1
FailFast FirstSemanticFailureOrdinal != null
FailFast FirstMaterializationHoldOrdinal != 0
FailFast NotExecutedCount != 79
Frozen validator receives Executed(Passed|Failed)
TranslationStale is counted as semantic Failed
Expected legacy disposition changes semantic result
Legacy oracle != 79/1
15C-R1 != 105/102/3
```

## 23. Current bake truth

```text
PatchId=ASH-CONTROL-RUNTIME-CF1-SEMANTIC-DISPOSITION-AND-MATERIALIZATION-HOLD-SEPARATION-01B-R1A-R2B
ParentSemanticProjectedCount=26
ParentFrozenSourceBoundCount=54
CoverageExpansionCount=0
CoreRegistryChanged=False
GeneratedProgramSourceChanged=False
CapabilityMatrixChanged=False
WorkspaceManifestChanged=False
LegacyDiagnosticPassCount=79
LegacyDiagnosticFailCount=1
LegacyFirstFailureOrdinal=56
Known15CR1CheckCount=105
Known15CR1PassCount=102
Known15CR1FailCount=3
SemanticReceiptSchema=ash.control_runtime.cf1.semantic_validation_shadow.r2b.v2
GenericFirstFailureSemanticRouteRetired=True
CoreMaterializationStateReused=True
ProductionAuthorityClaimed=False
PhysicalRustQualificationAvailableInBakeEnvironment=False
```

R2B closes the result-identity ambiguity before Factory coverage work resumes.
