# EVE-MCU-R3H

## RAM36 / HIMUON / RESIDENT-WEIGHT CORESIDENT FOOTPRINT AUTHORITY

**Revision:** EVE-MCU-R3H  
**Class:** host resident-weight lifetime authority / RAM36 replacement reservation closure  
**Parent:** BP-DK-R3 + EVE-MCU-R3G-R2-CF1 + EVE-MCU-R3C-R2/R3C1

```text
+ PROJECTION-ONLY OVERLIMIT ATTRIBUTION
+ RESIDENT WEIGHT PACK LIFETIME SEPARATION
+ R3B CANDIDATE-COMPLETE POST-MATERIALIZATION RETIREMENT
+ NO EARLY COMMIT
+ NO WEIGHT RELOAD
+ NO OPTIMIZER MATH CHANGE
+ NO RAM36 HARD-LIMIT INFLATION
```

## 1. Parent physical blocker

The parent physical canary reached R3B terminal candidate state:

```text
candidate_complete=true
commit_permit_ready=true
commit_performed=false
```

The subsequent `ResidentWeightPack` reservation was rejected with:

```text
requested_bytes=4666580992
observed_private_bytes=36459945984
projected_bytes=41126526976
hard_limit_bytes=38654705664
exact_excess_bytes=2471821312
actual_private_over_limit=false
projection_only_over_limit=true
```

Therefore the blocker is a full source/successor host weight co-residency topology, not an actual 36 GiB private-memory breach.

## 2. Core authority law

Physical host residency and semantic generation commitment are independent authorities.

R3H may physically retire the no-longer-needed source host Weight backing while semantic generation remains source `G`. The semantic generation may advance only inside the existing R3C consuming commit.

R3H MUST NOT solve the blocker by increasing the RAM36 hard limit, publishing `G+1` early, replaying optimizer arithmetic, or reopening persistent source Weight payloads.

## 3. Admission boundary

Source host Weight retirement is legal only when all of the following hold:

```text
R3B candidate_complete = true
R3B commit_permit_ready = true
R3B commit_performed = false
canonical target device generation exists
target device generation coverage is complete
source resident Weight read coverage is exact
source resident Weight reader has returned
source backing Arc strong-count is exactly 1
source RAM36 reservation is Promoted
```

Failure is fail-closed.

## 4. Source last-use authority

R3H materializes `SourceResidentWeightLastUseReceiptR3H` binding:

- source/target `TrainableGenerationId`
- source Weight SHA-256 and byte count
- exact optimizer source-read coverage
- source RAM36 reservation id
- source backing strong-count / alias count
- R3B terminal candidate state
- canonical target device-generation digest

Required:

```text
observed_read_bytes == expected_read_bytes
source_backing_strong_count == 1
live_alias_count == 0
reader_closed == true
```

## 5. Replacement typestate

Canonical transition:

```text
SourceResident
  -> SourceLastUseClosed
  -> SourcePhysicallyRetired
  -> SuccessorMaterializing
  -> SuccessorMaterializedPendingCommit
  -> TargetPromoted
```

No reverse hidden reload transition is permitted.

## 6. Physical source retirement

After last-use closure:

1. remove the canonical source `ResidentWeightPack` from runtime ownership,
2. deactivate its RAM inventory authority,
3. drop the unique `Arc<Vec<u8>>` backing,
4. release its RAM36 `HostRamReservation` exactly once,
5. physically re-observe process private bytes.

No synthetic subtraction of source bytes is accepted as memory evidence.

The immutable `RetiredSourceWeightAuthorityR3H` preserves source generation identity, Weight SHA-256/bytes, reservation identity, last-use receipt, physical retirement receipt, and target-device-generation binding without retaining the source payload.

## 7. Post-retirement RAM36 admission

Successor reservation authority MUST use a fresh post-retirement physical observation:

```text
projected =
  observed_private_after_source_retirement
  + reserved_not_yet_materialized_bytes
  + successor_weight_requested_bytes
```

Required:

```text
observed_private_after_source_retirement <= hard_limit
projected <= hard_limit
```

If headroom does not physically recover:

```text
FAIL_EVE_MCU_R3H_SOURCE_RETIREMENT_HEADROOM_NOT_RECOVERED
```

No RAM36 exception, temporary ceiling, or safety-margin inflation is introduced.

## 8. Successor late materialization

On the R3C1 production-cutover path only, the old early successor `ResidentWeightPackBuilder::new()` allocation is deferred.

Other ActiveVerified paths preserve the parent allocation behavior.

After source retirement, successor Weight is materialized from the already-produced canonical target GPU generation using bounded readback windows. It is not loaded from the source pack and is not recomputed.

Canonical source:

```text
TARGET_DEVICE_GENERATION
```

Required telemetry:

```text
resident_weight_successor_d2h_bytes == target_weight_bytes
resident_weight_successor_d2h_submission_count > 0
resident_weight_successor_staging_peak_bytes < target_weight_bytes
full_temporary_copy_count == 0
```

The bounded mapped window is appended directly into the successor `ResidentWeightPackBuilder`.

## 9. No weight reload

After source host retirement, R3H introduces zero new calls to `ResidentWeightPack::load_once` and no persistent source Weight reopen fallback.

Forbidden:

```text
source weights.r6pack reopen
checkpoint fallback Weight reload
historical source payload reload
optimizer replay to reconstruct target Weight
full target temporary Vec before successor Vec
```

## 10. Target exact identity

Late successor materialization MUST validate:

```text
successor.generation == target generation
successor.optimizer_step == target optimizer generation
successor.byte_len == candidate target Weight bytes
successor.sha256 == candidate target Weight SHA-256
```

This persistent Weight-pack SHA authority is independent of BP-DK-R3 production ExactSHA retirement.

## 11. R3C source authority decoupling

R3C1 Weight preparation now accepts exactly one source authority form:

```text
Live source:
  current ResidentWeightPack + current Promoted reservation

OR

Pre-retired R3H source:
  RetiredSourceWeightAuthorityR3H
```

Cardinality mismatch is rejected.

R3C2 precommit permits an absent live source host pack only when the prepared Weight ownership is explicitly marked `source_pre_retired_r3h=true` and carries the retirement authority digest.

## 12. R3C atomic semantics

Before R3C commit:

```text
source host Weight may be physically absent
semantic committed generation remains source G
successor host Weight is fully materialized and Materialized in RAM36
R3B commit_performed remains false
```

Inside the existing consuming R3C tail:

```text
None -> successor ResidentWeightPack
None -> promoted successor RAM36 reservation
```

is allowed only for a valid pre-retired R3H source authority.

No early EVE, HiMuon, cursor, scheduler, B06, or Weight generation promotion is added.

## 13. No double retirement

When R3H pre-retires source Weight, R3C post-commit retirement sees no old source pack/reservation and MUST NOT release the source reservation again.

Required source reservation release cardinality:

```text
exactly 1
```

After R3C target promotion the RAM inventory switches successor inactive and current Weight active.

## 14. R3G preservation

R3H does not alter R3G mutation/completion authority.

Required preserved semantics:

```text
exact allocation identity
exact write range
target generation binding
submission completion
completionCoverage=EXACT_TRACKED
exactWaitDelta=0
```

R3H introduces no new `wait_for_submission_exact` callsite.

## 15. BP-DK-R3 preservation

Production BP-DK authority remains:

```text
identity_policy=RUNTIME_IDENTITY
full_payload_sha_count=0
runtime_identity_count=3
full_candidate_d2h_bytes=0
host_candidate_materialization_count=0
```

R3H successor Weight D2H is a separate host-residency operation and MUST NOT be attributed as BP-DK candidate materialization.

## 16. Optimizer math preservation

No changes are permitted to:

- AdamW equations or candidate M/V arithmetic
- Muon / HiMuon update mathematics
- gradient scaling or accumulation
- LR / weight decay / epsilon / beta values
- target Weight numerical values

R3H changes host lifetime authority only.

## 17. Runtime witnesses

Expected R3H sequence:

```text
[ASH-EVE-MCU-R3H][replacement-required]
  actual_private_over_limit=false

[ASH-EVE-MCU-R3H][source-last-use-close]
  reader_closed=true
  live_alias_count=0

[ASH-EVE-MCU-R3H][source-host-retired]
  source_reservation_released=true
  semantic_generation_unchanged=true
  commit_performed=false

[ASH-EVE-MCU-R3H][successor-materialized]
  source=TARGET_DEVICE_GENERATION
  digest_exact=true
  full_temporary_copy_count=0
  admitted=true

[ASH-EVE-MCU-R3H][r3c-commit]
  source_host_weight_retired=true
  successor_host_weight_materialized=true
  semantic_generation_promoted_at_r3c=true
  r3c_generation_binding=true
  admitted=true
```

The existing R3G/R3C/BP-DK witnesses must then follow.

## 18. Negative controls

R3H must reject:

- actual private bytes already above hard limit,
- source read coverage incomplete,
- source Weight Arc alias still live,
- target device generation missing/incomplete,
- physical post-retirement headroom not recovered,
- successor Weight SHA/byte drift,
- source authority cardinality drift,
- non-Weight owner attempts to use replacement classification,
- hidden source Weight reload.

## 19. Source scope

Code delta is intentionally narrow.

```text
ADD
crates/base_train/src/resident_weight_replacement_authority_r3h.rs

MOD
crates/base_train/src/eve_himuon_full_trainable_generation_commit_r3c.rs
crates/base_train/src/eve_himuon_full_trainable_generation_production_cutover_r3c1.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_budget_exact_inventory.rs
crates/base_train/src/ram_weight_pack_persistent_residency.rs
```

No `ram36_process_budget.rs` hard-limit change is present.

## 20. Static seals from bake

```text
ADD 1
MOD 6
DEL 0

RAM36 hard limit parent/work:
38_654_705_664 / 38_654_705_664

new wait_for_submission_exact callsites = 0
new ResidentWeightPack::load_once callsites = 0
changed Rust delimiter scan = PASS
full ZIP CRC = PASS
overlay ZIP CRC = PASS
```

## 21. Baked artifacts

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_RAM36_HIMUON_RESIDENT_WEIGHT_CORESIDENT_FOOTPRINT_AUTHORITY_CODE_ONLY.zip
SHA-256 6269b9567959727efc4ec3bb058c8c843e363c2d8e439bf4c39c9194ca8e4b3a
Files 8426
CRC PASS
```

Overlay:

```text
ASH_EVE_MCU_R3H_RAM36_HIMUON_RESIDENT_WEIGHT_CORESIDENT_FOOTPRINT_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256 1e19830edc7282bf0c0966805da74aff2890af67866944fdac18ea811d2b034c
Files 7
CRC PASS
```

Both archives contain zero `specs/`, zero `artifacts/`, and zero Markdown files.

## 22. Evidence state at bake time

```text
SOURCE / STATIC   PASS
ARCHIVE           PASS
COMPILE           UNVERIFIED
RUNTIME-TEST      UNVERIFIED
PHYSICAL          UNVERIFIED
PERFORMANCE       UNMEASURED
```

The bake environment has no Rust toolchain; compile/runtime/physical claims require replay on the canonical Windows authority.

## 23. Compile / regression admission

Required:

```text
cargo test -p base_train --lib --locked r3h_
cargo test -p base_train --lib --release --locked r3h_
cargo test -p base_train --lib --release --locked r3g_r2_
cargo test -p base_train --lib --release --locked r3c_r2_
cargo test -p base_train --lib --release --locked bp_dk_r3_
cargo test -p burn_webgpu_backend --lib --release --locked
cargo build -p base_train --bin base_train --release --locked -j 1
```

Static/compile/runtime-test promotion token:

```text
PASS_EVE_MCU_R3H_RAM36_HIMUON_RESIDENT_WEIGHT_CORESIDENT_FOOTPRINT_AUTHORITY
```

## 24. Physical admission

Re-seal native CF1 for the new release binary and run the existing physical canary entrypoint:

```text
--eve-mcu-close-r2-phys-canary-r1
```

Required physical chain:

```text
R3B CandidateComplete / commit not performed
-> R3H source last-use close
-> R3H source host retirement
-> R3H post-drop RAM36 re-observation
-> R3H bounded target-device successor materialization
-> R3G EXACT_TRACKED mutation completion
-> BP-DK-R3 RuntimeIdentity / full_payload_sha_count=0
-> R3C consuming generation commit
```

Physical promotion token:

```text
PASS_EVE_MCU_R3H_PHYSICAL_RESIDENT_WEIGHT_REPLACEMENT_AUTHORITY
```

Hold token:

```text
HOLD_EVE_MCU_R3H_RESIDENT_WEIGHT_REPLACEMENT_HEADROOM_UNPROVEN
```

## 25. Completion law

R3H is complete only when the current full host Weight pack is physically retired after exact last use, process private memory is re-observed, the successor full host Weight pack is admitted and materialized from the already-produced target GPU generation without persistent Weight reload or another full temporary copy, semantic generation remains source `G` until R3C, R3G/BP-DK authority remains intact, and the 36 GiB hard limit is unchanged.
