# ASH-CONTROL-RUNTIME-CF1-SEMANTIC-SCAFFOLD-SEPARATION-AND-SYMBOLIC-DATAFLOW-01B-R1A-R2C

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-SCAFFOLD-SEPARATION-AND-SYMBOLIC-DATAFLOW-01B-R1A-R2C
Parent: ASH-CONTROL-RUNTIME-CF1-PYTHON-FIND-RANGE-ARGUMENT-PROJECTION-PARITY-01B-R1A-R2B1
Role: proven reporting/aggregation scaffold separation from semantic capability debt
Coverage expansion: 0
Production authority: false
Core registry mutation: forbidden
Existing semantic-program mutation: forbidden
104 structural-gate migration: false
Cargo authority migration: false
CF1 V2 producer migration: false
```

## Authority declaration

```text
Legacy Validator Semantic Body /
Reporting Scaffold Separation /
Check Collection Scaffold /
Failure Aggregation Scaffold /
Result Reporting Scaffold /
Process Exit Scaffold /
Argument Parsing Scaffold /
Main Entry Scaffold /
Parser-Admission Before Classification /
Check-Result Provenance /
No Syntax-Only If Debt /
No Syntax-Only Comprehension Debt /
No Semantic-Clause Deletion /
No Validator-Specific Skip Table /
No Line-Number Skip /
No Expected-Disposition Driven Classification /
No Python Runtime /
No importlib Execution /
No eval /
No exec /
R2B Disposition Axis Preservation /
R2B1 Python Find Parity Preservation /
26 SemanticProjected Preservation /
54 Frozen Preservation /
Legacy Oracle 79 PASS / 1 FAIL /
15C-R1 105 / 102 / 3 /
No Production Authority Claim
```

## 1. Parent physical truth

R2B1 was physically observed locally as:

```text
workflowMode = DiagnosticFullMatrix
registrySemanticProjectedCount = 26
registryFrozenSourceBoundCount = 54
observedSemanticPassCount = 25
observedSemanticFailureCount = 1
observedFrozenHoldCount = 54
notExecutedCount = 0
firstSemanticFailureOrdinal = 56
firstMaterializationHoldOrdinal = 0
workflowDisposition = HeldMaterializationIncomplete
semanticProjectionClosed = false
productionAuthorityClaimed = false
```

This is the R2C semantic execution baseline.

## 2. Problem

The R2A capability matrix conservatively classified Python control-flow syntax itself as semantic debt.

Parent blocker counts:

```text
SymbolicCondition = 52
StaticComprehension = 49
RepositoryQuery = 22
RegexSearch = 18
JsonStructured = 15
SetSequenceRelation = 13
RegistryStaticProjection = 12
RegexCapture = 9
SectionBalancedBrace = 7
PythonSyntaxValidation = 5
DigestCanonicalRecipe = 1
```

Some `if` and comprehension syntax belongs only to result collection/reporting:

```text
semantic check result
  -> check collection
  -> failure aggregation
  -> result reporting
  -> process exit
```

Those operations are not target-source semantic requirements.

## 3. R2C classifier

New Factory-side source:

```text
crates/ash_control_runtime/src/cf1/scaffold.rs
```

Classifier revision:

```text
control01b-r1a-r2c-semantic-scaffold-dataflow
```

Typed scaffold classes:

```text
CheckCollection
FailureAggregation
ResultReporting
ProcessExit
ArgumentParsing
MainEntry
```

All legacy source is still admitted through the existing pure-Rust `rustpython-parser` path before scaffold classification. The classifier is deny-by-default in the semantic direction: uncertain conditions remain semantic debt rather than being silently discarded.

## 4. Classification rule

R2C does not remove `if` or comprehensions by syntax alone.

A construct is retired from semantic debt only when its dataflow is provably downstream of already-computed check results, for example:

```python
failed = [name for name, ok in checks if not ok]
if failed:
    raise SystemExit(1)
```

The comprehension is `FailureAggregation`; the `if` is `ProcessExit`.

By contrast:

```python
if "feature" in source:
    ...
```

remains `SymbolicCondition` because it depends on target source.

A semantic comprehension such as:

```python
matches = [line for line in source.splitlines() if "foo" in line]
```

remains `StaticComprehension` debt.

## 5. No validator-specific exceptions

Forbidden:

```text
validator-ID skip rules
line-number skip rules
expected PASS/FAIL driven classification
source-hash outcome hardcoding
```

Classification is generic over check-collection names and failure-aggregate dataflow.

## 6. Capability matrix schema

Current canonical schema:

```text
ash.control_runtime.cf1.semantic_scaffold_dataflow.r2c.v1
```

The existing command remains:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-factory-capability-matrix `
  --repo-root .
```

Default receipt path becomes:

```text
artifacts/control_runtime/cf1_semantic_scaffold_dataflow/r2c_semantic_scaffold_dataflow_receipt.json
```

## 7. Receipt additions

R2C receipt adds:

```text
symbolicConditionBeforeCount
symbolicConditionAfterCount
staticComprehensionBeforeCount
staticComprehensionAfterCount
semanticStatementCount
scaffoldStatementCount
collectorScaffoldCount
failureAggregationScaffoldCount
resultReportingScaffoldCount
processExitScaffoldCount
argumentParsingScaffoldCount
mainEntryScaffoldCount
unclassifiedSemanticRelevantStatementCount
scaffoldClassifierRevision
capabilityBlockerFreeFrozenCount
```

Each Frozen matrix entry also binds:

```text
scaffoldAnalysis
scaffoldClassificationDigest
```

into its requirement digest.

## 8. Actual staged reclassification truth

The parent counts are reproduced before R2C filtering:

```text
SymbolicConditionBeforeCount = 52
StaticComprehensionBeforeCount = 49
```

After proven scaffold separation:

```text
SymbolicConditionAfterCount = 50
StaticComprehensionAfterCount = 46
```

Other substantive blocker counts remain:

```text
RepositoryQuery = 22
RegexSearch = 18
JsonStructured = 15
SetSequenceRelation = 13
RegistryStaticProjection = 12
RegexCapture = 9
SectionBalancedBrace = 7
PythonSyntaxValidation = 5
DigestCanonicalRecipe = 1
```

The reduction is therefore limited to proven scaffold debt:

```text
SymbolicCondition retired from debt = 2 validators
StaticComprehension retired from debt = 3 validators
```

## 9. Scaffold observation totals

For the current 54 Frozen validators, the staged classifier observes:

```text
SemanticStatementCount = 441
ScaffoldStatementCount = 323

CheckCollection = 55
FailureAggregation = 58
ResultReporting = 139
ProcessExit = 53
ArgumentParsing = 18
MainEntry = 0

UnclassifiedSemanticRelevantStatementCount = 0
```

These counts are classifier observations, not canonical validator membership.

## 10. Capability-blocker-free Frozen validators

R2C produces three Frozen validators with no remaining partial/unsupported capability blocker:

```text
cf1.production.ash-bp-dk-generation-revision-stale-observation-seal-02-static
cf1.production.ash-bp-dk-bridge-pair-evidence-source-closure-03a-static
cf1.production.ash-bp-dk-fusion-managed-trainer-authority-windows-lock-durability-recovery-15b-r1-static
```

Therefore:

```text
CapabilityBlockerFreeFrozenCount = 3
```

They are **not** promoted in R2C.

Capability closure alone is insufficient for atomic materialization admission. R2C does not yet have a per-validator certificate proving:

```text
all legacy semantic clauses mapped
compiled check count complete
unmapped semantic clause count = 0
program identity valid
```

So the legal state remains FrozenSourceBound.

## 11. Coverage preservation

```text
PreviousProjectedCount = 26
PreviousFrozenCount = 54
NewlyProjectedCount = 0
FinalProjectedCount = 26
FinalFrozenCount = 54
UnclassifiedFrozenCount = 0
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

No partial program is admitted.

## 12. Existing semantic programs preserved

R2C does not modify semantic execution programs.

```text
generated.rs       SHA256 e7f2cc33388bec593647dc896cc51ca2026fb0e23378fc043eb23cf5851e7f74
generated_r1ar1.rs SHA256 c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f
generated_r1ar2.rs SHA256 8425b9455ed67ee5b3c92c1492a2a11a9b2368d53be4c6013e025f74adcc8cc1
generated_r2a.rs   SHA256 af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

`programs/mod.rs` and `device/semantic.rs` are also byte-identical to R2B1.

Thus the physically observed R2B1 semantic baseline remains the required R2C regression target:

```text
25 semantic PASS
1 semantic FAIL
firstSemanticFailureOrdinal = 56
firstMaterializationHoldOrdinal = 0
```

## 13. Core / workspace preservation

```text
Cargo.toml
SHA256 = 4beccf28819d5d7c0b5505342c090824c40a25eb7d5a6994a0f04422a999ca16

crates/ash_core/src/cf1_control_authority.rs
SHA256 = 14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6
```

Both are byte-identical to R2B1.

## 14. R2B disposition preservation

The following R2B files are byte-identical:

```text
crates/ash_control_runtime/src/cf1/semantic_contract.rs
crates/ash_control_runtime/src/manager/semantic_validation.rs
crates/ash_control_runtime/src/orchestrator/cf1.rs
```

R2C cannot merge materialization HOLD back into semantic failure.

## 15. Legacy oracle regression

All active legacy validators were rerun in migration/reference mode after the R2C changes.

Observed:

```text
ordinals 00..55 = 56 PASS
ordinal 56 = FAIL
ordinals 57..79 = 23 PASS
TOTAL = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

15C-R1 remains:

```text
105 checks
102 PASS
3 scheduler-hash FAIL
```

The three failures are unchanged scheduler-hash checks for downstream validators 16, 17, and 18.

## 16. Changed source surface

Exactly five source files differ from R2B1:

```text
crates/ash_control_runtime/src/cf1/scaffold.rs                    NEW
crates/ash_control_runtime/src/cf1/capability_matrix.rs
crates/ash_control_runtime/src/cf1/compiler.rs
crates/ash_control_runtime/src/cf1/mod.rs
crates/ash_control_runtime/src/main.rs
```

Current SHA256:

```text
scaffold.rs          93132b0c4964deb049a770ff75293a89f3912e853649b3510da370f683799d70
capability_matrix.rs ce8e2f798e81864a215489570aa7cdab57600fda23166c1421716771d2c55c28
compiler.rs          7f1899f5c79404bde3d9cbdb4868c274c97cc213811062a01b3d9237d7ea5bda
cf1/mod.rs           ca7c8270f99071ca84a8369b5cc3ce9b5a2c55431172e52831235fc4e4343f91
main.rs              7392bc1bd17bdf363b23c90108a6a6b6159e17c2a0a3f47a7d993e54b1827f3b
```

## 17. Static qualification

Bake environment has no usable Cargo/Rust toolchain, so physical `cargo check/test` PASS is not claimed.

Completed static gates:

```text
changed Rust delimiter sanity = PASS
legacy parent blocker reproduction = 52 / 49
R2C blocker result = 50 / 46
Frozen matrix cardinality = 54
capability-blocker-free Frozen = 3
invalid Python-runtime fallback added = false
generated semantic program changes = 0
Core changes = 0
R2B disposition changes = 0
forbidden baked artifacts = 0
```

## 18. Local physical qualification

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime
```

Capability matrix:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-factory-capability-matrix `
  --repo-root .
```

Expected decisive values:

```text
previousProjectedCount=26
newlyProjectedCount=0
finalProjectedCount=26
finalFrozenCount=54
unclassifiedFrozenCount=0
capabilityBlockerFreeFrozenCount=3
symbolicConditionBeforeCount=52
symbolicConditionAfterCount=50
staticComprehensionBeforeCount=49
staticComprehensionAfterCount=46
unclassifiedSemanticRelevantStatementCount=0
productionAuthorityClaimed=false
```

Semantic regression:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode diagnostic-full-matrix
```

Expected:

```text
observedSemanticPassCount=25
observedSemanticFailureCount=1
firstSemanticFailureOrdinal=56
firstMaterializationHoldOrdinal=0
```

## 19. Mandatory gates

```text
PASS_R2C_PARENT_R2B1_PARITY_PRESERVED
PASS_R2C_CORE_REGISTRY_UNCHANGED
PASS_R2C_EXISTING_26_PROGRAMS_BYTE_IDENTICAL
PASS_R2C_SCAFFOLD_TAXONOMY_TYPED
PASS_R2C_CHECK_COLLECTION_CLASSIFICATION
PASS_R2C_FAILURE_AGGREGATION_CLASSIFICATION
PASS_R2C_RESULT_REPORTING_CLASSIFICATION
PASS_R2C_PROCESS_EXIT_CLASSIFICATION
PASS_R2C_ARGUMENT_PARSING_CLASSIFICATION
PASS_R2C_NO_SYNTAX_ONLY_IF_DEBT
PASS_R2C_NO_SYNTAX_ONLY_COMPREHENSION_DEBT
PASS_R2C_SOURCE_DEPENDENT_IF_PRESERVED
PASS_R2C_SEMANTIC_COMPREHENSION_PRESERVED
PASS_R2C_PARENT_BLOCKERS_52_49_REPRODUCED
PASS_R2C_SYMBOLIC_CONDITION_50
PASS_R2C_STATIC_COMPREHENSION_46
PASS_R2C_CAPABILITY_BLOCKER_FREE_FROZEN_3
PASS_R2C_UNCLASSIFIED_FROZEN_ZERO
PASS_R2C_UNCLASSIFIED_SEMANTIC_RELEVANT_ZERO
PASS_R2C_NO_VALIDATOR_SPECIFIC_SKIP
PASS_R2C_NO_LINE_NUMBER_SKIP
PASS_R2C_EXPECTED_DISPOSITION_INDEPENDENT
PASS_R2C_NO_PARTIAL_PROGRAM_PASS
PASS_R2C_COVERAGE_26_54
PASS_R2C_LEGACY_ORACLE_79_1
PASS_R2C_15C_105_102_3
PASS_R2C_R2B_DISPOSITION_AXIS_PRESERVED
PASS_R2C_R2B1_FIND_RANGE_PARITY_PRESERVED
PASS_R2C_NO_PYTHON_RUNTIME
PASS_R2C_NO_DYNAMIC_FALLBACK
PASS_R2C_NO_104_GATE_MIGRATION
PASS_R2C_NO_CARGO_AUTHORITY_MIGRATION
PASS_R2C_NO_CF1_V2_MUTATION
PASS_R2C_NO_PRODUCTION_AUTHORITY
```

Physical gates pending local Rust execution:

```text
PASS_R2C_CARGO_CHECK
PASS_R2C_CARGO_TEST
PASS_R2C_CAPABILITY_RECEIPT_PHYSICAL_52_50_49_46
PASS_R2C_DIAGNOSTIC_25_PASS_1_FAIL
PASS_R2C_FIRST_SEMANTIC_FAILURE_56
PASS_R2C_FIRST_MATERIALIZATION_HOLD_0
```

## 20. Promotion blockers

R2C must HOLD if any local run shows:

```text
existing projected program changes semantic result
ordinal 22 regresses to FAIL
firstSemanticFailureOrdinal != 56
legacy oracle != 79/1
15C-R1 != 105/102/3
parent blocker counts != 52/49
R2C blocker counts != 50/46
unclassified semantic-relevant statement > 0
blocker-free Frozen validator is promoted without full clause coverage proof
expected legacy disposition affects classification
validator-specific or line-number scaffold skip exists
Python execution enters Rust semantic route
```

## 21. Next tranche

R2C leaves three validators capability-blocker-free but intentionally unpromoted. The next patch should add **semantic clause coverage certification** before any of those three can cross:

```text
FrozenSourceBound -> SemanticProjected
```

Recommended next patch direction:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-CLAUSE-COVERAGE-CERTIFICATE-AND-ATOMIC-MATERIALIZATION-01B-R1A-R2C1
```

Its first duty is to prove, per candidate:

```text
LegacySemanticClauseCount
CompiledSemanticCheckCount
UnmappedLegacySemanticClauseCount = 0
ProgramIdentityValid = true
```

Only after that proof may capability-blocker-free validators be batch promoted.
