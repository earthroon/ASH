# ASH-TCU-K7N-D0R2R1 SPEC

## WGPU Type-Generation Split Prerequisite Repair

## 1. Patch Identity

- Patch ID: `ASH-TCU-K7N-D0R2R1_WGPU_TYPE_GENERATION_SPLIT_PREREQUISITE_REPAIR`
- Status target: `PASS_ASH_TCU_K7N_D0R2R1_WGPU_TYPE_GENERATION_SPLIT_PREREQUISITE_REPAIR_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- GitHub path: `specs/ASH_TCU_K7N_D0R2R1_WGPU_TYPE_GENERATION_SPLIT_PREREQUISITE_REPAIR_SPEC.md`
- Patch class: blocker-specific prerequisite repair

## 2. Parent State

Required parent:

- `ASH-TCU-K7N-D0R2_VOCAB_ATLAS_TILE_SHAPE_LAYOUT_TAIL_ROUTE_IDENTITY_CONTRACT`
- required status: `PASS_ASH_TCU_K7N_D0R2_VOCAB_ATLAS_TILE_SHAPE_LAYOUT_TAIL_ROUTE_IDENTITY_CONTRACT_NO_RUNTIME_DISPATCH_NO_OUTPUT_CHANGE`
- required verdict: `vocab_atlas_tile_shape_layout_tail_route_identity_contract_completed_but_candidate_remains_explicitly_blocked_without_runtime_dispatch_or_output_change`
- required eligibility: `BlockedMultiple`
- required execution: `d0r2-14196acbf30d92b8b5f4`

Required parent blocker set:

- `lhs_physical_layout_not_proven`
- `rhs_post_swap_physical_layout_not_contiguous`
- `raw_buffer_lease_preconditions_incomplete`
- `wgpu_version_split`

D0R2R1 clears only `wgpu_version_split`.

## 3. Confirmed Root Cause

The runtime type split was caused by two different concepts being treated as the same version axis:

- Burn crate release version `0.20.0`;
- concrete WGPU package generation used by Device, Queue and Buffer.

The inspected source confirms:

- `burn_webgpu_backend` carried an unused direct dependency `wgpu = "0.20"`;
- active raw bridge code used `wgpu26`;
- `burn-wgpu-local::gpu_api` re-exported `wgpu26`;
- vendor runtime handles used that `gpu_api` authority;
- TensorCube native modules used `wgpu26`.

Burn release `0.20.0` must not be interpreted as WGPU generation `0.20`.

## 4. Purpose

D0R2R1 establishes one concrete runtime WGPU type authority for:

1. Device;
2. Queue;
3. Buffer;
4. raw-buffer lease type;
5. native runtime handles;
6. future TensorCube runtime context;
7. future TensorCube runtime buffer bindings.

The authoritative generation is the concrete generation already used by the Burn raw-resource seam and runtime handles:

`wgpu 26.0.1`

D0R2R1 does not execute a raw lease, create a pipeline, create a command encoder, submit a queue, dispatch TensorCube or alter model output.

## 5. Runtime Authority SSOT

Authoritative module:

`crates/burn_webgpu_backend/src/runtime_wgpu_type_authority.rs`

Required authority constants:

- package name: `wgpu`
- package version: `26.0.1`
- dependency alias: `wgpu26`
- generation label: `wgpu-26.0.1`
- authority ID: `ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`

Required concrete aliases:

- `RuntimeWgpuDevice`
- `RuntimeWgpuQueue`
- `RuntimeWgpuBuffer`
- `RuntimeWgpuAdapter`
- `RuntimeWgpuCommandEncoder`
- `RuntimeWgpuComputePipeline`
- binding and buffer descriptor aliases

Only the authority module may directly bind the authoritative WGPU crate for the repaired runtime seam.

## 6. Dependency Repair

The following dependency is removed from `burn_webgpu_backend`:

```toml
wgpu = "0.20"
```

The following dependency remains authoritative:

```toml
wgpu26 = { package = "wgpu", version = "26.0.1" }
```

This is not a Burn framework upgrade. It removes an unused and misleading direct WGPU dependency.

## 7. Raw Bridge Contract

`raw_bridge.rs` must import runtime types from `runtime_wgpu_type_authority`.

Required aliases:

```rust
pub type BackendDevice = RuntimeWgpuDevice;
pub type BackendQueue = RuntimeWgpuQueue;
pub type BackendBuffer = RuntimeWgpuBuffer;
```

`RawWgpuBufferLease::buffer` therefore belongs to the same concrete type generation as the runtime Device and Queue.

The repair does not call any bridge method during audit.

Required count:

`raw_buffer_lease_count=0`

## 8. Native Runtime Handles Contract

`NativeWgpuRuntimeHandles` must own:

```rust
Arc<RuntimeWgpuDevice>
Arc<RuntimeWgpuQueue>
```

The vendor extraction path must return handles from `burn_wgpu_local::gpu_api`, which is bound to `wgpu26`.

Forbidden:

- replacement Device creation;
- replacement Queue creation;
- cross-generation object conversion;
- pointer or HAL reinterpretation.

## 9. TensorCube Runtime Boundary

The authority module declares type-only future boundaries:

```rust
pub struct TensorCubeRuntimeTypeBoundary<'a> {
    pub device: &'a RuntimeWgpuDevice,
    pub queue: &'a RuntimeWgpuQueue,
}
```

```rust
pub struct TensorCubeRuntimeBufferTypes<'a> {
    pub lhs: &'a RuntimeWgpuBuffer,
    pub rhs: &'a RuntimeWgpuBuffer,
    pub output: &'a RuntimeWgpuBuffer,
}
```

These types are compile contracts only. D0R2R1 does not instantiate or dispatch them.

## 10. Runtime Dependency Closure

The audit invokes:

```text
cargo metadata --locked --format-version 1
```

Runtime closure roots:

- `model_core`
- `burn_webgpu_backend`
- `burn-wgpu-local`

The audit traverses Cargo resolve-node dependencies from those roots and inventories every reachable package named `wgpu`.

PASS requires:

- exactly one runtime-reachable WGPU package;
- version exactly `26.0.1`;
- duplicate runtime generation count `0`;
- unknown runtime generation count `0`.

## 11. Non-Runtime Generation Quarantine

A WGPU package outside the vocab-atlas runtime dependency closure may remain only when:

- `runtime_reachable=false`;
- `exports_runtime_objects=false`;
- it is explicitly listed in the quarantine receipt.

Quarantine never converts WGPU objects between generations.

## 12. Compile-Time Type Proof

Focused tests must prove that:

- `NativeWgpuRuntimeHandles::device` is `Arc<RuntimeWgpuDevice>`;
- `NativeWgpuRuntimeHandles::queue` is `Arc<RuntimeWgpuQueue>`;
- `RawWgpuBufferLease::buffer` is `Arc<RuntimeWgpuBuffer>`;
- future TensorCube boundary aliases use the same types.

The proof is compile-time type assignment, not string comparison alone.

## 13. D0R2 Re-Audit Alignment

The D0R2 audit must no longer derive WGPU generation from the Burn crate release number or the removed `wgpu = "0.20"` line.

It must read `runtime_wgpu_type_authority.rs` and classify:

- Burn runtime generation: `wgpu-26.0.1`;
- bridge generation: `wgpu-26.0.1`;
- TensorCube generation: `wgpu-26.0.1`.

After D0R2R1, a D0R2 re-audit must not emit `wgpu_version_split`.

## 14. Forbidden Cross-Generation Techniques

Forbidden in repaired runtime files:

- `transmute`
- `transmute_copy`
- `ManuallyDrop` bridge
- `Arc::from_raw`
- `Arc::into_raw`
- `Box::from_raw`
- pointer casts
- `repr(C)` WGPU object bridge
- HAL handle reinterpretation
- replacement Device or Queue

Required counts:

- cross-generation conversion `0`
- unsafe generation bridge `0`
- pointer bridge `0`
- HAL reinterpretation `0`

## 15. Execution Prohibitions

D0R2R1 must keep all of the following at zero:

- raw-buffer lease;
- TensorCube dispatch;
- TensorCube output;
- parity comparison;
- queue submit;
- device poll;
- buffer map;
- pipeline creation;
- command encoder creation;
- runtime Device creation;
- runtime Queue creation;
- route mutation;
- downstream output commit.

Burn remains the sole output authority.

## 16. Required Implementation Files

Backend:

- `runtime_wgpu_type_authority.rs`
- `tensorcube_k7n_d0r2r1_wgpu_dependency_closure.rs`
- `tensorcube_k7n_d0r2r1_wgpu_type_compatibility.rs`
- `tensorcube_k7n_d0r2r1_wgpu_generation_quarantine.rs`
- `tensorcube_k7n_d0r2r1_contract_audit.rs`
- `tensorcube_k7n_d0r2r1_verdict.rs`

Modified runtime seam:

- `burn_webgpu_backend/Cargo.toml`
- `raw_bridge.rs`
- `device_handles.rs`
- `burn_webgpu_backend/src/lib.rs`

Orchestrator:

- `ash_tcu_k7n_d0r2r1_wgpu_type_generation_split_prerequisite_repair_report.rs`
- `ash_tcu_k7n_d0r2r1_wgpu_type_generation_split_prerequisite_repair_audit.rs`

Tests:

- runtime authority identity;
- dependency closure;
- concrete type identity;
- quarantine;
- model-core native runtime handle identity.

## 17. Protected State Guard

Protected before and after audit:

- Registry v4;
- R1F final seal;
- D0R2 final seal;
- D0R2 manifest;
- D0R2 WGPU compatibility receipt;
- D0R2 eligibility receipt;
- K6P canonical source;
- vocab-atlas Burn projection semantics;
- model weights;
- route bindings and epoch.

PASS requires no protected artifact rewrite.

## 18. Local Artifacts

Immutable bundle:

`artifacts/tensorcube/k7n_d0r2r1/<execution_id>/`

Latest receipt families:

- prior D0R2 receipt;
- cargo metadata;
- runtime dependency closure;
- WGPU package inventory;
- runtime generation authority;
- Device type identity;
- Queue type identity;
- Buffer type identity;
- quarantined generations;
- direct import audit;
- cross-generation safety;
- blocker clearance;
- protected state guard;
- static checks;
- report;
- final seal;
- verdict;
- local manifest.

Source bake contains no pre-generated D0R2R1 artifacts or SHA sidecars.

## 19. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d0r2r1_wgpu_type_generation_split_prerequisite_repair_audit -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d0r2-pass `
  --require-d0r2-explicit-blocked `
  --require-blocker wgpu_version_split `
  --require-registry-v4 `
  --require-route-epoch 1 `
  --collect-cargo-metadata-locked `
  --resolve-runtime-wgpu-dependency-closure `
  --inventory-all-wgpu-package-generations `
  --assign-runtime-wgpu-generation-authority `
  --bind-device-type-authority `
  --bind-queue-type-authority `
  --bind-buffer-type-authority `
  --verify-native-runtime-handles-use-authority `
  --verify-raw-buffer-lease-type-uses-authority `
  --verify-tensorcube-runtime-boundary-uses-authority `
  --quarantine-non-runtime-wgpu-generations `
  --verify-no-runtime-duplicate-generation `
  --verify-no-direct-runtime-wgpu-imports `
  --verify-no-cross-generation-object-conversion `
  --verify-no-unsafe-generation-bridge `
  --verify-feature-set-compatibility `
  --clear-wgpu-version-split-blocker `
  --require-no-raw-buffer-lease `
  --require-no-tensorcube-dispatch `
  --require-no-pipeline-creation `
  --require-no-command-encoder `
  --require-no-runtime-device-creation `
  --require-no-runtime-queue-creation `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-audit-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-performance-claim
```

## 20. PASS Conditions

- D0R2 blocked receipt is valid;
- prior blocker includes `wgpu_version_split`;
- direct `wgpu = "0.20"` dependency is absent;
- authority dependency is `wgpu26` version `26.0.1`;
- runtime dependency closure contains one WGPU generation;
- Device, Queue and Buffer aliases have one owner;
- native runtime handles use authority aliases;
- raw lease uses authority Buffer;
- future TensorCube boundaries use authority aliases;
- no cross-generation conversion exists;
- no runtime execution or output mutation occurs;
- `wgpu_version_split_before=true`;
- `wgpu_version_split_after=false`.

Expected remaining blockers:

- `lhs_physical_layout_not_proven`
- `rhs_post_swap_physical_layout_not_contiguous`
- `raw_buffer_lease_preconditions_incomplete`

## 21. Final Verdict

`runtime_wgpu_device_queue_and_buffer_type_generation_unified_under_burn_runtime_authority_and_non_authoritative_generations_quarantined_without_raw_buffer_lease_tensorcube_dispatch_or_output_change`

## 22. Explicit Non-Authorization

D0R2R1 PASS does not authorize:

- LHS physical-layout promotion;
- RHS post-swap contiguity claim;
- raw-buffer lease;
- TensorCube pipeline or dispatch;
- parity comparison;
- route registration or epoch change;
- D0R3 candidate closure;
- D1 binding;
- performance or production claims.

## 23. Next State

Only the following patch is authorized after PASS:

`ASH-TCU-K7N-D0R2R2_LHS_RHS_PHYSICAL_LAYOUT_EVIDENCE_CLOSURE`

Required sequence:

```text
D0R2 explicit blocker
-> D0R2R1 WGPU type-generation repair
-> D0R2R2 physical-layout evidence closure
-> D0R2R3 raw-buffer lease prerequisite closure
-> D0R2 re-audit
-> D0R3 candidate closure audit
-> D1 single shadow consumer contract
```
