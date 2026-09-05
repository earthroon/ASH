# ASH-BP-DELTA-K-PREPARED-GENERATION-OBSERVATION-PLAN-LOCAL-ENCODE-COLLECT-BATCH-BRIDGE-ENCODE-COLLECT-BATCH-POST-AGGREGATE-COLLECTION-THREE-GENERATION-VISIBILITY-BARRIER-CLOSURE-R2A

## 0. Revision

```text
Short name:
DK-PERF-R1A1-R2A

Static source state:
PREPARED GENERATION AUTHORITY / DEBT ACCOUNTING = MATERIALIZED
LOCAL/BRIDGE/POST PHYSICAL BATCH CUTOVER         = HOLD
<=3 GENERATION VISIBILITY BARRIER PASS           = HOLD
PHYSICAL PERFORMANCE PASS                        = HOLD
```

Static token:

```text
PASS_ASH_BP_DELTA_K_PREPARED_GENERATION_OBSERVATION_PLAN_LOCAL_BRIDGE_BATCH_POST_AGGREGATE_THREE_BARRIER_R2A_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_PREPARED_GENERATION_OBSERVATION_PLAN_LOCAL_BRIDGE_BATCH_POST_AGGREGATE_THREE_BARRIER_R2A_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_PREPARED_GENERATION_OBSERVATION_PLAN_LOCAL_BRIDGE_BATCH_POST_AGGREGATE_THREE_BARRIER_R2A
```

## 1. Direct parent

```text
ASH_PASS3_DK_PERF_R1A1_R2_SEGMENTED_DIRECT_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 cb4b6befcca47b97d1556d1e803b2db6c1efff6f9623e087adec7eeeececeba9
entries 8,433
```

The parent already materializes canonical R6 segmented direct Local/Bridge observation and keeps the legacy parameter-synchronous wait path on physical HOLD.

R2A is the generation scheduling successor. It does not change the segmented gradient ABI or Delta-K/Muon mathematics.

## 2. Non-goals

R2A does not change:

```text
Delta-K = I * M^2
Local I / Local M
Bridge exact flattened 256D cosine
Bridge temporal Delta-K
fusion/fission thresholds
confirmation streaks
cooldown
greedy pair ordering
Muon 16x16 / 16x32 / 32x16 geometry
Newton-Schulz
R6 segmentation geometry
counterfactual mathematics
objective-probe mathematics
```

## 3. Final physical target retained

The intended physical R2A target remains:

```text
Local parameter waits  = 0
Bridge parameter waits = 0
Post parameter waits   = 0

Local generation visibility wait  <= 1
Bridge generation visibility wait <= 1
Post generation visibility wait   <= 1
```

Thus Delta-K CPU-visible synchronization must eventually be bounded by at most three generation-level visibility barriers independent of Muon parameter count.

This static bake does not claim that target is already reached.

## 4. Prepared generation observation authority

Added:

```text
crates/base_train/src/bp_delta_k_prepared_generation_observation_r2a.rs
```

`BpDeltaKPreparedGenerationObservationR2A` binds one optimizer generation and one typed `BpDeltaKRuntimeModeR1` to generation-wide Local/Bridge/Planner/Post observation accounting.

It records:

```text
Local parameter count
Local tile count
Bridge parameter count
Bridge pair count
Planner parameter count
Post parameter count
legacy parameter-local wait count
```

The legacy-wait counter is deliberate: until the backend encode/collect cutover lands, parameter-local synchronization cannot disappear behind a new generation-level type.

## 5. Prepared generation plan ledger

Added:

```text
crates/base_train/src/bp_delta_k_prepared_generation_plan_r2a.rs
```

`BpDeltaKPreparedGenerationPlanR2A` collects the actual `AshBpDkFusionExecutionPlan` produced for each canonical parameter and sorts them by canonical parameter index.

At generation commit it freezes the collected plan set into a generation plan digest.

Current static truth:

```text
plan ledger is production-populated = YES
plan set is generation-frozen        = YES, at generation commit
Muon parameter loop consumes frozen generation plan before execution = NO
```

Therefore the final planner-before-Muon cutover remains HOLD.

## 6. Local generation batch debt ledger

Added:

```text
crates/base_train/src/bp_delta_k_local_generation_batch_r2a.rs
```

The current parameter-synchronous Local direct route records one legacy submit/wait/map/readback-buffer debt per observed parameter.

This makes the parent synchronization shape explicit in runtime state and provides the future physical receipt source for proving retirement rather than inferring it from source text.

## 7. Bridge generation batch debt ledger

Added:

```text
crates/base_train/src/bp_delta_k_bridge_generation_batch_r2a.rs
```

For each parameter with admitted Bridge pairs, the current legacy direct route records one parameter-local submit/wait/map/readback-buffer debt.

Zero-pair parameters record no Bridge synchronization debt.

## 8. Post generation batch debt ledger

Added:

```text
crates/base_train/src/bp_delta_k_post_generation_batch_r2a.rs
```

The current post-evidence route records the remaining exact-wait/map debt per parameter.

R1A busy-spin/yield retirement remains preserved; this ledger does not reintroduce polling spin.

## 9. Production runtime binding

`ProductionBpDkRuntimeR8` now owns:

```text
perf_r2a_prepared_observation
perf_r2a_prepared_plan
perf_r2a_local_batch
perf_r2a_bridge_batch
perf_r2a_post_batch
```

For ObserveOnly/Active, these authorities are opened for the active optimizer generation alongside the R1A/R1A1/R2 generation authorities.

For typed Disabled, they are not materialized.

This is runtime-authority binding, not yet the complete Disabled outer execution bypass: legacy Local/Bridge work still exists below the current callsite and remains a physical HOLD.

## 10. Current production instrumentation points

The active parameter route now records:

```text
Local observation completion
Bridge evidence completion
planner parameter plan production
Post evidence collection
```

into the R2A generation authorities.

The planner plan recorded is the exact plan already used by the existing path, so this bake adds no alternate planner semantics.

## 11. Generation transaction binding

At optimizer generation commit:

```text
R2A collected parameter plans -> frozen generation digest
R2A prepared observation       -> Committed
```

At optimizer generation abort:

```text
R2A prepared observation -> Aborted
```

The existing Local/Bridge/planner generation transaction remains authoritative for mathematical state. R2A adds scheduling lineage; it does not create a second Delta-K temporal state authority.

## 12. Physical receipt authority

Added:

```text
crates/base_train/src/bp_delta_k_perf_r2a_physical_receipt.rs
```

`BpDeltaKPerfR2APhysicalReceipt::validate_physical_pass()` requires:

```text
semantic parity = true
topology parity = true
generation transaction continuity = true
canonical direct coverage = all admitted parameters
legacy packed fallback = 0
Local parameter waits = 0
Bridge parameter waits = 0
Post parameter waits = 0
Local generation waits <= 1
Bridge generation waits <= 1
Post generation waits <= 1
Local/Bridge/Post maps <= 1 each
poll/yield = 0
planner call count = 1
prepared plan build count = 1
stale prepared plan accept count = 0
gradient/weight H2D = 0
duplicate gradient copy = 0
full gradient/candidate D2H = 0
steady-state pipeline builds = 0
normal hotpath full-payload SHA = 0
```

`DK_PERF_R2A_PHYSICAL_QUALIFIED_AT_BAKE = false`.

## 13. Current source-observed physical debt

Static inspection after this bake still finds:

```text
Local observer wait_for_submission_exact occurrences  = 2
Bridge observer wait_for_submission_exact occurrences = 2
Post collect_parameter_after_exact_wait_r1a call       = 1
```

These include legacy and segmented-direct observer paths.

Therefore this bake explicitly does NOT claim parameter-wait retirement or <=3-barrier physical closure.

## 14. Why the waits are not patched superficially

Removing the wait call alone is insufficient. Correct generation batching requires:

```text
external generation command-encoder ownership
submission lease aggregation
resource lifetime retention across the batch
aggregate readback backing
canonical decode ordering
planner publication only after full Local/Bridge visibility
Post source lease retention until generation Post collection
```

R2A does not replace an exact wait with an unsafe asynchronous lifetime gap merely to reduce a counter.

## 15. Required physical successor cut

The next source cut inside R2A must physically split backend observers into encode and collect phases:

```text
Local segmented direct:
    encode parameter work into generation encoder
    no submit/wait/map inside parameter observer

Bridge segmented direct:
    encode admitted pairs into generation encoder
    no submit/wait/map inside parameter observer

Post:
    register/encode parameter evidence
    no exact parameter wait
```

Generation owners then submit and collect each phase with bounded visibility barriers.

## 16. Planner cutover requirement

The prepared plan ledger in this bake is evidence-only until the scheduler order becomes:

```text
prepare all Local
collect Local
prepare all Bridge
collect Bridge
build/freeze generation planner
execute Muon parameter loop using frozen plan only
aggregate Post
```

Physical PASS is forbidden while `execute_muon_parameter()` still performs Local/Bridge/planner work parameter-by-parameter.

## 17. Disabled zero-cost target

The typed R2A authorities are not created in Disabled mode, but true Disabled physical PASS additionally requires that the outer call graph bypass Local/Bridge/graph/planner/Post work before those owners are touched.

Until that outer bypass is physically cut over, Disabled zero-cost remains HOLD.

## 18. R2 direct-source law preserved

This bake does not modify the R2 direct segmented shaders or source binding.

Canonical target remains:

```text
Delta-K gradient H2D = 0
Delta-K duplicate gradient copy = 0
Delta-K full gradient D2H = 0
Delta-K weight H2D = 0 on resident-weight route
```

Muon packing remains separately accounted.

## 19. Hotpath digest law preserved

Normal-hotpath full-payload SHA remains retired. Exact SHA remains an explicit audit/counterfactual qualification path.

## 20. Pipeline lifetime law preserved

No new GPU shader/BGL/pipeline owner is introduced in this bake. Persistent Device/session pipeline authority remains unchanged.

## 21. Static source delta

Relative to the direct R2 parent:

```text
ADD 6
MOD 2
DEL 0
```

Added:

```text
crates/base_train/src/bp_delta_k_prepared_generation_observation_r2a.rs
crates/base_train/src/bp_delta_k_prepared_generation_plan_r2a.rs
crates/base_train/src/bp_delta_k_local_generation_batch_r2a.rs
crates/base_train/src/bp_delta_k_bridge_generation_batch_r2a.rs
crates/base_train/src/bp_delta_k_post_generation_batch_r2a.rs
crates/base_train/src/bp_delta_k_perf_r2a_physical_receipt.rs
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
```

No WGSL, Delta-K equation, fusion threshold, Muon math, WGPU generation, Burn/CubeCL vendor file or Adam authority file is changed.

## 22. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PREPARED_GENERATION_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 5dbee0241d42748220b0565efb7f2dd7b3b77ed5146a56544b87ec36b6f73cfb
entries 8,439
```

Overlay artifact:

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PREPARED_GENERATION_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 553cc3ffd7d4d952a40d194d3704f12df3d26170c63193080948261c5c1517d2
entries 8
```

Parent + overlay reproduces the full 8,439-file tree byte-for-byte.

## 23. Compile truth

The artifact-construction environment has no Cargo/Rustc.

Post-bake compile PASS is not claimed.

Immediate local gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

Compiler output overrides static source assumptions.

## 24. Static bake claim

This bake may claim:

```text
prepared-generation observation authority materialized
prepared-generation plan ledger materialized and production-populated
Local/Bridge/Post generation debt ledgers materialized and production-populated
R2A generation commit/abort lineage materialized
R2A physical receipt authority materialized
R2 segmented-direct source preserved
legacy wait debt explicitly observable
```

This bake SHALL NOT claim:

```text
Local encode/collect physical split
Bridge encode/collect physical split
Post aggregate physical collection
planner-before-Muon execution cutover
frozen prepared-plan consumption by Muon
parameter-wait retirement
<=3 generation visibility barriers
Disabled zero-cost physical closure
physical semantic/topology parity
physical performance PASS
```

## 25. Direct physical completion slice

The next implementation slice is not a new algorithm revision. It is the physical completion of R2A:

```text
DK-PERF-R1A1-R2A-PHYS
External Generation Encoder Ownership
+ Submission-Lease Aggregation
+ Aggregate Readback Backing
+ Frozen-Plan Muon Consumption
+ Local/Bridge/Post Parameter-Wait Retirement
```

Only after that physical closure should ASH proceed to the algorithmic `DK-ALG-R2` Gram-geometry sensor comparison.

## 26. Final law

> R2A introduces one generation scheduling authority, not a second Delta-K mathematical authority.

> The current parameter-synchronous path is instrumented so its remaining waits cannot be hidden.

> The prepared generation plan is collected from the exact production planner output and frozen at the generation transaction boundary.

> Physical R2A PASS remains forbidden until the planner is actually prepared before Muon execution, Local/Bridge/Post no longer own parameter-local waits/maps, and the canonical path requires at most three generation-level visibility barriers.
