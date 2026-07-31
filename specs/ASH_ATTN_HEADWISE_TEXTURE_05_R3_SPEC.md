# ASH-ATTN-HEADWISE-TEXTURE-05-R3

## Session-Scoped Persistent Texture Residency /
## One-Time Full Population /
## Incremental KV Texel Append /
## Current·Previous Generation View /
## Immutable Page Reuse /
## Touched-Page Copy-on-Write /
## No Per-Commit Texture Reconstruction /
## Persistent Pipeline Manager Adoption /
## Per-Commit Manual GC for Transients Only /
## Full-Population Count Receipt /
## Append-Byte Accounting /
## Steady-State Latency Separation Seal

> Status: **SPEC RELEASE rev.1**  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-05-R3`  
> Build revision: `HEADWISE-TEXTURE-05-R3-session-persistent-texture-residency-v1`  
> Parent implementation: `ASH-ATTN-HEADWISE-TEXTURE-05-R2.3-R1`  
> Parent pipeline state: `FactoryManagerDeviceGenerationWakeBound`  
> Parent manual-GC state: `PerCommitManualGcBound`  
> Parent physical soak state: `HOLD - latency_p95_within_budget=false, latency_p99_within_budget=false`  
> Active production executor: `BufferAtlasV1` unchanged  
> Candidate executor: `KvTextureGqa4V1` unchanged  
> Production output authority: `HeadwiseFullActive` unchanged  
> Candidate output authority: shadow evidence only  
> Patch-local readiness after PASS: `SessionPersistentTextureResidencyBound`  
> `SustainedShadowSoakBound`: **forbidden until the original Texture-05 eligibility predicates return Promote**

---

# 0. Source-grounded diagnosis

## 0.1 Observed post-R2.3 physical result

The physical Texture-05 gate completed all 60 healthy shadow boundaries and reported manual-GC completion with an empty queue:

```text
boundary 56  generation 63  GC 11,500 ns  QueueEmpty
boundary 57  generation 64  GC  9,900 ns  QueueEmpty
boundary 58  generation 65  GC  9,200 ns  QueueEmpty
boundary 59  generation 66  GC 19,400 ns  QueueEmpty
boundary 60  generation 67  GC 11,300 ns  QueueEmpty
```

Final eligibility:

```text
disposition       hold
false predicates  latency_p95_within_budget
                  latency_p99_within_budget

p50Ns             3,529,053,184
p95Ns            15,980,678,144
p99Ns            16,255,533,056
maxNs            16,255,533,056
worstGeneration  19
worstRoute       incremental_decode
worstSeqQ        1
worstSeqKv       1792
```

This evidence proves:

```text
Confirmed
  Manual GC executes.
  The queue is empty at the disclosed GC boundaries.
  Manual-GC wait is measured in microseconds, not seconds.
  R2.3 pipeline-manager adoption does not materially remove the 16-second tail.
  The worst disclosed geometry remains Q1 / KV1792.

Not proved by this log alone
  Exact driver heap residency.
  Exact texture population percentage of the 16-second envelope.
  Vendor-level memory allocator behavior.
```

The active source closes the remaining structural localization:

```text
HeadwiseTextureSessionResidencyRegistry::default()
  is constructed inside every healthy soak iteration.

run_shadow_commit()
  creates Q/K/V source leases,
  performs 22 BufferAtlas reference dispatches,
  performs 22 full persistent K/V texture populations,
  publishes one freshly reconstructed generation,
  dispatches the shadow candidate,
  then allows the entire residency registry to be dropped.
```

Therefore the current gate is not a persistent-residency soak. It is a repeated cold residency reconstruction test.

## 0.2 Current source paths establishing the gap

```text
crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_gate.rs

crates/model_core/src/
  headwise_texture_persistent_kv_binding.rs
  headwise_texture_incremental_append.rs

crates/burn_webgpu_backend/src/
  headwise_kv_texture_residency.rs
  headwise_kv_texture_persistent_population.rs
  headwise_kv_texture_generation_view.rs
  headwise_kv_texture_incremental_append.rs
```

The required append machinery already exists:

```text
HeadwiseTextureAppendSpan
HeadwiseTexturePhysicalPageAllocator
HeadwiseTextureGenerationView
HeadwiseTexturePublishedGenerationState
HeadwiseTextureSessionResidencyRegistry::append_committed_generation
HeadwiseKvTextureResidency::append_persistent_cache_span
```

R3 does not invent a second append authority. It adopts the existing Texture-03 generation and page authority into the sustained Texture-05 gate.

---

# 1. Goal

R3 changes Texture-05 from:

```text
60 shadow commits
  -> 60 residency registries
  -> 60 full K/V texture reconstructions
  -> 60 generation-local texture object graphs
```

into:

```text
one decode session
  -> one persistent residency registry
  -> one full population at the first KV bucket
  -> five monotonic append transitions
  -> six published texture generations
  -> ten shadow commits per texture generation
  -> sixty total healthy shadow commits
```

Canonical session flow:

```text
Device and queue bootstrap
  -> R2.3 pipeline manager Ready(Gdevice)
  -> persistent texture registry creation
  -> initial generation source adoption at KV64
  -> one-time full population of 22 layer texture pairs
  -> publish texture generation T0
  -> run ten shadow commits against T0
  -> append KV64 -> KV192 and publish T1
  -> run ten shadow commits against T1
  -> append KV192 -> KV384 and publish T2
  -> run ten shadow commits against T2
  -> append KV384 -> KV768 and publish T3
  -> run ten shadow commits against T3
  -> append KV768 -> KV1280 and publish T4
  -> run ten shadow commits against T4
  -> append KV1280 -> KV1792 and publish T5
  -> run ten shadow commits against T5
  -> fault drill
  -> candidate disable
  -> explicit persistent-session retirement
  -> eight BufferAtlas-only continuity commits
```

R3 must preserve all 30 coverage cells and two healthy observations per cell.

---

# 2. Non-negotiable authority boundary

## 2.1 Authoritative production state

```text
DecodeState persistent K/V
BufferAtlasV1 production dispatch
HeadwiseFullActive output authority
W3 route authority
production token history
production generation lineage
```

## 2.2 Derived candidate state

```text
persistent K/V texture residency
physical page allocator
current and previous texture generation views
append transaction receipts
shadow candidate output
compact parity token
R3 timing and byte-accounting receipts
```

## 2.3 Forbidden authority inversion

```text
texture generation -> production K/V mutation
texture page state -> token-history mutation
append failure -> production K/V rollback
shadow failure -> BufferAtlas output suppression
texture candidate -> output authority
coverage-plan reorder -> route authority mutation
persistent residency -> TensorCube consumer admission
```

The candidate remains non-authoritative even after R3 PASS.

---

# 3. Why the 60-commit order must change

## 3.1 Existing order is not append-compatible

The current deterministic order revisits shorter `seq_kv` values after longer values. A single session cannot validly perform:

```text
KV1792 -> KV64
```

as an incremental append.

Texture-03 correctly forbids:

```text
committed_token_count <= prefix_token_count
empty append span
non-monotonic generation publication
silent full repopulation fallback
```

R3 must not fake shrinkage or reset the texture generation inside the same session.

## 3.2 Canonical R3 monotonic order

`seq_kv` representatives remain unchanged:

```text
64
192
384
768
1280
1792
```

For each `seq_kv`, run the following five route/query shapes twice:

```text
IncrementalDecode  Q1
ChunkedDecode      Q2
ChunkedDecode      Q6
ChunkedDecode      Q12
ChunkedDecode      Q24
```

Canonical per-bucket order:

```text
Q1, Q1,
Q2, Q2,
Q6, Q6,
Q12, Q12,
Q24, Q24
```

Canonical totals:

```text
6 KV buckets
× 5 route/query shapes
× 2 healthy commits
= 60 healthy shadow commits

6 × 5 = 30 coverage cells
2 healthy commits per cell
```

## 3.3 Generation and invocation identities are separate

R3 introduces an explicit distinction:

```text
texture_committed_generation
  changes only when seq_kv increases
  total distinct values = 6

shadow_commit_ordinal
  changes for every healthy shadow invocation
  total distinct values = 60
```

Ten shadow commits at the same `seq_kv` reuse the same texture generation.

The following must remain unique per shadow commit:

```text
attention invocation digest
production dispatch receipt digest
production nonce
guard slot lineage
capture submission serial
shadow commit ordinal
```

The following remains identical across the ten commits in one bucket:

```text
texture committed generation
texture generation-view digest
texture object identity digest
persistent physical page allocator identity
K/V committed token count
```

Reusing a texture generation must not reuse an invocation identity.

---

# 4. Canonical generation plan

Let the first texture generation be `T0`.

```text
T0  KV64    full population
T1  KV192   append 128 tokens
T2  KV384   append 192 tokens
T3  KV768   append 384 tokens
T4  KV1280  append 512 tokens
T5  KV1792  append 512 tokens
```

Required counts:

```text
published texture generations            6
full-population transactions             1
full-populated layers                    22
append transactions                       5
append layer transactions                110
shadow commits per texture generation     10
healthy shadow commits                    60
```

The CLI must no longer require a 60-value texture-generation range.

Suggested keys:

```text
--first-texture-generation
--expected-texture-generation-count=6
--expected-shadow-commit-count=60
```

`last_texture_generation` is derived as:

```text
first + 5
```

---

# 5. Session-scoped persistent runtime

## 5.1 New runtime owner

```rust
pub struct HeadwiseTexture05PersistentSessionRuntime {
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub session_epoch: u64,

    pub device: Arc<backend_wgpu::Device>,
    pub queue: Arc<backend_wgpu::Queue>,
    pub pipeline_manager: Arc<HeadwiseTexturePipelineManager>,

    pub residency_registry: Arc<HeadwiseTextureSessionResidencyRegistry>,
    pub current_texture_generation: u64,
    pub current_token_count: usize,

    pub persistent_identity_digest: String,
    pub state: HeadwiseTexture05PersistentSessionState,
}
```

## 5.2 Runtime state

```rust
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub enum HeadwiseTexture05PersistentSessionState {
    Cold,
    PipelineReady,
    BootstrapPopulationInProgress,
    Resident {
        texture_generation: u64,
        committed_token_count: usize,
    },
    AppendInProgress {
        prefix_generation: u64,
        target_generation: u64,
    },
    Quarantined,
    Retiring,
    Retired,
}
```

## 5.3 Ownership lifetime

```text
Device lifetime
  device
  queue
  R3 pipeline manager

Texture-05 session lifetime
  persistent residency registry
  22 K/V texture pairs
  physical page allocators
  current and previous generation metadata

Texture-generation lifetime
  exact source K/V lease set used by the gate harness
  generation source receipt

Shadow-commit lifetime
  Q source lease
  reference outputs
  Q snapshots
  reference snapshots
  candidate scratch
  comparison scratch
  compact token resources
  timestamp resources
  ticket registry
  transient bind groups
```

The per-commit manual GC may destroy only shadow-commit owners.

---

# 6. Persistent texture physical layout

Canonical geometry:

```text
batch count          1
K/V heads            4
head dimension      64
page tokens        128
dimension groups    16
max seq_kv        1792
max logical pages   14
retained views       current + previous
```

## 6.1 Physical capacity

R3 allocates each layer residency at bootstrap for the full session ceiling.

Canonical physical-page capacity:

```text
max logical pages                    14
current/previous COW retention slack  2
physical page capacity               16
```

This capacity is fixed at bootstrap. No later append may recreate or resize the texture.

Per layer:

```text
K texture  rgba32float  16 × 128 × (16 pages × 4 batch-head layers)
V texture  rgba32float  16 × 128 × (16 pages × 4 batch-head layers)
```

Required object cardinality:

```text
layer residency records       22
persistent K textures         22
persistent V textures         22
persistent K/V texture pairs  22
texture recreation after bootstrap 0
```

## 6.2 No per-generation texture object

Generation identity is represented by views and page mappings, not by a new texture allocation.

```text
One physical K/V texture pair per layer
  -> many immutable generation views
  -> current and previous views retained
```

Forbidden:

```text
new K texture per generation
new V texture per generation
new texture view graph per shadow commit
registry recreation per shadow commit
texture capacity growth during append
```

---

# 7. One-time full population

## 7.1 Bootstrap generation

The session begins at KV64.

```text
committed token count   64
logical page count       1
full population layers  22
texture generation      T0
```

The runtime performs exactly one session-level full-population transaction.

## 7.2 Bootstrap order

```text
pipeline manager Ready
  -> persistent registry created
  -> 22 layer residencies created at capacity 16
  -> exact T0 source leases adopted
  -> 22 full population submissions
  -> all pages sealed
  -> generation T0 published
  -> bootstrap receipt sealed
  -> first shadow commit admitted
```

## 7.3 Full-population count receipt

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTexture05FullPopulationCountReceipt {
    pub schema_version: u32,
    pub receipt_kind: String,

    pub session_id: String,
    pub session_epoch: u64,
    pub bootstrap_texture_generation: u64,
    pub bootstrap_token_count: usize,

    pub expected_session_full_population_count: u32,
    pub observed_session_full_population_count: u32,
    pub expected_layer_population_count: u32,
    pub observed_layer_population_count: u32,

    pub post_bootstrap_full_population_count: u32,
    pub per_shadow_commit_full_population_count: u32,
    pub silent_full_repopulation_fallback_count: u32,

    pub texture_pair_creation_count: u32,
    pub registry_creation_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

PASS values:

```text
session full population count           1
layer full population count            22
post-bootstrap full population count    0
per-shadow-commit full population count 0
silent fallback count                   0
texture-pair creation count            22
registry creation count                 1
```

---

# 8. Incremental append adoption

## 8.1 Existing authority reused

R3 must use:

```text
HeadwiseTextureSessionResidencyRegistry::append_committed_generation
HeadwiseTextureAppendTrigger
HeadwiseTextureAppendSpan
HeadwiseTexturePhysicalPageAllocator
build_touched_page_plans
HeadwiseKvTextureResidency::append_persistent_cache_span
```

A parallel R3-only page model is forbidden.

## 8.2 Append transitions

```text
64   -> 192   delta 128   touched logical pages 2
192  -> 384   delta 192   touched logical pages 2
384  -> 768   delta 384   touched logical pages 3
768  -> 1280  delta 512   touched logical pages 4
1280 -> 1792  delta 512   touched logical pages 4
```

Per layer totals:

```text
append tokens          1728
touched pages            15
COW pages                  2
new logical pages         13
```

All-layer totals:

```text
append layer transactions 110
touched-page plans         330
COW page plans              44
new-page plans             286
```

Because K and V are copied independently for every COW page:

```text
expected COW texture copy operations
  44 COW page plans × 2 textures
  = 88 copy operations
```

## 8.3 Append publication order

```text
new production K/V generation committed
  -> exact append trigger constructed
  -> base current generation verified
  -> touched-page plans allocated
  -> existing partial page copied on write when required
  -> append shader writes only append token span
  -> touched pages sealed
  -> all 22 layer views staged
  -> generation parity verified
  -> new generation published as current
  -> old current retained as previous
  -> old previous released
  -> unreferenced physical pages retired
```

## 8.4 Silent full population is forbidden

On append failure:

```text
previous current generation remains available
candidate append transaction aborts
BufferAtlas production remains committed
candidate enters explicit lag/quarantine state
```

Forbidden fallback:

```text
append fails
  -> repopulate entire prefix
  -> continue silently
```

---

# 9. Current and previous generation views

## 9.1 Retention state

```rust
pub struct HeadwiseTexturePublishedGenerationState {
    pub current: HeadwiseTextureGenerationView,
    pub previous: Option<HeadwiseTextureGenerationView>,
    pub candidate_readiness: HeadwiseTextureCandidateSynchronizationState,
    pub last_append_receipt_digest: Option<String>,
    pub last_failure_receipt: Option<HeadwiseTextureAppendFailureReceipt>,
}
```

R3 preserves this authority.

## 9.2 Required retention

After bootstrap:

```text
current   T0
previous  none
```

After each successful append:

```text
current   Tn
previous  Tn-1
older     released and retired when refcount reaches zero
```

## 9.3 View identity and physical identity

A new generation view may change:

```text
committed generation
committed token count
logical-to-physical page map
touched-page content digests
view digest
```

It must not change:

```text
underlying K texture object identity
underlying V texture object identity
texture format
texture dimensions
physical capacity
device lineage
pipeline-manager device generation
```

## 9.4 Refcount gate

Before retirement:

```text
old view released
page generation_ref_count decremented
only refcount-zero pages returned to free set
current and previous referenced pages remain sealed
```

Refcount underflow, page alias mismatch or retirement of a referenced page fails closed.

---

# 10. Immutable page reuse and COW

## 10.1 Untouched pages

Untouched pages are shared by physical page reference.

Required counters:

```text
untouched-page texture copy count 0
untouched-page rewrite count      0
untouched-page allocation count   0
```

Only refcount adoption is allowed.

## 10.2 Touched existing partial page

When append begins inside an existing page:

```text
base page remains sealed
new physical page allocated
K base page copied to K destination page
V base page copied to V destination page
append span written into destination page
new page sealed for target generation
```

This occurs at:

```text
64  -> 192
192 -> 384
```

## 10.3 Newly introduced pages

When a touched logical page did not exist in the base generation:

```text
new physical page allocated
no base-page copy
only append token span written
page sealed
```

## 10.4 Forbidden mutation

```text
overwrite a sealed current page in place
change previous generation page content
reuse a free page before retirement receipt
publish partially sealed layer set
share one physical page between different content digests
```

---

# 11. Persistent pipeline-manager adoption

## 11.1 R3 pipeline cardinality

R2.3 owns seven pipeline purposes. R3 append introduces one additional purpose:

```text
BufferAtlasReference
TexturePopulation
TexturePersistentPopulation
TextureValidation
TextureIncrementalAppend
Candidate
Compare
Finalize
```

Canonical R3 count:

```text
pipeline kinds                    8
initial factory creations         8
normal commit factory creations   0
append-time factory creations     0
layer-time factory creations      0
device-lost wake creations        8 for the new device generation
```

## 11.2 New kind

```rust
HeadwiseTexturePipelineKind::TextureIncrementalAppend
```

The append shader is:

```text
headwise_kv_texture_append_persistent_cache_rgba4.wgsl
```

## 11.3 Append backend API

R3 adds or adopts a manager-backed path equivalent to:

```rust
pub fn append_persistent_cache_span_with_pipeline_manager(
    &mut self,
    source_k: &RawWgpuBufferLease,
    source_v: &RawWgpuBufferLease,
    request: &PersistentKvTextureAppendRequest,
    pipeline_manager: &HeadwiseTexturePipelineManager,
) -> Result<PersistentKvTextureLayerAppendReceipt>
```

The R3 physical path must not call a local `create_append_pipeline()`.

## 11.4 Device loss

On authoritative device loss:

```text
persistent texture session quarantined
old texture objects invalidated
old pipeline generation invalidated
in-flight shadow commit aborted
new device generation established
pipeline factory creates all 8 kinds once
new texture session requires a new full bootstrap population
old generation views cannot cross devices
```

Wake-up does not resume an old texture object on a new device.

---

# 12. Gate source-K/V lease policy

R3 does not alter production K/V authority.

## 12.1 Production model path

```text
borrow exact committed DecodeState layer K/V leases
same device and queue lineage
no host materialization
no payload readback
```

## 12.2 Physical gate harness

The physical gate may create one exact K/V source pair per texture generation bucket:

```text
6 source K buffers
6 source V buffers
```

Each pair is reused by the ten shadow commits in that bucket.

This is a gate harness property, not a claim that production owns one global K/V pair.

Required gate counters:

```text
K source buffer creations        6
V source buffer creations        6
K/V source-pair creations        6
source-pair creation per shadow commit 0
```

The source pair may be retired after its bucket completes and the next generation has been appended and adopted.

The texture residency survives source-pair retirement.

---

# 13. Shadow replay against one generation

## 13.1 Per-bucket reuse

For each texture generation, ten independent shadow commits consume the same generation view.

Required identity receipt:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTexture05GenerationReuseReceipt {
    pub texture_generation: u64,
    pub committed_token_count: usize,
    pub expected_shadow_commit_count: u32,
    pub observed_shadow_commit_count: u32,

    pub texture_identity_digest: String,
    pub generation_view_digest: String,
    pub pipeline_set_digest: String,

    pub texture_creation_delta: u32,
    pub full_population_delta: u32,
    pub append_transaction_delta: u32,

    pub unique_invocation_digest_count: u32,
    pub unique_capture_serial_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

PASS per generation:

```text
shadow commits                  10
texture creation delta          0
full population delta           0
append delta during replay      0
unique invocation digests      10
unique capture serials         10
texture identity unchanged   true
generation view unchanged    true
```

## 13.2 Dispatch binding

Each shadow commit binds:

```text
new Q invocation snapshot
new BufferAtlas reference snapshot
same published K/V texture generation
same page LUT digest
same texture object identity
new transient candidate/compare resources
```

---

# 14. Per-commit manual GC for transients only

## 14.1 R2.2 behavior revised by ownership class

R2.2 required registry drop before poll because the registry was commit-scoped.

R3 moves the registry to session scope. Therefore the healthy boundary now requires:

```text
ticket registry dropped                       true
Q source owner closed                         true
reference output owners closed                true
snapshot owners closed                        true
candidate scratch closed                      true
comparison scratch closed                     true
compact token resources closed                true
timestamp resources closed                    true
transient bind groups closed                   true

persistent residency registry retained        true
persistent texture identities retained        true
current/previous generation views retained     true
pipeline manager retained                      true
device and queue retained                      true
```

## 14.2 R3 transient-GC receipt

```rust
pub struct HeadwiseTexture05TransientGcReceipt {
    pub boundary_ordinal: u32,
    pub shadow_commit_ordinal: Option<u32>,
    pub texture_generation: Option<u64>,

    pub transient_owner_drop_complete: bool,
    pub persistent_registry_retained: bool,
    pub persistent_texture_identity_before: Option<String>,
    pub persistent_texture_identity_after: Option<String>,
    pub pipeline_set_digest_before: String,
    pub pipeline_set_digest_after: String,

    pub poll_mode: String,
    pub poll_status: String,
    pub duration_ns: u64,
    pub pass: bool,
    pub receipt_digest: String,
}
```

## 14.3 Required boundary counts

```text
healthy shadow transient GC     60
fault-drill transient GC         1
post-disable transient GC        8
total per-commit transient GC   69
```

The existing 69-boundary admission chain remains.

## 14.4 Persistent-session retirement is separate

After candidate disable, persistent session resources are retired through a dedicated boundary that is not counted as one of the 69 per-commit transient-GC boundaries.

```text
candidate admission closed
  -> no in-flight texture dispatch
  -> current/previous metadata receipt preserved
  -> persistent registry dropped
  -> generation source pair dropped
  -> device.poll(Wait)
  -> session-retirement receipt sealed
  -> post-disable BufferAtlas-only phase admitted
```

This avoids retaining the persistent texture allocation through the eight BufferAtlas-only continuity commits.

---

# 15. Append-byte accounting

## 15.1 Logical payload formula

Per layer, K and V logical payload bytes for an append are:

```text
append_token_count
× batch_count
× kv_head_count
× head_dim
× sizeof(f32)
× 2 roles
```

Canonical scalar geometry:

```text
batch     1
kv heads  4
head dim 64
f32       4 bytes
K+V       2
```

Per appended token per layer:

```text
1 × 4 × 64 × 4 × 2 = 2,048 bytes
```

## 15.2 Canonical byte totals

Initial full population at KV64:

```text
64 × 2,048 × 22
= 2,883,584 bytes
```

Five append transitions:

```text
1,728 appended tokens × 2,048 × 22
= 77,856,768 bytes
```

R3 total logical K/V texture population payload:

```text
2,883,584 + 77,856,768
= 80,740,352 bytes
```

Current repeated-full-population theoretical payload:

```text
(64 + 192 + 384 + 768 + 1280 + 1792)
× 10 commits per bucket
× 2,048 bytes
× 22 layers
= 2,018,508,800 bytes
```

Expected logical payload reduction:

```text
2,018,508,800 / 80,740,352
= 25.0×
```

These values count logical K/V values processed across all layer population dispatches. They do not claim exact driver memory traffic.

## 15.3 Byte receipt

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HeadwiseTexture05AppendByteAccountingReceipt {
    pub schema_version: u32,
    pub receipt_kind: String,

    pub full_population_tokens: u64,
    pub append_tokens: u64,
    pub bytes_per_token_per_layer: u64,
    pub layer_count: u32,

    pub full_population_logical_bytes: u64,
    pub append_logical_bytes: u64,
    pub total_logical_population_bytes: u64,
    pub repeated_full_baseline_bytes: u64,
    pub logical_reduction_ratio: f64,

    pub touched_page_plan_count: u64,
    pub cow_page_plan_count: u64,
    pub new_page_plan_count: u64,
    pub cow_texture_copy_operation_count: u64,

    pub host_upload_count: u64,
    pub host_repack_count: u64,
    pub cpu_materialize_count: u64,
    pub payload_readback_count: u64,

    pub pass: bool,
    pub receipt_digest: String,
}
```

Canonical expected values:

```text
full population tokens               64
append tokens                       1728
bytes/token/layer                    2048
layers                                 22
full population bytes          2,883,584
append bytes                 77,856,768
total bytes                  80,740,352
baseline bytes            2,018,508,800
reduction ratio                       25.0

touched page plans                     330
COW page plans                          44
new page plans                         286
COW texture copies                      88

host upload                              0
host repack                              0
CPU materialization                      0
payload readback                         0
```

---

# 16. Steady-state latency separation

## 16.1 Existing measurement problem

The current `timestamp_gpu_envelope()` wraps the complete `run_shadow_commit()` closure, which includes full texture population. That makes the reported value a cold reconstruction envelope rather than a pure live-shadow envelope.

R3 must separate residency maintenance from shadow replay without deleting either cost.

## 16.2 Required timing planes

```text
session_bootstrap_full_population_ns
  measured once before the 60-commit soak

residency_append_ns
  measured for each of five append transitions

shadow_capture_ns
  Q/reference capture for each shadow commit

shadow_candidate_ns
  candidate dispatch for each shadow commit

shadow_compare_finalize_ns
  device comparison and compact token finalize

steady_state_shadow_total_ns
  capture + candidate + compare/finalize

transition_end_to_end_ns
  append + first shadow replay at a new KV bucket
```

## 16.3 Promotion semantics

The old latency budget must not be made easier by silently deleting work.

R3 reports both:

```text
steady-state shadow p50/p95/p99/max across 60 commits
transition end-to-end p50/p95/p99/max across 5 transitions
bootstrap full-population duration
```

Canonical original Texture-05 latency predicates apply to:

```text
steady_state_shadow_total_ns
```

because the Texture-05 specification defines the shadow GPU envelope as capture, candidate, comparison and compact finalize.

Residency maintenance remains separately visible and must not be hidden, zeroed or folded into an undocumented metric.

R3 rev.1 does not invent a device-independent append-latency promotion threshold. It seals the measurements for later calibration.

## 16.4 Timing receipt

```rust
pub struct HeadwiseTexture05SteadyStateLatencySeparationReceipt {
    pub bootstrap_full_population_ns: u64,

    pub append_observation_count: u32,
    pub append_p50_ns: u64,
    pub append_p95_ns: u64,
    pub append_p99_ns: u64,
    pub append_max_ns: u64,

    pub shadow_observation_count: u32,
    pub shadow_p50_ns: u64,
    pub shadow_p95_ns: u64,
    pub shadow_p99_ns: u64,
    pub shadow_max_ns: u64,

    pub transition_observation_count: u32,
    pub transition_p50_ns: u64,
    pub transition_p95_ns: u64,
    pub transition_p99_ns: u64,
    pub transition_max_ns: u64,

    pub residency_time_hidden_count: u32,
    pub timing_plane_alias_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Required counts:

```text
bootstrap observations  1
append observations     5
shadow observations    60
transition observations 5
hidden residency time   0
metric alias count      0
```

---

# 17. No per-commit texture reconstruction receipt

```rust
pub struct HeadwiseTexture05NoReconstructionReceipt {
    pub session_registry_creation_count: u32,
    pub persistent_layer_residency_count: u32,
    pub persistent_texture_pair_creation_count: u32,

    pub shadow_commit_count: u32,
    pub per_commit_registry_creation_count: u32,
    pub per_commit_texture_pair_creation_count: u32,
    pub per_commit_full_population_count: u32,

    pub append_transaction_count: u32,
    pub append_texture_creation_count: u32,
    pub append_texture_resize_count: u32,

    pub texture_identity_change_without_device_loss_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

PASS values:

```text
session registry creation               1
persistent layer residencies           22
persistent texture-pair creations      22
shadow commits                          60
per-commit registry creations            0
per-commit texture-pair creations        0
per-commit full populations              0
append transactions                      5
append texture creations                 0
append texture resizes                   0
identity changes without device loss     0
```

---

# 18. Persistent identity ledger

The runtime records immutable identities for:

```text
session registry
22 layer residency objects
22 K texture objects
22 V texture objects
22 physical page allocators
pipeline set
device generation
```

Per shadow commit, the ledger proves:

```text
same session registry identity
same layer residency identities
same K/V texture identities
same allocator identities
same pipeline-set digest
```

Generation-view and page-LUT digests may change only during the five append transitions.

---

# 19. Backpressure and concurrency

R3 allows one append transaction per decode session.

```text
append_in_flight set cardinality <= 1 per session
shadow replay admitted only against a published current generation
no replay against staged generation
no append while a shadow dispatch still references the current generation unless the implementation proves immutable-page safety and submission ordering
```

Canonical gate ordering is conservative:

```text
drain ten commits for bucket N
  -> transient GC complete
  -> append to bucket N+1
  -> publish
  -> begin ten commits for bucket N+1
```

No overlap is required for R3 PASS.

---

# 20. Failure and quarantine

Immediate R3 candidate failures:

```text
bootstrap full population count != 1
full population invoked after bootstrap
persistent registry recreated
texture identity changed without device loss
append span not monotonic
append layer cardinality != 22
COW plan invalid
sealed page overwritten
previous view mutated
refcount underflow
physical capacity exhausted
append pipeline created lazily
append transaction silently replaced with full population
shadow dispatch consumes staged generation
byte accounting mismatch
timing plane alias or hidden residency time
```

Failure consequences:

```text
candidate transaction aborts
last valid current generation preserved when possible
new shadow admission closed
BufferAtlas production authority unchanged
canonical Texture-05 promotion artifact forbidden
R3 failure artifact written
```

---

# 21. Persistent-session retirement

## 21.1 Trigger

```text
candidate quarantine and disable
normal session close
authoritative device loss
operator-requested teardown
```

## 21.2 Order

```text
close candidate admission
  -> drain submitted shadow work
  -> drop transient tickets and snapshots
  -> preserve final metadata receipts
  -> drop generation source leases
  -> drop persistent residency registry
  -> drop physical texture objects
  -> keep device/pipeline manager when session closes normally
  -> poll(Wait)
  -> seal retirement receipt
```

On device loss, the old device-bound pipeline manager and textures are invalidated together.

## 21.3 Receipt

```rust
pub struct HeadwiseTexture05SessionRetirementReceipt {
    pub reason: String,
    pub final_texture_generation: u64,
    pub final_token_count: usize,
    pub candidate_admission_closed: bool,
    pub submitted_work_drained: bool,
    pub persistent_registry_dropped: bool,
    pub persistent_texture_pair_drop_count: u32,
    pub device_retained: bool,
    pub pipeline_manager_retained: bool,
    pub poll_status: String,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Normal candidate-disable values:

```text
persistent texture pair drops 22
device retained              true
pipeline manager retained    true
```

---

# 22. Runtime implementation ownership

## 22.1 New backend module

```text
crates/burn_webgpu_backend/src/
  headwise_texture_05_persistent_session.rs
```

Responsibilities:

```text
persistent texture identity inspection
append manager-backed pipeline binding
texture object creation counters
append byte counters
session-retirement physical outcome
```

## 22.2 New model-core module

```text
crates/model_core/src/
  headwise_texture_05_persistent_residency_authority.rs
```

Responsibilities:

```text
R3 state machine
monotonic six-generation plan
full-population receipt
no-reconstruction receipt
generation-reuse receipt
append-byte accounting receipt
steady-state latency separation receipt
persistent identity ledger
session-retirement authority
```

## 22.3 Existing modules modified

```text
crates/burn_webgpu_backend/src/
  headwise_texture_pipeline_factory.rs
  headwise_texture_pipeline_manager.rs
  headwise_kv_texture_incremental_append.rs

crates/model_core/src/
  headwise_texture_persistent_kv_binding.rs

crates/orchestrator_local/src/bin/
  ash_attn_headwise_texture_05_gate.rs
  ash_attn_headwise_texture_05_r3_gate.rs
```

## 22.4 CLI registry

```text
crates/orchestrator_local/src/
  headwise_texture_05_r3_cli_registry.rs

specs/cli/
  ash_attn_headwise_texture_05_r3.args
```

---

# 23. Required physical source shape

The active Texture-05 gate must be reorganized so that:

```rust
let persistent_runtime = HeadwiseTexture05PersistentSessionRuntime::bootstrap(...)?;

for kv_bucket in [64, 192, 384, 768, 1280, 1792] {
    if kv_bucket != 64 {
        persistent_runtime.append_to(kv_bucket)?;
    }

    for (route, seq_q) in [
        (IncrementalDecode, 1),
        (ChunkedDecode, 2),
        (ChunkedDecode, 6),
        (ChunkedDecode, 12),
        (ChunkedDecode, 24),
    ] {
        for repeat in 0..2 {
            run_shadow_replay_against_current_generation(...)?;
            drop_commit_transients();
            manual_transient_gc()?;
        }
    }
}
```

Equivalent factoring is allowed. The source audit must still prove the same ownership and count invariants.

Forbidden physical shape:

```rust
for commit in soak_order {
    let registry = HeadwiseTextureSessionResidencyRegistry::default();
    populate_all_layers();
}
```

---

# 24. Artifact contract

## 24.1 Rust-authored child artifacts

```text
workspace/runtime/attention/headwise/texture/05/r3/
  persistent_session_bootstrap_receipt.json
  full_population_count_receipt.json
  monotonic_generation_plan.json
  generation_reuse_receipts.json
  append_transactions.json
  append_byte_accounting_receipt.json
  current_previous_view_ledger.json
  physical_page_retirement_ledger.json
  no_reconstruction_receipt.json
  persistent_identity_ledger.json
  transient_gc_receipts.json
  session_retirement_receipt.json
  steady_state_latency_separation_receipt.json
  failure_receipt.json                    only on failure
```

Top-level:

```text
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_05_r3_runtime_artifact.json
  ash_attn_headwise_texture_05_r3_local_manifest.json
```

## 24.2 Runtime artifact top-level fields

```text
schema
patchId
buildRevision
parentRevisions
pass
passToken
productionAuthority
candidateAuthority
coverageSummary
persistentSessionSummary
fullPopulationSummary
appendSummary
byteAccountingSummary
pipelineSummary
transientGcSummary
latencySeparationSummary
sessionRetirementSummary
artifactHashes
sourceHashes
```

## 24.3 Atomic write

All JSON artifacts use:

```text
canonical serialization
temporary sibling write
flush
atomic rename
readback
SHA-256 verification
```

---

# 25. CLI contract

Suggested required keys:

```text
--repo-root
--expected-patch-id
--expected-build-revision
--parent-r2-3-runtime-artifact
--parent-r2-3-local-manifest

--expected-layer-count=22
--expected-shadow-commit-count=60
--expected-coverage-cell-count=30
--expected-healthy-per-cell=2

--expected-texture-generation-count=6
--expected-full-population-transaction-count=1
--expected-layer-full-population-count=22
--expected-append-transaction-count=5
--expected-layer-append-count=110

--expected-physical-page-capacity=16
--expected-persistent-texture-pair-count=22
--expected-current-previous-retention=2

--expected-touched-page-plan-count=330
--expected-cow-page-plan-count=44
--expected-new-page-plan-count=286
--expected-cow-texture-copy-count=88

--expected-full-population-bytes=2883584
--expected-append-bytes=77856768
--expected-total-population-bytes=80740352
--expected-repeated-full-baseline-bytes=2018508800

--expected-r3-pipeline-kind-count=8
--require-manager-backed-append-pipeline
--forbid-lazy-append-pipeline-creation

--require-session-scoped-registry
--forbid-per-commit-registry-creation
--forbid-per-commit-texture-creation
--forbid-post-bootstrap-full-population
--forbid-silent-full-repopulation-fallback

--require-transient-only-manual-gc
--expected-transient-gc-boundary-count=69
--require-persistent-identity-across-gc

--require-latency-plane-separation
--forbid-hidden-residency-time

--runtime-artifact
--local-manifest
```

---

# 26. Positive controls

Minimum positive cases:

```text
01  One registry is created before the soak loop
02  Twenty-two persistent layer residencies are created
03  Twenty-two K/V texture pairs are created
04  Physical page capacity is sixteen per layer
05  One full population transaction is observed
06  Twenty-two layer full populations are observed
07  No full population occurs after bootstrap
08  Six texture generations are published
09  Five append transactions are observed
10  One hundred ten layer append receipts are observed
11  Texture generations increase monotonically
12  Token counts follow 64,192,384,768,1280,1792
13  Ten shadow commits reuse every texture generation
14  Sixty shadow commits remain
15  Thirty coverage cells remain
16  Two healthy commits satisfy every cell
17  Invocation identity remains unique within a shared texture generation
18  Texture identity remains stable across all six generations
19  Current and previous views are retained
20  Older views are released
21  Refcount-zero pages are retired
22  Untouched pages are physically reused
23  Touched partial pages use COW
24  Touched-page plan count is 330
25  COW page plan count is 44
26  New-page plan count is 286
27  COW texture copy count is 88
28  Append logical bytes equal 77,856,768
29  Total logical population bytes equal 80,740,352
30  Repeated-full baseline equals 2,018,508,800
31  Host upload remains zero
32  Host repack remains zero
33  CPU materialization remains zero
34  Payload readback remains zero
35  Pipeline manager owns eight pipeline kinds
36  Append pipeline is created once at initialization
37  Append-time pipeline creation is zero
38  Per-commit texture creation is zero
39  Manual GC count remains 69
40  Manual GC drops transients only
41  Persistent identity survives every healthy manual GC
42  Bootstrap timing is separated
43  Five append timings are separated
44  Sixty shadow timings are separated
45  Hidden residency-time count is zero
46  Candidate output commit remains zero
47  BufferAtlas authority remains unchanged
48  Session retirement drops twenty-two texture pairs
49  Device and pipeline manager survive normal session retirement
50  Runtime artifact and manifest are Rust-authored
```

---

# 27. Negative controls

Minimum negative cases:

```text
01  Registry constructed inside shadow commit loop
02  Texture residency constructed inside shadow commit loop
03  Full population after bootstrap
04  Append failure silently triggers full population
05  Texture object recreated for a new generation
06  Texture resized during append
07  KV token count decreases
08  Empty append span accepted
09  Texture generation increments for every replay
10  Invocation identity reused across two commits
11  Staged generation consumed by shadow replay
12  Previous generation page overwritten
13  Sealed page mutated in place
14  Untouched page rewritten
15  Referenced page retired
16  Refcount underflow
17  Physical page capacity exhaustion hidden by reallocation
18  Append layer count not equal to 22
19  Missing layer view at publish
20  Mixed generation layer set published
21  Direct create_append_pipeline call in R3 path
22  Pipeline cache miss silently rebuilds during Ready
23  Pipeline cardinality remains seven after append adoption
24  Per-commit K/V source pair creation
25  Manual GC drops persistent registry
26  Manual GC changes texture identity
27  Manual GC changes pipeline-set digest
28  Residency cost omitted from all timing planes
29  Append time folded into shadow time without disclosure
30  Bootstrap time counted as sixty shadow observations
31  Byte accounting uses host payload estimates silently
32  Host upload introduced
33  Host repack introduced
34  Payload readback introduced
35  Candidate output committed
36  BufferAtlas output suppressed
37  Canonical promotion artifact written while eligibility remains HOLD
38  R3 PASS mislabeled SustainedShadowSoakBound
39  Session retirement occurs before submitted work drain
40  Old device texture identity adopted after device wake-up
```

---

# 28. Source audits

The R3 verification gate must prove at minimum:

```text
HeadwiseTextureSessionResidencyRegistry::default()
  is absent from the 60-commit inner loop.

populate_layer_generation*
  appears only in bootstrap population flow for R3.

append_committed_generation
  is the physical generation transition path.

append_persistent_cache_span_with_pipeline_manager
  is used by R3.

create_append_pipeline
  is not reachable from the R3 physical path.

texture creation counters
  do not change after bootstrap.

full population counters
  do not change after bootstrap.

texture generation increments
  exactly five times after bootstrap.

shadow commit ordinal
  increments sixty times.

manual GC
  retains registry and texture identity for healthy boundaries.
```

The gate should combine:

```text
compiled behavioral fixtures
physical runtime receipts
source AST or constrained source audit
artifact hash verification
negative-control mutation fixtures
```

String search alone is not sufficient for final PASS.

---

# 29. Completion gate

R3 PASS requires:

```text
positive controls                              >= 50
negative controls                              >= 40

persistent registry creation                     1
persistent layer residencies                    22
persistent texture pairs                        22
physical page capacity per layer                16

full population transactions                     1
layer full populations                          22
post-bootstrap full populations                  0

texture generations                              6
append transactions                              5
layer append transactions                      110
shadow commits                                  60
coverage cells                                  30
healthy per cell                                 2

per-commit texture creations                     0
append texture creations                         0
texture resizes                                  0
silent full-repopulation fallbacks               0

append touched-page plans                      330
append COW page plans                            44
append new-page plans                           286
COW texture copies                               88

full population logical bytes             2,883,584
append logical bytes                     77,856,768
total logical population bytes           80,740,352
repeated-full baseline bytes           2,018,508,800

R3 pipeline kinds                                8
normal factory creation delta                    0
append-time factory creation delta               0

transient manual-GC boundaries                  69
persistent identity changes across GC            0

bootstrap timing observations                    1
append timing observations                       5
shadow timing observations                      60
hidden residency-time count                      0

candidate output commits                         0
host uploads                                     0
host repacks                                     0
CPU materializations                             0
payload readbacks                                0
production authority mutation                    0
```

Patch-local PASS token:

```text
PASS_ASH_ATTN_HEADWISE_TEXTURE_05_R3_SESSION_SCOPED_PERSISTENT_TEXTURE_RESIDENCY_ONE_TIME_FULL_POPULATION_INCREMENTAL_KV_TEXEL_APPEND_CURRENT_PREVIOUS_GENERATION_VIEW_IMMUTABLE_PAGE_REUSE_TOUCHED_PAGE_COPY_ON_WRITE_NO_PER_COMMIT_TEXTURE_RECONSTRUCTION_PERSISTENT_PIPELINE_MANAGER_ADOPTION_PER_COMMIT_MANUAL_GC_FOR_TRANSIENTS_ONLY_FULL_POPULATION_COUNT_APPEND_BYTE_ACCOUNTING_STEADY_STATE_LATENCY_SEPARATION_SEALED
```

After R3 PASS:

```text
KvTextureGqa4V1
  LiveShadowParityBound
  EligibilityFailureLocalized
  PerCommitManualGcBound
  PipelineFactoryManagerWakeBound
  SessionPersistentTextureResidencyBound
  ProductionOutputCommitForbidden
```

The original Texture-05 eligibility result may still be HOLD. R3 does not forge promotion.

---

# 30. Direct execution contract

R3 structural and artifact gate:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_r3_gate -- "@specs/cli/ash_attn_headwise_texture_05_r3.args"
```

Physical Texture-05 rerun after R3 PASS:

```powershell
cargo run --release --manifest-path crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_attn_headwise_texture_05_gate -- "@specs/cli/ash_attn_headwise_texture_05.args"
```

Expected physical disclosure:

```text
full population count  1
append count           5
texture generations    6
shadow commits         60
per-commit reconstruction 0

bootstrap population latency
append latency summary
steady-state shadow latency summary
transition end-to-end latency summary

final eligibility
  Promote
  or exact remaining HOLD predicates
```

---

# 31. Packaging contract for later bake

The code-baked ZIP must include:

```text
R3 backend implementation
R3 model-core authority
R3 physical gate integration
R3 verification gate
R3 CLI registry
R3 response file
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

Rust generates runtime artifact and manifest when the R3 gate executes.

The overlay ZIP contains only files changed by R3, rooted at repository root.

---

# 32. Final seal

R3 replaces:

```text
one shadow commit
  -> one registry
  -> twenty-two full texture populations
  -> destroy everything
```

with:

```text
one session
  -> one registry
  -> twenty-two persistent K/V texture pairs
  -> one bootstrap full population
  -> five append-only generation transitions
  -> sixty independent shadow replays
  -> transient-only per-commit GC
  -> explicit session retirement
```

The patch does not merely make allocation cheaper. It corrects the semantic identity of a sustained soak: the residency survives, only the committed append span changes, and the gate measures steady-state shadow work instead of repeatedly timing cold reconstruction.
