# ASH-BURN-CUBECL-WGPU26-VENDOR-FORK-CANONICAL-STORAGE-AND-RESOURCE-ABI-R2-FULL-COMPILE-CLOSURE

## 0. Revision

```text
Patch ID:
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-CANONICAL-STORAGE
-AND-RESOURCE-ABI-R2
-FULL-COMPILE-CLOSURE

Short name:
ASH WGPU26 R2 FULL COMPILE CLOSURE
R2-COMPILE

Status:
TOOLING STATIC MATERIALIZATION RELEASE
FULL COMPILE QUALIFICATION: HOLD
```

Direct parent:

```text
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-R2-PARENT-ARCHIVE
-AND-SOURCE-TREE-PROVENANCE-FREEZE-P0
```

Required inherited state:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_R2_PARENT_ARCHIVE_AND_SOURCE_TREE_PROVENANCE_FREEZE_P0_STATIC
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_SOURCE_ACTIVATED_STATIC
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING

activation_state = ActiveUncompiled
compile_pass_claimed = false
physical_pass_claimed = false
```

Current materialization token:

```text
PASS_ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_CLOSURE_TOOLING_STATIC
```

Current HOLD:

```text
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

Reserved full compile token:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_COMPILE_CLOSURE
```

Reserved successor HOLD:

```text
HOLD_ASH_BURN_WGPU26_R2A_EXISTING_DEVICE_HANDLE_AND_RAW_RESOURCE_TYPE_EQUALITY_PENDING
```

Claims at this bake:

```text
compile tooling materialized:   true
R1 static regression PASS:      true
R1A static regression PASS:     true
R2 successor static PASS:       true
R2-COMPILE tooling static PASS: true

Cargo metadata PASS:            NOT CLAIMED
Rust compile PASS:              NOT CLAIMED
Type-equality compile PASS:     NOT CLAIMED
GPU physical PASS:              NOT CLAIMED
```

## 1. Purpose

R2-COMPILE is the compiler qualification boundary between the already active canonical `cubecl-wgpu 0.9.0` path fork and R2A runtime physical identity work.

```text
R2 full source + root path patch active
        -> P0 exact parent freeze
        -> R2-COMPILE candidate compile
        -> claim promotion to CompileQualified
        -> fresh promoted compile
        -> R2 full compile PASS
        -> R2A physical Device / Queue / Buffer lineage qualification
```

R2-COMPILE proves compiler-accepted nominal package and type identity. It does not prove runtime physical instance identity.

## 2. Two-stage compile law

A candidate compile of source containing:

```text
compile_pass_claimed = false
activation_state = ActiveUncompiled
```

does not authorize compile PASS by itself.

The exact claim-bearing source containing:

```text
compile_pass_claimed = true
activation_state = CompileQualified
```

must itself compile from a different clean target directory.

Required transaction:

```text
candidate source
-> candidate clean compile matrix
-> all commands PASS
-> install claim promotion delta
-> promoted static validation
-> second clean compile matrix
-> all commands PASS
-> graph and Cargo.lock equality
-> external compile receipt
-> full compile PASS token
```

Any promoted compile failure invalidates promotion. Static promotion simulation is not compiler evidence.

## 3. P0 parent binding

```text
P0 code archive SHA-256:
9de7b67b1b0afd418108607653ea7196bfb13527c08ff95bb8b9521886daabab

R2 parent source-tree digest:
795fadb558dfdf9c6f72fc14f05367513bca7f90b6fda3bc98e244233c6a9d43

root Cargo.lock SHA-256:
00b5436550c645a93687554999b60e014cc255d7bb1d794e7c7d426d006e55f6
```

The runner consumes the external P0 manifest and freeze receipt, verifies all 8,398 frozen parent files and both P0 tooling additions, and rejects merely version-compatible substitute parents.

## 4. Frozen dependency authority

R2-COMPILE preserves:

```text
upstream wgpu       = 26.0.1
cubecl-wgpu         = 0.9.0 path fork
burn-wgpu           = 0.20.1 resolved
burn-fusion         = 0.20.1 resolved
burn-ir             = 0.20.1 resolved
```

The one ASH-owned direct upstream WGPU owner remains:

```text
crates/ash_wgpu26_api
```

The root patch remains exactly:

```toml
[patch.crates-io]
cubecl-wgpu = { path = "vendor_fork_scaffold/cubecl-wgpu-ash" }
```

Forbidden during R2-COMPILE:

```text
second WGPU package authority
registry cubecl-wgpu reappearance
Burn path fork activation
upstream_real_insert activation
root Cargo.lock rewrite
WGPU generation change
CubeCL version change
Burn version change
```

## 5. Materialized code surface

Relative to exact P0, this bake changes five paths:

```text
MOD crates/burn_webgpu_backend/src/lib.rs
ADD crates/burn_webgpu_backend/src/r2_full_compile_closure.rs
ADD tools/run_ash_burn_cubecl_wgpu26_r2_full_compile_closure.py
ADD tools/validate_ash_burn_cubecl_wgpu26_r2_full_compile_closure_static.py
MOD tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_canonical_storage_resource_abi_r2_static.py
```

No Cargo manifest, Cargo.lock, WGSL, CubeCL fork source, Burn local storage implementation, optimizer logic, Device/Queue bootstrap or runtime dispatch source changes in the tooling materialization bake.

## 6. Compile state projection

Materialized Rust module:

```text
crates/burn_webgpu_backend/src/r2_full_compile_closure.rs
```

Authority:

```text
ash.wgpu26.r2.full_compile_closure.v1
```

It owns no runtime GPU resource and projects state through Rust `match`:

```text
false -> ToolingMaterializedPending
true  -> CompileQualified
```

Current state:

```text
tooling_materialized = true
compile_pass_claimed = false
physical_pass_claimed = false
state = ToolingMaterializedPending
```

## 7. Successor-aware R2 static validator

Modified:

```text
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_canonical_storage_resource_abi_r2_static.py
```

Pending mode requires:

```text
compile claims false
activation_state = ActiveUncompiled
physical pass false
compile HOLD present
```

Compile-qualified mode requires:

```text
compile claims true
activation_state = CompileQualified
full compile token present in fork/equality surfaces
physical pass false
```

Mixed claim/state combinations fail.

Current result:

```text
118 / 118 PASS
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_SOURCE_ACTIVATED_STATIC
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
```

## 8. R2-COMPILE static validator

Materialized:

```text
tools/validate_ash_burn_cubecl_wgpu26_r2_full_compile_closure_static.py
```

It seals:

```text
compile closure Rust module/export
runner fail-closed surface
single WGPU 26.0.1 lock package
single path cubecl-wgpu 0.9.0
root patch exactness
P0 Cargo.lock digest
canonical staged/overlay storage equality
zero local WgpuResource/WgpuStorage definitions
conversion-free equality witness source
burn-raw-access-local feature retention
Burn path forks inactive
upstream_real_insert inactive
compile evidence absent from code artifact
compile specification absent from code artifact
compile/physical claim coherence
```

Current result:

```text
56 / 56 PASS
PASS_ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_CLOSURE_TOOLING_STATIC
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
COMPILE_PASS_CLAIMED=false
PHYSICAL_PASS_CLAIMED=false
```

## 9. Compile runner

Materialized:

```text
tools/run_ash_burn_cubecl_wgpu26_r2_full_compile_closure.py
```

Required interface:

```text
--p0-workspace <exact P0 code workspace>
--output-workspace <new compile-closure workspace>
--p0-evidence-dir <external P0 evidence>
--compile-evidence-dir <external compile evidence>
```

Optional:

```text
--candidate-only
--verify-only
```

No force-pass, ignore-error, witness-skip or raw-access-skip option exists.

## 10. Toolchain admission

Before promotion the runner requires real:

```text
cargo
rustc
```

Missing Cargo:

```text
E_R2C_CARGO_MISSING
```

Missing Rustc:

```text
E_R2C_RUSTC_MISSING
```

The current bake environment exposes neither Cargo nor Rustc. The runner was exercised and correctly terminated:

```text
E_R2C_CARGO_MISSING: cargo executable not found
```

No output workspace was promoted.

This is an environment HOLD, not a Rust source compile-failure claim.

## 11. Candidate compile matrix

A real qualification uses a fresh external `target_candidate` and executes:

```text
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

Compiler commands use:

```text
--message-format=json-render-diagnostics
```

## 12. Metadata gate

Before candidate compilation and after promotion:

```text
cargo metadata --locked --format-version 1
```

must prove:

```text
wgpu package count = 1
wgpu version = 26.0.1
cubecl-wgpu package count = 1
cubecl-wgpu version = 0.9.0
cubecl-wgpu source = path
cubecl-wgpu manifest = vendor_fork_scaffold/cubecl-wgpu-ash/Cargo.toml
root patch = cubecl-wgpu only
Burn path fork count = 0
upstream_real_insert patch count = 0
```

The selected dependency graph fingerprint must remain equal across promotion.

## 13. Canonical path compiler-artifact gate

At least one fresh check must emit a compiler artifact for target:

```text
cubecl_wgpu
```

from package:

```text
cubecl-wgpu 0.9.0
```

If not observed:

```text
E_R2C_CUBECL_PATH_COMPILER_ARTIFACT_MISSING
```

No promotion occurs.

## 14. Type-equality compile surface

The matrix must compile existing conversion-free witnesses for:

```text
workspace Device / Queue / Buffer
Burn WgpuSetup Device / Queue
Burn WgpuResource
CubeCL WgpuResource
CubeCL WgpuResource.buffer -> ash_wgpu26_api::Buffer
```

Mandatory `burn-raw-access-local` compile additionally includes:

```text
cubecl_wgpu::WgpuResource == burn_wgpu_local::WgpuResource
cubecl_wgpu::WgpuStorage  == burn_wgpu_local::WgpuStorage
```

The witness source remains free of:

```text
unsafe
transmute
from_raw
create_buffer
```

as type-generation adaptation mechanisms.

## 15. Claim promotion

Only after every candidate command PASS:

```text
ASH_CUBECL_WGPU_VENDOR_FORK_R2_COMPILE_PASS
false -> true

ASH_CUBECL_WGPU_R2_COMPILE_PASS_CLAIMED
false -> true

ActiveUncompiled -> CompileQualified
```

The runner then exposes the full compile token and R2A HOLD.

It keeps:

```text
physical_pass_claimed = false
compiler_delta_count = 0
shader_delta_count = 0
```

## 16. Promoted compile matrix

The claim-bearing promoted source is statically validated and compiled again with a different fresh external target:

```text
target_promoted
```

Candidate and promoted target directories may not alias.

Only this second successful matrix authorizes full compile PASS.

## 17. Cargo.lock law

Frozen root lock digest:

```text
00b5436550c645a93687554999b60e014cc255d7bb1d794e7c7d426d006e55f6
```

All Cargo admission commands use `--locked`.

Any lock mutation terminates:

```text
E_R2C_ROOT_LOCK_MUTATED
```

R2-COMPILE does not repair compilation by changing dependency resolution.

## 18. External compile evidence

A real successful compile run generates outside the code workspace:

```text
ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_METADATA.json
ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_COMMAND_RECEIPTS.jsonl
ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_CHANGED_FILES.json
ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_RECEIPT.json
```

These bind compiler identity, target, source digests, selected Cargo graph, command exit codes, stdout/stderr digests, path-fork compiler-artifact observation, Cargo.lock identity and claim state.

They are excluded from the code ZIP.

## 19. Code-only artifact

Current tooling archive:

```text
ASH_PASS3_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_CLOSURE_TOOLING_CODE_ONLY.zip
```

Identity:

```text
SHA-256:
d6ecc706b6810c3f5c3080df0e4bc909068af76c0fd4c59701e00c6f21a1b318

archive bytes:
21,330,876

entries:
8,403
unique entries:
8,403
Markdown entries:
0
embedded compile evidence:
0
.pyc / __pycache__ entries:
0
```

The archive was built twice with byte-identical output and identical SHA-256, then extracted and statically revalidated.

## 20. Static regression

Final extracted archive:

```text
R1                    84 / 84 PASS
R1A                  108 / 108 PASS
R2 successor-aware   118 / 118 PASS
R2-COMPILE tooling    56 / 56 PASS
```

Current authority remains:

```text
PASS_ASH_BURN_CUBECL_WGPU26_R2_FULL_COMPILE_CLOSURE_TOOLING_STATIC
HOLD_ASH_BURN_CUBECL_WGPU26_R2_COMPILE_PENDING
COMPILE_PASS_CLAIMED=false
PHYSICAL_PASS_CLAIMED=false
```

## 21. Promotion-path static simulation

Because the bake environment lacks Cargo/Rustc, the promotion transformation was tested only on an isolated disposable copy.

That copy statically reached:

```text
activation_state = CompileQualified
compile_pass_claimed = true
physical_pass_claimed = false
```

and the successor-aware R2 validator emitted the full compile token plus R2A HOLD.

The simulated copy was deleted and is not the artifact.

This proves only static promotion plumbing. It is not compiler evidence.

## 22. Fail-closed boundary

Representative errors:

```text
E_R2C_P0_PARENT_MISMATCH
E_R2C_P0_EVIDENCE_MISSING
E_R2C_CARGO_MISSING
E_R2C_RUSTC_MISSING
E_R2C_CARGO_METADATA_FAILED
E_R2C_WGPU_PACKAGE_SPLIT
E_R2C_WGPU_VERSION_DRIFT
E_R2C_CUBECL_WGPU_PACKAGE_SPLIT
E_R2C_CUBECL_WGPU_REGISTRY_REAPPEARED
E_R2C_CUBECL_WGPU_PATH_DRIFT
E_R2C_ROOT_LOCK_MUTATED
E_R2C_CANDIDATE_COMPILE_FAILED
E_R2C_CUBECL_PATH_COMPILER_ARTIFACT_MISSING
E_R2C_TYPE_EQUALITY_WITNESS_FAILED
E_R2C_PROMOTION_BEFORE_CANDIDATE_PASS
E_R2C_PROMOTED_SOURCE_STATIC_INVALID
E_R2C_PROMOTED_COMPILE_FAILED
E_R2C_PROMOTED_GRAPH_DRIFT
E_R2C_PHYSICAL_CLAIM_ESCALATED
E_R2C_UPSTREAM_REAL_INSERT_ACTIVATED
E_R2C_BURN_PATH_FORK_ACTIVATED
E_R2C_EVIDENCE_EMBEDDED_IN_CODE_ARCHIVE
E_R2C_SPEC_EMBEDDED_IN_CODE_ARCHIVE
E_R2C_RECEIPT_DIGEST_MISMATCH
E_R2C_OUTPUT_WORKSPACE_NOT_EMPTY
```

No failure is downgraded to a compile PASS warning.

## 23. Forbidden compile repair

R2-COMPILE must not obtain PASS by:

```text
adding another WGPU package
removing or cfg-gating equality witnesses
disabling burn-raw-access-local
removing burn-wgpu-local or burn-fusion-local
switching cubecl-wgpu back to registry
adding compatibility WgpuResource/WgpuStorage structs
using unsafe/transmute/from_raw for generation conversion
changing WGSL
changing optimizer math
changing runtime scheduling
adding host-copy materialization
adding another Device/Queue
activating upstream_real_insert
activating Burn path forks
```

Compiler-local corrections are admissible only when dependency graph, Cargo.lock, GPU semantics, storage ABI, Device/Queue ownership and shader bytes remain unchanged.

## 24. Local qualification invocation

The full transaction must run on a machine with real Cargo/Rustc using the exact P0 workspace and P0 evidence.

```powershell
python tools/run_ash_burn_cubecl_wgpu26_r2_full_compile_closure.py `
  --p0-workspace "D:\...\ASH_R2_P0" `
  --output-workspace "D:\...\ASH_R2_COMPILE" `
  --p0-evidence-dir "D:\...\ASH_R2_P0_EVIDENCE" `
  --compile-evidence-dir "D:\...\ASH_R2_COMPILE_EVIDENCE"
```

The runner comes from the R2-COMPILE tooling archive; `--p0-workspace` points to the exact sealed P0 code workspace.

Successful real qualification must terminate:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FULL_COMPILE_CLOSURE
HOLD_ASH_BURN_WGPU26_R2A_EXISTING_DEVICE_HANDLE_AND_RAW_RESOURCE_TYPE_EQUALITY_PENDING
```

Anything else leaves compile qualification incomplete.

## 25. Explicit non-claims

This tooling bake does not claim:

```text
Cargo metadata success
Rust compiler success
type-equality compiler acceptance
burn-raw-access-local compiler acceptance
CubeCL path compiler-artifact production
claim-bearing promoted source compilation
GPU execution
Device creation
Queue submission
same physical Device/Queue identity
same physical Buffer lineage
read-only alias zero-copy
writable alias D2D materialization
numerical parity
performance parity
R2A admission
```

## 26. Next transition

The next operation is execution of this R2-COMPILE transaction on the actual Rust build machine.

Only a real successful two-stage compiler transaction may transition:

```text
ToolingMaterializedPending
ActiveUncompiled
compile_pass_claimed = false
```

to:

```text
CompileQualified
compile_pass_claimed = true
physical_pass_claimed = false
```

After that, the architectural successor is:

```text
ASH-BURN-WGPU26
-EXISTING-DEVICE-HANDLE
-AND-RAW-RESOURCE-TYPE-EQUALITY-SEAL-R2A
```

## 27. Final law

> R2-COMPILE tooling may prepare, measure, validate and transactionally promote compile state, but it may not manufacture compiler qualification in an environment without Cargo and Rustc.

> Candidate compilation alone is insufficient. The exact claim-bearing `CompileQualified` source must compile again from a distinct clean target directory.

> Dependency authority, canonical CubeCL storage/resource identity, root Cargo.lock, shader bytes, runtime Device/Queue ownership and GPU semantics remain frozen throughout compiler qualification.

> Until the physical compiler transaction succeeds, R2 remains `ActiveUncompiled` and the compile HOLD remains authoritative.
