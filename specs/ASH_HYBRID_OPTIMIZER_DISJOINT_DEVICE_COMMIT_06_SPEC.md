# ASH-HYBRID-OPTIMIZER-DISJOINT-DEVICE-COMMIT-06

## Muon + AdamW Full-Trainable Generation Commit Authority

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-HYBRID-OPTIMIZER-DISJOINT-DEVICE-COMMIT-06` |
| Parent B05 | `ASH-TENSORCUBE-HIMUON-DEVICE-CANDIDATE-05` |
| Parent B04 | `ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04` |
| Ownership SSOT | existing first-candidate optimizer routing registry |
| Full-generation authority | `HybridOptimizerCommitCoordinator` |
| Muon candidate source | B05 candidate ticket |
| AdamW candidate source | B06 AdamW candidate ticket ABI |
| Host mirror state | explicit `Fresh / Stale / Materializing` |
| Numerical evidence compaction | not introduced |
| Async wait removal | not introduced |
| Mixed precision | not introduced |
| Validation class in this bake | `STATIC_SOURCE_ONLY` |

### Current BaseTrain bake rollout status

This bake physically connects the **MirrorVerified full-generation coordinator** to the production scheduler and generation commit path.

The `ActiveVerified` ABI and no-fail metadata commit surface are present, but production activation is intentionally rejected until both of the following are real:

1. AdamW R6 produces an exact device-resident W/M/V candidate ticket with physical backing and zero bulk candidate readback.
2. the next optimizer step consumes `DeviceSegmentedGenerationV1` without silent per-step host materialization.

Therefore this bake does **not** claim that B06 Active device commit has been physically qualified. It establishes the authority boundary and makes a false Active promotion impossible.

---

## 1. Authority chain

```text
A01  submission completion authority
A02  physical allocation authority
A03  reusable transfer authority
B04  committed Muon weight/momentum authority
B05  Muon device candidate producer
B06  full trainable generation commit authority
```

B06 alone may declare:

```text
Full Trainable Generation N+1 committed
```

B04 may not independently advance a B05 device-sealed Muon generation.

---

## 2. Ownership invariant

The existing registry remains SSOT.

```text
MuonOwned + AdamWOwned = TotalTrainable
MuonOwned ∩ AdamWOwned = 0
Unclassified = 0
```

B06 does not recalculate optimizer ownership.

Runtime construction fails if:

```text
muonOwnedElements + adamwOwnedElements != totalTrainableElements
overlapElements != 0
unclassifiedElements != 0
```

---

## 3. Generation identity

B06 uses:

```rust
TrainableGenerationId {
    model_generation,
    optimizer_generation,
}
```

A normal successor advances both fields together.

```text
(model N, optimizer S)
        ↓
(model N+1, optimizer S+1)
```

Muon and AdamW candidates must share one source and one target generation.

---

## 4. Runtime modes

```text
OFF
MIRROR_VERIFIED
ACTIVE_VERIFIED
```

Required matrix:

| B04 | B05 | B06 | Admission |
|---|---|---|---|
| any | any | OFF | parent behavior |
| ACTIVE_VERIFIED | MIRROR_VERIFIED | MIRROR_VERIFIED | allowed |
| ACTIVE_VERIFIED | ACTIVE_DEVICE_CANDIDATE | ACTIVE_VERIFIED | allowed only with segmented device successor consumer |
| non-active | enabled | enabled | reject |
| MIRROR | ACTIVE | any non-active B06 | reject |

`B06 MirrorVerified` requires B04 Active and B05 Mirror.

`B06 ActiveVerified` requires B04 Active, B05 Active, and `DeviceSegmentedGenerationV1`.

---

## 5. B05 consumer capability

B05 no longer owns the decision about whether an active full-model consumer exists.

B06 exposes:

```text
b05_consumer_capability()
```

Rules:

```text
B06 OFF
→ None

B06 MIRROR_VERIFIED
→ MirrorHostApply

B06 ACTIVE_VERIFIED + DeviceSegmentedGenerationV1
→ HybridDeviceCommitV1
```

A boolean feature flag is not sufficient to forge `HybridDeviceCommitV1`.

---

## 6. AdamW candidate ABI

B06 defines:

```text
AdamWDeviceCandidateTicket
AdamWDeviceCandidateBacking
AdamWCanonicalRangeReceipt
```

A true Active AdamW candidate requires:

```text
candidate W physical allocation
candidate M physical allocation
candidate V physical allocation
exact submission epochs
compact status PASS
candidate W/M/V bulk D2H = 0
host candidate Vec materialization = 0
```

The three physical candidate allocations may not alias one another.

---

## 7. Mirror AdamW candidate

The current production scheduler still obtains AdamW candidate W/M/V through the existing R6 host-visible path.

B06 Mirror binds that existing result to the canonical ownership registry:

```text
registry parameter routes
        ↓
all AdamW-owned element counts
        ↓
AdamWCanonicalRangeReceipt set
        ↓
exact AdamW element coverage
```

Mirror candidate D2H remains non-zero by design and is recorded, not hidden.

---

## 8. Scheduler binding

After the optimizer candidate is fully produced, the production scheduler calls:

```text
stage_b06_adamw_host_candidate(...)
```

before generation publication.

The call binds:

```text
source model generation
source optimizer step
target model generation
target optimizer step
AdamW candidate readback bytes
AdamW candidate W/M/V readback counts
compact status readback bytes
registry-derived AdamW coverage
```

`B06 OFF` is a no-op.

`B06 ACTIVE_VERIFIED` rejects this host candidate staging path with:

```text
FAIL_B06_ADAMW_DEVICE_CANDIDATE_REQUIRED
```

There is no silent Active-to-Mirror fallback.

---

## 9. Full coverage permit

B06 creates `FullModelDeviceCommitPermit` only after both candidate authorities exist.

Required equality:

```text
B05 Muon written == MuonOwned
B06 AdamW written == AdamWOwned
MuonOwned + AdamWOwned == TotalTrainable
```

and:

```text
overlap = 0
unclassified = 0
duplicate = 0
missing = 0
```

The permit binds:

```text
source generation
target generation
Muon ticket digest
AdamW ticket digest
ownership digest
canonical layout digest
full coverage receipt
mode
```

---

## 10. Mirror commit path

Current physical BaseTrain path:

```text
B05 Mirror candidate sealed
        +
B06 AdamW host-mirror candidate staged
        ↓
B06 full coverage PREPARE
        ↓
existing filesystem / host candidate commit
        ↓
existing B04 host-verified Muon promotion
        ↓
B06 commit_mirror_after_host_apply
```

B06 records the resulting generation as:

```text
HostMirrorState::Fresh
DeviceSuccessorPublished = false
```

This mode proves coordinator identity and coverage without claiming device-only successor authority.

---

## 11. Active prepare/commit split

Active B06 is split into:

```text
PREPARE
↓
NO-FAIL METADATA COMMIT
```

All fallible checks belong to PREPARE:

```text
source/target generation
ownership
coverage
candidate seal
physical backing
submission completion
status
next-step device consumer
```

B04 exposes:

```text
prepare_b06_full_model_promotion(...)
commit_b06_prepared_promotion(...)
```

The second method does not return a fallible `Result` and performs only prevalidated role/generation swaps.

B06 similarly exposes:

```text
commit_active_metadata_no_fail(...)
```

No allocation, GPU submit, map operation, file I/O, or new digest calculation is permitted in the commit phase.

---

## 12. Muon candidate immutability

B06 consumes the B05 ticket.

It may not:

```text
rerun Local Muon
rerun FUSED_RIGHT
rerun FUSED_DOWN
rewrite sealed Muon candidate payload
create a second Muon momentum lineage
```

B04 remains the sole Muon state owner.

---

## 13. AdamW resident state target

The Active ABI reserves a distinct AdamW lineage:

```text
Committed Weight N
Committed M N
Committed V N
        ↓
Candidate Weight N+1
Candidate M N+1
Candidate V N+1
```

Weight/M/V promotion must be one generation transition.

The current bake does not falsely materialize this by wrapping host Vecs in a device-looking ticket. A true Active ticket requires physical backing IDs and submission epochs.

---

## 14. Host mirror state

B06 explicitly models:

```text
Fresh
Stale
Materializing
```

Active device commit publishes:

```text
HostMirrorState::Stale
```

A stale host mirror may not be read as canonical trainable state.

```text
FAIL_B06_STALE_HOST_MIRROR_READ
```

is mandatory.

---

## 15. Explicit materialization

Device committed state may be copied to host only at an explicit compatibility/durability boundary.

Lifecycle:

```text
Stale
→ begin_explicit_materialization()
→ Materializing
→ exact same generation materialized
→ finish_explicit_materialization()
→ Fresh
```

If the generation changes during materialization:

```text
FAIL_B06_DURABLE_GENERATION_SPLIT
```

---

## 16. No per-step host fallback

Active mode may not implement:

```text
device commit
→ automatically read entire model/state to host
→ next step
```

That would preserve the old bottleneck under a new name.

`per_step_host_materialization_count` must remain zero for Active promotion.

---

## 17. Durable boundary

Existing N8 invariant remains authoritative:

```text
steps 1..7
→ no durable pack publication

step 8
→ explicit exact-generation materialization
→ existing durable serializer/publication
```

B06 does not silently change checkpoint format or durability frequency.

---

## 18. Candidate vs committed-state D2H

Metrics must remain separate.

```text
candidate_d2h_bytes
!=
committed_materialization_d2h_bytes
```

Active target:

```text
Muon candidate bulk D2H = 0
AdamW candidate W D2H = 0
AdamW candidate M D2H = 0
AdamW candidate V D2H = 0
```

Explicit step-8 committed-state materialization may be non-zero.

---

## 19. C07 boundary

B06 does not introduce:

```text
GPU weight digest kernel
GPU M/V digest
Muon momentum digest
candidate checksum tree
numerical reduction evidence graph
```

Those belong to C07.

B06 evidence is structural:

```text
generation identity
ownership identity
coverage
candidate ticket identity
physical backing identity where available
status
```

---

## 20. C08 boundary

B06 does not remove A01 exact completion waits and does not add submission coalescing.

Async retirement belongs to C08.

---

## 21. Telemetry

At minimum:

```text
prepare / commit / reject count
Muon / AdamW / total element counts
overlap / unclassified / missing / duplicate counts
partial commit violation count
AdamW candidate W/M/V D2H
host candidate materialization count
committed materialization count / bytes
per-step host materialization count
stale host mirror read count
generation publication count
next-step consumer reject count
```

None of these are presented as physical VRAM measurements.

---

## 22. Failure classes

```text
FAIL_B06_RUNTIME_MODE_UNKNOWN
FAIL_B06_MODE_MATRIX

FAIL_B06_SOURCE_GENERATION_SPLIT
FAIL_B06_TARGET_GENERATION_SPLIT

FAIL_B06_OWNERSHIP_DIGEST_MISMATCH
FAIL_B06_CANONICAL_LAYOUT_MISMATCH
FAIL_B06_OWNERSHIP_OVERLAP
FAIL_B06_UNCLASSIFIED_TRAINABLE_RANGE
FAIL_B06_MISSING_TRAINABLE_RANGE
FAIL_B06_DUPLICATE_CANDIDATE_WRITE

FAIL_B06_ADAMW_ROW_MAP_DRIFT
FAIL_B06_ADAMW_COMMITTED_CANDIDATE_ALIAS
FAIL_B06_ADAMW_DEVICE_BACKING_MISSING
FAIL_B06_ADAMW_DEVICE_CANDIDATE_REQUIRED
FAIL_B06_ADAMW_BULK_READBACK_ACTIVE
FAIL_B06_HOST_CANDIDATE_AUTHORITY_ACTIVE

FAIL_B06_CANDIDATE_NOT_COMPLETE
FAIL_B06_CANDIDATE_STATUS_REJECTED

FAIL_B06_PARTIAL_OPTIMIZER_COMMIT
FAIL_B06_PARTIAL_PARAMETER_COMMIT

FAIL_B06_STALE_HOST_MIRROR_READ
FAIL_B06_PER_STEP_HOST_MATERIALIZATION
FAIL_B06_NEXT_STEP_DEVICE_CONSUMER_REQUIRED

FAIL_B06_DURABLE_GENERATION_SPLIT
FAIL_B06_DURABLE_MATERIALIZATION_RACE
```

---

## 23. Static source validation

The bake carries:

```text
tools/ash_hybrid_optimizer_disjoint_device_commit_06_static_validate.py
```

The static gate verifies:

```text
B06 module exported
ownership union hard gate exists
Host mirror state is explicit
B05 capability is B06-derived
B04/B05/B06 mode matrix is enforced
scheduler stages AdamW Mirror candidate
full commit permit binds Muon + AdamW
B04 no-fail prepared promotion surface exists
Active host candidate fallback is rejected
Active requires DeviceSegmentedGenerationV1
no C07 evidence kernel introduced
no C08 wait removal introduced
Cargo/WGSL surfaces remain parent-identical
```

`STATIC_SOURCE_ONLY` is not Rust compilation and is not physical GPU promotion.

---

## 24. Promotion criteria

### MirrorVerified qualification

```text
B04 Active = true
B05 Mirror = true
B06 Mirror = true

Muon coverage exact
AdamW coverage exact
Muon + AdamW = TotalTrainable
overlap = 0
unclassified = 0
missing = 0

legacy host apply remains authoritative
B04 promotion passes
B06 mirror generation publish passes
```

### ActiveVerified qualification

In addition to the above structural invariants:

```text
B05 Active = true
B06 Active = true

AdamW physical device candidate W/M/V present
all AdamW candidate submission epochs complete
Muon device candidate sealed

Muon bulk candidate D2H = 0
AdamW W/M/V candidate D2H = 0
host candidate Vec materialization = 0

DeviceSegmentedGenerationV1 consumer physically connected
per-step host materialization = 0

one full-generation metadata commit
host mirror marked Stale
```

The current bake does not claim the ActiveVerified physical qualification.

---

## 25. Current handoff

This bake closes the **full-generation commit authority and Mirror rollout path**.

The remaining work before Active promotion is not permission logic. It is physical adoption:

```text
R6 AdamW device-resident candidate backing
+
next-step segmented device generation consumer
```

Once that physical path exists, the B06 Active ABI already has the admission gates needed to prevent silent host reconstruction or partial optimizer promotion.

### Center declaration

> **Muon and AdamW may calculate different disjoint ranges, but they do not own different model generations. B06 is the only authority allowed to join those ranges into one trainable successor. Mirror mode proves that ownership and generation bookkeeping against the existing host path. Active mode is deliberately impossible until AdamW has real device backing and the next step can consume the segmented device generation without reconstructing the model on the host.**
