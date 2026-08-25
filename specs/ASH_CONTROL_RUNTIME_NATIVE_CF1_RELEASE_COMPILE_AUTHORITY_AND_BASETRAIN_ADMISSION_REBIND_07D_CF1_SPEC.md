# ASH-CONTROL-RUNTIME-NATIVE-CF1-RELEASE-COMPILE-AUTHORITY-AND-BASETRAIN-ADMISSION-REBIND-07D-CF1

## 1. Parent and problem statement

Parent runtime revision:

`ASH-CONTROL-RUNTIME-NATIVE-OWNER-PHYSICAL-WITNESS-INVOCATION-07D-B`

07D-B requires the current `base_train` release executable to enter R6/N8 so actual owner-local witness publication can occur. The previous BaseTrain admission still consumed `R6AR2R2CF1CompileReceipt`, whose canonical producer was a PowerShell/Python CF1 chain. Rebuilding `base_train.exe` for 07D-B changed the binary SHA, making the old legacy receipt stale. Regenerating the legacy receipt re-entered retired Python static validators.

Observed blocker:

```text
validate_ram_budget_exact_inventory_r1_static.py
FAIL_RAM_BUDGET_EXACT_INVENTORY_R1_STATIC
pass=66 fail=1
inventory-seed-passed
```

07D-CF1 does not repair that Python validator. It retires that producer from current BaseTrain admission.

## 2. Authority rebind

Before:

```text
PowerShell / Python CF1 producer
    -> R6AR2R2CF1CompileReceipt
    -> BaseTrain R6/RAM36 admission
```

After:

```text
ash_control_runtime
    -> current native registry / contract / DAG / evidence-plan structural closure
    -> cargo build --locked --release -p base_train --bin base_train
    -> exact release binary SHA-256
    -> NativeCF1ReleaseCompileAuthority
    -> BaseTrain R6/RAM36 admission
```

The rebind changes who owns compile admission. It does not create another runtime evidence layer.

## 3. Rust dependency law

Semantic ownership and Rust crate dependencies remain separate.

```text
ash_core
  <- ash_control_runtime
  <- no dependency on base_train

ash_core
  <- base_train
```

Forbidden:

```text
ash_core -> ash_control_runtime
ash_control_runtime -> base_train
base_train -> ash_control_runtime
```

The shared protocol is owned by `ash_core`. The producer is owned by `ash_control_runtime`. BaseTrain consumes only the Core protocol.

## 4. New Core protocols

### 4.1 Compile input manifest

Schema:

`ash.control_runtime.native_cf1_compile_input_manifest.v1`

Fields include:

```text
workspaceManifestDigest
cargoLockDigest
packageManifestDigests
compileInputFileCount
compileInputEntries[path -> sha256]
compileInputManifestDigest
```

Compile input entries are content-addressed and lexically ordered through `BTreeMap`. Filesystem timestamps are not authority.

Current scope includes:

```text
/Cargo.toml
/Cargo.lock
/crates/ash_core/**
/crates/ash_control_runtime/**
/crates/base_train/**
```

Generated runtime roots such as `target`, `artifacts`, `workspace`, and `.git` are excluded when encountered in the compile-input walk.

### 4.2 Native release compile authority

Schema:

`ash.control_runtime.native_cf1_release_compile_authority.v1`

Patch identity:

`ASH-CONTROL-RUNTIME-NATIVE-CF1-RELEASE-COMPILE-AUTHORITY-AND-BASETRAIN-ADMISSION-REBIND-07D-CF1`

The authority seals:

```text
compileInputManifestDigest
workspaceManifestDigest
cargoLockDigest
nativeAuthorityRegistryDigest
nativeContractRegistryDigest
nativeInvariantRegistryDigest
nativeAuthorityDagDigest
nativeEvidencePlanRegistryDigest
compileRequiredEvidenceIds
compileRequiredEvidenceCount
compileRequiredEvidenceValidCount
compileRequiredEvidenceMissingCount
compileRequiredEvidenceInvalidCount
cargoBuildExitCode
buildProfile
packageName
binaryName
releaseBinaryRelativePath
releaseBinaryByteLength
releaseBinarySha256
rustcVersion
cargoVersion
targetTriple
featureSet
pythonProcessCount
powershellProcessCount
legacyValidatorExecutionCount
runtimePhysicalEvidenceRequiredCount
productionAuthorityClaimed
receiptHash
```

## 5. Compile authority boundary

Compile authority proves only compile-time structural and binary identity facts.

Required native structural evidence set:

```text
native-authority-registry
native-contract-and-invariant-catalog
native-authority-dag
native-evidence-plan-catalog
```

All four must materialize successfully through the existing Rust-native builders.

The compile authority explicitly requires:

```text
productionInvariantEvidenceExecutionCount=0
runtimePhysicalEvidenceRequiredCount=0
```

Therefore 07D live witness, GPU recovery qualification, training completion, optimizer commit, and production activation are not CF1 compile prerequisites.

This prevents the forbidden cycle:

```text
R6 -> 07D witness -> CF1 -> R6
```

The only supported direction is:

```text
Native CF1 -> BaseTrain admission -> R6 -> 07D witness
```

## 6. Rust-only producer

New control-runtime command:

```text
ash_control_runtime native-cf1-release-compile-authority
```

Canonical build identity is fixed to:

```text
package=base_train
bin=base_train
profile=release
```

The producer invokes only the configured Cargo and rustc executables. It does not execute Python, PowerShell, pwsh, or legacy validator scripts.

Canonical build:

```text
cargo build --locked --release -p base_train --bin base_train
```

`--locked` is mandatory so the input Cargo.lock digest cannot be silently invalidated by the authority-producing build.

## 7. Release binary authority

After a successful Cargo build, the producer requires the release executable to exist and hashes its actual bytes.

Windows canonical path:

```text
target/release/base_train.exe
```

The authority seals both byte length and SHA-256. File existence or pathname alone is insufficient.

## 8. Toolchain identity

The producer records actual:

```text
cargo --version
rustc --version --verbose
rustc host target triple
```

The current feature identity is explicitly recorded as `default`.

## 9. Immutable publication

Default authority root:

```text
artifacts/control_runtime/native_cf1_release_authorities/<receiptHash>/
```

Files:

```text
native_cf1_compile_input_manifest.json
native_cf1_release_compile_authority.json
```

Same path and same bytes is idempotent. Same path with different bytes fails closed. There is no mutable `latest` authority in the admission path.

## 10. BaseTrain admission rebind

New BaseTrain CLI:

```text
--native-cf1-release-authority <PATH>
```

The old flag remains recognized only to provide an explicit retirement error:

```text
--r6a-r2-r2-cf1-compile-receipt
-> E_LEGACY_CF1_COMPILE_RECEIPT_RETIRED
```

There is no automatic legacy fallback.

R6 admission now requires:

```text
native_cf1_release_authority_path != None
```

Missing authority:

```text
E_NATIVE_CF1_RELEASE_AUTHORITY_REQUIRED
```

## 11. Running executable exact-match

BaseTrain loads `NativeCF1ReleaseCompileAuthority` through `ash_core`, validates its receipt hash and structural fields, hashes `std::env::current_exe()`, then requires:

```text
currentExecutableSha256 == authority.releaseBinarySha256
```

Mismatch:

```text
E_NATIVE_CF1_RELEASE_BINARY_IDENTITY_MISMATCH
```

BaseTrain does not recompute the source tree. Source/input identity is the producer's responsibility and is already sealed to the exact release binary authority.

## 12. RAM36 separation

The existing `basetrain_ram_exact_inventory_receipt.json` remains a separate runtime parent authority. 07D-CF1 does not replace it.

RAM exact-inventory proves runtime memory/accounting facts. Native CF1 proves compile and release-binary identity. The two are not conflated.

`HostProcessRamBudget` now consumes `NativeCF1ReleaseCompileAuthority` for release profile and current executable exact-match rather than reading `R6AR2R2CF1CompileReceipt`.

## 13. R6 scheduler rebind

The R6 scheduler also loads the same native release authority and repeats current-executable exact-match at the actual production loop boundary.

The old legacy compile receipt is not read by the current BaseTrain path.

Historical legacy types and fixtures may remain for archived artifact compatibility. They are not current admission authority.

## 14. N8 resume-cut binding

Current N8 resume-cut code accepts `NativeCF1ReleaseCompileAuthority`. Its source identity is bound to `compileInputManifestDigest`, and its binary identity is bound to `releaseBinarySha256`.

This preserves a concrete compile/source identity without reviving Python validator provenance.

## 15. Runtime measured receipt compatibility

The existing R6 runtime CF1 measured receipt filename remains for downstream historical artifact continuity. It no longer imports pass counts from a legacy static validator producer.

Current emission uses:

```text
staticValidatorPassCount=0
staticValidatorFailureCount=0
parentValidatorPassCount=0
parentValidatorFailureCount=0
```

and binds source identity to the native compile-input manifest digest and binary identity to the native release authority.

This is compatibility output, not BaseTrain compile admission authority.

## 16. Expected producer truth

```text
ASH_NATIVE_CF1_RELEASE_COMPILE_AUTHORITY_VALID=true
compileRequiredEvidenceCount=4
compileRequiredEvidenceValidCount=4
compileRequiredEvidenceMissingCount=0
compileRequiredEvidenceInvalidCount=0
cargoBuildExitCode=0
pythonProcessCount=0
powershellProcessCount=0
legacyValidatorExecutionCount=0
runtimePhysicalEvidenceRequiredCount=0
productionAuthorityClaimed=false
```

## 17. Expected BaseTrain admission truth

```text
ASH_BASETRAIN_NATIVE_CF1_ADMISSION_VALID=true
releaseBinaryExactMatch=true
legacyCf1ReceiptReadCount=0
pythonValidatorExecutionCount=0
powershellValidatorExecutionCount=0
```

## 18. Mandatory gates

```text
PASS_07DCF1_CORE_PROTOCOL_OWNERSHIP
PASS_07DCF1_NO_ASH_CORE_TO_CONTROL_RUNTIME_DEPENDENCY
PASS_07DCF1_NO_CONTROL_RUNTIME_TO_BASE_TRAIN_DEPENDENCY
PASS_07DCF1_BASE_TRAIN_CONSUMES_CORE_PROTOCOL_ONLY

PASS_07DCF1_NATIVE_COMPILE_INPUT_MANIFEST
PASS_07DCF1_CARGO_LOCK_BOUND
PASS_07DCF1_WORKSPACE_MANIFEST_BOUND
PASS_07DCF1_COMPILE_SOURCE_CONTENT_BOUND
PASS_07DCF1_NO_MTIME_AUTHORITY

PASS_07DCF1_NATIVE_AUTHORITY_REGISTRY_BOUND
PASS_07DCF1_NATIVE_CONTRACT_REGISTRY_BOUND
PASS_07DCF1_NATIVE_INVARIANT_REGISTRY_BOUND
PASS_07DCF1_NATIVE_AUTHORITY_DAG_BOUND
PASS_07DCF1_NATIVE_EVIDENCE_PLAN_BOUND

PASS_07DCF1_COMPILE_REQUIRED_EVIDENCE_EXACT_SET
PASS_07DCF1_ZERO_COMPILE_REQUIRED_EVIDENCE_MISSING
PASS_07DCF1_ZERO_COMPILE_REQUIRED_EVIDENCE_INVALID
PASS_07DCF1_ZERO_RUNTIME_EVIDENCE_REQUIRED_FOR_COMPILE
PASS_07DCF1_ZERO_07D_WITNESS_DEPENDENCY

PASS_07DCF1_RELEASE_CARGO_BUILD_LOCKED
PASS_07DCF1_RELEASE_CARGO_BUILD_SUCCESS
PASS_07DCF1_RELEASE_BINARY_EXISTS
PASS_07DCF1_RELEASE_BINARY_SHA256
PASS_07DCF1_RELEASE_BINARY_BYTE_LENGTH
PASS_07DCF1_TOOLCHAIN_IDENTITY_BOUND
PASS_07DCF1_TARGET_IDENTITY_BOUND

PASS_07DCF1_IMMUTABLE_AUTHORITY_PUBLICATION
PASS_07DCF1_RECEIPT_HASH_VALID

PASS_07DCF1_ZERO_PYTHON_PROCESS
PASS_07DCF1_ZERO_POWERSHELL_PROCESS
PASS_07DCF1_ZERO_LEGACY_VALIDATOR_EXECUTION

PASS_07DCF1_BASETRAIN_NATIVE_AUTHORITY_CLI
PASS_07DCF1_BASETRAIN_RUNNING_BINARY_SHA_EXACT_MATCH
PASS_07DCF1_ZERO_LEGACY_CF1_RECEIPT_READ
PASS_07DCF1_ZERO_LEGACY_CF1_FALLBACK
PASS_07DCF1_LEGACY_FLAG_EXPLICITLY_RETIRED

PASS_07DCF1_RAM_RUNTIME_AUTHORITY_NOT_CONFLATED_WITH_CF1
PASS_07DCF1_R6_ADMISSION_NATIVE_REBOUND
PASS_07DCF1_COMPILE_AUTHORITY_RUNTIME_EVIDENCE_SEPARATION
PASS_07DCF1_PRODUCTION_AUTHORITY_FALSE
```

## 19. Explicit non-goals

```text
No Python validator repair
No PowerShell CF1 repair
No manual legacy receipt SHA patch
No fake legacy pass-count parity
No 07D 27/27 requirement for compile authority
No GPU physical qualification in compile authority
No training execution in compile authority
No checkpoint mutation
No production activation
No production authority claim
```

## 20. Completion truth

Before 07D-CF1, Rust-native CF1 existed but BaseTrain still consumed a legacy CF1 compile receipt produced by the retired script chain. Rebuilding BaseTrain for 07D-B therefore invalidated the old receipt and forced the workflow back into Python validation.

After 07D-CF1, `ash_control_runtime` directly materializes a Rust-native release compile authority, binds the current source/input manifest and native structural authority graph to an actual `base_train` release executable, and seals that executable's exact SHA-256. BaseTrain consumes that authority through `ash_core`, rejects the old compile-receipt flag, and requires its currently running executable to match the sealed release binary exactly.

07D physical witness remains downstream. Production authority remains false.
