# ASH-BP-DELTA-K-R2A-PHYSICAL-EXTERNAL-ENCODER-AGGREGATE-READBACK-FROZEN-PLAN-PARAMETER-WAIT-RETIREMENT

## 0. Revision

```text
Short name:
DK-PERF-R1A1-R2A-PHYS

Patch ID:
ASH-BP-DELTA-K-R2A-PHYSICAL-EXTERNAL-ENCODER-AGGREGATE-READBACK-FROZEN-PLAN-PARAMETER-WAIT-RETIREMENT
```

Static token:

```text
PASS_ASH_BP_DELTA_K_R2A_PHYSICAL_EXTERNAL_ENCODER_AGGREGATE_READBACK_FROZEN_PLAN_PARAMETER_WAIT_RETIREMENT_STATIC
```

Physical HOLD:

```text
HOLD_ASH_BP_DELTA_K_R2A_PHYSICAL_EXTERNAL_ENCODER_AGGREGATE_READBACK_FROZEN_PLAN_PARAMETER_WAIT_RETIREMENT_PENDING
```

Reserved physical PASS:

```text
PASS_ASH_BP_DELTA_K_R2A_PHYSICAL_EXTERNAL_ENCODER_AGGREGATE_READBACK_FROZEN_PLAN_PARAMETER_WAIT_RETIREMENT
```

## 1. Direct parent

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PREPARED_GENERATION_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 5dbee0241d42748220b0565efb7f2dd7b3b77ed5146a56544b87ec36b6f73cfb
entries 8,439
```

The parent already contains R6 canonical segmented direct Local/Bridge observation and R2A prepared-generation/debt ledgers.

This PHYS revision materializes the physical primitives and fail-closed receipt authority required for the final generation scheduler cutover.

## 2. Mathematical non-goal

No Delta-K or Muon mathematics changes in this bake.

Unchanged:

```text
Delta-K = I * M^2
Local row-sketch / I / M
Bridge exact flattened 256D cosine
Bridge temporal Delta-K
fusion/fission thresholds
confirmation / cooldown
greedy pair ordering
Muon rectangular geometry
Newton-Schulz
R6 segmented gradient geometry
counterfactual/objective mathematics
```

## 3. External phase submission aggregation primitive

Added backend module:

```text
crates/burn_webgpu_backend/src/bp_delta_k_generation_submission_aggregate_phys.rs
```

`BpDeltaKGenerationSubmissionAggregatePhys` is an actual tracked-submission aggregation primitive for Local, Bridge and Post generation phases.

It enforces:

```text
one Device authority per phase
one Queue authority per phase
strictly increasing tracked submission ordinals
no submission after phase wait
no release before final phase visibility
```

`wait_for_phase_completion()` waits only for the final tracked submission. Queue ordering makes that one final completion boundary cover all prior submissions in the same phase/queue domain.

`release_all()` then retires every tracked submission lease only after phase completion.

This is the physical primitive needed to reduce CPU-visible phase synchronization from parameter-proportional waits to one bounded phase wait.

## 4. Persistent aggregate WGPU readback backing primitive

Added backend module:

```text
crates/burn_webgpu_backend/src/bp_delta_k_aggregate_readback_phys.rs
```

`TensorCubeBpDeltaKAggregateReadbackPhys` owns one persistent-capacity pair:

```text
STORAGE | COPY_SRC | COPY_DST
+
COPY_DST | MAP_READ
```

Capacity grows geometrically and remains reusable after warmup.

The primitive exposes physical storage/readback buffer authorities and growth telemetry without introducing a gradient/weight copy authority.

## 5. BaseTrain physical aggregate directory

Added:

```text
crates/base_train/src/bp_delta_k_r2a_phys_aggregate_readback.rs
```

It materializes canonical generation slice directories for Local/Bridge/Post aggregate evidence.

Each slice binds:

```text
canonical parameter ordinal
logical item begin/count
aligned physical byte offset
semantic byte length
```

Physical padding is not semantic evidence.

## 6. Frozen-plan consumption authority

Added:

```text
crates/base_train/src/bp_delta_k_r2a_phys_frozen_plan.rs
```

`BpDeltaKFrozenPlanConsumptionPhys` rejects:

```text
unfrozen plan binding
empty plan digest
cross-generation plan consumption
missing parameter plan
```

The authority is ready for the scheduler cutover where Muon parameters consume one generation-frozen plan instead of planning inline.

## 7. Physical closure runtime

Added:

```text
crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs
```

`BpDeltaKR2APhysicalClosureRuntime` is now physically owned by `ProductionBpDkRuntimeR8` and participates in optimizer generation begin/commit/abort.

It records the exact remaining production debt:

```text
legacy parameter-synchronous Local count
legacy parameter-synchronous Bridge count
legacy parameter-synchronous Post count
Local/Bridge/Post parameter wait count
Local/Bridge/Post map count
parameter-local readback-buffer count
inline parameter planner count
prepared-plan build/consume count
```

It also records final cutover booleans:

```text
external_generation_encoder_production_cutover
aggregate_readback_production_cutover
frozen_plan_muon_consumption_cutover
disabled_outer_bypass_cutover
```

## 8. Active runtime debt instrumentation

The current production callsite now explicitly records PHYS debt at the points where the legacy path still executes:

```text
Local parameter observation
Bridge parameter observation
inline parameter planner
Post parameter exact-wait collection
```

This makes it impossible for a future receipt to claim physical closure while the old route remains active.

## 9. Generation transaction integration

For observing modes, PHYS runtime opens with the current optimizer generation.

At generation commit:

```text
R2A prepared plan freezes
PHYS prepared-plan build event is recorded
PHYS generation resolves Commit
```

At generation abort:

```text
PHYS generation resolves Abort
```

The existing Local/Bridge/planner temporal transaction remains the mathematical authority; PHYS adds scheduling/transport closure authority only.

## 10. Definitive physical receipt authority

Added:

```text
crates/base_train/src/bp_delta_k_r2a_phys_receipt.rs
```

`BpDeltaKR2APhysicalClosureReceipt` reports the active physical route and refuses physical PASS unless all of the following are true:

```text
legacy Local sync count = 0
legacy Bridge sync count = 0
legacy Post sync count = 0

Local parameter waits = 0
Bridge parameter waits = 0
Post parameter waits = 0

Local generation waits <= 1
Bridge generation waits <= 1
Post generation waits <= 1

Local maps <= 1
Bridge maps <= 1
Post maps <= 1

inline parameter planner count = 0

external generation encoder cutover = true
aggregate readback cutover = true
frozen-plan Muon consumption cutover = true
Disabled outer bypass cutover = true
```

`DK_PERF_R2A_PHYS_PHYSICAL_QUALIFIED_AT_BAKE = false`.

## 11. Public receipt projection

`ProductionMuonRuntime` exposes:

```text
bp_delta_k_r2a_phys_receipt()
```

for local qualification tooling without granting mutation authority over the physical closure runtime.

## 12. Current static source truth after this bake

Materialized now:

```text
backend tracked-submission phase aggregate primitive
backend persistent aggregate WGPU readback primitive
BaseTrain aggregate readback directory authority
frozen prepared-plan consumption guard
PHYS runtime bound to ProductionBpDkRuntimeR8
PHYS generation begin/commit/abort binding
active legacy synchronization debt accounting
definitive fail-closed PHYS receipt
```

Still HOLD:

```text
canonical Local external-encoder callsite cutover
canonical Bridge external-encoder callsite cutover
canonical Post aggregate collection cutover
actual aggregate readback use by Local/Bridge/Post
Muon parameter consumption of frozen plan
planner-before-Muon scheduler cutover
Disabled true outer bypass
parameter-local wait retirement
<=3 physical visibility barrier admission
```

## 13. Static evidence that HOLD remains real

After this bake the source still contains parameter-synchronous production mechanisms:

```text
Local observer wait_for_submission_exact callsites  = 2
Bridge observer wait_for_submission_exact callsites = 2
Post collect_parameter_after_exact_wait_r1a hotpath = 1
```

These include legacy/segmented observer paths and prevent R2A-PHYS physical PASS.

No source token in this bake may represent those waits as retired.

## 14. Why the waits are not simply deleted

Deleting a wait without moving ownership would create lifetime and visibility holes.

Correct physical cutover must simultaneously move:

```text
command encoder ownership
submission lease ownership
aggregate readback backing
map completion ownership
canonical evidence decode ordering
planner publication boundary
Post source-resource lifetime
```

from the parameter to the optimizer generation.

This bake supplies those primitive/receipt authorities before changing the production scheduler.

## 15. Final physical scheduler order

The remaining canonical cutover must become:

```text
R6 finalized gradient publication

if Delta-K observes:
    encode all Local direct observations
    submit Local phase batches
    one Local visibility boundary
    aggregate Local decode

    derive Bridge admissions
    encode all Bridge direct observations
    submit Bridge phase batches
    one Bridge visibility boundary
    aggregate Bridge decode

    build/freeze one generation planner

execute Muon parameter loop from frozen generation plan only

if Delta-K observes:
    encode/register Post evidence for all parameters
    submit Post phase batches
    one Post visibility boundary
    aggregate Post decode

optimizer generation commit/abort
```

## 16. Absolute final synchronization law

Physical promotion requires:

```text
Local parameter wait count  = 0
Bridge parameter wait count = 0
Post parameter wait count   = 0

Local generation waits  <= 1
Bridge generation waits <= 1
Post generation waits   <= 1
```

Thus:

```text
total CPU-visible Delta-K barriers <= 3 / optimizer generation
```

independent of the number of Muon parameters.

## 17. Transport laws retained

Canonical path must continue to satisfy:

```text
Delta-K gradient H2D = 0
Delta-K duplicate gradient D2D copy = 0
Delta-K full gradient D2H = 0
Delta-K resident weight H2D = 0
Delta-K full candidate D2H = 0
normal hotpath full-payload SHA = 0
```

No generation batching implementation may create a second full gradient/weight authority.

## 18. Frozen-plan law

Final PHYS cutover requires:

```text
planner freeze happens before first Muon parameter execution
planner call count = 1 / observing generation
execute_muon_parameter performs no Local/Bridge observation
execute_muon_parameter performs no planner call
all Muon parameters consume matching frozen plan entries
stale prepared-plan accepts = 0
```

## 19. Disabled law

Physical Disabled PASS requires zero incremental Delta-K work:

```text
prepared generation = 0
Local/Bridge/Post dispatch = 0
Delta-K submits/waits/maps = 0
graph/planner work = 0
Delta-K H2D/D2H = 0
```

Canonical Muon cost is not classified as Delta-K overhead.

## 20. Source delta

Relative to direct R2A parent:

```text
ADD 6
MOD 3
DEL 0
```

Added:

```text
crates/base_train/src/bp_delta_k_r2a_phys_aggregate_readback.rs
crates/base_train/src/bp_delta_k_r2a_phys_frozen_plan.rs
crates/base_train/src/bp_delta_k_r2a_phys_receipt.rs
crates/base_train/src/bp_delta_k_r2a_phys_runtime.rs
crates/burn_webgpu_backend/src/bp_delta_k_aggregate_readback_phys.rs
crates/burn_webgpu_backend/src/bp_delta_k_generation_submission_aggregate_phys.rs
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/burn_webgpu_backend/src/lib.rs
```

## 21. Code artifacts

Full code-only artifact:

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PHYS_STATIC_SOURCE_BAKE_CODE_ONLY.zip
SHA-256 8d066c370a3c8d5f92d37437a535b6561ca910d5ea76a326d6c1b3ed1846ba57
entries 8,445
```

Overlay artifact:

```text
ASH_PASS3_DK_PERF_R1A1_R2A_PHYS_STATIC_SOURCE_BAKE_OVERLAY.zip
SHA-256 58b9774e5220f9004417109dab89afc4dd695f7eb46f962ea1f34bc348c21952
entries 9
```

Parent + overlay reproduces the full source tree byte-for-byte.

## 22. Compile truth

The artifact-construction environment does not provide Cargo/Rustc.

Therefore post-bake compile PASS is not claimed.

Immediate local gates:

```powershell
cargo check --locked -p burn_webgpu_backend --all-targets
cargo check --locked -p base_train --all-targets
```

Compiler output overrides static assumptions.

## 23. Next physical cut inside the same closure

After compile PASS, the remaining source cut is:

```text
DK-PERF-R1A1-R2A-PHYS-R2

Canonical Local/Bridge External Encoder Cutover
+ Aggregate Physical Readback Activation
+ Planner-Before-Muon Scheduler Cutover
+ Post Generation Pending-Set Collection
+ Legacy Sync Route Retirement
```

This is a physical completion slice, not a new algorithm revision.

## 24. Final law

> R2A-PHYS does not call a primitive "active" until the canonical production route uses it.

> Submission aggregation waits only on the final tracked submission of one Queue-ordered phase.

> Aggregate readback memory belongs to persistent runtime capacity, not parameter function lifetime.

> Frozen plans belong to the optimizer generation and may never be reconstructed inside a Muon parameter fallback.

> The current legacy parameter waits remain explicit blockers and are counted at the exact active callsites.

> Physical PASS is forbidden until Local, Bridge and Post all move to generation-owned submission/readback, Muon consumes the frozen plan, Disabled performs zero Delta-K work, and total CPU-visible Delta-K synchronization is at most three generation barriers.
