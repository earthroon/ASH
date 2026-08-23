# ASH-CONTROL-RUNTIME-CF1-PYTHON-FIND-RANGE-ARGUMENT-PROJECTION-PARITY-01B-R1A-R2B1

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-PYTHON-FIND-RANGE-ARGUMENT-PROJECTION-PARITY-01B-R1A-R2B1
Parent: ASH-CONTROL-RUNTIME-CF1-SEMANTIC-DISPOSITION-AND-MATERIALIZATION-HOLD-SEPARATION-01B-R1A-R2B
Role: Python str.find positional-range semantic parity repair for already-admitted CF1 semantic programs
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
Python str.find Range Semantics Preservation /
Needle-Only Find /
Start-Bound Find /
Start-End-Bound Find /
No Silent Positional Argument Drop /
Nested Start Expression Preservation /
Python Minus-One Result Preservation /
Python Code-Point Index Preservation /
Compiler-Level Generic Lowering /
Device-Level Generic Execution /
No Validator-Specific Device Branch /
Ordinal 22 Projection False-Negative Repair /
Ordinal 56 Genuine Semantic Failure Preservation /
R2B Materialization-Hold Separation Preservation /
26 SemanticProjected / 54 Frozen Preservation /
Legacy Oracle 79 PASS / 1 FAIL Preservation /
15C-R1 105 / 102 / 3 Preservation /
No Production Authority Claim
```

## 1. Parent physical observation

R2B successfully separated materialization hold from semantic failure. The user's physical DiagnosticFullMatrix observation was:

```text
registrySemanticProjectedCount = 26
registryFrozenSourceBoundCount = 54
observedSemanticPassCount = 24
observedSemanticFailureCount = 2
observedFrozenHoldCount = 54
notExecutedCount = 0
firstSemanticFailureOrdinal = 22
firstMaterializationHoldOrdinal = 0
workflowDisposition = HeldMaterializationIncomplete
semanticProjectionClosed = false
productionAuthorityClaimed = false
```

Legacy oracle remains:

```text
79 PASS / 1 FAIL
FirstFailureOrdinal = 56
```

Therefore ordinal 22 was a semantic projection mismatch, not a target-source regression.

## 2. Confirmed defect

Ordinal 22:

```text
validatorId = cf1.production.qk-rmsnorm-attention-stability-static
legacyPath = tools/validate_qk_rmsnorm_attention_stability_static.py
checkId = q normalize before rope
legacyDisposition = PASS
preR2B1RustDisposition = FAIL
```

Legacy expression:

```python
forward.find('let q_for_rope') <
forward.find(
    'execute_base_train_atlas_wave_02_r6_r6_neox_rope',
    forward.find('let q_for_rope')
)
```

Observed source indices:

```text
let q_for_rope = 33268
first whole-file rope occurrence = 1148
rope occurrence after q_for_rope = 33475
```

Legacy semantics:

```text
33268 < 33475 = PASS
```

Pre-R2B1 generated program had dropped the second positional argument and evaluated:

```text
33268 < 1148 = FAIL
```

## 3. IR compatibility strategy

R2B1 does not add an `end` field to the existing `TextFind` variant because that would change the serialized shape and program digest of every existing TextFind-bearing program.

Existing ABI is preserved:

```rust
TextFind {
    text,
    needle,
    start: Option<Box<Cf1IntExpr>>,
}
```

Three-argument Python find receives a separate typed variant:

```rust
TextFindRange {
    text,
    needle,
    start: Box<Cf1IntExpr>,
    end: Box<Cf1IntExpr>,
}
```

This keeps prior one-argument and two-argument program encodings stable while admitting exact start/end semantics.

## 4. Compiler lowering

Generic Factory/compiler constructor:

```text
lower_python_str_find_call(text, needle, range_args)
```

Arity mapping:

```text
range_args = []
    -> TextFind(start=None)

range_args = [start]
    -> TextFind(start=Some(start))

range_args = [start,end]
    -> TextFindRange(start,end)

range_args > 2
    -> Cf1SemanticProjectionIncomplete
```

Extra arguments are never silently discarded.

Compiler capability inventory adds:

```text
text-find-range-arguments
```

Compiler patch identity:

```text
CF1_SEMANTIC_COMPILER_PATCH_ID =
ASH-CONTROL-RUNTIME-CF1-PYTHON-FIND-RANGE-ARGUMENT-PROJECTION-PARITY-01B-R1A-R2B1

CF1_SEMANTIC_COMPILER_REVISION =
control01b-r1a-r2b1-python-find-range-parity
```

## 5. Nested start preservation

The ordinal-22 expression is rematerialized as:

```text
TextFind("let q_for_rope", start=None)
<
TextFind(
    "execute_base_train_atlas_wave_02_r6_r6_neox_rope",
    start=Some(
        TextFind("let q_for_rope", start=None)
    )
)
```

The nested `Cf1IntExpr` is preserved. It is not reduced to `None`, zero, or a validator-specific constant.

## 6. Device semantics

The NativeSemanticDevice evaluates Python find semantics generically.

Canonical behavior:

```text
not found -> -1
found -> source index
start bound -> Python-compatible normalized start
start/end bounds -> Python-compatible [start,end) search
negative bounds -> Python slice-style normalization
Unicode index -> Unicode code-point index, not UTF-8 byte offset
```

The implementation does not branch on validator ID, ordinal, or check ID.

## 7. Reference semantic qualification

During bake, the generic range algorithm was compared against local Python `str.find` over a matrix containing:

```text
needle-only
positive start
negative start
positive end
negative end
empty needle
missing needle
ASCII
Unicode
start beyond length
start/end inversion
```

Result:

```text
EXHAUSTIVE_PARITY = PASS
```

This Python invocation is migration/reference qualification only. It is not called by Rust semantic execution and does not become production authority.

## 8. Generated program repair

Only the ordinal-22 `q normalize before rope` check changes inside `generated_r1ar2.rs`.

Before source SHA256:

```text
13c3bc10ca9dd7e41b8c403cf710ae5ffbc31d0f8499ce40cbdef0c83deb37cc
```

After source SHA256:

```text
8425b9455ed67ee5b3c92c1492a2a11a9b2368d53be4c6013e025f74adcc8cc1
```

The qk-rmsnorm validator check cardinality remains:

```text
101
```

Unrelated generated sources remain byte-identical:

```text
generated.rs       e7f2cc33388bec593647dc896cc51ca2026fb0e23378fc043eb23cf5851e7f74
generated_r1ar1.rs c96911569939dddefaa0abd054d90e3bce76fa360b467d605591fdd4534fb80f
generated_r2a.rs   af4dc3ce75cbcbf9841a65992bcb04362b52055318df3dfe8639e3243616ce18
```

## 9. Projection revision binding

Only the already-admitted ordinal-22 runtime projection receives the R2B1 translation revision:

```text
validatorId = cf1.production.qk-rmsnorm-attention-stability-static
translationRevision = control01b-r1a-r2b1-python-find-range-parity
```

`semantic_program_for` likewise publishes the R2B1 compiler revision only for this corrected program. Unrelated semantic programs retain their previous compiler revision.

## 10. Coverage preservation

R2B1 does not promote or demote validators.

```text
SemanticProjectedCount = 26
FrozenSourceBoundActiveCount = 54
DeclaredInactiveCount = 1
NewlyProjectedCount = 0
SemanticProjectionClosed = false
ProductionAuthorityClaimed = false
```

## 11. Core / capability preservation

Core Registry is byte-identical:

```text
crates/ash_core/src/cf1_control_authority.rs
SHA256 = 14b825fa1618ec5a7e98fd2ddceb6c0670a27c73ffddead212cdf9d6a418e3c6
```

R2A capability matrix source is byte-identical:

```text
crates/ash_control_runtime/src/cf1/capability_matrix.rs
SHA256 = 46dc230a41052c7be47770322b5011831b5140c6058ed7349404ea6771c2d66f
```

Workspace manifest is byte-identical:

```text
Cargo.toml
SHA256 = 4beccf28819d5d7c0b5505342c090824c40a25eb7d5a6994a0f04422a999ca16
```

## 12. Legacy oracle regression

All 80 active legacy validators were rerun in migration/reference mode after R2B1 source changes.

```text
PASS = 79
FAIL = 1
FirstFailureOrdinal = 56
Ordinal22 = PASS
```

15C-R1 remains:

```text
105 total
102 PASS
3 FAIL
```

The three failures remain scheduler-hash checks for validators 16, 17, and 18.

PowerShell producer remains byte-identical:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
SHA256 = 05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## 13. R2B disposition architecture preservation

R2B1 does not merge semantic failure and materialization hold again.

Expected DiagnosticFullMatrix after physical Rust qualification:

```text
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

Expected LegacyFailFast remains:

```text
observedSemanticPassCount = 0
observedSemanticFailureCount = 0
observedFrozenHoldCount = 1
notExecutedCount = 79
firstSemanticFailureOrdinal = null
firstMaterializationHoldOrdinal = 0
```

These are promotion gates until physically observed on a Rust toolchain.

## 14. Changed source surface

Exactly five source files differ from the R2B parent:

```text
crates/ash_control_runtime/src/cf1/compiler.rs
crates/ash_control_runtime/src/cf1/programs/generated_r1ar2.rs
crates/ash_control_runtime/src/cf1/programs/mod.rs
crates/ash_control_runtime/src/cf1/registry.rs
crates/ash_control_runtime/src/device/semantic.rs
```

No training, optimizer, checkpoint, Core, R2A capability, PowerShell producer, or CF1 V2 source is changed.

Current changed-source SHA256:

```text
compiler.rs          0797e72083d1b957025e70a0bb02d8b95aed9deecd1177f569822a07d9bc26ee
programs/mod.rs      27000ec1278c1e1b4c1ca8304b1fd1f05f6423e41cbfe8387bde07827eae19d8
generated_r1ar2.rs   8425b9455ed67ee5b3c92c1492a2a11a9b2368d53be4c6013e025f74adcc8cc1
registry.rs          3adf25e3d2c8a2f066a6c421052bb003144bae6b6b7f81952886c5627b5e50d5
device/semantic.rs   0582ff57b4e48957a927de60316e91399d3684fe66dadca79e998b7210c2ac19
```

## 15. Static qualification

Bake environment still exposes no usable Cargo/Rust compiler, so physical `cargo check/test` PASS is not claimed.

Static checks completed:

```text
changed Rust delimiter audit = PASS
invalid Rust \uXXXX escape count = 0
q program check count = 101
TextFind old ABI preserved = true
TextFindRange new end-bounded variant present = true
ordinal22 generated diff limited to q normalize before rope = true
generated_r1ar1 byte-identical = true
generated_r2a byte-identical = true
Core Registry byte-identical = true
PowerShell producer byte-identical = true
```

## 16. Physical qualification commands

```powershell
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime --no-run
cargo test -p ash_control_runtime
```

Diagnostic:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode diagnostic-full-matrix
```

Expected decisive fields:

```text
observedSemanticPassCount=25
observedSemanticFailureCount=1
firstSemanticFailureOrdinal=56
firstMaterializationHoldOrdinal=0
```

Ordinal-22 check receipt must report:

```text
q normalize before rope = Passed
```

Fail-fast:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-semantic-shadow `
  --repo-root . `
  --mode legacy-fail-fast
```

Capability matrix:

```powershell
cargo run -p ash_control_runtime -- `
  cf1-factory-capability-matrix `
  --repo-root .
```

Expected coverage:

```text
finalProjectedCount=26
finalFrozenCount=54
unclassifiedFrozenCount=0
```

## 17. Mandatory gates

```text
PASS_R2B1_CORE_REGISTRY_UNCHANGED
PASS_R2B1_CAPABILITY_MATRIX_UNCHANGED
PASS_R2B1_COVERAGE_26_54
PASS_R2B1_TEXTFIND_EXISTING_ABI_PRESERVED
PASS_R2B1_TEXTFIND_RANGE_VARIANT
PASS_R2B1_FIND_NEEDLE_ONLY_LOWERING
PASS_R2B1_FIND_START_LOWERING
PASS_R2B1_FIND_START_END_LOWERING
PASS_R2B1_NO_SILENT_ARGUMENT_DROP
PASS_R2B1_NESTED_START_EXPRESSION_PRESERVED
PASS_R2B1_PYTHON_MINUS_ONE_SEMANTICS
PASS_R2B1_PYTHON_CODEPOINT_INDEX_SEMANTICS
PASS_R2B1_NO_VALIDATOR_SPECIFIC_DEVICE_BRANCH
PASS_R2B1_ORDINAL22_CHECK_ID_PRESERVED
PASS_R2B1_ORDINAL22_CHECK_COUNT_101
PASS_R2B1_LEGACY_ORDINAL22_PASS
PASS_R2B1_LEGACY_ORACLE_79_1
PASS_R2B1_15C_105_102_3
PASS_R2B1_R2B_DISPOSITION_AXIS_PRESERVED
PASS_R2B1_NO_104_GATE_MIGRATION
PASS_R2B1_NO_CARGO_AUTHORITY_MIGRATION
PASS_R2B1_NO_CF1_V2_MUTATION
PASS_R2B1_NO_PRODUCTION_AUTHORITY
```

Physical promotion gates pending local Rust execution:

```text
PASS_R2B1_CARGO_CHECK
PASS_R2B1_CARGO_TEST
PASS_R2B1_ORDINAL22_RUST_PASS
PASS_R2B1_DIAGNOSTIC_25_PASS_1_FAIL
PASS_R2B1_FIRST_SEMANTIC_FAILURE_56
PASS_R2B1_FIRST_MATERIALIZATION_HOLD_0
```

## 18. Promotion blockers

R2B1 remains HOLD if any local physical run shows:

```text
ordinal22 q normalize before rope = Failed
observedSemanticFailureCount != 1
firstSemanticFailureOrdinal != 56
firstMaterializationHoldOrdinal != 0
coverage != 26 / 54
legacy oracle != 79 / 1
15C-R1 != 105 / 102 / 3
```

R2B1 repairs projection semantics only. It does not repair ordinal 56 and does not resume materialization coverage expansion until this already-admitted program is physically parity-clean.
