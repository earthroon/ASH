# TENSORCUBE-TABLE-R4A-CF2

## HIMUON PRODUCER MULTI-BATCH ASYNC AUTHORITY
## + R7A1 PACKED-GRADIENT EXACT BINDING
## + DIRECT SHARED-ARENA OUTPUT PROMOTION GATE

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4A-CF2

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4A-CF2-
HIMUON-PRODUCER-MULTI-BATCH-ASYNC-
DIRECT-SHARED-ARENA-OUTPUT

Direct parent:
TENSORCUBE-TABLE-R4A-CF1
```

Class:

```text
GPU producer scheduling / attribution / promotion-gate closure
No HiMuon numerical change
No reduction-order change
No optimizer semantic change
```

## 1. Target architecture

The final CF2 target remains:

```text
R7A1 packed gradient
    -> bounded multi-batch HiMuon producer window
    -> several physical batches in flight
    -> candidate W/M/update written directly into CF1 shared arenas
    -> no candidate payload D2H
    -> no CF1 candidate repack D2D
    -> CF1 cross-chunk TensorCube consumer
```

Physical batch is a dispatch partition, not a canonical semantic identity and not a host synchronization boundary.

Canonical execution identity remains:

```text
(parameter_index, tensorcube_ordinal)
```

## 2. Exact source closure in this bake

This first CF2 bake materializes the **producer cohort authority and physical attribution layer** on the real production ActiveAsync path.

The source now observes and seals:

```text
logical producer batch count
submitted batch count
completed batch count
submission count
in-flight batch peak
multi-batch async observation
out-of-order completion count
R7A1 packed-gradient exact physical binding
candidate W D2H bytes
candidate M D2H bytes
update D2H bytes
compact status D2H bytes
host candidate materialization count
ActiveDevice exact-wait count
current CF1 repack D2D bytes
```

The existing production topology already supports multiple pending HiMuon waves through P5 ActiveAsync. CF2 binds that real topology to an explicit TensorCube Table producer authority rather than inventing a second scheduler.

## 3. Honest promotion boundary

Source constants:

```text
TENSORCUBE_TABLE_R4A_CF2_MULTI_BATCH_ASYNC_AUTHORITY_MATERIALIZED = true
TENSORCUBE_TABLE_R4A_CF2_DIRECT_SHARED_ARENA_OUTPUT_MATERIALIZED = false
TENSORCUBE_TABLE_R4A_CF2_PER_BATCH_BLOCKING_POLL_REQUIRED = false
TENSORCUBE_TABLE_R4A_CF2_CANDIDATE_BULK_READBACK_REQUIRED = false
```

Therefore this bake does **not** falsely claim that ActiveDevice producer outputs already bind directly into CF1 shared W/M/update arenas.

`ACTIVE_VERIFIED` remains fail-closed behind:

```text
HOLD_TENSORCUBE_TABLE_R4A_CF2_DIRECT_SHARED_ARENA_OUTPUT_NOT_YET_MATERIALIZED
```

The intended first runtime campaign is `OBSERVE_ONLY`.

## 4. R7A1 packed-gradient authority

CF2 requires an exact `PackedGradientReadBindingR7A1` whenever CF2 is enabled.

Required physical identity includes the existing R7A1 authority:

```text
PhysicalAllocationId
QueueAuthorityId
arena domain
arena page ordinal
arena incarnation
logical byte range
```

CF2 does not create a new gradient lifetime system.

## 5. Existing ActiveDevice truth preserved

The current ActiveDevice pending producer already proves:

```text
candidate_weight_full_d2h_bytes = 0
candidate_momentum_full_d2h_bytes = 0
update_full_d2h_bytes = 0
host_full_candidate_materialization_count = 0
active_device_pending_exact_wait_count = 0
```

Only compact status evidence is mapped/read on the ActiveDevice path.

CF2 observes these physical contracts rather than reimplementing candidate mathematics.

## 6. Multi-batch async observation

For every submitted R6/P4 wave, CF2 records the canonical wave ordinal as producer-batch ordinal and the current production pending count after enqueue.

`in_flight_batch_peak > 1` establishes observed multi-batch overlap in the current production scheduler.

No physical speedup is inferred merely from the static existence of P5.

## 7. Out-of-order completion

CF2 records completion against the set of submitted but incomplete producer batches.

A completion whose ordinal is not the lowest outstanding ordinal increments:

```text
out_of_order_completion_count
```

Out-of-order completion is legal and must not alter TensorCube identity or parameter completion semantics.

## 8. Current CF1 repack attribution

While CF1 remains the consumer parent, every completed legacy ActiveDevice chunk currently contributes candidate W/M/update bytes that CF1 repacks into its shared source arenas.

CF2 records this as:

```text
current_cf1_repack_d2d_bytes
= elem_count * 4 * 3
```

for each CF1-routed producer chunk.

This is an attribution counter, not a new copy operation.

The direct-output successor must drive this counter to zero for CF2-produced chunks.

## 9. P5 semantic consumer adoption

New P5 consumer kind:

```text
TensorCubeTableHiMuonProducerR4ACf2
```

This binds the CF2 producer authority to the exact existing P5 wave lifetime rather than introducing an independent completion ledger.

## 10. Parent requirements

CF2 enabled requires:

```text
R4A-CF1 enabled
R7A1 packed-gradient exact binding present
logical producer batch count > 1
```

CF2 `ACTIVE_VERIFIED` additionally requires CF1 `ACTIVE_VERIFIED`.

## 11. ObserveOnly mode

```text
ASH_TENSORCUBE_TABLE_R4A_CF2_MODE=OBSERVE_ONLY
```

ObserveOnly does not change HiMuon candidate mutation or publication.

It records real production producer topology and requires:

```text
all logical batches submitted
all submitted batches completed
candidate W/M/update D2H = 0
host candidate materialization = 0
ActiveDevice exact waits = 0
R7A1 packed-gradient binding present
```

## 12. ActiveVerified mode

```text
ASH_TENSORCUBE_TABLE_R4A_CF2_MODE=ACTIVE_VERIFIED
```

Current first source bake intentionally terminates with the direct-arena HOLD because producer output rebinding has not yet been materialized.

A successor revision must close:

```text
producer candidate W -> CF1 shared weight arena
producer candidate M -> CF1 shared momentum arena
producer update      -> CF1 shared update arena

without intermediate candidate ArenaLease ownership per chunk
without CF1 repack D2D
without weakening B06/P4/P5 lifetime
```

## 13. Runtime receipt

CF2 emits:

```text
[ASH-TENSORCUBE-TABLE-R4A-CF2][producer-window]
```

Fields include:

```text
mode
logical_batches
submitted
completed
submissions
batches_per_submission
in_flight_peak
multi_batch_async
out_of_order
packed_gradient_r7a1_exact
packed_gradient_alloc
candidate_d2h_w
candidate_d2h_m
update_d2h
compact_status_d2h
host_candidate_materialization
exact_wait
bulk_readback_count
per_batch_blocking_poll
cf1_repack_d2d
direct_shared_arena_output
cf1_parent_active
admitted
receipt digest
```

## 14. Numerical preservation

CF2 changes none of:

```text
Local Muon formula
Newton-Schulz steps
momentum recurrence
Nesterov semantics
subgroup reduction order
execution expert routing
R6 job identity
B06 publication authority
BP-DK durability authority
generation commit authority
```

## 15. Changed files

```text
MOD crates/base_train/src/lib.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/unified_atlas_mcu_submission_epoch_dependency_active_async_r1.rs
ADD crates/base_train/src/tensorcube_table_r4a_cf2_himuon_producer.rs
ADD tools/validate_ash_tensorcube_table_r4a_cf2_himuon_producer_static.py
```

Delta:

```text
MOD 3
ADD 2
DEL 0
```

## 16. Static qualification

Current CF2 result:

```text
PASS_TENSORCUBE_TABLE_R4A_CF2_HIMUON_PRODUCER_MULTI_BATCH_ASYNC_DIRECT_SHARED_ARENA_OUTPUT_STATIC checks=40
```

Parent TensorCube chain retained:

```text
R4A-CF1  90/90 PASS
R4A      66/66 PASS
R3-CF1   51/51 PASS
R3       PASS
R2A      PASS
R2       PASS
R1       PASS
MCU R7   55/55 PASS
```

Known R7A1 validator baseline:

```text
77 / 82 PASS
```

The same five failures reproduce on the unmodified R4A-CF1 parent and are not attributed to CF2:

```text
producer A01 tracked submit
local muon reader cutover
active pending reader cutover
P5 pending reader cutover
fused pair reader cutover
```

## 17. Artifact seal

```text
Overlay ZIP
SHA-256 201442ada0cd70958b874c601f268b72f1c863bb4c77d4d94c4b70828aa462d2
files 5
CRC PASS

Full code-only ZIP
SHA-256 94014938a102e0512bce11d29de7b3ed67f6e9b7fe321c1308775fd557a0ef90
files 8,495
CRC PASS
```

## 18. Evidence boundary

```text
SOURCE       PASS
STATIC       PASS
ARCHIVE      PASS
COMPILE      NOT RUN
RUNTIME      NOT RUN
PHYSICAL     NOT RUN
PERFORMANCE  UNMEASURED
PROMOTED     NO
```

No compile/runtime/physical/performance claim is made by this bake.

## 19. Compile acceptance

```powershell
cargo test -p base_train --lib tensorcube_table_r4a_cf2_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_cf1_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_ --release --locked
cargo build -p base_train --bin base_train --release --locked
```

## 20. ObserveOnly physical acceptance

Required first campaign:

```text
ASH_TENSORCUBE_TABLE_R4A_CF2_MODE=OBSERVE_ONLY
```

Require at least:

```text
logical_batch_count > 1
submitted_batch_count == logical_batch_count
completed_batch_count == logical_batch_count
in_flight_batch_peak > 1
packed_gradient_r7a1_exact = true
candidate_weight_d2h_bytes = 0
candidate_momentum_d2h_bytes = 0
update_d2h_bytes = 0
host_candidate_materialization_count = 0
active_device_exact_wait_count = 0
current_cf1_repack_d2d_bytes > 0
```

The final line is expected in this first bake and quantifies the next optimization target.

## 21. Direct successor

The exact next source patch is:

```text
TENSORCUBE-TABLE-R4A-CF2-CF1

DIRECT PRODUCER OUTPUT → CF1 SHARED ARENA
+ SHARED W/M/UPDATE COHORT OWNER
+ OUTPUT SUBRANGE BINDING
+ CF1 REPACK D2D RETIREMENT
+ FINAL-READER ARENA RECLAIM
+ ACTIVE_VERIFIED PROMOTION
```

That revision must preserve the R7A1 exact multi-consumer lifetime law and must not reclaim a shared candidate arena after producer completion while CF1 still owns a reader epoch.

## 22. Final law

> R4A-CF2 first materializes the real producer-cohort authority before changing candidate buffer ownership.
>
> The current ActiveAsync production path already permits more than one HiMuon physical batch to remain in flight and already keeps candidate W/M/update payload off the CPU. CF2 measures and seals that fact against the exact R7A1 packed-gradient physical identity.
>
> The remaining measured debt is the producer-to-CF1 candidate repack D2D. ActiveVerified therefore remains fail-closed until producer outputs are written directly into CF1 shared arenas under exact producer/consumer lifetime tracking.
