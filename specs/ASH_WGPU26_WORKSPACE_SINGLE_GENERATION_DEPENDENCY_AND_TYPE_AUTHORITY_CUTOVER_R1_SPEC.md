# ASH-WGPU26-WORKSPACE-SINGLE-GENERATION-DEPENDENCY-AND-TYPE-AUTHORITY-CUTOVER-R1

## 0. Revision

```text
Patch ID:
ASH-WGPU26
-WORKSPACE-SINGLE-GENERATION-DEPENDENCY
-AND-TYPE-AUTHORITY-CUTOVER-R1

Short name:
ASH WGPU26 R1
WORKSPACE SINGLE GENERATION + TYPE AUTHORITY CUTOVER

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:           NOT CLAIMED
Cargo metadata PASS:         NOT CLAIMED
Type-equality compile PASS:  NOT CLAIMED
GPU physical PASS:           NOT CLAIMED
```

Static token:

```text
PASS_ASH_WGPU26_WORKSPACE_SINGLE_GENERATION_DEPENDENCY_AND_TYPE_AUTHORITY_CUTOVER_R1_STATIC
```

Physical state:

```text
HOLD_ASH_WGPU26_R1_PHYSICAL_PENDING
```

## 1. Parent Source Truth

The direct R8A source already resolves one upstream WGPU package in `Cargo.lock`:

```text
wgpu       26.0.1
wgpu-core  26.0.1
wgpu-hal   26.0.6
wgpu-types 26.0.0
naga       26.0.0
```

The Burn/CubeCL line remains:

```text
burn-wgpu   0.20.1
cubecl      0.9.0
cubecl-wgpu 0.9.0
```

R1 therefore closes distributed package/type authority rather than claiming a historical multi-version lockfile still exists.

## 2. Problem Closed

Before R1, six ASH/vendor manifests independently declared:

```toml
wgpu26 = { package = "wgpu", version = "26.0.1" }
```

while source code already used one common `wgpu26::...` spelling.

That meant current convergence on WGPU 26 was a repeated manifest decision rather than one workspace authority.

R1 makes exactly one ASH-owned crate responsible for requesting upstream WGPU.

## 3. New Workspace Authority Crate

Materialized:

```text
crates/ash_wgpu26_api
```

Package:

```text
ash-wgpu26-api 0.1.0
```

It is a workspace member and default member.

It alone directly owns:

```toml
wgpu_impl = { package = "wgpu", version = "=26.0.1" }
```

No other ASH-owned runtime manifest directly requests package `wgpu`.

## 4. Type Authority Law

`ash-wgpu26-api` does not wrap Device, Queue, Buffer or other WGPU objects.

It re-exports the exact upstream public WGPU API:

```rust
pub use wgpu_impl::*;
```

Therefore:

```text
ash_wgpu26_api::Buffer
== nominal upstream wgpu 26.0.1 Buffer
```

rather than merely being convertible to it.

The authority crate owns no runtime Device, Queue, allocation pool, optimizer state or global resource registry.

## 5. Workspace Authority Identity

Materialized constants/types include:

```text
ASH_WGPU26_WORKSPACE_AUTHORITY_ID
ASH_WGPU26_UPSTREAM_PACKAGE
ASH_WGPU26_UPSTREAM_VERSION
ASH_WGPU26_GENERATION
ASH_WGPU26_SOURCE_ALIAS
WorkspaceWgpu26AuthorityIdentityR1
Wgpu26ResolvedSuiteIdentityR1
WorkspaceWgpu26DependencyReceiptR1
```

Canonical authority ID:

```text
ash.wgpu26.workspace.single_generation_type_authority.r1
```

## 6. Source-compatible Dependency Alias Cutover

R1 deliberately does not mass-rewrite hundreds of existing `wgpu26::...` source references.

The dependency key remains:

```text
wgpu26
```

but now points to package:

```text
ash-wgpu26-api
```

instead of upstream `wgpu` directly.

Materialized consumers:

```text
base_train
burn_webgpu_backend
model_core
lora_train
orchestrator_local
vendor_fork_scaffold/burn-wgpu-local
```

This separates source namespace compatibility from Cargo package authority.

## 7. Cargo.lock Cutover

The path package:

```text
ash-wgpu26-api 0.1.0
```

is present in `Cargo.lock` and depends on the sole resolved upstream:

```text
wgpu 26.0.1
```

The six migrated ASH/vendor packages now have lock edges to:

```text
ash-wgpu26-api
```

and no direct lock edge to `wgpu`.

The resolved upstream WGPU package count remains exactly one.

## 8. Burn/CubeCL Convergence

The transitive Burn/CubeCL path remains:

```text
burn-wgpu
  -> CubeCL
  -> cubecl-wgpu
  -> wgpu 26.0.1
```

and converges on the same single resolved WGPU package used by `ash-wgpu26-api`.

R1 does not treat Burn 0.20.x or CubeCL 0.9.x package versions as WGPU generation labels.

## 9. Runtime WGPU Authority Binding

Historical:

```text
ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1
```

remains immutable.

`runtime_wgpu_type_authority` now sources its package/version labels from `ash-wgpu26-api` and materializes:

```text
RuntimeWgpuWorkspaceBindingR1
```

binding the historical runtime authority to the new workspace parent.

Existing aliases such as:

```text
RuntimeWgpuDevice
RuntimeWgpuQueue
RuntimeWgpuBuffer
RuntimeWgpuCommandEncoder
```

remain unchanged at their public semantic boundary.

## 10. Vendor Scaffold Binding

`vendor_fork_scaffold/burn-wgpu-local` now consumes `ash-wgpu26-api` through its historical dependency key `wgpu26`.

Its `gpu_api` surface remains source-compatible and now exposes:

```text
ASH_WGPU_API_AUTHORITY
```

bound to the workspace authority.

R1 does not yet merge local and upstream `WgpuStorage/WgpuResource` structs. That is successor R2 scope.

## 11. Compile-time Type Equality Witnesses

Materialized:

```text
wgpu26_workspace_type_equality_r1.rs
```

The module contains conversion-free compiler witnesses for:

```text
workspace Device <-> RuntimeWgpuDevice
workspace Queue <-> RuntimeWgpuQueue
workspace Buffer <-> RuntimeWgpuBuffer
workspace CommandEncoder <-> RuntimeWgpuCommandEncoder
burn_wgpu::WgpuSetup.device -> workspace Device
burn_wgpu::WgpuSetup.queue  -> workspace Queue
burn_wgpu::WgpuResource.buffer -> workspace Buffer
burn_wgpu_local::WgpuResource.buffer -> workspace Buffer
```

The witness module contains no `unsafe`, `transmute` or `from_raw` bridge.

Because this bake environment has no Rust compiler, compile equality PASS remains explicitly false/unclaimed.

## 12. Direct Manifest Authority Rule

Static R1 admission requires:

```text
ASH-owned direct upstream wgpu manifest owner count = 1
```

The only permitted owner is:

```text
crates/ash_wgpu26_api/Cargo.toml
```

A second ASH manifest directly requesting even the same `wgpu 26.0.1` is an authority violation.

## 13. Single Generation Rule

Static/metadata target:

```text
resolved upstream wgpu package count = 1
resolved upstream version            = 26.0.1
duplicate WGPU generation count      = 0
```

R1 treats two distinct Cargo package IDs as a split even when both claim WGPU generation 26.

## 14. Resolved Suite Baseline

Current recorded static baseline:

```text
wgpu       26.0.1
wgpu-core  26.0.1
wgpu-hal   26.0.6
wgpu-types 26.0.0
naga       26.0.0
```

The differing transitive patch versions are recorded suite evidence and are not mislabeled as nominal WGPU type-generation splits.

A future resolved-suite drift requires requalification.

## 15. No WGPU Patch/Fork in R1

R1 does not add a root `[patch.crates-io] wgpu` override and does not introduce a second local WGPU package.

The canonical vendor storage fork/cutover remains a later revision.

## 16. Existing-device Semantics Preserved

R1 does not change the existing shared Device/Queue bootstrap into Burn/CubeCL.

It does not create a second Device or Queue to escape a type mismatch.

The goal is that one physical Device/Queue and one nominal Rust WGPU generation are shared across ASH/Burn/CubeCL/vendor code.

## 17. WGPU Resource/Lifetime Parents Preserved

R1 does not modify semantics of:

```text
A01 SubmissionEpoch lease
A02 usage-segregated arena
A03 staging/readback
MCU R7A kernel/buffer resource lifetime
MCU R7B physical ownership
R7A1 packed-gradient lifetime
HiMuon R8/R8A state/mathematics
```

Only package/type authority changes.

## 18. Static Validation

Validator:

```text
tools/validate_ash_wgpu26_workspace_single_generation_dependency_type_authority_cutover_r1_static.py
```

Current result:

```text
84 / 84 PASS
```

Token:

```text
PASS_ASH_WGPU26_WORKSPACE_SINGLE_GENERATION_DEPENDENCY_AND_TYPE_AUTHORITY_CUTOVER_R1_STATIC
```

The validator checks workspace membership, exact pin, manifest direct-owner count, six consumer aliases, runtime/vendor binding, compile witness presence, lock edges, single resolved WGPU package and the current WGPU-family suite.

## 19. Parent Regression

Current bake retains:

```text
HiMuon R8A                         115 / 115 PASS
HiMuon R8                           90 / 90 PASS
packed-gradient R7A1               82 / 82 PASS
MCU child ownership R7B            78 / 78 PASS
MCU device resource R7A            73 / 73 PASS
Trainable Session R4A              65 / 65 PASS
Trainable Session R4               64 / 64 PASS
Eve R3G                            35 / 35 PASS
R3C                                18 / 18 PASS
R3C1                               30 / 30 PASS
R3D                                41 / 41 PASS
R3E                                52 / 52 PASS
R3F                                66 / 66 PASS
Unified Atlas MCU R6               PASS
Mixed-precision MCU R7             PASS
SubmissionEpoch active async       PASS
Resident Weight                    67 / 67 PASS
```

Vendor A00 remains at its direct-parent baseline:

```text
77 / 81 PASS
```

with the same four pre-existing allocation-site/hook count assertions on the direct R8A parent.

A01/A02/A03 standalone validators require Markdown specification files; the requested code-only source tree excludes `specs/`, so those standalone invocations stop at their historical missing-spec prerequisite.

## 20. Compile Boundary

This bake environment exposes no:

```text
cargo
rustc
rustfmt
```

Therefore R1 does not claim:

```text
cargo metadata PASS
cargo check PASS
type-equality compile PASS
GPU physical PASS
```

All modified Cargo manifests and `Cargo.lock` parse as TOML. New/modified Rust authority files pass UTF-8/NUL and balanced-delimiter structural checks. The R1 Python validator passes `py_compile`.

## 21. Compile Qualification

A later compile qualification requires at minimum:

```text
cargo metadata over the actual workspace/lock
resolved wgpu package count = 1
workspace cargo check
burn-raw-access-local feature cargo check
compiler acceptance of every R1 type-equality witness
no unsafe generation bridge
```

Only then may the reserved compile token be claimed.

## 22. Physical Qualification

Physical promotion additionally requires a real WGPU 26 Device/Queue bootstrap, Burn/CubeCL existing-device integration, raw Burn/vendor buffer borrowing and at least one real ASH GPU execution path, while proving no extra Device/Queue construction and no conversion compatibility layer.

Until then:

```text
HOLD_ASH_WGPU26_R1_PHYSICAL_PENDING
```

## 23. Explicit Non-claims

R1 does not claim:

```text
all `wgpu26::...` source spellings removed
vendor WgpuStorage/WgpuResource canonicalized
CubeCL vendor fork completed
runtime feature/limit/device-capability seal completed
all WGPU 26 APIs physically qualified
multi-device execution
tensor parallelism
```

## 24. Direct Successor

Recommended next revision:

```text
ASH-WGPU26
-DIRECT-IMPORT-RETIREMENT
-AND-RUNTIME-TYPE-FACADE-ADOPTION-R1A
```

After that:

```text
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-CANONICAL-STORAGE
-AND-RESOURCE-ABI-R2
```

can remove the remaining duplicate vendor/upstream storage/resource ABI while inheriting one already-fixed WGPU type generation.

## 25. Final Law

> ASH no longer merely happens to resolve WGPU 26.0.1. One workspace authority crate is the sole ASH-owned requester of upstream WGPU.

> Existing `wgpu26::...` source syntax may remain during migration, but it resolves through the workspace façade rather than independent direct package ownership.

> Burn, CubeCL, ASH runtime aliases and the vendor scaffold are required to inhabit one nominal WGPU type generation without conversion or unsafe bridging.
