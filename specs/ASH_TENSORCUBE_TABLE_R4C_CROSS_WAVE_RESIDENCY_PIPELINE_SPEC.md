# TENSORCUBE-TABLE-R4C

## CROSS-WAVE COMPUTE / TRANSFER OVERLAP
## + DEVICE-DRIVEN RESIDENCY REFILL AUTHORITY
## + CURRENT / NEXT / NEXT+1 PIPELINE
## + GLOBAL-WAIT RETIREMENT PROMOTION GATE

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4C

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4C-
CROSS-WAVE-COMPUTE-TRANSFER-OVERLAP-
DEVICE-DRIVEN-RESIDENCY-REFILL-
NO-GLOBAL-WAVE-WAIT

Direct parent:
TENSORCUBE-TABLE-R4B-CF2
FULL ROUTE TRAINING ROW TABLE
```

Class:

```text
GPU PIPELINE / RESIDENCY SCHEDULING / STALL ATTRIBUTION

NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
NO GENERATION COMMIT AUTHORITY CHANGE
```

---

## 1. Exact Source Boundary Found By This Bake

The current source already contains three independent ingredients:

```text
Weight:
resident source + bounded current/next/next+1 read-ahead projection

AdamW:
ActiveDevice pending generation scheduler
with several physical segments allowed in flight

HiMuon:
ActiveAsync pending Wave scheduler
with submit-while-prior-pending telemetry

R3B:
bounded candidate M/V retirement back to RAM
```

The missing authority is not another optimizer or another queue.

The missing boundary is:

```text
one generation Table
owning a unified cross-wave residency/refill state
```

and, physically, a real Weight cross-wave H2D submit path that can execute before the unrelated CURRENT work finishes.

---

## 2. Honest Materialization Boundary

This first R4C source bake materially establishes:

```text
TENSORCUBE_TABLE_R4C_RESIDENCY_PIPELINE_AUTHORITY_MATERIALIZED = true
TENSORCUBE_TABLE_R4C_COMPACT_REFILL_CONTROL_BLOCK_MATERIALIZED = true
TENSORCUBE_TABLE_R4C_PARENT_ASYNC_TELEMETRY_BINDING_MATERIALIZED = true
```

It intentionally retains:

```text
TENSORCUBE_TABLE_R4C_WEIGHT_CROSS_WAVE_H2D_SUBMIT_MATERIALIZED = false
TENSORCUBE_TABLE_R4C_NO_GLOBAL_WAVE_WAIT_CUTOVER_MATERIALIZED = false
TENSORCUBE_TABLE_R4C_MEASURED_PHYSICAL_OVERLAP_MATERIALIZED = false
```

Therefore this source bake MUST NOT claim that full R4C cross-wave overlap has already been physically cut over.

---

## 3. ActiveVerified Fail-Closed Law

`ACTIVE_VERIFIED` is rejected until both are materialized:

```text
real Weight cross-wave H2D submission
no-global-wave-wait production cutover
```

Reserved source HOLD:

```text
HOLD_TENSORCUBE_TABLE_R4C_WEIGHT_CROSS_WAVE_H2D_SUBMIT_NOT_YET_MATERIALIZED
```

The first physical campaign is therefore `OBSERVE_ONLY`.

---

## 4. Runtime Module

New source:

```text
crates/base_train/src/
tensorcube_table_r4c_cross_wave_residency_pipeline.rs
```

Runtime type:

```text
TensorCubeTableR4CRuntime
```

Mode:

```text
ASH_TENSORCUBE_TABLE_R4C_MODE=OFF
ASH_TENSORCUBE_TABLE_R4C_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4C_MODE=ACTIVE_VERIFIED
```

R4C requires the R4B-CF2 parent to be enabled. ActiveVerified additionally requires the R4B-CF2 parent itself to be ActiveVerified.

---

## 5. Pipeline State Vocabulary

Materialized state:

```text
NotPlanned
RamPrepared
H2dReserved
H2dInFlight
DeviceHot
ComputeReady
ComputeInFlight
ComputeComplete
RetirementReady
D2hInFlight
RamCommitted
Reclaimable
Failed
```

This is physical residency/lifecycle metadata only.

No tensor payload is stored in the R4C control plane.

---

## 6. Pipeline Roles

Materialized roles:

```text
Previous
Current
Next
NextPlusOne
```

The roles are transient scheduling identities, not optimizer route identities and not training generation identities.

---

## 7. Compact Refill Control Block

Materialized:

```text
R4CRefillControlBlock
```

It records at minimum:

```text
current_work_ordinal
next_work_ordinal
next_plus_one_work_ordinal
current_state
next_state
next_plus_one_state
refill_requested
retirement_requested
progress_epoch
```

The control block contains no Weight, gradient, Adam M/V or HiMuon momentum payload.

---

## 8. Device-Driven Meaning

R4C uses this exact meaning of device-driven refill:

> Existing GPU/Table lifecycle evidence determines which logical residency operation is eligible next.

It does NOT mean:

```text
WGSL reads arbitrary system RAM
WGSL calls queue.submit
GPU owns host allocator
GPU performs unrestricted bindless WGPU resource discovery
```

Host Rust remains the queue/RAM API owner.

---

## 9. Weight Parent Binding

Production already emits the actual `CheckpointRangeReadSessionReceipt` for the accumulation-wave execution.

R4C consumes:

```text
resident_readahead_projection_count
resident_readahead_projection_bytes
resident_readahead_wall_ns
physical_source_read_bytes
```

Under admitted R4C execution:

```text
physical_source_read_bytes = 0
```

is fail-closed.

Weight source disk I/O is not reintroduced as a refill mechanism.

---

## 10. Weight Read-Ahead Meaning In This Bake

A nonzero:

```text
resident_readahead_projection_count
```

establishes a real bounded `NEXT+1 RAM PREPARED` opportunity.

It does NOT yet establish:

```text
NEXT H2D physically submitted before CURRENT completion
```

For that reason the receipt currently records:

```text
weight_cross_wave_h2d_submit_count = 0
```

and the ActiveVerified gate remains closed.

---

## 11. Adam Parent Binding

R4C reuses the actual:

```text
AdamWPendingGenerationSchedulerReceiptR1
```

and records:

```text
submitted_segment_count
peak_pending_segment_count
max_in_flight_segments
ordinary_exact_wait_count
```

Required:

```text
ordinary_exact_wait_count = 0
```

No new Adam execution scheduler is introduced.

---

## 12. HiMuon Parent Binding

R4C exposes a read-only source surface:

```text
ProductionMuonRuntime::pending_wave_queue_telemetry_r4c()
```

It returns the existing session-cumulative:

```text
ProductionMuonPendingQueueCutoverTelemetryR1
```

R4C records:

```text
submitted_wave_count
peak_pending_wave_count
submit_while_prior_pending_count
active_path_exact_wait_count
```

Required:

```text
active_path_exact_wait_count = 0
```

No second HiMuon pending queue is introduced.

---

## 13. Cumulative Telemetry Handling

The HiMuon pending-queue telemetry is session-cumulative.

R4C therefore keeps the latest/high-water snapshot rather than summing the same cumulative counters again at every optimizer generation.

This prevents artificial inflation of:

```text
submitted waves
submit-while-prior-pending
exact-wait counts
```

---

## 14. Previous Retirement Binding

R4C consumes the actual R3B CandidateComplete receipt and records:

```text
logical_window_count
peak_writeback_windows_in_flight
candidate_m_d2h_bytes
candidate_v_d2h_bytes
```

Required:

```text
Adam disk read bytes = 0
Adam disk write bytes = 0
```

Candidate M/V PCIe retirement remains explicit. It is not mislabeled as zero-copy execution.

---

## 15. Structural Parent Async Observation

The source records:

```text
structural_parent_async_observed
```

when any existing parent demonstrates bounded asynchronous structure, including:

```text
Adam peak pending > 1
HiMuon peak pending > 1
HiMuon submit while prior pending > 0
R3B retirement peak > 1
```

This is parent topology evidence.

It is NOT proof of Weight/compute overlap or copy-engine/compute concurrency.

---

## 16. Physical Overlap Evidence Separation

The receipt explicitly retains:

```text
measured_physical_overlap_supported = false
measured_physical_overlap_ns = null
```

until a compatible same-clock-domain physical measurement is actually materialized.

R4C must never infer physical GPU overlap by comparing unrelated host wall-clock intervals with GPU timestamp intervals.

---

## 17. Global Wait Evidence Separation

This first bake does not pretend that all global waits have already been classified.

Receipt:

```text
global_wave_wait_count_measured = false
global_wave_wait_count = null
```

This is the exact reason:

```text
TENSORCUBE_TABLE_R4C_NO_GLOBAL_WAVE_WAIT_CUTOVER_MATERIALIZED = false
```

remains source truth.

---

## 18. Production Integration

R4C is opened once beside the R4B/R4B-CF1/R4B-CF2 generation runtimes.

Production integration points are:

```text
1. after actual R6 accumulation-wave execution
   -> observe Weight resident read-ahead

2. after actual Adam target + R3B CandidateComplete exist
   -> observe Adam pending / HiMuon pending / R3B retirement

3. after canonical generation commit
   -> generation rebind

4. final report boundary
   -> seal R4C receipt
```

No duplicate optimizer or HiMuon execution is performed for R4C observation.

---

## 19. Generation Rebind

After successful canonical generation commit:

```text
G   -> G+1
S   -> S+1
```

R4C resets the transient refill control block and increments:

```text
generation_rebind_count
```

R4C does not commit generation itself.

---

## 20. Runtime Receipt

Output:

```text
tensorcube_table_r4c_cross_wave_residency_pipeline_receipt.json
```

Production logs:

```text
[ASH-TENSORCUBE-TABLE-R4C][pipeline-open]
[ASH-TENSORCUBE-TABLE-R4C][performance]
```

The performance receipt includes:

```text
observed_work_domain_count
current_compute_count
weight_readahead_projection_count
weight_readahead_projection_bytes
weight_readahead_wall_ns
weight_next_plus_one_prepare_opportunity_count
weight_cross_wave_h2d_submit_count

Adam submitted / peak pending / max in flight / exact waits

HiMuon submitted / peak pending /
submit-while-prior-pending / exact waits

R3B retirement windows / peak / M/V D2H

structural parent async observation
refill opportunity observation
global-wait measurement support
physical-overlap measurement support
```

---

## 21. No New Math / No New GPU Backend

The new R4C module contains no:

```text
queue.submit
map_async
create_shader_module
create_compute_pipeline
Vec<f32> tensor payload
new optimizer route classifier
R3C commit call
```

It is a runtime control/attribution authority layered on existing execution parents.

---

## 22. Exact Source Delta

Compared with the supplied R4B-CF2 full code-only parent:

```text
MOD 3
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cross_wave_residency_pipeline.rs
tools/validate_ash_tensorcube_table_r4c_cross_wave_compute_transfer_overlap_static.py
```

---

## 23. Static Qualification

New validator:

```text
tools/validate_ash_tensorcube_table_r4c_cross_wave_compute_transfer_overlap_static.py
```

Current result:

```text
82 / 82 PASS
PASS_TENSORCUBE_TABLE_R4C_CROSS_WAVE_COMPUTE_TRANSFER_OVERLAP_STATIC
```

Modified Rust source delimiter sanity:

```text
PASS
```

Python validator `py_compile`:

```text
PASS
```

---

## 24. Parent Regression

Retained:

```text
R4B-CF2       118 / 118 PASS
R4B-CF1        77 / 77 PASS
R4B            58 / 58 PASS
R4A-CF2-CF1    90 / 90 PASS
R4A-CF2        40 / 40 PASS
R4A-CF1        90 / 90 PASS
R3C             18 / 18 PASS
```

Known parent baselines reproduced unchanged:

```text
ActiveAsync R2 validator:
missing historical BpDkDevicePostUpdateRuntimeR1::new(device) textual prerequisite
same on unmodified R4B-CF2 parent

R3C1 validator:
25 / 30 PASS
same five textual-count failures on unmodified R4B-CF2 parent
```

Neither is attributed to R4C.

---

## 25. Artifact Seal

```text
Overlay ZIP
ASH_TENSORCUBE_TABLE_R4C_CROSS_WAVE_RESIDENCY_PIPELINE_OVERLAY_CODE_ONLY.zip
SHA-256 0fc3bf596d36a9490559b89ca0a52ebd8c06a69332833e3dabffb5ffb2dbdd5c
files 5
CRC PASS

Full code-only ZIP
ASH_PASS3_TENSORCUBE_TABLE_R4C_CROSS_WAVE_RESIDENCY_PIPELINE_CODE_ONLY.zip
SHA-256 3fb197097b958987f7673ccfb06150204c0a397c0f9be11dcfe2e740c04ad35b
files 8,505
CRC PASS
```

---

## 26. Evidence Boundary

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

The bake environment exposes no Cargo/Rustc/WGPU physical execution authority.

---

## 27. Compile Acceptance

```powershell
cargo test `
  -p base_train `
  --lib tensorcube_table_r4c_ `
  --release `
  --locked

cargo test `
  -p base_train `
  --lib tensorcube_table_r4b_cf2_ `
  --release `
  --locked

cargo test `
  -p base_train `
  --lib tensorcube_table_r4b_cf1_ `
  --release `
  --locked

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked
```

---

## 28. First Physical Campaign

Use:

```powershell
$env:ASH_TENSORCUBE_TABLE_R4B_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4B_CF1_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4B_CF2_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4C_MODE="OBSERVE_ONLY"
```

R4C ObserveOnly should answer:

```text
weight readahead opportunity count > 0 ?
Adam pending peak > 1 ?
HiMuon pending peak > 1 ?
HiMuon submit-while-prior-pending > 0 ?
R3B retirement peak > 1 ?
which parent still serializes the useful path ?
```

---

## 29. First ObserveOnly Acceptance

At minimum:

```text
observed_work_domain_count > 0
current_compute_count > 0

weight source physical read bytes = 0
Adam ordinary exact wait count = 0
HiMuon active-path exact wait count = 0
Adam ordinary disk bytes = 0

weight_cross_wave_h2d_submit_count = 0
active_verified_admitted = false
```

The final two values are expected for this first bake and quantify the exact next debt.

---

## 30. Direct Successor

Exact next source revision:

```text
TENSORCUBE-TABLE-R4C-CF1

WEIGHT CROSS-WAVE H2D SUBMISSION CUTOVER
+ CURRENT COMPUTE / NEXT WEIGHT TRANSFER
+ EXACT SLOT LEASE HANDOFF
+ NO GLOBAL WAVE WAIT
+ BOUNDED REFILL DOORBELL
```

CF1 must materially turn:

```text
TENSORCUBE_TABLE_R4C_WEIGHT_CROSS_WAVE_H2D_SUBMIT_MATERIALIZED
```

from false to true through a real tracked submission path rather than a source constant alone.

After that the next child may address command/submission coalescing if host encode/submit overhead remains visible.

---

## 31. Final Law

> R4B-CF2 tells the runtime what the complete training generation contains.
>
> R4C begins the transition from a state directory into a pipeline scheduler.
>
> This first bake unifies existing Weight read-ahead, Adam pending execution, HiMuon ActiveAsync execution, and R3B retirement evidence under one residency pipeline authority.
>
> It does not falsify the one missing physical link. Weight read-ahead is currently a bounded RAM projection opportunity, not yet a proven cross-wave H2D submission.
>
> Therefore ActiveVerified remains fail-closed.
>
> The next child must connect that exact Weight H2D boundary, then remove the remaining unnecessary global Wave wait under exact SubmissionEpoch and slot-lifetime authority.
