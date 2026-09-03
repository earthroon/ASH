# ASH-MCU-HIMUON-PACKED-GRADIENT-EXACT-MULTI-CONSUMER-SUBMISSION-LEASE-AND-ARENA-REUSE-CLOSURE-R7A1

## 0. Revision

```text
Patch ID:
ASH-MCU-HIMUON
-PACKED-GRADIENT-EXACT-MULTI-CONSUMER-SUBMISSION-LEASE
-AND-ARENA-REUSE-CLOSURE-R7A1

Short name:
ASH MCU HIMUON R7A1
PACKED-GRADIENT EXACT MULTI-CONSUMER LIFETIME + ARENA REUSE

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:                NOT CLAIMED
GPU physical PASS:                NOT CLAIMED
multi-consumer physical PASS:     NOT CLAIMED
arena reuse physical PASS:        NOT CLAIMED
```

Static token:

```text
PASS_ASH_MCU_HIMUON_PACKED_GRADIENT_EXACT_MULTI_CONSUMER_SUBMISSION_LEASE_AND_ARENA_REUSE_CLOSURE_R7A1_STATIC
```

Physical state:

```text
HOLD_ASH_MCU_HIMUON_PACKED_GRADIENT_R7A1_PHYSICAL_PENDING
```

## 1. Direct Parents

R7A1 consumes without redefining:

```text
MCU SESSION R7
MCU device-resource R7A
MCU child-ownership R7B
Trainable Session R4 / R4A
A01 SubmissionEpoch exact physical lifetime
A02 usage-segregated bounded arena
```

R7A1 changes packed-gradient physical allocation/lifetime tracking only. HiMuon mathematics, optimizer routing, R3C/R3C1 commit authority and BPDK semantic ownership are unchanged.

## 2. Historical R7A Truth Preserved

Historical R7A remains immutable:

```rust
MCU_R7A_HIMUON_PACKED_GRADIENT_CONSUMER_RETIREMENT_MATERIALIZED = false;
```

R7A1 adds a successor materialization flag rather than changing R7A history.

The historical gradient-packer `pack(...)` compatibility path remains and retains its conservative unknown submission semantics.

## 3. Problem Closed

Before R7A1 the packed-gradient output was direct-created and its producer used raw queue submission. Later GPU readers could read the same buffer through external-read A01 witnesses, so R7A could not prove when the physical allocation was safe to reuse.

The unsafe inference:

```text
pack producer complete -> packed-gradient page reusable
```

is forbidden.

R7A1 requires exact producer and reader lifetime evidence for the same physical allocation.

## 4. R7A1 Backend ABI

New backend module:

```text
burn_webgpu_backend::himuon_packed_gradient_r7a1
```

Materialized types include:

```text
PackedGradientReadBindingR7A1
PackedGradientProducerOutputR7A1
PackedGradientProducerReceiptR7A1
PackedGradientConsumerKindR7A1
```

The read binding carries exact:

```text
PhysicalAllocationId
QueueAuthorityId
R7A arena-domain digest
arena page ordinal
arena incarnation
logical byte range
identity digest
```

No pointer address participates in packed-gradient reuse identity.

## 5. Arena-backed Producer

`TensorCubeLocalMuonGradientPacker` gains:

```text
pack_tracked_r7a1(...)
```

The R7A1 producer:

```text
acquires packed output from the bounded R7A arena
preserves explicit clear-before-read initialization
uses A01 submit_with_leases
binds the output through OwnedExisting to the exact PhysicalAllocationId
records exact producer SubmissionEpoch
records exact producer LogicalLeaseId
returns a RawWgpuBufferLease carrying the R7A1 physical binding
```

The admitted R7A1 producer path does not use `A01_CONSERVATIVE_UNKNOWN_SUBMISSION`.

## 6. Exact Reader Cutover

R7A1 adds a backend helper that interprets an R7A1 packed-gradient binding and generates an exact A01 `OwnedExisting` read lease for the same PhysicalAllocationId and logical range.

The helper validates:

```text
queue authority
physical allocation
R7A arena domain
page ordinal
active arena incarnation
```

When no R7A1 binding is present, historical compatibility execution may retain the external-read path. Active R7A1 packed-gradient execution uses the exact binding.

## 7. Materialized Reader Coverage

The current R7A1 bake wires exact packed-gradient read leases through the existing execution paths used by:

```text
Local Muon execution
ActiveDevice pending Local Muon
P5 pending Local Muon
BPDK local observer GPU submission
BPDK bridge-pair observer GPU submission
fused-pair compatibility GPU submission
```

Paths layered on these tracked submit surfaces inherit the same exact physical read identity.

Physical campaign coverage of every production mode remains required before physical PASS.

## 8. A01 Physical-allocation Snapshot

A01 gains a read-only successor inspection surface that enumerates logical leases associated with one exact PhysicalAllocationId after refreshing completion state.

Each snapshot exposes at least:

```text
LogicalLeaseId
site identity
DeviceAuthorityId
QueueAuthorityId
completion coverage
retirement disposition
```

This is lifetime evidence. It does not inspect or hash packed-gradient contents.

## 9. Arena Incarnation Safety

A02 gains an R7A1 active-incarnation assertion.

A reader binding is rejected unless the exact arena page is still:

```text
in use
same R7A domain
same PhysicalAllocationId
same arena incarnation
```

A stale binding from incarnation N cannot authorize access or reclaim of incarnation N+1.

## 10. BaseTrain Lifetime Runtime

New BaseTrain module:

```text
base_train::mcu_himuon_packed_gradient_r7a1
```

Materialized:

```text
McuPackedGradientIdentityR7A1
McuPackedGradientPhaseR7A1
McuPackedGradientRuntimeR7A1
PackedGradientLifetimeReceiptR7A1
```

The identity binds source model/optimizer generation, canonical parameter, packed geometry, logical bytes, physical allocation and arena incarnation.

The current implementation is parameter-scoped inside ProductionMuon execution and uses R7B/R7A physical authorities. It is not claimed as a persistent field of `McuPhysicalGenerationRuntimeR7B` in this revision.

## 11. Multi-consumer Reclaim Rule

At parameter completion the R7A1 runtime queries all A01 logical leases associated with the packed-gradient PhysicalAllocationId.

Reclaim requires:

```text
exact producer logical lease present
at least one known tracked consumer lease
all associated leases have ExactTracked completion coverage
all associated leases have RetiredComplete retirement disposition
all leases refer to the same physical allocation
arena page/domain/incarnation still exact
```

Any live, conservative-unknown or contradictory lease blocks reclaim.

Only after the complete exact lease set is retired does R7A1 delegate final physical-page return to the R7A arena.

## 12. No Last-epoch or Count Shortcut

R7A1 does not prove reuse through:

```text
largest SubmissionEpoch
reader count only
function return
Arc drop
producer completion only
```

The normal proof is the complete A01 logical-lease set associated with the exact physical allocation.

## 13. Known-consumer Fail-closed Policy

The BaseTrain R7A1 runtime recognizes the current exact tracked packed-gradient reader site families materialized by this bake.

An unexpected tracked consumer identity causes reclaim failure rather than optimistic reuse.

A future new GPU reader must be added to the tracked lifetime contract before R7A1 physical promotion for that mode.

## 14. ProductionMuon Integration

R4A carries new default-OFF admission fields for:

```text
packed-gradient exact multi-consumer lease R7A1
packed-gradient arena reuse R7A1
```

Arena reuse requires exact multi-consumer tracking and requires the R7A bounded arena plus R7B generation-ownership parents.

When active, ProductionMuon obtains the R7A device arena domain/budget, calls `pack_tracked_r7a1`, creates one parameter-scoped `McuPackedGradientRuntimeR7A1`, executes the existing readers, drops the ordinary raw view and then performs exact seal/reclaim before normal transient parameter reclamation completes.

When disabled, the historical pack path remains.

## 15. No Premature Parameter/Generation Reuse

The R7A1 runtime is reclaimed at the parameter boundary only after exact A01 lifetime proof.

A live packed-gradient arena incarnation may not be silently carried into a different canonical parameter or reused by a later generation.

Physical idle R7A arena pages may of course be reused after exact retirement under a new incarnation.

## 16. Scope Limits

R7A1 does not yet claim:

```text
gradient-pack per-segment parameter-uniform pooling
bind-group caching
command-encoder pooling
all external gradients arena-backed
BPDK semantic state moved into MCU
fused-pair promoted into the common R7 production fabric
HiMuon momentum segmentation
multi-device execution
tensor parallelism
```

The gradient-packer kernel itself continues to benefit from R7A device kernel caching.

## 17. Numerical Contract

R7A1 changes no numerical mapping.

Required static claim:

```text
packed-gradient mapping changed = false
HiMuon mathematics changed = false
norm reduction changed = false
BPDK mathematics changed = false
R6/R7/R8/R8A execution ABI changed = false
```

R7A1 introduces no packed-gradient D2H and no full-content hash for lifetime proof.

## 18. Static Validation

Validator:

```text
tools/validate_ash_mcu_himuon_packed_gradient_exact_multi_consumer_submission_lease_arena_reuse_closure_r7a1_static.py
```

Current result:

```text
82 / 82 PASS
```

Token:

```text
PASS_ASH_MCU_HIMUON_PACKED_GRADIENT_EXACT_MULTI_CONSUMER_SUBMISSION_LEASE_AND_ARENA_REUSE_CLOSURE_R7A1_STATIC
```

The new R7A1 backend and BaseTrain modules contain no Rust `if` keyword; their new state/validation branching is expressed with `match`.

## 19. Parent Regression

Current bake retains static PASS for:

```text
MCU R7A                     73 / 73
MCU R7B                     78 / 78
Trainable Session R4A       65 / 65
Trainable Session R4        64 / 64
Eve R3G                     35 / 35
R3C                         18 / 18
R3C1                        30 / 30
R3D                         41 / 41
R3E                         52 / 52
R3F                         66 / 66
Unified Atlas MCU R6        PASS
Mixed-precision MCU R7      PASS
SubmissionEpoch active      PASS
```

Historical parent baselines remain unchanged:

```text
RAM exact inventory         66 / 67
N8 RAM resume-cut          117 / 118
```

Both reproduce on the direct R7B parent ZIP and are not R7A1 regressions.

## 20. Compile Boundary

The bake environment exposes no `cargo`, `rustc` or `rustfmt` executable.

Therefore Rust compile PASS and GPU physical PASS are not claimed.

The new Python validator passes `py_compile`; modified Rust files pass UTF-8 and structural balanced-delimiter checks.

## 21. Physical Qualification

Physical promotion requires real production workloads containing multiple packed-gradient GPU readers and must prove at minimum:

```text
producer exact A01 lease
all active GPU readers exact A01 OwnedExisting leases
same PhysicalAllocationId for producer/readers
same arena incarnation
producer and every reader RetiredComplete before reclaim
producer completion alone cannot reclaim
early-reuse fault is rejected
stale-incarnation fault is rejected
arena reuse hit observed after warm-up
retained arena bytes remain bounded
no direct packed-gradient allocation on active R7A1 path
no numerical divergence
```

Until then:

```text
HOLD_ASH_MCU_HIMUON_PACKED_GRADIENT_R7A1_PHYSICAL_PENDING
```

## 22. Direct Successor

After R7A1, the preferred structural successor is:

```text
ASH-HIMUON
-SESSION-RUNTIME-OWNERSHIP-SPLIT
-AND-MOMENTUM-EXECUTION-DURABILITY-SEPARATION-R8
```

R7B has already extracted physical MCU children. R7A1 closes the packed-gradient physical-lifetime exception. HiMuon semantic/momentum decomposition can therefore proceed without carrying unresolved packed-gradient reuse debt.

## 23. Final Law

> Producer completion proves the packed gradient exists. Complete exact reader retirement proves its physical allocation may be reused.

> A reusable packed-gradient page is free only when the entire A01 lease lineage for that exact PhysicalAllocationId and arena incarnation is retired.
