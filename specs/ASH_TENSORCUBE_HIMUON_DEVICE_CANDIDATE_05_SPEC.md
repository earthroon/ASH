# ASH-TENSORCUBE-HIMUON-DEVICE-CANDIDATE-05

## Canonical Device Candidate Authority / Local + HiMuon Direct Write / Bulk Candidate Readback Retirement Gate

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-TENSORCUBE-HIMUON-DEVICE-CANDIDATE-05` |
| Parent | `ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04` |
| Candidate source | B04 committed weight / committed Muon momentum |
| Candidate backing | B04 candidate weight / candidate momentum / update scratch slots |
| Candidate writers | `LOCAL`, `FUSED_RIGHT`, `FUSED_DOWN` |
| Host candidate authority | retired in `ACTIVE_DEVICE_CANDIDATE` |
| Candidate bulk D2H | zero in `ACTIVE_DEVICE_CANDIDATE` |
| Compact status D2H | preserved |
| Full-model commit | forbidden in B05 |
| Active production consumer | `HybridDeviceCommitV1` required |
| Current BaseTrain bake | `None` consumer, therefore Active is deliberately rejected until B06 |
| Qualification mode | `MIRROR_VERIFIED` |
| Validation class | `STATIC_SOURCE_ONLY` in this bake |
| Next patch | `ASH-HYBRID-OPTIMIZER-DISJOINT-DEVICE-COMMIT-06` |

B05 changes the candidate authority boundary:

```text
B04:
GPU candidate -> bulk readback -> host Vec candidate authority

B05 Active:
GPU candidate -> DeviceCandidateTicket -> B06 consumer
```

B05 does not independently promote the B04 generation.

---

## 1. SSOT split

```text
B04 = Muon committed/candidate generation and resident slot authority
B05 = canonical device-candidate write-plan and producer-ticket authority
B06 = full-model Muon + AdamW atomic commit authority
```

B05 may produce a sealed Muon candidate. It may not decide that the full model generation is committed.

---

## 2. Canonical address is three-dimensional

The B04 physical backing is not a single contiguous full-model buffer. Local and fused domains use packed resident partitions.

Therefore B05 seals three distinct address axes:

```text
1. canonical Muon packed address
   momentum_base_element_offset + tile_ordinal * 256

2. canonical model projection
   model row/column projection for the 16x16 tile

3. physical B04 partition address
   partition identity + partition element offset + allocation identity
```

These axes must not be collapsed.

In particular:

```text
physical partition offset != canonical model linear address
```

This separation prevents edge residual AdamW-owned elements from being falsely admitted as Muon candidate writes.

---

## 3. Canonical Muon ownership

Existing optimizer routing remains the ownership SSOT.

Required invariant:

```text
Muon-owned + AdamW-owned = total trainable elements
Muon/AdamW overlap = 0
unclassified = 0
```

B05 only writes full 16x16 Muon tiles already admitted by that routing.

Any candidate segment outside the parameter's canonical Muon packed interval is rejected as:

```text
FAIL_B05_ADAMW_RANGE_INTRUSION
```

B05 does not create a new ownership planner.

---

## 4. Device-candidate runtime modes

```rust
pub enum MuonDeviceCandidateRuntimeMode {
    Off,
    MirrorVerified,
    ActiveDeviceCandidate,
}
```

### Off

B04 behavior.

### MirrorVerified

The executor writes directly into the B04 candidate slots and exposes exact backing/submission metadata, while existing bulk readback and host candidate materialization remain enabled.

Purpose:

```text
direct device backing
==
legacy host-visible candidate
```

without a second compute pass.

### ActiveDeviceCandidate

The same direct B04 candidate backing is used, but candidate weight, candidate momentum, and orthogonal update bulk readback paths are disabled.

Required steady-state values:

```text
candidate weight D2H = 0
candidate momentum D2H = 0
orthogonal update D2H = 0
host candidate Vec materialization = 0
```

Compact status readback remains.

---

## 5. Consumer capability gate

```rust
pub enum DeviceCandidateConsumerCapability {
    None,
    MirrorHostApply,
    HybridDeviceCommitV1,
}
```

`ACTIVE_DEVICE_CANDIDATE` requires:

```text
HybridDeviceCommitV1
```

The current B05 BaseTrain bake deliberately initializes with:

```text
DeviceCandidateConsumerCapability::None
```

because B06 has not been baked yet.

Therefore requesting Active now fails before training advancement with:

```text
FAIL_B05_DEVICE_COMMIT_CONSUMER_REQUIRED
```

This is intentional. It prevents Muon generation N+1 from being committed while AdamW-owned ranges remain at generation N.

---

## 6. B04 candidate slots are the only persistent candidate backing

B05 does not allocate a second persistent candidate cache.

```text
B04 candidate weight slot
B04 candidate momentum slot
B04 update scratch
        ↓
B05 device candidate backing
```

A backing record includes:

```text
partition kind
partition key digest
source generation
candidate generation
element count
candidate weight allocation identity
candidate momentum allocation identity
update scratch allocation identity
```

`LOCAL` and `FUSED_PAIR_SET` backings are distinct physical partitions but one semantic Muon candidate generation.

---

## 7. No second momentum lineage

The only Muon momentum chain is:

```text
B04 committed momentum N
        ↓
B04 candidate momentum N+1
        ↓
B06-authorized promotion
```

Forbidden persistent authorities include:

```text
HiMuonMomentumState
FusedMomentumCache
DeviceCandidateMomentumCache
```

B05 only binds writes to the B04 candidate momentum allocation.

---

## 8. Write-plan derivation

The B05 write plan is derived from:

```text
existing optimizer ownership registry
+
existing fusion execution plan
+
B04 resident partition backing
```

It does not create a new fusion planner.

### Local

`local_tiles` are sorted in the same canonical order used by the production executor.

Physical packed offset:

```text
local_index * 256
```

### Fused pair set

Fused pairs are sorted by the same pair key used by the production executor.

Physical packed offsets:

```text
pair_index * 512 + side * 256
```

The writer is derived from pair adjacency:

```text
Right -> FUSED_RIGHT
Down  -> FUSED_DOWN
```

Pair discovery order never becomes model address authority.

---

## 9. Candidate write segment

Each logical tile write seals:

```text
parameter identity
canonical parameter index
writer domain
canonical Muon packed start
256-element count
model projection start / row stride / 16x16 shape
B04 partition key
partition element start
candidate weight allocation
candidate momentum allocation
update scratch allocation
```

A segment does not claim its physical partition is a contiguous full-model address.

---

## 10. Coverage truth

Per parameter:

```text
written Muon elements == expected Muon elements
```

and all of the following must be zero:

```text
canonical gaps
duplicate canonical writes
physical range overlaps
AdamW intrusion
```

The generation-level seal additionally requires the sum of all parameter coverage to equal:

```text
registry.muon_eligible_element_count
```

This prevents a whole parameter from disappearing while the remaining parameters individually pass.

---

## 11. Physical overlap truth

Canonical non-overlap is not enough.

B05 also validates physical B04 partition offsets by allocation identity.

Two live candidate writes may not overlap the same weight or momentum allocation range.

The candidate weight, candidate momentum, and update scratch allocation identities must be distinct within a partition backing.

---

## 12. Executor ABI

Local and fused executors expose resident device-candidate entrypoints.

They still use:

```text
B04 committed source weight
B04 committed source momentum
```

and write the existing B04 candidate slots.

In Mirror mode they also create/copy/map bulk readback buffers.

In Active mode these three bulk paths are absent:

```text
candidate weight readback
candidate momentum readback
orthogonal update readback
```

Status remains an A03 compact whole-buffer readback.

---

## 13. Submission completion

Every device-candidate backing is accompanied by exact A01 `SubmissionEpoch` evidence.

The producer ticket may be sealed only after executor paths have completed their existing exact submission wait and compact status validation.

B05 does not introduce an alternate completion clock.

---

## 14. Compact status is not payload evidence

B05 reuses existing compact status semantics.

It must not claim that status proves candidate byte equality or candidate digest identity.

New GPU-side digest, norm reduction, checksum, or evidence trees are reserved for C07.

---

## 15. Mirror qualification

`MIRROR_VERIFIED` is the qualification route before B06 activation.

It requires:

```text
candidate weight bulk D2H > 0
candidate momentum bulk D2H > 0
update bulk D2H > 0
host candidate Vec materialization > 0
```

while the exact candidate slots/backing identities and submission epochs are simultaneously recorded.

The existing host verification and B04 promotion path remains authoritative in this mode.

---

## 16. Active candidate producer

Active output is a device ticket rather than host candidate vectors.

The ticket seals:

```text
source generation
candidate generation
ownership digest
per-parameter write-plan digests
expected/written Muon element counts
exact submission epochs
full-model-commit requirement
```

The ticket is an execution/generation identity, not a cryptographic digest of candidate payload bytes.

---

## 17. Autonomous promotion is forbidden

B04 carries an explicit B05 seal state.

A device-sealed B05 candidate cannot pass `B04::promote_generation()` unless a later full-model device-commit authorization has been registered.

Current B05 BaseTrain therefore refuses Active rather than silently falling back to host readback or independently promoting Muon state.

Forbidden:

```text
Active failure -> silently turn bulk readback back on
Active candidate -> directly promote B04
Muon N+1 -> advance while AdamW remains N
```

---

## 18. Host authority retirement scope

In Active mode:

```text
candidate_weight: Vec<f32>      = empty
candidate_momentum: Vec<f32>    = empty
orthogonal_update: Vec<f32>     = empty
```

The production B05 bake does not enable that mode without B06 because current higher-level post-update/counterfactual/durable model flows still consume host-visible candidate data.

That dependency is surfaced as an explicit consumer gate rather than hidden fallback.

---

## 19. B04 parent preservation

B05 must preserve all B04 truths:

```text
committed weight immutable during candidate execution
committed momentum immutable during candidate execution
single source/candidate generation chain
whole Muon generation coverage
F32 master state
A01 slot lifetime
A02 physical backing
A03 transfer/status authority
```

`MIRROR_VERIFIED` preserves the B04 host-verified promotion path exactly.

---

## 20. Telemetry

B05 records:

```text
candidate prepare/seal/reject counts
Mirror and Active execution counts
Muon elements written by Local / FusedRight / FusedDown
range gap / duplicate / overlap / AdamW intrusion counts
candidate weight/momentum/update D2H bytes
compact status D2H bytes
host candidate Vec materialization count
source weight/momentum H2D bytes
momentum lineage split count
autonomous promotion rejection count
missing commit consumer count
stale attempt count
```

Source H2D counters include bootstrap traffic. B04 remains the authority for the separate steady-state source-state H2D=0 claim.

---

## 21. Active success target

After B06 supplies `HybridDeviceCommitV1`, an Active B05 steady-state run targets:

```text
candidateWeightD2HBytes = 0
candidateMomentumD2HBytes = 0
updateD2HBytes = 0
hostCandidateVecMaterializationCount = 0

B04 steady-state sourceWeightH2DBytes = 0
B04 steady-state sourceMomentumH2DBytes = 0

rangeGapCount = 0
duplicateWriteCount = 0
physicalOverlapCount = 0
adamwIntrusionCount = 0
momentumLineageSplitCount = 0
```

Compact status bytes may remain nonzero.

---

## 22. Static source validator

The code bake includes:

```text
tools/ash_tensorcube_himuon_device_candidate_05_static_validate.py
```

It validates source contracts including:

```text
B05 module/export exists
B04 backing adoption exists
three-axis address description is represented in code
Local and Fused device-candidate APIs exist
Mirror/Active bulk-readback split exists
compact status remains
B04 autonomous-promotion guard exists
BaseTrain consumer capability is currently None
BaseTrain records Mirror device-candidate coverage
B04 parent validator still passes
no Cargo.toml change
no WGSL change
no new persistent HiMuon momentum authority
```

This validator is `STATIC_SOURCE_ONLY`. It does not claim Rust type-check, WGPU validation, numerical parity, or physical GPU execution.

---

## 23. Promotion gate

B05 physical promotion requires a target GPU run proving Mirror parity first.

```text
B04 parent = PASS
Mirror Local candidate parity = PASS
Mirror fused candidate parity = PASS
canonical coverage = exact
physical backing coverage = exact
compact status parity = PASS
no ownership intrusion
no generation drift
```

Active production promotion additionally requires B06 consumer capability and:

```text
candidate weight D2H = 0
candidate momentum D2H = 0
update D2H = 0
host candidate Vec materialization = 0
B05 autonomous promotion = 0
```

The current bake intentionally stops before that final Active promotion because B06 does not yet exist.

---

## 24. Failure classes

```text
FAIL_B05_SOURCE_GENERATION_MISMATCH
FAIL_B05_CANONICAL_LAYOUT_MISMATCH
FAIL_B05_OWNERSHIP_DIGEST_MISMATCH
FAIL_B05_WRITE_PLAN_DRIFT
FAIL_B05_CANONICAL_RANGE_GAP
FAIL_B05_DUPLICATE_CANDIDATE_WRITE
FAIL_B05_PHYSICAL_WRITE_OVERLAP
FAIL_B05_ADAMW_RANGE_INTRUSION
FAIL_B05_CANDIDATE_COMMITTED_ALIAS
FAIL_B05_STALE_CANDIDATE_BACKING
FAIL_B05_MOMENTUM_LINEAGE_SPLIT
FAIL_B05_CANDIDATE_NOT_PHYSICALLY_COMPLETE
FAIL_B05_COMPACT_STATUS_REJECTED
FAIL_B05_BULK_READBACK_ACTIVE
FAIL_B05_HOST_VEC_AUTHORITY_ACTIVE
FAIL_B05_AUTONOMOUS_PROMOTION
FAIL_B05_DEVICE_COMMIT_CONSUMER_REQUIRED
FAIL_B05_STALE_CANDIDATE_ATTEMPT
FAIL_B05_DEVICE_MISMATCH
FAIL_B05_QUEUE_MISMATCH
FAIL_B05_EVIDENCE_AUTHORITY_INTRUSION
```

---

## 25. B06 handoff

B05 leaves one deliberate missing authority:

```text
Muon candidate generation N+1 = device sealed
AdamW-owned candidate ranges   = not yet device committed
```

B06 must consume the B05 ticket, write the disjoint AdamW candidate ranges, verify complete trainable coverage, and authorize one full-model generation commit.

### Center declaration

> **B04 kept Muon's current state on the device. B05 keeps its next state there too. Local, FUSED_RIGHT, and FUSED_DOWN write one canonical Muon candidate generation directly into the existing B04 candidate slots; host vectors cease to be candidate authority in Active mode. But a sealed Muon candidate is not a committed model. Until B06 seals the disjoint AdamW ranges and authorizes one full-model generation, B05 is a producer, not a committer.**
