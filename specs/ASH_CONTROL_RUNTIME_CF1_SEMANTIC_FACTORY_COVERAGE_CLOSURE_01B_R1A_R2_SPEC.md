# ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-COVERAGE-CLOSURE-01B-R1A-R2

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-FACTORY-COVERAGE-CLOSURE-01B-R1A-R2
Parent: ASH-CONTROL-RUNTIME-CORE-ORCHESTRATOR-MANAGER-FACTORY-DEVICE-AUTHORITY-02
Role: expand Factory materialization coverage without changing Core membership authority
Production authority: false
Core registry mutation: forbidden
104 structural-gate migration: false
Cargo compile authority migration: false
CF1 V2 producer migration: false
Training math / optimizer / checkpoint change: none
```

## Authority declaration

```text
Core Registry SSOT Preservation /
CONTROL-02 Authority Architecture Preservation /
SemanticProgramFactory Coverage Expansion /
LegacyProjectionFactory Coverage Expansion /
No Core Membership Mutation /
No Orchestrator Materialization Policy /
No Manager Contract Mutation /
No Device Validator Policy /
Typed Semantic IR /
Deterministic Checked-In Program Materialization /
Legacy Check-ID Preservation /
Legacy Source Provenance Binding /
Immutable Program Identity /
Program Digest Binding /
No Frozen PASS Replay /
No Expected-Disposition Evaluation /
No Target-Source Hash Outcome Authority /
No Python Runtime /
No PowerShell Runtime /
No Cargo Runtime In Semantic Route /
No Dynamic Python Fallback /
Current Legacy Oracle 79 PASS / 1 FAIL Preserved /
Ordinal 56 First Failure Preserved /
15C-R1 105 / 102 / 3 Preserved /
No 15C Hash Repair /
No Mutation-Parity Promotion Yet /
No 104 Structural Gate Migration /
No Cargo Compile Authority Migration /
No CF1 V2 Mutation /
No Production Authority Claim
```

## Parent truth

CONTROL-02 owns the authority topology:

```text
Core         = canonical identity, membership, legal materialization states
Orchestrator = cross-validator workflow and fail-fast
Manager      = validation-session lifecycle and aggregation
Factory      = projection and immutable program materialization
Device       = primitive physical semantic execution
```

Parent materialization:

```text
Declared = 81
Active = 80
Inactive = 1
SemanticProjected = 20
Frozen = 60
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

Legacy reference oracle:

```text
79 PASS / 1 FAIL
FirstFailureOrdinal = 56
15C-R1 = 105 checks / 102 PASS / 3 scheduler-hash FAIL
```

## Normative final objective

R1A-R2 is fully closed only when:

```text
SemanticProjectedCount = 80
FrozenSourceBoundActiveCount = 0
ProjectionIncompleteCount = 0
UnsupportedProjectionCount = 0
TranslationStaleCount = 0
ExecutableSemanticProgramCount = 80
EmptyProgramCount = 0
SemanticProjectionClosed = true
```

Core membership must remain unchanged while executable coverage grows.

## Current staged bake truth

This implementation tranche does not claim final 80-node closure.

```text
PreviousSemanticProjectedCount = 20
NewlyMaterializedCount = 5
SemanticProjectedCount = 25
FrozenSourceBoundActiveCount = 55
DeclaredInactiveValidatorCount = 1
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

Five newly materialized programs:

```text
cf1.production.r27r1j-r6a-r2-r2-final-norm-tape-burn-owner-pin-r14-fault-attribution-static = 52 checks
cf1.production.tensorcube-local-muon-first-candidate-registry-static = 97 checks
cf1.production.ram36-process-budget-authority-r1-static = 63 checks
cf1.production.qk-rmsnorm-attention-stability-static = 101 checks
cf1.production.ram-adam-mv-pcie-transfer-overlap-static = 76 checks
```

New typed semantic check total:

```text
389
```

Each new program has unique check IDs inside its own validator.

## Core Registry preservation

Canonical Core source is byte-identical to the CONTROL-02 parent:

```text
crates/ash_core/src/cf1_control_authority.rs
SHA256 = 14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6
```

This revision does not mutate validator IDs, active/inactive membership, execution ordinals, validator classes, or parent membership.

## Factory and Device ownership

Coverage grows only through:

```text
Core Contract
  -> LegacyProjectionFactory
  -> Typed Semantic IR
  -> SemanticProgramFactory
  -> Immutable Program
  -> Executable Registry
```

Manager does not materialize programs. Orchestrator does not interpret semantic clauses. Device executes only generic primitives and never branches on validator identity or ordinal.

## New generic semantic capability

This tranche uses generic semantic operations including:

```text
PathExists
TextContains
TextContainsCaseInsensitive
TextCountEquals
TextFind
TextIndex
TextRFind
Text Slice
SectionContains
All / Any / Not
Integer ordering comparison
Multi-file absence composition
```

`TextRFind` preserves Python `str.rfind()` ordering semantics and is a generic Device primitive, not validator-specific policy.

## Generated source

Checked-in source:

```text
crates/ash_control_runtime/src/cf1/programs/generated_r1ar2.rs
```

contains exactly:

```text
5 programs
389 checks
```

Deterministic regeneration SHA256:

```text
6f988778f177ad942d60350f1ae214cf14ceb6306925d82f67ba486d5de13c14
```

Regeneration from identical inputs is byte-identical.

## Current-source check parity for new programs

Retained legacy validators independently report:

```text
Final Norm / R14 fault attribution  = 52 / 52 PASS
TensorCube first-candidate registry = 97 / 97 PASS
RAM36 process-budget authority      = 63 / 63 PASS
QK RMSNorm attention stability      = 101 / 101 PASS
RAM Adam M/V PCIe overlap           = 76 / 76 PASS
```

Restricted-AST gaps manually lowered into typed generic predicates were independently checked on current source. No new program uses remembered legacy PASS as its semantic outcome.

## Full legacy oracle regression

All 80 active legacy validators were rerun after this staged Factory expansion.

```text
79 PASS
1 FAIL
FirstFailureOrdinal = 56
```

The only failure remains:

```text
tools/validate_ash_bp_dk_fusion_legacy_restart_barrier_transaction_marker_classification_15c_r1_static.py
```

No new legacy failure is introduced.

## 15C-R1 preservation

Current output remains exactly three scheduler-hash failures:

```text
validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
```

```text
3 / 105 failures
```

R1A-R2 does not repair those hashes.

## PowerShell producer preservation

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
SHA256 = 05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## Coverage receipt

New evidence schema:

```text
ash.control_runtime.cf1.semantic_factory_coverage.v1
```

Current staged fields:

```text
previousProjectedCount = 20
newlyMaterializedCount = 5
finalProjectedCount = 25
frozenActiveCount = 55
declaredInactiveCount = 1
semanticProjectionClosed = false
productionAuthorityClaimed = false
```

The receipt is evidence, not membership SSOT.

## Coverage CLI

```text
ash_control_runtime cf1-semantic-factory-coverage
    --repo-root <path>
    [--receipt <path>]
```

Runtime-generated receipts are excluded from source bakes.

## Architecture preservation

CONTROL-02 ownership remains:

```text
Core membership authority = true
Orchestrator workflow authority = true
Manager lifecycle authority = true
Factory materialization authority = true
Device primitive execution authority = true
```

The generic architecture receipt validates `Executable + Frozen = 80`; staged coverage counts are owned by the dedicated R1A-R2 coverage receipt.

## Incomplete state

Fifty-five active validators remain `FrozenSourceBound` with no executable Rust semantic program.

Therefore:

```text
SemanticProjectionClosed = false
```

and mutation-parity promotion must not begin yet.

Remaining Factory coverage families include regex/capture semantics, advanced section extraction, symbolic conditional/comprehension lowering, structured JSON dataflow, canonical digest framing, set/sequence relations, repository queries, static registry projection, importlib replacement without execution, and pure-Rust Python syntax validation.

## Static qualification

Changed Rust source received deterministic lexical/delimiter checks:

```text
10 changed Rust files checked
0 delimiter failures
```

The current environment does not provide usable `cargo`, `rustc`, or `rustfmt`, so physical Rust compile/test/fmt PASS is not claimed.

## Production boundaries

No migration of:

```text
CF1 V2 compile receipt production authority
104 structural-gate physical authority
Cargo build authority
PowerShell SourceTreeDigest authority
production binary admission
training math
optimizer math
checkpoint semantics
GPU training kernels
```

## Mandatory final gates

```text
PASS_R1A_R2_CORE_REGISTRY_UNCHANGED
PASS_R1A_R2_FACTORY_MATERIALIZATION_OWNER
PASS_R1A_R2_DEVICE_EXECUTION_OWNER
PASS_R1A_R2_MANAGER_LIFECYCLE_OWNER
PASS_R1A_R2_ORCHESTRATOR_WORKFLOW_OWNER
PASS_R1A_R2_EXISTING_20_PRESERVED
PASS_R1A_R2_NEW_60_MATERIALIZED
PASS_R1A_R2_SEMANTIC_PROJECTED_80
PASS_R1A_R2_FROZEN_ZERO
PASS_R1A_R2_INCOMPLETE_ZERO
PASS_R1A_R2_UNSUPPORTED_ZERO
PASS_R1A_R2_STALE_ZERO
PASS_R1A_R2_EXECUTABLE_REGISTRY_EXACT_CORE_ACTIVE_SET
PASS_R1A_R2_PROGRAM_80
PASS_R1A_R2_PROGRAM_GENERATION_DETERMINISTIC
PASS_R1A_R2_EXPECTED_DISPOSITION_NOT_EVALUATION_INPUT
PASS_R1A_R2_FULL_MATRIX_79_1
PASS_R1A_R2_FIRST_FAILURE_56
PASS_R1A_R2_FAIL_FAST_56_1_23
PASS_R1A_R2_15C_105_102_3
PASS_R1A_R2_LEGACY_PARITY_MISMATCH_ZERO
PASS_R1A_R2_CROSS_LAYER_AUTHORITY_LEAK_ZERO
PASS_R1A_R2_DEPENDENCY_CYCLE_ZERO
PASS_R1A_R2_CF1_V2_UNCHANGED
PASS_R1A_R2_NO_104_GATE_MIGRATION
PASS_R1A_R2_NO_CARGO_AUTHORITY_MIGRATION
PASS_R1A_R2_NO_PRODUCTION_AUTHORITY
```

The current staged bake does not claim `NEW_60_MATERIALIZED`, `SEMANTIC_PROJECTED_80`, or `FROZEN_ZERO`.

## Current receipt truth

```text
CoreRegistryChanged=False
CoreRegistrySourceSha256=14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6
PreviousSemanticProjectedCount=20
NewlyMaterializedCount=5
SemanticProjectedCount=25
FrozenSourceBoundActiveCount=55
NewGeneratedProgramCount=5
NewGeneratedCheckCount=389
NewGeneratedUnsupportedClauseCount=0
GeneratedProgramSourceSha256=6f988778f177ad942d60350f1ae214cf14ceb6306925d82f67ba486d5de13c14
GeneratedProgramRegenerationDeterministic=True
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

R1A-R2 remains active until executable coverage reaches 80/0. Only then may the project advance to `ASH-CONTROL-RUNTIME-CF1-SEMANTIC-MUTATION-PARITY-01B-R2`.