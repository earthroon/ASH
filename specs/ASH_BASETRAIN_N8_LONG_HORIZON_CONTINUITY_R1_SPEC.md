# ASH-BASETRAIN-N8-LONG-HORIZON-CONTINUITY-R1

## Status

Implementation-aligned specification for the first continuous long-horizon BaseTrain run after Physical N2 Promotion.

## Patch identity

```text
ASH-BASETRAIN-N8-LONG-HORIZON-CONTINUITY-R1
```

## Core contract

```text
Promoted GEN5 Parent Admission /
Physical N2 Promotion Pointer Binding /
Physical GEN5 Packed-State Direct Resume /

Single-Process Continuous N8 Authority /
Accumulation8 × 8 Optimizer Commit Authority /
64 Logical Microbatch Authority /
8 Physical Accumulated Gradient Pass Authority /

GEN5→GEN13 Training Generation Continuity /
OPT5→OPT13 Optimizer Step Continuity /
CURSOR19→CURSOR83 Dataset Cursor Continuity /

Exact Per-Step Generation·Optimizer·Cursor Coupling /
No Batch Gap /
No Batch Duplicate /
No Cursor Skip /
No Partial Accumulation Commit /

R14 64-Lane Persistent Long-Horizon Authority /
R14 Owner-Pin 4-of-4 Continuity /
R14 Raw Owner Identity Continuity /
R14 Writable-Alias Zero Continuity /
R14 Zero-Fault Attribution Closure /

Per-Step Loss Observation Ledger /
Per-Step Gradient Norm Ledger /
Per-Step Update Norm Ledger /
No Cross-Batch Loss Improvement Assumption /

Packed Runtime State Continuity /
Micro-Atlas Residency Continuity /
Subgroup32 Physical Execution Continuity /
Segment Gradient·AdamW Continuity /

Source GEN5 Parent Immutability /
Physical State First /
Receipt Is Evidence, Not State /

No Receipt-to-State Synthesis /
No Genesis Fallback /
No Zero-Moment Fallback /
No Silent State Repair /
No Silent Migration /
No Hidden CPU Gradient Fallback /
No Legacy Full-Checkpoint Fallback /

Eight Physical Commits Or No N8 Admission /
GEN13·OPT13·CURSOR83 Continuous Candidate Authority /
No Resume-Cut Determinism Claim /
No Production Parent Promotion Yet
```

---

## 1. Source authority

The only admitted source is the promoted physical N2 state:

```text
GEN5
OPT5
cursor last=18
cursor next=19
cursor consumed=19
```

The run is located through the Physical N2 Promotion output:

```text
CURRENT_BASETRAIN_PARENT_POINTER.json
        ↓
physical N2 run root
        ↓
training_state/active_training_state.json
```

Promotion receipts locate and prove the state. They do not reconstruct it.

Required source validation:

- promotion PASS token is present
- promotion commit count is `1`
- physical state verified is `1`
- promoted generation is `5`
- promoted optimizer step is `5`
- promoted cursor next ordinal is `19`
- pointer state kind is `R6_PACKED_TRAINING_STATE`
- pointer run root equals the explicit resume run root
- active-state physical digest equals the digest bound by promotion
- weight / Adam-M / Adam-V physical digests equal the promotion-bound digests

---

## 2. Single-process N8 geometry

N8 is a single fresh process with no intentional mid-run restart.

```text
8 logical microbatches
→ 1 accumulated F32 gradient
→ 1 AdamW commit
```

repeated exactly eight times.

Total:

```text
logical microbatches     = 64
physical gradient passes = 8
optimizer commits        = 8
```

Exact batch geometry:

```text
commit 1 : 19..26
commit 2 : 27..34
commit 3 : 35..42
commit 4 : 43..50
commit 5 : 51..58
commit 6 : 59..66
commit 7 : 67..74
commit 8 : 75..82
```

Final state:

```text
GEN13
OPT13
cursor last=82
cursor next=83
cursor consumed=83
```

---

## 3. Generation / optimizer / cursor coupling

Every committed optimizer step advances all three authorities together.

| Commit | GEN | OPT | Last | Next |
|---|---:|---:|---:|---:|
| Parent | 5 | 5 | 18 | 19 |
| 1 | 6 | 6 | 26 | 27 |
| 2 | 7 | 7 | 34 | 35 |
| 3 | 8 | 8 | 42 | 43 |
| 4 | 9 | 9 | 50 | 51 |
| 5 | 10 | 10 | 58 | 59 |
| 6 | 11 | 11 | 66 | 67 |
| 7 | 12 | 12 | 74 | 75 |
| 8 | 13 | 13 | 82 | 83 |

Required invariant:

```text
generationDelta
== optimizerDelta
== committedOptimizerSteps
```

No generation, optimizer, or cursor synthesis is permitted.

---

## 4. Resume-state path

The existing R6 packed-state resume path is adopted for N8.

N8 must use:

```text
--resume-training-state <physical N2 run root>
```

and must not use:

```text
--r6-parent-r5-run-dir
--resume-checkpoint-bundle
--init-checkpoint-path
external atlas plans
```

The legacy GEN3 genesis-cache adoption path is not re-executed for N8.

The physical GEN5 `RUN_SLOT` packed state is consumed directly.

---

## 5. Preflight I/O rule

Dataset batch-count preflight must not trigger a second full packed-state scan.

For N8, required batch count is derived from the validated active state and cursor only.

The weight / Adam-M / Adam-V physical validation occurs at actual resume admission.

This prevents a redundant full source-pack read before the real run.

---

## 6. R14 persistent long-horizon authority

N8 upgrades R14 from console-only observation to a persistent per-step ledger.

Expected executions:

```text
8 optimizer steps × 8 lanes = 64 R14 lanes
```

Each lane persists:

```text
laneIndex
totalRows
hiddenWidth
activeLossRows
expectedOwnerPinCount
observedOwnerPinCount
preFinalHiddenOwnerPinned
normalizedHiddenOwnerPinned
finalNormInvRmsOwnerPinned
finalNormGammaOwnerPinned
rawOwnerIdentityValidated
unexpectedWritableAliasCount
payloadReadbackCount
aggregateFaultCount
rowdotCompletionCount
dxCompletionCount
dgammaCompletionCount
invRmsNonfiniteRows
invRmsNonpositiveRows
xNonfiniteRows
dyNonfiniteRows
gammaNonfiniteRows
rowdotAccNonfiniteRows
dxFaultElements
dxValueNonfiniteElements
dgammaInputFaultColumns
dgammaAccNonfiniteColumns
```

Required per-lane gate:

```text
owner pins = 4 / 4
raw identity = valid
unexpected writable aliases = 0
payload readback = 0
aggregate fault = sum(attributed fault fields) = 0
rowdot completion = 1
dx completion = 1
dgamma completion = 1
totalRows = activeLossRows + 1
```

Persistent layout:

```text
r14_long_horizon/
├─ optimizer_step_000006.json
├─ optimizer_step_000007.json
├─ optimizer_step_000008.json
├─ optimizer_step_000009.json
├─ optimizer_step_000010.json
├─ optimizer_step_000011.json
├─ optimizer_step_000012.json
└─ optimizer_step_000013.json
```

A step sidecar is written only after that optimizer step has committed its training state.

---

## 7. Per-step long-horizon ledger

The existing R6 step receipt is extended with observation-only fields:

```text
lossMean
accumulatedGlobalGradientL2
accumulatedGlobalGradientMaxAbs
accumulatedGlobalGradientNonzeroElementCount
parameterUpdateNonzeroElementCount
parameterUpdateL2
parameterUpdateMaxAbs
```

Final aggregate ledger:

```text
n8_long_horizon_step_ledger.json
```

Loss is observational only.

A lower loss on the next optimizer step is not a structural admission rule because the batch set changes between steps.

---

## 8. Accumulator and gradient continuity

Each physical pass remains:

```text
8 lanes
→ one F32 accumulator
→ 201 logical parameter gradients
→ one finalized gradient set
```

Hard failures include:

- accumulator nonfinite count > 0
- missing logical gradient
- duplicate logical gradient
- nonfinite gradient
- production gradient payload readback
- partial accumulation commit

Cross-step accumulated gradients must not survive into the next optimizer step.

---

## 9. Packed runtime continuity

N8 preserves the R6A packed runtime path.

Required invariants include:

```text
runtime arena create count = 0
runtime arena rewrite count = 0
post-write digest reread bytes = 0
per-parameter runtime payload file count = 0
partial pack adoption = 0
source pack mutation count = 0
```

The source GEN5 parent remains immutable because all child generations are written into the new N8 output root.

---

## 10. Micro-atlas continuity

Preserve:

```text
micro-atlas page = 16 MiB
ring slots       = 3
```

Required:

```text
oversized buffer create attempts = 0
full embedding GPU residency = 0
full LM-head GPU residency = 0
full vocab weight materialization = 0
full logits materialization = 0
microbatch-induced page refetch bytes = 0
```

Eight logical lanes must not become eight independent full weight traversals.

For N8:

```text
forward decoder weight traversals  = 8
backward decoder weight traversals = 8
```

not `64`.

---

## 11. Subgroup32 / AdamW authority

Each physical gradient pass retains:

```text
required subgroup size = 32
observed subgroup size = 32
subgroup exact32 = true
segment-native AdamW = true
```

No full-parameter gradient buffer or full-parameter optimizer materialization may silently return.

CF1 remains mandatory and must be regenerated after this source-tree change.

The N8 validator is included in the CF1 compile-chain validator set so the new source path is covered by both `sourceTreeDigest` and the static validation chain.

---

## 12. Source-parent immutability

Before N8 execution, bind:

```text
GEN5 active-state SHA256
weight pack SHA256
Adam-M pack SHA256
Adam-V pack SHA256
```

After all eight commits and terminal receipt validation, re-hash the same GEN5 parent files.

Required:

```text
sourceParentMutationCount = 0
```

The N8 child output must never overwrite the promoted N2 run root.

---

## 13. Eight-or-nothing admission

Partial physical commits remain real state but do not count as N8 success.

Example:

```text
GEN11 / OPT11 / partial cursor
```

may exist after a later failure.

That state must not be rewritten, synthesized, or promoted to GEN13.

N8 PASS requires:

```text
committedOptimizerSteps = 8
```

exactly.

---

## 14. Final receipt

Output:

```text
n8_long_horizon_continuity_receipt.json
```

Required terminal identity:

```text
sourceTrainingGeneration = 5
sourceOptimizerStep = 5
sourceCursorNextBatchOrdinal = 19

targetOptimizerSteps = 8
committedOptimizerSteps = 8
gradientAccumulation = 8
logicalMicrobatchCount = 64
physicalGradientPassCount = 8

trainingGenerationAfter = 13
optimizerStepAfter = 13
cursorLastBatchOrdinalAfter = 82
cursorNextBatchOrdinalAfter = 83
cursorConsumedBatchCountAfter = 83

r14ExpectedLaneCount = 64
r14ObservedLaneCount = 64
r14OwnerPinMismatchCount = 0
r14IdentityMismatchCount = 0
r14WritableAliasCount = 0
r14FaultCount = 0

sourceParentMutationCount = 0
hiddenFallbackCount = 0
productionCommitCount = 8
```

---

## 15. PASS / HOLD

PASS:

```text
PASS_ASH_BASETRAIN_N8_LONG_HORIZON_CONTINUITY_GEN5_TO_GEN13_OPT5_TO_OPT13_CURSOR19_TO_CURSOR83_R1
```

Normal next-stage HOLD:

```text
HOLD_ASH_BASETRAIN_N8_CONTINUOUS_GEN13_CANDIDATE_READY_RESUME_CUT_EXACT_DETERMINISM_NOT_YET_ADMITTED
```

The HOLD means the continuous N8 candidate exists, but interrupted-resume parity has not yet been proven.

---

## 16. Explicit non-goals

This patch does not prove:

- 4 + restart + 4 exact equivalence
- crash recovery
- checkpoint publication V2
- N=32 or N=128 stability
- model-quality convergence
- TensorCube production adoption

The next patch is:

```text
ASH-BASETRAIN-RESUME-CUT-EXACT-DETERMINISM-R1
```

and must compare the continuous GEN13 candidate against a fresh-process `4 + reload + 4` route from the same promoted GEN5 parent.
