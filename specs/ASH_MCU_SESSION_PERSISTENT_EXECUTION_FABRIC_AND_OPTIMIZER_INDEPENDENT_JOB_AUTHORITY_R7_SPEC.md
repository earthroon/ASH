# ASH-MCU-SESSION-PERSISTENT-EXECUTION-FABRIC-AND-OPTIMIZER-INDEPENDENT-JOB-AUTHORITY-R7

## 0. Revision

```text
Patch ID:
ASH-MCU
-SESSION-PERSISTENT-EXECUTION-FABRIC
-AND-OPTIMIZER-INDEPENDENT-JOB-AUTHORITY-R7

Short name:
ASH MCU SESSION R7
SESSION-PERSISTENT EXECUTION FABRIC
+ OPTIMIZER-INDEPENDENT JOB AUTHORITY

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:            NOT CLAIMED
GPU physical PASS:            NOT CLAIMED
multi-generation persistence: NOT CLAIMED
multi-invocation persistence: NOT CLAIMED
performance improvement:      NOT CLAIMED
N8 PASS:                      NOT CLAIMED
```

Static token:

```text
PASS_ASH_MCU_SESSION_PERSISTENT_EXECUTION_FABRIC_AND_OPTIMIZER_INDEPENDENT_JOB_AUTHORITY_R7_STATIC
```

Physical state:

```text
HOLD_ASH_MCU_SESSION_R7_PHYSICAL_PENDING
```

## 1. Revision Namespace

This revision is the `ASH-MCU-SESSION` architecture line. It does not replace or renumber the existing Unified Atlas MCU lineage:

```text
R6   Global TensorCube Job Queue
R7   Mixed Precision Execution Expert ABI
R8   Deterministic Precision Expert Router
R8A  GPU Resident Expert Bucket
```

Those remain immutable child authorities.

## 2. Direct Parent

Direct architecture parent:

```text
ASH-ADAMS-RIB-EVE
-PERSISTENT-AUTHORITY-INSTANCE
-AND-TRAINABLE-SESSION-LIFETIME-OWNERSHIP-CLOSURE-R3G
```

R3G establishes one persistent Eve live-authority incarnation and one trainable-session ownership envelope. MCU SESSION R7 extends that lifetime rule to physical optimizer execution infrastructure.

## 3. Existing Parent Authorities

R7 consumes without redefining:

```text
Eve R3 / R3A / R3G
MCU Eve Adam target writeback R3B
R3C / R3C1 atomic TrainableGeneration commit
Unified Atlas MCU R6 queue
Unified Atlas MCU mixed-precision R7
Unified Atlas MCU router R8
Unified Atlas MCU bucket R8A
Exact Atlas slot lease R1
SubmissionEpoch dependency active async R1
Local Muon pending Wave queue R1/R2
AdamW ActiveDevice pending generation scheduler R1
```

## 4. Current Source Truth

Before MCU SESSION R7, practical MCU execution machinery is co-located inside `ProductionMuonExecutionRuntime`, including R6/R7/R8/R8A authorities, SubmissionEpoch dependency state, pending Wave scheduling, AdamW generation scheduling, HiMuon batch executor, gradient packer and async retirement.

The AdamW scheduler directly constructs `AdamWActiveDeviceCandidateProducerR1`, so a new target generation can construct a new shader/pipeline producer.

HiMuon already lazily constructs `TensorCubeLocalMuonBatchExecutor` inside one `ProductionMuonRuntime`, so R7 MUST NOT falsely claim per-Wave pipeline reconstruction. Its remaining problem is ownership/lifetime above the optimizer runtime boundary.

## 5. Core Law

After admitted R7:

> One trainable session owns one MCU execution authority for one admitted DeviceAuthorityId / QueueAuthorityId pair.

And:

> AdamW and HiMuon share a common MCU job authority without surrendering their separate optimizer-state and mathematical authorities.

Authority separation:

```text
Eve                   = canonical Adam M/V authority
HiMuon                 = canonical Muon momentum authority
MCU SESSION R7         = physical execution authority
R3C / R3C1             = committed TrainableGeneration authority
```

## 6. Non-goals

R7 does not change:

```text
Adam mathematics
Adam hyperparameters
HiMuon mathematics
HiMuon norm/reduction order
optimizer routing semantics
Weight authority
Adam durability format
Muon durability format
R3C/R3C1 commit semantics
```

R7 does not yet claim:

```text
generalized GPU buffer arena
all bind-group reuse
device-lifetime cache across trainable sessions
multi-device MCU
tensor-parallel Adam
tensor-parallel HiMuon
cross-process GPU object persistence
```

## 7. Session Runtime

Materialized type:

```rust
pub struct McuSessionRuntimeR7
```

with typed lifecycle:

```rust
pub enum McuSessionPhaseR7 {
    Open,
    GenerationActive,
    Closing,
    Closed,
    Poisoned,
}
```

Critical new R7 lifecycle code uses typed `match` transitions rather than authoritative boolean combinations.

## 8. Trainable Session Successor Envelope

Materialized type:

```rust
pub struct TrainableSessionRuntimeR7 {
    eve_r3g: TrainableSessionRuntimeR3G,
    mcu: McuSessionRuntimeR7,
}
```

R7 therefore does not retroactively claim that R3G already owned MCU execution.

## 9. MCU Session Identity

`McuSessionIdentityR7` binds:

```text
R3G authority instance ordinal
R3G authority instance record digest
DeviceAuthorityId
QueueAuthorityId
optimizer routing digest
capability digest
```

Session identity does not use:

```text
raw pointer
PID
thread identity
wall-clock time
allocator address
hostname
```

## 10. Device / Queue Binding

R7 reuses the existing A01 physical authority:

```text
DeviceAuthorityId
QueueAuthorityId
```

through `queue_authority_ids`.

Once bound, a different Device/Queue authority fails closed with:

```text
E_MCU_SESSION_R7_DEVICE_QUEUE_AUTHORITY_DRIFT
```

No competing GPU device identity system is introduced.

## 11. R3G Binding

An admitted MCU session is bound to the exact Eve R3G authority incarnation by:

```text
bind_eve_authority_r3g
```

A fresh R3G authority incarnation therefore cannot silently continue an old MCU session identity.

## 12. Generation Runtime Identity

Materialized:

```rust
pub struct McuGenerationIdentityR7
```

binding:

```text
source model generation
target model generation
source optimizer generation
target optimizer generation
optimizer routing digest
identity digest
```

Model generation must be an exact checked successor.

## 13. Generation Phase

Materialized typed state:

```rust
pub enum McuGenerationPhaseR7 {
    Open,
    Sealed,
    Draining,
    Complete,
    Retired,
    Poisoned,
}
```

One MCU session may own at most one active R7 generation ledger.

## 14. Optimizer-independent Job Authority

Materialized:

```rust
pub struct McuOptimizerJobAuthorityR7
```

with optimizer class:

```rust
pub enum McuOptimizerClassR7 {
    AdamW,
    HiMuonLocal,
}
```

R7 does not flatten Adam and HiMuon into one fake mathematical optimizer.

## 15. Canonical Job Key

Materialized:

```rust
pub enum McuCanonicalJobKeyR7 {
    AdamW { range: AdamRangeR1 },
    HiMuon {
        canonical_parameter_index: u32,
        canonical_tensorcube_ordinal: u64,
    },
}
```

Queue position and SubmissionEpoch are not canonical semantic job identity.

## 16. Common Job Identity

`McuJobIdentityR7` binds:

```text
MCU session digest
source/target generation
source/target optimizer generation
optimizer class
canonical parameter index
generation submission ordinal
typed canonical job key
parent identity digest
```

For Adam the parent identity is the R3G lease digest.

For HiMuon the parent identity is the exact R6 epoch manifest digest.

## 17. Monotonic Submission Ordinal

Every R7 generation begins job submission ordinal at one.

Issued ordinals use checked increment and cannot wrap.

A duplicate semantic key is rejected even if a new physical queue position exists.

## 18. Adam Mutable Alias Check

R7 records admitted Adam ranges and rejects overlapping Adam mutable output ranges through `AdamRangeR1::overlaps`.

The canonical optimizer routing registry remains the cross-optimizer ownership SSOT.

R7 does not invent a second route classifier.

## 19. Persistent Adam Executor

Materialized:

```rust
pub struct McuAdamWExecutorR7
```

It lazily owns:

```text
Arc<AdamWActiveDeviceCandidateProducerR1>
```

and records producer build/borrow counts.

The physical producer contains the AdamW shader module layout and compute pipeline authority.

## 20. Adam Scheduler Injection

Historical scheduler constructor remains:

```rust
AdamWActiveDevicePendingGenerationSchedulerR1::new(...)
```

for compatibility.

R7 adds:

```rust
new_with_persistent_producer_r7(
    Arc<AdamWActiveDeviceCandidateProducerR1>,
    ...
)
```

Under admitted R7, the R3G Adam production path obtains the producer from `McuSessionRuntimeR7` rather than constructing a generation-local producer.

## 21. Adam Production Route

R7 Adam route:

```text
Eve R3G exact RAM lease
        -> MCU R7 job admission
        -> persistent Adam producer
        -> generation-local Adam scheduler
        -> ActiveDevice candidate
        -> existing R3B writeback
        -> Eve CandidateComplete
```

Arbitrary host M/V does not become R7 production authority.

## 22. HiMuon Executor Ownership

R7 makes the MCU session the owner of persistent shared handles for:

```text
TensorCubeLocalMuonBatchExecutor
TensorCubeLocalMuonGradientPacker
```

The production Muon runtime retains `Arc` handles as execution clients.

The underlying physical executor is therefore not duplicated merely to satisfy multiple internal callsites.

## 23. HiMuon R6 Parent Preservation

R7 does not replace `McuTensorCubeJobDescriptorR6`.

The production route remains:

```text
R6 descriptor / epoch seal
        -> R7 common job authority
        -> existing R7/R8/R8A expert selection
        -> HiMuon physical executor
```

Historical R6 identity stays canonical for Local Muon tiles.

## 24. HiMuon Job Admission

When optimizer-independent R7 authority is active, every execution descriptor in an admitted R6 epoch enters the R7 ledger with:

```text
source generation
candidate generation
canonical parameter index
canonical R6 job ordinal
R6 epoch manifest digest
```

A requested R7 HiMuon job without an R6 parent epoch fails closed.

## 25. Routing Law

Existing optimizer routing remains SSOT.

R3G Adam callsites already prove that submitted ranges are not Muon-owned.

HiMuon work remains derived from canonical Muon-eligible TensorCube planning.

R7 does not create an alternate routing table.

## 26. Generation Retirement

R7 generation ledger is retired after existing generation commit authority succeeds.

Legacy commit path and R3C1 no-fail tail both perform non-failing R7 ledger retirement after external commit ownership has been established.

Generation abort clears the R7 generation ledger without advancing committed optimizer authority.

## 27. R3C / R3C1 Authority Preservation

MCU R7 does not call Eve commit on its own authority.

MCU R7 does not commit HiMuon momentum on its own authority.

MCU R7 does not publish full TrainableGeneration on its own authority.

R3C/R3C1 remain the sole full-generation commit join.

## 28. Production Configuration

New config fields:

```text
admit_mcu_session_persistent_execution_fabric_r7
admit_mcu_optimizer_independent_job_authority_r7
```

Defaults are OFF.

The optimizer-independent job authority requires the session execution fabric.

## 29. Parent Admission

Active R7 execution fabric requires:

```text
R3G persistent authority instance
R3G trainable-session lifetime admission
ProductionMuonRuntime
```

Optimizer-independent job authority additionally requires:

```text
MCU Eve exact Adam source parent R3A/R3G
production Local Muon callsite
```

No parent gate is weakened.

## 30. Production Construction

`ProductionMuonRuntime` gains an R7-aware construction surface:

```text
load_or_initialize_with_admission_native_witness_and_mcu_session_r7
```

Historical constructors remain compatibility wrappers and pass R7 admission as false.

## 31. Static Lifetime Materialization Boundary

This static bake materially closes:

```text
Adam producer no longer required to be generation-local under R7
HiMuon batch executor owned through MCU session Arc authority
HiMuon gradient packer owned through MCU session Arc authority
R3G Adam jobs enter common MCU ledger
R6 HiMuon jobs enter common MCU ledger
Device/Queue and Eve authority are session-bound
```

The bake does not yet claim a physical campaign proving that the enclosing `McuSessionRuntimeR7` survives multiple top-level R6 execution invocations. That remains a physical HOLD condition.

## 32. Child MCU Runtime Location

Existing R6/R7/R8/R8A queue/router/bucket objects remain historical child implementations and are not redefined.

This revision establishes the new outer session/job authority and persistent physical executor ownership first. A later source cleanup may physically relocate every child field from `ProductionMuonExecutionRuntime` into a narrower MCU struct without changing the R7 semantic ABI.

Therefore source co-location is not treated as semantic ownership.

## 33. Buffer Policy

R7 permits existing job-local variable buffers:

```text
Adam candidate Weight/M/V
status/readback buffers
parameter uniform
Muon Wave output storage
readback staging
job bind groups
```

R7 MUST NOT claim complete allocation pooling.

## 34. R7A Boundary

Direct resource-lifetime successor:

```text
ASH-MCU
-DEVICE-LIFETIME-KERNEL-CACHE
-AND-BOUNDED-BUFFER-ARENA-R7A
```

R7A will target:

```text
candidate buffer reuse
status/readback rings
uniform slab
bounded size classes
SubmissionEpoch-governed recycling
bind-group reuse where legal
```

## 35. No Numerical Change

R7 changes scheduling/ownership only.

Required static claim:

```text
Adam math changed = false
Adam precision changed = false
HiMuon math changed = false
HiMuon reduction order changed = false
optimizer routing changed = false
```

Physical parity remains required before promotion.

## 36. No Silent Fallback

When active R7 authority has admitted a job, failure does not silently resubmit the same job through an unrelated legacy owner.

Fail-closed conditions include:

```text
missing R3G authority binding
Device/Queue authority drift
wrong generation
wrong optimizer generation
duplicate semantic job
Adam mutable alias
R7 HiMuon job without R6 parent
submission ordinal overflow
second active generation
```

## 37. Telemetry

`McuSessionTelemetryR7` records at least:

```text
session open count
execution invocation count
generation open count
generation complete count
admitted job count
Adam job count
HiMuon job count
Adam executor build count
HiMuon executor build count
gradient packer build count
legacy direct submit count
physical pass claimed
```

Physical PASS remains false in this static bake.

## 38. Required Persistence Relations

A future physical multi-generation campaign must show:

```text
sessionOpenCount = 1
generationOpenCount > 1
Adam executor build count <= 1
HiMuon executor build count <= 1
gradient packer build count <= 1
```

A future multi-invocation campaign additionally requires the same counts to remain stable across more than one execution invocation.

## 39. Static Validator

Validator:

```text
tools/validate_ash_mcu_session_persistent_execution_fabric_optimizer_independent_job_authority_r7_static.py
```

Current result:

```text
55 / 55 PASS
```

It verifies session/generation/job ABIs, R3G binding, A01 Device/Queue binding, persistent Adam producer injection, HiMuon Arc ownership, R6 HiMuon parent binding, config gates, generation retirement and explicit physical HOLD.

## 40. Parent Regression

Current code-only bake retains PASS for:

```text
Eve R3G                         35 / 35
MCU Eve R3A                    PASS
MCU Eve R3B                    PASS
Eve/HiMuon R3C                18 / 18
Eve/HiMuon R3C1               30 / 30
Adam durability R3D           41 / 41
Weight durability R3E         52 / 52
HiMuon durability R3F         66 / 66
Unified Atlas MCU R6          PASS
Unified Atlas mixed R7        PASS
SubmissionEpoch async R1      PASS
```

The R8 and R8A validators require their specification files to be present. The requested code-only source archive intentionally excludes `specs/`, so those two validator invocations stop at their spec-file prerequisite rather than a source assertion failure.

## 41. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore:

```text
Rust compile PASS = NOT CLAIMED
```

New/modified Rust files pass UTF-8 and structural delimiter checks. The R7 Python validator passes `py_compile`.

## 42. Physical Qualification

Physical promotion requires at minimum:

```text
real R3G trainable session
real R7 MCU session
both Adam and HiMuon jobs through R7 authority
at least three committed generations
Adam producer construction count = 1
HiMuon executor construction count <= 1
gradient packer construction count <= 1
exact DeviceAuthorityId / QueueAuthorityId stability
exact R3G authority-instance stability
R6 job identity parity
R3G Adam lease identity parity
R3C1 atomic commit preserved
no stale cross-generation writer
no numerical divergence
bounded memory growth
no material throughput regression
```

Multi-invocation qualification additionally requires one MCU session to survive multiple explicit execution invocations.

## 43. Static PASS Token

```text
PASS_ASH_MCU_SESSION_PERSISTENT_EXECUTION_FABRIC_AND_OPTIMIZER_INDEPENDENT_JOB_AUTHORITY_R7_STATIC
```

## 44. Physical PASS Token

Reserved:

```text
PASS_ASH_MCU_SESSION_PERSISTENT_EXECUTION_FABRIC_AND_OPTIMIZER_INDEPENDENT_JOB_AUTHORITY_R7_PHYSICAL
```

Until qualified:

```text
HOLD_ASH_MCU_SESSION_R7_PHYSICAL_PENDING
```

## 45. Final Architecture Law

R7 establishes:

```text
optimizer state authority != execution authority != committed-generation authority
```

and the lifetime target:

> The Adam/HiMuon execution machinery is no longer semantically owned by one generation. The MCU session owns persistent execution infrastructure, while generation-local ledgers are created and retired beneath it.

The next revision may optimize resources further, but it MUST preserve this authority split.
