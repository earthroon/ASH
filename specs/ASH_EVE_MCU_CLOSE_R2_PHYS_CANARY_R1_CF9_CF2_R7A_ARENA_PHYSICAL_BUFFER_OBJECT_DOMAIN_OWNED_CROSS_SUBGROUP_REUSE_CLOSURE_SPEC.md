# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF2

## R7A ARENA PHYSICAL BUFFER OBJECT
## DOMAIN-OWNED CROSS-SUBGROUP REUSE CLOSURE

```text
+ GLOBAL ARENA PAGE / BUFFER OBJECT SINGLE AUTHORITY
+ ArenaPage PHYSICAL BUFFER OWNERSHIP
+ DEVICE / QUEUE DOMAIN OBJECT IDENTITY
+ SUBGROUP-LOCAL ARENA OBJECT REGISTRY RETIREMENT FOR R7A
+ SAME-DOMAIN CROSS-SUBGROUP REUSE
+ SESSION ↔ RESIDENT-GRAPH BUFFER OBJECT PARITY
+ INCARNATION ADVANCE ON ARENA AUTHORITY
+ REUSE-HIT PHYSICAL OBJECT WITNESS
+ PACKED-GRADIENT PRODUCER / READER SAME-OBJECT WITNESS
+ NO CROSS-DEVICE REUSE
+ NO CROSS-QUEUE REUSE
+ NO DUPLICATE Arc<wgpu::Buffer> AUTHORITY
+ LEGACY A02 PATH PRESERVATION
+ NO DIRECT-CREATE FALLBACK
```

---

## 0. Revision identity

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF2

Class:
PHYSICAL OBJECT AUTHORITY CLOSURE
R7A DOMAIN-OWNED BUFFER REUSE

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF1
```

Parent code-only archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF1_R7A_RESOURCE_GEOMETRY_BOOTSTRAP_DOMAIN_BIND_RESEAL_ORDERING_CLOSURE_CODE_ONLY.zip
```

Current physical first failure before this revision:

```text
E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
```

The failing run had exact device/queue/domain lineage and reached the R7A1 packed-gradient reader under a ResidentGraph subgroup, so this revision does not reopen CF8 lease geometry, CF9 byte/page geometry, CF9-CF1 domain ordering, R1J subgroup selection, or R1K candidate routing.

---

## 1. Root cause

The R7A allocator had split physical authority:

```text
GLOBAL ArenaRuntime / ArenaPage
    page id
    physical allocation id
    capacity
    domain digest
    incarnation
    reuse eligibility
```

but the actual WGPU object lived in:

```text
McuDeviceSoftSubgroupHandleR1A.inner.arena_buffers
    PhysicalAllocationId -> Arc<wgpu::Buffer>
```

The global R7A pool is keyed by exact device/queue/pool/domain geometry and can legally select a free page created by another subgroup. The subsequent subgroup-local object lookup could therefore fail even though the global page metadata remained exact.

CF9-CF2 removes that split for R7A only.

---

## 2. Core law

For R7A:

```text
ArenaPage metadata authority
==
ArenaPage physical buffer authority
==
R7A reuse incarnation authority
```

A subgroup remains an execution caller and queue/device provenance witness. It is not the physical object registry for an R7A domain-owned page.

Legacy A02 remains subgroup-local.

---

## 3. ArenaPage physical ownership

`ArenaPage` gains:

```rust
r7a_buffer: Option<Arc<wgpu::Buffer>>
```

Authority split:

```text
Legacy A02 page:
    r7a_domain_digest = None
    r7a_buffer = None

R7A page:
    r7a_domain_digest = Some(exact_domain)
    r7a_buffer = Some(exact_buffer)
```

This keeps the existing shared page metadata type while preventing a forced migration of Legacy A02.

---

## 4. Legacy A02 preservation

Historical `acquire_arena_buffer(...)` continues to use:

```text
subgroup.insert_arena_buffer(...)
subgroup.advance_arena_buffer_generation(...)
subgroup.arena_buffer(...)
```

Legacy reuse is additionally restricted to:

```text
r7a_domain_digest == None
```

so a Legacy A02 caller cannot accidentally adopt an R7A domain-owned page from the shared physical pool.

No Legacy A02 physical object authority is changed by this revision.

---

## 5. R7A new-page publication

R7A new page creation now publishes the physical object directly into the global arena page:

```text
register PhysicalAllocationId
create wgpu::Buffer
publish ArenaPage {
    exact page id
    exact physical allocation id
    exact R7A domain
    incarnation = 1
    r7a_buffer = Some(Arc<Buffer>)
}
```

R7A no longer calls:

```text
subgroup.insert_arena_buffer(...)
```

for a new page.

Required witness:

```text
[ASH-MCU-R7A-CF9-CF2][new-page-object]
object_authority=R7A_DOMAIN
subgroup_registry_inserted=false
```

---

## 6. R7A reuse hit

R7A reuse now performs:

```text
lock ArenaRuntime
find exact free page in exact pool + exact domain
resolve page.r7a_buffer
checked incarnation + 1
mark in_use
materialize receipt
clone Arc<Buffer>
unlock
return ArenaLease
```

R7A reuse no longer calls:

```text
subgroup.advance_arena_buffer_generation(...)
subgroup.arena_buffer(...)
```

The previous subgroup-local `E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING` path is therefore retired from R7A reuse.

---

## 7. Incarnation authority

R7A reuse changes incarnation with checked arithmetic on `ArenaPage`:

```text
previous_incarnation
-> checked_add(1)
-> next_incarnation
```

Overflow fails with:

```text
E_MCU_R7A_ARENA_INCARNATION_OVERFLOW
```

There is no second R7A generation counter in a subgroup-local object registry.

---

## 8. Domain-owned object resolver

CF9-CF2 materializes:

```text
resolve_r7a_buffer_object_cf9_cf2(...)
```

It resolves an R7A physical object using exact:

```text
domain digest
device authority
queue authority
PhysicalAllocationId
ArenaPage ordinal
incarnation
```

Required fail-closed guards include:

```text
E_MCU_R7A_ARENA_DOMAIN_MISSING
E_MCU_R7A_ARENA_PHYSICAL_PAGE_MISSING
E_MCU_R7A_ARENA_DEVICE_AUTHORITY_DRIFT
E_MCU_R7A_ARENA_QUEUE_AUTHORITY_DRIFT
E_MCU_R7A_ARENA_DOMAIN_DRIFT
E_MCU_R7A_ARENA_PAGE_NOT_ACTIVE
E_MCU_R7A_ARENA_STALE_INCARNATION
E_MCU_R7A_ARENA_PHYSICAL_BUFFER_MISSING
```

No fallback allocation is permitted.

---

## 9. Same-domain cross-subgroup reuse

Same `McuDeviceSoftSubgroupHandleR1A.inner` identity is not an R7A reuse prerequisite.

Required R7A reuse authority is:

```text
same DeviceAuthorityId
same QueueAuthorityId
same R7A domain digest
same ArenaPage / PhysicalAllocationId authority
valid current incarnation
```

This permits Session-originated and ResidentGraph-originated callers to share one exact physical arena page without mirroring registries.

---

## 10. No cross-device reuse

The domain-owned resolver requires exact device parity between:

```text
binding / requested device
PhysicalAllocationId.device_id
ArenaPageId.device_id
ArenaPoolKey.device_id
```

A mismatch fails closed.

---

## 11. No cross-queue reuse

The exact pool key queue authority must equal the requested domain/binding queue authority.

A page cannot become device-wide but queue-agnostic through CF9-CF2.

---

## 12. No cross-domain reuse

The page's R7A domain digest must equal the current exact resealed domain digest.

Same device/queue/size/usage does not authorize reuse across a different policy/domain identity.

---

## 13. Reuse-hit witness

R7A reuse emits:

```text
[ASH-MCU-R7A-CF9-CF2][reuse-hit-object]
```

including:

```text
site
semantic role
page ordinal
physical allocation ordinal
previous incarnation
next incarnation
device authority
queue authority
domain digest
object_authority=R7A_DOMAIN
buffer_present=true
subgroup_local_lookup=false
```

This is the primary witness that the old subgroup registry path is no longer involved.

---

## 14. Packed-gradient producer object parity

`PackedGradientReadBindingR7A1::new(...)` resolves the arena-owned object and compares it with the producer `ArenaLease.buffer` using process-local:

```rust
Arc::ptr_eq(...)
```

Required witness:

```text
[ASH-MCU-R7A-CF9-CF2][packed-producer-object]
object_authority=R7A_DOMAIN
same_buffer_arc=true
```

Mismatch fails:

```text
E_MCU_R7A_CF2_PACKED_PRODUCER_BUFFER_OBJECT_DRIFT
```

Pointer values are never serialized.

---

## 15. Packed-gradient reader object parity

Before an R7A1 packed-gradient reader is admitted, CF9-CF2 resolves the exact arena-owned object from the encoded binding and compares it with the `RawWgpuBufferLease.buffer` object.

Required witness:

```text
[ASH-MCU-R7A-CF9-CF2][packed-reader-object]
arena_object_resolved=true
same_buffer_arc=true
```

Mismatch fails:

```text
E_MCU_R7A_CF2_PACKED_READER_BUFFER_OBJECT_DRIFT
```

This witness is valid even when the reader subgroup has a different `inner` from the producer subgroup.

---

## 16. Packed-gradient metadata preservation

CF9-CF2 does not add an Arc or pointer to `PackedGradientReadBindingR7A1`.

The durable binding remains metadata-only:

```text
PhysicalAllocationId
QueueAuthorityId
R7A domain digest
ArenaPage ordinal
incarnation
logical size
identity digest
```

---

## 17. R7A1 lifetime preservation

Packed-gradient reclaim still requires exact multi-consumer retirement authority.

CF9-CF2 does not change:

```text
producer lease lifetime
consumer lease lifetime
A01 exact completion requirement
arena reclaim timing
stale incarnation rejection
```

A page is not made reusable merely because its object authority moved to ArenaPage.

---

## 18. Reclaim law

`reclaim_arena_lease_in_domain_r7a(...)` continues to mark the exact page free only after existing A01 eligibility checks.

Reclaim changes:

```text
page.in_use = false
```

but preserves:

```text
page.r7a_buffer = Some(exact physical buffer)
```

so the retained page can be reused later.

---

## 19. No duplicate Arc authority

Allowed Arc holders:

```text
ArenaPage authority
ArenaLease consumer clone
RawWgpuBufferLease consumer clone
short-lived caller clone
```

Forbidden R7A authority split:

```text
ArenaPage authority
+
subgroup.arena_buffers authority
```

CF9-CF2 removes the second authority for R7A new/reused pages.

---

## 20. No registry-copy workaround

Forbidden:

```text
current subgroup misses page
-> copy producer subgroup registry entry
```

Forbidden:

```text
search all subgroup registries
```

Forbidden:

```text
force reader to producer subgroup
```

The domain itself owns the R7A object.

---

## 21. No direct-create fallback

If exact page metadata exists but the domain-owned buffer object is missing, fail:

```text
E_MCU_R7A_ARENA_PHYSICAL_BUFFER_MISSING
```

Do not create another buffer under the old page/allocation identity.

---

## 22. CF8 / CF9 / CF9-CF1 preservation

CF9-CF2 does not modify:

```text
CF8 exact Adam segment geometry
CF8 active lease ceiling
CF9 retained-byte floor
CF9 page-count floor
CF9 three-axis resource seal
CF9-CF1 bootstrap bind ordering
CF9-CF1 warm-domain reuse
```

No resource budget is increased by this revision.

---

## 23. R1J preservation

R1J remains the authority for selecting the reader subgroup.

A ResidentGraph reader is legal when device/queue authority is exact.

CF9-CF2 does not rewrite it to SessionInjected merely to avoid the previous page lookup failure.

---

## 24. Source delta

CF9-CF2 code delta is exactly:

```text
ADD 0
MOD 2
DEL 0
```

Modified files:

```text
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
crates/burn_webgpu_backend/src/himuon_packed_gradient_r7a1.rs
```

Source SHA-256:

```text
d47566a94c315813500266fdab36a9dea571d5a224bd911418e92aeff3a853fc
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs

e7e1163719a568b1589e200f01ce2f9784b59cc9745c736d0cc3ef2d037d754c
crates/burn_webgpu_backend/src/himuon_packed_gradient_r7a1.rs
```

---

## 25. Code-only archive seals

Full code-only:

```text
SHA-256:
96244e8f07d1f4a08901188de0f249efb8730721224830d1b32f03b58d791c48

Files: 8424
CRC: PASS
specs/: 0
artifacts/: 0
```

Overlay code-only:

```text
SHA-256:
db2faae3e6a3481458f379860e35b0ad4e7c68121e63e377fc3c5cde741367c4

Files: 2
CRC: PASS
specs/: 0
artifacts/: 0
```

---

## 26. Static checks

Structural checks establish:

```text
ArenaPage constructors                  2 runtime constructors + type declaration
Legacy r7a_buffer=None                  1
R7A r7a_buffer=Some                     1
R7A subgroup registry calls             0
Legacy A02 subgroup registry calls      preserved
CF9-CF2 object witnesses                materialized
Rust delimiter counts                   balanced in both modified files
UTF-8                                    PASS
```

Existing parent static validators were run before and after the patch.

Results remain unchanged from the CF9-CF1 parent:

```text
R7A validator:
79 / 83 PASS

R7A1 validator:
77 / 82 PASS
```

The remaining failures are pre-existing source-pattern/validator drift in the parent and are not introduced by CF9-CF2. No new validator regression is observed.

---

## 27. Compile boundary

The bake environment does not expose `cargo` / `rustc`.

Therefore:

```text
SOURCE:   STATIC INSPECTED
ARCHIVE:  SEALED / CRC PASS
COMPILE:  NOT CLAIMED
PHYSICAL: NOT CLAIMED
```

Compile authority belongs to the target machine.

---

## 28. Compile acceptance

Required:

```powershell
cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked `
  -j 1
```

Compile success establishes only `COMPILE`.

---

## 29. Native CF1 requirement

Backend physical object ownership changed.

Required:

```text
base_train rebuild = REQUIRED
Native CF1 reseal = REQUIRED
```

CF9-CF1 Native CF1 may not be reused.

---

## 30. Expected physical sequence

Relevant expected evidence:

```text
[ASH-MCU-R7A-CF9-CF2][new-page-object]
    object_authority=R7A_DOMAIN
    subgroup_registry_inserted=false

[ASH-MCU-R7A-CF9-CF2][packed-producer-object]
    same_buffer_arc=true

[ASH-MCU-R7A1-R1J][reader-authority]
    subgroup_source=ResidentGraph
    device/queue exact

[ASH-MCU-R7A-CF9-CF2][packed-reader-object]
    arena_object_resolved=true
    same_buffer_arc=true

[ASH-MCU-R7A-CF9-CF2][reuse-hit-object]
    object_authority=R7A_DOMAIN
    subgroup_local_lookup=false
```

---

## 31. Previous blocker retirement

The ordinary R7A path must no longer fail with:

```text
E_DEVICE_SOFT_SUBGROUP_ARENA_PAGE_MISSING
```

If that error remains, the failing caller must first be classified as:

```text
R7A domain-owned path
or
Legacy A02 subgroup-local path
```

before another repair is accepted.

---

## 32. Physical PASS boundary

CF9-CF2 is physically supported when one CANARY run proves:

```text
R7A page object is domain-owned
R7A new pages skip subgroup registry insertion
R7A reuse skips subgroup registry lookup
same device exact
same queue exact
same domain exact
same physical allocation exact
incarnation advances once on ArenaPage
packed producer object parity exact
packed reader object parity exact under ResidentGraph reader
previous subgroup-local page-missing failure retired
```

Reserved token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF2
```

---

## 33. Non-claims

CF9-CF2 does not claim:

```text
Legacy A02 domain migration
R7A1 complete physical promotion
packed-gradient lifetime redesign
R3B completion
2-step CANARY completion
Full R1B completion
A/B/C promotion
C08 ActiveAsync promotion
performance promotion
```

---

## 34. Final law

> An R7A arena page is one physical authority. Page metadata and `Arc<wgpu::Buffer>` may not live under different ownership scopes.

> R7A `ArenaPage` owns the physical WGPU buffer and the incarnation used for reuse. A subgroup remains an execution caller, not the physical object registry.

> Same-domain Session and ResidentGraph subgroup callers may reuse the exact same page when DeviceAuthority, QueueAuthority, domain, allocation and incarnation are exact.

> Legacy A02 remains subgroup-local. R7A does not copy registries, search registries, pin readers to producers, or direct-create a replacement buffer.
