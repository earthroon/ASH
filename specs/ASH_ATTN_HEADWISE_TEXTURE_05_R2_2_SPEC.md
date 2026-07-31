# ASH-ATTN-HEADWISE-TEXTURE-05-R2.2

## Per-Commit Manual Garbage Collection /
## Owner-Drop-Before-Poll Ordering /
## Deferred Destruction Drain /
## Fault-Drill Cleanup Boundary /
## GC Duration Receipt /
## Post-GC Next-Commit Admission Seal

> Status: **SPEC RELEASE rev.1**  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R2.2`  
> Build revision: `HEADWISE-TEXTURE-05-R2.2-per-commit-manual-gc-v1`  
> Parent implementation: `ASH-ATTN-HEADWISE-TEXTURE-05-R2.1-R1`  
> Parent build revision: `HEADWISE-TEXTURE-05-R2.1-eligibility-failure-localization-v1`  
> Parent runtime state: `HOLD - Texture05EligibilityHold:LatencyP95BudgetExceeded,LatencyP99BudgetExceeded`  
> Active production executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1` unchanged  
> Production output authority: `HeadwiseFullActive` unchanged  
> Candidate result authority: shadow evidence only  
> Patch-local readiness after PASS: `PerCommitManualGcBound`  
> `SustainedShadowSoakBound` claim: **forbidden until the original Texture-05 eligibility decision is Promote**

---

# 0. Source-grounded problem statement

## 0.1 Observed R2.1 runtime evidence

The localized Texture-05 run completed compilation and reached the final eligibility decision with the following disclosed values:

```text
canonicalPromotionArtifactWritten  false
diagnosticArtifactsVerified        true
diagnosticArtifactsWritten         true
disposition                        hold
falsePredicates
  latency_p95_within_budget
  latency_p99_within_budget

p50Ns             3,539,966,976
p95Ns            15,997,566,976
p99Ns            16,382,229,504
maxNs            16,382,229,504
worstGeneration  18
worstRoute       incremental_decode
worstSeqQ        1
worstSeqKv       1792
```

This proves:

```text
Confirmed
  The process did not fail during compilation.
  The gate completed enough work to seal diagnostic eligibility evidence.
  The final HOLD was caused by latency p95 and p99 predicates.
  The worst disclosed geometry was generation 18, incremental Q1, KV1792.

Not proved by the log alone
  A device-lost event.
  A hard WGPU OutOfMemory error.
  A DX12 committed-heap exhaustion event.
  A particular number of unreclaimed bytes.
```

R2.2 does not rename the observed HOLD into OOM. It closes the confirmed missing manual reclamation boundary so later evidence can distinguish live workload cost from deferred destruction pressure.

## 0.2 Confirmed current owner lifetime

The current Texture-05 soak loop creates the following commit-scoped owners outside `run_shadow_commit()`:

```rust
let registry = HeadwiseTextureSessionResidencyRegistry::default();
let tickets = HeadwiseTextureLiveShadowTicketRegistry::default();
```

`run_shadow_commit()` creates or causes creation of:

```text
Q source buffer lease
K source buffer lease
V source buffer lease
22 BufferAtlas reference outputs
22 production Q snapshots
22 reference output snapshots
22 layer K texture residencies
22 layer V texture residencies
candidate scratch
comparison scratch
compact parity resources
population / validation resources
```

Some function-local owners are dropped when `run_shadow_commit()` returns. The outer `registry` remains alive until the current loop iteration ends and owns the layer residency graph containing the generated textures.

The current gate contains no explicit post-owner-drop manual GC boundary before the next commit begins.

## 0.3 Existing poll is not the required GC poll

The Texture-05 timestamp helper already calls:

```rust
device.poll(backend_wgpu::PollType::Wait)
```

inside timestamp staging-buffer map resolution.

That poll has this purpose:

```text
submit timestamp resolve and copy
map staging buffer
wait for callback completion
read two timestamp words
```

At that point, the outer commit-scoped `registry` and `tickets` still exist because they were borrowed into the timed operation and remain in the soak-loop scope.

Therefore:

```text
existing timestamp poll
  = GPU completion / map callback wait
  != owner-drop-afterward deferred destruction drain
```

A poll executed while the residency owner is still alive cannot prove reclamation of resources still strongly owned by that registry.

R2.2 introduces a second, semantically distinct boundary:

```text
receipt materialization
  -> owner groups explicitly dropped
  -> manual GC poll(Wait)
  -> GC receipt sealed
  -> next commit admitted
```

## 0.4 Confirmed fault-drill gap

`run_bufferatlas_only_commit()` creates Q/K/V leases and 22 reference dispatch results inside the function. Those function-local owners are dropped on function return.

The current fault drill and eight post-disable commits proceed without a required manual `device.poll(PollType::Wait)` after each returned commit boundary.

R2.2 applies the same cleanup chain to:

```text
60 healthy soak commits
1 intentional fault-generation BufferAtlas-only commit
8 post-disable BufferAtlas-only commits
```

Canonical manual-GC boundary count:

```text
60 + 1 + 8 = 69
```

---

# 1. Goal

R2.2 must make GPU deferred destruction an explicit, ordered and receipt-bound stage of every Texture-05 commit.

Canonical flow:

```text
commit admission
  -> BufferAtlas and candidate work
  -> timestamp / compact evidence completion
  -> semantic receipt validation
  -> supervisor metadata adoption
  -> all commit-scoped GPU owner groups dropped
  -> device.poll(PollType::Wait)
  -> manual GC receipt sealed
  -> receipt appended to GC chain
  -> next commit admission token issued
```

The patch succeeds only when the gate proves all of the following:

```text
Every commit has one manual GC boundary.
Every GC boundary occurs after owner drop.
No next commit starts before the previous GC boundary passes.
Fault and post-disable BufferAtlas-only commits follow the same rule.
GC wait duration is measured separately from shadow GPU latency.
GC poll failure fails closed.
No latency, residency, coverage or authority threshold is weakened.
```

---

# 2. Scope boundary

## 2.1 In scope

```text
Explicit commit owner lifetime scopes
Explicit registry and ticket owner destruction
Post-drop device.poll(PollType::Wait)
Manual GC result validation
GC wall-clock duration measurement
Per-boundary GC receipt
Append-only GC receipt chain
Post-GC next-commit admission token
Fault-drill cleanup boundary
Post-disable cleanup boundary
Final GC summary
R2.2 verification gate
Rust-authored runtime artifact and local manifest
```

## 2.2 Explicitly out of scope

```text
Persistent atlas slot reuse
Incremental texture append adoption in the soak gate
Pipeline cache redesign
Scratch pool introduction
Snapshot ring introduction
Actual DX12 heap telemetry
Vendor-specific VRAM query
Texture payload CPU offload
Model weight RAM tiering
Latency budget increase
Latency budget decrease
Residency estimate replacement
Coverage matrix change
Sequence geometry change
60-commit order change
Candidate output promotion
Physical executor switch
TensorCube texture consumption
```

## 2.3 No silent performance waiver

R2.2 may change resource reclamation timing. It may not redefine PASS.

The following remain unchanged:

```text
p95 maximum                         5,000,000,000 ns
p99 maximum                        10,000,000,000 ns
coverage cells                                      30
healthy commits                                     60
candidate layer dispatches                        1320
device compare dispatches                         1320
compact token drains                                60
fault-generation BufferAtlas dispatches             22
post-disable BufferAtlas dispatches                 176
post-disable commit count                             8
```

A run may pass R2.2 manual-GC verification and still remain `Texture05EligibilityHold` on the original latency predicates.

---

# 3. Authority model

## 3.1 Production authority

```text
Route authority              W3-C1 through W3-C5
Production output authority  W3-C6 HeadwiseFullActive
Active physical executor     BufferAtlasV1
Candidate executor           KvTextureGqa4V1
Candidate output authority   forbidden
```

Manual GC may reclaim resources no longer owned by the completed shadow transaction. It may not reclaim or mutate any resource still required by BufferAtlas production or the active decode state.

## 3.2 GC decision SSOT

The per-boundary SSOT is:

```rust
HeadwiseTextureManualGcReceipt
```

The session-level SSOT is:

```rust
HeadwiseTextureManualGcSummaryReceipt
```

Next-commit admission is authorized only by:

```rust
HeadwiseTexturePostGcAdmissionToken
```

A boolean such as `poll_called = true` without the ordered receipt chain is insufficient.

## 3.3 Metadata-only retention

After a commit is semantically adopted, the gate may retain CPU metadata required for the final artifact:

```text
commit ordinal
generation
route
seq_q
seq_kv
coverage cell key
receipt digest
timing digest
residency estimate
gc receipt digest
```

The gate must not retain GPU handles merely to build later JSON artifacts.

## 3.4 Device and queue lifetime

The shared device and queue remain model/gate scoped:

```text
device  retained across all 69 boundaries
queue   retained across all 69 boundaries
```

R2.2 must not drop and recreate the device or queue as a substitute for resource reclamation.

---

# 4. Manual GC boundary kinds

```rust
#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq)]
pub enum HeadwiseTextureManualGcBoundaryKind {
    HealthyShadowCommit,
    FaultDrillBufferAtlasOnly,
    PostDisableBufferAtlasOnly,
}
```

Required counts:

```text
HealthyShadowCommit          60
FaultDrillBufferAtlasOnly     1
PostDisableBufferAtlasOnly    8
Total                        69
```

Boundary kind must be part of every receipt digest.

---

# 5. Commit owner taxonomy

## 5.1 Owner groups

R2.2 defines the following semantic owner groups:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTextureCommitOwnerDropReceipt {
    pub source_buffer_owner_scope_closed: bool,
    pub reference_output_owner_scope_closed: bool,
    pub snapshot_owner_scope_closed: bool,
    pub candidate_scratch_owner_scope_closed: bool,
    pub comparison_scratch_owner_scope_closed: bool,
    pub compact_token_owner_scope_closed: bool,
    pub timestamp_owner_scope_closed: bool,
    pub ticket_registry_dropped: bool,
    pub residency_registry_dropped: bool,
    pub device_retained: bool,
    pub queue_retained: bool,
    pub owner_drop_sequence: Vec<String>,
    pub receipt_digest: String,
}
```

These fields are semantic evidence backed by lexical ownership and source-level verification. They are not a claim that WGPU exposes a raw reference count for every object.

## 5.2 Healthy shadow owner requirements

A healthy shadow boundary requires:

```text
source buffer owner scope closed              true
reference output owner scope closed           true
snapshot owner scope closed                   true
candidate scratch owner scope closed          true
comparison scratch owner scope closed         true
compact token owner scope closed              true
timestamp owner scope closed                   true
ticket registry dropped                       true
residency registry dropped                    true
device retained                               true
queue retained                                true
```

## 5.3 BufferAtlas-only owner requirements

A fault or post-disable BufferAtlas-only boundary does not construct candidate texture owners. It requires:

```text
source buffer owner scope closed              true
reference output owner scope closed           true
snapshot owner scope closed                   true or not-created
candidate scratch owner scope                 not-created
comparison scratch owner scope                not-created
compact token owner scope                     not-created
timestamp owner scope                         not-created
ticket registry                               not-created
residency registry                            not-created
device retained                               true
queue retained                                true
```

The receipt must distinguish `closed` from `not-created`. It must not forge `dropped = true` for an owner that never existed.

## 5.4 Forbidden retained owners

Before manual GC poll admission, the commit owner audit must reject:

```text
live HeadwiseTextureSessionResidencyRegistry
live HeadwiseTextureLiveShadowTicketRegistry
live captured ticket vector
live HeadwiseKvTextureResidency handle
live candidate output scratch handle
live compare scratch handle
live timestamp query / resolve / staging handle
live per-layer BufferAtlas reference lease
live commit-local Q/K/V lease
```

CPU receipts, digests and primitive geometry values may remain.

---

# 6. Owner-drop-before-poll ordering

## 6.1 Required lexical shape

The healthy soak loop must adopt an inner owner scope equivalent to:

```rust
let commit_evidence = {
    let registry = HeadwiseTextureSessionResidencyRegistry::default();
    let tickets = HeadwiseTextureLiveShadowTicketRegistry::default();

    tickets.configure(/* unchanged policy */)?;

    let (receipt, timing) = timestamp_gpu_envelope(
        &device,
        &queue,
        generation,
        || run_shadow_commit(
            &registry,
            &tickets,
            device.clone(),
            queue.clone(),
            /* unchanged identity and geometry */
        ),
    )?;

    validate_commit_receipt(&receipt)?;
    let metadata = adopt_commit_metadata(receipt, timing, /* ... */)?;

    drop(tickets);
    drop(registry);

    metadata
};

let gc_receipt = manual_gc_after_owner_drop(
    &device,
    HeadwiseTextureManualGcBoundaryKind::HealthyShadowCommit,
    commit_evidence.commit_ordinal,
    commit_evidence.generation,
    commit_evidence.route,
    commit_evidence.seq_q,
    commit_evidence.seq_kv,
    commit_evidence.metadata_digest,
    previous_gc_receipt_digest.as_deref(),
)?;

admit_next_commit_only_after_gc(&gc_receipt)?;
```

Equivalent RAII scope structure is allowed. The invariant is not tied to literal calls if lexical destruction is stronger and statically auditable.

## 6.2 Mandatory order

```text
1. GPU work submitted
2. timestamp / compact readback completed
3. commit semantic receipt validated
4. supervisor adopts CPU-only metadata
5. commit-local GPU owners leave scope
6. ticket registry dropped
7. residency registry dropped
8. manual GC poll requested
9. manual GC poll completed successfully
10. GC receipt sealed
11. next-commit admission token issued
12. next commit begins
```

## 6.3 Forbidden orderings

```text
device.poll before residency registry drop
next commit allocation before previous GC completion
GC receipt sealed before poll returns
poll error ignored with `let _ = ...`
owner-drop flags inferred only from poll success
next admission inferred from loop progression
fault drill entered before generation 60 GC receipt passes
post-disable commit entered before prior GC receipt passes
```

## 6.4 Existing timestamp poll classification

Every timing receipt must preserve:

```text
timestamp_completion_poll_count = 1
manual_gc_poll_count             = 1
```

These are separate categories even though both call `device.poll(PollType::Wait)`.

The timestamp poll remains inside timing readback. The manual-GC poll must occur after the timing helper returns and after commit owners are destroyed.

---

# 7. Manual GC execution

## 7.1 Canonical function

```rust
pub fn execute_headwise_texture_manual_gc(
    device: &backend_wgpu::Device,
    request: &HeadwiseTextureManualGcRequest,
) -> Result<HeadwiseTextureManualGcReceipt>
```

## 7.2 Request

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTextureManualGcRequest {
    pub session_id: String,
    pub session_epoch: u64,
    pub supervisor_generation: u64,
    pub boundary_ordinal: u32,
    pub boundary_kind: HeadwiseTextureManualGcBoundaryKind,
    pub commit_ordinal: Option<u32>,
    pub generation: u64,
    pub route: String,
    pub seq_q: u32,
    pub seq_kv: u32,
    pub commit_evidence_digest: String,
    pub owner_drop_receipt_digest: String,
    pub previous_gc_receipt_digest: Option<String>,
    pub request_digest: String,
}
```

## 7.3 Poll call

The implementation must call exactly one patch-owned manual GC poll per boundary:

```rust
let started = std::time::Instant::now();
let status = device
    .poll(backend_wgpu::PollType::Wait)
    .map_err(|error| anyhow!(
        "Texture05ManualGcPollFailed:boundary={}:generation={}:error={error:?}",
        request.boundary_ordinal,
        request.generation,
    ))?;
let duration_ns = started.elapsed().as_nanos().min(u64::MAX as u128) as u64;
```

If the exact WGPU return type differs, the code may adapt the status serialization. It may not discard the result.

Forbidden:

```rust
let _ = device.poll(backend_wgpu::PollType::Wait);
```

## 7.4 Poll mode

Canonical mode:

```text
backend_wgpu::PollType::Wait
```

Nonblocking polling does not satisfy R2.2 because the next commit must not be admitted until deferred destruction work has been drained through the completed boundary.

## 7.5 Manual GC failure

Any poll failure produces a typed fail-closed error:

```text
Texture05ManualGcPollFailed
```

Required consequences:

```text
current boundary GC PASS receipt     forbidden
next admission token                forbidden
next commit allocation              forbidden
canonical promotion artifact        forbidden
candidate readiness promotion       forbidden
BufferAtlas authority mutation      forbidden
```

The gate may write a diagnostic failure artifact before returning non-zero.

---

# 8. Per-boundary GC receipt

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTextureManualGcReceipt {
    pub schema_version: u32,
    pub receipt_kind: String,

    pub session_id: String,
    pub session_epoch: u64,
    pub supervisor_generation: u64,

    pub boundary_ordinal: u32,
    pub boundary_kind: HeadwiseTextureManualGcBoundaryKind,
    pub commit_ordinal: Option<u32>,
    pub generation: u64,
    pub route: String,
    pub seq_q: u32,
    pub seq_kv: u32,

    pub commit_evidence_digest: String,
    pub owner_drop_receipt_digest: String,
    pub previous_gc_receipt_digest: Option<String>,

    pub owner_drop_completed_before_poll: bool,
    pub manual_gc_poll_requested: bool,
    pub manual_gc_poll_completed: bool,
    pub manual_gc_poll_mode: String,
    pub manual_gc_poll_status: String,
    pub manual_gc_duration_ns: u64,

    pub next_commit_admission_allowed: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Canonical constants:

```text
schema_version             1
receipt_kind               headwise-texture-manual-gc
manual_gc_poll_mode        wait
```

PASS formula:

```text
owner_drop_completed_before_poll
&& manual_gc_poll_requested
&& manual_gc_poll_completed
&& manual_gc_poll_mode == wait
&& manual_gc_poll_status indicates success
&& receipt chain identity is valid
```

`manual_gc_duration_ns == 0` is allowed only when the platform clock resolution genuinely returns zero. It must not be hardcoded.

---

# 9. GC duration accounting

## 9.1 Separate metric plane

Manual GC wall-clock duration is not the same metric as the GPU timestamp envelope.

```text
total_shadow_gpu_ns
  GPU timestamp delta between query 0 and query 1

manual_gc_duration_ns
  host monotonic wall-clock duration of post-drop poll(Wait)
```

R2.2 must not silently add manual GC time into `total_shadow_gpu_ns` or overwrite the R2.1 latency observations.

## 9.2 Required summary statistics

The final GC summary must publish nearest-rank:

```text
gc p50
GC p95
GC p99
GC max
GC total
```

It must also localize the worst five GC boundaries by:

```text
boundary ordinal
boundary kind
commit ordinal if present
generation
route
seq_q
seq_kv
manual_gc_duration_ns
receipt digest
```

## 9.3 No initial promotion threshold

R2.2 rev.1 records GC duration but does not invent a new device-independent GC latency budget.

The following are forbidden in rev.1:

```text
silently failing promotion because GC p95 exceeds an undocumented limit
silently passing GC because duration was omitted
folding GC duration into the old p95 / p99 threshold
```

A later calibrated patch may introduce a separately digested device profile.

---

# 10. Post-GC next-commit admission

## 10.1 Admission token

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTexturePostGcAdmissionToken {
    pub session_id: String,
    pub session_epoch: u64,
    pub previous_boundary_ordinal: u32,
    pub previous_generation: u64,
    pub previous_gc_receipt_digest: String,
    pub admitted_boundary_ordinal: u32,
    pub admitted_generation: u64,
    pub admission_reason: String,
    pub pass: bool,
    pub token_digest: String,
}
```

## 10.2 Genesis admission

The first soak commit is admitted by a distinct genesis token:

```text
previous boundary       none
previous generation     none
reason                  session-genesis
```

Genesis admission does not count as post-GC admission.

## 10.3 Chained admissions

Every boundary after the first requires the immediately preceding GC receipt.

Expected counts:

```text
total boundaries                     69
genesis admissions                     1
post-GC chained admissions            68
```

The chain crosses phase boundaries:

```text
healthy commit 60 GC
  -> fault drill admission

fault drill GC
  -> post-disable commit 1 admission

post-disable commit N GC
  -> post-disable commit N+1 admission
```

## 10.4 Admission failure

The next boundary is not admitted when:

```text
previous GC receipt missing
previous GC receipt pass false
receipt digest mismatch
boundary ordinal is not previous + 1
generation lineage mismatch
session or epoch mismatch
owner-drop-before-poll false
manual poll incomplete
```

---

# 11. Healthy soak integration

## 11.1 Supervisor adoption boundary

The supervisor may adopt only CPU metadata before owner destruction:

```text
coverage cell
healthy commit counters
candidate dispatch count
device compare count
compact drain count
timing receipt value
ranked observation value
residency estimate value
GPU-free receipt digest strings
```

The supervisor must not receive a GPU buffer, texture, view, bind group, pipeline or raw lease through the new GC path.

## 11.2 Generation progression

Generation increments only after the current GC receipt passes:

```rust
let gc_receipt = execute_headwise_texture_manual_gc(/* ... */)?;
ensure!(gc_receipt.pass, "Texture05ManualGcReceiptFailed");
previous_gc_receipt_digest = Some(gc_receipt.receipt_digest.clone());
generation += 1;
```

Forbidden:

```rust
generation += 1;
execute_headwise_texture_manual_gc(/* ... */)?;
```

## 11.3 Coverage non-regression

Manual GC boundaries do not count as coverage commits and do not mutate coverage cell evidence.

Required final healthy evidence remains:

```text
30 / 30 cells
2 healthy commits per cell
60 healthy commits
1320 candidate dispatches
1320 compare dispatches
60 compact drains
```

---

# 12. Fault-drill cleanup boundary

## 12.1 Fault generation

The intentional fault generation executes BufferAtlas-only work under the existing authority contract.

Required order:

```text
healthy soak commit 60 manual GC PASS
  -> fault-generation admission token
  -> run_bufferatlas_only_commit
  -> return CPU dispatch count
  -> function-local Q/K/V and references dropped
  -> fault manual GC poll(Wait)
  -> fault GC receipt PASS
  -> quarantine_and_disable metadata transition
```

The quarantine transition may occur before or after the fault GC receipt only if it owns no GPU handle and the source audit proves the next phase remains blocked until GC PASS. Canonical order places GC before post-disable admission.

## 12.2 Fault receipt requirements

```text
boundary kind                         FaultDrillBufferAtlasOnly
candidate owner groups                not-created
BufferAtlas dispatch count            22
manual GC poll count                   1
next post-disable admission allowed   true only after PASS
```

## 12.3 Post-disable commits

Each of the eight post-disable commits requires an independent manual GC boundary.

```text
post-disable commit 1 -> GC 1
post-disable commit 2 -> GC 2
...
post-disable commit 8 -> GC 8
```

Batching one GC poll after all eight commits is forbidden.

## 12.4 Production continuity

Manual GC must not alter:

```text
fault-generation BufferAtlas output committed
post-disable BufferAtlas output committed 8 times
candidate dispatch admitted 0 after disable
production wait on candidate 0
production output suppression 0
production output replacement 0
HeadwiseFullActive pointer unchanged
```

---

# 13. Session-level GC summary

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTextureManualGcSummaryReceipt {
    pub schema_version: u32,
    pub receipt_kind: String,

    pub session_id: String,
    pub session_epoch: u64,
    pub supervisor_generation: u64,

    pub expected_boundary_count: u32,
    pub observed_boundary_count: u32,
    pub healthy_boundary_count: u32,
    pub fault_boundary_count: u32,
    pub post_disable_boundary_count: u32,

    pub genesis_admission_count: u32,
    pub post_gc_admission_count: u32,

    pub owner_drop_before_poll_pass_count: u32,
    pub manual_gc_poll_requested_count: u32,
    pub manual_gc_poll_completed_count: u32,
    pub manual_gc_failure_count: u32,

    pub gc_duration_p50_ns: u64,
    pub gc_duration_p95_ns: u64,
    pub gc_duration_p99_ns: u64,
    pub gc_duration_max_ns: u64,
    pub gc_duration_total_ns: u64,

    pub worst_gc_boundaries: Vec<HeadwiseTextureManualGcReceipt>,
    pub ordered_gc_receipt_digests: Vec<String>,
    pub gc_receipt_chain_digest: String,

    pub all_boundaries_pass: bool,
    pub next_commit_admission_chain_pass: bool,
    pub production_authority_unchanged: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

PASS requirements:

```text
expected boundary count                    69
observed boundary count                    69
healthy boundary count                     60
fault boundary count                        1
post-disable boundary count                 8
genesis admission count                     1
post-GC admission count                    68
owner-drop-before-poll PASS count          69
manual GC poll requested count             69
manual GC poll completed count             69
manual GC failure count                     0
all boundaries pass                      true
next admission chain pass                true
production authority unchanged           true
```

---

# 14. Receipt chain integrity

## 14.1 Digest input

Each GC receipt digest binds at minimum:

```text
schema and receipt kind
session and epoch
supervisor generation
boundary ordinal and kind
commit ordinal
generation
route and geometry
commit evidence digest
owner-drop receipt digest
previous GC receipt digest
poll mode and status
GC duration
PASS state
```

## 14.2 Chain construction

```text
GC receipt 1.previous = GENESIS
GC receipt 2.previous = digest(GC receipt 1)
...
GC receipt 69.previous = digest(GC receipt 68)
```

The session chain digest is SHA-256 of the exact ordered receipt digests joined by `\n` without a trailing newline.

## 14.3 Chain failures

```text
missing receipt
duplicate boundary ordinal
out-of-order boundary
duplicate generation in the same phase
previous digest mismatch
session mismatch
epoch mismatch
boundary-kind count mismatch
```

Any chain failure blocks R2.2 PASS.

---

# 15. Artifact contract

## 15.1 Rust-authored artifacts

The Rust gate writes:

```text
workspace/runtime/attention/headwise/texture/05/r2_2/
  manual_gc_owner_drop_receipts.json
  manual_gc_boundary_receipts.json
  manual_gc_admission_tokens.json
  manual_gc_duration_summary.json
  manual_gc_chain_receipt.json
  manual_gc_failure_receipt.json        only on failure

workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r2_2_runtime_artifact.json
  ash_attn_headwise_texture_05_r2_2_local_manifest.json
```

No external script authors these files.

## 15.2 Runtime artifact

Required top-level fields:

```text
schema
patchId
buildRevision
pass
passToken
parentBuildRevision
productionAuthority
candidateAuthority
manualGcPolicy
manualGcSummary
receiptChainDigest
artifactHashes
sourceHashes
```

## 15.3 Local manifest

The local manifest binds:

```text
runtime artifact path and SHA-256
all R2.2 child artifact paths and SHA-256
binary name
Cargo feature
CLI response file path and SHA-256
source file paths and SHA-256
parent artifact digests
build revision
pass token
```

## 15.4 Atomic write

Every JSON artifact must use:

```text
serialize canonical value
write temporary sibling
flush
rename to final path
read final bytes
recompute SHA-256
verify expected digest
```

A partially written GC chain may not be treated as PASS.

## 15.5 Parent promotion artifact boundary

On R2.2 verification PASS but original Texture-05 eligibility HOLD:

```text
R2.2 runtime artifact                         written
R2.2 local manifest                           written
Texture-05 diagnostic HOLD artifacts          preserved
canonical Texture-05 promotion artifact       not written
candidate readiness                           PerCommitManualGcBound
SustainedShadowSoakBound                      forbidden
```

---

# 16. Runtime implementation ownership

## 16.1 New backend module

```text
crates/burn_webgpu_backend/src/
  headwise_texture_manual_gc.rs
```

Responsibilities:

```text
manual GC request validation
post-drop PollType::Wait execution
poll result handling
GC duration measurement
per-boundary receipt sealing
```

## 16.2 New model-core module

```text
crates/model_core/src/
  headwise_texture_manual_gc_authority.rs
```

Responsibilities:

```text
boundary kind
owner-drop receipt schema
post-GC admission token
GC receipt chain
GC summary
canonical digest construction
```

## 16.3 Gate integration

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_gate.rs
  ash_attn_headwise_texture_05_r2_2_gate.rs
```

`ash_attn_headwise_texture_05_gate.rs` performs the physical 69-boundary execution.

`ash_attn_headwise_texture_05_r2_2_gate.rs` verifies:

```text
source ordering
owner scope closure
receipt schemas
negative controls
chain integrity
artifact and manifest generation
parent authority non-regression
```

## 16.4 CLI registry

```text
crates/orchestrator_local/src/
  headwise_texture_05_r2_2_cli_registry.rs

specs/cli/
  ash_attn_headwise_texture_05_r2_2.args
```

Suggested required keys:

```text
--repo-root
--expected-patch-id
--expected-build-revision
--parent-texture05-runtime-source
--parent-r2-1-runtime-artifact
--parent-r2-1-local-manifest
--expected-manual-gc-boundary-count
--expected-healthy-gc-boundary-count
--expected-fault-gc-boundary-count
--expected-post-disable-gc-boundary-count
--expected-genesis-admission-count
--expected-post-gc-admission-count
--require-owner-drop-before-poll
--require-poll-wait
--require-poll-result-validation
--require-fault-drill-gc
--require-post-disable-per-commit-gc
--require-gc-duration-receipt
--forbid-gc-duration-in-shadow-latency
--forbid-next-admission-before-gc
--forbid-poll-result-discard
--forbid-production-authority-mutation
--runtime-artifact
--local-manifest
```

---

# 17. State machine

```text
SessionGenesis
  -> CommitAdmitted
  -> CommitExecuting
  -> EvidenceCompleted
  -> MetadataAdopted
  -> OwnersDropping
  -> OwnersDropped
  -> ManualGcPolling
  -> ManualGcCompleted
  -> GcReceiptSealed
  -> NextCommitAdmissible
```

Failure states:

```text
OwnerDropEvidenceInvalid
ManualGcPollFailed
GcReceiptIntegrityFailed
AdmissionChainBroken
AuthorityMutationDetected
```

Forbidden transitions:

```text
EvidenceCompleted -> ManualGcPolling
  when owners are still live

OwnersDropped -> NextCommitAdmissible
  without ManualGcCompleted

ManualGcPolling -> GcReceiptSealed
  when poll returned error

GcReceiptSealed -> canonical promotion
  when original Texture-05 eligibility remains HOLD
```

---

# 18. Positive cases

Minimum positive controls:

```text
01  Healthy boundary owner scope closes before poll
02  Ticket registry is dropped before poll
03  Residency registry is dropped before poll
04  Device remains alive across GC
05  Queue remains alive across GC
06  Poll mode is Wait
07  Poll result is checked
08  GC duration uses monotonic clock
09  GC duration is retained in receipt
10  Receipt binds commit ordinal
11  Receipt binds generation
12  Receipt binds route and geometry
13  Receipt binds owner-drop digest
14  Receipt binds previous GC digest
15  First boundary accepts genesis
16  Second boundary requires first receipt
17  Boundary 60 admits fault drill
18  Fault drill receives dedicated GC
19  Fault GC admits post-disable commit 1
20  Every post-disable commit receives GC
21  Final observed boundary count is 69
22  Chained admission count is 68
23  Manual poll completed count is 69
24  Manual poll failure count is zero
25  GC summary ranks worst five boundaries
26  Shadow GPU latency remains unmodified
27  Coverage counters remain unchanged
28  Candidate output commit remains zero
29  BufferAtlas authority remains unchanged
30  Rust writes runtime artifact and manifest
31  Artifact hashes verify after readback
32  Original latency HOLD remains visible when still false
```

---

# 19. Negative controls

Minimum negative controls:

```text
01  Poll before registry drop
02  Poll before ticket drop
03  Poll result discarded with `let _ =`
04  Nonblocking poll substituted for Wait
05  Next generation incremented before GC PASS
06  Next allocation begins before GC PASS
07  Missing healthy boundary receipt
08  Missing fault boundary receipt
09  Missing post-disable boundary receipt
10  One GC batched after all post-disable commits
11  Duplicate boundary ordinal
12  Duplicate GC receipt digest
13  Previous digest mismatch
14  Session mismatch
15  Epoch mismatch
16  Route mismatch
17  Generation mismatch
18  Owner-drop receipt missing
19  Owner-drop-before-poll false
20  Manual poll requested false
21  Manual poll completed false
22  Manual poll status error
23  GC duration omitted
24  GC duration hardcoded
25  GC duration folded into shadow p95
26  Original latency threshold modified
27  Coverage order modified
28  Candidate output authority mutated
29  BufferAtlas executor pointer mutated
30  Device recreated per commit
31  Queue recreated per commit
32  CPU texture payload readback added
33  Canonical promotion artifact written on HOLD
34  R2.2 PASS mislabeled SustainedShadowSoakBound
```

---

# 20. Source and structural audits

The R2.2 verification gate must inspect the active Texture-05 source and prove at minimum:

```text
69-boundary manual GC helper is physically called through all phases
`PollType::Wait` occurs in the manual-GC helper
manual poll result is not discarded
healthy owner scope ends before helper call
registry and ticket owners do not cross helper call
fault commit return precedes helper call
post-disable loop invokes helper once per iteration
generation increment follows GC PASS
next phase admission consumes previous GC digest
no latency budget constant changed
no coverage geometry changed
no candidate authority promotion added
```

String matching alone is insufficient for final authority if it can be trivially fooled by comments. The gate should combine:

```text
compiled behavioral tests
receipt count and chain checks
source AST or constrained source audit
physical runtime artifact verification
```

---

# 21. Completion gate

R2.2 PASS requires:

```text
positive controls                         >= 32
negative controls                         >= 34
manual GC boundaries                        69
healthy manual GC boundaries                60
fault manual GC boundaries                   1
post-disable manual GC boundaries             8
genesis admissions                            1
post-GC chained admissions                   68
owner-drop-before-poll PASS                  69
manual poll requested                        69
manual poll completed                        69
manual poll failures                          0
GC receipt chain integrity                  PASS
artifact atomic write                       PASS
artifact readback hash verification         PASS
production authority unchanged              PASS
candidate output commit count                  0
payload readback added                          0
host texture offload added                      0
```

Patch-local PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R2_2_PER_COMMIT_MANUAL_GARBAGE_COLLECTION_OWNER_DROP_BEFORE_POLL_ORDERING_DEFERRED_DESTRUCTION_DRAIN_FAULT_DRILL_CLEANUP_BOUNDARY_GC_DURATION_RECEIPT_POST_GC_NEXT_COMMIT_ADMISSION_SEALED
```

After PASS:

```text
KvTextureGqa4V1
  LiveShadowParityBound
  EligibilityFailureLocalized
  PerCommitManualGcBound
  ProductionOutputCommitForbidden

Texture-05 sustained promotion
  remains controlled by the original eligibility predicates
```

---

# 22. Direct execution

R2.2 verification gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r2_2_gate -- "@specs/cli/ash_attn_headwise_texture_05_r2_2.args"
```

Physical Texture-05 rerun after R2.2 verification:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected physical behavior:

```text
Each of 60 healthy commits prints or records one post-drop manual GC receipt.
The fault drill records one dedicated manual GC receipt.
Each of eight post-disable commits records one dedicated manual GC receipt.
No next boundary is admitted before the previous receipt passes.
The final eligibility output still reports Promote or the exact remaining HOLD predicates.
```

---

# 23. Packaging contract for the later bake

The code-baked ZIP must include:

```text
R2.2 Rust implementation
R2.2 verification gate
R2.2 CLI registry
R2.2 response file
Cargo bin registration
```

The code-baked ZIP must exclude:

```text
this Markdown specification
runtime artifact JSON
local manifest JSON
child runtime evidence JSON
target directory
.git directory
```

Runtime artifact and local manifest are generated by Rust when the user executes the gate.

An overlay ZIP must contain only files changed by R2.2, rooted at the repository root.

---

# 24. Final seal

R2.2 closes one precise gap:

```text
Rust owner leaves scope someday
```

is replaced with:

```text
commit evidence completed
  -> GPU owner groups demonstrably destroyed
  -> explicit Wait poll succeeds
  -> deferred destruction boundary receipt sealed
  -> only then may the next commit allocate
```

The patch does not claim that manual GC alone will reduce the observed p95 and p99 below budget. It proves that each commit begins from a completed post-drop reclamation boundary rather than inheriting unbounded deferred destruction from the previous commit.

If latency remains above budget after this closure, the remaining cost belongs to the workload itself or to allocation/population design and must be addressed by the persistent-runtime and slot-reuse phases without weakening the original gate.
