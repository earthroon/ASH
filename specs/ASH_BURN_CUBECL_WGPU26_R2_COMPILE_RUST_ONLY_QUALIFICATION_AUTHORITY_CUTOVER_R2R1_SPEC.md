# ASH-BURN-CUBECL-WGPU26-R2-COMPILE-RUST-ONLY-QUALIFICATION-AUTHORITY-CUTOVER-R2R1

## 0. Revision

```text
Patch ID:
ASH-BURN-CUBECL-WGPU26
-R2-COMPILE-RUST-ONLY
-QUALIFICATION-AUTHORITY-CUTOVER-R2R1

Short name:
ASH WGPU26 R2R1
RUST-ONLY QUALIFICATION AUTHORITY

Status:
RUST-ONLY SOURCE MATERIALIZATION STATIC PASS
FULL RUST COMPILE QUALIFICATION: HOLD
```

Direct parent:

```text
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-CANONICAL-STORAGE
-AND-RESOURCE-ABI-R2
-FULL-COMPILE-CLOSURE
-TOOLING-MATERIALIZED-PENDING
```

Current terminal state:

```text
qualification_authority = ash.wgpu26.qualification.rust_only.r2r1
R2CompileQualification = Pending
compile_pass_claimed = false
physical_pass_claimed = false
python_qualification_authority_count = 0
```

Static materialization token:

```text
PASS_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_RUST_ONLY_QUALIFICATION_AUTHORITY_CUTOVER_R2R1_STATIC
```

Current HOLD:

```text
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

Reserved full compile PASS:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_COMPILE_CLOSURE
```

Reserved successor HOLD:

```text
HOLD_ASH_BURN_WGPU26_R2A_EXISTING_DEVICE_HANDLE_AND_RAW_RESOURCE_TYPE_EQUALITY_PENDING
```

## 1. Purpose

R2R1 removes Python from the active WGPU26 R2 qualification authority path and makes the Rust workspace own:

```text
parent source-tree seal
Cargo.lock successor seal
Cargo metadata graph admission
compiler/toolchain identity
candidate compile matrix
canonical cubecl-wgpu compiler-artifact admission
source-state promotion
promoted-source recompilation
compile receipt generation
compile receipt verification
```

The active trust chain becomes:

```text
Cargo + rustc
    -> ash-wgpu26-qualification
    -> ASH WGPU26 R2 qualification
```

No Python process participates in this chain.

## 2. Scope boundary

R2R1 removes these four P0/R2-COMPILE Python authority files from the code artifact:

```text
tools/freeze_ash_burn_cubecl_wgpu26_vendor_fork_r2_parent_p0.py
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_r2_parent_freeze_p0_static.py
tools/run_ash_burn_cubecl_wgpu26_r2_full_compile_closure.py
tools/validate_ash_burn_cubecl_wgpu26_r2_full_compile_closure_static.py
```

Historical ASH Python tools outside this qualification path are not part of this migration.

The historical R2 static validator is restored byte-for-byte to the P0/R2 parent version:

```text
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_canonical_storage_resource_abi_r2_static.py
SHA-256 = c8989f532f8b1992e33deb9b93167886172e1f43e4e75d52c0d79c982af3c772
```

It remains historical regression evidence and is not the current R2R1 promotion authority.

## 3. New Rust authority crate

Materialized workspace package:

```text
crates/ash_wgpu26_qualification
package = ash-wgpu26-qualification 0.1.0
```

Authority:

```text
ash.wgpu26.qualification.rust_only.r2r1
```

The crate is present in both:

```text
workspace.members
workspace.default-members
```

It links no WGPU, Burn or CubeCL runtime crate.

Its only dependencies are already-resolved utility crates:

```text
serde
serde_json
sha2
```

The crate owns no:

```text
wgpu::Device
wgpu::Queue
wgpu::Buffer
ComputeClient
tensor state
optimizer state
GPU allocation
runtime global
```

## 4. Rust crate layout

Materialized:

```text
crates/ash_wgpu26_qualification/
├─ Cargo.toml
└─ src/
   ├─ lib.rs
   ├─ main.rs
   ├─ error.rs
   ├─ digest.rs
   ├─ path.rs
   ├─ parent.rs
   ├─ cargo_graph.rs
   ├─ command.rs
   ├─ matrix.rs
   ├─ compiler.rs
   ├─ promotion.rs
   └─ receipt.rs
```

The code artifact contains 13 files under this crate including `Cargo.toml`.

## 5. Rust-only command surface

The executable owns four subcommands:

```text
parent-seal
validate-r2
qualify-r2
verify-receipt
```

Canonical full qualification form:

```powershell
cargo run --locked -p ash-wgpu26-qualification -- qualify-r2 `
  --workspace "D:\...\ASH_R2R1_PENDING" `
  --output-workspace "D:\...\ASH_R2_COMPILE_QUALIFIED" `
  --evidence-dir "D:\...\ASH_R2_COMPILE_EVIDENCE"
```

The qualification executable launches Cargo and Rustc directly through `std::process::Command`.

It does not invoke:

```text
python
python3
py
pypy
PowerShell
cmd /C
bash -c
```

as qualification authority.

## 6. Control-flow rule

The new Rust qualification authority contains no Rust `if` statement.

Admission and state transitions use `match` and closed enums.

Canonical state machine:

```text
Pending
-> ParentVerified
-> MetadataVerified
-> CandidateCompiled
-> Promoted
-> CompileQualified
```

Failures are represented as:

```rust
Result<T, QualificationError>
```

No warning-and-continue promotion path exists.

## 7. Parent tree reconstruction

R2R1 keeps the original R2 source tree as semantic parent even though the successor must modify a small set of authority files.

The Rust parent verifier computes the same historical domain:

```text
ASH_R2_PARENT_TREE_V1\0
```

For successor-modified original files it substitutes the frozen original size and SHA-256 while excluding successor-only Rust authority files.

Frozen reconstruction result:

```text
file count = 8,398
file bytes = 102,019,518
source-tree digest = 795fadb558dfdf9c6f72fc14f05367513bca7f90b6fda3bc98e244233c6a9d43
```

The code bake independently reproduced those exact values before archive creation and again after final ZIP extraction.

## 8. Cargo.toml successor seal

R2R1 changes root `Cargo.toml` only by adding:

```text
crates/ash_wgpu26_qualification
```

to:

```text
workspace.members
workspace.default-members
```

Removing those exact two lines reconstructs the frozen parent root manifest:

```text
SHA-256 = 23f9651a598bc9fc99ce243f7f18b3fffe4840eb3095d1ce9732c6e0e27b34ad
```

Current R2R1 root manifest SHA-256:

```text
15863b0f5608184e8309aa03b2655c7d4e6e8b3a880d418789229bb291b72d49
```

The root CubeCL patch remains:

```toml
[patch.crates-io]
cubecl-wgpu = { path = "vendor_fork_scaffold/cubecl-wgpu-ash" }
```

No Burn path fork is activated.

## 9. Cargo.lock successor seal

R2R1 permits exactly one new local package entry:

```text
ash-wgpu26-qualification 0.1.0
```

with dependencies:

```text
serde
serde_json
sha2
```

All are already present in the parent lock.

No new external package version is introduced.

Current R2R1 `Cargo.lock` SHA-256:

```text
4898739c50acf44acab3e93beb78283713ad8b535943c656c4d00ef5db501f7b
```

Removing exactly the qualification local-package entry reconstructs:

```text
00b5436550c645a93687554999b60e014cc255d7bb1d794e7c7d426d006e55f6
```

which is the frozen P0 parent lock digest.

## 10. Typed compile state authority

Materialized:

```text
crates/burn_webgpu_backend/src/r2_compile_qualification.rs
```

Canonical type:

```rust
pub enum R2CompileQualification {
    Pending,
    Qualified(R2CompileQualificationIdentity),
}
```

Current checked-in state:

```rust
R2CompileQualification::Pending
```

Identity type:

```rust
pub struct R2CompileQualificationIdentity {
    pub schema: &'static str,
    pub parent_tree_digest: [u8; 32],
    pub cargo_lock_digest: [u8; 32],
    pub cargo_graph_digest: [u8; 32],
    pub promotion_seed_digest: [u8; 32],
}
```

The historical boolean compile claim remains only as a compatibility projection:

```text
Pending      -> false
Qualified(_) -> true
```

## 11. Promotion-seed binding

Meaning change from the initial draft specification:

```text
compile_receipt_digest inside Qualified source
```

is replaced by:

```text
promotion_seed_digest inside Qualified source
+
final external compile receipt binds qualification projection SHA-256
```

Reason:

Embedding the final compile-receipt digest inside the source that the final receipt itself must hash creates a self-reference cycle.

R2R1 instead computes the promotion seed from candidate-stage immutable evidence:

```text
parent seal
Rust toolchain identity
candidate Cargo graph
candidate compile matrix
candidate Cargo.lock digest
```

The promoted source embeds that seed.

After the promoted source recompiles, the final Rust-generated receipt binds the SHA-256 of the exact promoted projection source.

This preserves closed provenance without a self-referential digest.

## 12. Backend compatibility projection

Modified:

```text
cubecl_wgpu_vendor_fork_r2.rs
cubecl_wgpu_canonical_resource_equality_r2.rs
r2_full_compile_closure.rs
```

Both historical compile booleans now derive from:

```text
R2_COMPILE_QUALIFICATION
```

`CubeClWgpuForkActivationStateR2` is derived by typed matching:

```text
Pending + path active + full source
    -> ActiveUncompiled

Qualified
    -> CompileQualified

physical PASS
    -> PhysicalQualified
```

Current materialized state remains:

```text
ActiveUncompiled
```

## 13. Cargo graph authority

`cargo_graph.rs` executes:

```text
cargo metadata --locked --format-version 1
```

and parses it in Rust with `serde_json`.

Required admission:

```text
wgpu package count = 1
wgpu version = 26.0.1

cubecl-wgpu package count = 1
cubecl-wgpu version = 0.9.0
cubecl-wgpu source = canonical vendor path
registry cubecl-wgpu count = 0

ash-wgpu26-qualification present = true
root cubecl-wgpu patch active = true
Burn path fork active = false
upstream_real_insert active = false
```

The graph fingerprint normalizes package identities and dependency contracts instead of hashing absolute Cargo workspace paths.

## 14. Compile matrix SSOT

`matrix.rs` defines the single typed matrix:

```text
QualificationSelfCheck
WorkspaceDefaultMembers
WgpuAuthority
StorageInterop
BackendDefault
BackendRawAccess
BurnWgpuLocal
BurnFusionLocal
ModelCore
BaseTrain
LoraTrain
OrchestratorLocal
```

Required Cargo checks include:

```text
cargo check --locked -p ash-wgpu26-qualification --all-targets
cargo check --locked --all-targets
cargo check --locked -p ash-wgpu26-api --all-targets
cargo check --locked -p ash-wgpu26-storage-interop --all-targets
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p burn_webgpu_backend --all-targets --features burn-raw-access-local
cargo check --locked -p burn-wgpu-local --all-targets
cargo check --locked -p burn-fusion-local --all-targets
cargo check --locked -p model_core --all-targets
cargo check --locked -p base_train --all-targets
cargo check --locked -p lora_train --all-targets
cargo check --locked -p orchestrator_local --all-targets
```

Every check requests:

```text
--message-format=json-render-diagnostics
```

for Rust-owned compiler-artifact parsing.

## 15. Canonical CubeCL compiler-artifact gate

`compiler.rs` parses Cargo JSON output directly.

At least one compile command in each phase must observe:

```text
reason = compiler-artifact
target.name = cubecl_wgpu
package_id identifies cubecl-wgpu
```

The Cargo metadata gate independently proves that the one resolved `cubecl-wgpu` package points to:

```text
vendor_fork_scaffold/cubecl-wgpu-ash/Cargo.toml
```

Therefore graph identity and actual compiler-artifact production are both required.

## 16. Two-stage compile transaction

The Rust authority enforces:

```text
Pending source
    -> candidate graph
    -> candidate compile matrix in target_candidate
    -> all PASS
    -> promotion seed
    -> copy into new output workspace
    -> write Qualified projection
    -> promoted graph
    -> graph equality
    -> Cargo.lock equality
    -> promoted compile matrix in target_promoted
    -> all PASS
    -> final Rust receipt
    -> Rust receipt re-verification
```

Candidate and promoted target directories are distinct and external to the code workspace.

The input workspace is never promoted in place.

## 17. Promotion write boundary

Promotion writes only the copied output workspace.

The projection is written through a temporary sibling file, flushed, installed into the disposable output workspace, and re-read for byte equality.

On platforms where replacing an existing file requires removing the copied pending projection first, failure invalidates only the new output workspace. The immutable input workspace is never mutated.

The output becomes publishable only after promoted compilation succeeds.

## 18. Rust-generated evidence

Successful qualification writes externally:

```text
ASH_BURN_CUBECL_WGPU26_R2_RUST_ONLY_METADATA.json
ASH_BURN_CUBECL_WGPU26_R2_RUST_ONLY_COMMAND_RECEIPTS.jsonl
ASH_BURN_CUBECL_WGPU26_R2_RUST_ONLY_CHANGED_FILES.json
ASH_BURN_CUBECL_WGPU26_R2_RUST_ONLY_COMPILE_RECEIPT.json
```

These files are serialized and verified by the Rust qualification crate.

They are evidence data, not Python authority.

They are excluded from the code ZIP.

## 19. Receipt authority

Final receipt schema:

```text
ash.wgpu26.r2.rust_only.compile_receipt.r2r1.v1
```

It binds:

```text
R2 parent seal
Rust toolchain identity
candidate graph digest
promoted graph digest
Cargo.lock digest
promotion seed digest
qualified projection SHA-256
candidate command count
promoted command count
canonical CubeCL compiler-artifact observation
compile PASS claim
physical PASS claim
semantic receipt digest
```

`verify-receipt` rechecks the semantic digest and the SHA-256 of the exact qualified Rust projection.

## 20. Typed fail-closed errors

Materialized `QualificationError` variants cover:

```text
parent mismatch
forbidden workspace path
Cargo missing
Rustc missing
Cargo metadata failure
WGPU package split
WGPU version drift
CubeCL package split
registry CubeCL reappearance
CubeCL path drift
qualification package missing
root patch drift
Burn path fork activation
upstream_real_insert activation
compile gate failure
CubeCL compiler artifact missing
invalid promotion state
promoted compile failure
promoted graph drift
Cargo.lock drift
receipt mismatch
forbidden Python qualification authority
physical claim escalation
state projection mismatch
```

Missing evidence never becomes an inferred PASS.

## 21. Python process prohibition

The new Rust authority contains no process construction for:

```text
python
python3
py
pypy
```

The four superseded Python qualification files are physically absent from the final code ZIP.

Historical Python scripts elsewhere in ASH are outside R2R1 scope and do not participate in this authority chain.

## 22. Rust branching policy

The new qualification crate and new R2 state-projection modules contain no Rust `if` statements.

Control flow uses `match` and typed state.

This was checked across:

```text
crates/ash_wgpu26_qualification/src/*.rs
r2_compile_qualification.rs
r2_full_compile_closure.rs
cubecl_wgpu_vendor_fork_r2.rs
cubecl_wgpu_canonical_resource_equality_r2.rs
```

## 23. Historical static regression

The final extracted code ZIP retains:

```text
R1   84 / 84 PASS
R1A 108 / 108 PASS
R2  117 / 117 PASS
```

R2 result remains:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_SOURCE_ACTIVATED_STATIC
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

This is consistent with the checked-in R2R1 state being `Pending`.

## 24. Compile boundary

The bake environment used for R2R1 source materialization exposes no `cargo`, `rustc`, or `rustfmt` executable.

Therefore this bake does not claim:

```text
ash-wgpu26-qualification Rust compilation PASS
cargo metadata PASS
candidate compile matrix PASS
promoted compile matrix PASS
CompileQualified state
full R2 compile PASS
```

The code was structurally checked for UTF-8/NUL, balanced source delimiters, parent reconstruction, exact Cargo successor delta, removal of Python qualification authority, and forbidden Python process construction.

No compiler PASS is inferred from those checks.

## 25. Code-bake delta

Relative to the prior R2-COMPILE tooling artifact:

```text
ADD 14
REMOVE 4
MODIFY 7
```

Added paths comprise:

```text
13 ash-wgpu26-qualification package/source files
1 r2_compile_qualification.rs typed state projection
```

Removed paths are exactly the four Python qualification authority files listed in Section 2.

Modified paths are:

```text
Cargo.toml
Cargo.lock
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/cubecl_wgpu_vendor_fork_r2.rs
crates/burn_webgpu_backend/src/cubecl_wgpu_canonical_resource_equality_r2.rs
crates/burn_webgpu_backend/src/r2_full_compile_closure.rs
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_canonical_storage_resource_abi_r2_static.py
```

The last path is a restoration to the P0 historical byte identity, not a new current Python authority.

## 26. Code-only artifact

Artifact:

```text
ASH_PASS3_BURN_CUBECL_WGPU26_R2R1_RUST_ONLY_QUALIFICATION_AUTHORITY_CODE_ONLY.zip
```

Identity:

```text
SHA-256:
5fcae9e9504c5e7c5d8510721ebd6bb357ddcf3be0a042f2f4dcce40eb239c89

archive bytes:
21,330,822

entries:
8,413

unique entries:
8,413

Markdown entries:
0

.pyc / __pycache__ entries:
0

target directories:
0

active P0/R2-COMPILE Python authority files:
0
```

The ZIP was independently built twice with identical bytes and identical SHA-256.

The final ZIP was extracted and the parent reconstruction plus historical R1/R1A/R2 validators were rerun successfully.

## 27. Code-only artifact law

Excluded from the code ZIP:

```text
this Markdown specification
qualification receipts
changed-file evidence
Cargo target directories
compiler logs
Python bytecode
temporary promotion files
```

The separation remains:

```text
code ZIP = source
external JSON/JSONL = evidence
GitHub specs/ = specification
```

## 28. Current acceptance result

Static source materialization satisfies:

```text
[PASS] Rust qualification crate materialized
[PASS] qualification crate is workspace member
[PASS] qualification crate is default member
[PASS] no WGPU/Burn/CubeCL runtime dependency in qualification crate
[PASS] four Python qualification authority files removed
[PASS] historical R2 validator restored to P0 digest
[PASS] parent tree reconstruction exact
[PASS] Cargo.toml successor delta exact
[PASS] Cargo.lock successor delta exact
[PASS] typed R2CompileQualification materialized
[PASS] compile bool converted to typed-state projection
[PASS] Rust Cargo metadata parser materialized
[PASS] Rust compile matrix materialized
[PASS] Rust compiler-artifact parser materialized
[PASS] Rust promotion path materialized
[PASS] Rust receipt writer/verifier materialized
[PASS] no Python child-process path in Rust qualification authority
[PASS] no Rust if statement in new authority surface
[PASS] R1 84 / 84
[PASS] R1A 108 / 108
[PASS] R2 117 / 117
[HOLD] actual Rust compiler qualification
[HOLD] R2A physical qualification
```

## 29. Successful future compile terminal state

Only an actual successful Rust-owned two-stage transaction may produce:

```text
R2CompileQualification::Qualified(...)
compile_pass_claimed = true
physical_pass_claimed = false
```

and emit:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_COMPILE_CLOSURE
HOLD_ASH_BURN_WGPU26_R2A_EXISTING_DEVICE_HANDLE_AND_RAW_RESOURCE_TYPE_EQUALITY_PENDING
```

## 30. Explicit non-claims

R2R1 source materialization does not claim:

```text
all historical ASH Python removed
all historical validators migrated to Rust
Rust compile PASS in this bake environment
Cargo metadata PASS in this bake environment
GPU execution
same physical Device instance
same physical Queue instance
same physical Buffer lineage
read-only alias physical zero-copy
writable alias exact D2D materialization
completion-bound alias transition
Burn source fork
Burn Fusion source fork
WGPU upgrade beyond 26.0.1
multi-device
tensor parallelism
```

## 31. Direct successor

After real Rust-owned full compile qualification:

```text
ASH-BURN-WGPU26
-EXISTING-DEVICE-HANDLE
-AND-RAW-RESOURCE-TYPE-EQUALITY-SEAL-R2A
```

R2A receives compiler qualification from the Rust workspace itself rather than from an external-language orchestration layer.

## 32. Final law

> The WGPU26 qualification authority is part of the Rust workspace it qualifies.

> Cargo and rustc are the bootstrap trust root; `ash-wgpu26-qualification` owns parent sealing, Cargo graph admission, compile execution, promotion and receipt verification above them.

> Python may remain as unrelated historical project tooling, but it has zero authority over the R2R1 compile qualification transition.

> `CompileQualified` is a typed Rust state. The legacy boolean is only a projection of that state.

> Until the Rust-owned candidate compile and promoted-source compile both succeed, the checked-in R2R1 source remains `Pending` and `HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING` remains authoritative.
