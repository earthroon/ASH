# EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1-CF1-CF1

## RAM36 INITIAL RESIDENT WEIGHT
## CURRENT-SOURCE PROMOTION CLOSURE

```text
+ INITIAL RESERVATION MATERIALIZATION RECEIPT RETENTION
+ MATERIALIZED -> PROMOTED CURRENT-SOURCE ADOPTION
+ NO SUCCESSOR ATTRIBUTION SPOOF
+ CURRENT SOURCE GENERATION EXACT BINDING
+ CURRENT SOURCE OPTIMIZER STEP EXACT BINDING
+ CURRENT SOURCE WEIGHT IDENTITY EXACT BINDING
+ RAM36 LEDGER / BODY SNAPSHOT EXACT PARITY
+ FRESH LOAD / DURABLE REPLAY / R4 REENTRY SEPARATION
+ R3H LAST-USE PROMOTED PRECONDITION CLOSURE
+ R3C1 CURRENT-WEIGHT PROMOTED PRECONDITION PRESERVATION
+ NO WEIGHT BYTE CHANGE
+ NO EXTRA WEIGHT ALLOCATION
+ NO EXTRA FULL-WEIGHT SHA PASS
+ NO GENERATION ADVANCE DURING ADOPTION
+ NO SUCCESSOR ATTRIBUTION SPOOF
+ INITIALIZATION FAILURE CLEANUP CLOSURE
+ BPDK SNAPSHOT CLOSURE PRESERVATION
+ R8A CLOSURE PRESERVATION
+ PACKED M/V CLOSURE PRESERVATION
+ CF11-R1 MEMORY PRESERVATION
```

## 0. Revision

```text
Patch ID:
EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1-CF1-CF1

Class:
RAM36 RESIDENT-WEIGHT LIFECYCLE CLOSURE
CURRENT-SOURCE AUTHORITY ADOPTION
SOURCE / SUCCESSOR PROMOTION DOMAIN SEPARATION
```

Direct parent:

```text
EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1-CF1
```

Parent Full code-only SHA-256:

```text
c5aef3c9d8d01fd40cf9cbc07351291255b0b51f62a47860608e4a1f91365b56
```

## 1. Parent Physical Blocker

The parent canary physically passed CF11-R1 bounded COW workspace, R3B packed M/V digest/address closure, R8A pre-durability identity seal + stream verify, BP-DK transactional candidate snapshot, and BP-DK source-optimizer / target-BP generation binding, then failed at:

```text
E_R3H_SOURCE_WEIGHT_RESERVATION_NOT_PROMOTED
```

The compact candidate-terminal receipt had reached:

```text
R3B-MV:PASS
R8A-ID:PASS
R8A-STREAM:PASS
BPDK-SNAP:PASS
SRC-RETIRE:NR
SUCCESSOR:NR
COMMIT:NR
```

## 2. Root Cause

Initial resident-weight hydration previously performed:

```text
RAM36 reserve
    -> local reservation snapshot = Admitted

ResidentWeightPack load/replay

verify_materialized(...)
    -> RAM36 ledger = Materialized
    -> returned Materialized snapshot discarded

body.resident_weight_reservation
    -> stale Admitted snapshot
```

Even retaining the Materialized return alone is insufficient because the loaded resident pack is already the authoritative current source. R3H correctly requires the current source reservation to be Promoted.

This revision closes:

```text
Admitted -> Materialized -> Promoted current-source adoption
```

without treating current-source adoption as successor generation promotion.

## 3. New RAM36 Current-Source Authority

New APIs:

```text
promote_current_resident_weight_source_r3h(...)
verify_promoted_current_resident_weight_source_r3h(...)
```

New receipt:

```text
Ram36CurrentSourceAdoptionReceiptR3H
```

The promotion API requires the RAM36 ledger entry and caller snapshot to match exactly in reservation ID, owner, state, requested bytes, physical allocated bytes, and materialized bytes.

It additionally requires:

```text
owner == ResidentWeightPack
state == Materialized
requested_bytes == physical_allocated_bytes
requested_bytes == materialized_bytes
requested_bytes == actual ResidentWeightPack byte length
```

Only then may the same ledger entry transition:

```text
Materialized -> Promoted
```

## 4. No Successor Attribution Spoof

Current-source adoption does not call:

```text
set_successor_weight_attribution(...)
mark_resident_weight_promoted(...)
prepare_resident_weight_promotion_r3c1(...)
```

and does not set:

```text
Ram36ProjectionPhase::GenerationPromotion
```

The successor attribution tuple is preserved unchanged.

Receipt fields freeze:

```text
additional_weight_allocation_bytes = 0
generation_advanced = false
successor_attribution_changed = false
```

## 5. Source Identity Binding

Before adoption, the scheduler requires:

```text
ResidentWeightPack generation == selected source generation
ResidentWeightPack optimizer step == selected source optimizer step
ResidentWeightPack byte length == packed manifest weight bytes
ResidentWeightPack SHA-256 == packed manifest weight SHA-256
```

No second full-weight SHA pass is added. Identity is reused from the existing verified load or durable replay path.

## 6. Materialization Receipt Retention

The initial path now retains:

```rust
let materialized_reservation =
    budget.verify_materialized(&reservation, resident.byte_len())?;
```

and passes exactly that snapshot to:

```text
promote_current_resident_weight_source_r3h(...)
```

The old reserve() snapshot is never installed beside the resident pack after materialization.

## 7. Fresh Load Path

```text
reserve
-> ResidentWeightPack::load_once
-> verified generation / optimizer step / bytes / SHA
-> verify_materialized
-> current-source adoption
-> install ResidentWeightPack + Promoted reservation together
```

Compact receipt:

```text
[ASH-RAM36-R3H][current-source] origin=LOAD ... state_before=Materialized state_after=Promoted ...
```

## 8. Durable Replay Path

```text
validated durable head
-> replay_weight_head_to_resident_r3e
-> exact target identity verification
-> verify_materialized
-> current-source adoption
```

The same adoption authority is used for non-zero generations. No generation-zero special case exists.

Receipt origin:

```text
origin=REPLAY
```

## 9. R4 Reentry

R4 keep-resident reentry does not load, reserve, materialize, or promote the source again.

It verifies:

```text
resident generation / optimizer step == restored source
resident bytes / SHA == source packed manifest
reservation state == Promoted
RAM36 ledger snapshot == body reservation snapshot
```

using:

```text
verify_promoted_current_resident_weight_source_r3h(...)
```

Verbose mode may emit origin=R4_REUSE. No re-adoption occurs.

## 10. Initialization Failure Cleanup

Initial hydration is staged before body publication.

On failure after reservation creation:

```text
budget.release(reservation_id)
```

is executed against the live RAM36 ledger state.

This remains valid when verify_materialized() already transitioned the ledger before a later verification failure.

If cleanup also fails, the primary initialization error is preserved with cleanup-failure context.

No partially adopted pack/reservation bundle is installed into the body.

## 11. R3H Preservation

The existing strict gate remains unchanged:

```text
source_reservation.state == HostRamReservationState::Promoted
```

This revision does not weaken R3H to accept Materialized.

## 12. R3C1 Preservation

The existing successor contract remains:

```text
successor reservation == Materialized before R3C1 apply
```

and existing R3C1 apply remains the authority that transitions a real successor:

```text
Materialized -> Promoted
```

Current-source adoption does not replace successor generation-promotion semantics.

Inherited R3C1 static baseline:

```text
25 / 30 PASS
```

with the same five known parent drift checks.

## 13. Unit Guards Added

New RAM36 tests cover:

```text
materialized ledger/snapshot exact pair accepted
stale Admitted local snapshot rejected
weight-byte drift rejected
R4 Promoted ledger/snapshot pair accepted
```

## 14. Modified Files

```text
MOD crates/base_train/src/ram36_process_budget.rs
MOD crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
ADD tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_cf1_cf1_ram36_current_source_promotion_static.py
```

No BP-DK, R8A, packed M/V, WGSL or optimizer kernel source is modified.

## 15. Source SHA-256

```text
971e41f1283f07aac2d531e25a6efc729ac0aef3353e25cff3b1a9b4704e3fdb  crates/base_train/src/ram36_process_budget.rs
5dda1e380c0ae812b0e0f7f92626798ef3c7d39efafa7c391894dbf6544ed827  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
0f761cdf50dd9ab04c8135af79ea120d9e99886d4731670e35fb7f502ff04ff9  tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_cf1_cf1_ram36_current_source_promotion_static.py
```

## 16. Static Qualification

```text
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_STATIC checks=32
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
```

Inherited R3C1 validator:

```text
25 / 30 PASS
```

Rust toolchain is not installed in the bake environment.

```text
SOURCE        APPLIED
STATIC        PASS
ARCHIVE CRC   PASS
RUST COMPILE  NOT RUN
RUST TEST     NOT RUN
RUNTIME       NOT RUN
PHYSICAL      NOT RUN
PERFORMANCE   UNMEASURED
```

## 17. Code-Only Artifacts

Overlay:

```text
ASH_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_OVERLAY_CODE_ONLY.zip
SHA-256 ba4d295abc37bad9f82a46274e68d897c1ffb65cea729efa4a7f180e4a83a845
FILES 3
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_CODE_ONLY.zip
SHA-256 918fb8724ce05e7b76c7415055e9e8a2ac0f639dddc011a4bc7f3ad231223b00
FILES 8440
CRC PASS
```

Both archives exclude:

```text
specs/      0
artifacts/  0
manifests/  0
Markdown    0
__pycache__ 0
*.pyc       0
```

## 18. Physical Acceptance

On the same fixture that previously failed at:

```text
E_R3H_SOURCE_WEIGHT_RESERVATION_NOT_PROMOTED
```

required first evidence:

```text
[ASH-RAM36-R3H][current-source]
state_before=Materialized
state_after=Promoted
ledger_exact=true
additional_weight_allocation_bytes=0
generation_advanced=false
successor_attribution_changed=false
admitted=true
```

Required disappearance:

```text
E_R3H_SOURCE_WEIGHT_RESERVATION_NOT_PROMOTED
```

Execution must then advance into source-last-use / source-retirement.

Parent physical closures must remain intact:

```text
BPDK-SNAP:PASS
R8A-ID:PASS
R8A-STREAM:PASS
R3B-MV:PASS
CF11-R1 bounded workspace exact
```

## 19. Completion Law

This revision closes only when:

1. verify_materialized() return is retained;
2. RAM36 ledger and body reservation snapshots are exact;
3. loaded/replayed source is explicitly adopted as current authority;
4. current-source adoption performs Materialized -> Promoted on the real ledger entry;
5. source generation and optimizer step are exact;
6. source weight bytes and verified SHA identity are exact;
7. no additional full weight allocation occurs;
8. no additional full-weight SHA pass occurs;
9. no generation advance occurs during adoption;
10. no successor attribution is modified by adoption;
11. fresh load and durable replay use the same adoption contract;
12. R4 reentry reuses the existing Promoted authority without re-adoption;
13. initialization failure cannot leak the reservation;
14. R3H Promoted precondition remains strict;
15. R3C1 successor remains Materialized until its existing atomic apply;
16. BP-DK, R8A, packed M/V and CF11-R1 parent closures remain intact;
17. the same physical canary advances beyond E_R3H_SOURCE_WEIGHT_RESERVATION_NOT_PROMOTED.

## 20. Final Law

> The current ResidentWeightPack becomes Promoted because it has been explicitly adopted as the already-authoritative runtime source, not because a new training generation committed.

> Current-source adoption and successor generation promotion are separate authorities even though both end in HostRamReservationState::Promoted.

> Current-source adoption performs no weight copy, no extra full-weight hash, no generation advance and no successor attribution.

> The RAM36 ledger entry and the reservation snapshot stored beside the resident pack must always represent the same reservation state.

> Fresh load and durable replay perform current-source adoption; R4 keep-resident reentry verifies and reuses the already-promoted authority.

> R3H and R3C1 preconditions remain strict. This revision fixes the lifecycle so those checks pass naturally rather than weakening them.
