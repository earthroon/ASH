# ASH-CONTROL-RUNTIME-CF1-CONTRACT-EXTRACTION-01A

## Status

```text
Patch ID: ASH-CONTROL-RUNTIME-CF1-CONTRACT-EXTRACTION-01A
Parent: ASH-CONTROL-RUNTIME-BOOTSTRAP-AUTHORITY-01
Role: CF1 compile-contract ownership extraction
Production authority migration: false
CF1 producer migration: false
Training math change: none
Optimizer change: none
Checkpoint change: none
Inference route change: none
```

## Authority declaration

```text
CF1 Compile Contract Ownership Extraction /
BaseTrain Contract Ownership Retirement /

Ash-Core Shared Contract SSOT /
Producer / Consumer Neutral Contract /

Existing CF1 Compile Receipt V2 Exact Preservation /
Existing JSON Field Shape Preservation /
Existing Validation Semantics Preservation /
Existing Failure Token Preservation /

Cf1BuildProfile Extraction /
CF1 Compile Identity Constant Extraction /
CF1 Structural Gate Count Authority Extraction /
CF1 Compile Receipt Load / Validate Extraction /

BaseTrain Shared-Contract Adoption /
Control Runtime Shared-Contract Adoption /
Legacy BaseTrain Re-Export Compatibility /

No Duplicate Contract Definition /
No Competing Receipt Schema /

Debug Diagnostic Semantics Preserved /
Release Production Requirement Preserved /
No Release-Only Rebind Yet /

Legacy Validator Locator Rebind Only /
No Legacy Validator Semantic Rewrite /

No CF1 Typed Validation Graph Migration /
No 104-Gate Implementation Migration /
No Cargo Compile Authority Migration /
No Receipt Producer Migration /
No Source Digest Authority Migration /

No Python Runtime Retirement Yet /
No PowerShell Runtime Retirement Yet /

No Training Math Change /
No Optimizer Change /
No Checkpoint Change /
No Runtime Evidence Change /
No Production Authority Change
```

## 1. Problem

Before 01A, the CF1 compile contract is defined inside:

```text
crates/base_train/src/subgroup32_tiled_segment_gradient_accumulator_adamw.rs
```

That file owns both training/runtime implementation contracts and the compile-control contract. This makes a future `ash_control_runtime` producer depend on `base_train`, violating CONTROL-01 bootstrap isolation.

01A removes only this ownership inversion.

## 2. Core SSOT after 01A

```text
ash_core::cf1_compile_contract
= CF1 compile contract SSOT

base_train
= training/runtime consumer

ash_control_runtime
= future producer-side consumer, not producer yet

legacy PowerShell CF1 chain
= current physical receipt producer
```

Contract ownership and production authority are separate.

## 3. New shared module

Canonical module:

```text
crates/ash_core/src/cf1_compile_contract.rs
```

Export through `ash_core/src/lib.rs`:

```rust
pub mod cf1_compile_contract;
pub use cf1_compile_contract::*;
```

No new `ash_contracts` crate is introduced in 01A.

## 4. Extracted contract authority

The following canonical definitions move to `ash_core`:

```text
Cf1BuildProfile
R6AR2R2CF1CompileReceipt

R1J_R6A_R2_R2_CF1_PATCH_ID
R1J_R6A_R2_R2_CF1_BUILD_REVISION

CF1_RELEASE_PROFILE_AUTHORITY_PATCH_ID
CF1_RELEASE_PROFILE_AUTHORITY_BUILD_REVISION
CF1_COMPILE_RECEIPT_SCHEMA_V2
CF1_RELEASE_PROFILE_COMPILE_PASS_TOKEN

R6A_R2_R2_CF1_STRUCTURAL_GATES

R6AR2R2CF1CompileReceipt::load
R6AR2R2CF1CompileReceipt::validate
Cf1BuildProfile::as_str
```

## 5. Definitions that remain in base_train

The following remain training/runtime-owned:

```text
R1J_R6A_R2_R2_PATCH_ID
R1J_R6A_R2_R2_BUILD_REVISION
R1J_R6A_R2_R2_PASS_TOKEN
R1J_R6A_R2_R2_HOLD_TOKEN

R6A_R2_R2_GRADIENT_PAGE_BYTES
R6A_R2_R2_SUBGROUP_SIZE
R6A_R2_R2_TILE_ELEMENTS
R6A_R2_R2_ELEMENTS_PER_SUBGROUP_LANE

R6AR2R2Receipt
R6AR2R2CF1Receipt

R1J_R6A_R2_R2_CF1_PASS_TOKEN
R1J_R6A_R2_R2_CF1_HOLD_TOKEN
```

`R6AR2R2CF1Receipt` remains in `base_train` because it combines compile identity with measured training-runtime evidence.

## 6. Single-definition invariant

Repository-wide canonical definition counts:

```text
pub struct R6AR2R2CF1CompileReceipt = 1
pub enum Cf1BuildProfile = 1
pub const CF1_COMPILE_RECEIPT_SCHEMA_V2 = 1
pub const R6A_R2_R2_CF1_STRUCTURAL_GATES = 1
```

All four canonical definitions live in `ash_core::cf1_compile_contract`.

## 7. BaseTrain compatibility facade

`base_train` may preserve its previous public path through a re-export:

```rust
pub use ash_core::{
    Cf1BuildProfile,
    R6AR2R2CF1CompileReceipt,
    ...
};
```

```text
re-export != ownership
```

A second struct, enum, schema constant, adapter DTO, or serde bridge is forbidden.

## 8. Cross-crate type identity

These paths must denote the same Rust type:

```text
ash_core::R6AR2R2CF1CompileReceipt
base_train::R6AR2R2CF1CompileReceipt
```

No conversion layer is permitted between them.

## 9. Compile Receipt V2 exact preservation

Schema remains exactly:

```text
ash.basetrain.r6a_r2_r2_cf1.compile_receipt.v2
```

01A does not create V3.

`R6AR2R2CF1CompileReceipt` retains exactly 23 fields:

```text
schema
patchId
buildRevision
releaseProfileAuthorityPatchId
releaseProfileAuthorityBuildRevision
buildProfile
cargoProfileName
authoritativeBinaryPath
releaseProfileRequiredForProduction
cargoFmtPassed
cargoCheckPassed
targetedTestPassed
baseTrainBinaryBuildPassed
rustCompileErrorCount
sourceTreeDigest
cargoLockDigest
authoritativeBinarySha256
staticValidatorPassCount
staticValidatorFailureCount
parentValidatorPassCount
parentValidatorFailureCount
structuralGateCount
hardcodedRuntimeEvidenceFieldCount
```

No field addition, deletion, rename, or reinterpretation occurs in 01A.

## 10. Serde ABI preservation

Receipt struct remains:

```rust
#[serde(rename_all = "camelCase")]
```

Build profile remains:

```rust
#[serde(rename_all = "lowercase")]
```

Canonical values remain `debug` and `release`.

## 11. Build profile semantics

`Cf1BuildProfile` remains:

```text
Debug
Release
```

Debug remains a valid diagnostic compile-receipt profile.
Release remains required by existing production consumers.
01A does not collapse the enum to Release-only.

Debug validation remains:

```text
cargoProfileName = dev
authoritativeBinaryPath starts with target/debug/
```

Release validation remains:

```text
cargoProfileName = release
authoritativeBinaryPath starts with target/release/
```

## 12. Compile validation semantics preservation

The existing V2 validation continues to require:

```text
schema identity exact
patch identity exact
build revision exact
release-profile authority identity exact
release-profile production policy present
cargo fmt passed
cargo check passed
targeted test passed
base_train binary build passed
rust compile error count = 0
source tree digest non-empty
Cargo.lock digest non-empty
authoritative binary SHA non-empty
static validator failures = 0
parent validator failures = 0
structural gate count = 104
hardcoded runtime evidence field count = 0
```

No stronger digest, path, or publication semantics are added in 01A.

## 13. Failure-token preservation

The following legacy failure identities remain unchanged:

```text
R6AR2R2CF1CompileReceiptSchema
R6AR2R2CF1CompileReceiptPatch
R6AR2R2CF1CompileReceiptBuildRevision
R6AR2R2CF1ReleaseProfileAuthorityIdentity
R6AR2R2CF1ReleaseProfileProductionPolicyMissing
R6AR2R2CF1DebugCargoProfile
R6AR2R2CF1DebugBinaryPath
R6AR2R2CF1ReleaseCargoProfile
R6AR2R2CF1ReleaseBinaryPath
R6AR2R2CF1CompileChainIncomplete
R6AR2R2CF1CompileErrorsPresent
R6AR2R2CF1CompileIdentityMissing
R6AR2R2CF1StaticValidationFailed
R6AR2R2CF1StructuralGateCountDrift
R6AR2R2CF1HardcodedRuntimeEvidenceStaticFailure
```

## 14. Loader preservation

Canonical loader remains:

```rust
R6AR2R2CF1CompileReceipt::load(path)
```

Semantics remain:

```text
read bytes
-> serde_json parse
-> validate
-> return validated receipt
```

No second loader is introduced.

## 15. Shared module boundary

The shared module may:

```text
represent
parse
validate
```

It may not:

```text
spawn cargo
build base_train
publish production receipt
resolve workspace
run validators
```

## 16. BaseTrain direct adoption

Compile-contract consumers should import the shared type directly from `ash_core` where practical.

Primary surfaces:

```text
base_train/src/bin/base_train.rs
base_train/src/pipeline.rs
base_train/src/ram36_process_budget.rs
base_train/src/n8_ram_resident_adam_mv_resume_cut.rs
base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Parent training/runtime types continue to come from `base_train`.

## 17. Orchestrator contract adoption

Where `orchestrator_local` needs only shared compile identity/cardinality constants, it may import them directly from `ash_core`.

Terminal CF1 PASS/HOLD tokens remain imported from `base_train` in 01A.

This is contract ownership cleanup, not orchestrator authority retirement.

## 18. Control Runtime adoption

`ash_control_runtime` must be able to construct and validate a CF1 V2 test fixture using only `ash_core`.

It must not acquire a direct dependency on `base_train`.

Required proof:

```text
control_runtime_can_validate_cf1_without_base_train_dependency
```

## 19. No CF1 producer route yet

Forbidden in 01A:

```text
ash_control_runtime cf1-build
ash_control_runtime cf1-release
production CF1 receipt publication from Rust control runtime
```

Fixture construction in tests is allowed.

## 20. 104-gate boundary

Only this contract value moves:

```text
R6A_R2_R2_CF1_STRUCTURAL_GATES = 104
```

The physical 104-gate implementation, CLI arg sequence, and validator graph do not move in 01A.

```text
cardinality contract != gate implementation
```

## 21. Legacy validator source-locator rebind

Current legacy validators contain source-location assumptions that point directly at the old `base_train` contract file.
A pure contract extraction makes those location checks stale.

01A therefore permits one narrow compatibility edit:

```text
legacy validator source path
base_train CF1 contract location
    -> ash_core::cf1_compile_contract location
```

Only locator ownership may change.

Forbidden:

```text
validator check removal
validator PASS weakening
validator failure swallowing
new fallback behavior
Python validator retirement
validator semantic migration to Rust
fake Rust string/comment compatibility sentinels
```

## 22. Legacy validator preservation

The existing CF1 compile-chain validator continues to verify the same CF1 patch identity and structural-gate cardinality, but reads those contract values from the new shared source file.
All other checks remain unchanged.

The existing release-profile validator reads compile-contract identity/profile definitions from `ash_core` after 01A. Its no-training-math-rewrite marker continues to inspect the actual training implementation file in `base_train`.

## 23. PowerShell producer preservation

The current CF1 PowerShell compile chain is not modified by 01A.

Required closure:

```text
PowerShell producer before SHA256
=
PowerShell producer after SHA256
```

## 24. Python authority state

Python CF1 validators remain runtime authority in the legacy chain after 01A.

```text
PythonAuthorityRetired = false
```

The source-locator rebind does not constitute retirement or Rust adoption.

## 25. Production runtime preservation

Existing runtime route remains:

```text
compile receipt path
-> R6AR2R2CF1CompileReceipt::load
-> production Release profile gate
-> current_exe SHA256
-> receipt authoritativeBinarySha256
-> exact binary identity gate
```

01A changes type ownership, not runtime meaning.

## 26. Terminal runtime receipt preservation

`R6AR2R2CF1Receipt` remains a `base_train` type.
Its measured-runtime checks, binary-identity checks, structural count checks, PASS/HOLD tokens, and proof ledger remain unchanged.

## 27. No V2 semantic expansion

01A does not add:

```text
receiptHash
validationGraphDigest
sourceAuthorityManifestDigest
controlRuntimeVersion
64-hex digest enforcement
absolute path normalization
slash normalization
```

Existing non-empty digest and path-prefix rules remain intact.

## 28. Required shared tests

Compile-receipt tests live in `ash_core`:

```text
cf1_compile_receipt_requires_complete_compile_chain
cf1_compile_receipt_rejects_hardcoded_runtime_evidence
cf1_compile_receipt_release_profile_requires_release_path
cf1_compile_receipt_debug_profile_remains_diagnostic_authority
legacy_cf1_v2_release_shape_roundtrips_identically
legacy_cf1_v2_debug_shape_roundtrips_identically
legacy_cf1_v2_invalid_compile_chain_remains_invalid
```

`base_train` retains:

```text
base_train_cf1_type_is_shared_reexport
cf1_terminal_receipt_requires_binary_identity
```

## 29. Static ownership gates

Required:

```text
CF1 compile receipt definition count = 1
Cf1BuildProfile definition count = 1
CF1 schema definition count = 1
CF1 structural gate cardinality definition count = 1

ash_core -> base_train dependency = false
ash_control_runtime -> base_train dependency = false

terminal runtime receipt stays base_train
parent training receipt stays base_train
control runtime has no CF1 producer route
```

## 30. Legacy validator gates

Required after locator rebind:

```text
CF1 compile-chain static validator = PASS
CF1 release-profile static validator = PASS
R6A-R2-R2 parent static validator = PASS
```

No PASS may be achieved through fake Rust string/comment markers.

## 31. Generated-artifact bake policy

Generated runtime evidence is not source-bake material.

Exclude from baked ZIP:

```text
artifacts/
artifact/
target/
__pycache__/
*.pyc
*.pyo
*.sha256
runtime-generated receipt JSON
runtime-generated failure reports
runtime-generated manifest JSON/JSONL
```

Source files whose names contain `manifest` remain included when they are implementation source code.
`Cargo.toml` and `Cargo.lock` are build source/lock authority, not generated runtime manifests.

The 01A spec itself is committed to GitHub and need not be embedded in the baked source ZIP.

## 32. Physical compile gate

When a Rust toolchain is available, intended physical closure is:

```text
cargo fmt --check
cargo check -p ash_core
cargo test -p ash_core cf1
cargo check -p ash_control_runtime
cargo test -p ash_control_runtime
cargo check -p base_train
existing targeted CF1 tests
```

A bake environment without Cargo/rustc must not claim these gates passed.

## 33. Mandatory gates

```text
PASS_CONTROL01A_CF1_CONTRACT_IN_ASH_CORE
PASS_CONTROL01A_SINGLE_CF1_COMPILE_RECEIPT_DEFINITION
PASS_CONTROL01A_SINGLE_CF1_BUILD_PROFILE_DEFINITION
PASS_CONTROL01A_SINGLE_CF1_SCHEMA_AUTHORITY
PASS_CONTROL01A_SINGLE_CF1_STRUCTURAL_GATE_CARDINALITY_AUTHORITY

PASS_CONTROL01A_CF1_V2_FIELD_SHAPE_PRESERVED
PASS_CONTROL01A_CF1_CONSTANT_VALUE_PARITY
PASS_CONTROL01A_CF1_FAILURE_TOKEN_PRESERVED
PASS_CONTROL01A_DEBUG_DIAGNOSTIC_SEMANTICS_PRESERVED
PASS_CONTROL01A_RELEASE_PRODUCTION_POLICY_PRESERVED

PASS_CONTROL01A_BASETRAIN_SHARED_CONTRACT_ADOPTION
PASS_CONTROL01A_CONTROL_RUNTIME_SHARED_CONTRACT_ADOPTION
PASS_CONTROL01A_BASETRAIN_COMPATIBILITY_REEXPORT

PASS_CONTROL01A_TERMINAL_RUNTIME_RECEIPT_STAYS_BASETRAIN
PASS_CONTROL01A_PARENT_TRAINING_RECEIPT_STAYS_BASETRAIN

PASS_CONTROL01A_NO_BASETRAIN_DEPENDENCY_FROM_ASH_CORE
PASS_CONTROL01A_NO_BASETRAIN_DEPENDENCY_FROM_CONTROL_RUNTIME
PASS_CONTROL01A_NO_CF1_PRODUCER_ROUTE_IN_CONTROL_RUNTIME

PASS_CONTROL01A_LEGACY_VALIDATOR_LOCATOR_REBIND_ONLY
PASS_CONTROL01A_LEGACY_VALIDATOR_SEMANTICS_PRESERVED
PASS_CONTROL01A_POWERSHELL_PRODUCER_BYTE_IDENTITY

PASS_CONTROL01A_NO_TYPED_CF1_GRAPH_MIGRATION
PASS_CONTROL01A_NO_104_GATE_IMPLEMENTATION_MIGRATION
PASS_CONTROL01A_NO_CARGO_COMPILE_AUTHORITY_MIGRATION
PASS_CONTROL01A_NO_RECEIPT_PRODUCER_MIGRATION

PASS_CONTROL01A_NO_TRAINING_MATH_CHANGE
PASS_CONTROL01A_NO_OPTIMIZER_CHANGE
PASS_CONTROL01A_NO_CHECKPOINT_CHANGE
PASS_CONTROL01A_NO_RUNTIME_ROUTE_CHANGE
```

## 34. Completion truth

01A is closed when:

```text
CF1 compile receipt representation,
profile identity,
compile identity constants,
structural gate cardinality,
and V2 load/validation semantics

have exactly one producer-neutral definition in ash_core;

base_train consumes the shared type while retaining only
training/runtime-specific receipt authority;

ash_control_runtime can understand the CF1 contract without
linking base_train;

legacy CF1 validators still make the same decisions after only
source-locator rebinding;

and the existing PowerShell receipt producer remains physically unchanged.
```

01A does not mean:

```text
CF1 Rust compile authority promoted
Python validators retired
PowerShell retired
104 gates migrated
Rust receipt producer active
```

## 35. Next revision

```text
ASH-CONTROL-RUNTIME-CF1-TYPED-VALIDATION-GRAPH-01B
```

01B maps the current legacy validator semantics into a typed deterministic Rust validation graph in shadow mode while leaving the legacy CF1 chain as physical authority until parity is proven.
