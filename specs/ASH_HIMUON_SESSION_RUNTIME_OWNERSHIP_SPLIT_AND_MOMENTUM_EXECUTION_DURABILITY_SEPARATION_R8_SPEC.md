# ASH-HIMUON-SESSION-RUNTIME-OWNERSHIP-SPLIT-AND-MOMENTUM-EXECUTION-DURABILITY-SEPARATION-R8

## 0. Revision

```text
Patch ID:
ASH-HIMUON
-SESSION-RUNTIME-OWNERSHIP-SPLIT
-AND-MOMENTUM-EXECUTION-DURABILITY-SEPARATION-R8

Short name:
ASH HIMUON R8
SESSION RUNTIME OWNERSHIP SPLIT + MOMENTUM / EXECUTION / DURABILITY SEPARATION

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:              NOT CLAIMED
GPU physical PASS:              NOT CLAIMED
ownership split physical PASS:  NOT CLAIMED
R3F durability parity PASS:     NOT CLAIMED
```

Static token:

```text
PASS_ASH_HIMUON_SESSION_RUNTIME_OWNERSHIP_SPLIT_AND_MOMENTUM_EXECUTION_DURABILITY_SEPARATION_R8_STATIC
```

Physical state:

```text
HOLD_ASH_HIMUON_R8_PHYSICAL_PENDING
```

## 1. Direct Parents

R8 consumes without redefining Trainable Session R4/R4A, MCU R7/R7A/R7B, packed-gradient R7A1, R3C/R3C1 and HiMuon durability R3F.

R8 changes HiMuon runtime ownership. It does not change optimizer mathematics, R7B physical MCU ownership or R3F durable schema.

## 2. Problem Closed

Before R8, `ProductionMuonExecutionRuntime` combined the canonical momentum `Vec<f32>`, execution scratch/math authority, MCU client, BPDK evidence, resident-state/commit participants and durability-facing momentum access.

R8 removes that production owner and makes `ProductionMuonRuntime` an orchestration aggregate of sibling authorities.

## 3. New Runtime Split

Materialized modules:

```text
himuon_momentum_runtime_r8.rs
himuon_execution_runtime_r8.rs
himuon_durability_runtime_r8.rs
himuon_session_runtime_r8.rs
production_muon_commit_runtime_r8.rs
```

`ProductionMuonRuntime` now owns:

```text
HiMuonSessionRuntimeR8
McuSessionRuntimeR7B
ProductionBpDkRuntimeR8
ProductionMuonCommitRuntimeR8
ProductionMuonCompatibilityRuntimeR8
telemetry / lifecycle
```

MCU is a sibling of HiMuon, not a child of HiMuon.

## 4. Historical Compatibility Witness

The old `ProductionMuonExecutionRuntime` exists only under `#[cfg(any())]` as a historical static-validator witness. It is uninhabited in every build and is not the R8 production owner.

Historical R7/R7B/R4A/R3F validator source witnesses remain comments or cfg-disabled structure and do not restore old ownership.

## 5. Canonical Momentum Authority

Materialized:

```rust
pub struct HiMuonMomentumRuntimeR8
```

Its canonical backing remains exactly one private:

```rust
values: Vec<f32>
```

R8 creates no second canonical momentum body and no full-body clone for structural separation.

The current representation remains contiguous F32. Segmented backing is explicitly deferred to R8A.

## 6. Momentum API

R8 materializes typed APIs including:

```text
HiMuonMomentumRangeR8
HiMuonMomentumReadLeaseR8
HiMuonMomentumDurabilityLeaseR8
read_range_r8
copy_range_into_r8
copy_range_owned_r8
copy_tile_256_r8
commit_candidate_range_r8
commit_candidate_tile_r8
durability_lease_r8
```

There is no general `values_mut` or `momentum_mut` production API.

All range arithmetic is checked and candidate writes reject non-finite values.

## 7. Direct Backing Access Retirement

The active ProductionMuon source no longer contains `self.execution.momentum` or direct indexing of the canonical backing.

Parameter execution, streaming execution, BPDK tile reads and candidate momentum commits use the typed momentum runtime APIs.

R8 ownership receipt statically reports:

```text
momentumOwnerCount = 1
executionOwnerCount = 1
durabilityOwnerCount = 1
mcuOwnerCountInsideHiMuon = 0
fullMomentumCloneCount = 0
directBackingAccessCount = 0
physicalPassClaimed = false
```

## 8. Execution Runtime

Materialized:

```rust
HiMuonExecutionRuntimeR8
HiMuonExecutionScratchR8
HiMuonExecutionProfileR8
```

Execution owns noncanonical scratch and mathematical execution authorities:

```text
source Wave slab
momentum Wave slab
source slab generation
norm reduction path
SoftMatrix16 R4 authority
deterministic subgroup R5 authority
fused-pair compatibility executor
R4A Wave/R7A1 execution profile values
```

Wave momentum scratch is not canonical momentum authority and is never durable authority.

## 9. R4A Admission Binding

New default-OFF config:

```text
admit_himuon_session_runtime_ownership_split_r8
admit_himuon_momentum_execution_durability_separation_r8
```

Momentum/execution/durability separation requires the R8 ownership parent.

R8 ownership requires the R4 active session owner, R7B child extraction and R7A1 exact packed-gradient parent.

Both flags are included in the sealed R4A HiMuon profile and the ProductionMuon environment profile, so one live R4 session cannot change R8 ownership mode between invocations.

## 10. MCU Ownership Preserved

`McuSessionRuntimeR7B` remains directly owned by `ProductionMuonRuntime` as a sibling of `HiMuonSessionRuntimeR8`.

R8 does not move any R6/R7/R8/R8A queue/expert/router/bucket, SubmissionEpoch, pending Wave, Adam scheduler or physical device-generation ownership back into HiMuon.

R7B remains the physical GPU execution authority.

## 11. Commit Runtime

Materialized:

```rust
ProductionMuonCommitRuntimeR8
```

It owns:

```text
MuonResidentStateGraph
HybridOptimizerCommitCoordinator
GpuEvidenceRuntime
```

This split does not change R3C/R3C1. The full TrainableGeneration commit permit and no-fail tail remain external semantic commit authority.

## 12. BPDK Aggregate

Materialized in the ProductionMuon integration layer:

```rust
ProductionBpDkRuntimeR8
```

It groups existing observation, bridge, planning, control and evidence runtimes plus BPDK device-evidence arenas and startup-binding state.

BPDK remains outside the MCU and outside canonical HiMuon momentum authority.

## 13. Durability Runtime

Materialized:

```rust
HiMuonDurabilityRuntimeR8
```

Durability owns momentum durability policy/integration and metadata, not momentum bytes.

It accepts immutable momentum authority and owns no `BackendDevice`, `BackendQueue` or GPU execution object.

R3F identity, recovery-anchor preparation and historical full-payload compatibility writes are delegated through the durability runtime.

## 14. R3F Flat Identity Preserved

R8 intentionally reuses historical:

```text
digest_resident_muon_momentum_r3f
```

which scans the complete contiguous F32 body and hashes exact little-endian F32 bytes.

Therefore R3F schema/identity semantics remain unchanged.

Current truth:

```text
ordinary/full momentum identity O(N) RAM scan = still present
```

R8 MUST NOT claim this performance debt closed.

## 15. Legacy Full Momentum Persistence

Historical `persist_candidate_state` remains available as compatibility API, but full momentum payload writing now obtains the bytes through `HiMuonDurabilityRuntimeR8::persist_full_payload_r8` and an immutable momentum durability lease.

Ordinary R3F control-only persistence remains unchanged and still suppresses ordinary full momentum payload rewrite.

## 16. Cross-invocation Lifetime

The R4 parked ProductionMuon runtime now retains one R8 aggregate.

A KeepResident successor invocation retains the same:

```text
HiMuonMomentumRuntimeR8
HiMuonExecutionRuntimeR8
HiMuonDurabilityRuntimeR8
McuSessionRuntimeR7B
```

R8 does not use durability as live invocation-to-invocation transport and does not require a new momentum hydration merely because an invocation changes.

Cross-invocation physical proof remains HOLD until exercised on a real campaign.

## 17. No RAM Growth by Split

R8 adds no second full canonical momentum body.

Existing RAM36 ownership for `TensorCubeLocalMuonMomentum` remains attached to the same resident F32 body. Execution slabs remain scratch under their historical bounds.

## 18. No Synchronization Shortcut

New R8 components do not use `Arc<Mutex<_>>` as an ownership shortcut and do not introduce a dynamic `Box<dyn ...>` component fabric.

The new R8 runtime modules use static nested Rust ownership and new R8 state/validation code uses `match`; the new R8 modules contain no Rust `if` keyword.

## 19. Configuration Compatibility

R8 flags default OFF in `BaseTrainingRuntimeConfig` and the existing pipeline literal.

When R8 flags are disabled, historical numerical behavior remains. The new structural wrappers are representation-only and preserve compatibility APIs.

## 20. Static Validation

New validator:

```text
tools/validate_ash_himuon_session_runtime_ownership_split_momentum_execution_durability_separation_r8_static.py
```

Current result:

```text
90 / 90 PASS
```

Static token:

```text
PASS_ASH_HIMUON_SESSION_RUNTIME_OWNERSHIP_SPLIT_AND_MOMENTUM_EXECUTION_DURABILITY_SEPARATION_R8_STATIC
```

## 21. Parent Regression

Current bake retains:

```text
R7A1 packed-gradient lifetime      82 / 82 PASS
R7B MCU child ownership            78 / 78 PASS
R7A device resource                73 / 73 PASS
MCU SESSION R7                     55 / 55 PASS
Trainable Session R4A              65 / 65 PASS
Trainable Session R4               64 / 64 PASS
Eve R3G                            35 / 35 PASS
R3C                                18 / 18 PASS
R3C1                               30 / 30 PASS
R3D                                41 / 41 PASS
R3E                                52 / 52 PASS
R3F                                66 / 66 PASS
```

Historical unchanged baselines remain:

```text
RAM exact inventory                66 / 67
N8 RAM resume-cut                 117 / 118
```

Those two baseline failures predate R8.

## 22. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore Rust compile PASS and GPU physical PASS are not claimed.

The R8 validator passes Python `py_compile`; changed Rust files pass UTF-8 and balanced-delimiter structural checks.

## 23. Physical Qualification

Physical R8 promotion requires a real R4/R4A session using HiMuon and must prove at minimum:

```text
one canonical momentum body
momentum hydration count = 1 per live session
no full momentum clone due to split
no direct momentum backing access outside R8 owner
candidate Weight/Momentum parity against parent
BPDK evidence parity
R3F identity parity
R3F recovery-anchor parity
R3C1 generation parity
same R8 runtime across KeepResident invocations
no numerical or material performance regression
```

Until then:

```text
HOLD_ASH_HIMUON_R8_PHYSICAL_PENDING
```

## 24. Explicit Non-claims

R8 does not claim:

```text
segmented momentum backing
dirty-page momentum identity
incremental momentum root
ordinary O(N) momentum scan retired
device-hot canonical momentum
ProductionMuonRuntime removed
BPDK removed
fused-pair promoted into common MCU fabric
multi-device execution
tensor-parallel HiMuon
```

## 25. Direct Successor

Recommended successor:

```text
ASH-HIMUON
-SEGMENTED-MOMENTUM
-DIRTY-PAGE-IDENTITY
-AND-INCREMENTAL-ROOT-R8A
```

R8A may change the private momentum backing without reopening the ProductionMuon execution graph because execution and durability now depend on the R8 momentum API rather than `Vec<f32>` layout.

## 26. Final Law

> Momentum is canonical optimizer state. Execution mutates that state through a narrow contract. Durability observes and serializes it through an immutable contract. They are not one owner.

> The MCU executes HiMuon work, but it is a sibling physical authority and does not own HiMuon momentum.

> R8 creates the abstraction boundary that allows R8A to change momentum representation without reopening the entire HiMuon production call graph.
