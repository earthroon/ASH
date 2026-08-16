# `ASH-BASETRAIN-CF1-RELEASE-PROFILE-AUTHORITY-REBIND-R1`

## CF1 Release Build Authority / Exact Release Executable Identity / Production RAM Inventory Release Closure

---

## 0. Status

| Item | Authority |
|---|---|
| Patch ID | `ASH-BASETRAIN-CF1-RELEASE-PROFILE-AUTHORITY-REBIND-R1` |
| Parent | `ASH-BASETRAIN-BT-WGSL-R6A-R2-R2-CF1-COMPILE-CHAIN-AND-MEASURED-RECEIPT-CLOSURE` |
| Compile receipt schema | `ash.basetrain.r6a_r2_r2_cf1.compile_receipt.v2` |
| Production build profile | `release` |
| Production binary | `target/release/base_train.exe` on Windows |
| Debug profile | preserved as diagnostic/development authority |
| Production RAM inventory | Release profile required |
| Training math change | forbidden |
| Optimizer math change | forbidden |
| Checkpoint rewrite | forbidden |
| Receipt-to-state synthesis | forbidden |

```text
CF1 Release Build Authority /
cargo build --release /
target\release\base_train.exe Exact SHA256 /

Release Runtime Binary Exact Match /
Explicit Build-Profile Identity /
No Debug-to-Release Receipt Reuse /
No Release-to-Debug Receipt Reuse /

Existing CF1 Static Chain Preservation /
Existing Parent Validator Preservation /
Existing Subgroup32 Physical Authority Preservation /
Existing WGPU Feature Admission Preservation /

Existing Gradient Observation Authority Preservation /
Existing Segment AdamW Authority Preservation /
Existing Readback Accounting Preservation /

Production RAM Inventory Release Requirement /
RAM Inventory Receipt Runtime-Binary Binding /
Release Process-Memory Observation Authority /

No Training Math Change /
No Optimizer Math Change /
No Gradient Math Change /
No Adam State Migration /
No Checkpoint State Rewrite /
No Receipt-to-State Synthesis /

No Silent Build-Profile Fallback /
No Silent Debug Runtime Admission /
No Cargo-Run Runtime Substitution /

CF1 Production Release Authority Closure
```

---

## 1. Problem boundary

The original CF1 compile authority seals the exact executable, not only the source tree. Its prior production command built and sealed the debug binary. Running a release executable against a debug receipt must therefore fail with exact binary identity mismatch.

This revision does not weaken that gate. It makes the build profile an explicit authority and allows the same compile chain to seal either Debug or Release, while requiring Release for production RAM inventory.

```text
same source tree
!=
same executable bytes
```

---

## 2. Build profile authority

Canonical Rust authority:

```rust
pub enum Cf1BuildProfile {
    Debug,
    Release,
}
```

Canonical serialized values:

```text
debug
release
```

No build profile is inferred from a binary timestamp, file size, previous receipt, or checkpoint state.

---

## 3. Compile chain profile selection

The existing compile-chain script remains the one compile-chain SSOT:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

It accepts:

```powershell
-BuildProfile Debug
-BuildProfile Release
```

Default Debug is retained for backward-compatible developer diagnostics. Production physical RAM inventory must explicitly request Release.

### Debug build mapping

```text
cargo build --manifest-path crates/base_train/Cargo.toml --bin base_train
→ target/debug/base_train(.exe)
→ cargoProfileName = dev
```

### Release build mapping

```text
cargo build --release --manifest-path crates/base_train/Cargo.toml --bin base_train
→ target/release/base_train(.exe)
→ cargoProfileName = release
```

No second competing release-only compile script is introduced.

---

## 4. Compile receipt V2

The old V1 receipt is not silently reinterpreted as Release.

New schema:

```text
ash.basetrain.r6a_r2_r2_cf1.compile_receipt.v2
```

Required fields include:

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

Release authority identity:

```text
releaseProfileAuthorityPatchId
= ASH-BASETRAIN-CF1-RELEASE-PROFILE-AUTHORITY-REBIND-R1

releaseProfileAuthorityBuildRevision
= cf1-release-profile-authority-rebind-r1
```

---

## 5. Canonical binary path

Receipt canonical path:

```text
Debug   → target/debug/base_train.exe
Release → target/release/base_train.exe
```

The compile script may resolve the physical target directory through `cargo metadata`, but the receipt stores the profile-relative canonical path.

Absolute checkout path is not a cross-machine semantic identity.

---

## 6. Exact binary SHA authority

After successful profile-specific build:

```text
authoritativeBinarySha256
= SHA256(exact built base_train executable bytes)
```

Runtime obtains its own executable through the existing current-executable path and computes the exact file SHA.

Required:

```text
runtimeBinarySha256
==
compileReceipt.authoritativeBinarySha256
```

Mismatch remains fail-closed:

```text
R6AR2R2CF1CompileRuntimeBinaryMismatch
```

No file-size, modified-time, filename-only, or source-only substitution is accepted.

---

## 7. Production RAM inventory Release gate

When:

```text
admit_ram_budget_exact_inventory = true
```

runtime requires:

```text
cf1CompileReceipt.buildProfile = release
```

Otherwise:

```text
R6AR2R2CF1ProductionRamInventoryRequiresReleaseProfile
```

This is deliberately narrower than banning Debug globally. Debug remains usable for development and diagnostic routes that do not claim production RAM authority.

---

## 8. RAM inventory receipt binding

The RAM inventory authority records the CF1 execution binding:

```text
cf1BuildProfile
cf1AuthoritativeBinarySha256
cf1RuntimeBinarySha256
cf1ReleaseBinaryExactMatch
```

For production RAM inventory:

```text
cf1BuildProfile = release
cf1ReleaseBinaryExactMatch = true
```

The binding function fails if:

```text
profile != release
binary digest missing
compile/runtime binary digest mismatch
```

This does not change RAM allocation behavior or the 36 GiB policy. The hard 36 GiB process cap remains a later authority.

---

## 9. Existing CF1 authority preserved

The following remain unchanged in meaning:

```text
104 structural gates
parent static validators
cargo fmt checks
cargo check
CF1 targeted tests
source-tree digest
Cargo.lock digest
physical subgroup32 probe
SHADER_INT64 feature admission
TIMESTAMP_QUERY feature admission
segment-native gradient accumulation
segment AdamW
measured candidate readback accounting
gradient payload readback prohibition
```

The release rebind changes executable profile authority only.

---

## 10. Physical N2 compatibility

Physical N2 promotion parsing accepts both compile receipt schemas:

```text
v1 = historical Debug-era evidence
v2 = explicit profile-aware evidence
```

V1 is not promoted into Release semantics. V2 must contain a valid profile and authoritative binary path.

Existing historical promotion evidence therefore remains readable while all newly generated production RAM inventory evidence uses V2 Release authority.

---

## 11. No checkpoint or optimizer-state rewrite

The following are frozen:

```text
weights
Adam M
Adam V
dataset cursor
scheduler state
generation
optimizer step
packed state manifest
parameter registry
```

A Release compile receipt proves executable provenance. It does not synthesize or migrate training state.

```text
CF1 compile receipt
!=
checkpoint state authority
```

---

## 12. No Cargo-run production substitution

The production execution contract is:

```text
Release compile-chain receipt
→ exact target/release/base_train.exe
→ direct executable launch
```

Do not use a later `cargo run` as the production authority because it can rebuild or select a different executable after receipt creation.

The receipt-bound executable should be launched directly.

---

## 13. Static validators

New validator:

```text
tools/validate_cf1_release_profile_authority_rebind_r1_static.py
```

Required static truths:

```text
release patch identity exists
compile receipt schema V2 exists
explicit Cf1BuildProfile exists
compile script accepts Debug/Release
Release maps to cargo build --release
Debug mapping remains available
binary profile directory is profile-bound
canonical target/release path is emitted
binary SHA runtime bind is preserved
runtime CF1 receipt carries build profile/path
production RAM inventory requires Release
RAM receipt carries compile/runtime release binary binding
no runtime build-profile CLI shadow exists
physical N2 V1/V2 compatibility is explicit
Release compile PASS token exists
training math constants remain untouched
```

Pass token:

```text
PASS_ASH_BASETRAIN_CF1_RELEASE_PROFILE_AUTHORITY_REBIND_R1_STATIC
```

---

## 14. Required Rust tests

CF1 targeted tests include profile-specific receipt semantics:

```text
release profile requires target/release binary path
Debug profile remains valid diagnostic authority
complete compile chain required
hardcoded runtime evidence rejected
terminal binary identity required
```

---

## 15. Compile PASS tokens

Existing compile authority PASS remains:

```text
PASS_ASH_BASETRAIN_BT_WGSL_R6A_R2_R2_CF1_COMPILE_CHAIN_AND_MEASURED_RECEIPT_CLOSURE_COMPILE_AUTHORITY
```

Release profile additionally emits:

```text
PASS_ASH_BASETRAIN_CF1_RELEASE_PROFILE_COMPILE_AUTHORITY_R1
```

---

## 16. Production execution order

```text
current source tree
↓
CF1 static chain
↓
-BuildProfile Release
↓
cargo build --release
↓
target/release/base_train.exe
↓
exact executable SHA256
↓
compile receipt V2
↓
direct exact executable launch
↓
runtime SHA exact match
↓
native WGPU bootstrap
↓
subgroup32 probe
↓
packed state validation
↓
RAM inventory Release binding
↓
Adam M/V hydration
↓
N8 physical run
```

---

## 17. Non-goals

This revision does not introduce:

```text
36 GiB process hard cap
Job Object process memory limit
Adam compression
Adam quantization
parallel Adam hydration
mmap hydration
8 MiB hydration chunk change
dataset streaming rewrite
prefetch reduction
batch geometry change
scheduler change
loss change
gradient formula change
optimizer formula change
checkpoint migration
```

---

## 18. Relationship to RAM36

Production hard-cap work must consume **Release-profile** RAM inventory evidence.

```text
Debug RAM peak
= diagnostic only

Release RAM peak
= production planning authority
```

Natural successor:

```text
ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-36GIB-PROCESS-BUDGET-AUTHORITY-R1
```

The hard cap remains:

```text
36 GiB = 38,654,705,664 bytes
```

but is not enforced by this patch.

---

## 19. Bake policy

Code ZIPs include source/runtime/tooling and required `.args` contract files.

Exclude:

```text
manifest files
artifact directories/files
accumulated Markdown specs
*.sha256
__pycache__
*.pyc
```

The Markdown spec is committed to the ASH GitHub SSOT separately.

---

## 20. Final SSOT

```text
CF1 COMPILE AUTHORITY
= exact executable bytes

PRODUCTION BUILD PROFILE
= Release

PRODUCTION EXECUTABLE
= target/release/base_train.exe

DEBUG EXECUTABLE
= diagnostic/development authority

SOURCE PARITY
!= BINARY IDENTITY

V1 DEBUG RECEIPT
!= RELEASE AUTHORITY

PRODUCTION RAM INVENTORY
= Release process only

CF1 RECEIPT
!= CHECKPOINT STATE

BUILD PROFILE CHANGE
!= TRAINING SEMANTIC CHANGE

NO DEBUG → RELEASE SILENT PROMOTION
NO RECEIPT → STATE SYNTHESIS
NO CARGO-RUN PRODUCTION SUBSTITUTION
NO TRAINING MATH CHANGE
NO OPTIMIZER CHANGE
NO CHECKPOINT REWRITE
```

> **Production CF1 now proves not merely that the source compiled, but that the exact Release executable sealed by the compile receipt is the same executable currently performing the physical run. Production RAM evidence is accepted only from that exact Release process.**
