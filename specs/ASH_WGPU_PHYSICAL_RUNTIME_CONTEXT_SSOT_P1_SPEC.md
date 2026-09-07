# ASH-WGPU-PHYSICAL-RUNTIME-CONTEXT-SSOT-P1

## PHYSICAL WGPU RUNTIME CONTEXT SSOT
## + DETACHED DEVICE/QUEUE AUTHORITY RETIREMENT
## + PRODUCTION LEAF SUBGROUP PASS-THROUGH

### 0. Revision

```text
Patch ID:
ASH-WGPU-PHYSICAL-RUNTIME-CONTEXT-SSOT-P1

Class:
FOUNDATIONAL RUNTIME IDENTITY CUT
PHYSICAL AUTHORITY PASS-THROUGH
CURRENT R7 PRODUCTION PATH ADOPTION

Direct parent:
ASH_PASS3_BURN_FUSION_EXTERNAL_PRIMITIVE_TOKEN_PASS_THROUGH_R1_CODE_ONLY.zip

Parent SHA-256:
48e75a915417166b669533142ebbe0ac775868d18f10cd680baea0242c7de0f1
```

Bake qualification:

```text
SOURCE MATERIALIZED
STATIC PASS
CARGO CHECK NOT RUN
RELEASE BUILD NOT RUN
NATIVE NOT RUN
WGPU NOT RUN
PHYSICAL HOLD
```

The bake environment exposes neither Cargo nor rustc. No compile or execution PASS is issued by this document.

---

# 1. Purpose

P1 establishes one canonical physical Device/Queue identity chain for the current R7 production runtime.

Previous production execution could create software-detached `DeviceAuthorityId` / `QueueAuthorityId` values inside subgroup or cache helpers without inheriting identity from the WGPU Device/Queue bootstrap.

P1 changes the production chain to:

```text
actual WGPU request_device
    ↓
WgpuDevice::Existing(existing_id)
    ↓
PhysicalWgpuRuntimeBindingR1
    ↓
NativeWgpuRuntimeHandles
    ↓
production scheduler
    ↓
McuSessionRuntimeR7
    ↓
McuDeviceSoftSubgroupHandleR1A
    ↓
MuonResidentStateGraph
    ↓
production Muon / A01 / A02 / A03 execution
```

Physical identity is no longer minted by the current R7 production leaf path.

---

# 2. Identity law

The following identities are distinct:

```text
Physical Device authority
Physical Queue authority
backend Existing device id
physical runtime generation
MCU session identity
subgroup generation
training generation
invocation identity
Atlas wave identity
```

A session or subgroup may inherit a physical identity but may not define a replacement physical identity.

Canonical law:

> Physical WGPU authority originates only after the actual WGPU Device and Queue have been created by the canonical existing-device bootstrap.

---

# 3. PhysicalWgpuRuntimeBindingR1

Materialized in:

```text
crates/burn_webgpu_backend/src/device_handles.rs
```

Shape:

```rust
pub struct PhysicalWgpuRuntimeBindingR1 {
    pub existing_id: u32,
    pub device_authority_id: DeviceAuthorityId,
    pub queue_authority_id: QueueAuthorityId,
    pub runtime_generation: u64,
}
```

It is lightweight identity metadata. It does not own WGPU objects.

Validation requires nonzero Device authority, Queue authority and runtime generation.

---

# 4. Canonical bootstrap authority

Materialized in:

```text
crates/burn_webgpu_backend/src/existing_device_bootstrap.rs
```

After `request_device` and `init_device` yield the actual `WgpuDevice::Existing(existing_id)`, P1 issues exactly one binding for that bootstrap instance:

```text
Physical DeviceAuthorityId
Physical QueueAuthorityId
Physical runtime generation
Existing backend id
```

The resulting `ExistingDeviceBootstrap` exposes the same binding.

Registration/extraction is checked for exact equality:

```text
E_PHYSICAL_WGPU_RUNTIME_BINDING_REGISTRY_DRIFT
```

Overflow is fail-closed.

No pointer-derived or Debug-derived identity is used.

---

# 5. Existing runtime handle bridge

Materialized in:

```text
vendor_fork_scaffold/burn-wgpu-local/src/runtime_handles.rs
crates/burn_webgpu_backend/src/device_handles.rs
```

The pre-existing `runtime_handles` registry continues to hold its existing Arc<Device>/Arc<Queue> payload in P1. P1 does **not** claim to retire that pre-existing WGPU object registry.

P1 adds only the canonical physical identity metadata to the same registration so every `NativeWgpuRuntimeHandles` extraction returns the exact bootstrap binding.

This distinction is intentional:

```text
P1 authority SSOT       = bootstrap PhysicalWgpuRuntimeBindingR1
existing object bridge  = unchanged transport/lookup mechanism
```

Therefore P1 alone does not claim to remove every possible WGPU `Send/Sync` obligation from the workspace.

---

# 6. Subgroup physical binding

Materialized in:

```text
crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs
```

New bound constructors:

```text
new_with_physical_runtime_r1
new_with_physical_runtime_and_chunks_r1
```

A physically bound subgroup receives Device/Queue authority from `PhysicalWgpuRuntimeBindingR1`.

It may not remint those identities.

It retains independent subgroup generation and existing arena/transfer ownership.

Exact binding checks reject:

```text
E_PHYSICAL_WGPU_RUNTIME_NOT_BOUND
E_PHYSICAL_WGPU_SUBGROUP_REBIND_FORBIDDEN
E_PHYSICAL_WGPU_DEVICE_AUTHORITY_DRIFT
E_PHYSICAL_WGPU_QUEUE_AUTHORITY_DRIFT
```

---

# 7. MCU session adoption

Materialized in:

```text
crates/base_train/src/mcu_session_runtime_r7.rs
```

New physical constructor:

```text
McuSessionRuntimeR7::new_with_physical_runtime_r1
```

The constructor creates its Soft Subgroup from the inherited physical binding.

New queue binding surface:

```text
bind_device_queue_with_physical_r1
```

Before Device/Queue child identity is admitted it verifies that:

```text
session physical binding
== expected bootstrap binding
== subgroup physical binding
```

A physically admitted production session without a binding is fail-closed in the current R7 production construction path.

---

# 8. Production scheduler pass-through

Materialized in:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

The scheduler already extracts `NativeWgpuRuntimeHandles` from the active WGPU device.

P1 now passes:

```text
native_handles.physical_runtime_binding_r1
```

into both current R7A production Muon construction variants and into the R1B Device/Queue child binding.

The scheduler does not mint a new Device/Queue authority.

---

# 9. Resident graph / subgroup single line

Materialized in:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/muon_resident_state_graph.rs
```

The current R7 production construction order is changed to:

```text
physical binding
    ↓
McuSessionRuntimeR7
    ↓
session Soft Subgroup
    ↓
MuonResidentStateGraph::new_with_soft_subgroup_r1a
```

The resident graph therefore reuses the session's subgroup rather than creating another subgroup for the same production runtime.

This is the core P1 physical pass-through line.

---

# 10. Production leaf adoption

The current production Muon paths reuse the resident/session subgroup.

Modified:

```text
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_pending_p5_r1.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
```

Specifically:

```text
pending P5
    resident_graph.soft_subgroup_r1a()

active-device pending
    resident_graph.soft_subgroup_r1a()

parameter assembly R2
    caller-supplied subgroup

local Muon production with resident graph
    resident graph subgroup

fused-pair production with resident graph
    resident graph subgroup
```

The active production R7/Atlas path no longer creates a replacement subgroup at those leaves.

---

# 11. R7A1 packed-gradient pass-through

`pack_tracked_r7a1` no longer creates its own subgroup.

The current production caller supplies:

```text
self.mcu.parent_r7.device_soft_subgroup_r1a()
```

Thus the packed-gradient arena allocation participates in the same physical Device/Queue authority line as the parent R7 session.

Existing R7A1 lease and exact consumer semantics remain unchanged.

---

# 12. Kernel-cache identity correction

Materialized in:

```text
crates/burn_webgpu_backend/src/mcu_device_kernel_cache_r7a.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
```

Previous helper behavior:

```text
receive Queue
ignore Queue
mint McuQueueAuthorityBindingR1A::new_detached()
return detached DeviceAuthorityId
```

P1 behavior:

```text
receive already-bound McuQueueAuthorityBindingR1A
validate nonzero Device/Queue IDs
return inherited DeviceAuthorityId
```

Cached Muon constructors now receive the R7 session subgroup queue binding explicitly.

Cache identity no longer manufactures physical Device identity.

---

# 13. Non-goals

P1 does not modify:

```text
Soft Tensor Matrix coordinate topology
Soft Tensor Atlas scheduler
Adam / HiMuon mathematics
R3C / R3C1 commit semantics
A01 SubmissionEpoch semantics
A02 reclaim semantics
A03 staging bytes/lifecycle
Fusion token semantics
FastMemory
MIRASASH
```

P1 also does not claim to delete every legacy/synthetic subgroup constructor from the repository.

---

# 14. Remaining detached/synthetic constructor inventory

After this bake, eight `McuDeviceSoftSubgroupHandleR1A::new_default()` references remain in source.

They are outside the newly bound current R7 production chain and fall into legacy/qualification/compatibility categories:

```text
crates/base_train/src/mcu_device_resource_runtime_r7a.rs
    legacy device-resource constructor

crates/base_train/src/mcu_session_runtime_r7.rs
    legacy session constructor

crates/burn_webgpu_backend/src/async_submission_retirement.rs
    qualification path

crates/burn_webgpu_backend/src/gpu_evidence_compaction.rs
    qualification path

crates/burn_webgpu_backend/src/muon_resident_state_graph.rs
    legacy graph constructor

crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
    compatibility fallback when no resident graph is supplied

crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
    compatibility fallback when no resident graph is supplied

crates/burn_webgpu_backend/src/base_train_r5_optimizer_continue.rs
    older generation2 deterministic-resume path
```

P1 does not falsely claim repository-wide detached-constructor deletion.

P2 must consume only the physically bound R7 production path. Any future promotion of one of the legacy paths to production must first migrate it to the physical binding ABI.

---

# 15. Fail-closed law

For the current physically admitted R7 production construction path:

```text
admitted MCU session + no PhysicalWgpuRuntimeBindingR1
    → E_PHYSICAL_WGPU_RUNTIME_NOT_BOUND
```

Physical binding mismatch does not fall back to a detached subgroup.

No `unsafe impl Send`, `unsafe impl Sync`, raw-pointer authority or recursion-limit workaround is introduced.

---

# 16. Relationship to the outstanding E0275

Current observed release blocker before P1:

```text
error[E0275]: overflow evaluating the requirement
validation::NumericDimension: Sync
```

P1 does **not** claim this is solely caused by detached identity minting.

The following result matrix applies after the bake is compiled by the user:

```text
release base_train lib PASS
    → P1 release compile PASS

release base_train lib still E0275
    → P1 physical authority normalization remains valid
    → exact outer Send/Sync obligation remains OPEN
```

Do not increase `recursion_limit` to qualify P1.

---

# 17. Static acceptance actually executed

Focused P1 source contract:

```text
14 / 14 PASS
```

Existing regression validators:

```text
R7A                 83 / 83 PASS
R7                  55 / 55 PASS
R7B                 83 / 83 PASS
R7A1                82 / 82 PASS
Eve R3G             35 / 35 PASS
R3C                 18 / 18 PASS
R3C1                30 / 30 PASS
vendor/storage     117 / 117 PASS
active-device pending handoff PASS
device-segmented source direct submit PASS
```

One unrelated AdamW pending-generation validator reports the same two stale failures in both parent and P1 working trees:

```text
runtime_scheduler_owner
runtime_target_generation_owner
```

Parent status = 1
P1 status     = 1

It is recorded as a pre-existing baseline failure, not counted as a P1 regression and not silently rewritten in this bake.

---

# 18. Toolchain qualification

Bake environment:

```text
cargo: unavailable
rustc: unavailable
```

Therefore:

```text
borrow checking   NOT RUN
Rust type checking NOT RUN
release codegen   NOT RUN
linking           NOT RUN
native tests      NOT RUN
WGPU execution    NOT RUN
```

Any compile PASS must come from the user's Rust environment.

---

# 19. Required compile commands

Run in this order:

```powershell
cargo check -p burn_webgpu_backend --lib
cargo check -p base_train --lib

cargo build -p burn_webgpu_backend --lib --release -j 1
cargo build -p base_train --lib --release -j 1

cargo build -p base_train `
  --bin ash_basetrain_eve_mcu_close_phys_r1 `
  --release -j 1
```

The most important gate for the currently observed E0275 is:

```powershell
cargo build -p base_train --lib --release -j 1
```

---

# 20. Required native commands

After release compile passes:

```powershell
cargo test -p burn_webgpu_backend --lib -j 1 --no-fail-fast
cargo test -p base_train --lib -j 1 --no-fail-fast
```

Broad historical `cargo test --tests` is not the primary P1 gate.

---

# 21. P2 handoff

P1 answers:

```text
WHO is the physical Device/Queue authority?
```

P2 must answer:

```text
WHICH AdamM/AdamV segment resolves to WHICH existing physical storage/range/lease?
```

P2 begins from the physical line materialized here:

```text
bootstrap binding
→ R7 session
→ same subgroup
→ resident graph
→ production wave/leaf
```

P2 must not create another Device/Queue identity system.

---

# 22. Actual bake record

```text
ADD 0
MOD 15
DEL 0
```

Modified files:

```text
crates/base_train/src/mcu_session_runtime_r7.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_pending_p5_r1.rs
crates/burn_webgpu_backend/src/device_handles.rs
crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs
crates/burn_webgpu_backend/src/existing_device_bootstrap.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/mcu_device_kernel_cache_r7a.rs
crates/burn_webgpu_backend/src/muon_resident_state_graph.rs
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
tools/validate_ash_mcu_device_lifetime_kernel_cache_bounded_buffer_arena_r7a_static.py
vendor_fork_scaffold/burn-wgpu-local/src/runtime_handles.rs
```

The validator modification updates one stale cached-constructor source expectation from the old two-argument call to the new explicit queue-binding call. It does not relax the R7A contract.

---

# 23. Artifacts

Overlay:

```text
ASH_WGPU_PHYSICAL_RUNTIME_CONTEXT_SSOT_P1_OVERLAY.zip
SHA-256: b93994fc05dd57fe584466746843ccc4a27a7a843cb6b3234ee9b86a2027d599
Bytes: 380,893
Files: 15
CRC: PASS
Duplicate paths: 0
PowerShell files: 0
Generated spec/artifact roots: 0
```

Full code-only bake:

```text
ASH_PASS3_WGPU_PHYSICAL_RUNTIME_CONTEXT_SSOT_P1_CODE_ONLY.zip
SHA-256: a0a86eda600105041fd7357708f02dc87fc6c7d7a3c79d947b490faf4788d0fb
Bytes: 21,386,966
Files: 8,414
CRC: PASS
Duplicate paths: 0
PowerShell files: 0
Generated spec/artifact roots: 0
```

Validation logs:

```text
ASH_WGPU_PHYSICAL_RUNTIME_CONTEXT_SSOT_P1_VALIDATION_LOGS.zip
SHA-256: daa8eb2defb5642b25e0d689fa6eabe0639b7e4aa7dea858930c9329d877dff9
```

---

# 24. Final law

> Physical Device/Queue authority starts at the actual existing-device bootstrap.
>
> The current R7 production scheduler passes that authority into the MCU session rather than allowing leaf code to invent a replacement identity.
>
> The MCU session, resident graph, packed-gradient path, active-device pending path and cached Muon construction reuse the same subgroup/queue binding in the current production chain.
>
> Legacy and qualification detached constructors are not misreported as deleted. They remain non-authoritative for the P1 production path and must be migrated before any future production promotion.
>
> P1 normalizes physical authority. It does not claim to solve the outstanding WGPU-core E0275 until release codegen proves that result.
