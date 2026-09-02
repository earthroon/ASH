# ASH-MCU-EVE-ADAMW-ACTIVEDEVICE-TARGET-TO-BOUNDED-RAM-WRITEBACK-CIRCULATION-AND-EVE-CANDIDATE-COMPLETE-CLOSURE-R3B

## 0. Revision

```text
Patch ID:
ASH-MCU-EVE-ADAMW-ACTIVEDEVICE-TARGET
-TO-BOUNDED-RAM-WRITEBACK-CIRCULATION
-AND-EVE-CANDIDATE-COMPLETE-CLOSURE-R3B

Short name:
ADAM'S RIB EVE R3B
ADAMW ACTIVEDEVICE TARGET -> BOUNDED EVE RAM WRITEBACK -> CANDIDATE COMPLETE

Status:
SPEC RELEASE
```

Authority ceiling:

```text
R3A device-generation handoff consumption        OPEN
bounded candidate M/V D2H                        OPEN
Eve candidate RAM write                          OPEN
HiMuon inherited M/V copy-forward                OPEN
Eve candidate coverage closure                   OPEN
Eve candidate M/V digest closure                 OPEN
Eve CandidateComplete                            OPEN
Eve candidate seal                               OPEN
commit-permit-ready boundary                     OPEN

Eve committed generation advance                 CLOSED
physical committed M/V mutation                  CLOSED
RamAdamMvSwapPermit execution                     CLOSED
HiMuon + AdamW full-trainable generation commit  CLOSED
durable Adam writeback                           CLOSED
ordinary-step Adam durable-format retirement     CLOSED
device-hot Eve                                   CLOSED
physical N8 PASS                                 NOT CLAIMED
```

---

## 1. Direct Parent

R3B directly inherits:

```text
ASH-MCU-EVE-EXACT-ADAM-SEGMENT-LEASE
-AND-GENERATION-OWNERSHIP-CLOSURE-R3A
```

R3A terminal truth is:

```text
Eve committed generation = G
Eve candidate generation = G+1
Eve phase = CandidateFilling
AdamW device target G+1 = complete
R3A handoff = ready
candidate M D2H bytes = 0
candidate V D2H bytes = 0
```

R3B consumes that exact handoff. It MUST NOT rediscover generation identity independently.

---

## 2. Existing Source Truth

Current R3A already materializes:

```text
EveAdamSegmentLeaseIdentityR3A
EveRamAdamSegmentLeaseR3A
issue_eve_adam_segment_lease_r3a
submit_from_eve_source_r3a
McuEveAdamDeviceGenerationHandoffR3A
```

The current `AdamWDeviceSegmentedGenerationR1` retains exact candidate segments with candidate M/V device buffers, canonical parameter index, element range, physical allocation identity and SubmissionEpoch lineage.

The existing Eve RAM body `RamResidentAdamMv` already owns:

```text
write_candidate_slices
seal_candidate_r1
candidate coverage cursor
candidate M/V streaming hashers
full transactional A/B candidate storage
HiMuon route-sparse compact candidate overlay
Eve R3 CandidateFilling -> CandidateComplete transition
```

R3B MUST reuse these authorities and MUST NOT create a second Adam candidate store, second coverage ledger or second Eve generation state machine.

---

## 3. Problem Statement

After R3A:

```text
Eve RAM G
    -> exact Eve lease
    -> MCU / GPU AdamW
    -> complete device target G+1
```

is closed, but:

```text
Device Target G+1
    -> ???
    -> Eve RAM Candidate G+1
```

remains open.

GPU target completion is not Eve candidate completion. R3B closes this circulation boundary.

---

## 4. Objective

Canonical route:

```text
R3A Device Generation Handoff G+1
        |
        v
AdamWDeviceSegmentedGenerationR1
        |
        | bounded exact candidate M/V D2H
        v
Fixed Two-Slot MCU Eve Writeback Pool
        |
        v
bounded host M/V window
        |
        +-- AdamW-owned ranges: device target M/V
        |
        +-- Muon-owned ranges: committed Eve RAM M/V inherited bit-exact
        |
        v
RamResidentAdamMv::write_candidate_slices
        |
        v
full logical candidate coverage + streaming digest
        |
        v
RamResidentAdamMv::seal_candidate_r1
        |
        v
Eve CandidateComplete
        |
        v
Commit-Permit-Ready boundary
```

No Eve committed generation advance occurs in R3B.

---

## 5. Central Memory Invariant

> R3B materializes exact target Adam logical state into Eve's existing transactional candidate body without creating a full host candidate M/V pair.

Required:

```text
full candidate M host Vec count = 0
full candidate V host Vec count = 0
full Adam target host materialization count = 0
candidate weight D2H bytes = 0
```

Only bounded M/V writeback windows are permitted.

---

## 6. Non-Goals

R3B MUST NOT:

```text
commit Eve G+1
call RamResidentAdamMv::commit_candidate_r1
execute RamAdamMvSwapPermitR1
scatter sparse candidate into committed M/V
swap full A/B committed and candidate slots
advance committed Adam generation
advance WeightGeneration
advance full TrainableGeneration
alter HiMuon momentum
alter optimizer routing
change Adam mathematics
change GPU AdamW kernels
change R3A source lease semantics
change durable checkpoint format
write Adam recovery anchor
write ordinary-step Adam durable payload
materialize full candidate M/V on host
read back candidate weight
promote Device-Hot Eve
replace SubmissionEpoch
```

---

## 7. Admission

New CLI:

```text
--admit-mcu-eve-adamw-target-ram-writeback-r3b
--mcu-eve-r3b-component-window-bytes <BYTES>
```

Defaults:

```text
R3B admission = false
component window = 16 MiB
```

Required parents:

```text
Eve R3 admitted
R3A admitted
transactional RamResidentAdamMv active
R3A handoff valid
AdamWDeviceSegmentedGenerationR1 complete
R3A pending segment count = 0
R3A active device source reader count = 0
```

R3B without R3A fails closed.

---

## 8. R3A Handoff Is Sole Parent Identity

R3B MUST consume `McuEveAdamDeviceGenerationHandoffR3A` and validate:

```text
r3b_handoff_ready = true
generation exact
Eve layout digest exact
Eve range-set digest exact
mutable authority epoch exact
scheduler receipt digest exact
device generation digest exact
legacy host source count = 0
R3A candidate M/V D2H = 0
```

No workspace scan, latest-file lookup or generation rediscovery is admitted.

---

## 9. R3B State Machine

```rust
pub enum McuEveAdamWritebackPhaseR3B {
    R3aHandoffBound,
    Projecting,
    Draining,
    CandidateWritten,
    CandidateComplete,
    CommitPermitReady,
    FailedPendingRetirement,
    Aborted,
}
```

Critical transitions SHOULD use `match` over typed state.

---

## 10. Route Model

R3B introduces transport-only route identities:

```rust
pub enum EveAdamWritebackRouteKindR3B {
    MuonInherited,
    ExplicitAdamw,
}
```

and exact per-parameter route spans:

```text
canonical parameter index
parameter id
packed byte offset
logical element count
ordered route spans
```

Route spans MUST be contiguous, non-overlapping and cover the full logical parameter exactly.

R3B does not replace the canonical optimizer route owner. In HiMuon route-sparse mode it materializes its plan from the already admitted routing and packed/canonical bridge.

---

## 11. Device Generation Requirement

R3B consumes a complete `AdamWDeviceSegmentedGenerationR1`.

Required:

```text
device generation complete = true
source generation exact
target generation exact
device generation digest == R3A handoff digest binding
published parameter count exact
published element count exact
active source readers = 0
```

Partial device generation is not admissible.

---

## 12. Fixed Two-Slot Staging Pool

R3B owns exactly two reusable physical readback slots.

```text
slot count = 2
component window bytes = W
slot capacity = 2W
```

The two halves of each slot hold compact candidate M and candidate V bytes for one logical window.

After pool construction:

```text
post-pool fresh staging allocation count = 0
third staging slot creation = forbidden
```

If both slots are unavailable, the runtime progresses existing physical work rather than allocating a third slot.

---

## 13. Staging Slot State

```rust
Free
-> CopySubmitted
-> MapPending
-> Mapped
-> CandidatePublished
-> Free
```

A slot cannot be reused before GPU completion, map completion, byte consumption, unmap and SubmissionEpoch lease release.

---

## 14. M/V-Only D2H

For every ExplicitAdamw range R3B copies only:

```text
candidate M buffer
candidate V buffer
```

using exact candidate-segment physical allocation identity and byte range.

Forbidden:

```text
candidate Weight D2H
```

Required:

```text
candidate_weight_d2h_bytes = 0
```

---

## 15. SubmissionEpoch Authority

Every R3B device-to-staging copy uses the existing SubmissionEpoch / lease machinery.

Mapped bytes may be consumed only after:

```text
map_async completed
AND
physical SubmissionEpoch completion observed
```

A map callback arriving before physical completion does not authorize publication.

R3B does not introduce a second GPU-lifetime counter.

---

## 16. HiMuon Route-Sparse Semantics

For `HIMUON_ROUTE_SPARSE_TRANSACTIONAL`:

```text
ExplicitAdamw ranges
= exact device candidate M/V D2H

MuonInherited ranges
= committed Eve RAM M/V retained bit-exact
```

No Muon-owned Adam state is read back from the GPU.

Expected D2H:

```text
candidate M D2H = AdamW-owned elements * 4
candidate V D2H = AdamW-owned elements * 4
```

Muon inherited bytes are CPU RAM reads, not D2H and not disk I/O.

---

## 17. Full A/B Profile

For `FULL_TRANSACTIONAL_AB_COMPAT`, the R3B device target must cover the full Eve logical Adam state unless a later explicitly versioned hybrid-full-profile authority exists.

Expected:

```text
candidate M D2H = full canonical M bytes
candidate V D2H = full canonical V bytes
Muon inherited RAM bytes = 0
```

---

## 18. Canonical Logical Window Assembly

For each sequential packed logical window:

```text
1. Read committed Eve M/V window.
2. Resolve route spans.
3. Overlay ExplicitAdamw M/V from bounded GPU D2H.
4. Leave MuonInherited M/V unchanged.
5. Hash final logical M window.
6. Hash final logical V window.
7. Call RamResidentAdamMv::write_candidate_slices.
```

This is the canonical R3B candidate materialization path.

---

## 19. Canonical Publication Order

Candidate publication order is exact packed-byte order:

```text
0 -> canonical end
```

GPU segment submission or completion order does not define candidate order.

Before every candidate write:

```text
write byte offset == current candidate cursor
```

No cursor repair or out-of-order publication is permitted.

---

## 20. Existing Candidate Writer Is Sole RAM Mutation Path

R3B MUST use:

```rust
RamResidentAdamMv::write_candidate_slices(...)
```

It MUST NOT mutate candidate backing, sparse overlay, committed M or committed V directly.

The existing RAM Adam body remains the sole physical candidate storage owner.

---

## 21. Streaming Candidate Digest

R3B streams the final logical M/V windows into its own expected hashers while the existing candidate writer streams the same logical bytes through Eve's candidate hash state.

At terminal coverage R3B already owns expected full logical target digests.

Forbidden:

```text
post-write full candidate M rescan
post-write full candidate V rescan
```

Required:

```text
post_write_full_candidate_rescan_count = 0
```

---

## 22. Candidate Seal

After full logical candidate coverage, R3B invokes the existing:

```rust
RamResidentAdamMv::seal_candidate_r1(
    target_training_generation,
    target_optimizer_generation,
    expected_m_sha256,
    expected_v_sha256,
)
```

exactly once.

Required:

```text
candidate cursor complete
candidate sparse overlay coverage complete
candidate M digest exact
candidate V digest exact
target generation exact
```

---

## 23. Eve CandidateComplete

Successful candidate seal must result in:

```text
Eve phase = CandidateComplete
Eve candidate generation = G+1
Eve committed generation = G
```

CandidateComplete is not Committed.

---

## 24. Committed-State Mutation Firewall

R3B MUST NOT perform:

```text
full A/B slot swap
route-sparse scatter into committed M/V
committed generation advancement
```

Required:

```text
committed_slot_mutation_count delta during R3B = 0
```

---

## 25. Commit-Permit-Ready Boundary

Successful R3B may publish:

```text
commit_permit_ready = true
```

but MUST retain:

```text
commit_performed = false
```

R3B closes candidate materialization only. Final generation promotion must join Adam, HiMuon, Weight, full trainable coverage and SubmissionEpoch lineage in a later authority.

---

## 26. Downstream Full-Trainable Projection Reuse

When R3B has sealed Eve candidate RAM, later full-trainable projection MUST NOT read the same candidate Adam M/V from GPU again.

Under R3B:

```text
Weight durable projection
= existing bounded GPU weight projection

Adam M/V source for downstream manifest/durable assembly
= sealed Eve candidate RAM bounded logical view
```

This prevents duplicate Adam M/V D2H.

---

## 27. Bounded Candidate Logical Read View

`RamResidentAdamMv` exposes a bounded R3B candidate logical view for downstream consumers only after candidate state is Complete.

For full A/B it reads the candidate slot bounded range.

For HiMuon route-sparse it reconstructs a bounded target logical range from:

```text
committed M/V
+
exact AdamW sparse candidate overlay
```

No full candidate Vec is created.

---

## 28. Disk Firewall

R3B performs:

```text
Adam disk read bytes = 0
Adam disk write bytes = 0
```

R3B output destination is Eve candidate RAM, not SafeTensors, optimizer pack, recovery anchor or durable journal.

---

## 29. Failure Atomicity

Before any GPU copy, failure may abort the Eve candidate immediately if no physical R3B owners exist.

After any GPU copy submission:

```text
stop new work
retain staging ownership
retire SubmissionEpoch work
unmap buffers
release leases
verify active staging submissions = 0
then abort Eve candidate
```

Partial candidate bytes are disposable. Committed Eve G remains canonical.

---

## 30. No Rollback Copy

R3B abort does not restore candidate backing by copying the full committed state over it.

Abort resets logical candidate state and allows physical candidate/staging backing reuse.

No full-state repair copy is admitted.

---

## 31. Materialized Source

New BaseTrain module:

```text
crates/base_train/src/unified_atlas_mcu_eve_adamw_target_ram_writeback_r3b.rs
```

Key materialized source identities:

```text
ASH_MCU_EVE_ADAMW_TARGET_RAM_WRITEBACK_R3B_PATCH_ID
MCU_EVE_ADAMW_TARGET_RAM_WRITEBACK_MATERIALIZED_R3B = true
MCU_EVE_ADAMW_TARGET_RAM_WRITEBACK_STAGING_SLOT_COUNT_R3B = 2
MCU_EVE_ADAMW_TARGET_RAM_WRITEBACK_DEFAULT_COMPONENT_WINDOW_BYTES_R3B = 16 MiB
HOLD_ASH_MCU_EVE_R3B_PHYSICAL_PENDING
```

New source types include:

```text
EveAdamWritebackRouteKindR3B
EveAdamWritebackRouteSpanR3B
EveAdamWritebackParameterPlanR3B
McuEveAdamWritebackPhaseR3B
McuEveAdamWritebackCandidateCompleteReceiptR3B
```

---

## 32. Modified Integration Surfaces

R3B bake modifies the existing production spine as required across:

```text
crates/base_train/src/lib.rs
crates/base_train/src/ram_resident_adam_mv.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/config.rs
crates/base_train/src/bin/base_train.rs
crates/base_train/src/pipeline.rs
```

The existing AdamW math backend is not replaced.

---

## 33. R3B Receipt

`McuEveAdamWritebackCandidateCompleteReceiptR3B` binds at minimum:

```text
source/target generation
R3A handoff digest
device generation digest
Eve layout/range-set digest
mutable authority epoch
configured component window bytes
staging slot count/capacity
post-pool fresh staging allocation count
third-slot attempt count
logical window count
writeback SubmissionEpoch count
peak writeback windows in flight
candidate M/V D2H bytes
candidate weight D2H bytes
Muon inherited RAM read bytes
full logical candidate stream bytes
candidate write call count
candidate final cursor
R3B expected M/V digests
RAM candidate M/V digests
RAM candidate seal digest
Eve candidate seal digest
CandidateComplete state
Eve committed-generation unchanged flag
commit-permit-ready
commit-performed=false
Adam disk read/write bytes
physical-pass claim
receipt digest
```

---

## 34. Successful Receipt Invariants

```text
staging_slot_count = 2
post_pool_fresh_staging_allocation_count = 0
third_slot_attempt_count = 0
peak_writeback_windows_in_flight <= 2
candidate_weight_d2h_bytes = 0
full candidate M host Vec count = 0
full candidate V host Vec count = 0
post_write_full_candidate_rescan_count = 0
R3B expected M digest == RAM candidate M digest
R3B expected V digest == RAM candidate V digest
candidate_complete = true
Eve phase = CandidateComplete
Eve committed generation unchanged = true
committed slot mutation delta = 0
commit_permit_ready = true
commit_performed = false
Adam disk read bytes = 0
Adam disk write bytes = 0
final active staging submission count = 0
final mapped staging slot count = 0
```

---

## 35. Static Validator

New gate:

```text
tools/validate_ash_mcu_eve_adamw_target_ram_writeback_candidate_complete_r3b_static.py
```

Static PASS must prove:

```text
R3A direct parent binding
fixed two-slot staging pool
third slot forbidden
M/V-only candidate readback
candidate weight D2H absent
SubmissionEpoch/physical map guard preserved
HiMuon inherited RAM path
existing packed/canonical bridge reused
canonical sequential candidate publication
existing write_candidate_slices used
existing seal_candidate_r1 used
no direct candidate backing mutation
no committed M/V mutation
no commit_candidate_r1 call in R3B module
Eve CandidateComplete reached
Eve committed generation unchanged
no full candidate host Vec
no post-write full candidate rescan
no Adam disk I/O
failure retirement precedes candidate abort
R3B downstream projection avoids duplicate M/V GPU D2H
```

Reserved static token:

```text
PASS_ASH_MCU_EVE_ADAMW_ACTIVEDEVICE_TARGET
_TO_BOUNDED_RAM_WRITEBACK_CIRCULATION
_AND_EVE_CANDIDATE_COMPLETE_CLOSURE_R3B_STATIC
```

---

## 36. Required Parent Regressions

R3B bake must retain PASS for:

```text
Eve R1 geometry/generation ABI
Eve R2 canonical Adam math
Eve R3 mutable RAM authority
MCU Eve R3A exact segment lease
RAM Adam transactional A/B
HiMuon route-sparse R1
packed/canonical bridge R1A
sparse overlay R1B
MCU AdamW pending generation scheduler
full-model device segmented AdamW successor
SubmissionEpoch active async authority
```

No parent static gate is waived.

---

## 37. Physical Qualification

R3B physical PASS requires actual local WGPU execution with at least:

```text
2 AdamW device target segments
2 logical writeback windows
both staging slots physically used/reused
```

HiMuon route-sparse qualification additionally requires at least one AdamW route and at least one MuonInherited route.

Required evidence:

```text
R3A handoff valid
device target complete
candidate M/V D2H physically executed
candidate weight D2H = 0
staging slot peak = 2
post-pool fresh staging allocation = 0
all SubmissionEpochs complete
all staging buffers unmapped
candidate cursor complete
candidate M/V digest exact
candidate coverage exact
Eve CandidateComplete = true
Eve committed generation unchanged = true
committed M/V mutation delta = 0
commit performed = false
```

Reserved physical token:

```text
PASS_ASH_MCU_EVE_ADAMW_ACTIVEDEVICE_TARGET
_TO_BOUNDED_RAM_WRITEBACK_CIRCULATION
_AND_EVE_CANDIDATE_COMPLETE_CLOSURE_R3B_PHYSICAL
```

Until actual physical qualification:

```text
HOLD_ASH_MCU_EVE_R3B_PHYSICAL_PENDING
```

---

## 38. No Full N8 Claim Yet

R3B alone does not authorize full N8 production PASS.

`Eve CandidateComplete G+1` still must join:

```text
HiMuon target G+1
Weight target G+1
full trainable coverage
SubmissionEpoch union
one generation transaction identity
```

before committed Adam and full trainable generation may advance.

---

## 39. Negative Fixtures

Mandatory later negative fixtures include:

```text
R3B without R3A
invalid/reused R3A handoff
wrong device generation digest
incomplete device generation
active source reader remains
wrong Eve candidate generation
Eve phase not CandidateFilling
stale authority epoch
layout/range-set drift
zero or unaligned writeback window
third staging slot attempt
staging reuse before unmap/completion
map before physical completion
device AdamW segment missing/overlapping
device segment generation drift
route gap/overlap
out-of-order candidate write
candidate M/V cardinality mismatch
candidate digest mismatch
candidate coverage incomplete
candidate seal before final window
committed M/V mutation during R3B
commit_candidate_r1 attempt in R3B
candidate weight D2H attempt
Adam disk write attempt
full candidate host Vec allocation
abort before outstanding readback retirement
```

---

## 40. Bake Truth

Static bake may claim only static materialization after the new R3B gate and inherited regression gates pass.

If Cargo/Rustc or a compatible physical WGPU runtime is unavailable, the bake MUST NOT claim:

```text
Rust compile PASS
GPU physical PASS
N8 physical PASS
atomic full-trainable generation commit PASS
```

---

## 41. Terminal Authority

Successful R3B terminal truth:

```text
Eve committed = G
Eve candidate = G+1
Eve phase = CandidateComplete
AdamW device target = G+1 complete
candidate RAM = exact
candidate digest = exact
candidate coverage = complete
commit-permit-ready = true
commit performed = false
```

---

## 42. Direct Successor

Recommended successor:

```text
ASH-EVE-HIMUON-FULL-TRAINABLE-GENERATION
-COMMIT-PERMIT-JOIN
-AND-ATOMIC-ADAM-MUON-WEIGHT-PROMOTION-CLOSURE-R3C
```

Objective:

```text
Eve CandidateComplete G+1
+
HiMuon target G+1
+
Weight target G+1
+
full trainable coverage
+
SubmissionEpoch union
    -> one generation commit identity
    -> Eve commit permit
    -> atomic trainable generation promotion
```

---

## 43. Final Invariant

```text
R3A proves where Adam M/V came from.
R3B proves where the resulting Adam M/V returned.

The GPU target is read back only in bounded M/V windows.
No full host candidate world is created.

AdamW ranges come from the GPU target.
HiMuon ranges remain inherited from Eve committed RAM.
Both are assembled in canonical packed order.

The existing Eve candidate writer receives the full logical target stream.
The existing Eve candidate seal closes exact coverage and exact digest.

CandidateComplete is real.
Committed is not.

The body of Eve contains a complete G+1 candidate,
but Eve's committed crown remains G until the full trainable generation transaction grants promotion.
```

Final sentence:

> **R3B closes Eve's circulation system: Adam M/V leaves Eve through the exact R3A source lease, is transformed on the GPU, and returns through bounded MCU-controlled M/V writeback into Eve's reusable candidate body. Once every logical byte, route, coverage boundary and digest is closed, Eve may declare `CandidateComplete`, but she may not yet declare a new committed generation.**
