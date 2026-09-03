# ASH-MCU-DEVICE-LIFETIME-KERNEL-CACHE-AND-BOUNDED-BUFFER-ARENA-R7A

## 0. Revision

```text
Patch ID:
ASH-MCU-DEVICE-LIFETIME-KERNEL-CACHE-AND-BOUNDED-BUFFER-ARENA-R7A
Short name: ASH MCU SESSION R7A
Status: STATIC MATERIALIZATION RELEASE
Rust compile PASS: NOT CLAIMED
GPU physical PASS: NOT CLAIMED
```

Static token:

```text
PASS_ASH_MCU_DEVICE_LIFETIME_KERNEL_CACHE_AND_BOUNDED_BUFFER_ARENA_R7A_STATIC
```

Physical state:

```text
HOLD_ASH_MCU_DEVICE_RESOURCE_R7A_PHYSICAL_PENDING
```

## 1. Parent and Scope

Direct parent:

```text
ASH-MCU-SESSION-PERSISTENT-EXECUTION-FABRIC-AND-OPTIMIZER-INDEPENDENT-JOB-AUTHORITY-R7
```

R7A preserves R7 execution/job authority and the historical A00/A01/A02/A03 WGPU resource lineage. R7A changes physical WGPU resource lifetime only. It does not change Adam or HiMuon mathematics, optimizer routing, Eve authority, Weight authority, durability, or R3C/R3C1 TrainableGeneration commit semantics.

## 2. Core Law

```text
immutable kernel object lifetime = DeviceAuthority lifetime
reusable mutable buffer domain   = DeviceAuthority + QueueAuthority
optimizer execution authority    = MCU session lifetime
logical mutable lease            = job / SubmissionEpoch lifetime
```

A physical buffer may be reused only after exact lifetime evidence proves its previous logical lease is dead. Physical reuse never transfers semantic optimizer authority.

## 3. Device Kernel Cache

New backend module:

```text
burn_webgpu_backend::mcu_device_kernel_cache_r7a
```

Materialized ABI:

```text
McuKernelBundleKindR7A
McuKernelCacheKeyR7A
McuKernelCacheTelemetryR7A
```

Initial bundle kinds:

```text
AdamWActiveDeviceR1
HiMuonGradientPackR1
HiMuonBatch
```

The cache key binds exact `DeviceAuthorityId`, bundle kind, shader-set digest, bind-group ABI digest, pipeline-layout digest, capability digest and backend-revision digest. Generation, parameter, Wave and session ordinals are not kernel compatibility keys.

A new DeviceAuthorityId always creates a new cache domain. R7A is process-local and does not persist WGPU handles across device recreation or process restart.

Same-key concurrent construction is serialized through a build cell so an identical ready bundle is published once. Partial bundle publication is forbidden.

## 4. Adam Kernel Adoption

`cached_adamw_producer_r7a` caches an `Arc<AdamWActiveDeviceCandidateProducerR1>` per exact kernel key. The producer contains the AdamW pipeline/layout authority and one persistent zero-gradient fallback buffer.

When R7A kernel-cache admission is active, `McuSessionRuntimeR7` obtains its Adam producer from this device cache. Historical R7 session-persistent construction remains the compatibility branch when R7A is disabled.

## 5. HiMuon Kernel Adoption

`TensorCubeLocalMuonGradientPacker` is split from its immutable kernel bundle and can borrow a cached bundle.

`TensorCubeLocalMuonBatchExecutor` is split into:

```text
TensorCubeLocalMuonKernelBundleR7A
    immutable layouts/pipelines/capability

TensorCubeLocalMuonBatchExecutor
    Arc<kernel bundle>
    executor-local mutable tensor-data cache
```

Mutable tensor/data residency is explicitly not stored in the device kernel cache. Historical mixed-precision R7 execution-expert witness fields remain materialized.

## 6. Bounded Arena Successor

R7A extends historical A02 with:

```text
McuArenaDomainIdR7A
McuArenaBudgetSealR7A
McuArenaTelemetryR7A
acquire_arena_buffer_in_domain_r7a
reclaim_arena_lease_in_domain_r7a
```

Historical A02 acquire/reclaim entry points remain unchanged.

The R7A arena domain binds `DeviceAuthorityId`, `QueueAuthorityId`, policy digest and domain digest. Historical A02 pages are not silently reinterpreted as R7A pages.

## 7. Arena Budget

Active R7A arena admission requires non-zero bounds for:

```text
max retained bytes
max page count
max in-flight leases
control size quantum
bulk size quantum
```

Domain-aware acquire checks device/queue authority, WGPU buffer and binding limits, lease count, retained bytes and page count. Capacity is reserved before a miss allocates a new page so concurrent misses cannot independently overrun the sealed budget.

If an R7A-authoritative request cannot fit safely, it fails closed. There is no hidden direct-create fallback outside the budget.

## 8. A01 Lifetime Authority

A01 remains the physical lifetime authority. R7A reuses `PhysicalAllocationId`, logical lease identity and exact SubmissionEpoch evidence.

`ConservativeUnknown` completion is not sufficient for R7A reuse.

A site-scoped tracked-submission release helper is added so transient Adam params/status/readback sites can retire without prematurely releasing longer-lived candidate/source sites.

## 9. Adam Arena Adoption

R7A materializes an arena-backed Adam source path for execution copies of Weight/M/V. Exact host values are written into bounded arena allocations before A01 submission ownership is attached. Eve R3G remains canonical Adam M/V semantic authority.

R7A Adam submission also uses bounded arena leases for:

```text
parameter uniform
candidate Weight
candidate M
candidate V
status storage
status readback
```

The no-gradient fallback is persistent under the cached Adam producer rather than created per job.

## 10. Candidate Reclaim Law

Candidate Weight/M/V are not reclaimed merely when their original command completes. Their arena backing survives through device-generation ownership and becomes reclaimable only after:

```text
candidate segment dead
AND active readers == 0
AND A01 tracked lifetime allows release
```

This prevents stale physical page reuse while a candidate is still a device input.

## 11. Adam Status Readback Boundary

Adam status readback is currently backed by the bounded R7A readback arena. This revision does not claim migration of Adam status onto the historical A03 compact-readback ring. A03 remains an unchanged parent used by existing paths.

## 12. HiMuon Existing Arena Preservation

Existing Local Muon A02/A03 source/upload/readback paths remain intact. R7A does not replace already-adopted parent resource paths simply to rename them.

## 13. HiMuon Packed-gradient HOLD

The current packed-gradient output remains direct-created and retains explicit:

```text
A01_CONSERVATIVE_UNKNOWN_SUBMISSION
```

because one pack producer may be followed by multiple later HiMuon consumer submissions. Producer completion is not the last reader lifetime event.

Current source truth is therefore:

```rust
MCU_R7A_HIMUON_PACKED_GRADIENT_CONSUMER_RETIREMENT_MATERIALIZED = false;
```

R7A does not claim packed-gradient arena reuse or full gradient-pack parameter-buffer retirement. Its materialized gain on this path is immutable kernel caching.

## 14. BaseTrain Device Resource Runtime

BaseTrain materializes:

```text
McuDeviceResourceConfigR7A
McuDeviceResourceRuntimeR7A
McuDeviceResourceReceiptR7A
```

`McuSessionRuntimeR7` gains R7A resource configuration and surfaces cached Adam/HiMuon executors plus the bounded arena domain/budget.

## 15. Configuration

New config fields:

```text
admit_mcu_device_kernel_cache_r7a
admit_mcu_bounded_buffer_arena_r7a
mcu_r7a_arena_budget_bytes
mcu_r7a_arena_max_pages
mcu_r7a_arena_max_in_flight_leases
```

Defaults are disabled/zero. Active R7A requires MCU SESSION R7. Active bounded arena admission requires explicit non-zero resource bounds.

## 16. Authority Ceiling

R7A owns physical kernel-object and physical allocation reuse only.

It does not own:

```text
Eve Adam M/V semantic state
HiMuon momentum
Weight state
optimizer routing
checkpoint durability
TrainableGeneration commit
```

## 17. Numerical Contract

```text
Adam math changed = false
Adam precision changed = false
HiMuon math changed = false
HiMuon reduction order changed = false
optimizer route changed = false
R3G lease semantics changed = false
R3C/R3C1 commit semantics changed = false
```

Physical parity remains required before promotion.

## 18. Static Validation

Validator:

```text
tools/validate_ash_mcu_device_lifetime_kernel_cache_bounded_buffer_arena_r7a_static.py
```

Current result:

```text
73 / 73 PASS
PASS_ASH_MCU_DEVICE_LIFETIME_KERNEL_CACHE_AND_BOUNDED_BUFFER_ARENA_R7A_STATIC
```

The validator explicitly requires packed-gradient multi-consumer arena cutover to remain unclaimed.

## 19. Parent Regression

Current code-only bake retains static PASS for:

```text
Eve R3G                         35 / 35
MCU SESSION R7                 55 / 55
Unified Atlas MCU R6           PASS
Unified Atlas mixed R7         PASS
SubmissionEpoch active async   PASS
Eve/HiMuon R3C                 18 / 18
Eve/HiMuon R3C1                30 / 30
Adam durability R3D            41 / 41
Weight durability R3E          52 / 52
HiMuon durability R3F          66 / 66
```

The standalone A01/A02/A03 validators require their Markdown specification files under `specs/`. The requested code-only bake deliberately excludes specifications, so those invocations stop at the missing-spec prerequisite rather than a source assertion. R7A static validation separately checks preservation and use of the relevant A01/A02 source surfaces.

## 20. Compile Boundary

The R7A Python validator passes `py_compile`. Modified Rust files pass UTF-8 and structural balanced-delimiter checks.

The bake environment exposes no `cargo`, `rustc` or `rustfmt`, therefore Rust compile PASS and GPU physical PASS are not claimed.

## 21. Required Physical Qualification

Physical kernel qualification requires compatible cross-session cache hits under the same DeviceAuthorityId, no hit after device-authority replacement, stable kernel build counts after warm-up and numerical parity.

Physical arena qualification requires:

```text
peak retained bytes <= sealed budget
page count <= sealed bound
active leases <= sealed bound
reuse hits after warm-up
no early reuse while SubmissionEpoch is live
no candidate reuse while an active reader exists
no stale incarnation access
no hidden budget fallback
no numerical divergence
```

Performance qualification must measure pipeline creation, physical buffer creation by role, arena hit/miss rate, retained bytes, active leases, CPU preparation time, Adam segment latency, HiMuon Wave latency and generation wall time. No speedup percentage is claimed statically.

## 22. Physical PASS Token

Reserved:

```text
PASS_ASH_MCU_DEVICE_LIFETIME_KERNEL_CACHE_AND_BOUNDED_BUFFER_ARENA_R7A_PHYSICAL
```

Until qualified:

```text
HOLD_ASH_MCU_DEVICE_RESOURCE_R7A_PHYSICAL_PENDING
```

## 23. Explicit Non-claims

R7A does not claim:

```text
HiMuon packed-gradient arena reuse complete
HiMuon multi-consumer reader retirement complete
all WGPU buffers pooled
all bind groups cached
command encoders pooled
all ASH pipelines globally cached
cross-process WGPU cache
multi-device MCU
tensor-parallel Adam
tensor-parallel HiMuon
device-loss transparent recovery
```

## 24. Direct Successor

Immediate resource-lifetime successor:

```text
ASH-MCU-HIMUON
-PACKED-GRADIENT-EXACT-MULTI-CONSUMER-SUBMISSION-LEASE
-AND-ARENA-REUSE-CLOSURE-R7A1
```

R7A1 must bind the pack producer epoch and every downstream reader epoch, and permit packed-gradient reclaim only after the final exact reader retires.

## 25. Final Law

> A pipeline is a device-authority resource, not a generation resource.

> A physical buffer may outlive one job, but it may be reassigned only after exact lifetime authority proves the old logical lease is dead.

> Warm physical reuse must never be confused with stale semantic-state reuse.
