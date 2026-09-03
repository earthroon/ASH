# ASH-BURN-CUBECL-WGPU26-VENDOR-FORK-CANONICAL-STORAGE-AND-RESOURCE-ABI-R2

## 0. Revision

```text
Patch ID:
ASH-BURN-CUBECL-WGPU26
-VENDOR-FORK-CANONICAL-STORAGE
-AND-RESOURCE-ABI-R2

Status:
FOUNDATION STATIC MATERIALIZATION RELEASE
FULL PATH-FORK ACTIVATION: HOLD

Rust compile PASS:             NOT CLAIMED
Cargo metadata PASS:           NOT CLAIMED
canonical ABI compile PASS:    NOT CLAIMED
full CubeCL path-fork PASS:     NOT CLAIMED
GPU physical PASS:             NOT CLAIMED
```

Foundation static token:

```text
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FOUNDATION_STATIC
```

Full-fork hold:

```text
HOLD_ASH_BURN_CUBECL_WGPU26_R2_FORK_ACTIVATION_SOURCE_PENDING
```

## 1. Direct Parents

R2 consumes:

```text
ASH-WGPU26-WORKSPACE-SINGLE-GENERATION-DEPENDENCY-AND-TYPE-AUTHORITY-CUTOVER-R1
ASH-WGPU26-DIRECT-IMPORT-RETIREMENT-AND-RUNTIME-TYPE-FACADE-ADOPTION-R1A
```

R1 keeps one upstream WGPU 26 package/type authority. R1A keeps one ASH runtime WGPU type facade. R2 addresses the remaining CubeCL/Burn storage and resource ABI split.

## 2. Parent Source Limitation

The direct R1A code-only parent contains only the modified CubeCL `compute/storage.rs` mirror and not the complete `cubecl-wgpu 0.9.0` source package.

The current Cargo lock records:

```text
cubecl-wgpu 0.9.0
29787364632fc7ec6a11cf3d95187f82f6fcce17d6bb4f0fb0dde580b837631d
```

R2 therefore does not fabricate a complete fork tree and does not falsely activate `[patch.crates-io]` against an incomplete crate.

## 3. Cycle-free Storage Interop Leaf

Materialized workspace crate:

```text
crates/ash_wgpu26_storage_interop
package = ash-wgpu26-storage-interop
```

Dependencies:

```text
ash-wgpu26-api
cubecl-runtime = 0.9.0
```

It has no dependency on `cubecl-wgpu`, `burn-wgpu`, `burn-wgpu-local`, `burn-fusion`, `burn-fusion-local`, or `burn_webgpu_backend`, preventing the historical potential cycle `cubecl-wgpu -> burn-wgpu-local -> burn-wgpu -> cubecl-wgpu`.

## 4. Interop Authority

Authority:

```text
ash.wgpu26.storage_interop.alias_lifecycle.r2
```

The leaf owns external StorageHandle alias lifecycle, fork snapshot/merge state, in-flight materialization counters, and vendor allocation/deallocation/materialization instrumentation. It does not own `WgpuStorage` or Burn tensor semantics.

## 5. Primitive External Alias ABI

Materialized:

```rust
ExternalWgpuBufferAliasR2 {
    buffer: ash_wgpu26_api::Buffer,
    offset: u64,
    size: u64,
}
```

The lower leaf intentionally does not store `cubecl_wgpu::WgpuResource`, avoiding a dependency cycle.

## 6. Alias Lifecycle Preservation

The existing lifecycle remains:

```text
BorrowedReadOnly
DetachedOwned
Tombstoned
```

The single registry retains registered epoch, last-access epoch, producer stream identity, in-flight materialization count, fork snapshot/merge, and perf counters.

## 7. Inventory Hook Extraction

The previous `burn-wgpu-local` buffer inventory singleton is moved into the interop leaf. `burn-wgpu-local/src/buffer_inventory_hook.rs` is now a re-export shim.

## 8. Local Duplicate Resource ABI Retirement

`burn-wgpu-local::compute::storage` no longer defines independent `WgpuStorage` or `WgpuResource` structs. Current local duplicate definition counts are zero.

Instead it directly re-exports:

```rust
pub use cubecl_wgpu::{WgpuResource, WgpuStorage};
```

Therefore the local extension resource/storage names already resolve to the real CubeCL types before full fork activation.

## 9. Local Arc<Buffer> Storage ABI Retired

The historical local `HashMap<StorageId, Arc<wgpu::Buffer>>` competing storage ABI is removed from active `burn-wgpu-local` source. The canonical resource representation uses the CubeCL WGPU Buffer handle directly.

## 10. Canonical Storage Extension Trait

R2 materializes `CanonicalWgpuStorageAliasExtR2` for caller-encoder external-alias materialization on canonical `cubecl_wgpu::WgpuStorage`.

It resolves the interop primitive alias, allocates through `ComputeStorage::alloc`, obtains the destination through `ComputeStorage::get`, encodes exact-size D2D copy, records materialization bytes, and binds completion after actual submission.

## 11. Completion-bound Materialization

The lifecycle is:

```text
resolve borrowed alias
-> canonical CubeCL destination allocation
-> caller-owned encoder copy
-> actual queue submission
-> mark in-flight
-> queue completion callback
-> complete lifecycle transition
```

Zero-byte resources emit no copy command.

## 12. Canonical Resource Registration Adapter

`burn-wgpu-local::storage_alias_registry` becomes an adapter/re-export surface. Registration accepts canonical `cubecl_wgpu::WgpuResource`, clones only its WGPU Buffer handle metadata, then records `ExternalWgpuBufferAliasR2` in the lower registry. This is not a GPU buffer copy and not a second `WgpuResource` ABI.

## 13. WGPU Feature Passthrough

`ash-wgpu26-api` exposes passthrough features needed when the complete CubeCL fork is activated:

```text
fragile-send-sync-non-atomic-wasm
vulkan-portability
```

Both forward to the sole upstream WGPU implementation dependency, preserving R1 authority.

## 14. CubeCL Fork Overlay

Materialized:

```text
vendor_fork_scaffold/cubecl-wgpu-ash-overlay/storage.rs
vendor_fork_scaffold/cubecl-wgpu-ash-overlay/activate_cubecl_wgpu_r2.py
```

The storage overlay has no dependency on `burn-wgpu-local` and consumes the cycle-free interop leaf directly.

## 15. Overlay Canonical Storage Semantics

The overlay preserves upstream-style `HashMap<StorageId, wgpu::Buffer>` and `WgpuResource { buffer: wgpu::Buffer, offset, size }`, while adding external alias resolution in `get`, allocation/deallocation inventory hooks, deallocation tombstoning, flush sweeping, caller-encoder exact D2D materialization, and completion-bound alias transition. No host readback is introduced.

## 16. Fork Activation Script

`activate_cubecl_wgpu_r2.py` requires a separately available complete `cubecl-wgpu 0.9.0` source directory. It validates package name/version, stages the full tree into `vendor_fork_scaffold/cubecl-wgpu-ash`, installs the R2 storage overlay, adds the storage interop dependency, redirects CubeCL's source-level `wgpu` key to `ash-wgpu26-api`, preserves the upstream non-mac/mac WGPU feature requests, and can activate the root `cubecl-wgpu` patch entry.

## 17. Full Fork Activation Intentionally Not Claimed

Current code-only R2 bake explicitly records:

```text
full_source_present = false
patch_active = false
```

The root workspace still resolves the registry `cubecl-wgpu 0.9.0` package until a complete source tree is staged. This is a deliberate fail-closed boundary.

## 18. Compile-time Canonical ABI Witnesses

Materialized `cubecl_wgpu_canonical_resource_equality_r2.rs` requires zero-conversion identity for:

```text
cubecl_wgpu::WgpuResource -> burn_wgpu::WgpuResource
cubecl_wgpu::WgpuResource -> burn_wgpu_local::WgpuResource
cubecl_wgpu::WgpuStorage  -> burn_wgpu_local::WgpuStorage
cubecl_wgpu::WgpuResource.buffer -> ash_wgpu26_api::Buffer
```

No field-by-field compatibility reconstruction, `unsafe`, `transmute`, or buffer allocation appears in the equality module. Actual compile equality PASS is not claimed without `cargo/rustc`.

## 19. Fork Provenance State

Materialized:

```text
CubeClWgpuVendorForkIdentityR2
CubeClWgpuForkActivationStateR2
CubeClWgpuForkDiffReceiptR2
```

Current activation state is `OverlayReadySourcePending`; compiler and shader delta counts are zero in the R2 overlay receipt.

## 20. Cargo Graph Changes Already Materialized

Workspace now includes `ash-wgpu26-storage-interop`. `burn-wgpu-local` directly consumes `ash-wgpu26-api`, `ash-wgpu26-storage-interop`, and `cubecl-wgpu = 0.9.0`. `burn_webgpu_backend` directly names `cubecl-wgpu = 0.9.0` for compile-time ABI witnesses. Current lock still contains one registry `cubecl-wgpu` because full fork activation is held.

## 21. R1 / R1A Preservation

Current results:

```text
WGPU26 R1   84 / 84 PASS
WGPU26 R1A 108 / 108 PASS
```

R1A remains successor-aware while preserving one upstream WGPU package, exact `wgpu 26.0.1`, zero high-level direct primitive dependencies, and zero active `wgpu26` source imports.

## 22. R2 Foundation Static Validation

Validator:

```text
tools/validate_ash_burn_cubecl_wgpu26_vendor_fork_canonical_storage_resource_abi_r2_static.py
```

Current result:

```text
103 / 103 PASS
PASS_ASH_BURN_CUBECL_WGPU26_VENDOR_FORK_CANONICAL_STORAGE_AND_RESOURCE_ABI_R2_FOUNDATION_STATIC
```

The validator also requires the full-fork HOLD token while the staged full source and root patch are absent.

## 23. Parent Regression

Current bake retains PASS for HiMuon R8A/R8, packed-gradient R7A1, MCU R7B/R7A/R7, Trainable Session R4A/R4, Eve R3G, R3C/R3C1/R3D/R3E/R3F, Unified Atlas MCU R6, mixed-precision MCU R7, SubmissionEpoch active async, resident Weight, and vendor mixed precision.

Historical unchanged baselines remain:

```text
RAM exact inventory          66 / 67
N8 RAM resume-cut           117 / 118
vendor buffer A00            77 / 81
```

Vendor A01/A02/A03 standalone validators still require Markdown spec files that code-only artifacts intentionally exclude.

## 24. Compile Boundary

The current bake environment exposes no `cargo`, `rustc`, or `rustfmt`. Therefore no Cargo metadata/check or compiler type-equality claim is made. Changed Cargo files parse as TOML; R2 Python tools pass `py_compile`; critical changed Rust files pass UTF-8/NUL and balanced-delimiter structural checks.

## 25. Full R2 Closure Requirements

Full R2 static/compile closure requires a complete exact `cubecl-wgpu 0.9.0` source tree to be staged, then root patch activation, one path `cubecl-wgpu` resolution, Burn closure verification, one upstream WGPU 26.0.1 package, compiled WgpuResource/WgpuStorage identity witnesses, workspace cargo check, raw-access feature check, and burn-fusion-local check.

Only then may full R2 static/compile tokens replace the source-pending HOLD.

## 26. Physical Qualification

Physical R2 additionally requires real Burn/CubeCL execution proving read-only external alias zero-copy, same physical Buffer/offset/size, writable detach exact D2D logical-byte copy, zero D2H for materialization, completion-bound DetachedOwned transition, in-flight tombstone retention, canonical CubeCL alloc/dealloc route, no local duplicate allocator, no second Device/Queue, and no numerical regression.

## 27. Explicit Non-claims

This bake does not claim a complete embedded `cubecl-wgpu` fork, active root path patch, Burn full source fork, Burn Fusion full source fork, WGPU beyond 26.0.1, runtime device capability R3 seal, or GPU physical R2 qualification.

## 28. Direct Closure

The next immediate operation is R2 activation closure:

```text
stage exact full cubecl-wgpu 0.9.0 source
run activate_cubecl_wgpu_r2.py --activate-root-patch
run Cargo metadata/check
promote R2 from FOUNDATION STATIC to FULL STATIC/COMPILE
```

After full R2 closure, the architectural successor is:

```text
ASH-BURN-WGPU26-EXISTING-DEVICE-HANDLE-AND-RAW-RESOURCE-TYPE-EQUALITY-SEAL-R2A
```

## 29. Final Law

> `burn-wgpu-local` no longer defines a competing `WgpuStorage/WgpuResource` ABI.

> Alias lifecycle state now lives below Burn/CubeCL in a cycle-free WGPU26 interop leaf.

> The exact CubeCL storage modifications are prepared as a real fork overlay, but the workspace does not pretend an incomplete fork is active.

> R2 foundation closes the local ABI split now; full CubeCL runtime hook authority activates only when the complete exact upstream source is present and compiler-qualified.
