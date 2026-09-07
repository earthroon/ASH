# ASH-BASE-TRAIN-P1B-R1A2-R1A-REQUIRED-PACKAGE-METADATA-PROJECTION

## REQUIRED-PACKAGE METADATA PROJECTION
## + BIN-ONLY WORKSPACE MEMBER EXCLUSION
## + EXACT THREE-PACKAGE LIB TARGET AUTHORITY
## + PRE-RECEIPT FAILURE DIAGNOSTIC CLOSURE
## + RUST-ONLY OBSERVER REPAIR

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-P1B-R1A2-R1A-REQUIRED-PACKAGE-METADATA-PROJECTION

Short name:
P1B-R1A2-R1A

Class:
OBSERVER METADATA AUTHORITY REPAIR
WORKSPACE PACKAGE SCOPE REPAIR
LIB TARGET CARDINALITY REPAIR
PRE-RECEIPT FAILURE DIAGNOSTIC CLOSURE
RUST-ONLY
DIAGNOSTIC ONLY
NO PRODUCTION RUNTIME CHANGE

Direct code parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A2_R1_E0382_FLATTENED_MOVE_COMPILEFIX_CODE_ONLY.zip
```

---

# 1. Authoritative Parent Failure

User-side execution reached the new R1A2-R1 source/binary line but the observer process terminated with:

```text
exit code = 4
```

In the parent observer this means:

```text
observe_current_production_suite(...)
    returned Err
    before paired receipt derivation
```

Therefore no E0275 paired promotion is admitted from that run.

---

# 2. Confirmed Metadata Scope Defect

The parent metadata resolver iterates all Cargo metadata packages and requires each package to expose exactly one library-compatible target.

The source tree contains legitimate bin-only packages including:

```text
ash_p1a_trait_probe
ash_p1br1a2_release_observer
asr_sidecar
native_host
```

Therefore:

```text
workspace/package graph membership
!=
release-observation lib-target authority
```

The workspace-wide lib-target requirement is invalid.

---

# 3. Required Observation Packages

The CurrentProduction paired suite requires exact identities only for:

```text
burn-wgpu-local
burn_webgpu_backend
base_train
```

Materialized enum:

```text
P1bR1a2R1aRequiredPackage
    BurnWgpuLocal
    BurnWebgpuBackend
    BaseTrain
```

and explicit required-package lookup table.

No arbitrary required package vector is promotion authority.

---

# 4. Full Metadata Graph + Required Projection

The originally proposed `cargo metadata --no-deps` authority is repaired.

`burn-wgpu-local` is not a root workspace member in the supplied source tree; it is a path dependency reachable from the workspace graph.

Therefore R1A2-R1A executes:

```text
cargo metadata --format-version 1
```

without `--no-deps`, then projects the full metadata graph onto exactly the three required package names.

This preserves exact package authority while excluding unrelated registry/path/bin packages from semantic projection.

---

# 5. Required Package Projection Law

For every metadata package:

```text
package.name matches required lookup
    -> parse exact package identity and exact library target

package.name is not required
    -> ignore for release-observation lib authority
```

A non-required bin-only package is not an error.

Malformed Cargo metadata remains fail-closed.

---

# 6. Required Package Cardinality

For each required role:

```text
0 matching packages
    -> MissingRequiredPackage

1 matching package
    -> candidate

>1 matching packages
    -> DuplicateRequiredPackage
```

No first-match fallback.

---

# 7. Required Lib Target Cardinality

Within each required package, library-compatible target cardinality must be exactly one.

```text
0
    -> MissingRequiredLibTarget

1
    -> admitted

>1
    -> AmbiguousRequiredLibTarget
```

`bin`, `example`, `test`, `bench`, and `custom-build` are not substitutes for a required lib target.

---

# 8. Projection Identity

`P1bR1a2R1WorkspaceMetadataIdentity` now separates:

```text
metadata_stdout_sha256
required_projection_sha256
metadata_identity_sha256
```

`metadata_stdout_sha256` binds the full Cargo metadata output.

`required_projection_sha256` binds only the exact projected identities of:

```text
burn-wgpu-local
burn_webgpu_backend
base_train
```

`metadata_identity_sha256` is the promotion-facing projection identity for compatibility with existing observer call sites.

Unrelated workspace/dependency package additions do not change the semantic projection digest unless one required package identity changes.

---

# 9. Required Package Identity

Each projected package binds:

```text
package id
package name
manifest path
library target name
library target kind vector
crate types
library target source path
```

Cargo compiler-message matching remains exact package-ID/target identity matching.

Substring matching remains retired.

---

# 10. Pre-Receipt Failure Authority

Materialized typed failure stages:

```text
WorkspaceResolution
CargoMetadataExecution
CargoMetadataParsing
RequiredPackageProjection
ToolchainIdentity
SourceIdentity
SuiteObservation
ReceiptDerivation
```

Materialized reasons include:

```text
CargoMetadataSpawnFailed
CargoMetadataExitFailed
CargoMetadataInvalidJson
MissingRequiredPackage
DuplicateRequiredPackage
MissingRequiredLibTarget
AmbiguousRequiredLibTarget
RequiredPackageMetadataInvalid
MetadataMalformed
SourceIdentityFailed
ToolchainIdentityFailed
ObservationFailed
Other
```

Exit code 4 is no longer an opaque number.

---

# 11. Pre-Receipt Rendering

On pre-receipt failure the observer prints:

```text
[P1B-R1A2-R1A-PRE-RECEIPT-FAIL]
stage=<typed stage>
reason=<typed reason>
package=<required package when applicable>
detail=<diagnostic detail>
```

No external parser is required.

---

# 12. Runtime Revision Identity

Successful receipt rendering header is advanced to:

```text
[P1B-R1A2-R1A]
```

Observation and suite schema identities are advanced to:

```text
P1B-R1A2-R1A
```

This provides a direct stale-binary witness.

---

# 13. Existing R1A2-R1 Laws Preserved

R1A2-R1A does not change:

```text
exact compiler-message package/target matching
failure target admission via compiler-message
successful BuildPass artifact requirement
JSON-vs-auxiliary stdout framing
InvalidSlice precedence
canonical E0275 fingerprint threshold
paired CurrentProduction promotion matrix
```

---

# 14. Canonical Paired Promotion Law

Final promotion remains:

```text
burn-wgpu-local             = BuildPass
burn_webgpu_backend         = BuildPass
CanonicalBaseline           = SameE0275
BisectControl               = SameE0275
CurrentProductionCut        = BuildPass
source stable
toolchain stable
environment stable
required metadata projection stable
```

Only then:

```text
CurrentProductionClosureRequired
```

---

# 15. Rust-Side Regression Fixtures

Materialized tests include:

```text
required 3 lib packages + observer/probe bin-only members
    -> projection succeeds

unrelated bin-only members added/removed
    -> required projection digest stable

missing base_train
    -> MissingRequiredPackage(BaseTrain)

exact package ID rejects overlapping package name
```

These are Rust tests, not external Python/PowerShell validators.

---

# 16. Branch Style

New/modified observer code introduces:

```text
new if tokens = 0
```

State selection is match/enum/lookup driven.

---

# 17. Production Non-Goals

R1A2-R1A modifies no production source under:

```text
crates/base_train/src/**
crates/burn_webgpu_backend/src/**
vendor_fork_scaffold/burn-wgpu-local/src/**
```

No changes to:

```text
optimizer math
Adam / HiMuon state
MCU ownership
WGPU Device/Queue authority
Soft Matrix
R3C / R3C1
Atlas runtime
checkpoint format
kernel code
```

No:

```text
unsafe impl Send
unsafe impl Sync
Arc<Mutex> conversion
recursion_limit increase
```

is introduced.

---

# 18. Actual Source Delta

Relative to the E0382 compilefix parent:

```text
ADD 0
MOD 4
DEL 0
```

Modified:

```text
crates/ash_p1br1a2_release_observer/src/metadata.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/receipt.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
```

No Cargo feature, dependency, workspace, lockfile, or production source change is required.

---

# 19. Static Qualification Actually Executed

Bake-side source/static checks:

```text
source delta MOD4 only                    PASS
production source delta                   0
new `if` tokens in changed Rust files     0
balanced {} / () / [] counts              PASS
required package enum                     PRESENT
required 3-package lookup                 PRESENT
workspace-wide lib requirement            RETIRED
full metadata graph projection            PRESENT
typed pre-receipt stage/reason             PRESENT
R1A2-R1A runtime header                   PRESENT
old exact R1A2-R1 runtime header           ABSENT
```

These are SOURCE/STATIC checks only.

---

# 20. Toolchain Qualification Boundary

Bake environment exposes no usable Cargo/rustc toolchain.

Therefore:

```text
observer compile       NOT RUN
observer Rust tests    NOT RUN
paired release suite   NOT RUN
base_train release     NOT RUN IN BAKE ENVIRONMENT
```

No COMPILE/RELEASE PASS is claimed.

---

# 21. ZIP Packaging Law

Both code ZIPs exclude generated:

```text
specs/
docs/
artifacts/
target/
PowerShell loaders
runtime receipt output
```

No Python loader or PowerShell loader is added.

The specification is committed separately to GitHub.

---

# 22. Bake Artifacts

Overlay code-only:

```text
ASH_BASE_TRAIN_P1B_R1A2_R1A_REQUIRED_PACKAGE_METADATA_PROJECTION_OVERLAY_CODE_ONLY.zip
SHA-256: e497c5476ab5c980e87e01c78bf76667572bee30c93f9ae35c8104889e8b063f
Bytes: 13,375
Files: 4
CRC: PASS
```

Full applied code-only:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A2_R1A_REQUIRED_PACKAGE_METADATA_PROJECTION_CODE_ONLY.zip
SHA-256: 18da61d71fe3b1a309be2bafa54b3d0fd04903958bf4984713a63168932af9ff
Bytes: 21,519,512
Files: 8,432
CRC: PASS
```

Forbidden path counts:

```text
specs/      0
docs/       0
artifacts/  0
target/     0
.ps1        0
```

---

# 23. User-Side Qualification

First compile/test gate:

```powershell
cargo clean -p ash_p1br1a2_release_observer
cargo test -p ash_p1br1a2_release_observer --release
```

Then rebuild observer:

```powershell
cargo build -p ash_p1br1a2_release_observer --release
```

Binary revision witness must contain:

```text
[P1B-R1A2-R1A]
```

Then run:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-production
```

---

# 24. Expected Result Boundary

Current external evidence supports the expectation:

```text
burn-wgpu-local=BuildPass
burn_webgpu_backend=BuildPass
canonical-baseline=SameE0275
bisect-control=SameE0275
current-production-cut=BuildPass
paired-status=CurrentProductionClosureRequired
```

This is not pre-promoted.

If exit code 4 remains, R1A2-R1A must now print exact `stage/reason/package` evidence.

---

# 25. Completion Law

Source completion requires:

```text
required package projection over exact 3 package roles
non-required bin-only packages excluded from lib authority
required packages fail closed on missing/duplicate/ambiguous state
full metadata graph used so path dependency burn-wgpu-local is observable
projection digest separated from full metadata stdout digest
pre-receipt failure is typed and rendered
runtime header advanced to R1A2-R1A
production source unchanged
no external loader added
```

Release completion remains dependent on user-side observer execution.

---

# 26. Stop Law

When the repaired observer emits:

```text
paired-status=CurrentProductionClosureRequired
```

stop metadata/parser repair.

Next revision:

```text
P1B-R1A3
CURRENT PRODUCTION INTERNAL CLASSIFICATION
+ MCU / MUON / SCHEDULER DEPENDENCY-CLOSED SUBCUTS
+ SHAREDCORE MATERIALIZATION
```

---

# 27. Final Law

> Workspace/dependency graph membership does not imply release-observation lib-target authority.
>
> R1A2-R1A reads the full Cargo metadata graph because `burn-wgpu-local` is a path dependency rather than a root workspace member, then projects that graph onto exactly three required package roles.
>
> Bin-only observers, probes, sidecars and hosts cannot abort required-package projection merely because they expose no library target.
>
> Required packages remain fail-closed: missing package, duplicate package, missing lib target and ambiguous lib target all stop observation.
>
> Exit code 4 is no longer opaque. The observer exposes typed pre-receipt stage and reason.
>
> R1A2-R1A repairs metadata authority only. Production training/runtime semantics remain unchanged.
