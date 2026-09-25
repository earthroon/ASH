# TENSORCUBE-TABLE-R4C-CF1

## WEIGHT CROSS-WAVE H2D SUBMISSION CUTOVER
## + CURRENT COMPUTE / NEXT WEIGHT TRANSFER
## + EXACT SLOT LEASE HANDOFF
## + NO GLOBAL WEIGHT-WAVE WAIT

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4C-CF1

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4C-CF1-
WEIGHT-CROSS-WAVE-H2D-SUBMISSION-CUTOVER-
EXACT-SLOT-LEASE-HANDOFF-
NO-GLOBAL-WAVE-WAIT

Direct parent:
TENSORCUBE-TABLE-R4C
```

Class:

```text
WEIGHT RESIDENCY PIPELINE
+ ASYNC H2D ORDERING
+ EXACT LIFETIME HANDOFF
+ GLOBAL-WAIT RETIREMENT

NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
NO GENERATION COMMIT AUTHORITY CHANGE
```

## 1. Exact parent debt

R4C already materializes the generation-scoped residency pipeline and compact refill control plane, but historical R4C source truth intentionally remains:

```text
TENSORCUBE_TABLE_R4C_WEIGHT_CROSS_WAVE_H2D_SUBMIT_MATERIALIZED = false
TENSORCUBE_TABLE_R4C_NO_GLOBAL_WAVE_WAIT_CUTOVER_MATERIALIZED = false
TENSORCUBE_TABLE_R4C_MEASURED_PHYSICAL_OVERLAP_MATERIALIZED = false
```

R4C-CF1 closes the first two through a real production Weight path. It does not claim measured copy-engine/compute overlap.

## 2. Physical Weight authority preserved

The physical hot-residency object remains the existing production decoder GPU bundle stored by `GpuWeightPageCache`.

R4C-CF1 does not create a second raw-page Weight cache or a qualification-only shadow Weight buffer.

```text
GPU hot Weight authority
= actual decoder GPU bundle later consumed by compute

RAM miss source
= current-generation ResidentWeightPack

HDD refill on GPU miss
= forbidden
```

The existing deterministic Atlas future-reuse-distance eviction and bounded VRAM cache budget remain authoritative.

## 3. Source implementation

New module:

```text
crates/base_train/src/tensorcube_table_r4c_cf1_weight_cross_wave_h2d.rs
```

Materialized source constants:

```text
TENSORCUBE_TABLE_R4C_CF1_WEIGHT_CROSS_WAVE_H2D_SUBMIT_MATERIALIZED = true
TENSORCUBE_TABLE_R4C_CF1_NO_GLOBAL_WEIGHT_WAVE_WAIT_MATERIALIZED = true
TENSORCUBE_TABLE_R4C_CF1_BOUNDED_REFILL_DOORBELL_MATERIALIZED = true
TENSORCUBE_TABLE_R4C_CF1_MEASURED_WEIGHT_COPY_COMPUTE_OVERLAP_MATERIALIZED = false
```

Activation:

```text
ASH_TENSORCUBE_TABLE_R4C_CF1_MODE=OFF
ASH_TENSORCUBE_TABLE_R4C_CF1_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4C_CF1_MODE=ACTIVE_VERIFIED
```

Historical R4C constants are not rewritten. R4C uses explicit child admission to derive effective closure.

## 4. Exact Weight slot identity

CF1 materializes two bounded logical prefetch slots. Each slot owns:

```text
slot index
lease epoch
bundle incarnation
source generation
logical work identity
state
```

State includes:

```text
Free
PrefetchReserved
H2dInFlight
DeviceHotReady
ExecutionLeased
Retiring
Failed
```

Slot number alone is never lifetime authority. Every reuse increments the lease epoch and bundle incarnation.

## 5. Compact refill doorbell

Materialized:

```text
WeightRefillDoorbellR4CCF1
```

It binds only compact identity/geometry metadata:

```text
source generation
work ordinal
layer index
slot index
slot lease epoch
bundle incarnation
expected source bytes
R4C progress epoch
forward/backward phase
```

No tensor payload is copied into the doorbell.

## 6. Production prefetch path

For each eligible next decoder layer:

```text
CURRENT layer work submitted
    -> tracked CURRENT same-queue fence submitted
    -> observe whether CURRENT fence remains nonterminal
    -> acquire NEXT through existing GpuWeightPageCache
       -> hit: retain existing actual decoder bundle
       -> miss: decode exact ResidentWeightPack source and materialize actual decoder GPU bundle
    -> on miss, raw-borrow the nine actual Burn Weight backings
    -> record queued Weight-write site
    -> submit one tracked A01 same-queue upload-fence SubmissionEpoch
    -> retain pending bundle + slot lease
```

The production compute bundle itself is the prefetched object. There is no shadow-upload-and-reupload path.

## 7. Real H2D and tracked fence semantics

Current Burn decoder-bundle construction performs its actual Weight uploads through the existing same WGPU queue before CF1 regains control.

CF1 then raw-borrows the nine actual bundle backings and submits an A01 tracked empty command-buffer fence on the same queue while binding exact logical write-range leases.

Therefore:

```text
Burn queue.write_buffer uploads
    -> CF1 A01 upload-fence SubmissionEpoch
    -> all later same-queue compute using that bundle
```

The A01 epoch is an exact same-queue completion fence for the already-enqueued real bundle uploads. It is not falsely described as a second copy command.

## 8. Raw actual-backing seal

CF1 raw-borrows all production decoder Weight roles:

```text
input RMSNorm
post-attention RMSNorm
Q
K
V
O
gate
up
down
```

through the existing strict raw bridge.

The bridge must resolve the same native WGPU runtime/device/queue lineage as production.

## 9. A01 Weight upload lease

For each borrowed backing CF1 registers an A01 physical allocation identity and binds an `OwnedExisting` logical range lease with:

```text
semantic role = SourceWeight
lease class   = VendorOpaque
access        = Write
exact raw buffer offset
exact raw buffer size
```

The allocation identity is an A01 lifetime/tracking identity for the borrowed physical backing. It does not create or own a second WGPU buffer.

After the upload-fence completes, CF1 releases those logical leases and retires their temporary A01 allocation registrations. The actual decoder bundle remains owned by the hot-weight cache / execution Arc.

## 10. CURRENT compute fence

After a CURRENT decoder layer has enqueued all of its lane work, CF1 submits an empty same-queue tracked compute fence and pins the actual CURRENT decoder bundle with an `Arc` until that fence completes.

This provides the structural observation:

```text
CURRENT compute still pending
```

without a host exact wait.

## 11. Cross-wave evidence definition

A real cross-wave Weight submission is counted only when:

```text
CURRENT compute fence is nonterminal
AND
NEXT actual decoder bundle miss/upload has been enqueued
AND
NEXT upload-fence SubmissionEpoch has been issued
```

R4C-CF1 records:

```text
weight_cross_wave_h2d_submit_count
weight_submit_while_current_compute_pending_count
```

RAM read-ahead opportunity, cache lookup, or ObserveOnly planning does not increment these counters.

## 12. Execution handoff and queue ordering

CF1 intentionally does not add a host `wait_for_submission_exact` before the next layer consumes the prefetched bundle.

If the NEXT upload completion callback has not yet fired when host code reaches the next layer, the bundle may be handed to the later compute path because:

```text
real Weight writes
< same-queue A01 upload fence
< later production compute submissions
```

WGPU queue ordering prevents the later compute from physically overtaking the upload.

CF1 records:

```text
handoff_while_upload_pending_count
```

as explicit evidence of this no-host-wait handoff.

Host-side lease handoff before callback completion is therefore legal only under this exact same-queue ordering. Cross-queue adoption is not admitted by CF1.

## 13. Slot reclamation

A prefetch slot is not free merely because host execution acquired the bundle.

The slot remains pinned until:

```text
upload-fence completion observed
AND
bundle handed to execution
AND
CURRENT execution fence for that handed bundle completes
```

Only then may its logical slot identity return to `Free`.

If the compute fence appears complete while its preceding upload fence remains nonterminal, CF1 fails closed with an ordering inconsistency rather than reusing the slot.

## 14. Cache hits

A same-generation `GpuWeightPageCache` hit is a valid fast path:

```text
cache hit
-> ready prefetched handle
-> zero new H2D
```

Cache-hit prefetch is tracked separately and does not qualify physical H2D cutover by itself.

A physical CF1 campaign must contain at least one actual cache miss/upload.

## 15. No HDD refill

CF1 inherits the persistent Weight source firewall.

Required runtime evidence:

```text
weight_refill_hdd_read_bytes = 0
weight_prefetch_d2h_bytes = 0
```

No cross-wave scheduling failure may silently reopen the durable Weight file as a compute source.

## 16. No global Weight-wave wait

The canonical ActiveVerified path does not insert a process/device-wide wait between every decoder layer merely to prepare NEXT Weight.

Source receipt seals:

```text
weight_prefetch_exact_wait_count = 0
ordinary_weight_global_wait_count = 0
unclassified_weight_wait_count = 0
```

Transaction/generation/durability drains remain separate parent authorities and are not reclassified as ordinary Weight-wave waits.

## 17. Forward integration

In the accumulation8 forward layer loop:

```text
acquire CURRENT from prefetched handle when available
execute all eight lanes
submit CURRENT compute fence
schedule layer+1 NEXT prefetch
release local CURRENT handle
```

The cache/execution pin keeps the physical bundle alive through exact queue completion.

## 18. Backward integration

The reverse decoder traversal applies the same law:

```text
acquire CURRENT backward layer
execute all eight backward lanes
submit CURRENT compute fence
schedule layer-1 NEXT prefetch
```

Training reduction/order semantics are unchanged.

## 19. Step drain

Before the R6 GPU gradient accumulator step exits, CF1 performs a nonblocking refresh and requires:

```text
all scheduled prefetches handed to execution
all upload fences complete
all CURRENT compute pins retired
```

The existing accumulator finalize/status path is allowed to provide the parent transaction-level GPU progress boundary. CF1 does not insert a new per-layer exact wait.

## 20. Generation boundary

CF1 forbids pending Weight uploads or live CURRENT pins from crossing generation promotion.

After existing canonical commit:

```text
G -> G+1
optimizer S -> S+1
```

CF1 rebinds its generation identity. The existing ResidentWeightPack / VRAM hot-cache generation promotion rules remain authoritative.

## 21. R3C/R3C1 firewall

CF1 introduces no generation commit call.

No Weight prefetch, doorbell processing, new upload, or GPU wait is inserted into the R3C1 no-fail mutation tail.

R3C/R3C1 remain the sole trainable-generation commit authority.

## 22. Parent R4C effective closure

R4C historical source truth remains false for the standalone parent revision.

R4C now exposes child-aware construction/seal surfaces so that explicit CF1 ActiveVerified admission may make the effective receipt report:

```text
weight_cross_wave_h2d_submit_materialized = true
no_global_wave_wait_cutover_materialized = true
```

R4C measured physical-overlap support remains false.

## 23. Parent validator maintenance

The R4C static validator previously required literal standalone receipt values:

```text
weight_cross_wave_h2d_submit_count = 0
global_wave_wait_count = None
```

CF1 updates that validator to prove both:

```text
historical standalone R4C default is still 0 / None
AND
explicit CF1 child override is accepted only through seal_with_cf1(...)
```

This is validator maintenance, not weakening of the parent gate.

## 24. Runtime receipt

New output:

```text
tensorcube_table_r4c_cf1_weight_cross_wave_h2d_receipt.json
```

Runtime log:

```text
[ASH-TENSORCUBE-TABLE-R4C-CF1][pipeline-open]
[ASH-TENSORCUBE-TABLE-R4C-CF1][performance]
```

Receipt includes:

```text
refill doorbells
cache hit/miss prefetch counts
Weight H2D submit count/bytes
cross-wave Weight H2D submit count/bytes
submit-while-CURRENT-pending count
prefetch/execution handoffs
handoff while upload callback pending
CURRENT compute fences/pending observations
pending upload peak
stale/premature/duplicate counters
exact/global/unclassified wait counters
Weight D2H / HDD refill counters
final pending uploads
final CURRENT pins
physical overlap measurement support
```

## 25. Static materialization

New validator:

```text
tools/validate_ash_tensorcube_table_r4c_cf1_weight_cross_wave_h2d_submission_static.py
```

Current result:

```text
127 / 127 PASS
PASS_TENSORCUBE_TABLE_R4C_CF1_WEIGHT_CROSS_WAVE_H2D_SUBMISSION_STATIC
```

Parent R4C validator after child-aware maintenance:

```text
82 / 82 PASS
PASS_TENSORCUBE_TABLE_R4C_CROSS_WAVE_COMPUTE_TRANSFER_OVERLAP_STATIC
```

## 26. Parent regressions

Retained:

```text
R4B-CF2        118 / 118 PASS
R4B-CF1         77 / 77 PASS
R4B             58 / 58 PASS
R4A-CF2-CF1     90 / 90 PASS
R4A-CF2         40 / 40 PASS
R4A-CF1         90 / 90 PASS
R3C              18 / 18 PASS
```

Known code-only parent baselines reproduced unchanged:

```text
R3C1 validator = 25 / 30
same five textual-count failures on unmodified R4C parent

VRAM hot-weight validator
= stops before semantic validation because
  tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
  is absent from both parent and child code-only packages
```

Neither baseline is attributed to CF1.

## 27. Exact implementation delta

Compared with the supplied R4C full code-only parent:

```text
MOD 6
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_table_r4c_cross_wave_residency_pipeline.rs
crates/base_train/src/vram_hot_weight_page_residency.rs
tools/validate_ash_tensorcube_table_r4c_cross_wave_compute_transfer_overlap_static.py
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cf1_weight_cross_wave_h2d.rs
tools/validate_ash_tensorcube_table_r4c_cf1_weight_cross_wave_h2d_submission_static.py
```

## 28. Source SHA-256

```text
c351ae850614cd7ba3306cb09f5654b5d12b82c2a2744ff6a540b080cc1c6b4f  crates/base_train/src/lib.rs
6e5022028d5529a2f6dbef1022dafaf9ab4e634e6a537b2051547bd045afc599  crates/base_train/src/packed_runtime_native_bootstrap_accumulation_wave_residency.rs
42a9a1a3895117c691d7f8177bb23d07dd227affa44cb47e34ef4f2369035b78  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
c7ab4356a7c51aed8be0abfee41fd66ae630402e6cb678363d0defe3bd7d55ea  crates/base_train/src/tensorcube_table_r4c_cross_wave_residency_pipeline.rs
0737ed464968cb3c7e1ec4a8cbcf3deed9e993e119d0abbfda8318a72f936fdd  crates/base_train/src/vram_hot_weight_page_residency.rs
8dbcabcf7463690a171bd290d67e82e5d6ec901fe1b34064b1d57c2514d0c4b8  crates/base_train/src/tensorcube_table_r4c_cf1_weight_cross_wave_h2d.rs
8adfbf9b5125134e8786c10f902a85cc29ddfb1dbbb84874d1353ac196998e6f  tools/validate_ash_tensorcube_table_r4c_cross_wave_compute_transfer_overlap_static.py
6ef8b811ebec6705dd62844513528d7bd719696e15ad79fa91cd965db0eacce3  tools/validate_ash_tensorcube_table_r4c_cf1_weight_cross_wave_h2d_submission_static.py
```

## 29. Artifact seal

```text
Overlay ZIP
SHA-256 8a1285f2e95cd2eb4ece2263a49c697ca0d52df9cf5225aa2dd89532bb436989
files 8
CRC PASS

Full code-only ZIP
SHA-256 44c92c4448d1a291fc2e85e5b340d389d89d2ff907c94650b5c479e4bda7e31c
files 8,507
CRC PASS
```

## 30. Evidence boundary

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

The bake environment exposes no Cargo/Rustc toolchain. Source delimiter sanity and Python validator compilation pass, but these do not substitute for the Rust compiler or WGPU execution.

## 31. Compile acceptance

```powershell
cargo test `
  -p base_train `
  --lib tensorcube_table_r4c_cf1_ `
  --release `
  --locked

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

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked
```

## 32. First physical campaign

First qualify planning without duplicate Weight mutation:

```powershell
$env:ASH_TENSORCUBE_TABLE_R4B_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4B_CF1_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4B_CF2_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4C_MODE="OBSERVE_ONLY"
$env:ASH_TENSORCUBE_TABLE_R4C_CF1_MODE="OBSERVE_ONLY"
```

Then, after ObserveOnly geometry/identity parity:

```powershell
$env:ASH_TENSORCUBE_TABLE_R4C_MODE="ACTIVE_VERIFIED"
$env:ASH_TENSORCUBE_TABLE_R4C_CF1_MODE="ACTIVE_VERIFIED"
```

## 33. Physical PASS requirements

At least one real cache miss must satisfy:

```text
CURRENT compute fence nonterminal
NEXT actual production decoder bundle materialized
NEXT upload-fence SubmissionEpoch issued
CURRENT still nonterminal at NEXT submission observation
NEXT eventually consumed by production without a second upload
```

Required terminal counters:

```text
weight_cross_wave_h2d_submit_count > 0
weight_submit_while_current_compute_pending_count > 0
weight_h2d_submit_count > 0
cache_miss_prefetch_count > 0
weight_prefetch_exact_wait_count = 0
ordinary_weight_global_wait_count = 0
unclassified_weight_wait_count = 0
stale_slot_completion_count = 0
premature_slot_reuse_count = 0
duplicate_weight_upload_count = 0
weight_refill_hdd_read_bytes = 0
weight_prefetch_d2h_bytes = 0
final_pending_weight_prefetch_count = 0
final_current_compute_pin_count = 0
```

Exact numerical/state parity with the parent training route remains mandatory.

## 34. Performance boundary

CF1 does not claim speedup or hardware transfer/compute overlap from source structure alone.

Measure at least:

```text
CURRENT -> NEXT useful GPU idle gap
Weight acquisition stall
Weight H2D wall time
host Weight decode/prepare time
queue submission overhead
optimizer-step wall time
generation wall time
VRAM high-water
```

If no compatible same-clock-domain overlap measurement exists:

```text
measured_weight_copy_compute_overlap_supported = false
measured_weight_copy_compute_overlap_ns = null
```

## 35. Direct successor

After compile/physical/performance evidence, choose by the measured remaining bottleneck.

If host queue/encoder overhead dominates:

```text
TENSORCUBE-TABLE-R4C-CF2
COMMAND ENCODER SUPER-WAVE
+ WEIGHT / ADAM / HIMUON SUBMISSION COALESCING
```

If host refill wakeup/doorbell overhead dominates:

```text
TENSORCUBE-TABLE-R4C-CF1-R1
REFILL TOKEN COMPACTION
+ BOUNDED DOORBELL BATCH
+ HOST WAKEUP REDUCTION
```

If transfer starts too late:

```text
TENSORCUBE-TABLE-R4C-CF1-R2
ADAPTIVE PREFETCH DISTANCE
+ BOUNDED LEAD CONTROL
```

## 36. Final law

> R4C found a Weight pipeline that could prepare RAM projections but could not yet prove that the next actual compute bundle entered the GPU queue while current useful compute remained alive.
>
> R4C-CF1 closes that source boundary. The existing hot-weight cache materializes the exact bundle production will later consume. CF1 observes its actual Burn backing, seals the queued uploads with a same-queue A01 SubmissionEpoch, retains the bundle through an exact prefetch slot lifetime, and lets later compute consume the same object without another Weight upload.
>
> Host code does not block on each upload callback. Same-queue ordering is the dependency that prevents later compute from overtaking the Weight upload. Slot reuse remains forbidden until both upload and execution lifetimes have retired.
>
> Historical R4C standalone truth remains immutable. Only explicit CF1 admission closes the effective Weight-H2D and no-global-wait gates. Physical overlap and performance remain separate future evidence.
