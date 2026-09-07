# ASH-BASE-TRAIN-FAIL-CLOSED-RELEASE-OBSERVATION-RECEIPT-AUTHORITY-P1B-R1A2

## FAIL-CLOSED RELEASE OBSERVATION
## + RECEIPT AUTHORITY CLOSURE
## + SAME-SOURCE PAIRED CONTROL / CUT OBSERVATION
## + RUST-ONLY OBSERVER

---

# 0. Revision

```text
Patch ID:
ASH-BASE-TRAIN-FAIL-CLOSED-RELEASE-OBSERVATION-RECEIPT-AUTHORITY-P1B-R1A2

Short name:
P1B-R1A2

Class:
RELEASE OBSERVATION AUTHORITY
PAIRED BUILD EVIDENCE CLOSURE
FAIL-CLOSED RECEIPT DERIVATION
DIAGNOSTIC ONLY
RUST-ONLY
NO PRODUCTION RUNTIME SEMANTIC CHANGE

Direct code parent:
ASH_PASS3_BASE_TRAIN_P1B_R1A1_COMPILE_DISCOVERED_TRANSITIVE_CLOSURE_R1_CODE_ONLY.zip
```

---

# 1. Authoritative Input Evidence

User-side release evidence preceding this bake:

```text
NO CUT
cargo build -p base_train --lib --release -j 1
    -> SAME_E0275

CURRENT PRODUCTION CUT
cargo build -p base_train --lib --release -j 1 \
  --no-default-features \
  --features p1br1a-cut-current-production
    -> RELEASE PASS
```

The no-cut canonical fingerprint contains:

```text
error[E0275]
validation::NumericDimension: Sync
ShaderModule
RenderPipeline
BindGroupLayout
BindGroup
Device
Queue
LifetimeTracker
PendingWrites
```

R1A2 does not promote an exact MCU / Muon / scheduler / natural Send-Sync demand site.

---

# 2. Purpose

R1A1 establishes structural slice validity.

R1A2 establishes whether the exact intended release target was observed under the exact source, toolchain, feature plan and process result.

Authority ordering:

```text
SOURCE IDENTITY
-> TOOLCHAIN IDENTITY
-> TYPED OBSERVATION PLAN
-> EXACT CARGO INVOCATION
-> TARGET OBSERVATION
-> PROCESS EXIT STATUS
-> STRUCTURED CARGO/RUSTC DIAGNOSTICS
-> SLICE VALIDITY
-> FINGERPRINT CLASSIFICATION
-> PAIRED CONTROL/TREATMENT RELATION
-> DERIVED PROMOTION STATUS
```

---

# 3. Independent Rust Observer Crate

Added:

```text
crates/ash_p1br1a2_release_observer/
    Cargo.toml
    src/main.rs
    src/observation.rs
    src/fingerprint.rs
    src/source_identity.rs
    src/receipt.rs
```

Package:

```text
ash_p1br1a2_release_observer
```

Workspace policy:

```text
workspace member      = yes
default member        = no
base_train dependency = no
burn backend dependency = no
```

The observer depends only on:

```text
serde
serde_json
sha2
```

This keeps the observer compilable independently of the failing `base_train` release target.

---

# 4. Rust-Only Law

R1A2 adds no:

```text
Python loader
PowerShell loader
shell runner
Node runner
external manifest generator
```

Cargo execution uses:

```rust
std::process::Command
```

Cargo message parsing, source digesting, toolchain identity, classification, receipt derivation and receipt serialization remain Rust-side.

---

# 5. Typed Observation Plans

Materialized:

```text
DependencyBurnWgpuLocal
DependencyBurnWebgpuBackend
CanonicalBaseline
BisectControl
CurrentProductionCut
AtlasCheckpointSupportCut
```

Authoritative plans do not accept an arbitrary feature vector.

---

# 6. Canonical Commands

CanonicalBaseline:

```text
cargo build -p base_train --lib --release -j 1 \
  --message-format=json-render-diagnostics
```

BisectControl:

```text
cargo build -p base_train --lib --release -j 1 \
  --no-default-features \
  --features p1br1a-release-bisect \
  --message-format=json-render-diagnostics
```

CurrentProductionCut:

```text
cargo build -p base_train --lib --release -j 1 \
  --no-default-features \
  --features p1br1a-cut-current-production \
  --message-format=json-render-diagnostics
```

Dependency controls use the same release/lib/jobs/message-format shape.

---

# 7. Paired Control Law

The strong CurrentProduction comparison is:

```text
BisectControl
    SAME_E0275

CurrentProductionCut
    BUILD_PASS
```

The canonical baseline remains a lineage control.

This prevents the `--no-default-features` / diagnostic feature-mode difference from being confused with the actual CurrentProduction cut delta.

---

# 8. Required Promotion Suite

The CurrentProduction promotion suite contains:

```text
1. burn-wgpu-local release control
2. burn_webgpu_backend release control
3. canonical base_train baseline
4. p1br1a-release-bisect control
5. p1br1a-cut-current-production treatment
```

Promotion target matrix:

```text
burn-wgpu-local             BUILD_PASS
burn_webgpu_backend         BUILD_PASS
CanonicalBaseline           SAME_E0275
BisectControl               SAME_E0275
CurrentProductionCut        BUILD_PASS
```

Only the observer may derive the final paired status.

---

# 9. Toolchain Identity

Before and after a suite the observer records:

```text
cargo --version --verbose
rustc -Vv
```

and SHA-256 identities for the resulting process output.

Compiler-affecting environment variables are hashed without storing raw values:

```text
RUSTFLAGS
CARGO_ENCODED_RUSTFLAGS
RUSTC
RUSTC_WRAPPER
RUSTC_WORKSPACE_WRAPPER
CARGO_TARGET_DIR
```

Drift is fail-closed.

---

# 10. Source Identity

The observer computes deterministic SHA-256 identity over sorted source inventory including:

```text
Cargo.toml
Cargo.lock
crates/base_train/**/*.rs + Cargo.toml
crates/burn_webgpu_backend/**/*.rs + Cargo.toml
crates/ash_p1br1a2_release_observer/**/*.rs + Cargo.toml
vendor_fork_scaffold/burn-wgpu-local/**/*.rs + Cargo.toml
```

Each entry contributes:

```text
normalized relative path
byte length
content SHA-256
```

Excluded from source identity:

```text
target/
.git/
docs/
specs/
artifacts/
runtime receipts/logs
```

The source digest is recomputed after the suite. Mismatch yields `HoldSourceDrift`.

---

# 11. Cargo JSON Authority

All plans add:

```text
--message-format=json-render-diagnostics
```

The observer parses structured messages:

```text
compiler-message
compiler-artifact
build-finished
```

Terminal string absence alone is not release authority.

---

# 12. Target Observation

Materialized target observation binds:

```text
intended package
lib target
compiler artifact
artifact freshness
build-finished presence
build-finished success
```

A process exit 0 without the intended lib artifact and successful build-finished observation is not `BuildPass`.

It is fail-closed as `WrongTarget`.

---

# 13. Process Result Authority

Materialized:

```text
ExitSuccess
ExitFailure(code)
TerminatedWithoutCode
SpawnFailure
```

No boolean-only process status is the sole authority.

---

# 14. Release Classification

Materialized:

```text
SameE0275
DifferentE0275
BuildPass
InvalidSlice
WrongTarget
OtherCompilerFailure
SpawnFailure
SourceDrift
ToolchainDrift
Unclassified
```

There is no standalone terminal `E0275Absent` authority.

A clean negative is represented by actual `BuildPass`.

---

# 15. SAME_E0275 Fingerprint

Materialized fingerprint fields:

```text
rustc_code_e0275
numeric_dimension_sync
shader_module
render_pipeline
bind_group_layout
bind_group
device
queue
lifetime_tracker
pending_writes
```

`SameE0275` requires:

```text
E0275
validation::NumericDimension: Sync
ShaderModule
Device
Queue
PendingWrites
and at least one of:
    RenderPipeline
    BindGroupLayout
```

An E0275 without these canonical markers is `DifferentE0275`.

---

# 16. Invalid-Slice Precedence

R1A2 preserves the R1A1 structural law.

For an active cut, structural compiler diagnostics such as:

```text
E0432 / E0433 unresolved crate-local symbol
E0412 missing type
E0425 missing value/function
```

are classified `InvalidSlice` before any E0275-absence inference.

The previous compile-discovered E0432 campaign is therefore represented as invalid evidence, not a successful negative.

---

# 17. Observation Receipt

Materialized sealed receipt:

```text
P1bR1a2ReleaseObservationReceipt
```

It binds:

```text
observation identity
plan
source digest
cargo toolchain digest
rustc toolchain digest
environment digest
invocation digest
process result
target observation
slice validity
release classification
stdout digest
stderr digest
Cargo JSON digest
canonical diagnostic digest
optional E0275 fingerprint
```

Promotion-capable fields are private.

Classification is derived from raw observation and is not accepted from the caller.

---

# 18. Paired Suite Receipt

Materialized:

```text
P1bR1a2PairedReleaseSuiteReceipt
```

It owns all five observation receipts and derives:

```text
Unknown
HoldDependencyBaselineDrift
HoldCanonicalBaselineDrift
HoldBisectControlDrift
HoldSourceDrift
HoldToolchainDrift
HoldEnvironmentDrift
HoldInvalidObservation
CurrentProductionClosureRequired
CurrentProductionCutStillSameE0275
CurrentProductionCutDifferentE0275
Unresolved
```

No `R7Culprit`, `ExactDemandSite`, or equivalent stronger state exists in R1A2.

---

# 19. CurrentProductionClosureRequired Law

This state is derived only when:

```text
both dependency controls = BuildPass
CanonicalBaseline        = SameE0275
BisectControl            = SameE0275
CurrentProductionCut     = BuildPass
source identity          = stable
toolchain identity       = stable
environment identity     = stable
```

Exact meaning:

```text
under one source/toolchain/environment and paired bisect mode,
removing the dependency-closed CurrentProduction closure changes
base_train release compilation from the canonical E0275 to successful build completion
```

It does not identify a specific module or Send/Sync demand site.

---

# 20. Bisect-Control Drift Law

If:

```text
CanonicalBaseline = SameE0275
BisectControl      = BuildPass or another non-canonical result
```

then:

```text
HoldBisectControlDrift
```

No CurrentProduction attribution is allowed because the feature-mode control itself changed the reproducer.

---

# 21. Receipt Output

The observer may serialize its derived typed receipt to:

```text
target/p1br1a2/receipts/<suite-digest>.json
```

This file is output evidence only.

It is never read as an input promotion authority.

Runtime receipt files are not included in code ZIPs.

---

# 22. Human Output

The observer prints a concise rendering:

```text
[P1B-R1A2]
source=<digest>
toolchain=<digest>
environment=<digest>
burn-wgpu-local=<classification>
burn_webgpu_backend=<classification>
canonical-baseline=<classification>
bisect-control=<classification>
current-production-cut=<classification>
paired-status=<derived status>
suite-digest=<digest>
```

This text is a rendering of the sealed typed receipt, not a second authority.

---

# 23. CLI

Build only the observer:

```powershell
cargo build -p ash_p1br1a2_release_observer --release
```

Run the paired suite:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-production
```

No PowerShell logic performs classification.

---

# 24. Branch Style

New observer Rust source uses explicit `match`-based state handling.

The baked observer source contains no new `if` branch token.

No branch maze is used for promotion derivation.

---

# 25. Rust Tests Materialized

The observer contains Rust tests for:

```text
canonical E0275 fingerprint recognition
different E0275 rejection
cut E0432 -> InvalidSlice
typed plan argument distinction
exit success without intended target -> WrongTarget
structural failure precedence
SAME/SAME/PASS -> CurrentProductionClosureRequired
BisectControl PASS -> HoldBisectControlDrift
source drift -> HoldSourceDrift
treatment SAME_E0275 -> unpromoted same-E0275 state
promotion taxonomy contains no exact R7/demand-site claim
```

These tests are materialized in source.

---

# 26. Production Non-Goals

R1A2 modifies no production source under:

```text
crates/base_train/src
crates/burn_webgpu_backend/src
vendor_fork_scaffold/burn-wgpu-local/src
```

No change to:

```text
optimizer math
Adam / HiMuon state
MCU session ownership
Rc<RefCell>
WGPU Device/Queue authority
Soft Tensor Matrix
R3C/R3C1 commit semantics
Atlas execution
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

# 27. Actual Source Delta

Relative to the supplied R1A1-R1 parent:

```text
ADD 6
MOD 2
DEL 0
```

Added:

```text
crates/ash_p1br1a2_release_observer/Cargo.toml
crates/ash_p1br1a2_release_observer/src/fingerprint.rs
crates/ash_p1br1a2_release_observer/src/main.rs
crates/ash_p1br1a2_release_observer/src/observation.rs
crates/ash_p1br1a2_release_observer/src/receipt.rs
crates/ash_p1br1a2_release_observer/src/source_identity.rs
```

Modified:

```text
Cargo.toml
Cargo.lock
```

`Cargo.toml` adds the observer to workspace members only, not default-members.

`Cargo.lock` materializes the observer package entry using already resolved serde/serde_json/sha2 generations.

---

# 28. Static Qualification Actually Executed

Bake environment static checks:

```text
root Cargo.toml TOML parse                         PASS
observer Cargo.toml TOML parse                     PASS
Cargo.lock TOML parse                              PASS
observer workspace member                          PASS
observer absent from default-members               PASS
observer dependency set = serde/serde_json/sha2    PASS
observer has no base_train dependency               PASS
new external loader files                           0
new observer Rust `if` branch tokens                0
critical typed contract surfaces present            PASS
source delta ADD 6 / MOD 2 / DEL 0                 PASS
```

These are SOURCE/STATIC checks only.

---

# 29. Toolchain Qualification Boundary

The initial bake container exposed no preinstalled:

```text
cargo
rustc
```

A local Rust toolchain was therefore not available for authoritative observer compilation in the bake environment.

Consequently:

```text
observer Rust compile   NOT RUN
observer Rust tests     NOT RUN
paired release suite    NOT RUN
base_train release      NOT RUN IN BAKE ENVIRONMENT
WGPU execution          NOT RUN
```

The user-provided no-cut SAME_E0275 and repaired-cut release PASS remain external user-side release evidence.

No observer compile PASS is claimed by this specification.

---

# 30. ZIP Packaging Law

Delivered separately:

```text
overlay code-only ZIP
full applied code-only ZIP
```

Both exclude generated:

```text
specs/
docs/
artifacts/
target/
PowerShell loaders
runtime receipt output
```

No generated specification or external manifest package is embedded in either ZIP.

The Rust `Cargo.toml` / `Cargo.lock` required to register the new Rust crate are source/build metadata and are part of the code delta.

---

# 31. Bake Artifacts

Overlay:

```text
ASH_BASE_TRAIN_P1B_R1A2_FAIL_CLOSED_RELEASE_OBSERVATION_RECEIPT_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256: 1c5cac1e57102f6d167de518da2c32c843edb2b15c62dec1d86b8b13c3916318
Bytes: 53,378
Files: 8
CRC: PASS
```

Full applied:

```text
ASH_PASS3_BASE_TRAIN_P1B_R1A2_FAIL_CLOSED_RELEASE_OBSERVATION_RECEIPT_AUTHORITY_CODE_ONLY.zip
SHA-256: 4f78c08c1c8c3e4e824cad11dafaa8dcdd9f8dc2df04c5d65a8f869c72bd4d4a
Bytes: 21,966,260
Files: 8,431
CRC: PASS
```

Forbidden ZIP path check:

```text
specs/      0
docs/       0
artifacts/  0
target/     0
.ps1        0
```

---

# 32. First User-Side Qualification

Compile/test observer without compiling the default workspace set:

```powershell
cargo test -p ash_p1br1a2_release_observer --release
```

Then run:

```powershell
cargo run -p ash_p1br1a2_release_observer --release -- current-production
```

Expected from current external evidence, but not predeclared:

```text
burn-wgpu-local=BuildPass
burn_webgpu_backend=BuildPass
canonical-baseline=SameE0275
bisect-control=SameE0275
current-production-cut=BuildPass
paired-status=CurrentProductionClosureRequired
```

If `BisectControl` does not reproduce `SameE0275`, attribution is held.

---

# 33. Completion Law

R1A2 source bake is complete when:

```text
isolated Rust observer crate exists
observer is not a default member
observer does not depend on base_train
typed observation plans exist
CanonicalBaseline/BisectControl/CurrentProductionCut are distinct
source/toolchain/environment identities exist
exact Cargo invocation is typed
target/package/lib/profile observation exists
process exit status is bound
Cargo JSON is structurally parsed
canonical E0275 fingerprint is explicit
InvalidSlice precedence remains fail-closed
BuildPass requires successful intended-target completion
paired promotion is internally derived
caller cannot inject promotion status
runtime receipt is output-only
no production semantics change
no Python/PowerShell loader is added
```

---

# 34. Release Promotion Law

R1A2 may issue:

```text
PASS_P1B_R1A2_CURRENT_PRODUCTION_CLOSURE_REQUIRED
```

only from its own paired Rust observer receipt satisfying:

```text
dependency controls = BuildPass
CanonicalBaseline    = SameE0275
BisectControl        = SameE0275
CurrentProductionCut = BuildPass
source stable
toolchain stable
environment stable
```

Anything else remains an explicit HOLD state.

---

# 35. Final Law

> R1A2 does not classify release evidence from the mere absence of `E0275` text.
>
> The exact intended `base_train` release target, process completion, Cargo structured messages, source identity, toolchain identity and paired feature-mode control are all bound before promotion.
>
> `BisectControl` separates diagnostic feature-mode effects from the CurrentProduction cut itself.
>
> `InvalidSlice`, source drift, toolchain drift, environment drift, dependency baseline drift and wrong-target observations are fail-closed.
>
> Promotion status is derived from sealed Rust observations and is never caller-selected.
>
> A successful R1A2 suite establishes only that the dependency-closed CurrentProduction closure is required for the observed E0275 reproducer. Exact MCU, Muon, scheduler and natural Send/Sync demand attribution remain downstream work.
