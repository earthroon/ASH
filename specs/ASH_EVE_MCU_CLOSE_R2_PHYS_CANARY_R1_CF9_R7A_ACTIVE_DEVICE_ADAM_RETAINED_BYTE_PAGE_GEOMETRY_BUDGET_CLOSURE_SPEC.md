# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9

## R7A ACTIVE-DEVICE ADAM
## RETAINED-BYTE / PAGE-GEOMETRY BUDGET CLOSURE

```text
+ PRE-REJECT PROJECTED-BYTE / PAGE ATTRIBUTION
+ RETAINED-BYTES / PENDING-RETAINED-BYTES WITNESS
+ PAGE-COUNT / PENDING-PAGE-COUNT WITNESS
+ EXACT SEGMENT RESERVED-BYTE GEOMETRY
+ SOURCE W/M/V RESERVED-BYTE ACCOUNTING
+ CANDIDATE W/M/V GENERATION-RESIDENCY BYTE ACCOUNTING
+ PARAMS / STATUS / READBACK SIZE-CLASS ACCOUNTING
+ 93-SEGMENT ACTUAL GEOMETRY BINDING
+ MAX-PENDING-SEGMENT BYTE OVERHEAD COUPLING
+ DERIVED RETAINED-BYTE FLOOR
+ DERIVED PAGE-COUNT FLOOR
+ CANARY / FULL-R1B SAME RESOURCE-GEOMETRY LAW
+ BYTE / PAGE SEPARATE FAIL-CLOSED ERRORS
+ NO MAGIC 512-MIB PROMOTION
+ NO MAGIC 256-PAGE PROMOTION
+ NO EARLY CANDIDATE RECLAIM
+ NO DIRECT-CREATE FALLBACK
```

---

# 0. Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9

Short name:
R7A-ADAM-RETAINED-BYTE-PAGE-GEOMETRY-BUDGET-CF9

Class:
PHYSICAL RESOURCE-GEOMETRY CLOSURE

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF8
```

Status at bake time:

```text
SOURCE BAKE       COMPLETE
STATIC STRUCTURE  CHECKED
RUST COMPILE      NOT CLAIMED
GPU PHYSICAL      NOT CLAIMED
```

CF9 changes resource geometry only.

```text
Adam math changed          = false
optimizer routing changed  = false
candidate lifetime changed = false
C08 promotion changed      = false
R1K mode policy changed    = false
```

---

# 1. Parent physical boundary

CF8 physically crossed the prior R7A active-lease-count blocker.

Observed parent evidence:

```text
CF8 sealed_max_in_flight_leases = 303
active lease observations       = low 30s at former failure site
old E_MCU_R7A_ARENA_ACTIVE_LEASE_BOUND no longer first failure
```

The new first failure became:

```text
E_MCU_R7A_ARENA_BUDGET_EXHAUSTED:adamw.active.candidate.m
```

The active Adam segment ledger implied by the CF8 physical geometry is currently 93 segments. CF9 does not encode `93` as a generic runtime constant. It consumes the exact CF8 segment ledger and binds byte/page geometry to its count and digest. A physical rerun of this exact campaign is expected to report `segment_count=93` again.

---

# 2. Core correction

R7A owns three independent bounded-arena axes:

```text
max retained physical bytes
max retained physical pages
max active logical leases
```

CF8 closed the third axis.

CF9 closes the first two axes without weakening CF8.

The historical campaign values:

```text
512 MiB retained bytes
256 pages
```

remain bootstrap values only. They are no longer final physical authority after exact Adam geometry is available.

---

# 3. Retained bytes are not active bytes

R7A reclaim retires a logical lease but preserves the physical arena page for compatible reuse.

Therefore:

```text
retained_bytes != sum(active logical lease bytes)
page_count      != active_lease_count
```

A correct planner must model physical pool residency.

This is why CF9 does not multiply the CF8 lease formula by one nominal segment size.

---

# 4. Arena reservation SSOT

CF9 exposes one pure reservation-geometry surface from the existing arena implementation.

It reuses the exact production rules for:

```text
required device alignment
control/bulk quantum selection
reserved-size quantization
usage bits
binding class
storage/uniform device binding limits
max buffer size
```

The production acquire path now calls the same reservation helper.

No duplicate scheduler-side align-up approximation is admitted.

CF9 resource pool identity binds:

```text
device authority id
queue authority id
usage bits
binding class
alignment
reserved size
```

through a stable pool-key digest.

---

# 5. Exact Adam resource roles

The bounded-arena roles remain:

```text
SOURCE
  source Weight
  source M
  source V

CANDIDATE
  candidate Weight
  candidate M
  candidate V

TRANSIENT
  Params
  Status
  StatusReadback
```

Source and candidate W/M/V use the same production storage usage and binding geometry for a given reserved size class.

Params, Status and StatusReadback derive their own actual reservation/pool geometry.

---

# 6. Candidate generation residency

Candidate W/M/V backing remains live after collection until the existing lifetime law permits exact reclaim.

```text
candidate segment dead
AND active readers == 0
AND A01 tracked lifetime permits release
```

CF9 does not alter this law.

For each exact Adam segment `i`:

```text
candidate retained bytes += 3 * segment_reserved_bytes[i]
candidate pages          += 3
```

Thus for the currently observed 93-segment campaign the physical rerun is expected to derive:

```text
candidate_page_floor = 279
```

from the dynamic ledger, never from a hard-coded 279.

---

# 7. Source retained-pool geometry

Source W/M/V logical leases are pending-lifetime resources, but reclaimed pages remain retained.

The exact segment ledger is grouped by the arena storage pool-key digest.

For each storage pool class `k`:

```text
source_segment_slots[k]
  = min(max_pending_segments, segment_count_in_pool_class[k])

source_page_floor[k]
  = 3 * source_segment_slots[k]

source_retained_byte_floor[k]
  = source_page_floor[k] * reserved_size[k]
```

CF9 sums these exact size-class floors.

This preserves reusable source pools without pretending every source submission needs a permanently unique page.

---

# 8. Transient geometry

The actual Adam backend exports the reservation geometry for:

```text
Params
Status
StatusReadback
```

using the same production arena helper.

For each transient role:

```text
transient pages = effective max pending segments
transient bytes = pages * actual reserved size
```

The resource digest binds each transient pool-key and reserved size.

No assumptions such as `Params=256` or `Status=64KiB` are used as final authority even if those values are observed physically.

---

# 9. Derived resource floors

CF9 derives:

```text
candidate_retained_byte_floor
source_retained_byte_floor
transient_retained_byte_floor

DERIVED_RETAINED_BYTE_FLOOR
  = candidate + source + transient
```

and independently:

```text
candidate_page_floor
source_page_floor
transient_page_floor

DERIVED_PAGE_FLOOR
  = candidate + source + transient
```

The page floor is allowed to exceed the active-lease floor because reclaimed pages remain physically retained.

CF9 explicitly does not assert:

```text
page_floor <= lease_floor
```

---

# 10. CF8 preservation

CF9 consumes the parent CF8 values:

```text
segment ledger
segment count
Adam element count
segment geometry digest
max pending segment authority
derived active-lease floor
```

The exact CF8 segment vector is retained internally for CF9 physical planning but is excluded from serialized CF8 receipt output.

Actual submission still must satisfy the existing CF8 terminal guards:

```text
submitted segment count parity
published Adam element parity
segment geometry digest parity
pending-bound parity
```

---

# 11. Atomic three-axis reseal

CF9 performs one pre-execution reseal of:

```text
max_retained_bytes
max_page_count
max_in_flight_leases
```

under one new R7A policy/domain identity.

The existing CF8 lease floor is supplied unchanged as the lease-axis input.

The reseal is allowed only before resource materialization.

Required pre-reseal state:

```text
acquire_count           = 0
retained_bytes          = 0
pending_retained_bytes  = 0
page_count              = 0
pending_page_count      = 0
active_lease_count      = 0
```

Violation fails with:

```text
E_CF9_R7A_ARENA_RESEAL_AFTER_RESOURCE_MATERIALIZATION
```

No mid-generation capacity growth is permitted.

---

# 12. Pre-reject resource attribution

On an arena reuse miss, CF9 computes before reservation:

```text
projected_bytes
projected_pages
byte_admitted
page_admitted
```

and emits:

```text
[ASH-MCU-R7A-CF9][resource-admission]
```

with:

```text
site
semantic role
binding class
logical size
reserved size
retained bytes
pending retained bytes
projected bytes
sealed byte ceiling
byte admitted
page count
pending page count
projected pages
sealed page ceiling
page admitted
active lease count
sealed lease ceiling
domain digest
```

Witness emission precedes fail-closed rejection.

---

# 13. Byte/page failure deconfounding

The previous combined error is retired as the authoritative CF9 Adam new-page rejection.

Exact dispatch:

```text
byte=true  page=true
  -> admit

byte=false page=true
  -> E_MCU_R7A_ARENA_RETAINED_BYTE_BOUND:{site}

byte=true  page=false
  -> E_MCU_R7A_ARENA_PAGE_BOUND:{site}

byte=false page=false
  -> E_MCU_R7A_ARENA_RETAINED_BYTE_AND_PAGE_BOUND:{site}
```

The active-lease bound remains separately fail-closed under CF8.

---

# 14. Pending reservation accounting

CF9 preserves capacity reservation before physical page creation.

On an admitted miss:

```text
pending_retained_bytes += reserved_size
pending_page_count     += 1
```

These two increments use checked arithmetic for CF9 admission.

Physical allocation failure still rolls pending reservation back through the existing path.

---

# 15. Runtime resource-state snapshot

CF9 materializes a domain snapshot containing:

```text
acquire_count
retained_bytes
pending_retained_bytes
page_count
pending_page_count
active_lease_count
peak_active_lease_count
```

It is used for:

```text
pre-reseal proof
post-generation geometry validation
physical summary
```

---

# 16. Post-generation guard

After the exact Adam generation is collected and CF8 segment parity passes, CF9 requires:

```text
observed retained bytes <= derived retained-byte floor
observed page count     <= derived page floor
observed active leases  <= CF8 derived lease floor
```

and emits:

```text
[ASH-MCU-R7A-CF9][generation-resource-summary]
```

If actual residency exceeds the derived model, CF9 fails rather than silently increasing headroom.

---

# 17. Resource-geometry digest

CF9 seals:

```text
ASH.MCU.R7A.CF9.ADAM.RESOURCE.GEOMETRY
```

The digest binds at minimum:

```text
CF8 segment geometry digest
segment indices/ranges/counts
logical bytes
actual reserved size class
pool-key digest
pending bound
control quantum
bulk quantum
device/queue authority ids
candidate/source/transient derived floors
CF8 lease floor
```

No filesystem timestamps or process pointers participate.

---

# 18. CANARY / Full R1B law

For identical:

```text
model
route
gradient segmentation
device reservation geometry
pending bound
```

CANARY and Full R1B derive the same per-generation:

```text
lease floor
retained-byte floor
page floor
resource geometry digest
```

The two-step versus eight-step training horizon does not multiply simultaneous arena capacity.

---

# 19. Explicit non-repairs

CF9 forbids:

```text
512 MiB -> arbitrary larger constant
256 pages -> arbitrary larger constant
early reclaiming candidate W/M/V
reclaiming source before exact completion
reclaiming status/readback before exact completion
lowering max pending segments merely to fit memory
disabling R7A arena
direct device.create_buffer overflow fallback
mid-generation budget reseal
```

If current topology requires substantial retained capacity, CF9 reports that topology honestly. Memory optimization is a later revision.

---

# 20. Expected physical sequence

```text
R1K preflight PASS
CF7 D10 non-promoting profile PASS
CF6 FreshGenesis lifetime exact
CF8 lease geometry PASS

[ASH-MCU-R7A-CF9][pre-reseal-state]
[ASH-MCU-R7A-CF9][adam-resource-geometry]
[ASH-MCU-R7A-CF9][resource-admission] ...

R7A Adam submission continues
```

For the current campaign, expected parent identity includes:

```text
segment_count=93
lease_floor=303
candidate_page_floor=279
```

The last two page/segment numbers must be derived from the runtime ledger, not hard-coded.

---

# 21. Physical pass boundary

CF9 is physically supported when one canonical 2-step CANARY proves:

```text
CF8 exact segment ledger consumed
actual reservation geometry derived
byte/page/lease axes atomically sealed
arena runtime observes the resealed authority
former candidate.m combined budget failure is crossed
no early reclaim is introduced
actual resource state remains within derived floors
```

Recommended token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9
```

CF9 does not claim R3B/full-R1B/A-B-C/C08 promotion completion.

---

# 22. Static bake acceptance

Checked in this bake environment:

```text
Parent full-file count       8424
CF9 full-file count          8424
ADD                          0
MOD                          6
DEL                          0
Rust delimiter structure    balanced on all modified files
Full ZIP CRC                 PASS
Overlay ZIP CRC              PASS
specs/ in code ZIP           0
artifacts/ in code ZIP       0
new generated JSON receipt   0
```

Rust compiler is unavailable in the bake environment.

Therefore:

```text
RUST COMPILE PASS NOT CLAIMED
GPU PHYSICAL PASS NOT CLAIMED
```

---

# 23. Changed files

```text
crates/base_train/src/mcu_device_resource_runtime_r7a.rs
crates/base_train/src/mcu_session_runtime_r7.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/adamw_active_device_candidate_r1.rs
crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
```

Source SHA-256:

```text
3309c01e0dc3c833c5e8f5541ae490d0a59e27f5897e423375aa81ccb8d2c78c  crates/base_train/src/mcu_device_resource_runtime_r7a.rs
acddb0c08702c980adac0e8154b64b52d43a3cfac3c15ae07f6f67ec631d166b  crates/base_train/src/mcu_session_runtime_r7.rs
38d1f0230b2732e8d7761451a5511338e3cf8a289409bf2eebcd768484e1df48  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
a32c5e5165e4a688250c40edb6fdf1b11f033be19197e5541830743706dcdc96  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
0cc7c1d80b7321152fb52ef33dd6609d495168489d85144fb0730efd0538c215  crates/burn_webgpu_backend/src/adamw_active_device_candidate_r1.rs
043370a38ed4ac5942698ea5673e7217ed7aef78aca35cb52e026792b4347b60  crates/burn_webgpu_backend/src/usage_segregated_buffer_arena.rs
```

---

# 24. Archive seal

Full code-only ZIP:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_R7A_ACTIVE_DEVICE_ADAM_RETAINED_BYTE_PAGE_GEOMETRY_BUDGET_CLOSURE_CODE_ONLY.zip
SHA-256 73e817296bda51fac8ed53f90fae6cdaf8ba2ac2a7e11240d845bb64de7cccfd
FILES 8424
CRC PASS
```

Overlay code-only ZIP:

```text
ASH_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_R7A_ACTIVE_DEVICE_ADAM_RETAINED_BYTE_PAGE_GEOMETRY_BUDGET_CLOSURE_OVERLAY_CODE_ONLY.zip
SHA-256 4b8ce9d2e6676e6fcdee13bdeed4e73e857adef6899c851d3655f1684adb00fe
FILES 6
CRC PASS
```

---

# 25. Final law

> The R7A arena retained-byte and page ceilings are physical residency contracts, not historical constants.

> CF9 derives them from the same exact segment ledger closed by CF8 and the same reservation/quantization rules used by the production arena acquire path.

> Candidate W/M/V remain generation-resident. Source and transient pages remain reusable only under exact pool-key compatibility and exact lifetime retirement.

> Byte, page and active-lease admission are independent fail-closed axes.

> No magic 512 MiB, no magic 256 pages, no early candidate reclaim, and no direct-create escape hatch.
