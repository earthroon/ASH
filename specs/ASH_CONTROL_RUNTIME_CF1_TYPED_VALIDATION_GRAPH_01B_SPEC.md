# ASH-CONTROL-RUNTIME-CF1-TYPED-VALIDATION-GRAPH-01B

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-TYPED-VALIDATION-GRAPH-01B
Parent: ASH-CONTROL-RUNTIME-CF1-CONTRACT-EXTRACTION-01A
Role: source-bound Rust CF1 static-validation shadow graph
Production authority: false
CF1 producer migration: false
Python retirement: false
PowerShell retirement: false
104 structural-gate migration: false
Cargo compile authority migration: false
Training math change: none
Optimizer change: none
Checkpoint change: none
Inference route change: none
```

## Authority declaration

```text
CF1 Legacy Validator Inventory Closure /
Rust-Native Typed Shadow Registry /
One Generic Control Validation Graph /
No Competing Graph Engine /

Exact Active-Set Preservation /
Exact Validator-Class Preservation /
Exact Legacy Execution Ordering /
Exact Parent-Subset Preservation /

81 Declared Validators /
80 Active Validators /
1 Declared-Inactive Validator /

Production 75 /
Historical Preservation 1 /
Operational Recovery 1 /
Runtime Qualification 3 /
Parent Subset 6 /

Frozen Source-Bound Projection /
Legacy Validator SHA256 Binding /
Observed Input Read-Set Binding /
Repository Source-Surface Binding /
Stale Translation Fail-Closed /

Legacy Fail-Fast Replay /
Diagnostic Full-Matrix Replay /
Existing Legacy Failure Preservation /
No Silent Legacy Repair /

No Python Subprocess In Rust Shadow /
No PowerShell Subprocess In Rust Shadow /
No Cargo Subprocess In CF1 Shadow /
No Dynamic Validator Discovery /

Shadow Receipt Only /
No CF1 Compile Receipt V2 Mutation /
No Production Authority Claim /

Legacy PowerShell CF1 Authority Preserved /
Legacy Python Validator Authority Preserved /

No 104 Structural Gate Implementation Migration /
No Cargo Compile Authority Migration /
No Receipt Producer Migration /
No SourceTreeDigest Authority Migration /

No Training Math Change /
No Optimizer Change /
No Checkpoint Change /
No Runtime Route Change
```

## 1. Parent closure

01A established:

```text
ash_core::cf1_compile_contract
= producer / consumer neutral CF1 compile-contract SSOT
```

01B does not change that contract. It establishes a separate typed representation of the current legacy CF1 static-validation execution set inside `ash_control_runtime`. The word `shadow` remains mandatory. This revision does not replace the physical legacy validator chain.

## 2. Legacy inventory truth

The current CF1 PowerShell chain declares 81 validator paths but executes 80:

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

The six parent validators are already members of the Production set. `Parent` is a projection subset, not a second execution class, and those validators must not be double-executed.

## 3. Declared-inactive legacy entry

The legacy path:

```text
tools/validate_ash_production_import_surface_contraction_15.py
```

is declared but not executed by the current PowerShell chain. The active successor is:

```text
tools/validate_ash_production_import_surface_contraction_15_r1.py
```

The older entry is represented as:

```text
active = false
executionOrdinal = None
translationState = DeclaredInactive
```

File-system presence alone never grants validator execution authority.

## 4. Current legacy disposition truth

The current source tree is not an 80/80 PASS baseline. Diagnostic full-matrix execution of the 80 active legacy validators yields:

```text
PASS = 79
FAIL = 1
```

The existing failure is execution ordinal 56:

```text
tools/validate_ash_bp_dk_fusion_legacy_restart_barrier_transaction_marker_classification_15c_r1_static.py
```

It currently reports three pre-existing scheduler-hash failures against:

```text
validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
```

Therefore the current legacy fail-fast behavior is:

```text
ordinal 0..55   = 56 PASS
ordinal 56      = 1 FAIL
ordinal 57..79  = 23 not executed
```

01B preserves this fact. It must not update those scheduler hashes merely to make the shadow receipt green.

## 5. Existing-failure preservation invariant

Forbidden:

```text
legacy validator fails
-> Rust registry declares PASS
```

Forbidden:

```text
legacy hash mismatch
-> 01B edits downstream expected hashes
-> legacy becomes PASS
```

The current baseline is represented explicitly:

```text
CF1_CURRENT_LEGACY_FIRST_FAILURE_ORDINAL = 56
CF1_CURRENT_LEGACY_FULL_MATRIX_PASS_COUNT = 79
CF1_CURRENT_LEGACY_FULL_MATRIX_FAIL_COUNT = 1
```

01B is a projection patch, not a legacy-repair patch.

## 6. One validation engine

CONTROL-01 already introduced the control-runtime validation graph. 01B generalizes that engine rather than creating a separate CF1 graph runtime.

Canonical generic node:

```rust
ValidationNode {
    id,
    domain,
    class,
    dependencies,
    execution_ordinal,
    program,
}
```

Domains:

```text
ControlBootstrap
Cf1StaticValidation
```

Classes:

```text
Bootstrap
Production
HistoricalPreservation
OperationalRecovery
RuntimeQualification
```

## 7. Bootstrap semantic preservation

The CONTROL-01 graph remains exactly:

```text
B001 ManifestExists
B002 DependencyBoundary
B003 CargoAvailable
B004 MetadataResolution
B005 CargoLockResolution
B006 ControlCargoFmt
B007 ControlCargoCheck
B008 ControlUnitTests
B009 BinaryIdentity
B010 ReceiptPublication
```

01B may generalize the node representation but may not alter these IDs, dependency semantics, or fail-closed behavior.

Required regression:

```text
bootstrap_graph_semantics_unchanged
```

## 8. CF1 module boundary

Canonical layout:

```text
crates/ash_control_runtime/src/cf1/
├─ mod.rs
├─ types.rs
├─ registry.rs
├─ source_binding.rs
├─ shadow.rs
└─ receipt.rs
```

The generic graph engine remains outside the domain module.

## 9. Explicit registry authority

Each declared legacy validator has an explicit Rust registry entry:

```rust
Cf1ValidatorSpec {
    validator_id,
    class,
    parent_validator,
    legacy_path,
    legacy_source_sha256,
    active,
    execution_ordinal,
    expected_legacy_disposition,
    translation_state,
    translation_revision,
    input_binding,
}
```

No directory scan determines registry membership.

Forbidden:

```text
glob tools/validate_*.py
sort filenames
execute whatever exists
admit validator because file exists
```

## 10. Stable ID and execution ordinal separation

```text
validatorId != executionOrdinal
```

Every active validator has one unique ordinal in `0..79`. The declared-inactive validator has no ordinal. Parent membership is metadata over active Production nodes and never creates a second execution pass.

Required:

```text
ParentSubsetCount = 6
ParentDoubleExecutionCount = 0
```

## 11. Translation level in 01B

01B deliberately does not claim full clause-level Rust reimplementation of all 80 Python validators. Its initial translation state is:

```text
FrozenSourceBound
```

Meaning:

```text
legacy validator source identity
+
observed validator input identity
+
known current legacy disposition
```

are bound into a typed Rust registry.

This is a strict snapshot-parity authority candidate, not yet a semantic interpreter for every Python condition. Source/input drift must fail closed rather than reuse an old disposition.

## 12. Legacy validator source binding

Every declared validator records:

```text
legacyPath
legacySourceSha256
```

At shadow execution time:

```text
SHA256(current legacy validator source)
==
registered legacySourceSha256
```

is mandatory. Mismatch becomes `Cf1BindingStale`.

## 13. Input binding modes

01B supports two typed input binding modes:

```rust
Cf1InputBinding::ExactReadSet { files }
```

for validators with a bounded observed read set, and:

```rust
Cf1InputBinding::RepositorySourceSurface {
    expected_digest,
    expected_file_count,
}
```

for broad repository scanners.

Each exact file binding records path plus SHA256. Missing or changed input becomes `StaleBinding`; the Rust shadow does not guess whether the changed input would have preserved the Python result.

## 14. Repository source-surface binding

Repository-wide scanners use one deterministic source-surface digest over source-like files such as:

```text
.rs .wgsl .toml .py .ps1 .json .jsonl .args
.md .txt .yaml .yml .js .mjs .cjs .ts .tsx .vue
.css .html .sh
Cargo.toml
Cargo.lock
```

Excluded runtime/build surfaces:

```text
.git/
target/
artifacts/
artifact/
__pycache__/
*.pyc
*.pyo
*.sha256
```

The generated Rust registry file is excluded from this repository-surface digest to avoid a self-referential hash cycle.

Canonical framing is:

```text
relative/path NUL sha256 LF
```

with lexically sorted relative paths. Machine absolute paths, timestamps, and receipt locations are excluded.

## 15. Stale translation behavior

Any active validator with:

```text
legacy source SHA drift
input read-set drift
repository source-surface drift
missing input binding
```

is not allowed to reuse its frozen disposition. It becomes:

```text
StaleBinding
```

and shadow parity is not closed.

## 16. Python lexical preflight boundary

01B may perform a Rust-local lexical plausibility preflight on frozen Python source bytes. This is corruption detection only. It is not Python execution and is not claimed as full CPython grammar equivalence.

Full clause-level Python semantic replacement belongs to a later projection revision.

## 17. Process isolation

The Rust CF1 shadow route contains no Python, PowerShell, or Cargo subprocess execution.

Required counters:

```text
pythonProcessSpawnCount = 0
powershellProcessSpawnCount = 0
cargoProcessSpawnCount = 0
```

CONTROL-01 bootstrap may still execute its own Cargo self-validation operations. That is a separate route.

## 18. Shadow execution modes

```rust
Cf1ShadowExecutionMode::LegacyFailFast
Cf1ShadowExecutionMode::DiagnosticFullMatrix
```

### LegacyFailFast

Reproduces current PowerShell sequencing. After the first known legacy FAIL, later active validators become:

```text
NotExecutedFailFast
```

They are never falsely marked PASS.

Current expected result:

```text
PassedCount                  = 56
FailedLegacyParityCount      = 1
NotExecutedFailFastCount     = 23
FirstFailureOrdinal          = 56
StaleBindingCount            = 0
```

### DiagnosticFullMatrix

Replays the complete bound baseline:

```text
PassedCount                  = 79
FailedLegacyParityCount      = 1
NotExecutedFailFastCount     = 0
FirstFailureOrdinal          = 56
StaleBindingCount            = 0
```

Diagnostic full matrix is not the legacy execution policy.

## 19. Shadow parity versus validator success

These are separate truths:

```text
shadowParityClosed = true
```

means the Rust shadow faithfully represents the frozen current legacy baseline. It does not mean all legacy validators passed.

A faithfully reproduced legacy FAIL is parity evidence. A stale source/input binding is a shadow failure.

## 20. Per-node receipt

Each node receipt binds:

```text
validatorId
class
executionOrdinal
parentValidator
legacyPath
legacySourceSha256
translationRevision
expectedLegacyDisposition
disposition
bindingFresh
detail
receiptHash
```

## 21. Shadow receipt

Schema:

```text
ash.control_runtime.cf1.static_validation_shadow.v1
```

Patch identity:

```text
ASH-CONTROL-RUNTIME-CF1-TYPED-VALIDATION-GRAPH-01B
```

The shadow receipt is not `R6AR2R2CF1CompileReceipt` V2 and must never be written into the V2 production path.

Required cardinality:

```text
declaredValidatorCount       = 81
activeValidatorCount         = 80
declaredInactiveCount        = 1
productionCount              = 75
historicalPreservationCount  = 1
operationalRecoveryCount     = 1
runtimeQualificationCount    = 3
parentSubsetCount             = 6
frozenSourceBoundTranslationCount = 80
```

Required isolation:

```text
pythonProcessSpawnCount      = 0
powershellProcessSpawnCount  = 0
cargoProcessSpawnCount       = 0
productionAuthorityClaimed   = false
staleBindingCount            = 0
shadowParityClosed           = true
```

## 22. No CF1 V2 mutation

01A's V2 contract remains exact. Forbidden V2 additions include:

```text
rustShadowPassed
shadowReceiptHash
validationGraphDigest
controlRuntimeVersion
```

All 01B shadow evidence stays in its own schema.

## 23. Control-runtime route

01B adds:

```text
ash_control_runtime cf1-static-shadow
  --repo-root <path>
  [--receipt <path>]
  [--mode legacy-fail-fast|diagnostic-full-matrix]
```

The route performs static shadow observation only and always reports:

```text
productionAuthorityClaimed = false
```

## 24. Legacy authority preservation

After 01B:

```text
PowerShell CF1 compile chain = physical authority
Python CF1 validators        = legacy validator authority
Rust CF1 typed graph         = shadow authority candidate
```

The existing CF1 PowerShell producer remains byte-identical through this patch.

Frozen SHA256 for this bake line:

```text
05754a698c1c4f8d883bbd177633fd45d7d00290972b81f030f1f2ed6ce7b486
```

## 25. 104 structural-gate boundary

The 104 structural gates are not translated into the Rust graph in 01B. The 104-line `.args` contract remains legacy source authority required by existing validators and the PowerShell chain.

Including that deterministic source contract in the baked source ZIP is not the same as migrating its validation implementation into Rust.

## 26. Restored deterministic source contracts

The prior source bake lacked source contracts/profile documents required by current legacy validators. 01B restores them as source authority material:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6a_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6a_r1_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6a_r2_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6a_r2_r1_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1j_r6a_r2_r2_cf1_contract.args
specs/r6_physical_admission_probe_scheduler_profile.json
specs/n8_long_horizon_scheduler_profile.json
specs/tensorcube_local_muon_production_profile_r1.json
```

These are source contracts, not generated runtime manifests or receipts.

## 27. No compile/release authority migration

01B does not move any of the following to Rust CF1 authority:

```text
104 structural-gate implementation
cargo fmt
cargo check
targeted cargo test
cargo build --release
PowerShell SourceTreeDigest
production CF1 V2 receipt publication
```

The 01B repository source-surface digest is only a shadow binding mechanism and is not the future canonical release source digest.

## 28. Read-only behavior

The CF1 shadow may read source and publish its own diagnostic receipt. It must not:

```text
modify source
repair JSON
rewrite validators
update legacy expected hashes
run cargo fmt apply
```

## 29. Required tests

Registry and order:

```text
cf1_declared_validator_count_is_81
cf1_active_validator_count_is_80
cf1_declared_inactive_count_is_1
cf1_production_count_is_75
cf1_historical_count_is_1
cf1_operational_count_is_1
cf1_runtime_qualification_count_is_3
cf1_parent_subset_count_is_6
parent_subset_is_not_double_executed
inactive_import_surface_validator_cannot_resurrect
cf1_execution_ordinals_are_unique_contiguous_0_to_79
duplicate_cf1_validator_id_is_rejected
duplicate_execution_ordinal_is_rejected
cf1_order_is_deterministic
```

Current baseline:

```text
current_legacy_first_failure_is_explicit_not_silently_repaired
legacy_fail_fast_preserves_first_failure
legacy_fail_fast_marks_tail_not_executed
full_matrix_preserves_known_79_1_baseline
shadow_parity_can_close_while_legacy_validation_contains_known_failure
```

Binding:

```text
legacy_source_digest_drift_is_rejected
exact_read_set_digest_drift_is_rejected
repository_source_surface_digest_drift_is_rejected
missing_bound_file_is_rejected
```

Isolation:

```text
cf1_shadow_never_spawns_python
cf1_shadow_never_spawns_powershell
cf1_shadow_never_spawns_cargo
bootstrap_graph_semantics_unchanged
```

## 30. Dynamic-discovery poison rule

Adding an unrelated file such as:

```text
tools/validate_fake_should_never_run.py
```

must never admit a new validator node. It may make repository-surface-bound projections stale, which is correct source-drift behavior, but registry cardinality must remain unchanged.

## 31. Generated-artifact bake policy

Exclude from the baked source ZIP:

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

Do not exclude implementation source merely because a filename contains `manifest`.

```text
Cargo.toml
Cargo.lock
source .args contracts
source JSON profiles
```

remain source material.

This 01B specification is committed to the ASH Git repository and is not required inside the baked source ZIP.

## 32. Physical Rust toolchain gate

When Cargo/rustc/rustfmt are available, physical closure includes:

```text
cargo fmt --check
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime
```

plus legacy CF1 matrix evidence.

A bake environment without a Rust toolchain must not claim these Rust compile/test gates passed.

## 33. Mandatory gates

```text
PASS_CONTROL01B_GENERIC_VALIDATION_GRAPH_REUSED
PASS_CONTROL01B_BOOTSTRAP_GRAPH_SEMANTICS_PRESERVED

PASS_CONTROL01B_DECLARED_VALIDATOR_COUNT_81
PASS_CONTROL01B_ACTIVE_VALIDATOR_COUNT_80
PASS_CONTROL01B_DECLARED_INACTIVE_COUNT_1
PASS_CONTROL01B_PRODUCTION_COUNT_75
PASS_CONTROL01B_HISTORICAL_COUNT_1
PASS_CONTROL01B_OPERATIONAL_COUNT_1
PASS_CONTROL01B_RUNTIME_QUALIFICATION_COUNT_3
PASS_CONTROL01B_PARENT_SUBSET_COUNT_6
PASS_CONTROL01B_INACTIVE_VALIDATOR_NOT_RESURRECTED
PASS_CONTROL01B_CONTIGUOUS_LEGACY_ORDER_0_79

PASS_CONTROL01B_FROZEN_SOURCE_BOUND_TRANSLATION_80
PASS_CONTROL01B_LEGACY_SOURCE_BINDING
PASS_CONTROL01B_INPUT_SURFACE_BINDING
PASS_CONTROL01B_STALE_BINDING_FAIL_CLOSED

PASS_CONTROL01B_CURRENT_LEGACY_FAILURE_PRESERVED
PASS_CONTROL01B_LEGACY_FAIL_FAST_BASELINE_56_1_23
PASS_CONTROL01B_FULL_MATRIX_BASELINE_79_1

PASS_CONTROL01B_NO_PYTHON_SUBPROCESS
PASS_CONTROL01B_NO_POWERSHELL_SUBPROCESS
PASS_CONTROL01B_NO_CARGO_SUBPROCESS
PASS_CONTROL01B_NO_DYNAMIC_VALIDATOR_DISCOVERY

PASS_CONTROL01B_SHADOW_RECEIPT_SEPARATE_FROM_CF1_V2
PASS_CONTROL01B_NO_PRODUCTION_AUTHORITY_CLAIM
PASS_CONTROL01B_POWERSHELL_PRODUCER_UNCHANGED
PASS_CONTROL01B_LEGACY_PYTHON_AUTHORITY_PRESERVED

PASS_CONTROL01B_NO_104_GATE_IMPLEMENTATION_MIGRATION
PASS_CONTROL01B_NO_CARGO_COMPILE_AUTHORITY_MIGRATION
PASS_CONTROL01B_NO_RECEIPT_PRODUCER_MIGRATION
PASS_CONTROL01B_NO_SOURCETREE_DIGEST_AUTHORITY_MIGRATION

PASS_CONTROL01B_NO_TRAINING_MATH_CHANGE
PASS_CONTROL01B_NO_OPTIMIZER_CHANGE
PASS_CONTROL01B_NO_CHECKPOINT_CHANGE
PASS_CONTROL01B_NO_RUNTIME_ROUTE_CHANGE
```

## 34. Current bake truth

```text
DeclaredValidatorCount=81
ActiveValidatorCount=80
DeclaredInactiveValidatorCount=1

ProductionValidatorCount=75
HistoricalPreservationValidatorCount=1
OperationalRecoveryValidatorCount=1
RuntimeQualificationValidatorCount=3
ParentValidatorSubsetCount=6

CurrentLegacyFullMatrixPassCount=79
CurrentLegacyFullMatrixFailCount=1
CurrentLegacyFirstFailureOrdinal=56

LegacyFailFastPassCount=56
LegacyFailFastFailureCount=1
LegacyFailFastNotExecutedTailCount=23

FrozenSourceBoundTranslationCount=80
StaleBindingCount=0

PythonProcessSpawnCount=0
PowerShellProcessSpawnCount=0
CargoProcessSpawnCount=0
ProductionAuthorityClaimed=False

StructuralGate104Migration=False
CargoCompileAuthorityMigration=False
ReceiptProducerMigration=False
SourceTreeDigestAuthorityMigration=False

TrainingMathChanged=False
OptimizerChanged=False
CheckpointChanged=False
RuntimeRouteChanged=False
```

## 35. Completion truth

01B is closed when ASH can represent the exact current CF1 legacy validator set as a deterministic typed Rust graph, including:

```text
81 declared entries,
80 active executions,
1 declared inactive entry,
exact category membership,
exact legacy ordinal ordering,
exact parent subset membership,
exact current known PASS/FAIL baseline,
and source/input identity binding,
```

while the Rust CF1 shadow itself executes no Python, PowerShell, or Cargo subprocess and claims no production authority.

A legacy failure faithfully reproduced by the shadow is parity evidence, not a shadow failure. A stale source/input binding is a shadow failure.

## 36. Explicit limitation and next revision

01B `FrozenSourceBound` does not yet prove that Rust independently evaluates every semantic clause implemented by all 80 Python validators. It proves a narrower, fail-closed statement for exact bound validator revisions and exact bound source surfaces.

Before Python retirement, the next natural subrevision is:

```text
ASH-CONTROL-RUNTIME-CF1-SEMANTIC-CHECK-PROJECTION-01B-R1
```

It replaces frozen disposition replay node-by-node with typed Rust checks such as:

```text
TextContains / TextAbsent
Section checks
Token ordering
Occurrence count
Regex
Structured JSON
SHA256
Registry relation checks
Rust-local Python syntax parsing
```

while retaining the 01B registry identity, source provenance, negative fixtures, and current known legacy failure baseline.

After 01B-R1 semantic parity is closed, the next major authority surface is:

```text
ASH-CONTROL-RUNTIME-CF1-STRUCTURAL-GATE-ADOPTION-01C
```

for the separate 104 structural-gate contract.
