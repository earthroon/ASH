# ASH-TRAINABLE-SESSION-ACTIVE-PRODUCTION-OWNER-AND-CROSS-INVOCATION-RUNTIME-CUTOVER-R4

## 0. Revision

```text
Patch ID:
ASH-TRAINABLE-SESSION
-ACTIVE-PRODUCTION-OWNER
-AND-CROSS-INVOCATION-RUNTIME-CUTOVER-R4

Short name:
ASH TRAINABLE SESSION R4
ACTIVE PRODUCTION OWNER + CROSS-INVOCATION RUNTIME CUTOVER

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:                 NOT CLAIMED
GPU physical PASS:                 NOT CLAIMED
cross-invocation persistence PASS: NOT CLAIMED
crash/reopen PASS:                 NOT CLAIMED
```

Static token:

```text
PASS_ASH_TRAINABLE_SESSION_ACTIVE_PRODUCTION_OWNER_AND_CROSS_INVOCATION_RUNTIME_CUTOVER_R4_STATIC
```

Physical state:

```text
HOLD_ASH_TRAINABLE_SESSION_R4_PHYSICAL_PENDING
```

## 1. Direct Parents

R4 consumes without redefining:

```text
Eve R3G persistent authority instance and live Adam authority
MCU SESSION R7 persistent execution fabric
MCU R7A device kernel cache and bounded arena
R3C/R3C1 atomic full TrainableGeneration commit
R3D Adam durability
R3E Weight durability
R3F HiMuon momentum durability
RAM36 process-budget authority
```

R4 changes production runtime ownership, not optimizer mathematics.

## 2. Problem Closed

Before R4, `TrainableSessionRuntimeR3G` and `TrainableSessionRuntimeR7` existed as architecture ABIs, but the active R6 production caller still entered a large invocation that owned live Adam, resident Weight, ProductionMuonRuntime and MCU-related lifetime locally.

R4 creates an explicit production owner outside the R6 invocation and adds a cross-invocation parking/restoration boundary for the concrete live runtime.

## 3. Core Law

> A generation belongs to a transaction. An execution invocation belongs to a trainable session. Live Adam, resident Weight, ProductionMuonRuntime, MCU execution state and their RAM reservations are not reconstructed merely because an invocation returns.

And:

> Durable state is recovery authority. It is not the normal transport between two live invocations of one R4 session.

## 4. Active Production Owner

Materialized:

```rust
pub struct TrainableSessionRuntimeR4
```

with typed lifecycle:

```rust
TrainableSessionPhaseR4::{
    Opening,
    Open,
    InvocationActive,
    Closing,
    Closed,
    Poisoned,
}
```

The production pipeline constructs `TrainableSessionRuntimeR4::open_active_production_owner()` outside the R6 invocation and passes `&mut TrainableSessionRuntimeR4` to the R4 execution entry.

The historical no-session R6 entry fails closed when R4 active-owner admission is enabled.

## 5. Invocation ABI

Materialized entry:

```rust
execute_r6_production_invocation_r4(
    session: &mut TrainableSessionRuntimeR4,
    ...,
    exit: TrainableInvocationExitR4,
)
```

Exit ABI:

```rust
TrainableInvocationExitR4::{
    KeepResident,
    DurableCheckpointKeepResident,
    CloseAfterDurableWriteback,
}
```

Only one mutable invocation may be active on one R4 session.

Invocation ordinals use checked monotonic increment and are never reused.

## 6. First Materialization Boundary

The current static cutover deliberately avoids a large pre-loop extraction of the existing 5k-line R6 setup path.

Therefore the first R4 invocation may perform the existing one-time live runtime materialization. R4 records this as first materialization, not reconstruction.

After that invocation, a KeepResident-class exit moves the concrete live runtime into the outer R4 owner.

A later invocation restores that exact runtime rather than hydrating/loading it again.

This source structure is intentionally conservative and does not claim multi-invocation physical PASS until an actual campaign exercises the restore branch.

## 7. Parked Runtime Authority

Materialized:

```rust
pub struct TrainableSessionParkedRuntimeR4
```

It owns the live resources required for invocation-to-invocation continuation, including:

```text
HostProcessRamBudget
BaseTrainRamInventoryAuthority
dataset RAM36 reservation identity

ResidentWeightPack
resident Weight reservation
initial Weight load/replay evidence
resident Weight projection counters and cumulative residency counters

RamResidentAdamMv
Adam M/V resident reservations
Adam candidate reservations
OptimizerPcieTransferRing

ProductionMuonRuntime
HiMuon momentum RAM36 reservation

TrainableSessionRootGuardR3G
EveLeaseSequencerR3G
```

No second canonical Adam M/V or Weight body is created to achieve persistence.

## 8. Restore Path

On successor invocation R4 restores parked state before one-time live materialization paths.

Required restore checks include:

```text
ResidentWeightPack generation == durable/current source generation
ResidentWeightPack optimizer step == current optimizer generation

RamResidentAdamMv committed training generation == current source generation
RamResidentAdamMv committed optimizer generation == current optimizer generation

R3G root guard remains present
R3G authority remains bound to resident Adam
Eve lease sequencer continues rather than restarting
```

Generation drift fails closed.

## 9. Eve R3/R3G Continuity

On restored runtime:

```text
Eve mutable R3 adoption is not repeated
R3G authority journal allocation is not repeated
R3G authority instance is not rebound
R3G root guard is not reacquired
Eve lease ordinal sequence is not reset
```

The existing MCU R7 session is rebound only to verify the same R3G authority identity. Its bind operation rejects identity drift.

## 10. HiMuon Continuity

`ProductionMuonRuntime` becomes a parked/restored session resource.

On restored R4 runtime:

```text
ProductionMuonRuntime::load_or_initialize... is not called
HiMuon momentum RAM reservation is not reacquired
D10 runtime admission environment lookup is not repeated
```

The existing D10 admission receipt is republished into the fresh invocation output directory from the retained runtime authority.

The route-sparse Adam overlay and packed-canonical bridge are not rematerialized on a restored invocation.

## 11. MCU Continuity

Because `ProductionMuonRuntime` itself survives, its R7 `McuSessionRuntimeR7` and R7A persistent executor/resource bindings survive the invocation boundary.

R4 does not yet physically extract every R6/R7/R8/R8A child field from `ProductionMuonRuntime`; that remains R7B scope.

## 12. Weight Continuity

When KeepResident is selected, the final resident Weight pack and its RAM36 reservation are retained instead of dropped/released.

The resident Weight's current generation is validated against the next invocation source before use.

Historical R3E replay/keyframe durability remains recovery authority and is not used as live cross-invocation transport.

## 13. RAM36 Continuity

For a KeepResident-class exit, R4 does not finalize/release the session RAM36 budget or exact inventory.

The following remain live in the parked runtime:

```text
Adam resident reservations
Adam candidate reservations where admitted
resident Weight reservation
HiMuon momentum reservation
session process-budget authority
exact RAM inventory authority
```

The final close path retains historical finalization/release behavior.

## 14. Invocation Boundary

R4 parks the runtime only after the existing R6 generation loop and generation commit/finalization path has completed.

The current source does not introduce a half-generation return path.

R3C/R3C1 remain the full TrainableGeneration commit authority.

## 15. Production Pipeline Cutover

The active pipeline now performs:

```text
create TrainableSessionRuntimeR4 outside R6 invocation
        ↓
execute_r6_production_invocation_r4(...)
```

When R4 is disabled the historical `execute_r6_production_multistep_loop_with_native_witness` compatibility branch remains.

The current top-level pipeline uses `CloseAfterDurableWriteback` for its existing one-shot production flow so legacy external behavior is preserved. Multi-invocation callers may select a KeepResident exit and call the same R4 entry again on the same session.

This distinction is why cross-invocation physical PASS remains HOLD.

## 16. Configuration

New BaseTrainingRuntimeConfig fields:

```text
admit_trainable_session_active_production_owner_r4
admit_trainable_session_cross_invocation_runtime_r4
```

Defaults are OFF.

Cross-invocation admission requires active-owner admission.

The full cross-invocation path requires the existing R3G, resident Adam, resident Weight, ProductionMuonRuntime, MCU R7 and R3C1 parents.

## 17. No Silent Fallback

R4 fails closed on conditions including:

```text
legacy no-session entry reached while R4 active
second active invocation
invocation ordinal overflow
restored Weight generation drift
restored Adam generation drift
R3G guard/authority split restoration
restored Muon runtime without its parent admission
KeepResident without a complete runtime bundle
double park
close with live parked runtime through the wrong close surface
```

A poisoned R4 owner does not silently reconstruct live runtime and continue.

## 18. Telemetry

R4 materializes telemetry for:

```text
session open count
invocation open/complete counts
generation commit count
Adam first hydration count
resident Weight first adoption count
ProductionMuonRuntime first construction count
HiMuon momentum first load count
MCU session first open count
runtime park count
runtime restore count
runtime reconstruction count
poison count
```

Physical PASS remains false.

## 19. Invocation Receipt

Every R4 invocation emits:

```text
trainable_session_invocation_r4_<ordinal>.json
```

binding at least:

```text
invocation ordinal
source generation
final generation
committed generation count
exit class
whether parked runtime was restored
whether runtime was parked for the successor invocation
runtime reconstruction count
whether the session remains open
```

## 20. Static Validation

Validator:

```text
tools/validate_ash_trainable_session_active_production_owner_cross_invocation_runtime_cutover_r4_static.py
```

Current result:

```text
64 / 64 PASS
```

Token:

```text
PASS_ASH_TRAINABLE_SESSION_ACTIVE_PRODUCTION_OWNER_AND_CROSS_INVOCATION_RUNTIME_CUTOVER_R4_STATIC
```

## 21. Parent Regression

Current R4 bake retains:

```text
Eve R3G                 35 / 35 PASS
MCU SESSION R7          55 / 55 PASS
MCU R7A                 73 / 73 PASS
R3C                     18 / 18 PASS
R3C1                    30 / 30 PASS
R3D                     41 / 41 PASS
R3E                     52 / 52 PASS
R3F                     66 / 66 PASS
Unified Atlas MCU R6    PASS
Mixed-precision MCU R7  PASS
SubmissionEpoch async   PASS
```

Two older validators remain at their exact parent-baseline result and are not R4 regressions:

```text
RAM exact inventory validator       66 / 67
- stale inventory-seed-passed call-name expectation

N8 RAM resume-cut validator        117 / 118
- stale sourceTreeDigest symbol expectation
```

Both failures reproduce unchanged on the direct R7A parent ZIP.

## 22. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore Rust compile PASS is not claimed.

The new R4 Python validator passes `py_compile`; changed Rust source passes UTF-8 and structural delimiter checks.

## 23. Physical Qualification

Physical R4 promotion requires a real caller to perform at least:

```text
open one R4 owner
Invocation A -> KeepResident
Invocation B -> KeepResident or DurableCheckpointKeepResident
Invocation C -> CloseAfterDurableWriteback
```

and demonstrate:

```text
session open count = 1
Adam hydration count = 1
ProductionMuonRuntime construction count = 1
HiMuon momentum load count = 1
MCU session open count = 1
runtime restore count >= 1
runtime reconstruction count = 0
same R3G authority instance across live invocations
monotonic Eve lease ordinal sequence across invocations
resident Weight continuity exact
RAM36 bounds preserved
R3C1 commit atomicity preserved
no numerical divergence
```

Until then:

```text
HOLD_ASH_TRAINABLE_SESSION_R4_PHYSICAL_PENDING
```

## 24. Explicit Non-claims

R4 does not claim:

```text
all current production deployments already invoke multiple R4 slices
ProductionMuonRuntime structurally decomposed
MCU child fields physically extracted
BPDK separated
HiMuon momentum dirty-page identity
hot-path environment reads retired
configuration bool explosion resolved
multi-device training
tensor parallel execution
```

## 25. Direct Successors

Recommended immediate successors:

```text
ASH-TRAINABLE-SESSION
-SEALED-ADMISSION-PROFILE
-AND-HOTPATH-ENVIRONMENT-READ-RETIREMENT-R4A
```

then:

```text
ASH-MCU
-CHILD-AUTHORITY-PHYSICAL-EXTRACTION
-AND-GENERATION-RUNTIME-OWNERSHIP-CLOSURE-R7B
```

## 26. Final Law

> Returning from an R4 invocation is no longer inherently equivalent to destroying the live training runtime.

> A KeepResident boundary moves the live runtime back to the production owner, and the next invocation restores the same authority instead of rebuilding it from durability.

> Persistent runtime is now represented in the active production call graph rather than only by persistent-looking type names.
