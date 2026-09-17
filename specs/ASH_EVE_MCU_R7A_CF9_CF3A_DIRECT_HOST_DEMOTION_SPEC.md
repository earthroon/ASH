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
```

For the current Adam geometry:

```text
planned_adam_element_count=197761024
197761024 × 4 × 2 = 1582088192
```

Therefore the retired host M/V payload exactly matched one extra complete candidate M/V generation copy.

The same run later failed with:

```text
memory allocation of 2147483648 bytes failed
```

The exact 2 GiB allocation owner remains unproven at the parent evidence level.

---

## 2. Parent duplication

CF9-CF3 fixed generation-wide candidate VRAM retention by demoting completed W/M/V segments to host payload objects.

However, the parent direct-host staging still retained payload-owning completed segment entries before later canonical host adoption.

The unwanted shape is:

```text
GPU candidate W/M/V
→ host-demoted segment Vec<W/M/V>
→ generation ledger retains segment payload
→ later canonical candidate W/M/V authority receives the same payload
→ duplicate generation payload finally dropped
```

CF3A replaces this with:

```text
GPU W
→ bounded readback
→ ResidentWeightPackBuilder canonical destination

GPU M/V
→ bounded readback
→ RamResidentAdamMv candidate destination

completed generation ledger
→ metadata / digest / R3G receipt only
```

---

## 3. Direct candidate authorities

Candidate W authority:

```text
ResidentWeightPackBuilder
→ ResidentWeightPack
```

Candidate M/V authority:

```text
RamResidentAdamMv
CandidateFilling
→ direct candidate segment writes
→ CandidateComplete
```

No additional generation-wide W/M/V payload authority is permitted in direct CF3A mode.

---

## 4. Direct W demotion

Each completed Adam candidate W segment is copied through the bounded CF3A readback staging allocation and written directly to:

```text
ResidentWeightPackBuilder::write_at(...)
```

using the canonical parameter weight byte offset plus segment-local byte offset.

The completed host generation entry retains only:

```text
range identity
historical physical allocation IDs
transfer evidence
W digest
M digest
V digest
R3G mutation receipts
```

and zero candidate payload Vecs.

---

## 5. Direct M/V demotion

Mapped M/V bytes are consumed in bounded chunks and written directly to:

```text
RamResidentAdamMv::write_candidate_adam_segment_cf3a(...)
```

The direct write validates:

```text
CandidateFilling phase
canonical parameter identity
route-local segment bounds
exact M/V cardinality
no overlap
no replay
no overrun
```

Candidate M/V coverage is therefore advanced during physical segment collection instead of a later full-generation R3B copy.

---

## 6. R3B seal-only path

When the generation is direct-host-demoted:

```text
AdamWHostDemotedGenerationCf3.direct_host_demoted_cf3a == true
```

R3B no longer materializes M/V from a host-demoted payload copy.

Instead it requires:

```text
resident phase == CandidateFilling
candidate coverage exact
candidate generation == target generation
```

then performs:

```text
seal_candidate_r1(...)
```

and publishes the existing R3B receipt.

The old runtime event:

```text
[ASH-MCU-R7A-CF9-CF3][host-mv-retire-after-r3b]
```

is absent in the direct CF3A path because there is no duplicate M/V generation payload to retire.

---

## 7. B06 schema realignment

The parent B06 schema assumed any host-demoted Adam generation had produced host candidate Vec materializations.

CF3A adds:

```text
ASH_MCU_ADAMW_DIRECT_HOST_DEMOTED_GENERATION_CF3A
```

For this schema:

```text
host_demoted_segment_count == expected segment count
host_candidate_vec_materialization_count == 0
candidate W D2H bytes > 0
candidate M D2H bytes > 0
candidate V D2H bytes > 0
```

Legacy CF3 host-demoted schema preserves the previous positive host Vec requirement.

Therefore zero Vec materialization is interpreted as successful direct canonical host ownership rather than missing candidate materialization.

---

## 8. RAM36 successor reservation realignment

Direct CF3A materializes the candidate weight successor before the later R3H reservation site.

Without realignment, the later projection can treat the already-existing candidate W as a future requested allocation and double-count host headroom.

CF3A therefore binds the R3H reservation request to:

```text
existing candidate weight successor present
    → additional requested successor bytes = 0

candidate weight successor absent
    → existing parent requested-byte projection
```

The already-resident candidate remains visible through process-private accounting.

CF3A does not discount actual resident memory from RAM36.

---

## 9. Physical device residency preservation

CF3A preserves CF3's device-side behavior:

```text
max_in_flight_segments bounded
completed physical candidate segment
→ R3G completion receipt
→ direct host destination
→ GPU segment retirement
```

Generation-wide W/M/V candidate GPU residency remains forbidden.

CF9-CF2 continues to manage reusable free pages and physical trim.

---

## 10. Direct-generation metadata

`AdamWHostDemotedCandidateSegmentCf3` remains the segment receipt type for compatibility, but direct CF3A construction uses:

```text
new_direct_cf3a(...)
```

with:

```text
legacy_weight = None
legacy_m = None
legacy_v = None
```

Direct generation admission requires every segment to report:

```text
direct_host_cf3a == true
```

and generation-level:

```text
host_payload_vec_materialization_count == 0
```

---

## 11. 2 GiB allocation tracing

The parent already traced:

```text
[ASH-R3H-HOST-ALLOC-TRACE][resident-weight-builder]
[ASH-R3H-HOST-ALLOC-TRACE][objective-probe-read-range]
```

CF3A adds or preserves large-allocation attribution at canonical host owners, including:

```text
[ASH-R3H-HOST-ALLOC-TRACE][resident-weight-load-once]
[ASH-R3H-HOST-ALLOC-TRACE][ram-adam-mv-slot]
```

The exact failing 2 GiB allocation remains `UNKNOWN` until a trace site immediately identifies the matching requested size.

CF3A does not infer a root cause from the byte count alone.

---

## 12. Logging law

No per-segment direct-demotion success logging is introduced.

Successful direct demotion remains aggregated in the generation summary.

CF9-CF2 per-page physical trim success lines remain compacted as established by CF3.

Failure attribution remains detailed and fail-closed.

---

## 13. Preserved semantics

CF3A changes no:

```text
AdamW arithmetic
Muon / HiMuon arithmetic
WGSL
Device / Queue authority
R3G completion-before-retirement
R3C consuming commit semantics
CF6 packed validation
CF8 runtime evidence compaction
CF9-CF2 physical free-page trim
```

The ownership change is host-representation only:

```text
payload-owning demotion ledger
→ direct canonical candidate destinations
```

---

## 14. Explicit non-scope

CF3A does not implement:

```text
CPU historical evidence → disk write-through
planner snapshot streaming
objective-probe bounded digest scratch
packed GPU gather
new optimizer algorithm
new tensor-parallel policy
```

Canonical transactional source and candidate W/M/V remain in CPU RAM until the consuming commit/abort lifecycle resolves them.

---

## 15. Source delta

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

---

## 16. Runtime target

The direct path must close:

```text
planned_segment_count=93
direct_demoted_segment_count=93
planned_element_count=197761024
weight_direct_written_elements=197761024
m_direct_written_elements=197761024
v_direct_written_elements=197761024
host_payload_vec_materialization_count=0
terminal_live_adam_candidate_segment_count=0
```

The parent duplicate M/V retirement marker must have count zero.

---

## 17. Code-only archives

Overlay:

```text
ASH_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_OVERLAY_CODE_ONLY.zip
SHA-256 24667c1426e118d630b3f4a8c6e46bfc168935fbb4927156444135875c915d1a
FILES 11
CRC PASS
```

Full applied code-only:

```text
ASH_PASS3_EVE_MCU_R7A_CF9_CF3A_DIRECT_HOST_DEMOTION_CODE_ONLY.zip
SHA-256 4321fcf0ff3489c411216e756feaf7b24b62b3d33203328ee3e9020a98c95242
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

## 18A. User compile failure and compilefix-1

The first user-side `base_train` compile exposed two source-migration omissions rather than a numerical or ownership-contract failure.

Observed compile errors:

```text
production_multistep_loop_accumulation8_scheduler.rs
    submit_adamw_active_device_pending_segment_r1(...)
    4 legacy/reference callsites still supplied the pre-CF3A 17-argument ABI

unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
    collect_ready_once(...) still referenced demote_segment_to_host_cf3(...)
    after the legacy/reference demotion helper had been removed
```

Compilefix-1 preserves the CF3A production semantics. It only closes the reference/legacy ABI migration:

```text
legacy scheduler callsites:
    host_parameter_weight_byte_offset = src.weight_byte_offset
    direct_host_cf3a = false

legacy collect_ready_once:
    restore the parent CF3 demote_segment_to_host_cf3(...) implementation

direct production path:
    demote_segment_to_host_cf3a(...) unchanged
    direct_host_cf3a = true path unchanged
```

No optimizer math, direct-host ownership, R3G ordering, RAM36 policy or physical residency law changes.

Compilefix source SHA-256:

```text
production_multistep_loop_accumulation8_scheduler.rs
4604f0a641d0c944faea92b8a537a0e6eab35aa4a46357ffa254961d62894b40

unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
3ddb5f7c74dbf0dc36d2a2c293981330acc9eec772749d6cc478a5492f377a84
```

Static validators were rerun after compilefix and remained PASS.

Evidence boundary after compilefix bake:

```text
FIRST USER COMPILE    FAIL
CAUSE                 legacy/reference callsite ABI migration incomplete
COMPILEFIX-1          APPLIED
SOURCE / STATIC       PASS
RECOMPILE             REQUIRED
RUNTIME / PHYSICAL    UNVERIFIED
```

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
