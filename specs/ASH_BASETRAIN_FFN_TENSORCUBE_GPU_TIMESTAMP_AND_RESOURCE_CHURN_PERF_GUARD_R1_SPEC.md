# `ASH-BASETRAIN-FFN-TENSORCUBE-GPU-TIMESTAMP-AND-RESOURCE-CHURN-PERF-GUARD-R1`

## Status

```text
Patch ID
ASH-BASETRAIN-FFN-TENSORCUBE-GPU-TIMESTAMP-AND-RESOURCE-CHURN-PERF-GUARD-R1

Build revision
basetrain-ffn-tensorcube-gpu-timestamp-and-resource-churn-perf-guard-r1

Parent
ASH-BASETRAIN-FFN-TENSORCUBE-PERSISTENT-RESOURCE-SLAB-AND-BINDGROUP-REUSE-R1

Execution role
BaseTrain production performance-observation authority

Mathematical contract
unchanged from parent
```

This revision does not change the 16x16x16 Gate/Up/exact-SiLU/SwiGLU production math or the persistent texture-content policy. It adds a device-bound performance-observation surface that separates GPU timestamp evidence, host orchestration timing and physical resource-churn counters.

The purpose is to make subsequent FFN optimization decisions evidence-driven rather than inferred from dispatch count or resource topology.

---

## 1. Authority boundary

The parent remains authoritative for:

```text
weight-generation identity
FfnTextureContentKey eligibility
one persistent Gate/Up texture pair
same-allocation content repopulation
static texture bind-group reuse
dynamic weight/input/tape bind-group lifetime
16x16x16 fused production math
exact SiLU
four training-tape outputs
existing Down projection
existing backward
```

R1 observes these operations. It does not mutate them.

Forbidden authority inversion:

```text
perf receipt -> weight generation mutation
perf receipt -> texture-content key mutation
perf receipt -> production route mutation
perf receipt -> fallback selection
perf receipt -> optimizer mutation
```

---

## 2. Timing semantic separation

The revision distinguishes:

```text
GPU timestamp duration
host command-encode duration
host queue-submit duration
executor mutex wait duration
```

These values are never written into one shared duration field.

In particular:

```text
host Instant::elapsed()
!=
GPU execution time
```

No host-wall measurement is relabeled as GPU nanoseconds.

---

## 3. Timestamp capability classification

```rust
pub enum FfnGpuTimestampCapability {
    Supported,
    Unsupported,
    Unknown,
}
```

`Supported` requires the existing runtime device to expose:

```text
TIMESTAMP_QUERY
TIMESTAMP_QUERY_INSIDE_ENCODERS
valid positive queue timestamp period
successful persistent timestamp resource creation
```

`Unsupported` is an explicit valid device classification when required features are absent.

`Unknown` is retained for a feature-advertised but invalid/failed timestamp resource probe.

No second adapter, device or queue is requested for performance measurement.

---

## 4. Measurement mode

```rust
pub enum FfnPerfMeasurementMode {
    Disabled,
    Audit,
    Guard,
}
```

Current baked production default:

```text
Audit
```

R1 implements measurement authority and receipt collection. It does not yet apply a hard percentage regression threshold to training continuation.

`Guard` is represented in the ABI for the later threshold-promotion revision.

---

## 5. Persistent timestamp slab

New backend authority:

```text
BaseTrainFfnTensorCubePerfTimestampSlab
```

It owns, per persistent FFN executor:

```text
one Timestamp QuerySet
one QUERY_RESOLVE buffer
one compact MAP_READ readback buffer
exact timestamp period
capability classification
```

Canonical query count:

```text
4
```

Canonical compact timing payload:

```text
4 x u64 = 32 bytes
```

These resources are created with the executor lifetime, not for every FFN dispatch.

---

## 6. Query indices

```text
query 0 = texture population begin
query 1 = texture population end
query 2 = fused Gate/Up/SiLU/SwiGLU begin
query 3 = fused Gate/Up/SiLU/SwiGLU end
```

For a texture-content HIT, the population pass is not executed. Queries 0 and 1 are still initialized back-to-back so the query set remains fully resolved, while the receipt records:

```text
texturePopulationExecuted = false
populationGpuNs = None
```

A non-executed population stage is not reported as a measured 0-ns GPU operation.

---

## 7. Hot-path nonblocking rule

Production `execute()` is forbidden from performing:

```text
map_async
get_mapped_range
PollType::Wait for timing collection
blocking timestamp drain
```

The hot path may only:

```text
write GPU timestamps
resolve four query values
copy the 32-byte compact timing result into the persistent readback buffer
submit the existing command encoder
```

This keeps performance observation from inserting a mandatory CPU/GPU synchronization point into every FFN invocation.

---

## 8. Explicit audit drain

GPU nanoseconds become authoritative only through:

```text
BaseTrainFfnTensorCubePersistentExecutor::collect_pending_perf_sample_blocking(...)
```

The route context exposes:

```text
AtlasRuntimeRouteAdmissionContext::collect_ffn_perf_sample_blocking(...)
```

The blocking `map_async + PollType::Wait` operation exists only behind this explicit audit/drain API.

Therefore:

```text
production execute
!=
blocking timing collection
```

---

## 9. Single outstanding timestamp ticket

R1 intentionally allows at most one unresolved timestamp sample per persistent executor.

State:

```text
next_perf_ticket_serial
pending_perf_sample
```

If no sample is pending and timestamp capture is supported:

```text
capture issued
new ticket serial allocated
```

If a prior ticket has not been drained:

```text
new GPU timing capture skipped
production FFN execution continues
```

Receipt field:

```text
timestampCaptureSkippedPending
```

This prevents the persistent 32-byte readback slot from being overwritten before explicit collection while avoiding a hot-path wait.

R1 does not claim continuous every-invocation timestamp coverage.

---

## 10. Consumer classification

```rust
pub enum FfnPerfConsumerKind {
    Forward,
    BackwardRecompute,
}
```

Both authoritative forward callsites pass:

```text
Forward
```

Both real-loss backward recomputation callsites pass:

```text
BackwardRecompute
```

This prevents forward and recomputation samples from being silently aggregated into one undifferentiated timing class.

---

## 11. Execution classification

```rust
pub enum FfnPerfExecutionClass {
    ColdExecutor,
    WarmContentMiss,
    WarmContentHit,
    GenerationTransition,
    LayerTransition,
}
```

Classification uses the existing exact `FfnTextureContentKey` and persistent executor state.

### ColdExecutor

First production use before initialization has been reported.

### WarmContentHit

Exact content key equality. Texture population is skipped.

### LayerTransition

Previous and requested layer differ while the one-slot allocation is reused.

### GenerationTransition

Same layer surface with a changed authoritative source weight generation.

### WarmContentMiss

Other exact-key mismatch, including source-buffer identity/range drift.

---

## 12. Resource churn receipt

New receipt:

```text
FfnResourceChurnReceipt
```

It records:

```text
pipeline create count
pipeline-layout create count
bind-group-layout create count
texture create count
texture-view create count
static bind-group create count
static bind-group reuse count
dynamic population bind-group create count
dynamic fused bind-group create count
uniform buffer create count
uniform write count
blocking device poll count
content request count
content hit count
content miss count
population dispatch count
population skip count
```

Raw counts remain authority. A percentage-only reuse claim is not sufficient.

---

## 13. Churn invariants

R1 seals:

```text
contentRequestCount
=
contentHitCount + contentMissCount
```

```text
contentHitCount
=
populationSkipCount
```

```text
contentMissCount
=
populationDispatchCount
```

Violation fails receipt sealing.

---

## 14. Parent persistent-reuse truth

Warm invocation evidence continues to distinguish:

```text
pipeline creation avoided
texture allocation avoided
texture-view allocation avoided
static texture bind-group reuse
persistent uniform reuse
```

Dynamic source and output bind groups remain invocation-local by design.

R1 does not reinterpret their creation as a persistent-resource regression.

---

## 15. Immediate production perf receipt

New hot-path receipt:

```text
BaseTrainFfnTensorCubeGpuPerfDispatchReceipt
```

It records:

```text
patch/build identity
measurement mode
timestamp capability
timestamp capture state
timestamp ticket serial
consumer kind
execution class
layer index
actual source weight generation
batch / seq_len / token_count
content-key digest
texture content hit state
texture population execution state
host encode ns
host submit ns
executor lock wait ns
queue submit count
resource-churn receipt digest
payload readback count
```

GPU duration fields in this hot-path receipt are required to remain:

```text
None
```

They are not populated from host timers.

---

## 16. Collected GPU receipt

Explicit audit drain returns:

```text
BaseTrainFfnTensorCubeGpuPerfCollectedReceipt
```

It contains:

```text
exact ticket serial
consumer kind
execution class
layer index
actual source weight generation
shape identity
content-key digest
raw four timestamp ticks
timestamp period
optional population GPU ns
fused GPU ns
whole texture-FFN GPU ns
compact timing readback count
payload readback count = 0
timestamp-order validity
receipt digest
```

The only CPU readback in this operation is the 32-byte timing payload.

Tensor/weight payload readback remains zero.

---

## 17. Timestamp ordering

For a MISS:

```text
populationBegin <= populationEnd <= fusedBegin < fusedEnd
```

For a HIT:

```text
population stage marked not executed
fusedBegin < fusedEnd
```

Invalid order is rejected rather than converted into a duration.

---

## 18. GPU duration conversion

GPU duration is derived only as:

```text
deltaTicks * queueTimestampPeriodNs
```

The receipt retains both raw ticks and the conversion period.

Invalid/non-finite/non-positive timestamp periods do not produce fabricated GPU durations.

---

## 19. Production forward observability

`AtlasRuntimeForwardLayerReceipt` now binds:

```text
ffnPerfReceiptDigest
ffnPerfExecutionClass
ffnPerfTimestampSupported
ffnPerfTimestampCaptureIssued
ffnPerfTimestampTicketSerial
ffnPerfContentKeyDigest
```

The timestamp ticket makes later explicit audit drain traceable to the layer receipt that scheduled the query.

---

## 20. Backward recomputation observability

Backward recomputation uses the same production executor and receives its own:

```text
BackwardRecompute
```

consumer classification.

No separate mathematical or fallback implementation is introduced for performance measurement.

---

## 21. Aggregation helpers

R1 provides:

```text
nearest_rank_percentile(...)
aggregate_gpu_samples(...)
```

Aggregate output includes:

```text
sample count
minimum
median
mean
p95
maximum
aggregate digest
```

The current implementation does not automatically drain and aggregate production invocations. Explicit audit/harness code must collect samples first.

---

## 22. Content-performance window ABI

R1 defines:

```text
FfnTextureContentPerfWindow
```

with:

```text
content-key digest
population count
fused consume count
first/last use serial
sealed state
```

This is the ABI surface for later population-amortization accounting.

R1 does not yet promote an automatic long-horizon window manager into production state.

---

## 23. Population amortization boundary

The performance model distinguishes:

```text
content MISS
population + fused
```

from:

```text
content HIT
fused only
```

A later audit harness may derive:

```text
amortized population cost
=
population GPU duration / exact-content consume count
```

Only uses under the same exact content-key lifetime may share that amortization window.

Cross-generation amortization is forbidden.

---

## 24. Down projection boundary

The current timestamp slab measures:

```text
texture population
fused Gate/Up/exact-SiLU/SwiGLU
```

Existing Down projection remains outside the R1 four-query measurement envelope.

R1 therefore does not claim a measured whole-FFN value including Down.

Down timing/fusion remains a later revision decision after the fused-stage evidence is collected.

---

## 25. No hard regression threshold yet

R1 does not encode an arbitrary rule such as:

```text
candidate must be 10% faster
```

The first promotion target is trustworthy measurement authority.

A subsequent revision may add a baseline-bound median/p95 regression threshold after sufficient physical samples exist on the same device/model/geometry.

---

## 26. Timestamp unsupported behavior

When timestamp features are unavailable:

```text
timestampSupported = false
timestampCaptureIssued = false
timestampTicketSerial = None
GPU duration fields = None
```

Production math continues.

Host encode/submit/lock timings may still be reported under their own host fields.

They are not promoted into GPU fields.

---

## 27. Timestamp probe failure behavior

If timestamp features are advertised but persistent query resources or timestamp period validation fail:

```text
capability = Unknown
GPU duration remains unavailable
```

R1 does not silently request another device or replace the measurement with a CPU timer.

---

## 28. No measurement-induced fallback

Forbidden:

```text
timestamp unsupported -> legacy FFN
timestamp collection failure -> legacy FFN
perf receipt unavailable -> CPU FFN
```

Performance telemetry has no production writer-selection authority.

---

## 29. Parent mathematical preservation

Static closure requires unchanged:

```text
@workgroup_size(64, 1, 1)
16x16x16 mapping
integer textureLoad
no sampler
exact SiLU using exp
four training-tape writes
one persistent texture slot
exact FfnTextureContentKey equality
```

No SiLU LUT is introduced.

---

## 30. Implementation surfaces

New:

```text
crates/burn_webgpu_backend/src/
  base_train_ffn_tensorcube_perf_guard.rs

tools/
  validate_basetrain_ffn_tensorcube_gpu_timestamp_and_resource_churn_perf_guard_r1_static.py
```

Modified:

```text
crates/burn_webgpu_backend/src/
  base_train_ffn_tensorcube_persistent_executor.rs
  lib.rs

crates/model_core/src/
  actual_decoder_block_split_forward.rs

crates/base_train/src/
  atlas_runtime_route_admission.rs
  atlas_runtime_forward_wave_execution.rs
  atlas_runtime_real_loss_backward.rs
```

No WGSL math source is changed by this revision.

---

## 31. Static validation

Current baked result:

```text
GPU timestamp and resource churn perf guard
101 / 101 PASS

Persistent resource slab parent
66 / 66 PASS

16x16x16 fused production parent
45 / 45 PASS

Local Muon PAD17 parent regression
52 / 52 PASS
```

The new validator verifies at minimum:

```text
explicit capability states
GPU/host timing field separation
persistent query/resolve/readback slab
one outstanding timestamp ticket
no hot-path blocking map/poll
timestamp markers around population/fused stages
resource-churn counters and invariants
forward/backward consumer classification
forward ticket observability
exact source generation/content-key binding
aggregate helpers
unchanged fused math and residency policy
```

---

## 32. Legacy validator availability boundary

Some older R2/R2B/R2D validators require `specs/cli/*.args` files that are not present in the lightweight baked parent package.

Those validators cannot be executed from this package without restoring external CLI-spec assets.

R1 does not manufacture replacement CLI files or report those unavailable validators as PASS.

---

## 33. Compile and physical evidence status

The bake environment used for this revision does not provide the Rust toolchain or a physical WGPU training device.

Therefore:

```text
cargo fmt/check = not established here
physical timestamp collection = not established here
GPU speedup = not established here
```

Static structure is established; physical timing remains the user's local runtime authority.

---

## 34. Local validation order

```powershell
cd D:\1111113232\DUST\1\ash_pass3

cargo fmt --all -- --check
cargo check -p burn_webgpu_backend --release
cargo check -p model_core --release
cargo check -p base_train --release

python tools\validate_basetrain_ffn_tensorcube_gpu_timestamp_and_resource_churn_perf_guard_r1_static.py
python tools\validate_basetrain_ffn_tensorcube_persistent_resource_slab_and_bindgroup_reuse_r1_static.py
python tools\validate_basetrain_ffn_tensorcube_16x16x16_gate_up_swiglu_fused_production_r1_static.py
python tools\validate_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1_static.py
```

N8 is not required for the first performance-measurement promotion.

---

## 35. Packaging closure

The baked code ZIPs exclude:

```text
Markdown specs
*.sha256
manifest JSON
runtime artifact JSON
report JSON
```

The Markdown specification is committed separately to GitHub.

Current bake:

```text
full body files = 7036
overlay files   = 8
```

Both ZIPs passed archive integrity verification.

---

## 36. Next decision after physical receipts

The next optimization is chosen from actual evidence.

If texture population dominates MISS cost:

```text
multi-slot / layer-local texture residency
```

If fused dispatch dominates:

```text
input staging / instruction / precision work
```

If host dynamic binding dominates:

```text
dynamic binding slab/lease reuse
```

If Down dominates the remaining FFN envelope:

```text
Down projection production optimization
```

No one of these is promoted before the timing receipts identify the actual bottleneck.

---

## Final seal

```text
The previous revisions changed the FFN execution path.
This revision changes what can be proven about that path.

GPU time is GPU timestamp time.
Host time stays host time.
A stage that did not execute has no fabricated 0-ns measurement.
A device without timestamp support is classified explicitly.

The persistent executor owns one compact query/resolve/readback slab.
Production execution writes timestamps without waiting for them.
One outstanding ticket protects the timing slot from overwrite.
The explicit audit drain is the only place where blocking readback occurs.

Resource reuse is represented by raw create/reuse counts, not by a guessed percentage.
Content HIT, MISS, layer transition and weight-generation transition remain distinct classes.

No kernel math changes.
No cache policy changes.
No optimizer changes.
No fallback route appears.

The next optimization is selected from physical receipts, not from intuition.
```
