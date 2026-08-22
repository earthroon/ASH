# ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04

## Resident Muon Weight/Momentum Generation Graph / Source-State H2D Retirement

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04` |
| Parent A01 | `ASH-VENDOR-WGPU-SUBMISSION-EPOCH-LEASE-01` |
| Parent A02 | `ASH-VENDOR-WGPU-USAGE-SEGREGATED-ARENA-02` |
| Parent A03 | `ASH-VENDOR-WGPU-STAGING-AND-COMPACT-READBACK-RING-03` |
| Primary role | Muon committed weight/momentum device residency and generation promotion |
| Default runtime mode | `OFF` |
| Physical promotion mode | `ACTIVE_VERIFIED` |
| State dtype | `F32` only |
| Candidate bulk readback | preserved |
| Host candidate verification | preserved |
| Filesystem/model commit | remains upstream of resident promotion |
| AdamW M/V | outside B04 authority |
| Next patch | `ASH-TENSORCUBE-HIMUON-DEVICE-CANDIDATE-05` |

B04 changes the optimizer-state time axis. A03 made repeated host→device transport reusable. B04 removes the repeated Muon source-state transport itself for a stable resident lineage.

---

## 1. Authority chain

```text
A00 semantic inventory
      ↓
A01 GPU completion / lease lifetime
      ↓
A02 physical allocation reuse
      ↓
A03 reusable host↔device transport
      ↓
B04 Muon committed-state residency
```

SSOT split:

```text
Global model parameter authority
= existing BaseTrain/model generation authority

Muon hotpath source weight for an exactly bound generation
= B04 resident graph

Muon momentum hotpath authority
= B04 resident graph

Physical buffer lifetime
= A01 + A02

Bootstrap transfer
= A03
```

B04 must not create a second independent AdamW state authority or a second mutable Muon weight cache.

---

## 2. Core state rule

For a Muon model generation `N`:

```text
CommittedWeight[N]
CommittedMomentum[N]
```

are immutable while candidate generation `N+1` is computed into distinct slots:

```text
CandidateWeight[N+1]
CandidateMomentum[N+1]
UpdateScratch[N+1]
```

Promotion is metadata-atomic across weight and momentum. In-place mutation of the committed pair is forbidden.

Required generation relation:

```text
candidateGeneration = sourceGeneration + 1
```

No generation jump is admitted.

---

## 3. Resident graph key

The graph key is derived from:

```text
parameter identity
canonical parameter index
stable fusion execution layout digest
packed layout digest
optimizer ownership partition digest
```

### Stable fusion layout digest

B04 deliberately does **not** use the full `AshBpDkFusionExecutionPlan::plan_digest` as resident identity. The full plan identity carries generation/evidence state and may legitimately change while the physical execution topology remains identical.

B04 therefore hashes the canonical `plan.domains` execution layout. This digest contains Local/Fused domain ordering and pair topology without making current-generation evidence part of the persistent resident-state identity.

If this stable execution layout changes, B04 fails closed with:

```text
FAIL_B04_FUSION_PLAN_DRIFT
```

B04 v1 does not silently remap an active resident graph in place.

---

## 4. Physical partition model

A parameter may have up to two B04 resident physical partitions in the current production topology:

```text
Local
FusedPairSet
```

`FusedPairSet` intentionally preserves the existing fused executor call topology. A single executor call may contain both `FUSED_RIGHT` and `FUSED_DOWN` pair descriptors. B04 does not split those orientations into independent optimizer histories merely to make the state graph look symmetrical.

Therefore:

```text
Local + FusedPairSet
= one semantic Muon parameter generation
```

and the individual pair descriptors still carry exact Right/Down orientation.

No Local/Fused partition may promote independently.

---

## 5. Whole-graph capacity admission

ActiveVerified requires an explicit budget:

```text
ASH_MUON_RESIDENT_STATE_MODE=ACTIVE_VERIFIED
ASH_MUON_RESIDENT_STATE_BUDGET_BYTES=<explicit bytes>
```

The first static preflight is:

```text
required requested bytes
=
MuonEligibleElements × 4 bytes × 5 state surfaces
```

The five F32 surfaces are:

```text
Committed Weight
Candidate Weight
Committed Muon Momentum
Candidate Muon Momentum
Update Scratch
```

ActiveVerified is rejected before physical graph construction when the configured budget is smaller than this whole-graph requested-byte requirement.

This number is **not** labeled physical VRAM usage. A02 alignment/reservation and the WGPU allocator remain separate physical layers.

---

## 6. Whole-generation promotion closure

B04 promotion is not satisfied merely because every partition that happened to run reports PASS.

Before promotion, the graph sums all candidate partition elements for the target generation and requires:

```text
candidate target element coverage
=
registry.muon_eligible_element_count
```

This closes the case where an entire Muon parameter could otherwise be omitted from the resident graph while the remaining parameters promote successfully.

Failure:

```text
FAIL_B04_PARTIAL_STATE_PROMOTION
```

---

## 7. A02 persistent slot relationship

B04 acquires persistent state surfaces from the A02 arena but does not return them after every executor call.

```text
A02 ArenaLease
       ↓
B04 resident slot keeps physical ownership
       ↓
per submission A01 range lease opens/closes
       ↓
physical slot remains resident across optimizer generations
```

This prevents A02 page trimming from reclaiming a committed optimizer state merely because one submission has completed.

B04 state surfaces use A02-owned `PhysicalAllocationId` and A01 `owned_existing_range` leases for every physical batch.

---

## 8. Bootstrap

A newly created resident partition requires exactly one bootstrap of its committed state:

```text
Host Weight[N]
Host Muon Momentum[N]
      ↓
A03 BulkState staging
      ↓
B04 Committed Weight/Momentum slots
```

Bootstrap is recorded into the same command encoder as the consuming compute submission.

After a partition is initialized, re-uploading committed state into the same generation is a committed-state mutation violation.

### Existing generation-sealed cache

The pre-B04 generation-sealed Muon cache remains present for OFF/compatibility execution and structural cache behavior.

B04 v1 deliberately does not zero-copy adopt the old weight-cache backing allocation into the mutable ping-pong graph because that cache does not share B04's A02 persistent-slot ownership contract. Silent dual ownership would be worse than one explicit bootstrap.

No second continuously updated weight cache is created.

---

## 9. Steady-state source authority

After bootstrap and successful generation promotion:

```text
Muon source weight H2D = 0
Muon source momentum H2D = 0
```

for the steady B04 resident path.

The BaseTrain caller may still possess host copies for durability, replay, counterfactual analysis, or legacy compatibility, but the production ActiveVerified executor receives an empty source bootstrap slice and binds the committed resident buffers as the actual GPU inputs.

This is the authority change introduced by B04.

---

## 10. Local Muon resident execution

`TensorCubeLocalMuonBatchExecutor` exposes a dedicated resident-graph execution path.

For each physical batch it binds a byte range of the persistent partition:

```text
CommittedWeight  → READ
CommittedMomentum → READ
CandidateWeight → READWRITE
CandidateMomentum → READWRITE
UpdateScratch → READWRITE
```

A01 tracks the exact byte range against the persistent physical allocation ID. The range offset is the current packed batch offset, not zero unless the batch actually begins at zero.

Candidate/readback behavior remains unchanged.

---

## 11. Fused HiMuon resident execution

`TensorCubeFusedPairMuonExecutor` uses the same B04 graph contract.

The resident fused physical partition is packed in the same canonical pair order used by the existing fused callsite. Each pair still carries its explicit Right/Down descriptor.

B04 changes source and candidate storage, not fused math, workgroup geometry, pair orientation, or the planner's physical execution truth.

---

## 12. Candidate readback is intentionally preserved

B04 keeps:

```text
candidate weight D2H
candidate Muon momentum D2H
orthogonal update D2H
status D2H
```

The host vectors remain the input to the existing BaseTrain validation, post-update evidence, replay/counterfactual checks, and model/filesystem apply path.

Therefore this is a valid B04 state:

```text
steadyStateWeightH2DBytes = 0
steadyStateMomentumH2DBytes = 0

candidateWeightD2HBytes > 0
candidateMomentumD2HBytes > 0
updateD2HBytes > 0
```

Bulk candidate D2H retirement belongs to B05/C07, not B04.

---

## 13. Host verification binding

After the existing candidate validation/evidence path succeeds, BaseTrain seals the resident parameter candidate as host-verified using:

```text
parameter identity
stable fusion layout digest
packed layout digest
optimizer ownership digest
source generation
candidate generation
host candidate weight digest
```

Every expected resident physical partition for that parameter must already be physically complete.

Host verification is not promotion.

---

## 14. Promotion ordering

Canonical ordering:

```text
GPU candidate complete
        ↓
existing bulk readback
        ↓
existing host validation / evidence
        ↓
host candidate apply / filesystem generation commit
        ↓
filesystem commit witness exists
        ↓
B04 promote_generation(target)
        ↓
atomic Weight/Momentum role swap
```

B04 promotion is invoked only during generation transaction finalization, after the existing filesystem commit witness has been sealed.

Promotion uses the filesystem candidate-parameter-set digest as the non-empty host-apply witness binding.

A resident candidate may never advance ahead of the committed model generation.

---

## 15. Atomic ping-pong promotion

Promotion swaps:

```text
CommittedWeight ↔ CandidateWeight
CommittedMomentum ↔ CandidateMomentum
```

for every target-generation partition only after all promotion gates pass.

Then:

```text
committedGeneration = targetGeneration
candidateGeneration = targetGeneration + 1
physicalComplete = false
hostVerified = false
```

for the next cycle.

There is no separate weight-only or momentum-only promotion API.

---

## 16. Abort

Generation abort does not mutate committed slots.

For the aborted target generation:

```text
Candidate physical-complete seal → cleared
Host-verified seal → cleared
Committed weight/momentum → unchanged
```

The persistent candidate slots may be overwritten by a later retry only after the failed generation has passed through the explicit abort boundary.

---

## 17. Fusion/layout drift policy

B04 v1 is deliberately fail-closed on live resident-layout drift:

```text
fusion execution layout change
packed layout change
optimizer ownership partition change
```

results in an explicit error before allocating a competing second resident layout for the same parameter.

There is no silent host rebootstrap fallback in ActiveVerified.

A process/device restart naturally reconstructs the graph from durable host state. A future rebind revision may add an explicit in-process retirement/rebootstrap transaction after A01/A02 lifetime proof, but that is not silently fabricated in B04 v1.

---

## 18. Device/process authority

B04 physical IDs and A02/A01 leases are process-local runtime state.

Forbidden:

```text
serialize PhysicalAllocationId into checkpoint
serialize ArenaPageId into checkpoint
reuse a resident graph after process restart
reuse an old-device graph after device replacement
```

A new process or device requires a new resident graph bootstrap from durable/model state.

---

## 19. AdamW isolation

B04 owns Muon state only.

```text
Muon Momentum != AdamW first moment M
Muon Momentum != AdamW second moment V
```

AdamW M/V must never enter `MuonResidentStateGraph`.

B06 is responsible for the later hybrid atomic device commit while keeping both optimizer state lineages disjoint.

---

## 20. Runtime modes

```text
OFF
SHADOW
ACTIVE_VERIFIED
```

### OFF

A03 production behavior is preserved.

### SHADOW

B04 v1 reserves the configuration value but does not mutate or allocate resident state in the production callsite. It is a non-active compatibility mode, not a fabricated residency claim.

### ACTIVE_VERIFIED

The production primary Muon execution uses the resident graph. Replay and counterfactual executions deliberately remain on the existing non-authoritative path so they cannot write or promote the primary resident candidate slots.

This is enforced by activating B04 only for the primary physical fusion execution path.

---

## 21. Telemetry

B04 exports counters for:

```text
graph bootstrap
rebootstrap (reserved, fail-closed v1 normally remains zero)
promotion
rejection
partial-promotion rejection
resident partition count
requested/reserved bytes
bootstrap weight H2D
bootstrap momentum H2D
steady-state weight H2D
steady-state momentum H2D
candidate weight D2H
candidate momentum D2H
update D2H
committed-state mutation violation
host-verified parameter count
```

The graph telemetry is mirrored into `ProductionMuonExecutionCounters` so the existing production receipt surface can carry the B04 observations without inventing a parallel telemetry owner.

---

## 22. Parent A03 correction included in this bake

During the B04 bake, the supplied A03 parent was found to reference Local Muon `candidate_weight_arena`, `candidate_momentum_arena`, and `update_arena` after their acquisition declarations had been dropped during the prior staging migration.

B04 restores those A02 acquisitions for the non-B04 path before layering the resident graph on top.

This correction is explicit because leaving it untouched would preserve a likely Rust compile regression rather than preserve parent semantics.

B04 does not change the intended A03 authority boundary by making this repair.

---

## 23. Static source gate

The bake includes:

```text
tools/ash_tensorcube_muon_resident_state_graph_04_static_validate.py
```

The gate verifies at minimum:

```text
B04 module/export present
F32 ping-pong surface count = 5
contiguous generation rule
whole-Muon element coverage before promotion
whole-graph explicit ActiveVerified budget
A02-owned persistent surfaces
A01 owned-existing range tracking
A03 bootstrap staging
Local resident execution path
Fused resident execution path
primary-only production adoption
steady source slices may be empty after bootstrap
bulk candidate readback remains present
host verification precedes production momentum commit
filesystem witness precedes resident promotion
abort resets candidate, not committed state
AdamW state is absent from B04 graph
no mixed precision authority
no async wait removal
A03 Local candidate-arena parent regression repaired
Cargo/WGSL surfaces unchanged from the supplied A03 parent
```

`STATIC_SOURCE_ONLY` is not Rust type-check and not a physical GPU promotion.

---

## 24. Promotion gate

Physical B04 promotion requires a real target run proving:

```text
A01 valid
A02 valid
A03 valid

whole graph capacity admitted
whole Muon candidate element coverage exact

bootstrap count >= 1
promotion count >= 1
partial promotion count = 0

steady-state source weight H2D = 0
steady-state source momentum H2D = 0

committed-state mutation violation = 0

Local candidate parity = true
Fused candidate parity = true

candidate bulk readback semantics unchanged
host/model/filesystem commit succeeds before resident promotion
```

No static validator may claim these physical runtime facts on its own.

---

## 25. B05 handoff

After B04:

```text
SOURCE
GPU resident

CANDIDATE
GPU resident internally
but bulk-copied to Host for authority/verification
```

B05 can now remove the host-vector candidate ABI without also solving source-state residency in the same patch.

The next authority target is:

```text
ASH-TENSORCUBE-HIMUON-DEVICE-CANDIDATE-05
```

where Local/Fused candidate destinations remain GPU-native and host receives only explicitly admitted verification evidence.

### Center declaration

> B04 promotes Muon source-state residency, not device-only candidate authority. The committed weight/momentum pair remains immutable while a complete next generation is written into distinct persistent slots. Local and FusedPairSet are physical partitions of one semantic Muon generation. Existing host verification and model/filesystem commit remain the promotion gate, and only after that gate passes may the resident weight and momentum roles swap together.
