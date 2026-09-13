# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF3

## LEGACY A02 BUFFER ARENA
## SUBGROUP-OWNED REUSE-SCOPE IDENTITY CLOSURE

```text
+ A02 GLOBAL METADATA-ONLY AUTHORITY PRESERVATION
+ SUBGROUP OBJECT-DOMAIN IDENTITY MATERIALIZATION
+ CLONED-HANDLE SAME OBJECT-DOMAIN IDENTITY
+ ArenaPage LEGACY OWNER-SUBGROUP METADATA
+ LEGACY A02 REUSE SAME-SUBGROUP-ONLY
+ CROSS-SUBGROUP FREE-PAGE REUSE REJECTION
+ RESIDENT-GRAPH LOCAL A02 PAGE MATERIALIZATION
+ SESSION / RESIDENT-GRAPH POOL ISOLATION
+ DEVICE / QUEUE KEY PRESERVATION
+ USAGE / BINDING / SIZE-CLASS PRESERVATION
+ A02 INCARNATION / GENERATION PRESERVATION
+ R7A DOMAIN-OWNED OBJECT PATH PRESERVATION
+ NO GLOBAL A02 Arc<wgpu::Buffer> OWNERSHIP
+ NO SUBGROUP REGISTRY MIRRORING
+ NO SEARCH-OTHER-SUBGROUP FALLBACK
```

---

## 0. Revision identity

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF3

Class:
PHYSICAL REUSE-SCOPE / OBJECT-OWNER IDENTITY CLOSURE

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF2
```

Parent code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF2_R7A_ARENA_PHYSICAL_BUFFER_OBJECT_DOMAIN_OWNED_CROSS_SUBGROUP_REUSE_CLOSURE_CODE_ONLY.zip
```

CF9-CF3 changes Legacy A02 ownership admission only. R7A domain-owned physical object authority from CF9-CF2 remains unchanged.

---

## 1. Parent physical boundary

CF9-CF2 physically established:

```text
R7A new-page object authority = R7A_DOMAIN
subgroup_registry_inserted = false
packed-gradient producer same_buffer_arc = true
```

Execution then entered a `ResidentGraph` reader and failed before the CF9-CF2 packed-reader object witness with:

```text
E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
```

Source attribution shows that after CF9-CF2 the remaining subgroup-local `arena_buffer()` reuse path is Legacy A02 `acquire_arena_buffer()`.

Classification:

```text
LEGACY A02 CROSS-SUBGROUP REUSE-SCOPE DRIFT
```

---

## 2. Existing ownership contract

Legacy A02 preserves the existing Soft Tensor Matrix R1A ownership cut:

```text
GLOBAL / STATIC A02
    = page metadata, allocation identity, telemetry

ACTUAL Arc<wgpu::Buffer>
    = McuDeviceSoftSubgroupHandleR1A local object registry
```

CF9-CF3 MUST NOT move Legacy A02 `Arc<wgpu::Buffer>` objects into process-global/static arena state.

R7A and Legacy A02 intentionally use different object authorities:

```text
R7A
    ArenaPage owns actual Arc<wgpu::Buffer>

Legacy A02
    subgroup-local arena_buffers owns actual Arc<wgpu::Buffer>
```

---

## 3. Root conflict

Legacy A02 global page reuse currently keys physical compatibility by:

```text
device authority
queue authority
usage
binding class
size class
```

but the actual WGPU object is only present in one subgroup-local `arena_buffers` registry.

Therefore two independent subgroup inners can share device/queue identity while not sharing the actual Buffer table.

Current invalid sequence:

```text
Subgroup A creates page P
→ P metadata later becomes free globally
→ actual Buffer remains only in A.arena_buffers

Subgroup B shares device/queue
→ global A02 chooses P
→ B.arena_buffers does not contain P
→ E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
```

---

## 4. Core law

For Legacy A02:

```text
physical object owner scope
==
reuse eligibility scope
```

A Legacy A02 page can be reused only by the same subgroup object domain that owns the corresponding actual WGPU Buffer.

---

## 5. Subgroup object-domain identity

`McuDeviceSoftSubgroupInnerR1A` gains a process-local monotonic identity:

```rust
object_domain_id: u64
```

The identity is allocated once when a new subgroup inner is created.

It is:

```text
process-local
non-zero
monotonic
non-persistent
```

It is not a DeviceAuthorityId, QueueAuthorityId, checkpoint identity, generation, SubmissionEpoch, or pointer address.

---

## 6. Clone identity law

Cloning `McuDeviceSoftSubgroupHandleR1A` preserves the same inner and therefore the same object-domain identity:

```text
clone.object_domain_id
==
original.object_domain_id
```

Two independently created subgroup inners receive distinct object-domain identities even if their device and queue authority IDs are equal.

---

## 7. Explicit API

The subgroup exposes:

```rust
pub fn object_domain_id(&self) -> u64
```

This exposes the explicit process-local owner identity without exposing or serializing an `Rc` pointer address.

---

## 8. ArenaPage Legacy owner metadata

`ArenaPage` gains:

```text
legacy_owner_object_domain_id: Option<u64>
```

Authority classification:

```text
Legacy A02 page:
    r7a_domain_digest = None
    legacy_owner_object_domain_id = Some(X)
    r7a_buffer = None

R7A page:
    r7a_domain_digest = Some(...)
    legacy_owner_object_domain_id = None
    r7a_buffer = Some(...)
```

A page that simultaneously claims a Legacy object owner and R7A domain-owned Buffer authority is invalid.

---

## 9. Legacy new-page publication

Legacy A02 new-page creation continues to:

```text
register physical allocation
→ create Buffer
→ publish global page metadata
→ insert actual Buffer into caller subgroup arena_buffers
```

The page additionally binds:

```text
legacy_owner_object_domain_id
=
caller.object_domain_id
```

No global actual-Buffer ownership is introduced.

---

## 10. Legacy reuse admission

Existing compatibility requirements remain:

```text
same device
same queue
same usage
same binding class
same aligned size class
page free
Legacy A02 ownership class
```

CF9-CF3 adds:

```text
page.legacy_owner_object_domain_id
==
caller.object_domain_id
```

Only after this owner check may the caller invoke the existing subgroup-local generation advance and actual Buffer lookup.

---

## 11. Cross-owner free-page rule

A globally free Legacy A02 page with another owner object domain is not corrupt and does not raise PAGE_MISSING.

It is simply not an eligible reuse candidate:

```text
free=true
same geometry=true
same device/queue=true
same object domain=false
→ SKIP_REUSE
```

The current caller may then reuse a same-owner free page or allocate a new local page subject to existing resource limits.

---

## 12. No owner adoption

Forbidden:

```text
page owned by subgroup A
→ rewrite metadata owner to subgroup B
```

The actual Buffer still belongs to A's registry, so metadata reassignment is not ownership transfer.

---

## 13. No registry mirroring

Forbidden:

```text
copy Arc<Buffer> from subgroup A arena_buffers
into subgroup B arena_buffers
```

This would create duplicate subgroup-local object authorities for one Legacy A02 page.

---

## 14. No cross-registry search fallback

Forbidden:

```text
current subgroup lookup misses
→ scan other subgroup registries
```

Owner mismatch must be resolved at page reuse admission, before physical object lookup.

---

## 15. No forced subgroup convergence

ResidentGraph remains a legitimate independent subgroup authority.

CF9-CF3 does not replace ResidentGraph with the SessionInjected subgroup merely to expose Legacy A02 Buffers.

---

## 16. Global metadata remains global

The A02 runtime remains one global metadata/telemetry authority.

CF9-CF3 does not create separate arena runtimes or separate global pool maps per subgroup.

`object_domain_id` is an additional Legacy page owner/reuse predicate, not a replacement for device/queue/usage/binding/size-class compatibility.

---

## 17. Generic pool-key preservation

The generic arena pool key remains unchanged.

CF9-CF3 intentionally does not add subgroup owner identity to the generic `ArenaPoolKey`, because R7A must continue to support same-domain cross-subgroup reuse.

Legacy owner filtering is applied only to Legacy A02 pages.

---

## 18. R7A preservation

R7A pages remain:

```text
legacy_owner_object_domain_id = None
r7a_buffer = Some(...)
```

R7A reuse continues to be scoped by exact:

```text
DeviceAuthorityId
QueueAuthorityId
R7A domain digest
```

and remains cross-subgroup capable.

CF9-CF3 MUST NOT reintroduce subgroup-local R7A Buffer lookup.

---

## 19. Legacy generation/incarnation preservation

For owner-matched Legacy A02 reuse, existing:

```text
advance_arena_buffer_generation
arena_buffer
```

semantics remain authoritative.

CF9-CF3 does not migrate Legacy A02 incarnation authority to ArenaPage.

---

## 20. Legacy reclaim preservation

Reclaim continues to validate exact allocation, page, incarnation, queue/device authority and A01 completion eligibility before marking metadata free.

Reclaim does not clear `legacy_owner_object_domain_id`, because the retained actual Buffer remains in that subgroup-local registry.

---

## 21. Physical witnesses

Owner mismatch witness:

```text
[ASH-MCU-A02-CF9-CF3][cross-subgroup-skip]
```

Same-owner reuse witness:

```text
[ASH-MCU-A02-CF9-CF3][reuse-candidate]
```

New local page witness:

```text
[ASH-MCU-A02-CF9-CF3][new-local-page]
```

---

## 22. Expected current physical flow

```text
Session subgroup object_domain_id = X
ResidentGraph object_domain_id    = Y
X != Y
```

Then:

```text
ResidentGraph sees free Session-owned Legacy A02 page
→ cross-subgroup-skip
→ ResidentGraph creates/reuses Y-owned local page
→ subgroup local Buffer lookup succeeds
→ execution reaches CF9-CF2 packed-reader object resolution
```

---

## 23. PAGE_MISSING reclassification

After CF9-CF3, an owner-mismatched page must never reach:

```text
E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
```

The error remains valid when the page owner object-domain equals the caller object-domain but the same-owner local registry is actually missing the object.

---

## 24. Resource-budget preservation

CF9-CF3 does not widen retained-byte, page-count, or active-lease ceilings. Cross-subgroup Legacy isolation may increase real page demand. If existing CF9 geometry becomes insufficient, that becomes the next physical boundary and MUST NOT be hidden by arbitrary padding.

---

## 25. Native/static acceptance

```text
subgroup object_domain_id materialized
clone preserves object_domain_id
independent inner receives distinct object_domain_id
Legacy ArenaPage owner metadata materialized
Legacy new page binds caller owner ID
Legacy reuse requires same owner ID
cross-owner free page skipped before subgroup lookup
same-owner reuse preserves old generation/object lookup path
R7A page owner metadata remains None
R7A r7a_buffer path unchanged
no global Legacy A02 Arc<Buffer>
no registry mirroring
no other-subgroup search fallback
```

Materialized unit checks include clone identity, independent-inner identity, and exact Legacy owner predicate checks.

---

## 26. Static validation status of this bake

```text
R7A static validator: 79 / 83 PASS
R7A1 static validator: 77 / 82 PASS
```

These results are unchanged from the direct parent source state. The standalone A02 validator requires its Markdown spec under `specs/`; the code-only tree deliberately excludes specs and therefore stops at that prerequisite. Rust compile/link/GPU execution are NOT RUN in the bake environment and are not claimed.

---

## 27. Code delta

```text
ADD 0
MOD 2
DEL 0
```

Modified files:

```text
crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
```

Source SHA-256:

```text
f50a4cf0444afdeb9e5bc0c62402cac21e6fbc4d50f4f17f33c5aca350761fe4
crates/burn_webgpu_backend/src/device_soft_subgroup_r1a.rs

707c665fa6cfa9dbdde70c13494ff6cf0aea235909f1fbd8df795e4c31364ce8
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
```

---

## 28. Archive seal

Full code-only bake:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF3_LEGACY_A02_SUBGROUP_OWNED_REUSE_SCOPE_IDENTITY_CLOSURE_CODE_ONLY.zip
SHA-256: ffe69c9b7907773cdb05041141b47fed4d5b23e76b30ea150c48c0135364a429
Files: 8424
CRC: PASS
specs/: 0
artifacts/: 0
```

Overlay code-only bake:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF3_LEGACY_A02_SUBGROUP_OWNED_REUSE_SCOPE_IDENTITY_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256: d904d3c7151c13c756aeaa61ecb77f734652e0a8e4d14aba6ec0d9681ee3976e
Files: 2
CRC: PASS
specs/: 0
artifacts/: 0
```

---

## 29. Single-build physical workflow

CF9-CF3 uses the single-build CF1 flow:

```text
apply overlay
→ source SHA verification
→ CF1 release compile authority once
→ CF1 binary SHA == disk EXE SHA
→ 2-step CANARY
```

Do not run a separate full `base_train` release build immediately before CF1 unless diagnosing compilation itself.

---

## 30. Physical PASS boundary

CF9-CF3 is physically supported when one CANARY proves:

```text
Session and ResidentGraph have explicit object-domain identities
cross-owner Legacy A02 free pages are skipped
ResidentGraph creates/reuses only its own Legacy A02 pages
same-owner A02 reuse remains valid
R7A CF9-CF2 domain-owned cross-subgroup path remains valid
cross-owner PAGE_MISSING blocker is crossed
```

Reserved token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF3
```

---

## 31. Explicit non-claims

CF9-CF3 does not claim Legacy A02 global Buffer ownership, merged subgroup pools, continued CF9 budget sufficiency after isolation, complete packed-gradient lifetime, R3B closure, complete 2-step CANARY, Full R1B closure, or A/B/C promotion.

---

## 32. Final law

> Legacy A02 global state owns metadata, not actual WGPU Buffer objects.
>
> Because the actual Buffer lives in one device-soft-subgroup object registry, Legacy A02 reuse eligibility must include that exact subgroup object-domain identity.
>
> A globally free page owned by another subgroup is not adopted, mirrored, searched for, or treated as corrupt. It is skipped.
>
> Handle clones sharing one subgroup inner continue to reuse the same Legacy A02 physical pages. Independent subgroup inners remain physically isolated even when DeviceAuthority and QueueAuthority match.
>
> R7A remains different by design: its ArenaPage owns the actual Buffer, so same-domain cross-subgroup R7A reuse remains legal.
>
> No global Legacy A02 `Arc<wgpu::Buffer>`, no registry mirroring, no search-other-subgroup fallback, no forced subgroup convergence.
