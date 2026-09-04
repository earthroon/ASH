# ASH-BP-DELTA-K-OBSERVATION-HOTPATH-PERSISTENT-RUNTIME-DEVICE-SOURCE-ADOPTION-ASYNC-EVIDENCE-COLLECTION-HOTPATH-DIGEST-RETIREMENT-R1

## 0. Revision

```text
Patch ID:
ASH-BP-DELTA-K
-OBSERVATION-HOTPATH
-PERSISTENT-RUNTIME
-DEVICE-SOURCE-ADOPTION
-ASYNC-EVIDENCE-COLLECTION
-HOTPATH-DIGEST-RETIREMENT
-R1

Short name:
DK-PERF-R1
```

Status at this source bake:

```text
STATIC SOURCE MATERIALIZATION       = PARTIAL / ACTIVE
RUST COMPILE PASS                   = NOT CLAIMED BY BAKE ENVIRONMENT
SEMANTIC PARITY PASS                = NOT YET CLAIMED
PHYSICAL PERFORMANCE PASS           = NOT YET CLAIMED
PRODUCTION PERFORMANCE PROMOTION    = HOLD
```

Static source token:

```text
PASS_ASH_BP_DELTA_K_OBSERVATION_HOTPATH_PERSISTENT_RUNTIME_DEVICE_SOURCE_ASYNC_EVIDENCE_DIGEST_RETIREMENT_R1_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_OBSERVATION_HOTPATH_PERSISTENT_RUNTIME_DEVICE_SOURCE_ASYNC_EVIDENCE_DIGEST_RETIREMENT_R1_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_OBSERVATION_HOTPATH_PERSISTENT_RUNTIME_DEVICE_SOURCE_ASYNC_EVIDENCE_DIGEST_RETIREMENT_R1
```

## 1. Parent

Direct source parent:

```text
ASH_PASS3_EVE_PHYS_R1_BASE_TRAIN_R8_OWNER_MOVE_FIX_CODE_ONLY.zip
SHA-256 = f05bec5faad2ed6fa83003cca0f57e3941df72ba1a90ac7bd1b7dfcf101adf5a
```

The parent already contains the current WGPU26 vendor path, TensorCube/MCU R8 ownership split, and EVE-PHYS-R1 static source materialization.

DK-PERF-R1 does not change WGPU generation, Burn/CubeCL package generation, Adam mathematics, Muon mathematics, or TensorCube fusion geometry.

## 2. Claim boundary

DK-PERF-R1 is a physical-plumbing performance revision.

It preserves the current Delta-K mathematics and topology semantics:

```text
Delta-K                 = I * M^2
local information       = existing row-sketch temporal definition
local material          = existing relative update-scale definition
bridge cosine           = existing exact flattened 256D gradient cosine
bridge temporal I       = existing cosine temporal-delta definition
fusion thresholds       = unchanged
fission thresholds      = unchanged
hysteresis              = unchanged
cooldown                = unchanged
pair matching           = unchanged
Muon 16x16/16x32/32x16  = unchanged
Newton-Schulz            = unchanged
```

The revision is allowed to change resource lifetime, transport, evidence identity policy, and generation transaction boundaries only when those changes preserve planner/topology semantics.

## 3. Parent static cost model

The pre-bake static architecture review estimated the canonical 22-layer Muon scope as:

```text
Muon matrix parameter count = 154
Muon eligible elements       = 968,884,224
16x16 tile count T           = 3,784,704
neighbor pair count P        = 7,520,128
```

The parent architecture was modeled as approximately:

```text
pre-observation:
  H2D ~ 3.996 GB / optimizer generation
  D2H ~ 0.422 GB / optimizer generation
  submits ~ 462
  explicit hard waits ~ 308

post-evidence:
  H2D ~ 0.120 GB
  D2H ~ 0.422 GB
  submits ~ 154
  CPU drain barriers ~ 154

combined evidence transport:
  ~4.96 GB / optimizer generation
```

The same review identified a normal-path full-payload GPU SHA implementation that could serialize candidate-weight, candidate-momentum, and orthogonal-update digest work per parameter.

These values are architecture-derived estimates, not physical benchmark receipts.

## 4. Target laws

Final DK-PERF-R1 physical promotion requires all of the following:

```text
A. Disabled mode is true zero Delta-K hotpath cost.
B. Delta-K full weight H2D is zero on canonical resident-source operation.
C. Per-parameter local/bridge hard waits are zero.
D. Steady-state Delta-K pipeline construction is zero.
E. Normal-hotpath full-payload SHA count is zero.
F. Local/bridge/planner temporal state shares one generation commit/abort authority.
G. Planner/topology decision parity is exact on qualification fixtures.
```

The initial source bake intentionally does not claim that all target laws are physically closed.

## 5. Typed runtime mode authority

Materialized:

```text
crates/base_train/src/bp_delta_k_runtime_mode_r1.rs
```

Typed state:

```rust
pub enum BpDeltaKRuntimeModeR1 {
    Disabled,
    ObserveOnly,
    Active,
}
```

Existing `ASH_BP_DK_FUSION_PLANNER_MODE` is parsed through this typed authority.

`OBSERVE_ONLY` is accepted by the legacy planner parser and is mapped to no topology mutation while the full observe-only shadow planner cutover remains pending.

### Current static truth

```text
typed Disabled/ObserveOnly/Active authority  = MATERIALIZED
ObserveOnly no topology mutation             = MATERIALIZED
Disabled true outer zero-cost bypass         = NOT YET PHYSICALLY CUT OVER
ObserveOnly full shadow-decision semantics   = NOT YET FULLY CUT OVER
```

Therefore Disabled zero-cost physical PASS remains HOLD.

## 6. Evidence epoch authority

Materialized:

```text
crates/base_train/src/bp_delta_k_evidence_epoch_r1.rs
```

State model:

```text
Encoding -> Submitted -> Ready -> Consumed
       \       \          \
        +-------> Aborted <-+
```

This is the generation-scoped authority for the later local+bridge aggregate submission/readback cutover.

### Current static truth

```text
typed evidence epoch state machine     = MATERIALIZED
full generation-wide encoder batching  = NOT YET CUT OVER
aggregate readback arena               = NOT YET CUT OVER
```

## 7. Canonical resident weight device-source adoption

The local observer now supports:

```rust
TensorCubeBpDkLocalObserverSourceWeight::DeviceBuffer {
    buffer,
    allocation,
    byte_offset,
    byte_size,
}
```

When `ProductionMuonRuntime` has the committed segmented Muon generation for the requested source generation, the observer binds the exact resident weight `Arc<wgpu::Buffer>` directly.

It also submits a read-only existing-allocation lease for that physical allocation.

No observer-only weight buffer is allocated and no `queue.write_buffer` of the complete weight payload is performed for that direct path.

Telemetry reports:

```text
parameter_upload_bytes = 0
```

for the DeviceBuffer branch.

Fallback Packed/WaveTiles paths remain for source configurations that do not expose the committed device generation.

### Current static truth

```text
direct resident weight source seam        = MATERIALIZED
physical allocation identity carried      = MATERIALIZED
observer-only full H2D on direct path      = RETIRED
all production routes guaranteed direct   = NOT YET PHYSICALLY QUALIFIED
```

Therefore global `delta_k_weight_h2d_bytes = 0` remains a physical qualification condition, not a static PASS claim.

## 8. Local Delta-K generation transaction

The parent local observer validated the candidate state and then immediately submitted a second GPU copy from candidate state into committed resident state.

DK-PERF-R1 retires that early-commit model.

New state:

```text
committed local temporal buffer
pending local candidate buffer
```

Observation now:

```text
committed state
  -> GPU observation
  -> candidate state
  -> compact receipt validation
  -> candidate retained as pending authority
```

No second parameter-local GPU state-copy submit occurs.

Generation resolution:

```text
Commit:
  pending Arc becomes committed Arc
  metadata advances

Abort:
  pending Arc is dropped
  committed Arc and metadata remain unchanged
```

Materialized transition:

```rust
TensorCubeBpDkLocalGenerationTransitionR1::{Commit, Abort}
```

## 9. Reinitialization is transactional

Policy/source/registry/routing reinitialization previously zeroed the committed local EMA buffer before the optimizer generation outcome was known.

The static bake moves reinitialization to candidate-side state:

```text
old committed state remains untouched
        |
revision mismatch
        v
fresh zero source buffer for this candidate observation
        |
        v
pending candidate
```

On generation abort, the prior committed temporal authority remains intact.

On generation commit, the pending buffer and its next source/observer/policy/registry/routing metadata become committed together.

This removes the reinitialization exception from the generation-transaction law.

## 10. Local generation integration

`ProductionBpDkObservationRuntime` now exposes internal generation operations:

```text
pending_generation_r1
commit_pending_generation_r1
abort_pending_generation_r1
```

The Muon generation commit preflight checks local pending generation identity alongside bridge/planner pending state.

Finalization commits the local pending state and updates the existing Delta-K state-commit telemetry.

Generation abort resolves the local pending state with Abort.

The intended generation identity is the existing optimizer-step / BP-generation identity already passed to the local observer.

## 11. Persistent post-update runtime

Materialized:

```text
crates/base_train/src/bp_delta_k_persistent_device_runtime_r1.rs
```

`ProductionBpDkRuntimeR8` now owns one `BpDeltaKPersistentDeviceRuntimeR1` for the runtime lifetime.

The post-update reduction producer is no longer constructed in the per-parameter post-evidence callsite.

Normal shape:

```text
ProductionMuonRuntime / device lifetime
  -> BpDeltaKPersistentDeviceRuntimeR1
     -> persistent BpDkDevicePostUpdateRuntimeR1
        -> persistent reduction BGL/pipelines
```

### Current static truth

```text
per-parameter post runtime construction       = RETIRED
persistent post reduction pipelines           = MATERIALIZED
steady-state post pipeline rebuild intent      = ZERO
physical build-count receipt                   = NOT YET EXECUTED
```

## 12. Digest authority split

The post-update backend now has two typed policies:

```rust
BpDkDevicePostUpdateDigestModeR1::ExactSha256
BpDkDevicePostUpdateDigestModeR1::RuntimeIdentity
```

### ExactSha256

Preserves the existing qualification/counterfactual full-payload SHA path.

### RuntimeIdentity

Normal hotpath mode:

```text
SHA shader module creation    = 0
SHA BGL creation              = 0
SHA pipeline creation         = 0
SHA output buffer             = 0
SHA compute pass              = 0
SHA readback bytes            = 0
hotpath_full_payload_sha_count= 0
```

It produces small 64-hex runtime identity digests from generation/resource/allocation/backing/semantic-plan metadata instead of reading every f32 payload through a cryptographic shader.

The digest policy is explicitly tagged:

```text
ASH.BP-DK.DEVICE.POST-UPDATE.RUNTIME-IDENTITY.R1
```

These runtime identity values are not represented as durable content equivalence.

## 13. Exact audit path remains available

DK-PERF-R1 does not delete exact SHA capability.

When the existing local counterfactual mode is enabled, the persistent post runtime is created with `ExactSha256` so the existing exact oracle/qualification path continues to compare exact candidate weight, momentum, and update digests.

Normal counterfactual-disabled hotpath uses `RuntimeIdentity`.

Thus:

```text
production identity proof  != durable/audit content digest
```

and each has an explicit policy authority.

## 14. Compact evidence ABI compatibility

`BpDkDevicePostUpdateCompactEvidenceR1` adds:

```text
hotpath_full_payload_sha_count
runtime_identity_digest_count
```

with serde defaults so older serialized evidence that lacks these counters can still deserialize as zero-valued fields where applicable.

The base_train wrapper accepts either:

```text
ASH.BP-DK.DEVICE.POST-UPDATE.F32-SHA256.R1
ASH.BP-DK.DEVICE.POST-UPDATE.RUNTIME-IDENTITY.R1
```

while the dedicated exact physical-comparison closure remains an ExactSha256 qualification path.

## 15. Physical receipt authority

Materialized:

```text
crates/base_train/src/bp_delta_k_perf_physical_receipt_r1.rs
```

Receipt fields include:

```text
runtime mode
parameter/tile/pair counts
weight/control H2D
local/bridge/post D2H
submit counts
parameter-local hard waits
generation-level waits
post spin waits
pipeline builds
steady-state pipeline builds
hotpath full-payload SHA count
local transaction commit/abort counts
semantic parity
topology-decision parity
physical claim state/pass token
```

Bake constant:

```text
DK_PERF_R1_PHYSICAL_QUALIFIED_AT_BAKE = false
```

## 16. Current remaining physical blockers

The static source inspection intentionally records the remaining legacy hotpath boundaries.

### 16.1 Local observer wait remains

Current local observer still contains:

```text
wait_for_submission_exact(...)
```

per observed parameter.

Therefore:

```text
parameter_local_hard_wait_count = 0
```

is NOT yet physically satisfied.

### 16.2 Bridge observer wait remains

The existing bridge pair observer still uses its parameter/batch-local exact wait.

Generation-wide local+bridge batch collection is not yet the active execution path.

### 16.3 Post evidence spin/drain remains

The production callsite still loops around `try_collect_parameter` and calls `std::thread::yield_now()` while waiting for the per-parameter post evidence result.

Therefore:

```text
post_spin_wait_count = 0
```

is NOT yet physically satisfied.

### 16.4 Disabled outer bypass remains

Typed Disabled authority is present, but the outer production call graph still reaches the existing observation machinery before legacy planner Disabled takes effect.

Therefore Disabled is not yet proven zero-cost.

## 17. Why static PASS is partial

The source bake is deliberately split into:

```text
MATERIALIZED NOW:
  typed runtime mode
  evidence epoch authority
  direct resident weight source seam
  persistent post runtime
  normal-hotpath SHA retirement mode
  exact audit SHA preservation
  local candidate/commit/abort transaction
  transactional reinitialization
  physical receipt type

STILL HOLD:
  Disabled outer zero-cost bypass
  true generation-wide local+bridge submission batch
  aggregate pre evidence readback arena
  local per-parameter wait removal
  bridge per-parameter wait removal
  post per-parameter spin-drain removal
  physical semantic/topology parity campaign
  physical performance campaign
```

No physical PASS token may be emitted from this source bake.

## 18. Semantic invariants

The following are unchanged by the source bake:

```text
local I formula
local M formula
local Delta-K formula
bridge exact 256D cosine
bridge temporal information
bridge material
bridge Delta-K
fusion/fission thresholds
confirmation counts
cooldown policy
pair candidate ordering
Muon execution-domain geometry
counterfactual algorithm
objective probe algorithm
```

RuntimeIdentity affects evidence identity plumbing only; it does not feed planner mathematics.

## 19. Physical promotion requirements

Final physical PASS requires, at minimum:

```text
semantic_parity                   = true
topology_decision_parity          = true

normal direct-path weight H2D     = 0
parameter-local hard waits        = 0
post spin waits                   = 0
steady-state pipeline builds      = 0
normal-hotpath full-payload SHA   = 0

local generation identity
  == bridge generation identity
  == planner generation identity
  == optimizer committed generation
```

Disabled mode additionally requires literal zero Delta-K submits/maps/H2D/D2H/pipeline/graph/digest work.

## 20. Performance qualification method

Physical performance evidence shall separate:

```text
Disabled
ObserveOnly
Active without extended counterfactual/objective qualification
Active with post evidence
Explicit counterfactual/objective qualification
```

Use warm steady-state and paired order-balanced runs such as ABBA/BAAB where feasible.

Record local/bridge GPU time, pre collect time, planner CPU time, Muon GPU time, post evidence time, H2D/D2H, submits, maps, waits, pipeline builds, and unattributed time.

No fixed speedup percentage is invented by this spec.

If structural targets pass but timing is inconclusive, the verdict shall be:

```text
STRUCTURAL_PASS_PERFORMANCE_INCONCLUSIVE
```

## 21. Static source delta

Relative to the direct parent:

```text
ADD 4
MOD 6
DEL 0
```

Added:

```text
crates/base_train/src/bp_delta_k_runtime_mode_r1.rs
crates/base_train/src/bp_delta_k_evidence_epoch_r1.rs
crates/base_train/src/bp_delta_k_persistent_device_runtime_r1.rs
crates/base_train/src/bp_delta_k_perf_physical_receipt_r1.rs
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/bp_delta_k_fusion_fission_planner.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_bp_dk_device_post_update_reduction_exact_digest_compact_evidence_r1.rs
crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
crates/burn_webgpu_backend/src/bp_dk_device_post_update_r1.rs
```

## 22. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_PERF_R1_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 = 485c51c4227564dc7069d5efca8c1fcf97fd007b75876a080bb14d7df3e8e08d
entries = 8,419
```

Overlay artifact:

```text
ASH_PASS3_DK_PERF_R1_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 = ce78fbb71a7e02044e3ac293e9f48c12a379adfec0d17440216822799cc11f1b
entries = 10
```

Parent + overlay reproduces the full source tree byte-for-byte.

No `target`, `target_*`, `__pycache__`, `.pyc`, or `.pyo` entries are included.

## 23. Compile truth

The artifact-construction environment does not provide Cargo/Rustc.

Therefore this specification does not claim a post-bake Rust compile PASS.

Recommended first local gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

Compiler failures, if any, override this static source claim and must be corrected before physical qualification.

## 24. Non-goals after static bake

Not claimed:

```text
flattened gradient cosine is optimal
Gram compatibility is better
pair-only fusion is globally optimal
greedy matching is optimal
Delta-K thresholds are globally optimal
automatic threshold self-tuning is safe
```

These are algorithmic questions, not DK-PERF-R1 transport/lifetime questions.

## 25. Direct successor after physical closure

After DK-PERF-R1 physical PASS:

```text
DK-ALG-R2
Orientation-Aware Gram-Geometry Fusion Compatibility
vs Flattened Gradient Cosine
Same-Source Counterfactual Admission
```

Candidate comparison:

```text
Right: AA^T vs BB^T
Down:  A^T A vs B^T B
```

using the existing same-source counterfactual/objective evidence system.

## 26. Final law

> Delta-K mathematics is not the hotpath-performance problem being changed here.

> The observer must consume canonical resident resources rather than duplicating full model payloads when the canonical device source exists.

> Temporal state belongs to the optimizer generation transaction. Abort cannot advance local, bridge, or planner history.

> Normal production runtime identity and exact durable/audit content digest are separate authorities.

> Pipeline objects belong to the Device/session lifetime, not the parameter lifetime.

> Final DK-PERF-R1 physical promotion is forbidden until Disabled is truly zero-cost, parameter-local waits/spins are removed, steady-state pipeline construction is zero, normal full-payload SHA is zero, and topology decisions remain semantically identical.
