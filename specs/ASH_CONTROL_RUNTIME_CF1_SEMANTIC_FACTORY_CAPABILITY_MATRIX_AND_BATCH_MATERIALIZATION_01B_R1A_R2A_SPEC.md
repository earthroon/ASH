# ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-CAPABILITY-MATRIX-AND-BATCH-MATERIALIZATION-01B-R1A-R2A

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-CAPABILITY-MATRIX-AND-BATCH-MATERIALIZATION-01B-R1A-R2A
Parent: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-COVERAGE-CLOSURE-01B-R1A-R2
Role: Factory capability-debt SSOT and capability-driven batch materialization
Production authority: false
Core registry mutation: forbidden
104 structural-gate migration: false
Cargo compile authority migration: false
CF1 V2 producer migration: false
Training math / optimizer / checkpoint change: none
```

## Authority declaration

```text
CONTROL-02 Authority Architecture Preservation /
Core Registry SSOT Preservation /
Factory Capability Matrix /
Materialization Requirement Evidence /
Capability Dependency DAG /
No Per-Validator Device Policy /
No Per-Validator Manager Policy /
No Orchestrator Capability Policy /
No Factory Membership Authority /
Frozen Validator Capability Classification /
Unclassified Frozen Zero /
Capability-Driven Batch Materialization /
No Partial-Program PASS /
No Frozen PASS Replay /
No Expected-Disposition Evaluation /
No Target-Source Hash Outcome Authority /
Pure-Rust Legacy Source Parse Admission /
No Python Runtime /
No Python Fallback /
No importlib Execution /
No eval /
No exec /
Immutable Semantic Program /
Program Digest Binding /
Legacy Source Provenance Binding /
Legacy Oracle 79 PASS / 1 FAIL Preserved /
Ordinal 56 First Failure Preserved /
15C-R1 105 / 102 / 3 Preserved /
No 15C Repair /
No Mutation-Parity Promotion /
No 104 Gate Migration /
No Cargo Authority Migration /
No CF1 V2 Mutation /
No Production Authority Claim
```

## 1. Parent truth

```text
DeclaredValidatorCount = 81
ActiveValidatorCount = 80
DeclaredInactiveValidatorCount = 1
SemanticProjectedCount = 25
FrozenSourceBoundActiveCount = 55
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

CONTROL-02 ownership remains:

```text
Core         = identity / membership / legal state
Orchestrator = cross-validator workflow and fail-fast
Manager      = session lifecycle and aggregation
Factory      = projection and immutable program materialization
Device       = generic primitive execution
```

Legacy baseline:

```text
DiagnosticFullMatrix = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
15C-R1 = 105 checks / 102 PASS / 3 scheduler-hash FAIL
```

## 2. Capability matrix boundary

The matrix is Factory evidence, not a second membership SSOT.

```text
Core Validator Contract
  -> Legacy source revision binding
  -> Factory requirement analysis
  -> direct capability requirements
  -> dependency closure
  -> missing capability set
  -> materialize or HOLD
```

Core alone owns validator existence, active/inactive state, class, ordinal, and parent membership.

## 3. Typed capabilities

```text
PythonSyntaxParse
TextBasic
TextTransform
TextSearchOrdering
HelperInline
StaticCollection
StaticIteration
StaticComprehension
SymbolicCondition
SectionAnchor
SectionBalancedBrace
RegexSearch
RegexCapture
JsonStructured
DigestSha256
DigestCanonicalRecipe
SetSequenceRelation
RepositoryQuery
RegistryStaticProjection
PythonSyntaxValidation
```

Capability names describe reusable semantic meaning only. Validator-specific capabilities are forbidden.

## 4. Capability status and dependencies

Statuses:

```text
Implemented
Partial
Unsupported
```

`Partial` never satisfies final materialization admission.

Current staged registry:

```text
ImplementedCapabilityCount = 9
PartialCapabilityCount = 11
UnsupportedCapabilityCount = 0
```

Implemented families:

```text
PythonSyntaxParse
TextBasic
TextTransform
TextSearchOrdering
HelperInline
StaticCollection
StaticIteration
SectionAnchor
DigestSha256
```

Dependency examples:

```text
TextTransform -> TextBasic
TextSearchOrdering -> TextBasic
StaticIteration -> StaticCollection
StaticComprehension -> StaticIteration
SymbolicCondition -> TextBasic
SectionBalancedBrace -> SectionAnchor -> TextBasic
RegexCapture -> RegexSearch -> TextBasic
DigestCanonicalRecipe -> DigestSha256
SetSequenceRelation -> StaticCollection
RegistryStaticProjection -> PythonSyntaxParse + StaticCollection
PythonSyntaxValidation -> PythonSyntaxParse
```

Mandatory:

```text
CapabilityDependencyCycleCount = 0
```

## 5. Matrix entry and provenance

Each remaining Frozen active validator records:

```text
validatorId
legacyPath
legacySourceSha256
materializationState
directRequirements
transitiveRequirements
missingCapabilities
requirementDigest
```

Legacy source SHA256 binds the analysis to the exact translated validator revision. Target Rust/WGSL/JSON content remains execution input rather than remembered-result authority.

## 6. Frozen classification truth

After the staged batch:

```text
FrozenSourceBoundActiveCount = 54
FrozenMatrixEntryCount = 54
UnclassifiedFrozenCount = 0
```

Current conservative blocker counts:

```text
SymbolicCondition          = 52
StaticComprehension        = 49
RepositoryQuery            = 22
RegexSearch                = 18
JsonStructured             = 15
SetSequenceRelation        = 13
RegistryStaticProjection   = 12
RegexCapture                = 9
SectionBalancedBrace        = 7
PythonSyntaxValidation      = 5
DigestCanonicalRecipe       = 1
```

Counts overlap. The analyzer is deliberately conservative: uncertain semantic constructs remain debt rather than silently granting executable status.

## 7. Materialization admission

A Frozen validator may transition to `SemanticProjected` only when:

```text
all semantic clauses mapped
all required capabilities closed
no unsupported clause
program non-empty
check IDs unique
legacy source binding current
program identity valid
```

Forbidden half-states:

```text
SemanticProjected + Program(None)
FrozenSourceBound + Program(Some)
```

Expected legacy PASS/FAIL is never an evaluation or requirement-analysis input.

## 8. R2A stage-1 batch materialization

One additional validator is fully materialized:

```text
validatorId = cf1.production.vram-hot-weight-page-residency-r1-static
legacyPath = tools/validate_vram_hot_weight_page_residency_r1_static.py
legacyCheckCount = 70
RustCheckCount = 70
checkIdOrderParity = exact
```

Checked-in program:

```text
crates/ash_control_runtime/src/cf1/programs/generated_r2a.rs
SHA256 = af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

The program uses generic generated-expression primitives for contains/absence, lowercase membership, count comparisons, index ordering, and conditional promotion-marker selection. No validator-specific Device branch is introduced.

## 9. Current materialization state

```text
PreviousSemanticProjectedCount = 25
NewlyProjectedCount = 1
FinalSemanticProjectedCount = 26
FinalFrozenSourceBoundActiveCount = 54
DeclaredInactiveCount = 1
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

Core active cardinality remains 80.

## 10. Core Registry preservation

```text
crates/ash_core/src/cf1_control_authority.rs
SHA256 = 14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6
```

The file is byte-identical to the parent. No membership, ordinal, class, active/inactive, or parent relation changes.

## 11. Architecture receipt truthfulness

CONTROL-02 closed at a 20-executable baseline. Later admitted Factory expansion must not leave `coverageInflationCount` permanently hardcoded to zero.

R2A makes the field observational:

```text
coverageInflationCount = executableSemanticCount - 20
```

Current staged value:

```text
26 - 20 = 6
```

This is admitted post-CONTROL-02 coverage growth, not authority leakage.

## 12. Capability matrix route

```text
ash_control_runtime cf1-factory-capability-matrix
    --repo-root <path>
    [--receipt <path>]
```

Default receipt:

```text
artifacts/control_runtime/cf1_factory_capability_matrix/factory_capability_matrix_receipt.json
```

Schema:

```text
ash.control_runtime.cf1.factory_capability_matrix.v1
```

The command performs read-only source analysis plus optional receipt publication. It does not generate source programs during semantic execution.

## 13. Receipt fields

```text
coreRegistryDigest
executableRegistryDigest
capabilityRegistryDigest
capabilityMatrixDigest
activeValidatorCount
previousProjectedCount
previousFrozenCount
newlyProjectedCount
finalProjectedCount
finalFrozenCount
frozenMatrixEntryCount
unclassifiedFrozenCount
implementedCapabilityCount
partialCapabilityCount
unsupportedCapabilityCount
capabilityDependencyCycleCount
blockerCounts
matrixEntries
semanticProjectionClosed
productionAuthorityClaimed
receiptHash
```

## 14. Pure-Rust analysis boundary

Every Frozen validator is admitted through the existing `rustpython-parser` Device boundary before requirement classification.

Forbidden fallback:

```text
Rust analyzer unsupported -> execute Python to infer requirements
```

Python execution is permitted only in the separate migration reference-oracle harness, never as semantic candidate runtime authority.

## 15. Legacy regression truth

All 80 active legacy validators were rerun after R2A stage 1:

```text
ordinals 0..55 = 56 PASS
ordinal 56 = FAIL
ordinals 57..79 = 23 PASS
TOTAL = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

The only failure remains 15C-R1:

```text
105 checks
102 PASS
3 FAIL
```

The three failed clauses remain the scheduler-hash consumers for validators 16, 17, and 18. R2A does not repair them.

## 16. PowerShell producer preservation

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
SHA256 = 05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## 17. Cross-layer boundaries

```text
Core membership authority = Core
Capability analysis = Factory/materialization layer
Workflow = Orchestrator
Session aggregation = Manager
Primitive execution = Device
```

Forbidden:

```text
Device branches on validator ID/ordinal
Manager translates legacy AST
Orchestrator examines Regex/JSON/Digest capability debt
Factory creates membership absent from Core
```

## 18. Static qualification

Changed Rust surface:

```text
cf1/capability_matrix.rs
cf1/programs/generated_r2a.rs
cf1/programs/mod.rs
cf1/compiler.rs
cf1/registry.rs
cf1/executable_registry.rs
cf1/coverage.rs
cf1/architecture.rs
cf1/mod.rs
main.rs
```

Static delimiter audit:

```text
10 changed Rust files checked
0 delimiter failures
```

The environment does not expose usable `cargo`, `rustc`, or `rustfmt`; physical Rust compile/fmt/test PASS is therefore not claimed. This does not authorize a Python or PowerShell production fallback.

## 19. Final R2A target

R2A remains open until:

```text
SemanticProjectedCount = 80
FrozenSourceBoundActiveCount = 0
UnclassifiedFrozenCount = 0
UnsupportedProjectionCount = 0
ProjectionIncompleteCount = 0
SemanticProjectionClosed = true
```

Only then may mutation parity begin.

## 20. Mandatory staged gates

```text
PASS_R2A_CORE_REGISTRY_UNCHANGED
PASS_R2A_CAPABILITY_MATRIX_ALL_FROZEN
PASS_R2A_UNCLASSIFIED_FROZEN_ZERO
PASS_R2A_CAPABILITY_DEPENDENCY_DAG_ACYCLIC
PASS_R2A_REQUIREMENT_ANALYSIS_EXPECTED_DISPOSITION_INDEPENDENT
PASS_R2A_NO_PYTHON_RUNTIME
PASS_R2A_NO_DYNAMIC_PYTHON_FALLBACK
PASS_R2A_PROGRAM_ADMISSION_ATOMIC
PASS_R2A_EXISTING_25_PRESERVED
PASS_R2A_VRAM_70_CHECK_PROGRAM
PASS_R2A_VRAM_CHECK_ID_PARITY
PASS_R2A_LEGACY_ORACLE_79_1
PASS_R2A_15C_105_102_3
PASS_R2A_CROSS_LAYER_AUTHORITY_PRESERVED
PASS_R2A_CF1_V2_UNCHANGED
PASS_R2A_NO_104_GATE_MIGRATION
PASS_R2A_NO_CARGO_AUTHORITY_MIGRATION
PASS_R2A_NO_PRODUCTION_AUTHORITY
```

Pending final-closure gates:

```text
PASS_R2A_SEMANTIC_PROJECTED_80
PASS_R2A_FROZEN_ZERO
PASS_R2A_RUST_FULL_MATRIX_79_1
PASS_R2A_RUST_FAIL_FAST_56_1_23
```

## 21. Current staged truth

```text
PatchId=ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-CAPABILITY-MATRIX-AND-BATCH-MATERIALIZATION-01B-R1A-R2A
CoreRegistryChanged=False
CoreRegistrySourceSha256=14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6
PreviousProjectedCount=25
PreviousFrozenCount=55
NewlyProjectedCount=1
FinalProjectedCount=26
FinalFrozenCount=54
FrozenMatrixEntryCount=54
UnclassifiedFrozenCount=0
ImplementedCapabilityCount=9
PartialCapabilityCount=11
UnsupportedCapabilityCount=0
CapabilityDependencyCycleCount=0
GeneratedR2AProgramCount=1
GeneratedR2ACheckCount=70
GeneratedR2AProgramSourceSha256=af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
LegacyDiagnosticPassCount=79
LegacyDiagnosticFailCount=1
LegacyFirstFailureOrdinal=56
Known15CR1LegacyCheckCount=105
Known15CR1LegacyPassCount=102
Known15CR1LegacyFailCount=3
PowerShellProducerSha256=05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
SemanticProjectionClosed=False
ProductionAuthorityClaimed=False
PhysicalRustCompileQualificationAvailable=False
```

## 22. Next priority

The matrix converts vague migration debt into explicit Factory debt. The largest conservative blockers are `SymbolicCondition` and `StaticComprehension`; the next tranche should first separate genuine semantic use from legacy result-reporting scaffold. After that, the largest substantive families are `RepositoryQuery`, `RegexSearch`, `JsonStructured`, `SetSequenceRelation`, and `RegistryStaticProjection`.

R2A remains the active patch until 80 executable / 0 Frozen is reached.
