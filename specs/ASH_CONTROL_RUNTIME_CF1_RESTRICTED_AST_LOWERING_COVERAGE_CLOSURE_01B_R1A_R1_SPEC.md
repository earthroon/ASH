# ASH-CONTROL-RUNTIME-CF1-RESTRICTED-AST-LOWERING-COVERAGE-CLOSURE-01B-R1A-R1

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-RESTRICTED-AST-LOWERING-COVERAGE-CLOSURE-01B-R1A-R1
Parent: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-IR-COMPILER-AND-80-NODE-CLOSURE-01B-R1A
Role: restricted-AST lowering coverage expansion toward complete 80-node semantic closure
Production authority: false
CF1 V2 producer migration: false
104 structural-gate authority migration: false
Cargo compile authority migration: false
Python retirement: false
PowerShell retirement: false
Training math change: none
Optimizer change: none
Checkpoint change: none
Runtime route change: none
```

## Authority declaration

```text
Restricted Python AST Semantic Lowering /
Compiler Coverage Expansion /

74 Remaining Active Validator Projection Target /
Existing Semantic Programs Preserved /
80 Active Programs Final Closure Target /

One Compiler /
One Typed Semantic IR /
One Program Registry /
One Semantic Evaluator /

No Handwritten Validator Proliferation /
No Frozen PASS Replay /
No Expected-Disposition Evaluation /

Helper Function Inlining /
Static Loop Expansion /
Static Collection Evaluation /
Local Variable Dataflow /
Boolean Expression Lowering /
Comparison Lowering /
String Operation Lowering /
Section Extraction Lowering /
Regex Lowering /
Structured JSON Lowering /
SHA256 Lowering /
Set / Sequence Lowering /
Repository Query Lowering /
Registry Projection Lowering /
Python Syntax Check Lowering /

Explicit Unsupported Surface Inventory /
Deny-By-Default Compiler /
No Python Fallback /

Program Generation Determinism /
Legacy Check-ID Preservation /
Per-Check Provenance /

Existing 15C-R1 Failure Preserved /
Current 79 PASS / 1 FAIL Legacy Oracle Preserved /

No Python Runtime /
No PowerShell Runtime /
No Cargo Runtime In Semantic Route /

No CF1 V2 Mutation /
No 104-Gate Migration /
No Compile Authority Migration /
No Production Authority Claim
```

## 1. Parent state

The parent R1A bake established the semantic compiler/evaluator architecture and six independently evaluated active validators. It intentionally held the remaining 74 active validators rather than replaying their remembered legacy PASS dispositions.

Parent truth:

```text
DeclaredValidatorCount = 81
ActiveValidatorCount = 80
DeclaredInactiveCount = 1
SemanticProjectedCount = 6
FrozenSourceBoundActiveCount = 74
SemanticProjectionClosed = false
```

The current legacy Python oracle remains:

```text
DiagnosticFullMatrix = 79 PASS / 1 FAIL
FirstFailureOrdinal = 56
15C-R1 = 105 checks / 102 PASS / 3 scheduler-hash FAIL
```

## 2. R1A-R1 final objective

The normative completion target remains:

```text
SemanticProjectedCount = 80
FrozenSourceBoundActiveCount = 0
IncompleteProjectionCount = 0
UnsupportedProjectionCount = 0
ProgramCount = 80
EmptyProgramCount = 0
SemanticProjectionClosed = true
```

No active validator may be converted to PASS merely because its legacy expected disposition is PASS.

## 3. Current staged bake truth

This implementation tranche materially expands semantic lowering but does not claim final 80-node closure.

Current staged counts:

```text
DeclaredValidatorCount = 81
ActiveValidatorCount = 80
DeclaredInactiveCount = 1

SemanticProjectedCount = 20
FrozenSourceBoundActiveCount = 60
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

The staged 20 consist of:

```text
5 prior declarative semantic programs
1 independent 15C-R1 semantic pilot
14 newly generated R1A-R1 restricted-AST semantic programs
```

The 14 new programs contain:

```text
GeneratedR1AR1ProgramCount = 14
GeneratedR1AR1CheckCount = 1003
CurrentGeneratedCheckFailureCount = 0
```

All 1003 generated checks independently evaluate the current target source rather than consuming legacy expected PASS dispositions as outcome authority.

## 4. Newly projected validators

The staged restricted-AST generated programs cover the following execution ordinals:

```text
05  R6A-R2-R2 subgroup32 tiled segment gradient AdamW            36 checks
08  training lineage rebuild                                      86 checks
09  R2A genesis micro-segment plan rebase                         32 checks
10  N8 long-horizon continuity                                    70 checks
13  N8 source-weight generation SSOT                              28 checks
15  N8 phase wall-time attribution                                77 checks
16  N8 HiMuon production hotpath bind                             86 checks
17  RAM-resident Adam MV final writeback                          73 checks
18  N8 RAM-resident Adam MV resume-cut                           118 checks
20  TensorCube local Muon optimizer                              101 checks
26  RAM weight-pack persistent residency / atlas readahead        67 checks
29  TensorCube local Muon multi-tile batch dispatch               61 checks
33  TensorCube local Muon X-pad17 bank-conflict reduction         52 checks
49  BP/DK legacy migration ephemeral Muon lineage admission      116 checks
```

Total:

```text
14 programs
1003 checks
```

## 5. Existing semantic programs preserved

Existing semantic programs remain semantically owned by the same Rust evaluator path. The staged registry therefore has 20 active semantic projections in total.

The existing 15C-R1 program remains the known current semantic failure and is not repaired in this patch.

## 6. Typed generated semantic IR

R1A-R1 extends the checked-in Rust semantic-program model with generated expression types including:

```text
Cf1TextExpr
Cf1TextTransform
Cf1IntExpr
Cf1GeneratedBoolExpr
Cf1SemanticPredicate::Generated
```

Current staged transform coverage includes:

```text
lowercase
strip
lstrip
rstrip
replace
whitespace removal
text slicing
```

Current integer/text-expression coverage includes:

```text
text find
text index
text count
text length
constant integer
```

Current boolean coverage includes:

```text
constant
path exists
text contains
text equality
integer comparison
all
any
not
```

The compiler remains deny-by-default. An unsupported expression is not converted to the legacy expected result.

## 7. Restricted-AST compiler coverage surface

The current compiler declares an explicit staged lowering-coverage inventory. Supported staged families include:

```text
path / read_text / read_bytes
text contains / absence
lower / replace / whitespace normalization
count / find / index
text slicing
boolean all / any / not
integer comparison
static helper inlining
static loop expansion
static negative-fixture folding
```

The inventory states:

```text
denyByDefault = true
pythonRuntimeRequired = false
```

## 8. Remaining coverage blockers

The remaining 60 active validators are still fail-closed because their legacy dialect requires additional lowering families. Current observed blocker families include:

```text
regex and regex capture/canary extraction
split / splitlines / section extraction variants
symbolic conditional lowering
conditional-expression lowering
symbolic comprehension filters
repository path queries / rglob
advanced JSON and SHA256 dataflow
set / sequence membership and equality
registry static projection
importlib-style registry source handling without execution
Python syntax / sys-path style validator scaffolding
static starred collection expansion
additional string operations such as rfind
```

These are compiler-coverage gaps, not permission to replay frozen PASS results.

## 9. No arbitrary Python interpreter

R1A-R1 continues to distinguish:

```text
parse / inspect / statically lower / expand
```

from:

```text
execute Python / eval / exec / dynamic dispatch / VM fallback
```

The latter remains forbidden.

No Python executable, CPython runtime, pyo3 execution, PowerShell process, or Cargo process is part of the CF1 semantic route.

## 10. Program generation source authority

Checked-in generated source:

```text
crates/ash_control_runtime/src/cf1/programs/generated_r1ar1.rs
```

is build source, not a generated runtime manifest.

The program source is deterministic for identical compiler inputs.

Observed deterministic generation proof for this staged bake:

```text
Generated source SHA256 before regeneration:
c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f

Generated source SHA256 after regeneration:
c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f

ByteDeterministic = true
```

## 11. Program registry authority

The validator registry remains explicit and deterministic. File-system presence does not admit validators.

The 14 newly compiled validator registry entries move from:

```text
FrozenSourceBound
```

to:

```text
SemanticProjected
```

with translation revision:

```text
control01b-r1a-r1-restricted-ast-stage2
```

The staged registry truth is:

```text
SemanticProjected = 20
FrozenSourceBoundActive = 60
DeclaredInactive = 1
```

Parent-subset and class cardinalities are unchanged.

## 12. Target-source evaluation authority

The generated semantic programs evaluate current source bytes through typed Rust IR.

Target-source content is not required to retain the old frozen input SHA to be evaluated. The target may change and the semantic program must evaluate the changed source.

Legacy validator source identity remains provenance-bound. A changed legacy validator revision requires translation review/recompilation rather than silent reuse.

## 13. Expected legacy disposition boundary

Required order remains:

```text
Rust semantic evaluation
 -> semantic disposition
 -> legacy expected disposition comparison
 -> parity evidence
```

Forbidden:

```text
expected legacy PASS
 -> Rust PASS
```

Generated R1A-R1 semantic predicates do not consume the expected legacy disposition as evaluation input.

## 14. Legacy oracle regression

After the staged compiler/program changes, the full legacy Python validator set was re-run in execution-ordinal ranges.

Observed combined result:

```text
ordinals 00..33 = 34 PASS / 0 FAIL
ordinals 34..62 = 28 PASS / 1 FAIL
ordinals 63..79 = 17 PASS / 0 FAIL

TOTAL = 79 PASS / 1 FAIL
FIRST FAILURE = ordinal 56
```

The only failure remains the pre-existing 15C-R1 failure.

No newly generated Rust semantic source introduced an additional legacy validator failure.

## 15. Existing 15C-R1 failure preservation

Current ordinal 56 truth remains:

```text
checkCount = 105
passedCheckCount = 102
failedCheckCount = 3
```

The three failures remain scheduler-hash checks for downstream validators 16, 17, and 18.

R1A-R1 does not update those expected hashes. Repairing that baseline belongs to a later dedicated authority revision.

## 16. Legacy PowerShell producer preservation

The physical CF1 PowerShell compile-chain source remains byte-identical.

```text
SHA256 = 05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

R1A-R1 does not migrate compile orchestration authority.

## 17. Semantic route process isolation

Required and preserved:

```text
PythonProcessSpawnCount = 0
PowerShellProcessSpawnCount = 0
CargoProcessSpawnCount = 0
```

The development-time analysis/generation tooling used during migration is not shipped as a runtime control dependency and is not included as a new production authority surface.

## 18. Single semantic evaluator

R1A-R1 does not create one executable or evaluation engine per validator.

Topology remains:

```text
one ash_control_runtime
one CF1 semantic evaluator
one explicit CF1 validator registry
multiple typed semantic programs
```

The goal remains exactly 80 active programs in the single registry.

## 19. Final compiler families still required for 80-node closure

Before this patch ID can be promoted to final PASS, the compiler must additionally close the remaining observed families with explicit semantics:

```text
helper and local dataflow completion
static iterable/comprehension completion
regex search/findall/split/capture semantics
section and balanced-body extraction
structured nested JSON semantics
SHA256/digest fanout dataflow
set/sequence relations
repository deterministic source queries
source-mention exact-set relations
static registry projections
pure-Rust Python syntax parsing
known importlib registry projections without execution
```

Unsupported dynamic Python remains rejected rather than implemented as an arbitrary interpreter.

## 20. Normative final current-tree parity target

After all 80 programs are projected, the current tree must still produce:

```text
DiagnosticFullMatrixSemanticPassCount = 79
DiagnosticFullMatrixSemanticFailCount = 1
FirstFailureOrdinal = 56

LegacyFailFastSemanticPassCount = 56
LegacyFailFastSemanticFailCount = 1
LegacyFailFastNotExecutedCount = 23
```

The staged implementation has not reached this whole-graph Rust semantic result because 60 earlier/later active validators remain incomplete.

## 21. Mutation sanity versus R2

R1A-R1 may include narrow mutation sanity tests proving that a target-source change triggers semantic re-evaluation rather than frozen-binding rejection.

It does not perform the full Python-vs-Rust negative mutation matrix. That remains:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-MUTATION-PARITY-01B-R2
```

and is blocked until semantic projection reaches 80/80.

## 22. Physical Rust qualification

Final promotion requires a usable Rust toolchain and:

```text
cargo fmt --check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo check --manifest-path crates/ash_control_runtime/Cargo.toml
cargo test --manifest-path crates/ash_control_runtime/Cargo.toml
```

The current bake environment does not provide a usable Cargo/rustc/rustfmt toolchain. Therefore no physical Rust compile/test PASS is claimed for this staged bake.

## 23. Static/source sanity for the staged bake

Observed source-change boundary relative to the parent R1A bake:

```text
modified: crates/ash_control_runtime/src/cf1/compiler.rs
modified: crates/ash_control_runtime/src/cf1/programs/mod.rs
added:    crates/ash_control_runtime/src/cf1/programs/generated_r1ar1.rs
modified: crates/ash_control_runtime/src/cf1/registry.rs
modified: crates/ash_control_runtime/src/cf1/semantic.rs
```

No legacy validator, training implementation, optimizer implementation, checkpoint implementation, or PowerShell compile producer source is modified by this tranche.

## 24. Bake policy

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

Retain source authority material:

```text
Cargo.toml / Cargo.lock when present
source .args contracts
source JSON profiles
legacy validator source
Rust compiler/evaluator/program source
checked-in generated Rust semantic programs
```

This specification is committed to GitHub and is not embedded in the baked source ZIP.

## 25. Mandatory final promotion gates

The patch ID remains active until all of the following are true:

```text
PASS_CONTROL01B_R1A_R1_PROGRAM_COUNT_80
PASS_CONTROL01B_R1A_R1_SEMANTIC_PROJECTED_80
PASS_CONTROL01B_R1A_R1_FROZEN_ACTIVE_ZERO
PASS_CONTROL01B_R1A_R1_INCOMPLETE_ZERO
PASS_CONTROL01B_R1A_R1_UNSUPPORTED_ZERO
PASS_CONTROL01B_R1A_R1_NO_EMPTY_PROGRAM
PASS_CONTROL01B_R1A_R1_DETERMINISTIC_PROGRAM_GENERATION
PASS_CONTROL01B_R1A_R1_EXPECTED_DISPOSITION_NOT_EVALUATION_INPUT
PASS_CONTROL01B_R1A_R1_TARGET_SOURCE_REEVALUATION
PASS_CONTROL01B_R1A_R1_LEGACY_VALIDATOR_PROVENANCE_BINDING
PASS_CONTROL01B_R1A_R1_FULL_MATRIX_79_1_PARITY
PASS_CONTROL01B_R1A_R1_FAIL_FAST_56_1_23_PARITY
PASS_CONTROL01B_R1A_R1_15C_R1_105_102_3_PARITY
PASS_CONTROL01B_R1A_R1_NO_PYTHON_PROCESS
PASS_CONTROL01B_R1A_R1_NO_POWERSHELL_PROCESS
PASS_CONTROL01B_R1A_R1_NO_CARGO_PROCESS
PASS_CONTROL01B_R1A_R1_CF1_V2_UNCHANGED
PASS_CONTROL01B_R1A_R1_NO_104_GATE_AUTHORITY_MIGRATION
PASS_CONTROL01B_R1A_R1_NO_COMPILE_AUTHORITY_MIGRATION
PASS_CONTROL01B_R1A_R1_NO_PRODUCTION_AUTHORITY
```

The current staged bake does not claim `PROGRAM_COUNT_80` or `SEMANTIC_PROJECTED_80`.

## 26. Current staged receipt truth

```text
PatchId=ASH-CONTROL-RUNTIME-CF1-RESTRICTED-AST-LOWERING-COVERAGE-CLOSURE-01B-R1A-R1

DeclaredValidatorCount=81
ActiveValidatorCount=80
DeclaredInactiveValidatorCount=1

ExistingParentSemanticProjectionCount=6
GeneratedR1AR1ProgramCount=14
GeneratedR1AR1CheckCount=1003
SemanticProjectedCount=20
FrozenSourceBoundActiveCount=60

GeneratedProgramCurrentPassCount=14
GeneratedCheckCurrentPassCount=1003
GeneratedCheckCurrentFailCount=0

GeneratedProgramSourceDeterministic=True
GeneratedProgramSourceSha256=c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f

LegacyDiagnosticFullMatrixPassCount=79
LegacyDiagnosticFullMatrixFailCount=1
LegacyFirstFailureOrdinal=56

Known15CR1CheckCount=105
Known15CR1PassedCheckCount=102
Known15CR1FailedCheckCount=3
Known15CR1SchedulerHashFailureCount=3

PythonProcessSpawnCount=0
PowerShellProcessSpawnCount=0
CargoProcessSpawnCount=0

PowerShellProducerSha256=05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486

CF1CompileReceiptV2Mutation=False
StructuralGate104Migration=False
CargoCompileAuthorityMigration=False
ProductionAuthorityClaimed=False

SemanticProjectionClosed=False
```

## 27. Next implementation tranche

R2 remains blocked.

The immediate continuation stays under this same R1A-R1 authority and must close the remaining 60 validators by implementing the explicit unsupported families rather than replaying frozen results.

Only after:

```text
80 projected
0 frozen
0 incomplete
0 unsupported
```

may the roadmap advance to:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-MUTATION-PARITY-01B-R2
```
