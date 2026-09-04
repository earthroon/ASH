# ASH-BP-DELTA-K-GENERATION-SCOPED-BATCHED-EVIDENCE-EPOCH-ZERO-PER-PARAMETER-SYNCHRONIZATION-DISABLED-ZERO-COST-OUTER-BYPASS-R1A

## 0. Revision

```text
Patch ID:
ASH-BP-DELTA-K
-GENERATION-SCOPED-BATCHED-EVIDENCE-EPOCH
-ZERO-PER-PARAMETER-SYNCHRONIZATION
-DISABLED-ZERO-COST-OUTER-BYPASS
-R1A

Short name:
DK-PERF-R1A
```

Status at this source bake:

```text
R1 parent compile                         = REPORTED PASS BEFORE R1A BAKE
R1A static source materialization         = PARTIAL / ACTIVE
R1A post spin-drain retirement            = MATERIALIZED
R1A generation epoch authority            = MATERIALIZED
R1A batched arena capacity authority       = MATERIALIZED
R1A physical receipt authority             = MATERIALIZED
R1A local/bridge generation-wide batching  = HOLD
R1A Disabled true outer zero-cost bypass   = HOLD
R1A zero per-parameter synchronization     = HOLD
R1A Rust compile after this bake           = NOT CLAIMED BY BAKE ENVIRONMENT
R1A physical performance PASS              = HOLD
```

Static source token:

```text
PASS_ASH_BP_DELTA_K_GENERATION_SCOPED_BATCHED_EVIDENCE_EPOCH_ZERO_PARAMETER_SYNC_DISABLED_ZERO_COST_R1A_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_GENERATION_SCOPED_BATCHED_EVIDENCE_EPOCH_ZERO_PARAMETER_SYNC_DISABLED_ZERO_COST_R1A_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_GENERATION_SCOPED_BATCHED_EVIDENCE_EPOCH_ZERO_PARAMETER_SYNC_DISABLED_ZERO_COST_R1A
```

## 1. Direct parent

Direct parent source artifact:

```text
ASH_PASS3_DK_PERF_R1_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 = 485c51c4227564dc7069d5efca8c1fcf97fd007b75876a080bb14d7df3e8e08d
entries = 8,419
```

R1 established:

```text
typed Disabled / ObserveOnly / Active authority
resident weight direct-source seam
persistent post-evidence runtime
normal-hotpath full-payload SHA retirement mode
exact SHA audit-path preservation
local Delta-K candidate / commit / abort transaction
transactional local reinitialization
generation evidence epoch type
```

The parent `burn_webgpu_backend --all-targets` and `base_train --all-targets` compile gates were reported passing before this R1A bake.

This R1A source bake does not convert that parent report into a post-R1A compile claim.

## 2. Claim boundary

R1A is a synchronization/lifetime revision.

It does not modify:

```text
Delta-K = I * M^2
local I definition
local M definition
bridge flattened 256D cosine
bridge temporal information/material/Delta-K
fusion thresholds
fission thresholds
confirmation streaks
cooldown
pair ordering / greedy matching
Muon 16x16 / 16x32 / 32x16 geometry
Newton-Schulz coefficients
counterfactual mathematics
objective probe mathematics
```

The intended final change is:

```text
parameter-owned GPU/CPU synchronization
                ↓
generation-owned evidence synchronization
```

while preserving exact topology decisions.

## 3. Why the complete batch cutover is not forced in this bake

The live call graph reveals an important dependency:

```text
per-parameter gradient segments
        ↓
packed gradient producer
        ↓
local Delta-K observation
        ↓
local receipt freshness / ready endpoints
        ↓
bridge pair admission
        ↓
bridge observation
        ↓
planner
        ↓
Muon execution
```

The packed gradient is currently created and lifetime-owned inside `execute_muon_parameter`.

A true generation-wide local+bridge submission requires the packed-gradient authority itself to cross the parameter-call boundary, or requires an equivalent generation-scoped prepack phase.

R1A SHALL NOT duplicate the gradient payload or introduce a second gradient packing authority merely to claim batching.

Therefore the initial source bake materializes the generation authorities and retires the busy-spin path, while keeping local/bridge physical batch cutover on HOLD until gradient-pack lifetime is moved cleanly.

## 4. Absolute final R1A laws

Physical PASS still requires:

```text
local_parameter_wait_count  = 0
bridge_parameter_wait_count = 0
post_parameter_wait_count   = 0
poll_yield_count            = 0

Disabled local dispatch     = 0
Disabled bridge dispatch    = 0
Disabled post dispatch      = 0
Disabled Delta-K submit     = 0
Disabled Delta-K map        = 0
Disabled Delta-K H2D/D2H    = 0
Disabled graph/planner work = 0

canonical Delta-K weight H2D = 0
steady-state pipeline builds = 0
normal hotpath full SHA      = 0
semantic parity              = true
topology decision parity     = true
```

The current static bake intentionally does not claim those final laws as physically satisfied.

## 5. Pre-observation epoch authority

Added:

```text
crates/base_train/src/bp_delta_k_pre_observation_epoch_r1a.rs
```

State machine:

```text
CollectingSources
      ↓
Encoded
      ↓
Submitted
      ↓
Ready
      ↓
Decoded
      ↓
Planned
```

Any pre-final state may transition to `Aborted`.

The epoch records:

```text
optimizer generation
parameter count
tile count
pair count
local dispatch count
bridge dispatch count
submit count
map count
generation wait count
```

The live production runtime now owns an optional pre-observation epoch for the active optimizer generation whenever the typed Delta-K mode observes.

### Current static truth

```text
generation-scoped identity/count authority = ACTIVE
one encoder for all parameters             = NOT YET CUT OVER
one pre-observation submission             = NOT YET CUT OVER
one aggregate pre readback                 = NOT YET CUT OVER
```

## 6. Post-evidence epoch authority

Added:

```text
crates/base_train/src/bp_delta_k_post_evidence_epoch_r1a.rs
```

State machine:

```text
CollectingParameters
      ↓
Submitted
      ↓
Ready
      ↓
Decoded
      ↓
Consumed
```

Abort is explicitly represented.

The epoch records:

```text
parameter count
submit count
map count
exact wait count
spin wait count
poll yield count
```

This separates the final R1A requirement from the current transitional implementation: the current source can explicitly report that post spin has been retired while parameter-local exact waits still remain.

## 7. Batched evidence arena authority

Added:

```text
crates/base_train/src/bp_delta_k_batched_evidence_arena_r1a.rs
```

It owns bounded capacity/growth authority for future generation-level:

```text
local evidence bytes
bridge evidence bytes
post evidence bytes
```

The runtime now accumulates generation-local local/bridge/post evidence requirements and grows capacity geometrically instead of modeling every parameter as a fresh zero-capacity evidence world.

The arena records:

```text
local capacity bytes
bridge capacity bytes
post capacity bytes
local growth count
bridge growth count
post growth count
```

### Current static truth

The capacity authority is active.

The underlying WGPU local/bridge/post mapped buffers have not all been physically replaced by one generation arena yet.

Therefore `map_count = O(1)` is still a physical HOLD condition.

## 8. Production runtime integration

`ProductionBpDkRuntimeR8` now owns:

```text
perf_r1a_pre_epoch
perf_r1a_post_epoch
perf_r1a_arena
```

Epoch generation is bound to the same `optimizer_step` already used by:

```text
local pending temporal state
bridge pending temporal state
planner pending state
```

Generation regression is rejected.

When typed mode does not observe, R1A epoch authorities are not opened.

This does not yet constitute the final Disabled outer execution bypass because the legacy observation call graph itself still needs to be skipped above `execute_muon_parameter` Delta-K observation work.

## 9. Parameter-count and evidence-capacity accounting

After local receipt freshness and bridge pair planning, the active pre epoch records:

```text
+1 parameter
+tile_count
+admitted bridge pair count
```

The arena reserves cumulative compact evidence capacity using the existing ABI sizes:

```text
local compact evidence  = 48 bytes / tile
bridge compact evidence = 32 bytes / pair
```

After post-update semantic evidence is produced, post capacity is reserved from cumulative generation tile/pair counts plus bounded per-parameter control allowance.

These values are capacity authority, not a claim that the underlying physical readbacks have already been coalesced.

## 10. Post busy-spin retirement

The active-device Delta-K post evidence path previously used:

```rust
loop {
    match try_collect_parameter(...) {
        Some(value) => break value,
        None => std::thread::yield_now(),
    }
}
```

R1A removes that Delta-K-specific busy-spin loop.

Backend now exposes:

```text
wait_for_pending_submission_r1a
```

through the existing tracked-submission exact completion authority.

BaseTrain wrapper exposes:

```text
collect_parameter_after_exact_wait_r1a
```

The callsite performs:

```text
submit post evidence
        ↓
one exact tracked-submission completion wait
        ↓
one collect
```

No Delta-K post `yield_now()` loop remains at that callsite.

### Static claim

```text
post busy-spin loop                = RETIRED
post Delta-K poll-yield loop       = RETIRED
post per-parameter exact wait      = STILL PRESENT
post generation-wide batch         = NOT YET CUT OVER
```

Therefore the final R1A `post_parameter_wait_count = 0` law remains HOLD.

## 11. Existing non-Delta-K yield loop is not reclassified

The active asynchronous Muon pending-wave queue has its own progress `yield_now()` loop.

That loop is not Delta-K post-evidence collection and is outside the R1A poll-yield claim.

R1A telemetry SHALL distinguish Delta-K evidence synchronization from general MCU/Muon async queue progress.

## 12. Physical receipt authority

Added:

```text
crates/base_train/src/bp_delta_k_perf_r1a_physical_receipt.rs
```

Receipt covers:

```text
runtime mode
parameter/tile/pair counts
runtime construction count
local/bridge/post dispatch counts
pre/post submit counts
local/bridge/post parameter wait counts
pre/post generation wait counts
pre/post map counts
poll-yield count
weight/total H2D
D2H
graph node/edge counts
planner call count
steady pipeline builds
hotpath full-payload SHA count
semantic parity
topology decision parity
generation transaction continuity
physical claim state
```

`validate_physical_pass()` contains stricter Disabled-mode zero-work checks.

Bake constant:

```text
DK_PERF_R1A_PHYSICAL_QUALIFIED_AT_BAKE = false
```

## 13. Disabled final semantics

Final R1A requires the typed mode gate to sit above all Delta-K observation work:

```text
Disabled
  -> canonical local Muon execution
  -> no Delta-K runtime/evidence/graph/planner path

ObserveOnly
  -> Delta-K evidence/planner shadow
  -> physical topology remains local

Active
  -> Delta-K evidence/planner
  -> admitted physical topology mutation
```

### Current static truth

R1 typed mode and R1A epoch non-opening for Disabled exist.

The actual outer execution bypass before local observation remains uncut.

Therefore Disabled zero-cost remains explicit HOLD.

## 14. Local/bridge zero-wait successor work

The remaining physical R1A cutover SHALL split local and bridge observation into encode/collect phases whose submission ownership belongs to a generation coordinator.

It must not achieve batching by copying full gradients into a second generation-owned buffer authority if the existing packed-gradient producer can be promoted to the generation lifetime instead.

Preferred successor structure:

```text
generation gradient-pack lease set
       ↓
encode local observations for admitted parameters
       ↓
encode bridge observations when dependency can be represented without CPU barrier
       ↓
bounded submission epoch(s)
       ↓
aggregate compact readback
       ↓
one planner visibility boundary
```

If bridge readiness still requires local CPU receipt decode, a two-stage generation barrier is acceptable as an intermediate physical implementation:

```text
all local observations -> one generation wait
all bridge observations -> one generation wait
```

This is still O(1) in parameter count and satisfies the R1A architectural objective better than parameter-local barriers.

## 15. No semantic shortcut

R1A SHALL NOT pre-admit bridge pairs whose endpoints were not `VerifiedCurrent` merely to reduce synchronization unless equivalence is proven.

The current local warming/freshness semantics remain authoritative.

## 16. Transaction law

Inherited R1 local pending state remains candidate-only until optimizer generation commit.

Final R1A requires:

```text
local pending generation
== bridge pending generation
== planner pending generation
== optimizer generation
```

On abort:

```text
local pending   -> abort
bridge pending  -> abort
planner pending -> abort
R1A evidence epoch -> aborted
```

No committed observation authority advances.

## 17. Compile scope

Recommended immediate local gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

R1A does not require workspace-wide historical target compilation as part of its own claim boundary.

## 18. Semantic parity campaign

Parent R1 and R1A candidate must compare identical source state for:

```text
local information/material/Delta-K
bridge cosine/information/material/Delta-K
candidate graph
candidate ordering
fusion/fission plan
cooldown
confirmation state
```

Final physical requirement:

```text
semantic_parity = true
topology_decision_parity = true
```

## 19. Performance campaign

Measure separately:

```text
Disabled
ObserveOnly
Active normal hotpath
Active + explicit extended post evidence
counterfactual/objective qualification mode
```

Capture:

```text
local GPU time
bridge GPU time
pre collect time
planner CPU time
Muon GPU time
post evidence GPU time
post collect time
optimizer generation wall time
submit count
wait count
map count
H2D
D2H
pipeline builds
arena growth/reuse
```

Do not invent a mandatory speedup percentage.

## 20. Source delta

Relative to the direct R1 parent:

```text
ADD 4
MOD 4
DEL 0
```

Added:

```text
crates/base_train/src/bp_delta_k_batched_evidence_arena_r1a.rs
crates/base_train/src/bp_delta_k_perf_r1a_physical_receipt.rs
crates/base_train/src/bp_delta_k_post_evidence_epoch_r1a.rs
crates/base_train/src/bp_delta_k_pre_observation_epoch_r1a.rs
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_bp_dk_device_post_update_reduction_exact_digest_compact_evidence_r1.rs
crates/burn_webgpu_backend/src/bp_dk_device_post_update_r1.rs
```

## 21. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_PERF_R1A_GENERATION_EPOCH_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 = 98b2d2fc93c0ca05876245153735118c9948cdfe2b4ce2b8724b3d86978b2933
entries = 8,423
```

Overlay artifact:

```text
ASH_PASS3_DK_PERF_R1A_GENERATION_EPOCH_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 = 7f60397ea9f4a1326db1495e91a3ceafa16e1b7218827b84f2f42047ee4d954e
entries = 8
```

Parent + overlay reproduces the full source tree byte-for-byte.

No target/cache bytecode entries are included.

## 22. Static bake claims

This bake may claim:

```text
R1A typed pre-observation epoch authority materialized
R1A typed post-evidence epoch authority materialized
R1A batched evidence capacity authority materialized
R1A physical receipt authority materialized
R1A generation identity/count binding materialized
Delta-K post busy-spin/yield collection retired
existing R1 resident-source/SHA/transaction laws preserved
```

This bake SHALL NOT claim:

```text
Disabled zero-cost physical closure
local parameter wait retirement
bridge parameter wait retirement
post parameter exact-wait retirement
generation-wide WGPU command batching
aggregate physical mapped readback cutover
physical semantic parity
physical performance PASS
```

## 23. Direct successor inside R1A closure

Before algorithmic DK-ALG-R2, the remaining R1A physical cutover is:

```text
DK-PERF-R1A1
Generation-Lifetime Packed-Gradient Lease
+ Local/Bridge Encode-Collect Split
+ O(1) Generation Synchronization Closure
```

This is not a new algorithmic feature. It is the physical completion slice of R1A required because the live packed-gradient owner is currently parameter-scoped.

Only after R1A/R1A1 physical closure should ASH proceed to:

```text
DK-ALG-R2
Orientation-Aware Gram-Geometry Fusion Compatibility
vs Flattened Gradient Cosine
Same-Source Counterfactual Admission
```

## 24. Final law

> Delta-K evidence synchronization belongs to the optimizer generation, but the gradient authority must be moved cleanly before that synchronization can be honestly batched.

> R1A does not duplicate gradients merely to make a submit counter smaller.

> The post evidence busy-spin is retired immediately because it has no semantic value.

> Local/bridge parameter waits remain explicit HOLD until the packed-gradient lease can survive the parameter-call boundary.

> Disabled is not zero-cost until the mode gate physically bypasses local observation, bridge observation, graph construction, planner execution and post evidence before those owners are touched.

> Physical PASS is forbidden until the remaining parameter-proportional synchronization is reduced to bounded generation-level synchronization with exact topology parity.
