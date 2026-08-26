# ASH-BP-DK-FUSION-STORAGE-QUIESCENCE-15C-R2

## External Resume Parent Lineage Recognition / Committed Active Slot Staging Residue Classification

### Status

- Patch ID: `ASH-BP-DK-FUSION-STORAGE-QUIESCENCE-15C-R2`
- Build revision: `bp-dk-fusion-storage-quiescence-15c-r2`
- PASS token: `PASS_ASH_BP_DK_FUSION_STORAGE_QUIESCENCE_15C_R2`
- Scope: BP-DK managed activation storage-quiescence classifier only
- No 08-BASE measurement topology change
- No checkpoint mutation
- No manual staging-marker deletion
- Fail closed on any identity or digest mismatch

## 1. Problem

15C-R1 classifies a canonical `transaction.staging.json` as unresolved whenever its `sourceSlot` is `slot_a` or `slot_b` but the matching local source committed-history file is absent from the current run root.

That is incorrect for the first generation of a run resumed from an external checkpoint. In that topology the source generation belongs to the external parent run, while the candidate generation, candidate history, active state, and packed manifest belong to the current run.

Observed production fixture:

```text
source       = generation 5 / optimizer step 5 / slot_a
candidate    = generation 6 / optimizer step 6 / slot_b
active       = generation 6 / optimizer step 6 / slot_b
local H5     = absent
local H6     = present
active SHA   = H6 SHA
manifest SHA = active.packedStateManifestDigest
active.parentTrainingStateDigest = manifest.sourceTrainingStateDigest
recoveryPreservedPaths = []
```

The storage state is committed, but 15C-R1 reports `UnresolvedPendingStorage` because local H5 is missing.

## 2. Authority / SSOT

### Active state authority

`training_state/active_training_state.json`

Owns `trainingGeneration`, `optimizerStep`, `packedStateSlot`, `packedStateManifestDigest`, `parentTrainingStateDigest`, and `trainingStateDigest`.

### Candidate committed-history authority

`training_state/committed_training_state_step_<candidateOptimizerStep>.json`

The candidate history must exist and match the active candidate exactly when the candidate slot is active.

### Packed-state authority

`training_state/<candidateSlot>/packed_state_manifest.json`

Owns physical candidate slot/generation/step identity and `sourceTrainingStateDigest`.

### Transaction progression evidence

- `transaction.staging.json`
- `transaction.validated.json`
- `transaction.ready_for_commit.json`

These files prove transaction progression. They do not replace active-state authority.

## 3. Candidate exact-admission contract

A staging marker is eligible for committed-active classification only when all of the following are exact:

```text
candidateGeneration == active.trainingGeneration
candidateOptimizerStep == active.optimizerStep
candidateSlot == active.packedStateSlot
```

The candidate committed history must exist and match:

```text
history.trainingGeneration == candidateGeneration
history.optimizerStep == candidateOptimizerStep
history.packedStateSlot == candidateSlot
history.packedStateManifestDigest == packed manifest SHA-256
history.candidateManifestDigest == packed manifest SHA-256
history.trainingStateDigest validates
```

For the active candidate, serialized file SHA-256 parity is required:

```text
SHA256(active_training_state.json)
==
SHA256(committed_training_state_step_<candidateOptimizerStep>.json)
```

## 4. Packed manifest contract

The candidate manifest must exist and parse:

```text
training_state/<candidateSlot>/packed_state_manifest.json
```

Required identity:

```text
manifest.slotId == candidateSlot
manifest.trainingGeneration == candidateGeneration
manifest.optimizerStep == candidateOptimizerStep
SHA256(manifest) == validated.packedStateManifestDigest
SHA256(manifest) == active.packedStateManifestDigest   # active candidate
```

When both values are present:

```text
validated.candidateParameterSetDigest
==
manifest.parameterSetDigest
```

A mismatch remains unresolved pending storage.

## 5. Transaction phase contract

### Staging

`transaction.staging.json` must parse as `AshTrainingTransactionStagingMarker` and pass its existing validation contract, including:

```text
state == STAGING
candidateGeneration == sourceGeneration + 1
candidateOptimizerStep == sourceOptimizerStep + 1
microbatchCount == 8
sourceSlot != candidateSlot
```

### Validated

`transaction.validated.json` must exist with:

```text
state == VALIDATED
schedulerStep == candidateOptimizerStep
packedStateManifestDigest == SHA256(candidate packed manifest)
```

### Ready for commit

`transaction.ready_for_commit.json` must exist with:

```text
trainingGeneration == candidateGeneration
optimizerStep == candidateOptimizerStep
packedStateSlot == candidateSlot
state is non-empty
```

## 6. Local source history first

When the local source history exists, 15C-R2 preserves the R1 rule:

```text
committed_training_state_step_<sourceOptimizerStep>.json
```

must match source generation, optimizer step, source slot, and `trainingStateDigest`.

If local source history exists but is invalid, classification fails closed. There is no fallback to external-parent admission.

## 7. External resume parent recognition

External-parent admission is attempted only when:

1. `sourceSlot` is `slot_a` or `slot_b`.
2. The local source committed-history file is absent.
3. The candidate is the exact current active generation/step/slot.
4. Candidate history, manifest, validated evidence, ready evidence, and active/history parity pass.

The external parent is admitted only when both digests are present and non-empty:

```text
active.parentTrainingStateDigest
manifest.sourceTrainingStateDigest
```

and:

```text
active.parentTrainingStateDigest
==
manifest.sourceTrainingStateDigest
```

No external parent digest is guessed, copied from another run, or synthesized.

## 8. Classification

15C-R2 defines:

```text
CommittedActiveSlot
CommittedHistoricalSlot
CommittedActiveSlotExternalResumeParent
UnresolvedPendingStorage
```

The new class is selected only for:

```text
candidateIsExactActive
AND candidateHistoryExact
AND manifestExact
AND validatedExact
AND readyExact
AND localSourceHistoryAbsent
AND externalParentDigestExact
```

Historical candidate staging residue does not receive the external-parent fallback. Missing local source history for a historical candidate remains unresolved.

## 9. Quiescence counters

A staging marker remains physically observable, so `observedStagingCount` is not suppressed.

For an admitted external-resume committed residue:

```text
observedStagingCount += 1
committedTransactionResidueCount += 1
externalResumeParentResidueCount += 1
unresolvedPendingStateCount += 0
```

Expected diagnostic for the current fixture:

```text
[ASH-BP-DK-FUSION-STORAGE-QUIESCENCE-15C-R2]
observedPartialCount=0
observedTmpCount=0
observedStagingCount=1
committedTransactionResidueCount=1
externalResumeParentResidueCount=1
unresolvedPendingStateCount=0
```

The legacy restart barrier may proceed when unresolved pending state is zero. A non-zero observed staging count alone is not a failure when every staging marker is proven committed residue.

## 10. Fail-closed rules

The following remain unresolved pending storage:

- candidate committed history missing
- candidate history identity mismatch
- active/history file SHA mismatch
- candidate generation mismatch
- candidate optimizer-step mismatch
- candidate slot mismatch
- packed manifest missing or unparsable
- manifest slot/generation/step mismatch
- manifest digest mismatch
- validated transaction missing or mismatched
- ready-for-commit transaction missing or mismatched
- local source history exists but is invalid
- external parent digest missing
- manifest source digest missing
- external parent digest mismatch
- malformed staging marker
- noncanonical staging location

## 11. Explicit prohibitions

```text
No Manual transaction.staging.json Delete
No Staging Count Suppression
No Timestamp-Based Stale Heuristic
No Missing Candidate History Relaxation
No Missing Manifest Relaxation
No Active-State Rewrite
No Candidate-History Rewrite
No Parent Digest Fabrication
No Cross-Run H5 Copy
No Silent External-Parent Guess
No 08-BASE Measurement Topology Change
```

## 12. Regression fixtures

### Positive

`external_resume_parent_committed_active_staging_residue_is_quiescent`

```text
local H5 = absent
H6 = present and valid
active == H6
candidate = gen6 / step6 / slot_b
manifest = gen6 / step6 / slot_b
validated = exact
ready = exact
active.parentTrainingStateDigest == manifest.sourceTrainingStateDigest
```

Expected:

```text
observedStagingCount = 1
committedTransactionResidueCount = 1
externalResumeParentResidueCount = 1
unresolvedPendingStateCount = 0
```

### Negative

`external_resume_parent_digest_mismatch_remains_pending`

The fixture is identical except:

```text
active.parentTrainingStateDigest
!=
manifest.sourceTrainingStateDigest
```

Expected:

```text
committedTransactionResidueCount = 0
externalResumeParentResidueCount = 0
unresolvedPendingStateCount = 1
```

## 13. Current production fixture closure

The observed `n8_perf_20260820_002426` state satisfies the external-resume pattern:

```text
active generation = 6
active optimizer step = 6
active slot = slot_b
H5 source history = absent
H6 candidate history = present
active SHA == H6 SHA
manifest SHA == active.packedStateManifestDigest
recoveryPreservedPaths = []
```

15C-R2 classifies that topology from exact lineage evidence rather than from the physical presence of a staging marker alone.

## 14. Acceptance

Code acceptance requires:

```text
cargo check --locked -p base_train --bin base_train
cargo test --locked -p base_train --lib storage_quiescence_15c_r2 -- --nocapture
cargo build --release --locked -p base_train --bin ash_bp_dk_fusion_policy_explicit_production_activation_15
```

Physical acceptance then reruns `seal-legacy-restart-barrier` against the unchanged `n8_perf_20260820_002426` source run and expects:

```text
observedStagingCount=1
committedTransactionResidueCount=1
externalResumeParentResidueCount=1
unresolvedPendingStateCount=0
```

No source checkpoint file or staging marker is deleted as part of acceptance.
