# ASH-BP-DELTA-K-PHYS-R2-CANONICAL-LOCAL-BRIDGE-EXTERNAL-ENCODER-CUTOVER-AGGREGATE-READBACK-PLANNER-BEFORE-MUON-POST-PENDING-SET-LEGACY-SYNC-RETIREMENT

## 0. Revision

```text
Short name:
DK-PERF-R1A1-R2A-PHYS-R2
```

Static token:

```text
PASS_ASH_BP_DELTA_K_PHYS_R2_CANONICAL_EXTERNAL_ENCODER_AGGREGATE_READBACK_FROZEN_PLAN_PENDING_SET_LEGACY_SYNC_RETIREMENT_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_PHYS_R2_CANONICAL_EXTERNAL_ENCODER_AGGREGATE_READBACK_FROZEN_PLAN_PENDING_SET_LEGACY_SYNC_RETIREMENT_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_PHYS_R2_CANONICAL_EXTERNAL_ENCODER_AGGREGATE_READBACK_FROZEN_PLAN_PENDING_SET_LEGACY_SYNC_RETIREMENT
```

## 1. Direct parent

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PHYS_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 8d066c370a3c8d5f92d37437a535b6561ca910d5ea76a326d6c1b3ed1846ba57
entries 8,445
```

The parent supplied tracked phase-submission aggregation, persistent aggregate WGPU readback backing, frozen-plan guards, and fail-closed physical debt accounting.

PHYS-R2 activates the Local/Bridge/planner portion of that physical path in the canonical scheduler.

## 2. Non-goals

No change to Delta-K = I * M^2, Local information/material mathematics, exact flattened 256D Bridge cosine, fusion/fission policy, cooldown/confirmation, Muon geometry, Newton-Schulz, R6 segmentation, counterfactual mathematics, or objective-probe mathematics.

## 3. Scheduler-before-Muon cutover

`production_multistep_loop_accumulation8_scheduler.rs` now prepares the complete Delta-K generation before entering the Muon parameter loop.

The scheduler builds canonical R6 segmented gradient inputs and calls:

```text
ProductionMuonRuntime::prepare_delta_k_generation_phys_r2(...)
```

before the first Muon parameter executes.

This is an active production callsite, not a receipt-only scaffold.

## 4. Canonical generation input

New:

```text
crates/base_train/src/bp_delta_k_phys_r2_generation.rs
```

It defines the canonical per-parameter preparation input and frozen prepared parameter context.

The input contains the canonical parameter identity, training provenance, R6 segmented gradient set, and source-weight identity.

No new full-gradient allocation is introduced.

## 5. Local external encoder cutover

The Local segmented observer now exposes:

```text
encode_segmented_phys_r2(...)
collect_segmented_phys_r2(...)
```

The encode method accepts externally owned generation command encoding / aggregate evidence backing and does not own the generation visibility boundary.

`prepare_delta_k_generation_phys_r2()` encodes all admitted Local parameter work first.

It then uses `BpDeltaKGenerationSubmissionAggregatePhys` and performs one final Local phase completion wait before decoding the Local generation.

## 6. Local aggregate readback activation

The persistent `TensorCubeBpDeltaKAggregateReadbackPhys` backing is now active for the Local production prepass.

A generation-level Local evidence directory assigns aligned slices for each canonical parameter.

The R2A Local batch ledger is updated through `observe_batched_generation(...)`, not `observe_legacy_parameter(...)`, on the new canonical prepass.

Static source claim:

```text
Local generation external-encoder path = ACTIVE
Local aggregate backing                = ACTIVE
Local generation wait authority        = ACTIVE
```

Legacy synchronous Local observer methods remain in source for fallback/qualification.

## 7. Bridge external encoder cutover

After Local generation decode, the prepass derives the exact Bridge pair set and encodes the segmented direct Bridge work using the external generation path.

The active Bridge backend exposes:

```text
encode_segmented_phys_r2(...)
collect_segmented_phys_r2(...)
```

and the generation prepass aggregates submissions and performs one final Bridge phase completion boundary.

## 8. Bridge aggregate readback activation

The persistent aggregate backing is active for Bridge physical receipts.

The Bridge batch ledger records the generation-batched route through `observe_batched_generation(...)`.

Zero-pair parameters do not manufacture synthetic synchronization work.

## 9. Prepared planner before Muon

After Local/Bridge collection, `prepare_delta_k_generation_phys_r2()` builds the actual fusion graph/planner result for each admitted parameter before the parameter Muon loop.

The prepared plan ledger is frozen and bound through the existing frozen-plan guard.

The physical runtime records the prepared plan as frozen before scheduler execution continues into Muon.

## 10. Frozen-plan Muon consumption

When `perf_r2a_phys_scheduler_cutover_active == true`, `execute_muon_parameter()` no longer runs the Local/Bridge/planner branch.

Instead it:

```text
looks up the frozen prepared plan
validates optimizer generation
validates canonical parameter identity
consumes the prepared parameter context
executes Muon from that frozen context
```

This is the active canonical path after the prepass.

The legacy inline observation/planner branch remains only under the explicit false branch.

## 11. No duplicate Local/Bridge observation on active cutover

The active scheduler-prepared branch requires matching graph/plan ledger entries and consumes the prepared parameter context exactly once.

It does not append a second planner result for the same canonical parameter.

## 12. R1A/R2A batch ledgers

The Local and Bridge generation batch ledgers now support explicit batched-generation observation:

```text
parameter_wait_count = 0
generation_wait_count <= 1
map_count <= 1
parameter_local_readback_buffer_create_count = 0
```

when the physical prepass is active.

These values describe the new prepass route and are not retroactively assigned to legacy fallback calls.

## 13. Prepared observation authority

The R2A prepared-generation observation authority is updated to distinguish the physical generation cutover from parameter-synchronous legacy debt.

The generation preparation records Local/Bridge/planner production at generation scope.

## 14. R2A-PHYS runtime

The physical runtime now contains explicit cutover recorders for:

```text
Local generation cutover
Bridge generation cutover
Post generation cutover
frozen-plan consumption
Disabled outer bypass
aggregate-readback cutover
```

The Local/Bridge preparation path activates the corresponding generation-cutover markers.

## 15. Post generation pending-set authority

New:

```text
crates/base_train/src/bp_delta_k_post_generation_pending_set_phys_r2.rs
```

The type owns a generation-scoped set of pending post-update parameters and enforces canonical parameter uniqueness / generation identity.

Backend and BaseTrain wrappers also expose a generation-tail completion API:

```text
wait_for_pending_generation_tail_phys_r2(...)
collect_parameter_after_generation_wait_phys_r2(...)
```

This is the required seam for a future one-tail-wait Post generation collect.

## 16. Post physical truth in this bake

The canonical active async Muon path still performs:

```text
submit post evidence
collect_parameter_after_exact_wait_r1a(...)
```

inside the parameter execution path.

The downstream post receipt is immediately consumed by counterfactual/evidence logic in the same parameter call, so simply deleting the wait would create a semantic/lifetime hole.

Therefore:

```text
Post pending-set type                     = MATERIALIZED
Post generation-tail collection seam      = MATERIALIZED
Post canonical pending-set route           = NOT YET CUT OVER
Post parameter exact-wait retirement       = HOLD
```

This is the sole major remaining PHYS-R2 synchronization blocker in this source bake.

## 17. Legacy synchronization truth

Source still contains legacy synchronous helper implementations for Local and Bridge, including `wait_for_submission_exact`, but the active scheduler-prepared Local/Bridge path uses the new `encode_segmented_phys_r2` / generation aggregate / `collect_segmented_phys_r2` route.

Static qualification must distinguish helper existence from canonical route invocation.

Post still has one canonical parameter exact-wait call and therefore prevents physical PASS.

## 18. Disabled route truth

The generation preparation function explicitly returns without opening the scheduler cutover when typed mode does not observe.

However full zero-incremental-cost Disabled admission remains physical qualification work because the entire outer scheduler route must be measured and verified.

No physical Disabled PASS is claimed by this bake.

## 19. Transport law

The active Local/Bridge prepass continues to use canonical R6 segmented gradient sets.

Required source properties preserved:

```text
Delta-K gradient H2D = 0
Delta-K duplicate full-gradient copy = 0
Delta-K full gradient D2H = 0
resident-weight H2D = 0 on canonical route
normal hotpath full-payload SHA = 0
```

Muon's packed-gradient representation remains a Muon cost, not a Delta-K gradient source.

## 20. Generation transaction

The generation-prepared Local/Bridge/planner state remains pending until the existing optimizer generation commit authority resolves the transaction.

Frozen prepared context is generation-bound and rejects generation/parameter drift.

Abort does not turn the prepared generation into successor-generation authority.

## 21. Current synchronization claim boundary

This static bake may claim:

```text
Local parameter-synchronous observation removed from active prepared path
Bridge parameter-synchronous observation removed from active prepared path
one prepared planner generation before Muon
frozen-plan Muon consumption active
Local generation aggregate backing active
Bridge generation aggregate backing active
```

It may NOT claim:

```text
Post parameter wait = 0
total Delta-K barriers <= 3
full R2A-PHYS physical PASS
physical semantic parity PASS
physical topology parity PASS
physical performance PASS
```

## 22. Source delta

Relative to direct PHYS parent:

```text
ADD 2
MOD 14
DEL 0
```

Added:

```text
crates/base_train/src/bp_delta_k_phys_r2_generation.rs
crates/base_train/src/bp_delta_k_post_generation_pending_set_phys_r2.rs
```

Modified:

```text
crates/base_train/src/bp_delta_k_bridge_generation_batch_r2a.rs
crates/base_train/src/bp_delta_k_local_generation_batch_r2a.rs
crates/base_train/src/bp_delta_k_parameter_pre_snapshot.rs
crates/base_train/src/bp_delta_k_post_generation_batch_r2a.rs
crates/base_train/src/bp_delta_k_prepared_generation_observation_r2a.rs
crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_bp_dk_device_post_update_reduction_exact_digest_compact_evidence_r1.rs
crates/burn_webgpu_backend/src/bp_delta_k_aggregate_readback_phys.rs
crates/burn_webgpu_backend/src/bp_delta_k_bridge_pair_observer.rs
crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
crates/burn_webgpu_backend/src/bp_dk_device_post_update_r1.rs
```

## 23. Code artifacts

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PHYS_R2_CANONICAL_CUTOVER_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 e1c6dc421146397d46973cb11330a8c5a7191c755683fca38510d6834a2b51a4
entries 8,447
```

Overlay:

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PHYS_R2_CANONICAL_CUTOVER_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 5ca4448607574698359b12fb9c377fa75f81c18ebf95c763d274bd4c161ab2d9
entries 16
```

Parent + overlay reproduces the full source tree byte-for-byte.

## 24. Compile truth

The bake environment does not provide Cargo/Rustc.

No post-bake Rust compile PASS is claimed.

Immediate gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

Compiler output overrides static source assumptions.

## 25. Immediate remaining physical slice

After compile PASS, the remaining physical completion is deliberately narrow:

```text
DK-PERF-R1A1-R2A-PHYS-R2P

Post Generation Pending-Set Production Cutover
+ Deferred Post Receipt Finalization
+ Counterfactual/Post-Evidence Continuation Split
+ Post Parameter Exact-Wait Retirement
+ <=3 Barrier Final Admission
```

This is not another Local/Bridge redesign.

Local/Bridge/planner scheduling is already cut over in this source bake.

## 26. Final law

> Local and Bridge observation now belong to the optimizer generation on the active prepared path.

> Their canonical segmented direct work is encoded before the Muon parameter loop and collected through generation-owned submission/readback authority.

> The planner is built and frozen before Muon parameter execution.

> Muon consumes prepared parameter context instead of reobserving/replanning.

> Post generation pending-set authority exists, but the canonical post receipt is still synchronously collected per parameter because downstream evidence currently consumes it immediately.

> Therefore physical PASS remains HOLD until Post receipt finalization is split from parameter Muon execution and collected at generation scope.

> No future Post cutover may regress the direct segmented gradient authority, frozen planner authority, generation transaction, or semantic/topology parity.
