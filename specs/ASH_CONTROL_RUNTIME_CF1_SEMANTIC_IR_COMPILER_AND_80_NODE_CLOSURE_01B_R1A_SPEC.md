# ASH-CONTROL-RUNTIME-CF1-SEMANTIC-IR-COMPILER-AND-80-NODE-CLOSURE-01B-R1A

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-IR-COMPILER-AND-80-NODE-CLOSURE-01B-R1A
Parent: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-CHECK-PROJECTION-01B-R1
Role: restricted Python-AST to typed Rust semantic-program closure
Production authority: false
CF1 V2 producer migration: false
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
Legacy Validator Restricted-AST Compiler /
Pure-Rust Python Source Parsing /
No Python Execution /

Typed Semantic IR /
Deterministic Semantic Program Source /
Explicit Program Registry /

80 Active Validator Final Target /
1 Declared-Inactive Validator Preserved /

No Expected-Disposition Evaluation /
No Frozen PASS Replay /
No Target-Source Hash Outcome Authority /

Legacy Validator Source Provenance Binding /
Compiler Revision Binding /
Semantic Program Digest /

Unsupported Syntax Fail-Closed /
Incomplete Translation Fail-Closed /

No Python Subprocess /
No PowerShell Subprocess /
No Cargo Subprocess In Semantic Route /

Current Legacy Failure Preserved /
Ordinal 56 / 15C-R1 /
Three Scheduler-Hash Failures Preserved /

No CF1 Compile Receipt V2 Mutation /
No 104 Structural Gate Authority Migration /
No Cargo Compile Authority Migration /
No Production Authority Claim
```

## 1. Parent state

01B established the exact legacy validator registry:

```text
Declared = 81
Active = 80
Declared inactive = 1
Production = 75
Historical Preservation = 1
Operational Recovery = 1
Runtime Qualification = 3
Parent subset = 6
```

01B-R1 introduced the independent Rust semantic route and independently projected ordinal 56 / 15C-R1 with 105 current-source checks. Remaining active validators were intentionally fail-closed rather than replaying remembered PASS results.

## 2. Final R1A objective

R1A is complete only when:

```text
SemanticProjectedCount = 80
FrozenSourceBoundActiveCount = 0
IncompleteProjectionCount = 0
UnsupportedProjectionCount = 0
DeclaredInactiveCount = 1
```

An active validator without an independently executable Rust semantic program may never be represented as PASS.

## 3. Compiler boundary

The compiler reads retained legacy Python validator source using a pure-Rust Python parser and lowers only an explicit supported subset into typed semantic programs.

```text
Python source
 -> restricted AST admission
 -> typed semantic lowering
 -> deterministic checked-in Rust program source
 -> Rust semantic evaluator
```

Parsing Python is not Python execution.

Forbidden runtime dependencies:

```text
python
python3
py.exe
CPython embedding
pyo3 execution
eval
exec
arbitrary Python VM
```

Unsupported syntax or semantics produce an explicit HOLD. There is no Python fallback.

## 4. Compiler and program SSOT

Canonical compiler surface:

```text
crates/ash_control_runtime/src/cf1/compiler.rs
```

Canonical staged program surface:

```text
crates/ash_control_runtime/src/cf1/programs/mod.rs
crates/ash_control_runtime/src/cf1/programs/generated.rs
```

Checked-in generated Rust is build source, not a runtime-generated manifest. Generated runtime receipts, failure reports, target directories, and artifact directories are excluded from source ZIP authority.

## 5. Deterministic program generation

For identical:

```text
legacy validator bytes
compiler revision
registry projection bytes
```

semantic program generation must be deterministic.

Machine absolute paths, timestamps, receipt locations, and durations are excluded from semantic-program identity.

Every program retains:

```text
validator ID
legacy validator path
legacy validator SHA256
compiler revision
semantic program digest
```

If the legacy validator changes, the translation becomes stale. If a target Rust/WGSL/JSON/TOML file changes, the existing program evaluates the changed target rather than rejecting it merely because an old target digest changed.

## 6. Typed semantic predicates

The first declarative layer includes:

```text
PathExists
TextContains
TextContainsCaseInsensitive
TextCountEquals
TextSearchCompare
JsonStringEquals
JsonU64Equals
JsonF64Equals
N8ProfileDigestExact
All
Any
Not
```

The final compiler may extend this with explicit section extraction, regex, set/sequence relations, registry projections, Python syntax parsing, repository queries, digest fanout, and named custom semantics.

Anonymous closure authority is forbidden.

Search ordering preserves legacy Python `.find()` behavior, including `-1` for absent text where that behavior affected the legacy predicate.

Migration must not silently strengthen or weaken a check. A text check remains a text check; a section/order/hash rule remains section/order/hash semantics unless a separate policy revision explicitly changes it.

## 7. Structured JSON and digest semantics

Where legacy validators use structured JSON, Rust uses structured JSON values rather than substring substitution.

Where a legacy validator computes SHA256, Rust computes SHA256 over current bytes. Expected digests are not outcome shortcuts.

The N8 scheduler profile digest preserves the legacy framing order and little-endian numeric encoding contract.

## 8. Expected legacy disposition

`expected_legacy_disposition` is comparison metadata only.

Mandatory order:

```text
Rust semantic checks
 -> Rust semantic disposition
 -> compare against expected legacy disposition
 -> parity result
```

Changing only the expected legacy disposition must not change the semantic result.

## 9. Current legacy oracle truth

The retained Python oracle remains:

```text
Diagnostic full matrix = 79 PASS / 1 FAIL
First failure ordinal = 56
```

Ordinal 56 is:

```text
tools/validate_ash_bp_dk_fusion_legacy_restart_barrier_transaction_marker_classification_15c_r1_static.py
```

Current 15C-R1 result:

```text
105 checks
102 PASS
3 FAIL
```

All three failures are the existing scheduler-hash failures for validators 16, 17, and 18. R1A does not repair those hashes.

Final semantic target on the current tree is therefore:

```text
DiagnosticFullMatrix = 79 PASS / 1 FAIL
LegacyFailFast = 56 PASS / 1 FAIL / 23 NotExecutedFailFast
FirstFailureOrdinal = 56
```

A legacy semantic FAIL faithfully reproduced by Rust is parity evidence. It is not an evaluator crash.

## 10. Semantic failure versus authority failure

Normal outcomes:

```text
Passed
Failed
```

Authority/evaluator failures remain distinct:

```text
SemanticProjectionIncomplete
SemanticTranslationStale
SemanticUnsupported
SemanticEvaluationFailed
RegistryProjectionStale
PythonSyntaxProjectionMismatch
```

Incomplete or unsupported translation is never converted to the expected legacy PASS result.

## 11. One runtime, one semantic registry

R1A does not create 80 Rust executables.

```text
one ash_control_runtime
one semantic evaluator
one explicit validator registry
80 semantic programs
```

is the final topology.

File-system presence never admits a validator. The existing 81-entry registry remains membership SSOT, and the declared-inactive legacy entry remains inactive.

## 12. Current staged bake implementation

This bake deliberately does not claim final 80-node closure.

Independently projected nodes now present:

```text
ordinal 11  basetrain storage-root authority             39 checks
ordinal 12  N8 scheduler horizon extension               23 checks
ordinal 24  CF1 release-profile authority                16 checks
ordinal 28  GPU successor weight commit continuity       52 checks
ordinal 30  TensorCube local-Muon production callsite    63 checks
ordinal 56  15C-R1 transaction marker classification    105 checks
```

Current staged state:

```text
SemanticProjectedCount = 6
FrozenSourceBoundActiveCount = 74
DeclaredInactiveCount = 1
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

The five newly declarative PASS nodes evaluate current source without consuming their expected legacy PASS disposition as outcome authority.

The three automatically generated direct-check programs have zero expression-result mismatches against their legacy check expressions on the current source:

```text
storage-root   39 / 39
GPU successor  52 / 52
TensorCube     63 / 63
```

Generated direct checks: 154.

The generated Rust program source was regenerated from identical inputs and compared byte-for-byte during this bake; the result was deterministic.

## 13. Legacy oracle regression after staged bake

The added compiler/program source introduces no new legacy Python validator failure.

Observed full matrix after the staged bake:

```text
ordinal 0..39  = 40 PASS
ordinal 40..55 = 16 PASS
ordinal 56     = existing 15C-R1 FAIL
ordinal 57..79 = 23 PASS in diagnostic full matrix

TOTAL = 79 PASS / 1 FAIL
```

## 14. Legacy producer preservation

The physical CF1 PowerShell compile producer remains byte-identical.

```text
SHA256 = 05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## 15. Process isolation

The semantic compiler/evaluator path contains no process-spawn authority for Python, PowerShell, or Cargo.

Required counters:

```text
pythonProcessSpawnCount = 0
powershellProcessSpawnCount = 0
cargoProcessSpawnCount = 0
```

Literal source strings mentioning Cargo or PowerShell are evidence inspected by semantic checks, not process execution.

## 16. Explicit non-goals

R1A does not migrate:

```text
104 structural-gate physical authority
cargo fmt authority
cargo check authority
targeted cargo test authority
cargo build --release authority
PowerShell SourceTreeDigest authority
CF1 V2 production receipt publication
production binary admission
```

`R6AR2R2CF1CompileReceipt` V2 remains unchanged.

## 17. Source mutation boundary

The semantic compiler/evaluator validates and reports. It does not repair source or legacy validators.

A stale legacy validator translation does not silently regenerate itself during validation. Program regeneration is an explicit development-time source change subject to review.

## 18. Final R1A required tests

```text
all_80_active_validators_compile
inactive_validator_is_not_compiled
semantic_projected_count_is_80
frozen_active_count_is_0
semantic_incomplete_count_is_0
semantic_unsupported_count_is_0

program_generation_is_deterministic
program_ids_are_unique
check_ids_are_unique_per_validator
no_active_program_is_empty

semantic_result_is_independent_of_expected_legacy_disposition
target_source_change_is_re_evaluated
legacy_validator_change_marks_translation_stale

semantic_full_matrix_is_79_pass_1_fail
semantic_first_failure_is_ordinal_56
semantic_fail_fast_is_56_pass_1_fail_23_not_executed
semantic_15c_r1_is_105_checks_3_scheduler_hash_failures

semantic_route_never_spawns_python
semantic_route_never_spawns_powershell
semantic_route_never_spawns_cargo
```

## 19. Physical Rust qualification

When a usable Rust toolchain is available:

```text
cargo fmt --check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo test --manifest-path crates/ash_control_runtime/Cargo.toml
```

must pass before final promotion. A bake environment without the toolchain must not claim these gates passed.

## 20. Mandatory final promotion gates

```text
PASS_CONTROL01B_R1A_PURE_RUST_PARSER
PASS_CONTROL01B_R1A_SEMANTIC_PROGRAM_80
PASS_CONTROL01B_R1A_NO_ACTIVE_FROZEN_REPLAY
PASS_CONTROL01B_R1A_NO_INCOMPLETE_PROGRAM
PASS_CONTROL01B_R1A_NO_UNSUPPORTED_PROGRAM
PASS_CONTROL01B_R1A_EXPECTED_DISPOSITION_NOT_EVALUATION_INPUT
PASS_CONTROL01B_R1A_TARGET_SOURCE_HASH_OUTCOME_AUTHORITY_RETIRED
PASS_CONTROL01B_R1A_LEGACY_VALIDATOR_PROVENANCE_BOUND
PASS_CONTROL01B_R1A_DETERMINISTIC_PROGRAM_GENERATION
PASS_CONTROL01B_R1A_FULL_MATRIX_79_1_PARITY
PASS_CONTROL01B_R1A_FAIL_FAST_56_1_23_PARITY
PASS_CONTROL01B_R1A_15C_R1_105_102_3_PARITY
PASS_CONTROL01B_R1A_NO_PYTHON_PROCESS
PASS_CONTROL01B_R1A_NO_POWERSHELL_PROCESS
PASS_CONTROL01B_R1A_NO_CARGO_PROCESS
PASS_CONTROL01B_R1A_CF1_V2_UNCHANGED
PASS_CONTROL01B_R1A_NO_104_GATE_AUTHORITY_MIGRATION
PASS_CONTROL01B_R1A_NO_COMPILE_AUTHORITY_MIGRATION
PASS_CONTROL01B_R1A_NO_PRODUCTION_AUTHORITY
```

The current staged bake does **not** claim `PASS_CONTROL01B_R1A_SEMANTIC_PROGRAM_80`.

## 21. Current staged bake truth

```text
SemanticCompilerSourcePresent=True
PureRustPythonParserDependencyDeclared=True

DeclarativeSemanticProgramCount=5
Handwritten15CR1PilotCount=1
SemanticProjectedCount=6
FrozenSourceBoundActiveCount=74

GeneratedDirectCheckCount=154
GeneratedDirectCheckTranslationMismatchCount=0

LegacyDiagnosticFullMatrixPassCount=79
LegacyDiagnosticFullMatrixFailCount=1
LegacyFirstFailureOrdinal=56

Known15CR1CheckCount=105
Known15CR1PassedCheckCount=102
Known15CR1FailedCheckCount=3

PythonProcessSpawnCount=0
PowerShellProcessSpawnCount=0
CargoProcessSpawnCount=0

PowerShellProducerSha256=05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486

SemanticProjectionClosed=False
ProductionAuthorityClaimed=False
```

## 22. Bake policy

Exclude from the delivered source ZIP:

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

Retain build/source authority material such as Cargo files, source `.args` contracts, source JSON profiles, retained legacy validators, and Rust compiler/evaluator/program source.

This specification is committed to the ASH Git repository and is not embedded in the baked source ZIP.

## 23. Next execution step

R1A remains the active patch until:

```text
80 semantic programs
0 frozen active
0 incomplete
0 unsupported
```

are reached. The next implementation tranche must extend restricted AST lowering for remaining helper/loop/regex/registry families rather than starting mutation parity early.

Only after full R1A closure should the project advance to:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-MUTATION-PARITY-01B-R2
```
