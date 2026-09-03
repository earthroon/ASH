# ASH-MCU-CHILD-AUTHORITY-PHYSICAL-EXTRACTION-AND-GENERATION-RUNTIME-OWNERSHIP-CLOSURE-R7B

## 0. Revision

```text
Patch ID:
ASH-MCU
-CHILD-AUTHORITY-PHYSICAL-EXTRACTION
-AND-GENERATION-RUNTIME-OWNERSHIP-CLOSURE-R7B

Short name:
ASH MCU SESSION R7B
PHYSICAL CHILD EXTRACTION + GENERATION RUNTIME OWNERSHIP CLOSURE

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:               NOT CLAIMED
GPU physical PASS:               NOT CLAIMED
ownership physical PASS:         NOT CLAIMED
multi-generation physical PASS:  NOT CLAIMED
R3C1 no-fail physical PASS:      NOT CLAIMED
```

Static token:

```text
PASS_ASH_MCU_CHILD_AUTHORITY_PHYSICAL_EXTRACTION_AND_GENERATION_RUNTIME_OWNERSHIP_CLOSURE_R7B_STATIC
```

Physical state:

```text
HOLD_ASH_MCU_CHILD_AUTHORITY_R7B_PHYSICAL_PENDING
```

## 1. Direct Parents

R7B consumes without redefining:

```text
MCU SESSION R7
MCU device-resource R7A
Trainable Session R4
Trainable Session admission seal R4A
Eve R3G
R3C / R3C1 full TrainableGeneration commit
Unified Atlas MCU R6 / mixed R7 / router R8 / bucket R8A
Atlas lease R1
SubmissionEpoch dependency R1
pending Wave queue R1/R2
AdamW pending generation scheduler R1
```

R7B changes physical Rust ownership and physical device-generation lifetime only. It does not change Adam or HiMuon mathematics.

## 2. Problem Closed

Before R7B, `ProductionMuonExecutionRuntime` owned `McuSessionRuntimeR7` and also directly owned most physical MCU children beside it. This made semantic MCU ownership and actual Rust field ownership disagree.

R7B makes the type tree match the authority tree.

## 3. Core Law

> Physical scheduling, submission, device-candidate tracking, GPU completion and physical retirement children are owned beneath the MCU session.

> Current device source generations are session state. Target generations and pending schedulers are one physical-generation transaction. Previous sources survive only in bounded post-commit retirement slots.

> HiMuon momentum, BPDK semantics, ResidentStateGraph and HybridOptimizerCommitCoordinator remain outside MCU ownership.

## 4. New R7B Runtime

Materialized:

```rust
McuSessionRuntimeR7B
```

with:

```text
parent_r7
persistent children
committed device source
physical generation
post-commit retirement
R4A seal binding
R7B admission state
R7B telemetry
```

`McuSessionRuntimeR7` remains an immutable historical semantic parent.

## 5. Persistent Child Extraction

Materialized:

```rust
McuPersistentChildAuthoritiesR7B
```

It physically owns:

```text
McuGlobalTensorCubeJobQueueR6
McuMixedPrecisionExecutionExpertAuthorityR7
McuDeterministicPrecisionExpertRouterR8
McuGpuResidentExpertBucketAuthorityR8A
McuExactAtlasSlotLeaseGenerationRuntimeR1
McuSubmissionEpochDependencyRuntimeR1
ProductionMuonPendingQueueCutoverRuntimeR1
ProductionMuonPendingWaveQueueCoreR2
MuonDeviceCandidateRuntime
AsyncRetirementRuntime
McuRealProductionWaveShadowRuntimeR1
```

These objects are constructed once and moved into the R7B owner.

## 6. ProductionMuon Physical Cut

After R7B, `ProductionMuonExecutionRuntime` directly owns one MCU field:

```text
mcu_session_r7b: McuSessionRuntimeR7B
```

It no longer directly owns the R6 queue, mixed R7 expert, R8 router, R8A bucket, Atlas lease runtime, SubmissionEpoch dependency runtime, pending Wave queue, device candidate runtime or async retirement runtime.

The historical R7 static-witness strings remain comments only so older static validators can continue proving their parent ABI without restoring physical ownership.

## 7. HiMuon Executor Ownership

The previous direct ProductionMuon `batch_executor` and `gradient_packer` fields are removed.

Production code now obtains the executor and packer from the parent R7 MCU session. R7A cached-kernel semantics remain intact.

## 8. State That Remains Outside MCU

R7B explicitly leaves outside:

```text
HiMuon canonical momentum
source / momentum host Wave slabs
SoftMatrix and norm mathematical authorities
BpDkDevicePostUpdateEvidenceArenaR1
R3C1 retired BPDK evidence
MuonResidentStateGraph
HybridOptimizerCommitCoordinator
GpuEvidenceRuntime
ProductionRuntimeAdmissionReceipt
Eve R3A compatibility lease ordinal
fused-pair executor
```

GPU-produced evidence is not automatically MCU semantic authority.

## 9. Committed Device Source State

Materialized:

```rust
McuCommittedDeviceSourceStateR7B
```

with exact current physical:

```text
MuonDeviceSegmentedGenerationR1
AdamWDeviceSegmentedGenerationR1
```

when present.

The two source generations must agree where the admitted full-device path requires both.

`committed` here means current physical GPU source after external TrainableGeneration commit. It does not transfer semantic commit authority to MCU.

## 10. Physical Generation Runtime

Materialized:

```rust
McuPhysicalGenerationRuntimeR7B
McuPhysicalGenerationIdentityR7B
McuPhysicalGenerationPhaseR7B
```

It owns generation-local:

```text
Muon target generation
AdamW pending generation scheduler
AdamW target generation
FullTrainableDeviceGenerationR1
Adam scheduler receipt
Eve Adam device-generation handoff
exact physical SubmissionEpoch union
```

The physical generation identity is joined to the active parent R7 generation identity and rejects source/target drift.

## 11. Physical Generation Admission

New default-OFF config:

```text
admit_mcu_child_authority_physical_extraction_r7b
admit_mcu_generation_runtime_ownership_closure_r7b
```

Generation-runtime ownership requires child extraction.

R7B production admission requires MCU SESSION R7 and the sealed R4A session profile. Active generation-runtime ownership additionally requires the R3C1 production atomic cutover parent.

## 12. R4A Seal Binding

R4A `McuAdmissionProfileR4A` now binds both R7B admission flags.

The live ProductionMuon runtime binds the exact R4A admission-seal digest to `McuSessionRuntimeR7B` and rejects seal drift.

R4A raw runtime-config digest therefore also covers R7B admission state across invocations.

## 13. Parent R7 Generation Join

After Adam or HiMuon job admission creates/validates the R7 semantic generation, R7B lazily materializes the exact physical-generation identity from the active R7 generation digest.

Required relation:

```text
R7 semantic G -> G+1
==
R7B physical G -> G+1
```

Only one active physical generation is admitted.

## 14. Exact Submission Union

Materialized:

```rust
McuPhysicalSubmissionUnionR7B
```

It stores deduplicated target Muon/Adam SubmissionEpoch ordinals, class counts and a stable union digest.

`collect_target_submission_epoch_ordinals_r3c1` seals this physical union before R3C1 commit preparation.

## 15. R3C1 Prepare Closure

`prepare_full_trainable_device_rotation_r3c1` now verifies the physical target and R7B ownership state before producing the historical prepared rotation token.

For admitted R7B generation ownership it additionally requires:

```text
exact physical generation identity
sealed exact SubmissionEpoch union
empty previous post-commit retirement slots
zero current-source readers
zero target readers
```

Then the R7B physical generation enters `CommitPrepared`.

All recoverable checks occur before the no-fail tail.

## 16. R3C1 No-fail Rotation

The existing R3C1 no-fail commit tail remains the semantic commit coordinator.

Physical device rotation now acts on R7B-owned state:

```text
FullTrainableDevice target
        -> new Muon current source
        -> new Adam current source

old Muon source
old Adam source
        -> bounded post-commit retirement slots
```

R7B marks the physical rotation committed without introducing GPU waits, environment reads, pipeline construction or new buffer allocation in the no-fail tail.

Parent R7 generation retirement remains in the same no-fail external-commit path.

## 17. Post-commit Retirement

Materialized:

```rust
McuPostCommitRetirementRuntimeR7B
```

with one bounded retired Muon source slot and one bounded retired Adam source slot.

Before a new physical generation opens, both slots must be empty.

Retirement validates zero active source readers before release. After safe release R7B clears the physical-generation identity and returns to an invocation-safe session state.

BPDK evidence retirement remains a sibling semantic participant outside MCU.

## 18. R4 Cross-invocation Safety

Before a `KeepResident` R4 boundary, ProductionMuon now verifies for admitted R7B generation ownership:

```text
no active physical generation identity
no live Muon target
no live Adam scheduler
a no live Adam target
no live full target
no post-commit retired device source
R7B session phase Open
```

Therefore an ephemeral generation transaction cannot leak across a safe R4 invocation boundary, while committed physical device source state may remain resident with the session.

## 19. Construction and Compatibility

Historical child constructor order and parent mode selection are preserved. Child authorities are first built with their existing APIs and then moved into `McuPersistentChildAuthoritiesR7B` without creating a second authoritative instance.

Historical R6/R7/P5 static witnesses are retained as non-owning comments because older validators search for those exact source strings.

## 20. No Numerical Change

Required:

```text
Adam mathematics changed = false
HiMuon mathematics changed = false
norm reduction changed = false
expert selection policy changed = false
optimizer routing changed = false
R3G lease semantics changed = false
R3C/R3C1 semantic commit authority changed = false
```

R7B is an ownership revision.

## 21. Static Validation

New validator:

```text
tools/validate_ash_mcu_child_authority_physical_extraction_generation_runtime_ownership_closure_r7b_static.py
```

Current result:

```text
78 / 78 PASS
```

Token:

```text
PASS_ASH_MCU_CHILD_AUTHORITY_PHYSICAL_EXTRACTION_AND_GENERATION_RUNTIME_OWNERSHIP_CLOSURE_R7B_STATIC
```

The new R7B Rust module contains no `if` keyword; new R7B state-machine branching is expressed with typed `match`.

## 22. Parent Regression

Current bake retains:

```text
Trainable Session R4A       65 / 65 PASS
Trainable Session R4        64 / 64 PASS
Eve R3G                     35 / 35 PASS
MCU SESSION R7              55 / 55 PASS
MCU R7A                     73 / 73 PASS
R3C                         18 / 18 PASS
R3C1                        30 / 30 PASS
R3D                         41 / 41 PASS
R3E                         52 / 52 PASS
R3F                         66 / 66 PASS
Unified Atlas MCU R6        PASS
Mixed-precision MCU R7      PASS
SubmissionEpoch active      PASS
```

Two historical direct-parent baselines remain unchanged:

```text
RAM exact inventory         66 / 67
N8 RAM resume-cut          117 / 118
```

Both reproduce on the direct R4A parent ZIP and are not R7B regressions.

## 23. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore Rust compile PASS is not claimed.

The new R7B Python validator passes `py_compile`; changed Rust files pass UTF-8 and structural balanced-delimiter checks.

## 24. Physical Qualification

Physical promotion requires a real R4/R4A/R7B session with multiple committed generations and must prove at minimum:

```text
persistent MCU child construction count = 1 set
physical generation open count > 1
same persistent child authority across generations
parent R7 and R7B physical generation identities exact
exact SubmissionEpoch union for every prepared generation
current Muon/Adam source advances only after R3C1 permit
old source retained only in bounded retirement slots
zero readers before old-source release
no active physical generation at KeepResident boundary
R7A kernel/arena semantics preserved
R3C1 atomicity preserved
no numerical divergence
```

Until then:

```text
HOLD_ASH_MCU_CHILD_AUTHORITY_R7B_PHYSICAL_PENDING
```

## 25. Explicit Non-claims

R7B does not claim:

```text
ProductionMuonRuntime eliminated
HiMuon runtime decomposed
BPDK moved into MCU
HybridOptimizerCommitCoordinator moved into MCU
HiMuon momentum segmented
packed-gradient multi-consumer arena closure
fused-pair execution promoted to common MCU R7 fabric
multi-device execution
tensor-parallel Adam
tensor-parallel HiMuon
new scheduling policy
```

## 26. Direct Successor

Recommended next revision:

```text
ASH-MCU-HIMUON
-PACKED-GRADIENT-EXACT-MULTI-CONSUMER-SUBMISSION-LEASE
-AND-ARENA-REUSE-CLOSURE-R7A1
```

Then:

```text
ASH-HIMUON
-SESSION-RUNTIME-OWNERSHIP-SPLIT
-AND-MOMENTUM-EXECUTION-DURABILITY-SEPARATION-R8
```

## 27. Final Law

> If an object exists to schedule, submit, track, complete or retire admitted GPU execution, its physical owner is the MCU.

> Persistent execution children live with the session. Target device generations live with one physical generation transaction. Previous sources live only through bounded post-commit retirement.

> The MCU owns physical device execution state, but it does not own Adam mathematics, HiMuon momentum, BPDK semantics or TrainableGeneration commit authority.

> After R7B, ProductionMuon orchestrates the MCU. It no longer secretly is the MCU.
