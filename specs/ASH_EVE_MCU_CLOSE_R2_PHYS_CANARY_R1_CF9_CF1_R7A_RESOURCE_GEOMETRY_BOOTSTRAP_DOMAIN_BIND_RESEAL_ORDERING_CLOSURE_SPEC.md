# ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF1

## R7A RESOURCE-GEOMETRY
## BOOTSTRAP DOMAIN-BIND / RESEAL ORDERING CLOSURE

```text
+ CANONICAL DEVICE / QUEUE BIND BEFORE CF9 ARENA LOOKUP
+ ZERO-ALLOCATION BOOTSTRAP DOMAIN MATERIALIZATION
+ BOOTSTRAP DOMAIN / BUDGET WITNESS
+ CF8 SEGMENT-GEOMETRY PRESERVATION
+ CF9 RESOURCE-GEOMETRY DERIVATION AFTER DOMAIN BIND
+ PRE-RESEAL ZERO-STATE PRESERVATION
+ ATOMIC BYTE / PAGE / LEASE RESEAL
+ POST-RESEAL DOMAIN DIGEST WITNESS
+ LATER CANDIDATE bind_device_queue IDEMPOTENCE
+ DEVICE / QUEUE AUTHORITY PARITY GUARD
+ NO ARENA ACQUIRE BEFORE RESEAL
+ NO RESOURCE-BUDGET RELAXATION
+ NO DUPLICATE DOMAIN AUTHORITY
```

---

# 0. Revision

```text
Patch ID:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9-CF1

Class:
ORDERING / AUTHORITY-BINDING CORRECTION FIX

Direct parent:
ASH-EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF9
```

CF9-CF1 changes no Adam mathematics, no CF8 segment geometry, no CF9 byte/page geometry formula, no R7A lifetime law, no C08 authority and no R1K mode policy.

---

# 1. Parent physical first failure

The parent CF9 physical run reached the real R1K ActiveDevice candidate branch and then failed with:

```text
E_MCU_R7A_ARENA_DOMAIN_NOT_BOUND
```

The failure occurs before CF9 can derive or seal the retained-byte/page geometry.

Current incorrect ordering:

```text
R1K candidate branch
-> CF8 segment geometry
-> CF9 arena lookup
-> E_MCU_R7A_ARENA_DOMAIN_NOT_BOUND
-> later candidate submit would have called bind_device_queue
```

The caller therefore asks for an arena domain before the canonical R7 device/queue binding path has materialized it.

---

# 2. Canonical ordering law

CF9-CF1 establishes:

```text
canonical R7 bind_device_queue(queue)
-> zero-allocation bootstrap R7A domain
-> exact CF8 segment geometry
-> exact CF9 resource geometry
-> pre-reseal zero-state proof
-> atomic byte/page/lease reseal
-> resealed-domain publication
-> actual Adam candidate submission
-> later bind_device_queue idempotence proof
```

No alternate domain factory is introduced.

---

# 3. Canonical bootstrap binding

`ProductionMuonRuntime::bind_r7a_resource_geometry_bootstrap_cf9_cf1` invokes the existing:

```text
McuSessionRuntimeR7::bind_device_queue
```

before the first CF9 arena lookup.

The canonical binding remains the owner of:

```text
DeviceAuthorityId
QueueAuthorityId
R7A arena domain identity
bootstrap R7A budget seal
```

No scheduler-local DeviceAuthority, QueueAuthority or arena registry is created.

---

# 4. Zero-allocation bootstrap law

On the first CF9 resource-geometry generation the bound bootstrap domain must satisfy:

```text
acquire_count = 0
active_lease_count = 0
retained_bytes = 0
pending_retained_bytes = 0
page_count = 0
pending_page_count = 0
```

Failure:

```text
E_CF9_CF1_R7A_BOOTSTRAP_DOMAIN_NOT_EMPTY
```

The bootstrap domain exists only to expose the real physical device/queue reservation authority before CF9 geometry derivation.

---

# 5. Bootstrap witness

Required witness:

```text
[ASH-MCU-R7A-CF9-CF1][bootstrap-domain]
```

Fields include:

```text
device_authority_id
queue_authority_id
bootstrap_domain_digest
bootstrap_max_retained_bytes
bootstrap_max_page_count
bootstrap_max_in_flight_leases
acquire_count
active_lease_count
retained_bytes
pending_retained_bytes
page_count
pending_page_count
zero_allocation
bootstrap_allocation_authority=false
already_resealed
```

`already_resealed=false` is required for the first generation resource reseal.

---

# 6. CF8 geometry preservation

CF9-CF1 reuses the parent CF8 exact segment ledger without recomputation or reinterpretation.

Preserved authority includes:

```text
planned segment count
planned Adam element count
segment geometry digest
max pending segment count
derived active-lease floor
```

For the currently observed campaign lineage, parent physical evidence derived:

```text
planned_segment_count = 93
derived_lease_floor = 303
```

These remain physical evidence for that lineage, not generic constants.

---

# 7. CF9 geometry preservation

CF9-CF1 does not modify the CF9 resource geometry equations.

Preserved calculation includes:

```text
candidate generation-resident retained bytes/pages
source pool-key and size-class retained reuse ceiling
params/status/readback transient retained reuse ceiling
derived retained-byte floor
derived page-count floor
resource geometry digest
```

The parent arena reservation helper remains the reservation/quantization SSOT.

---

# 8. Pre-reseal witness

After CF9 resource geometry is derived and before the budget is changed, emit:

```text
[ASH-MCU-R7A-CF9-CF1][pre-reseal]
```

The witness binds:

```text
device authority
queue authority
bootstrap domain digest
current arena resource state
derived retained-byte ceiling
derived page ceiling
derived lease ceiling
zero_state
```

The first-generation reseal requires `zero_state=true`.

Failure:

```text
E_CF9_CF1_R7A_RESEAL_AFTER_ARENA_USE
```

---

# 9. Atomic resource reseal

The existing CF9 resource reseal remains authoritative and atomically replaces:

```text
max_retained_bytes
max_page_count
max_in_flight_leases
```

The values are respectively sourced from:

```text
CF9 retained-byte geometry
CF9 page geometry
CF8 lease geometry
```

No historical `512 MiB`, `256 pages` or magic lease constant is promoted as the final execution budget.

---

# 10. Device/queue parity across reseal

Reseal may change policy/domain identity because the budget changed.

Required:

```text
bootstrap device authority == resealed device authority
bootstrap queue authority  == resealed queue authority
```

Failures:

```text
E_CF9_CF1_R7A_RESEAL_DEVICE_AUTHORITY_DRIFT
E_CF9_CF1_R7A_RESEAL_QUEUE_AUTHORITY_DRIFT
```

---

# 11. Domain policy digest law

Let:

```text
budget_changed = any byte/page/lease seal value changed

domain_digest_changed = bootstrap domain digest != resealed domain digest
```

Required:

```text
domain_digest_changed == budget_changed
```

Failure:

```text
E_CF9_CF1_R7A_RESEAL_DOMAIN_POLICY_DRIFT
```

A changed domain digest caused by an actual policy change is expected and is not device/queue authority drift.

---

# 12. Post-reseal zero-state

Immediately after reseal and before the first arena acquisition:

```text
acquire_count = 0
active_lease_count = 0
retained_bytes = 0
pending_retained_bytes = 0
page_count = 0
pending_page_count = 0
```

Failure:

```text
E_CF9_CF1_R7A_RESEAL_MATERIALIZED_RESOURCE
```

This proves no physical arena resource was created between bootstrap bind and final CF9 resource seal.

---

# 13. Post-reseal witness

Required:

```text
[ASH-MCU-R7A-CF9-CF1][post-reseal-domain]
```

It records:

```text
device_authority_id
queue_authority_id
bootstrap_domain_digest
resealed_domain_digest
domain_digest_changed
budget_changed
sealed_max_retained_bytes
sealed_max_page_count
sealed_max_in_flight_leases
resource-state zero proof
single_current_domain_authority=true
```

The resealed domain is published as the one expected CF9-CF1 domain authority for later candidate submission.

---

# 14. Single current expected domain

`ProductionMuonCompatibilityRuntimeR8` stores one expected resealed authority:

```text
expected device authority id
expected queue authority id
expected domain digest
```

Publishing a conflicting authority fails closed.

Failure:

```text
E_CF9_CF1_R7A_DUPLICATE_DOMAIN_AUTHORITY
```

This state is evidence only. The canonical R7A runtime remains the physical domain owner.

---

# 15. Later candidate bind idempotence

The existing candidate execution call to:

```text
bind_device_queue(queue)
```

is preserved.

After the call, candidate execution resolves the canonical current R7A arena domain and compares it with the resealed CF9-CF1 expected authority.

Required witness:

```text
[ASH-MCU-R7A-CF9-CF1][candidate-bind-idempotence]
```

Expected:

```text
same_device=true
same_queue=true
same_domain=true
new_domain_created=false
```

Failures:

```text
E_CF9_CF1_R7A_CANDIDATE_DEVICE_AUTHORITY_DRIFT
E_CF9_CF1_R7A_CANDIDATE_QUEUE_AUTHORITY_DRIFT
E_CF9_CF1_R7A_CANDIDATE_DOMAIN_POLICY_DRIFT
```

---

# 16. No historical-path regression

The candidate idempotence check activates only after CF9-CF1 has published an expected resealed domain.

If no CF9-CF1 expected authority exists:

```text
(None, None, None)
```

the historical candidate bind path continues without requiring a pre-bound CF9 domain.

A partially materialized expected authority is illegal:

```text
E_CF9_CF1_R7A_PARTIAL_EXPECTED_DOMAIN_AUTHORITY
```

---

# 17. Two-step CANARY repeat-safe law

CANARY executes two optimizer generations.

After the first generation, physical arena pages may remain retained for warm reuse. Therefore later optimizer generations must not require the arena to return to zero retained bytes/pages.

When the already-published resealed domain is observed:

```text
already_resealed=true
```

CF9-CF1 skips reseal and instead requires exact equality between the current seal and the newly derived geometry:

```text
current max retained bytes == newly derived retained-byte floor
current max page count     == newly derived page floor
current max leases         == newly derived lease floor
```

Failures:

```text
E_CF9_CF1_R7A_RETAINED_BYTE_GEOMETRY_DRIFT_AFTER_RESEAL
E_CF9_CF1_R7A_PAGE_GEOMETRY_DRIFT_AFTER_RESEAL
E_CF9_CF1_R7A_LEASE_GEOMETRY_DRIFT_AFTER_RESEAL
```

---

# 18. Warm-generation resource reuse witness

For later generations emit:

```text
[ASH-MCU-R7A-CF9-CF1][generation-resource-reuse]
```

Fields include:

```text
device authority
queue authority
current resealed domain digest
retained/pending bytes
page/pending-page counts
active leases
current byte/page/lease seals
geometry_exact=true
reseal_skipped=true
```

Retained physical pages are legal. Geometry drift is not.

---

# 19. No acquire before first reseal

On first-generation CF9-CF1 setup, both pre-reseal and post-reseal state proofs require zero arena resource materialization.

Thus source/candidate/transient arena acquisition cannot legally occur before the final CF9 resource seal.

No direct-create fallback is added.

---

# 20. CF9 byte/page classification preservation

After ordering closure the existing CF9 fail-closed resource errors remain unchanged:

```text
E_MCU_R7A_ARENA_RETAINED_BYTE_BOUND
E_MCU_R7A_ARENA_PAGE_BOUND
E_MCU_R7A_ARENA_RETAINED_BYTE_AND_PAGE_BOUND
```

CF9-CF1 does not loosen those axes.

---

# 21. CF8 lease-axis preservation

The independent lease-axis guard remains:

```text
E_MCU_R7A_ARENA_ACTIVE_LEASE_BOUND
```

CF9-CF1 does not weaken or bypass it.

---

# 22. Physical expected sequence

First optimizer generation:

```text
[ASH-MCU-EVE-R1K][candidate-branch]
[ASH-MCU-R7A-CF9-CF1][bootstrap-domain] already_resealed=false
[ASH-MCU-R7A-CF9-CF1][pre-reseal]
[ASH-MCU-R7A-CF9-CF1][post-reseal-domain]
[ASH-MCU-R7A-CF8][adam-lease-geometry]
[ASH-MCU-R7A-CF9][adam-resource-geometry]
[ASH-MCU-R7A-CF9-CF1][candidate-bind-idempotence]
[ASH-MCU-R7A-CF8][lease-acquire]
[ASH-MCU-R7A-CF9][resource-admission]
```

Second optimizer generation:

```text
[ASH-MCU-R7A-CF9-CF1][bootstrap-domain] already_resealed=true
[ASH-MCU-R7A-CF9-CF1][generation-resource-reuse]
[ASH-MCU-R7A-CF9-CF1][candidate-bind-idempotence]
...
```

---

# 23. Previous failure retirement

The ordinary CF9 ActiveDevice CANARY path must no longer terminate with:

```text
E_MCU_R7A_ARENA_DOMAIN_NOT_BOUND
```

If it does, bootstrap binding ordering is not closed.

---

# 24. Static acceptance

Required source properties:

```text
canonical bind_device_queue before CF9 first arena lookup
bootstrap zero-state witness
CF8 geometry unchanged
CF9 geometry unchanged
pre-reseal zero-state guard
atomic parent CF9 resource reseal retained
device/queue parity guard across reseal
post-reseal domain witness
one expected resealed domain authority
candidate bind idempotence witness
historical non-CF9 path does not require pre-bound domain
second optimizer generation reuses same seal without zero-retained requirement
no resource budget relaxation
no early reclaim
no direct-create fallback
```

---

# 25. Compile / physical evidence boundary

This bake environment does not provide a Rust toolchain.

Therefore:

```text
SOURCE     STATIC-INSPECTED
COMPILE    NOT CLAIMED
PHYSICAL   NOT CLAIMED
```

Compile must be established externally with:

```text
cargo build -p base_train --bin base_train --release --locked -j 1
```

Native CF1 must be resealed after that build.

---

# 26. Bake delta

Parent archive:

```text
ASH_PASS3_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_R7A_ACTIVE_DEVICE_ADAM_RETAINED_BYTE_PAGE_GEOMETRY_BUDGET_CLOSURE_CODE_ONLY.zip
```

Modified files only:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

```text
ADD 0
MOD 2
DEL 0
```

Source SHA-256:

```text
c2fe1184fdceffaf3c816935f4509f59d2261cbaf0c2737bd1ce4cbc033255c9
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs

48c67960ca095444c30da201bcf0229eb730c2fef28f97fd9834895c69b01ad1
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

Full code-only archive:

```text
SHA-256:
1b7fd4d0bac42fb98227aaa7099410cb932fa5f873bbd82a0d996afbe7384569

file count: 8424
CRC: PASS
specs/: 0
artifacts/: 0
```

Overlay code-only archive:

```text
SHA-256:
766df97b91c1473af3415bce7cd1a785d7806ca83d287a771602303a21ebbd99

file count: 2
CRC: PASS
specs/: 0
artifacts/: 0
```

---

# 27. PASS boundary

Reserved physical token:

```text
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF9_CF1
```

It may be claimed only after a physical CANARY establishes:

```text
canonical device/queue bind occurs before CF9 arena lookup
first-generation bootstrap state is empty
CF9 resource geometry derives
atomic reseal succeeds
resealed domain keeps exact device/queue authority
candidate bind is idempotent
no arena acquire precedes first reseal
E_MCU_R7A_ARENA_DOMAIN_NOT_BOUND is retired
```

Second-step warm reuse must additionally show either successful reuse under the same exact seal or a new explicit physical boundary.

---

# 28. Final law

> CF9-CF1 repairs authority ordering, not resource capacity.

> The canonical R7 device/queue bind creates an empty bootstrap R7A domain before CF9 inspects physical reservation geometry.

> CF8 segment geometry and CF9 retained-byte/page geometry remain unchanged.

> The first optimizer generation atomically reseals byte, page and lease authority before any arena resource acquisition.

> Later candidate `bind_device_queue` calls must resolve idempotently to the same resealed domain.

> Later optimizer generations reuse the already-resealed warm arena when the exact resource geometry remains unchanged; retained pages are not mistaken for an illegal dirty bootstrap.

> No duplicate domain authority, no resource-budget relaxation, no early reclaim, no hidden fallback.
