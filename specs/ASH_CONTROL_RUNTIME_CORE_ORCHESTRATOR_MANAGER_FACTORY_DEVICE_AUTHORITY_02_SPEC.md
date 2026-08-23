# ASH-CONTROL-RUNTIME-CORE-ORCHESTRATOR-MANAGER-FACTORY-DEVICE-AUTHORITY-02

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CORE-ORCHESTRATOR-MANAGER-FACTORY-DEVICE-AUTHORITY-02
Parent: ASH-CONTROL-RUNTIME-CF1-RESTRICTED-AST-LOWERING-COVERAGE-CLOSURE-01B-R1A-R1
Role: control-plane authority ownership rebase
Production authority: false
Semantic coverage expansion: forbidden in this revision
CF1 V2 producer migration: false
104 structural-gate authority migration: false
Cargo compile authority migration: false
Training math / optimizer / checkpoint change: none
```

## Authority declaration

```text
Canonical Core Registry SSOT /
Authority State SSOT /

Orchestrator Workflow Ownership /
Manager Lifecycle Ownership /
Factory Materialization Ownership /
Device Primitive Execution Ownership /

No Cross-Layer Authority Leakage /

CF1 Registry Core Promotion /
Executable Registry Projection /

Semantic Program Factory /
Semantic Validation Manager /
Semantic Device Boundary /
Legacy Projection Factory /
Python AST Device /
Parse Only / No Python Execution /

Immutable Program Identity /
Program Digest Binding /

No Device Policy /
No Factory Membership Authority /
No Manager Contract Authority /
No Orchestrator Primitive Execution /
No Core Physical IO /

Existing 20 Semantic Programs Rebased /
Existing 60 Frozen States Preserved /
Zero Coverage Inflation /
No Frozen PASS Replay /

15C-R1 Handwritten Executor Retirement /
15C-R1 Generic 105-Check Program /
Existing 15C-R1 102 PASS / 3 FAIL Preserved /

Existing Legacy Oracle 79 PASS / 1 FAIL Preserved /

No CF1 V2 Mutation /
No 104-Gate Migration /
No Cargo Authority Migration /
No Production Authority Change
```

## 1. Parent truth

The parent bake is the authority baseline for this revision:

```text
DeclaredValidatorCount = 81
ActiveValidatorCount = 80
DeclaredInactiveValidatorCount = 1
SemanticProjectedCount = 20
FrozenSourceBoundActiveCount = 60
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

Legacy diagnostic truth remains:

```text
79 PASS / 1 FAIL
FirstFailureOrdinal = 56
15C-R1 = 105 checks / 102 PASS / 3 scheduler-hash FAIL
```

CONTROL-02 does not improve semantic coverage. Its job is to put the same 20/60 state under explicit ownership boundaries before the remaining semantic translation continues.

## 2. Authority flow and dependency rule

Conceptual execution authority flows:

```text
CORE SSOT
    ↓
ORCHESTRATOR
    ↓
MANAGER
    ↓
FACTORY
    ↓
DEVICE
    ↓
PHYSICAL EVIDENCE
```

This is not a Rust source-dependency arrow. `ash_core` remains the lowest shared contract dependency and must not depend on `ash_control_runtime`.

The source/authority graph must remain acyclic.

## 3. Core Registry SSOT

Canonical CF1 membership is promoted into:

```text
crates/ash_core/src/cf1_control_authority.rs
```

Core owns:

```text
Cf1ValidatorId
Cf1ValidatorClass
Cf1ExecutionOrdinal
Cf1CanonicalValidatorContract
Cf1MaterializationState
Cf1ValidationDisposition
Cf1SemanticProgramIdentity
```

Core registry cardinality is exact:

```text
Declared = 81
Active = 80
Inactive = 1
Production = 75
HistoricalPreservation = 1
OperationalRecovery = 1
RuntimeQualification = 3
ParentSubset = 6
ActiveOrdinals = 0..79 contiguous
```

No control-runtime file may become a second membership SSOT.

## 4. Core physical-IO prohibition

Core defines identities, legal states, and transitions. It does not perform:

```text
filesystem reads
process spawning
regex execution
Python parsing execution
Cargo execution
GPU execution
receipt publication IO
```

## 5. Authority State SSOT

Materialization state is Core-owned:

```text
DeclaredInactive
FrozenSourceBound
SemanticProjected
TranslationStale
ProjectionIncomplete
Unsupported
```

Materialization state and validation result are separate truths. Valid examples include:

```text
SemanticProjected + Passed
SemanticProjected + Failed
FrozenSourceBound + NotExecutable
TranslationStale + NotExecutable
```

A Frozen validator cannot become Passed merely from remembered legacy disposition.

## 6. Legacy projection metadata

Legacy Python provenance remains a projection surface, not membership authority. It may contain:

```text
validator ID
legacy path
legacy source SHA256
expected legacy disposition
materialization state
translation revision
input/provenance binding
```

It may not author:

```text
active/inactive
ordinal
class
parent membership
```

Those values are joined from the Core canonical registry.

Orphan legacy IDs are rejected.

## 7. Executable Registry Projection

`Cf1ExecutableRegistry` is a derived control-runtime projection of Core membership and current materialization.

Mandatory current state:

```text
ExecutableSemanticCount = 20
FrozenSemanticCount = 60
DeclaredInactiveCount = 1
```

Mandatory relation:

```text
ExecutableRegistry IDs == Core canonical IDs
Executable semantic set ⊆ Core active set
```

The architecture receipt fails closed if executable coverage drifts from 20/60 in this revision.

## 8. Zero coverage inflation

CONTROL-02 is architecture-only:

```text
SemanticProjectedBefore = 20
SemanticProjectedAfter = 20
FrozenBefore = 60
FrozenAfter = 60
CoverageInflationCount = 0
```

No Frozen validator may be promoted during this patch.

## 9. Orchestrator ownership

`Cf1Orchestrator` owns cross-validator workflow:

```text
active ordering
LegacyFailFast
DiagnosticFullMatrix
first-terminal attribution
workflow progression
whole semantic-shadow receipt assembly
```

The Orchestrator does not directly read files, execute regex/hash/parser primitives, or spawn processes.

Cross-validator fail-fast is Orchestrator policy, not Device policy.

## 10. Manager ownership

`SemanticValidationManager` owns one validation session:

```text
materialization-state handling
program acquisition
device execution coordination
check aggregation
validator semantic disposition
legacy parity comparison after semantic evaluation
session-local evidence
```

Manager consumes immutable Core contracts. It does not mutate membership, ordinal, class, or parent identity and does not directly implement filesystem/parser/hash primitives.

Frozen active validators fail closed as incomplete/not executable. Expected legacy PASS is never replayed.

## 11. Factory ownership

Factories own deterministic materialization:

```text
LegacyProjectionFactory
SemanticProgramFactory
```

Conceptual flow:

```text
Legacy source
    ↓
PythonAstDevice
    ↓
LegacyProjectionFactory
    ↓
Typed projection
    ↓
SemanticProgramFactory
    ↓
Immutable semantic program
```

Factory does not decide membership, active state, ordinal, class, workflow order, or validator PASS/FAIL.

## 12. Python AST Device

`PythonAstDevice` is parse-only:

```text
Python source -> syntax tree
```

It does not execute imports, module top-level code, functions, `eval`, `exec`, Python subprocesses, or a CPython VM.

AST semantic interpretation/lowering belongs to Factory, not Device.

## 13. Semantic Device

`SemanticDevice` / `NativeSemanticDevice` owns low-level physical semantic primitives such as:

```text
read_text
file_sha256
path existence
text predicates
section predicates
digest fanout
token ordering
JSON predicates
generated expression execution
program primitive execution
```

Device must not know or branch on:

```text
validator ordinal 56
Production class
LegacyFailFast
79/1 baseline
expected_legacy_disposition
semantic coverage counts
production authority
```

Device returns primitive evidence/results. Manager aggregates validator outcome. Orchestrator decides cross-validator progression.

## 14. Program identity and immutability

Factory output is immutable after materialization.

Program identity binds semantic policy/projection identity, including validator/program/projection digests. Target repository bytes are evaluation input, not remembered-result authority.

Manager and Device consume the program without mutating it.

## 15. Generic 15C-R1 rebase

CONTROL-02 retires the ordinal-56 handwritten semantic executor.

Ordinal 56 is materialized by Factory as an ordinary generic semantic program with exactly:

```text
105 checks
```

using generic primitives including:

```text
PathExists
TextContains / Not
SectionContains / SectionAbsent
DigestAppearsInText
TokenOrder
```

After the rebase:

```text
HandwrittenSemanticExecutionCount = 0
```

There is no `evaluate_15c_r1` runtime authority and no validator-ID-specific physical evaluator branch.

## 16. 15C baseline preservation

Architecture movement must preserve the retained legacy oracle:

```text
15C-R1 Total = 105
PASS = 102
FAIL = 3
```

The same three scheduler-hash failures for validators 16, 17, and 18 remain. CONTROL-02 does not repair them.

## 17. Existing semantic program preservation

The parent semantic coverage contained 19 non-15C declarative/generated definitions plus the ordinal-56 pilot.

CONTROL-02 preserves the existing generated source definitions and moves primitive execution ownership behind Device. It does not regenerate semantic coverage.

Current executable topology becomes:

```text
5 existing declarative programs
14 R1A-R1 generated programs
1 generic Factory-materialized 15C program
-------------------------------------------
20 executable semantic validators
```

## 18. Single execution authority

Primitive declarative-program evaluation exists behind Device only.

Manager, Factory, Orchestrator, and Core must not retain second physical semantic evaluators. Historical frozen-shadow evidence may remain for audit but is not a second semantic execution candidate.

## 19. Semantic route topology

```text
Core Validator Contract
        ↓
Executable Registry Projection
        ↓
Cf1Orchestrator
        ↓
SemanticValidationManager
        ↓
SemanticProgramFactory
        ↓
SemanticDevice
        ↓
check results
        ↓
Manager aggregation
        ↓
validator disposition
        ↓
Orchestrator progression
```

## 20. Architecture receipt

CONTROL-02 adds a non-production architecture receipt:

```text
schema = ash.control_runtime.authority_architecture.v1
```

It records at least:

```text
canonical / active / inactive counts
executable / frozen counts
Core registry digest
Executable registry digest
Orchestrator/Manager/Factory/Device presence
PythonAstDevice presence
handwritten semantic execution count
coverage inflation count
cross-layer authority leak count
dependency cycle count
productionAuthorityClaimed
receipt self hash
```

Current expected receipt truth:

```text
CanonicalValidatorCount = 81
ActiveValidatorCount = 80
InactiveValidatorCount = 1
ExecutableSemanticCount = 20
FrozenSemanticCount = 60
HandwrittenSemanticExecutionCount = 0
CoverageInflationCount = 0
CrossLayerAuthorityLeakCount = 0
DependencyCycleCount = 0
ProductionAuthorityClaimed = false
```

## 21. Architecture CLI

CONTROL-02 adds:

```text
ash_control_runtime control02-architecture
    --repo-root <path>
    [--receipt <path>]
```

The route builds the architecture receipt and uses the existing atomic publication primitive. Runtime-generated receipts remain excluded from baked source archives.

## 22. Existing semantic route

`cf1-semantic-shadow` now routes through Orchestrator and Manager.

Because only 20 of 80 active validators have executable semantic programs:

```text
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

CONTROL-02 success must not be confused with full semantic coverage closure.

## 23. Legacy oracle regression

After the architecture rebase all 80 retained legacy validators are rerun. Observed diagnostic matrix:

```text
ordinals 00..19 = 20 PASS / 0 FAIL
ordinals 20..39 = 20 PASS / 0 FAIL
ordinals 40..59 = 19 PASS / 1 FAIL
ordinals 60..79 = 20 PASS / 0 FAIL

TOTAL = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

No new legacy validator failure is introduced by the authority-layer files.

## 24. PowerShell producer preservation

The physical legacy CF1 producer remains byte-identical:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
SHA256 = 05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## 25. Production boundaries preserved

CONTROL-02 does not migrate:

```text
R6AR2R2CF1CompileReceipt V2 producer authority
104 structural-gate physical authority
cargo fmt/check/test/build authority
PowerShell SourceTreeDigest authority
production binary admission
```

It does not change training math, optimizer behavior, checkpoint mutation, GPU kernels, or runtime training scheduler semantics.

## 26. `orchestrator_local` boundary

The new `Cf1Orchestrator` is internal to `ash_control_runtime`. It does not promote the existing `orchestrator_local` crate into control authority. `orchestrator_local` remains an external workflow/audit consumer.

## 27. Static architecture invariants

Required:

```text
Core validator IDs = 81 unique
Legacy projection IDs = 81 unique
Core ID set == legacy projection ID set
Core active = 80
Core inactive = 1
Core parent subset = 6
Materialization = 20 projected / 60 frozen / 1 inactive
```

Generated semantic source from the parent remains byte-identical where CONTROL-02 only changes ownership.

The physical PowerShell producer remains byte-identical.

## 28. Cross-layer prohibitions

Forbidden examples:

```text
Device branches on validator ID/class/fail-fast policy
Factory creates validator membership from file discovery
Manager mutates Core ordinal/class/active state
Orchestrator reads target source or runs regex/hash/parser/Cargo directly
Core performs filesystem/process IO
```

Architecture receipt requires:

```text
CrossLayerAuthorityLeakCount = 0
DependencyCycleCount = 0
```

## 29. Physical Rust qualification

When a usable Rust toolchain is available, qualification must include at least:

```text
cargo fmt --check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo test --manifest-path crates/ash_control_runtime/Cargo.toml
```

and relevant `ash_core` checks.

The bake environment for this revision does not provide usable `cargo`, `rustc`, or `rustfmt`. Physical Rust compile/test PASS is therefore not claimed. This does not authorize a Python or PowerShell compile wrapper fallback.

Changed Rust source must still pass deterministic lexical/delimiter sanity and architecture-specific static audits.

## 30. Bake policy

Exclude from delivered source ZIP:

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

Retain source material including Cargo files, Rust source, checked-in generated Rust programs, source `.args` contracts, source JSON profiles, and retained legacy validators.

The CONTROL-02 spec is committed to GitHub and is not embedded in the baked source ZIP.

## 31. Mandatory gates

```text
PASS_CONTROL02_CORE_REGISTRY_SSOT
PASS_CONTROL02_AUTHORITY_STATE_SSOT

PASS_CONTROL02_ORCHESTRATOR_WORKFLOW_OWNERSHIP
PASS_CONTROL02_MANAGER_LIFECYCLE_OWNERSHIP
PASS_CONTROL02_FACTORY_MATERIALIZATION_OWNERSHIP
PASS_CONTROL02_DEVICE_EXECUTION_OWNERSHIP

PASS_CONTROL02_NO_DEVICE_POLICY
PASS_CONTROL02_NO_FACTORY_MEMBERSHIP_AUTHORITY
PASS_CONTROL02_NO_MANAGER_CONTRACT_AUTHORITY
PASS_CONTROL02_NO_ORCHESTRATOR_PRIMITIVE_EXECUTION
PASS_CONTROL02_NO_CORE_PHYSICAL_IO

PASS_CONTROL02_EXECUTABLE_REGISTRY_IS_CORE_PROJECTION
PASS_CONTROL02_EXISTING_20_PROGRAM_REBASE
PASS_CONTROL02_EXISTING_60_FROZEN_PRESERVED
PASS_CONTROL02_ZERO_COVERAGE_INFLATION
PASS_CONTROL02_NO_FROZEN_PASS_REPLAY

PASS_CONTROL02_15C_HANDWRITTEN_EXECUTOR_RETIREMENT
PASS_CONTROL02_15C_GENERIC_PROGRAM_105
PASS_CONTROL02_15C_R1_LEGACY_105_102_3_PRESERVED
PASS_CONTROL02_LEGACY_ORACLE_79_1_PRESERVED

PASS_CONTROL02_PROGRAM_IDENTITY_IMMUTABLE
PASS_CONTROL02_PRIMITIVE_EVALUATOR_DEVICE_ONLY
PASS_CONTROL02_DEPENDENCY_DAG_ACYCLIC
PASS_CONTROL02_CROSS_LAYER_AUTHORITY_LEAK_ZERO

PASS_CONTROL02_CF1_V2_UNCHANGED
PASS_CONTROL02_POWERSHELL_AUTHORITY_UNCHANGED
PASS_CONTROL02_NO_104_GATE_AUTHORITY_MIGRATION
PASS_CONTROL02_NO_CARGO_COMPILE_AUTHORITY_MIGRATION

PASS_CONTROL02_NO_TRAINING_MATH_CHANGE
PASS_CONTROL02_NO_OPTIMIZER_CHANGE
PASS_CONTROL02_NO_CHECKPOINT_CHANGE
PASS_CONTROL02_NO_PRODUCTION_AUTHORITY_CHANGE
```

## 32. Current bake truth

```text
PatchId=ASH-CONTROL-RUNTIME-CORE-ORCHESTRATOR-MANAGER-FACTORY-DEVICE-AUTHORITY-02
CanonicalRegistryAuthority=ash_core
AuthorityStateSSOT=ash_core

DeclaredValidatorCount=81
ActiveValidatorCount=80
DeclaredInactiveValidatorCount=1
ProductionValidatorCount=75
HistoricalPreservationValidatorCount=1
OperationalRecoveryValidatorCount=1
RuntimeQualificationValidatorCount=3
ParentValidatorSubsetCount=6

ExecutableSemanticCount=20
FrozenSemanticCount=60
CoverageInflationCount=0

OrchestratorWorkflowOwner=True
ManagerLifecycleOwner=True
FactoryMaterializationOwner=True
DeviceExecutionOwner=True
PythonAstDeviceParseOnly=True
PythonRuntimeRequired=False

HandwrittenSemanticExecutionCount=0
Generic15CR1ProgramCheckCount=105

LegacyDiagnosticPassCount=79
LegacyDiagnosticFailCount=1
LegacyFirstFailureOrdinal=56
Known15CR1LegacyCheckCount=105
Known15CR1LegacyPassCount=102
Known15CR1LegacyFailCount=3

CrossLayerAuthorityLeakCount=0
DependencyCycleCount=0
PowerShellProducerSha256=05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486

CF1CompileReceiptV2Mutation=False
StructuralGate104Migration=False
CargoCompileAuthorityMigration=False
TrainingMathChanged=False
OptimizerChanged=False
CheckpointChanged=False
ProductionAuthorityChanged=False
ProductionAuthorityClaimed=False
PhysicalRustCompileQualificationAvailable=False
```

## 33. Completion truth and next revision

CONTROL-02 is closed when the pre-patch CF1 semantic state is reproduced with explicit non-overlapping ownership:

```text
Core owns canonical identity/membership/state contracts
Orchestrator owns workflow
Manager owns session lifecycle and aggregation
Factory owns immutable materialization
Device owns physical primitive execution
```

while preserving exactly:

```text
20 executable semantic validators
60 frozen active validators
1 declared-inactive validator
79/1 legacy diagnostic baseline
```

The next semantic-coverage patch should extend materialization through this architecture rather than growing another monolithic validator engine:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-COVERAGE-CLOSURE-01B-R1A-R2
```

Its target is `20 SemanticProjected / 60 Frozen -> 80 SemanticProjected / 0 Frozen` without changing Core membership authority.