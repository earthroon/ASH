# EVE-MCU-R7A-CF9-CF3A

## DIRECT HOST DEMOTION + METADATA-ONLY GENERATION LEDGER

**Revision:** `EVE-MCU-R7A-CF9-CF3A`  
**Parent code:** `EVE-MCU-R7A-CF9-CF3 + COMPILEFIX-1`  
**Class:** host residency compaction / direct GPU→canonical-host transfer / duplicate generation-payload retirement

```text
+ GPU W → RESIDENT WEIGHT BUILDER DIRECT
+ GPU M/V → RAM-ADAM CANDIDATE DIRECT
+ NO GENERATION-WIDE HOST W/M/V PAYLOAD COPY
+ METADATA-ONLY DEMOTED SEGMENT LEDGER
+ R3G RECEIPT BEFORE PHYSICAL RETIREMENT
+ CF3 WAVE-BOUNDED VRAM PRESERVATION
+ R3B SEAL-ONLY DIRECT PATH
+ RAM36 EARLY-CANDIDATE DOUBLE-COUNT CLOSURE
+ 2 GiB HOST ALLOCATION ATTRIBUTION EXTENSION
+ NO SILENT LEGACY FALLBACK
```

---

## 1. Physical parent evidence

The CF9-CF3 physical run established:

```text
CF9-CF2 generation retained bytes:
2,381,119,488

CF9-CF3 generation retained bytes:
307,495,936

CF9-CF3 max in-flight segments:
4

CF9-CF3 observed host M/V duplicate retirement:
1,582,088,192 bytes

terminal host allocation failure:
2,147,483,648 bytes
```

For the admitted Adam geometry:

```text
planned segment count        = 93
planned Adam element count   = 197,761,024
full candidate M/V raw bytes = 197,761,024 × 4 × 2
                           = 1,582,088,192
```

Therefore the CF3 `host-mv-retire-after-r3b` payload was exactly one extra full-generation M/V representation.

CF3A removes that duplicate lifetime while preserving the CF3 device-residency cutover.

---

## 2. Ownership law

Production ownership after CF3A:

```text
VRAM
    bounded active / in-flight Adam segments

CPU RAM source
    current ResidentWeightPack
    current committed RamResidentAdamMv

CPU RAM candidate
    one ResidentWeightPackBuilder / ResidentWeightPack successor
    one RamResidentAdamMv candidate M/V authority

Generation ledger
    metadata + digests + R3G completion receipts only
```

Forbidden in the CF3A direct path:

```text
full generation demoted Vec<W>
full generation demoted Vec<M>
full generation demoted Vec<V>
payload-owning completed-segment generation map
```

Committed and candidate transactional state may coexist. CF3A removes only the third duplicate demotion representation.

---

## 3. Direct W demotion

After exact physical completion and R3G receipt capture, candidate W bytes are copied from bounded mapped readback directly into:

```text
ResidentWeightPackBuilder::write_at(...)
```

using the canonical host packed byte offset resolved for the Adam segment.

The completed generation metadata does not retain W payload.

For later full-trainable projection, already initialized Adam W ranges are read from the candidate builder through the bounded projection helper rather than reconstructed from segment payload vectors.

---

## 4. Direct M/V demotion

After exact physical completion, mapped candidate M/V are decoded in bounded chunks and written directly through:

```text
RamResidentAdamMv::write_candidate_adam_segment_cf3a(...)
```

into the existing route-sparse transactional candidate slots.

The direct M/V path records exact packed/canonical coverage and performs no generation-wide segment M/V retention.

At R3B, production direct mode calls:

```text
admit_mcu_eve_adamw_direct_candidate_r3b_cf3a(...)
```

R3B validates/seals the already-populated candidate M/V and performs:

```text
late GPU M D2H = 0
late GPU V D2H = 0
staging slots  = 0
```

The parent `host-mv-retire-after-r3b` operation remains only on the legacy CF3 path. It is not executed on CF3A direct production.

---

## 5. M/V exact digest closure

Physical segment completion order is not promoted as canonical digest order.

CF3A direct sealing performs one canonical host read pass over:

```text
Muon-inherited M/V → committed authority
Explicit-AdamW M/V → candidate compact overlay
```

and computes the exact canonical candidate M/V SHA-256 values.

This is a bounded host read pass. It does not materialize another full candidate M/V payload.

---

## 6. Metadata-only segment representation

The existing CF3 segment type remains dual-mode for qualification compatibility.

Legacy CF3 constructor:

```text
legacy_weight = Some(Vec<f32>)
legacy_m      = Some(Vec<f32>)
legacy_v      = Some(Vec<f32>)
direct_host_cf3a = false
```

CF3A direct constructor:

```text
legacy_weight = None
legacy_m      = None
legacy_v      = None
direct_host_cf3a = true
```

Direct generation admission requires:

```text
host_payload_vec_materialization_count_cf3a() == 0
```

The generation keeps only segment range identity, transfer evidence, W/M/V digests, submission epoch identity, physical-allocation provenance IDs, and prepared R3G receipts.

Historical physical IDs are evidence only after retirement and must not be reused as live allocations.

---

## 7. R3G law

R3G exact completion evidence is captured while the candidate physical allocations are still live:

```text
GPU writer completion
→ PreparedGpuMutationReceiptR3G2
→ direct host write
→ host validation
→ metadata publication
→ GPU segment retirement
```

Generation seal reconstructs its R3G completion set from retained immutable receipts rather than requiring old live allocations to remain resident.

No fabricated completion receipt is allowed after physical retirement.

---

## 8. B06 schema realignment

CF3A direct generation tickets use:

```text
ASH_MCU_ADAMW_DIRECT_HOST_DEMOTED_GENERATION_CF3A
```

Direct-host B06 contract:

```text
host_demoted = true
candidate W/M/V D2H bytes > 0
candidate W/M/V component bytes exact
host_candidate_vec_materialization_count == 0
device_sealed = false
```

Legacy CF3 host-demoted tickets retain the previous contract requiring payload materialization count `> 0`.

Unknown host-demoted schema revisions fail closed.

---

## 9. Bounded device residency

CF3A preserves the CF3 pending-generation bound and direct collection path.

Completed candidate segments are demoted while the generation is still open. Successful direct host demotion therefore does not migrate completed segments into a generation-wide GPU payload owner.

The physical target remains:

```text
peak live Adam candidate segments
    <= bounded producer / demotion depth

terminal live Adam candidate segment count
    == 0 before consuming commit
```

CF9-CF2 remains the physical free-page reuse/trim authority.

---

## 10. Resident weight successor authority

CF3A opens the candidate weight successor before Adam direct demotion when the direct path is active.

That candidate is the single candidate W destination used by:

```text
Adam direct W demotion
full-trainable projection
final ResidentWeightPack successor
```

The later R3H replacement stage recognizes the already-materialized direct successor and emits a direct-host materialization receipt with no second W D2H.

If no direct successor exists, the legacy R3H materialization path remains available for non-CF3A paths.

---

## 11. RAM36 accounting closure

Creating the direct candidate W earlier means it is already a real reserved/allocated host authority before the later R3H replacement phase.

CF3A therefore changes the R3H projection request law:

```text
candidate successor already exists
    → additional successor request bytes = 0

candidate successor absent
    → legacy successor request bytes
```

This prevents the same already-materialized candidate W from being counted again as a hypothetical future allocation.

It does not discount actual process-private bytes.

RAM36 hard limit remains unchanged.

---

## 12. Large host allocation tracing

The exact owner of the observed `2,147,483,648` byte host allocation remains unknown at bake time.

CF3A preserves existing traces:

```text
[ASH-R3H-HOST-ALLOC-TRACE][resident-weight-builder]
[ASH-R3H-HOST-ALLOC-TRACE][objective-probe-read-range]
```

and adds:

```text
[ASH-R3H-HOST-ALLOC-TRACE][resident-weight-load-once]
[ASH-R3H-HOST-ALLOC-TRACE][ram-adam-mv-slot]
```

The new traces emit only for large allocations and carry scalar request/capacity context. No per-wave success logging is added.

Attribution is promoted only when the failing allocation size is matched to a concrete preceding allocation trace.

---

## 13. Runtime summary

Direct production emits one aggregate marker:

```text
[ASH-MCU-R7A-CF9-CF3A][direct-host-demotion-summary]
```

The receipt includes:

```text
planned_segment_count
direct_demoted_segment_count
planned_element_count
weight_direct_written_elements
m_direct_written_elements
v_direct_written_elements
duplicate_candidate_weight_bytes=0
duplicate_candidate_m_bytes=0
duplicate_candidate_v_bytes=0
host_payload_vec_materialization_count
peak_live_device_segment_count
terminal_live_adam_candidate_segment_count
admitted=true
```

No per-segment success receipt is introduced.

---

## 14. Current physical acceptance target

For the current campaign:

```text
planned_segment_count             = 93
direct_demoted_segment_count      = 93
planned_element_count             = 197761024
weight_direct_written_elements    = 197761024
m_direct_written_elements         = 197761024
v_direct_written_elements         = 197761024
duplicate_candidate_weight_bytes  = 0
duplicate_candidate_m_bytes       = 0
duplicate_candidate_v_bytes       = 0
host_payload_vec_materialization_count = 0
terminal_live_adam_candidate_segment_count = 0
```

The direct path must not emit a successful `host-mv-retire-after-r3b` event because there is no full duplicate demoted M/V payload to retire.

---

## 15. Explicit non-scope

CF3A does not implement:

```text
CPU historical/evidence RAM → disk write-through
planner snapshot streaming
objective-probe bounded digest scratch
packed GPU gather
new optimizer mathematics
new WGSL
Device / Queue reconstruction
```

Canonical source and candidate training state legitimately remain in RAM through the transaction.

---

## 16. Source delta

```text
ADD 1
MOD 10
DEL 0
```

Added:

```text
tools/validate_ash_eve_mcu_r7a_cf9_cf3a_static.py
```

Modified:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_resident_adam_mv.rs
crates/base_train/src/ram_weight_pack_persistent_residency.rs
crates/base_train/src/resident_weight_replacement_authority_r3h.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
crates/base_train/src/unified_atlas_mcu_eve_adamw_target_ram_writeback_r3b.rs
crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
crates/burn_webgpu_backend/src/hybrid_optimizer_device_commit.rs
tools/validate_ash_basetrain_unified_atlas_mcu_full_model_device_segmented_successor_adamw_active_candidate_r1_static.py
```

Source SHA-256 after bake:

```text
d70d4df1ae039d7ea03bdfae020dfe157f0d105b18c77e74c224b506a6ef3171  production_multistep_loop_accumulation8_scheduler.rs
015f379006c9be6e9aaa5873b43b3e6e2365b8ec439f7ac60c57933d7919c27b  ram_resident_adam_mv.rs
720210e9623c500466591ae7f523798963d0431de64b6216a2bc931225035c16  ram_weight_pack_persistent_residency.rs
ff7e9cd6662dc3ee3c8756abc3e6c3f571558f2aca1540b94ff518ac6c59048d  resident_weight_replacement_authority_r3h.rs
31e32005c5e5290fd7e723cdb7f5a33ab61fd32f6c778b85dd8d2dc9ae7ca599  tensorcube_local_muon_production_callsite_adoption.rs
cc271cd2463bbff4e4ec2d9dbd534a8ac54eec7e9bca003e8bfbca8cdf148093  unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
ec7c20f4de8e590244ba68e686c2a4028277ce29a2efa6576c03bd9e6ffe1ef7  unified_atlas_mcu_eve_adamw_target_ram_writeback_r3b.rs
f1755aec057b51d3bdc919cbd3208962e1f8d59e814bb416bb510f20c3299b8d  unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
f1b5486df4056c6c6f17145c5e9744314d596d85d1b28e9aecad24a333b01a29  hybrid_optimizer_device_commit.rs
ee921c3a3186832d1b2c29fd8d93339e897c1b0841b9216fb8f607626fcce661  validate_ash_basetrain_unified_atlas_mcu_full_model_device_segmented_successor_adamw_active_candidate_r1_static.py
861978eecc2234f9f622486e5e23a44136e8b622a0353b69bcaffadf74be74bf  validate_ash_eve_mcu_r7a_cf9_cf3a_static.py
```

---

## 17. Code-only archives

Parent:

```text
ASH_PASS3_EVE_MCU_R7A_CF9_CF3_GPU_HOST_CANDIDATE_DEMOTION_WAVE_BOUNDED_DEVICE_RESIDENCY_CODE_ONLY.zip
SHA-256 1f642da5bb444f6550932073d6df7c11b1adce23a9662a3f0e4ca4caf8136b5d
```

Overlay:

```text
ASH_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_OVERLAY_CODE_ONLY.zip
SHA-256 507e688a6904580c5d20e0342152cb3c03e20172dfeefeef214db0c55c5dc059
FILES 11
CRC PASS
```

Full applied code-only:

```text
ASH_PASS3_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_CODE_ONLY.zip
SHA-256 27454cc4d0e5807b798d44855021fbcbbfb5fb969a7d0eab746cd1a0ac531fb4
FILES 8428
CRC PASS
```

Both archives contain zero:

```text
specs/
artifacts/
manifests/
Markdown
__pycache__
*.pyc
```

Build inputs such as `Cargo.toml` and `Cargo.lock` remain in the full archive.

---

## 18. Static qualification performed at bake time

Passed:

```text
PASS_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_STATIC
PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_ADAMW_ACTIVE_DEVICE_PENDING_GENERATION_PRODUCTION_SCHEDULER_MULTI_SEGMENT_COLLECT_R1_STATIC
PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_FULL_MODEL_DEVICE_SEGMENTED_SUCCESSOR_R1_STATIC
PASS_ASH_MCU_EVE_ADAMW_ACTIVEDEVICE_TARGET_TO_BOUNDED_RAM_WRITEBACK_CIRCULATION_AND_EVE_CANDIDATE_COMPLETE_CLOSURE_R3B_STATIC
PASS_ASH_BASETRAIN_RAM36_HIMUON_ROUTE_SPARSE_TRANSACTIONAL_ADAM_AB_CANDIDATE_OVERLAY_AND_RESIDENT_WEIGHT_SUCCESSOR_HEADROOM_CLOSURE_R1_STATIC
PASS_ASH_BASETRAIN_RAM36_SUCCESSOR_WEIGHT_RESERVATION_PHYSICAL_ALLOCATION_OWNERSHIP_TRANSITION_CLOSURE_R1_STATIC
PASS_ASH_BASETRAIN_RAM36_RESERVATION_PROJECTION_REMAINING_UNDERFLOW_ATTRIBUTION_CLOSURE_R1_STATIC
```

Modified Python validators also passed Python AST parsing.

---

## 19. Evidence boundary at bake time

```text
SOURCE / STATIC       PASS
ARCHIVE / CRC         PASS
RUST COMPILE          UNVERIFIED
RUST TEST             UNVERIFIED
RUNTIME               UNVERIFIED
PHYSICAL              UNVERIFIED
PERFORMANCE           UNMEASURED
2 GiB ALLOCATION OWNER UNKNOWN
```

The bake environment does not contain `cargo`, `rustc`, or `rustfmt`.

No compile, runtime, physical, memory-peak, or performance PASS is claimed.

---

## 20. Promotion tokens

Source / compile qualification:

```text
PASS_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION
```

Zero duplicate generation payload:

```text
PASS_EVE_MCU_R7A_CF9_CF3A_ZERO_GENERATION_HOST_PAYLOAD_DUPLICATION
```

Physical:

```text
PASS_EVE_MCU_R7A_CF9_CF3A_PHYSICAL
```

2 GiB owner attribution:

```text
PASS_EVE_MCU_R7A_CF9_CF3A_HOST_ALLOCATION_OWNER_ATTRIBUTED
```

Hold:

```text
HOLD_EVE_MCU_R7A_CF9_CF3A_UNPROVEN
```

---

## 21. Completion law

CF9-CF3A is complete only when:

1. GPU W is written directly into the single candidate weight authority.
2. GPU M/V are written directly into the single RamResidentAdamMv candidate authority.
3. direct completed segment metadata retains no W/M/V payload Vec.
4. B06 recognizes direct host-demoted generation with zero host candidate Vec materialization.
5. R3G completion evidence is captured before physical retirement.
6. R3B seals the already-populated direct M/V candidate without late full M/V D2H.
7. the direct path does not perform `host-mv-retire-after-r3b` because no duplicate exists.
8. the early candidate weight successor is not double-counted by later RAM36 projection.
9. CF3 wave-bounded candidate VRAM remains preserved.
10. physical W/M/V candidate bytes and digests remain exact.
11. no silent legacy full GPU or duplicate host-payload fallback occurs.
12. the 2 GiB allocation owner is attributed separately if the failure remains.

> A demoted tensor is not demoted twice. CF9-CF3A writes GPU candidate W/M/V directly into their canonical transactional host destinations and retains only metadata after each segment completes.
