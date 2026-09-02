# ASH-BASETRAIN-RAM36-RESIDENT-WEIGHT-FIXED-TWO-SLOT-GENERATIONAL-REUSE-ARC-EXACT-READER-RETIREMENT-AND-NO-REALLOCATION-COMMIT-CLOSURE-R1

## 0. Revision

`ASH-BASETRAIN-RAM36-RESIDENT-WEIGHT-FIXED-TWO-SLOT-GENERATIONAL-REUSE-ARC-EXACT-READER-RETIREMENT-AND-NO-REALLOCATION-COMMIT-CLOSURE-R1`

Parent:

`ASH-BASETRAIN-RAM36-HIMUON-ROUTE-SPARSE-TRANSACTIONAL-ADAM-AB-CANONICAL-COMPACT-OVERLAY-ORDER-INDEPENDENT-PACKED-WRITE-COVERAGE-AND-EXACT-SCATTER-CLOSURE-R1B`

## 1. Physical trigger

The parent physical N8 campaign established that sparse Adam itself is no longer the memory blocker:

- R1A packed/canonical bridge: ADMITTED
- R1B order-independent compact-overlay coverage: ADMITTED
- AdamW coverage: 47/47 complete
- AdamW written elements: 197,761,024
- sparse Adam transaction: COMMITTED
- exact sparse scatter: COMMITTED
- Muon committed M/V writes: 0
- full sparse candidate allocation count: 0
- N8 step 1/8 completed

Current model authority observed:

- canonical full weight bytes: 4,666,580,992
- sparse Adam combined overlay bytes: 1,582,088,192
- sparse candidate bytes avoided: 7,751,073,792

Generation 5 to 6 entered successor allocation from approximately 27.10 GB private bytes and completed.
Generation 6 to 7 entered successor allocation from approximately 30.15 GB private bytes and then terminated with `memory allocation of 6176 bytes failed` after another full successor backing had been allocated.

R1 does not claim whether the inter-generation growth was caused by stale `Arc` readers, allocator retained commit, or both. Instead it removes repeated full-weight allocation/free from normal generation progression and emits exact ownership evidence.

## 2. Closure objective

The production resident weight lifecycle becomes a fixed two-physical-slot system:

- Slot A: one full canonical weight backing
- Slot B: one full canonical weight backing

Generation identity moves between slots. Backing allocations do not.

After the second physical slot has been created:

- fresh full-weight allocation per optimizer step = 0
- normal full-weight deallocation/reallocation dependency per optimizer step = 0
- physical full-weight slot count peak = 2
- third full slot creation is forbidden

The unchanged process hard limit remains exactly 38,654,705,664 bytes (36 GiB).

## 3. Explicit admission

New CLI admission:

`--admit-ram36-resident-weight-fixed-two-slot-generational-reuse`

Default: false.

Required parents:

- N8 long-horizon execution
- RAM weight-pack persistent residency
- RAM36 process budget authority
- exact RAM inventory
- deferred durable writeback

Legacy resident-weight behavior remains available when the new flag is absent.

## 4. Physical slot identity

New slot identity:

`ResidentWeightSlotIdR1::{A,B}`

Initial source load is Slot A.
The first fresh successor is Slot B.
Subsequent generations alternate the recovered A/B backing.

The slot identity is physical-lifetime metadata and is separate from generation identity.

## 5. ResidentWeightPack ownership extension

`ResidentWeightPack` now carries `slot_id_r1` and exposes exact physical ownership observations:

- `slot_id_r1()`
- `backing_strong_count_r1()`
- `backing_capacity_bytes_r1()`
- `into_reusable_backing_r1()`

`into_reusable_backing_r1()` requires exact unique backing ownership.

Before reuse:

`Arc::strong_count(backing) == 1`

Then:

`Arc::try_unwrap(backing)`

must succeed.

Failure tokens:

- `FAIL_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_TWO_SLOT_STALE_READER_REMAINS_R1`
- `FAIL_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_TWO_SLOT_EXACT_OWNERSHIP_RECOVERY_FAILED_R1`

No full-buffer clone/copy fallback is allowed.

## 6. Reusable builder

`ResidentWeightPackBuilder` gains an explicit physical slot identity and allocation provenance:

- slot ID
- fresh allocation bytes
- reused capacity bytes

Fresh construction is still permitted for the first secondary slot.

Reusable construction uses:

`ResidentWeightPackBuilder::from_reusable_backing_r1(...)`

It requires retained capacity at least equal to canonical weight bytes, calls `Vec::clear()` to reset logical length, verifies capacity was retained, and then overwrites the existing backing.

No whole-slot zero-fill is required. Existing exact initialized-range and final full-coverage checks remain authoritative.

After reuse:

- `fresh_allocation_bytes_r1() == 0`
- existing capacity is retained
- full successor coverage is still required
- final SHA-256 must still equal the candidate weight manifest digest

## 7. Runtime SSOT

New module:

`crates/base_train/src/resident_weight_fixed_two_slot_r1.rs`

Runtime authority:

`ResidentWeightTwoSlotRuntimeR1`

It owns:

- canonical weight byte size
- current physical slot identity
- optional inactive reusable backing
- physical slot count and peak
- total fresh full allocation count
- post-seal fresh full allocation count
- reuse count
- reused capacity bytes
- third-slot attempt count
- last retired backing strong count

It does not own optimizer math or sparse Adam state.

## 8. Slot lifecycle

Bootstrap:

`A = CURRENT`

First successor:

`A = CURRENT`
`B = SUCCESSOR_BUILDING`

After promotion:

`B = CURRENT`
`A = retired -> exact reader retirement -> INACTIVE_REUSABLE`

Next successor:

`A = SUCCESSOR_BUILDING` using the same recovered backing

After promotion:

`A = CURRENT`
`B = INACTIVE_REUSABLE`

The cycle repeats without a third backing.

## 9. Reader-retirement boundary

A former current slot is not reusable merely because logical promotion occurred.

Before promotion/recovery the runtime observes the current pack strong count and requires it to be exactly one.

The actual old `ResidentWeightPack` is then consumed and `Arc::try_unwrap` recovers the backing `Vec<u8>`.

This makes stale reader lifetime a structural failure rather than a hidden allocator symptom.

No retry/sleep loop is used to wait for readers to disappear.

## 10. Third-slot prohibition

Once two slots are physically sealed, absence of a reusable slot is an error, not permission to allocate another 4.346 GiB buffer.

Failure:

`FAIL_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_THIRD_PHYSICAL_SLOT_FORBIDDEN_R1`

Related failure:

`FAIL_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_REUSABLE_SLOT_NOT_AVAILABLE_R1`

## 11. RAM36 physical accounting

R1 separates physical slot ownership from logical generation role.

First secondary slot:

- full logical successor bytes are projected
- a normal `ResidentWeightPack` RAM36 reservation is created
- physical allocation transition is observed

Post-seal reused successor:

- logical successor size remains full canonical weight size
- fresh physical allocation contribution = 0
- existing old-slot RAM36 reservation identity is recycled into successor-building state
- the reused physical capacity remains represented exactly once

New RAM36 transition:

`transition_promoted_resident_weight_to_reuse_building_r1(...)`

Expected log:

`[ASH-RAM36-RESIDENT-WEIGHT-TWO-SLOT-REUSE-RESERVATION-R1]`

Required post-seal fields include:

- `fresh_physical_allocation_bytes=0`
- `reused_physical_capacity_bytes=<canonical weight bytes>`
- `projection_contribution_bytes=0`
- `two_slot_sealed=true`

No blanket RAM36 discount, hard-limit mutation, private-memory subtraction, or saturating repair is introduced.

## 12. Sparse-R1 headroom compatibility

The existing sparse Adam headroom receipt continues to carry the full logical successor requested byte count.

Its projected RAM calculation now receives the physical allocation contribution:

- first successor: canonical full weight bytes
- post-seal reused successor: 0

The runtime log adds `projection_contribution_bytes` so logical successor size and new physical allocation are not conflated.

## 13. Exact RAM inventory

The existing current-generation and successor weight inventory entries remain the two physical allocation identities.

When the first secondary slot is materialized, R1 calls:

`seal_resident_weight_fixed_two_slot_pool_r1()`

Both entries become run-resident fixed physical slots and remain active while generation roles alternate.

At final shutdown:

`release_resident_weight_fixed_two_slot_pool_r1()`

releases both inventory identities.

No third inventory entry is created for later generations.

## 14. Promotion semantics

Existing successor identity validation remains unchanged:

- target generation exact
- target optimizer step exact
- path exact
- byte length exact
- digest exact

The successor reservation is still marked promoted.

In two-slot mode the old resident and old reservation are not immediately dropped/released. They are transferred into the reusable physical slot authority after exact reader retirement and ownership recovery.

The new current slot becomes the runtime current slot identity.

Expected log:

`[ASH-RAM36-RESIDENT-WEIGHT-TWO-SLOT-PROMOTION-R1]`

Required:

- old current slot != new current slot
- reader retirement exact
- physical slot count = 2
- candidate complete and digest exact

## 15. Process-memory observation

After old-current retirement into reusable backing, RAM36 observes current process memory with no extra full-weight projection.

Expected log:

`[ASH-RAM36-RESIDENT-WEIGHT-TWO-SLOT-MEMORY-R1]`

This is diagnostic evidence for residual process-private growth after repeated full-weight allocation has been eliminated.

R1 does not claim that process-private bytes must be numerically constant from step to step.

## 16. Shutdown

At final shutdown:

1. final current resident backing is dropped;
2. reusable inactive slot backing is dropped;
3. reusable slot RAM36 reservation is released;
4. current slot RAM36 reservation is released;
5. both fixed-slot exact-inventory identities are deactivated.

This prevents the two physical reservations from being reported as leaks by the existing RAM36 receipt.

## 17. Physical receipt

New file:

`resident_weight_fixed_two_slot_authority_r1.json`

Receipt type:

`ResidentWeightFixedTwoSlotReceiptR1`

Fields include:

- revision
- canonical weight bytes
- current slot ID
- inactive slot ID
- physical slot count
- physical slot count peak
- fresh full allocation count
- post-seal fresh full allocation count
- reuse count
- reused capacity bytes
- third-slot attempt count
- last retired strong count
- two-slot sealed
- optimizer steps completed
- physical pass claimed
- receipt digest

## 18. Physical PASS rule

Physical PASS is permitted only when the actual requested N8 campaign completes eight optimizer steps and the runtime receipt proves:

- physical slot count = 2
- physical slot count peak = 2
- lifetime fresh full allocation count = 2 (initial A plus first B)
- post-seal fresh full allocation count = 0
- third-slot attempt count = 0
- reuse count = optimizer steps minus one
- an inactive reusable slot exists at final stable boundary

Reserved PASS token:

`PASS_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_FIXED_TWO_SLOT_GENERATIONAL_REUSE_ARC_EXACT_READER_RETIREMENT_AND_NO_REALLOCATION_COMMIT_PHYSICAL_R1`

Static code may contain the token but does not claim the physical result.

Physical HOLD token:

`HOLD_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_FIXED_TWO_SLOT_GENERATIONAL_REUSE_PHYSICAL_PENDING_R1`

## 19. Preserved sparse Adam semantics

R1 does not modify the mathematical or coordinate authority established by the parent lineage.

Preserved:

- R1 route-sparse candidate allocation
- R1A packed-to-canonical parameter bridge
- R1A exact Muon inherited M/V comparison
- R1B order-independent AdamW overlay coverage ledger
- R1B exact scatter
- `fullCandidateAllocationCount=0`
- no HDD spill

## 20. Backend boundary

R1 does not promote the HiMuon matrix backend.

The known performance boundary remains separate:

- `backend_id=F32_WORKGROUP_LEGACY`
- `tensor_core_execution_claimed=false`
- `qualified=false`

The two-slot closure is a host resident-lifetime closure, not a GPU kernel optimization.

## 21. Baked source truth

Actual diff against the exact R1B full-source parent contains 11 files.

New:

- `crates/base_train/src/resident_weight_fixed_two_slot_r1.rs`
- `tools/validate_ash_basetrain_ram36_resident_weight_fixed_two_slot_generational_reuse_arc_exact_reader_retirement_and_no_reallocation_commit_closure_r1_static.py`

Modified:

- `crates/base_train/src/bin/base_train.rs`
- `crates/base_train/src/config.rs`
- `crates/base_train/src/lib.rs`
- `crates/base_train/src/pipeline.rs`
- `crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs`
- `crates/base_train/src/ram36_process_budget.rs`
- `crates/base_train/src/ram_budget_exact_inventory.rs`
- `crates/base_train/src/ram_weight_pack_persistent_residency.rs`
- `tools/validate_ash_basetrain_ram36_successor_weight_reservation_physical_allocation_ownership_transition_closure_r1_static.py`

The last validator modification only follows the existing legacy reservation -> builder -> physical-allocation transition after that sequence was extracted into `acquire_resident_weight_successor_builder_r1`; it does not weaken the legacy transition checks.

## 22. Static validation

New R1 validator checks 40 structural invariants, including:

- explicit admission and default false
- fixed A/B slot type
- exact Arc strong-count gate
- exact `Arc::try_unwrap`
- no third slot
- reusable capacity retained
- post-seal fresh allocation zero
- post-seal RAM36 projection zero for existing weight capacity
- reused reservation transition
- fixed two-slot exact inventory
- promotion reader-retirement gate
- final release of both reservations
- unchanged RAM36 36 GiB cap
- preserved R1/R1A/R1B sparse semantics
- no process-cap inflation

Bake regression result:

- static validators executed: 17
- PASS: 17
- FAIL: 0

The regression set includes R1, R1B, R1A, sparse R1, RAM36 HiMuon route-exact, transactional RAM Adam A/B, trainable-generation durability, Eve Adam R1/R2, Weight Successor Journal, MCU AdamW scheduler, bounded full-trainable device projection, SubmissionEpoch, MCU active transactional commit/restart, RAM36 remaining-underflow attribution, successor weight reservation/physical-allocation ownership transition, and immutable N2 RAM36 authority.

The bake environment has no Cargo or Rustc. Therefore no Rust compile PASS and no physical PASS are claimed by this bake.

## 23. Static PASS token

`PASS_ASH_BASETRAIN_RAM36_RESIDENT_WEIGHT_FIXED_TWO_SLOT_GENERATIONAL_REUSE_ARC_EXACT_READER_RETIREMENT_AND_NO_REALLOCATION_COMMIT_CLOSURE_R1_STATIC`

## 24. Physical qualification target

The next local N8 must use:

- fresh isolated Cargo target directory
- incremental compilation disabled
- the new two-slot admission flag
- matching exact Native CF1 produced after all builds
- fresh cross-release consumer authority
- immutable N2 parent
- RAM36 process authority
- sparse Adam R1/R1A/R1B
- HiMuon production routing
- Weight Journal OFF for the baseline physical run

The decisive boundary is generation 6 to 7.

Expected after the first promotion:

- old Slot A strong count = 1
- exact ownership recovery succeeds
- Slot A becomes inactive reusable

Expected for the next successor:

- target slot = A
- fresh full allocation bytes = 0
- reused physical capacity = canonical weight bytes
- RAM36 successor projection contribution = 0
- no `memory allocation of 6176 bytes failed` caused by a fresh full-weight backing allocation

## 25. Failure interpretation

If stale reader failure occurs, reader ownership/lifetime becomes the next SSOT.

If exact A/B reuse succeeds but process-private memory still grows materially until failure, the next SSOT is non-weight resident lifetime or allocator/runtime retention.

Do not increase the RAM36 cap and do not introduce a third slot to mask either case.

## 26. Final invariant

Two physical weight backings exist.

One is current.

The other is reusable or building the successor.

Generation changes do not create a third backing.

A retired backing is reusable only after exact reader retirement and unique Arc ownership recovery.

The first secondary allocation is physical and fully accounted.

Every later successor reuses an already-accounted backing and contributes zero new full-weight bytes to RAM36 projection.

Full successor coverage and digest remain exact.

Sparse Adam remains sparse and bit-exact.

The RAM36 hard limit remains 36 GiB.

No allocator-specific decommit workaround, no process-cap inflation, no HDD spill, no full-buffer clone fallback, and no physical PASS without an actual eight-step N8 run.