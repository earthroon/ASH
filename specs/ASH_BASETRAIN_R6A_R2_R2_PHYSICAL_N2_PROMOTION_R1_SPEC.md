# ASH-BASETRAIN-R6A-R2-R2-PHYSICAL-N2-PROMOTION-R1

## Status

Implementation-aligned promotion specification for the already completed physical N=2 BaseTrain run.

## Patch identity

```text
ASH-BASETRAIN-R6A-R2-R2-PHYSICAL-N2-PROMOTION-R1
```

## Core contract

```text
Physical N2 Evidence Admission /
Exact R5 Canonical Parent Binding /
Exact R6 Physical Run Binding /

GEN3→GEN5 Training Generation Closure /
OPT3→OPT5 Optimizer Step Closure /
CURSOR3→CURSOR19 Continuity Closure /

Accumulation8 × 2 Commit Authority /
16 Logical Microbatch Authority /
2 Physical Gradient Pass Authority /

R6 Receipt Chain Binding /
R6A Packed Runtime Binding /
R6A-R1 Native Wave Residency Binding /
R6A-R2 Micro-Atlas Paging Binding /
R6A-R2-R1 Canonical Genesis Reuse Binding /
R6A-R2-R2 Subgroup32 Gradient·AdamW Binding /

Physical N2 CF1 SourceTree·CargoLock·Binary Digest Binding /
R14 Fail-Closed Execution Closure /
Optional Exact Console Owner-Pin Evidence Binding /
No Fabricated R14 Persistent Sidecar Claim /

Physical State First /
Receipt Is Evidence, Not State /
No Receipt-to-State Reconstruction /
No Generation Synthesis /
No Optimizer-State Synthesis /
No Cursor Synthesis /

Exact Packed State Physical Verification /
Atomic Promotion Metadata Publication /
Previous Canonical Parent Preservation /
Failed Promotion Leaves Parent Unchanged /

No Training Replay /
No Optimizer Replay /
No Gradient Replay /
No Checkpoint Rewrite /
No Packed-State Rewrite /
No Silent State Repair /
No Silent Migration /
No Hidden Fallback /

Promoted GEN5·OPT5·CURSOR19 BaseTrain Parent Authority
```

---

## 1. Purpose

This patch does **not** execute N=2 again.

It promotes the existing physical state:

```text
R5 canonical parent
GEN3 / OPT3 / CURSOR next=3
        ↓
Accumulation8 × 2 optimizer commits
        ↓
GEN5 / OPT5 / CURSOR last=18 next=19 consumed=19
```

into the next explicit BaseTrain parent authority.

The promotion rule is:

> Receipts may prove the state, but they may not create the state.

If the physical GEN5 packed state is missing, inconsistent, or unverifiable, promotion is rejected.

---

## 2. Separate control-plane binary

Promotion is implemented as a dedicated Rust binary:

```text
ash_basetrain_physical_n2_promotion
```

It is intentionally separated from the training binary path.

The promotion binary may only:

```text
inspect
→ hash
→ bind
→ validate
→ publish promotion metadata
```

It must not invoke:

```text
forward
loss
backward
gradient replay
optimizer replay
training replay
checkpoint export
packed state rewrite
```

This separation prevents a promotion-only source change from pretending to be the physical N=2 training binary.

---

## 3. Physical source authority vs promotion control authority

The physical N=2 run remains bound to the exact CF1 identity that produced it:

```text
physicalSourceTreeDigest
physicalCargoLockDigest
physicalAuthoritativeBinarySha256
```

The later promotion-control source tree is a different authority layer.

Therefore promotion must verify:

```text
N2 runtime CF1 receipt
==
N2 compile CF1 receipt
```

for source-tree, Cargo.lock, and authoritative binary identity.

Promotion must **not** require the new promotion binary's source digest to equal the historical physical N=2 binary digest. Doing so would force an unnecessary N=2 replay merely because the post-hoc promotion tool was added.

---

## 4. R5 canonical parent authority

Required parent:

```text
schema = ash.basetrain.training_state.v2
trainingGeneration = 3
optimizerStep = 3
```

Required cursor:

```text
consumedBatchCount = 3
lastCommittedBatchOrdinal = 2
nextBatchOrdinal = 3
cursorRevision = 2
```

The R5 deterministic comparison receipt must also prove exact primary/shadow parity and generation3 promotion.

The parent active state is hashed before promotion and re-hashed before final commit. Any mutation rejects promotion.

---

## 5. Physical GEN5 state authority

Required N2 active state:

```text
schema = ash.basetrain.training_state.v3
trainingGeneration = 5
optimizerStep = 5
gradientAccumulation = 8
accumulatedMicrobatchCount = 8
```

Required cursor:

```text
trainingGeneration = 5
optimizerStep = 5
lastCommittedBatchOrdinal = 18
nextBatchOrdinal = 19
consumedBatchCount = 19
```

Required history chain:

```text
committed_training_state_step_000004.json
        ↓ parentTrainingStateDigest
committed_training_state_step_000005.json
        ==
active_training_state.json
```

The current training-state digest and cursor digest must be recomputed and verified.

---

## 6. Packed physical state verification

The active slot must be one of:

```text
slot_a
slot_b
```

The active state must point to:

```text
training_state/<slot>/packed_state_manifest.json
```

Required packed manifest:

```text
schema = ash.basetrain.packed_runtime_state.r6a.v1
publicationState = VALIDATED_READY_FOR_CANONICAL_POINTER
trainingGeneration = 5
optimizerStep = 5
parameterCount = 201
```

The packed manifest logical digest and physical manifest SHA256 must both validate.

The following payloads are read-only rehashed once for promotion verification:

```text
weight pack
Adam M pack
Adam V pack
```

For each payload:

```text
physical file size
== manifest declared size

physical SHA256
== manifest SHA256
== active training state SHA256
```

No payload is rewritten.

---

## 7. R6 execution authority

Required R6 receipt:

```text
source generation = 3
source optimizer step = 3
source cursor next = 3

gradient accumulation = 8
optimizer commits = 2
logical microbatches = 16

step #1 ordinals = 3..10
step #2 ordinals = 11..18

training generation after = 5
optimizer step after = 5
cursor last = 18
cursor next = 19
cursor consumed = 19
```

Required safety values:

```text
accumulatorNonfiniteCount = 0
productionGradientPayloadReadback = 0
canonicalWeightCommitCount = 2
optimizerStateCommitCount = 2
cursorCommitCount = 2
partialAccumulationAdoption = 0
checkpointExportFromUncommittedState = 0
```

---

## 8. R6A packed runtime authority

Required:

```text
packedRuntimeStateAdopted = 1
packedRuntimeGenesisAdoption = 1
productionLoopCommittedOptimizerSteps = 2
productionMicrobatchCount = 16
gradientAccumulation = 8
runtimePayloadFilesPerGeneration = 3
perParameterRuntimePayloadFileCount = 0
runtimeArenaCreateCount = 0
runtimeArenaRewriteCount = 0
postWriteDigestRereadBytes = 0
partialPackAdoption = 0
```

Final state must remain GEN5 / OPT5 / CURSOR19.

---

## 9. R6A-R1 native wave residency authority

Required:

```text
productionNativeRuntimeRequired = 1
productionInternalNativeBootstrap = 1
nativeRuntimeHandlesBound = 1
sameDeviceArcIdentity = 1
sameQueueArcIdentity = 1
logicalMicrobatchCount = 16
physicalGradientPassCount = 2
forwardWaveFanout = 8
backwardWaveFanout = 8
perMicrobatchAtlasPlanMaterialization = 0
```

This establishes the physical geometry:

```text
16 logical microbatches
→ 2 physical accumulated gradient passes
```

---

## 10. R6A-R2 micro-atlas authority

Required:

```text
deviceLimitPreflight = 1
microAtlasPageBytes = 16777216
microAtlasRingSlotCount = 3
oversizedBufferCreateAttemptCount = 0
multiSegmentTensorPlanAdopted = 1
fullEmbeddingGpuResidency = 0
fullLmHeadGpuResidency = 0
fullVocabWeightBufferMaterialization = 0
fullLogitsMaterialization = 0
microbatchInducedPageRefetchBytes = 0
```

---

## 11. R6A-R2-R1 canonical genesis reuse authority

Required:

```text
canonicalPathIdentityAdopted = 1
rawPathIdentityComparisonCount = 0
checkpointRangePhysicalFileDriftCount = 0
genesisCacheLookup = 1
duplicateGeneration3PackWriteCount = 0
r5SourceMutationCount = 0
genesisCacheMutationCount = 0
runtimeArenaCreateCount = 0
```

No synthetic GEN3 recreation is allowed.

---

## 12. R6A-R2-R2 subgroup32 gradient / AdamW authority

Required:

```text
requiredSubgroupSize = 32
subgroupSizeObserved = 32
subgroupExact32 = true
segmentNativeAdamw = true

gradientSegmentGapCount = 0
gradientSegmentOverlapCount = 0
gradientSegmentDuplicateCount = 0
fullParameterGradientBufferCreateCount = 0
fullParameterOptimizerMaterializationCount = 0
oversizedGradientBufferCreateAttemptCount = 0
gradientPayloadReadbackCount = 0
hardcodedRuntimeEvidenceFieldCount = 0
```

---

## 13. CF1 binding

Promotion binds both:

```text
external compile CF1 receipt
runtime measured CF1 closure from the physical N2 run
```

Required parity:

```text
sourceTreeDigest
cargoLockDigest
authoritativeBinarySha256
```

The physical run's CF1 identity is immutable evidence.

---

## 14. R14 closure under current persistence contract

### Current fact

Pass132 emits:

```text
[R14][owner-pin]
[R14][fault]
```

on the console, but does **not** persist a dedicated R14 sidecar receipt.

Therefore this patch must not fabricate:

```text
r14PersistentSidecarBound = 1
```

The candidate manifest explicitly records:

```text
r14PersistentSidecarBound = 0
```

### Fail-closed implication

The current R6 code calls owner-pin validation before each R14 backward and R14 backward returns an error on any non-zero fault status.

A fully completed R6 N=2 receipt chain therefore proves that all expected R14 calls crossed those fail-closed gates.

For this N=2 geometry:

```text
2 physical gradient passes
× 8 lanes
= 16 R14 executions
```

Promotion records:

```text
r14ExpectedLaneCount = 16
r14FailClosedExecutionCount = 16
r14OwnerPinValidationImpliedByCompletedR6Chain = 1
r14ZeroFaultImpliedByCompletedR6Chain = 1
```

### Optional exact console evidence

If `--r14-console-log-path` is supplied, promotion additionally parses the physical console log and requires exactly 16 owner-pin lines:

```text
lane 0..7 each appears exactly twice
expectedOwnerPinCount = 4
observedOwnerPinCount = 4
all four owner flags = true
rawOwnerIdentityValidated = true
unexpectedWritableAliasCount = 0
payloadReadbackCount = 0
totalRows = activeLossRows + 1
[R14][fault] count = 0
```

This is evidence binding, not state construction.

A future long-horizon patch should persist a first-class R14 sidecar authority rather than relying on console evidence.

---

## 15. Promotion output transaction

The final output path must not exist.

Promotion first writes to:

```text
<output>.partial/
```

with:

```text
promotion_candidate_gen5/promotion_manifest.json
physical_n2_promotion_receipt.json
promoted_parent_manifest.json
CURRENT_BASETRAIN_PARENT_POINTER.json
```

Only after all source mutation rechecks pass is the entire partial directory renamed to the requested final output directory.

A failed promotion leaves the previous canonical parent untouched.

---

## 16. Current parent pointer

The promotion pointer binds the existing physical N2 run, not copied state:

```text
stateKind = R6_PACKED_TRAINING_STATE
trainingGeneration = 5
optimizerStep = 5
cursorNextBatchOrdinal = 19
runRoot = <physical N2 run>
activeTrainingStatePath = <physical N2 active state>
```

The next N=8 run must resume from the promoted physical N2 run root.

---

## 17. No-replay / no-rewrite seal

Required final receipt values:

```text
physicalStateVerified = 1
receiptToStateSynthesisCount = 0
stateRewriteCount = 0
trainingReplayCount = 0
optimizerReplayCount = 0
previousParentMutation = 0
physicalN2SourceMutation = 0
promotionCommitCount = 1
```

---

## 18. PASS / HOLD

PASS:

```text
PASS_ASH_BASETRAIN_R6A_R2_R2_PHYSICAL_N2_PROMOTION_GEN5_OPT5_CURSOR19_R1
```

Normal next-stage HOLD:

```text
HOLD_ASH_BASETRAIN_PHYSICAL_N2_PROMOTED_GEN5_PARENT_READY_N8_LONG_HORIZON_NOT_YET_ADMITTED
```

The HOLD means promotion is complete and N=8 has not yet been admitted.

---

## 19. Next authority

After PASS, the BaseTrain parent is:

```text
GEN5
OPT5
CURSOR last=18 next=19 consumed=19
```

Next patch:

```text
ASH-BASETRAIN-N8-LONG-HORIZON-CONTINUITY-R1
```

must start from this promoted physical run using the existing R6 resume-state path rather than reconstructing state from promotion receipts.
