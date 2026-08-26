# ASH-BP-DK-FUSION-LEGACY-MIGRATION-N8-PROMOTED-DESCENDANT-SOURCE-AUTHORITY-CLOSURE-11A-R4

## Status

Implementation bake for explicit legacy-migration descendant source admission on top of 11A-B0 and 11A-R3.

```text
Legacy Sealed Source gen6/step6 /
Original Physical N2 Promoted Ancestor gen5/step5 /
Exact Descendant Lineage Proof /
Committed History Chain /
No Arithmetic Generation Fabrication /
N2 Ancestor Authority Preserved /
No Direct Gen6-As-N2 Fiction /
No N8 Exact-Parent Gate Blind Relaxation /
Explicit Legacy Migration Descendant Admission /
Source Digest Bound /
Barrier Digest Bound /
Ancestor N2
-> Exact Committed Descendant
-> Sealed Legacy Source
-> Exact N8 Capture Window
```

## 1. Problem closed

Normal N8 admission is intentionally strict. The physical N2 promotion receipt identifies one exact promoted parent at training generation 5, optimizer step 5, cursor 19, and normal N8 requires the resume root to be that exact promoted parent.

The sealed legacy migration source is instead the already committed run `n8_perf_20260820_002426` at generation 6 / optimizer step 6. Treating this source directly as the original promoted N2 parent would be false authority.

R4 does not relax the normal N8 exact-parent rule. R4 introduces a typed alternate source role that is admitted only after proving that the sealed generation-6 source contains the exact committed generation-5 ancestor bound by the physical N2 promotion receipt and an exact generation-5 -> generation-6 committed-state edge.

## 2. Authority roles

```text
Physical N2 Promotion Authority
  owns original promoted ancestor identity

Committed Training-State Chain
  owns exact ancestor -> descendant transition

Legacy Restart Barrier
  owns sealed legacy source admission state

11A-B0
  owns migration-evidence-only seed authority

11A-R3
  owns exact physical capture horizon = 8 optimizer steps

11A-R4
  owns exact legacy descendant source admission only
```

R4 does not become a production-policy authority, activation authority, or a second N2 promotion authority.

## 3. Source roles

BaseTrain now distinguishes:

```text
PROMOTED_PARENT
LEGACY_MIGRATION_DESCENDANT
```

Without an explicit R4 authority path, normal N8 still executes the existing exact promoted-parent validation path, including the canonical promoted parent run-root equality check.

With an explicit R4 authority path, BaseTrain validates the exact typed descendant authority and uses its descendant source identity. There is no `generation >= 5` rule and no arbitrary later-checkpoint admission.

## 4. R4 authority receipt

Schema:

```text
ash.bp_dk.fusion_legacy_migration.n8_promoted_descendant_source_authority.r4
```

Patch identity:

```text
ASH-BP-DK-FUSION-LEGACY-MIGRATION-N8-PROMOTED-DESCENDANT-SOURCE-AUTHORITY-CLOSURE-11A-R4
```

Source role:

```text
LEGACY_MIGRATION_DESCENDANT
```

Output name recommended for operator materialization:

```text
n8_promoted_descendant_source_authority_receipt.json
```

## 5. Exact ancestor evidence

R4 consumes the existing physical N2 promotion directory and requires:

```text
physical_n2_promotion_receipt.json
CURRENT_BASETRAIN_PARENT_POINTER.json
```

The promotion receipt must remain an exact committed physical N2 receipt:

```text
promotionCommitCount = 1
physicalStateVerified = 1
promotedTrainingGeneration = 5
promotedOptimizerStep = 5
promotedCursorNextBatchOrdinal = 19
repoPhysicalPayloadCount = 0
promotionPayloadCopyCount = 0
promotionPayloadMutationCount = 0
receiptToStateSynthesisCount = 0
stateRewriteCount = 0
```

The pointer must preserve the original promoted parent run-root string, physical storage root, state kind, and native-CF1 receipt hash from the historical promotion authority.

R4 does not rewrite the old pointer or promotion receipt.

## 6. Exact descendant evidence

The sealed source must contain:

```text
training_state/committed_training_state_step_000005.json
training_state/committed_training_state_step_000006.json
training_state/active_training_state.json
```

Required ancestor parity:

```text
SHA256(committed step 5)
== physicalN2.activeStateSHA256

step5.trainingGeneration = 5
step5.optimizerStep = 5
step5.datasetCursor.nextBatchOrdinal = 19
```

Required descendant parity:

```text
step6.trainingGeneration = 6
step6.optimizerStep = 6

SHA256(active state)
== SHA256(committed step 6)

step6.parentTrainingStateDigest
== SHA256(committed step 5)
```

This committed history edge is the lineage authority. `5 + 1 = 6` arithmetic is not evidence.

## 7. Packed-state parity

The active descendant state must reference `slot_a` or `slot_b`. R4 verifies the active state's packed manifest digest against the actual packed manifest bytes and verifies exact weight, Adam-M, and Adam-V payload hashes against the manifest.

Required failure-closed conditions include missing payloads, manifest digest drift, active/committed drift, and parent training-state digest drift.

## 8. Source and barrier binding

The R4 authority binds the exact sealed source checkpoint digest and the exact legacy restart barrier digest.

Current migration lineage is expected to bind:

```text
sourceCheckpointDigest = d4dcc266fe4e9c3691176e0041f736dc1809b90c04dabb358403a9a2568041b2
legacyRestartBarrierDigest = 80f450c27ae356c9ae03e5d45e6f4e14a1d59556f74c1b705abd70b85aa6ddc6
```

The actual physical sealer re-observes these values. The implementation does not accept a caller-supplied digest as a substitute for fresh observation.

## 9. Scope invariants

Every valid R4 authority requires:

```text
exactDescendantLineageProof = true
committedHistoryChainVerified = true
arithmeticLineageInferenceCount = 0
sourceRewriteCount = 0
n2ReceiptRewriteCount = 0
n8GateRelaxationCount = 0
syntheticAncestorCount = 0
unresolvedHistoryEdgeCount = 0
n8AncestorAuthorityPreserved = true
n8ExactParentGateRelaxed = false
migrationCaptureAuthority = true
productionAuthority = false
activationAuthority = false
```

## 10. BaseTrain CLI admission

R4 adds the child-runtime flag:

```text
--legacy-migration-descendant-source-authority <R4_RECEIPT>
```

The flag is legal only with N8 admission. It is forbidden with N8 resume-cut roles.

Without this flag, the original normal-N8 exact promoted-parent validation remains unchanged.

## 11. 11A ownership

11A capture adds the operator-facing flag:

```text
--n8-promoted-descendant-source-authority <R4_RECEIPT>
```

11A revalidates:

```text
R4 promotion directory == common-args N2 promotion directory
R4 descendant source == source checkpoint
R4 source digest == fresh source digest
R4 barrier digest == supplied barrier
R4 operator identity == capture operator identity
```

11A owns the child `--legacy-migration-descendant-source-authority` argument. Common args are forbidden from owning it.

## 12. R3 exact-eight horizon preservation

R4 does not alter R3 horizon semantics:

```text
requestedGenerationCount = 8
physicalOptimizerStepHorizon = 8
effectiveProductionLoopOptimizerSteps = 8
syntheticResumeCutCount = 0
```

The branch runner remains the only owner of `--production-loop-optimizer-steps`.

## 13. Runtime N8 source binding

`N8ParentBinding` now carries both ancestor and source identities.

Normal role:

```text
role = PROMOTED_PARENT
ancestor = gen5 / step5 / cursor19
source   = gen5 / step5 / cursor19
```

R4 role:

```text
role = LEGACY_MIGRATION_DESCENDANT
ancestor = gen5 / step5 / cursor19
source   = exact committed gen6 / step6 / observed cursor
```

Runtime packed source and RAM-resident optimizer-state admission use the exact bound source identity rather than a second hard-coded gen5 assumption.

## 14. Exact eight-step finalization

Normal N8 keeps the original exact result:

```text
source 5/5/19
-> final 13/13/83
```

R4 descendant mode validates the final state by exact observed deltas:

```text
training generation delta = 8
optimizer step delta = 8
cursor-next delta = 64
committed optimizer steps = 8
logical microbatches = 64
```

R4 does not pre-authorize a fabricated final checkpoint identity. The final generation, optimizer step, and cursor are read from runtime receipts after execution.

Descendant N8 pass token:

```text
PASS_ASH_BASETRAIN_N8_LEGACY_MIGRATION_DESCENDANT_EXACT_8_WINDOW_R4
```

## 15. Scheduler horizon closure discovered during bake

The normal N8 scheduler profile closes at optimizer step 13. A sealed legacy descendant starting at optimizer step 6 and executing one exact eight-step N8 window reaches target optimizer step 14.

Running the original total-step-13 profile through target step 14 would fail scheduler range validation. R4 therefore materializes a deterministic migration-only scheduler profile before child launch.

Source scheduler contract required for derivation:

```text
profileId = ash_basetrain_n8_long_horizon_continuity_r1
schedulerKind = LINEAR_WARMUP_CONSTANT
warmupOptimizerSteps = 4
totalOptimizerSteps = 13
baseLearningRate == minimumLearningRate == warmupStartLearningRate
sourceOptimizerStep = 6
optimizerStepBudget = 8
```

Derived profile:

```text
profileId = ash_basetrain_n8_legacy_migration_descendant_r4
totalOptimizerSteps = 14
profileRevision = source revision + 1
profileDigest = recomputed canonical scheduler digest
```

The original operator common-args file is not mutated. 11A creates the derived profile under its isolated output admission directory and replaces only the effective child scheduler-profile argument.

Required invariant:

```text
schedulerMathChangeCount = 0
```

The extension is horizon authority only. Learning-rate math is unchanged because the admitted source profile is constant across the boundary.

Descendant scheduler pass token:

```text
PASS_ASH_BASETRAIN_N8_LEGACY_MIGRATION_DESCENDANT_SCHEDULER_EXTENSION_STEP6_TO_STEP14_R4
```

## 16. Storage publication closure discovered during bake

The existing N8 storage publisher had normal-N8 final identity literals for generation 13 / step 13 / cursor 83 and copied a hard-coded `committed_training_state_step_000013.json`.

R4 changes storage publication to consume the already validated N8 final receipt identity:

```text
trainingGeneration = n8.trainingGenerationAfter
optimizerStep = n8.optimizerStepAfter
cursorNext = n8.cursorNextBatchOrdinalAfter
committed state filename = optimizerStepAfter
```

The normal role still publishes 13/13/83 because the normal N8 finalizer retains its exact original hard gate. R4 does not weaken normal-N8 storage semantics.

## 17. Native CF1 release authority lifecycle

R4 changes BaseTrain compile inputs and therefore invalidates any pre-R4 native CF1 release authority for the old `base_train.exe`.

Physical execution order must be:

```text
apply R4 source
-> cargo check/tests
-> build R4 helper/capture binaries
-> run native CF1 release compile authority materializer
-> allow that materializer to perform the final canonical Release build of base_train.exe
-> use the newly emitted native CF1 authority path
-> do not rebuild base_train.exe afterward
-> seal R4 descendant authority
-> run 11A-R4 capture
```

Using a pre-R4 native-CF1 receipt with the post-R4 binary must fail exact binary identity validation.

## 18. Common-args ownership

11A continues to own and forbid common-args ownership of:

```text
--output-dir
--resume-training-state
--r6-parent-r5-run-dir
--production-loop-optimizer-steps
--basetrain-storage-root
--atlas-plan-output-dir
--legacy-migration-descendant-source-authority
--admit-tensorcube-local-muon-new-lineage
```

Common args must bind the source-independent production authorities required by BaseTrain, including the current native CF1 release authority, physical N2 promotion directory, original N8 scheduler profile, RAM36 parent exact-inventory receipt, and Local-Muon registry/profile.

11A conditionally owns first-hybrid Muon new-lineage admission only when both source Muon momentum and source Muon manifest are absent.

## 19. Capture receipt R4

Capture schema advances to:

```text
ash.bp_dk.fusion_legacy_migration.evidence_capture.r4
```

The capture receipt adds:

```text
n8DescendantSourceAuthorityReceiptDigest
n8DescendantSourceRole
exactDescendantLineageProof
committedHistoryChainVerified
n8ExactParentGateRelaxed
descendantSchedulerProfilePath
descendantSchedulerProfileDigest
schedulerMathChangeCount
```

R3 exact-eight horizon fields and R2 Muon-lineage fields remain present.

## 20. Source immutability

R4 sealer and 11A capture do not modify the sealed source or historical N2 promotion authority.

11A independently hashes the R4 authority before and after capture and fails if it changes.

Existing source checkpoint, barrier, seed, model, production policy pointer, and managed authority mutation gates remain preserved.

## 21. Failure examples

Representative failures:

```text
ASH_BP_DK_LEGACY_MIGRATION_N8_ANCESTOR_RECEIPT_MISSING
ASH_BP_DK_LEGACY_MIGRATION_N8_ANCESTOR_RECEIPT_NOT_COMMITTED
ASH_BP_DK_LEGACY_MIGRATION_N8_ANCESTOR_IDENTITY_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_N8_ANCESTOR_HISTORY_DIGEST_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_COMMITTED_STATE_MISSING
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_ACTIVE_COMMITTED_PARITY_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_HISTORY_EDGE_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_MANIFEST_DIGEST_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_SOURCE_DIGEST_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_BARRIER_MISMATCH
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_AUTHORITY_REQUIRED
ASH_BP_DK_LEGACY_MIGRATION_DESCENDANT_RESUME_CUT_FORBIDDEN
R4DescendantSchedulerSourceOrBudgetMismatch
R4DescendantSchedulerTargetMustBe14
R4DescendantSchedulerExistingConflict
```

## 22. Unit regression surface

R4 adds focused Rust unit tests:

```text
r4_typed_descendant_receipt_seals_without_global_n8_gate_relaxation
r4_typed_descendant_receipt_rejects_gate_relaxation_or_arithmetic_fiction
```

R3 exact-eight regression tests remain required.

The bake environment does not contain a Rust toolchain, so Rust compilation and unit execution are not claimed by the bake artifact. They must run on the Windows authority host.

## 23. Static validation

Bake-side static validation:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_N8_PROMOTED_DESCENDANT_SOURCE_AUTHORITY_CLOSURE_11A_R4_STATIC 54/54
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EXACT_N8_CAPTURE_HORIZON_CLOSURE_11A_R3_STATIC 22/22
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_SEED_AUTHORITY_BOOTSTRAP_11A_B0_STATIC 17/17
```

Static validation proves source surfaces and prohibitions only. It does not prove Rust type/borrow correctness or physical N8 execution.

## 24. Implementation surface

New:

```text
crates/base_train/src/bp_delta_k_fusion_legacy_migration_n8_promoted_descendant_source_authority.rs
crates/base_train/src/bin/ash_bp_dk_fusion_legacy_migration_n8_promoted_descendant_source_authority_11a_r4.rs
tools/validate_ash_bp_dk_fusion_legacy_migration_n8_promoted_descendant_source_authority_closure_11a_r4_static.py
```

Modified:

```text
crates/base_train/Cargo.toml
crates/base_train/src/lib.rs
crates/base_train/src/bin/ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a.rs
crates/base_train/src/bin/base_train.rs
crates/base_train/src/bp_delta_k_fusion_legacy_migration_seed_policy_evidence_capture.rs
crates/base_train/src/config.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/n8_long_horizon_continuity.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/storage_root_authority.rs
tools/validate_ash_bp_dk_fusion_legacy_migration_exact_n8_capture_horizon_closure_11a_r3_static.py
```

R4 does not modify optimizer kernels, Local-Muon math, AdamW math, model math, dataset math, or the B0 seed bootstrap implementation.

## 25. Physical sealer PASS

Successful R4 authority sealing emits:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_N8_PROMOTED_DESCENDANT_SOURCE_AUTHORITY_CLOSURE_11A_R4
source_role=LEGACY_MIGRATION_DESCENDANT
ancestor_training_generation=5
ancestor_optimizer_step=5
descendant_training_generation=6
descendant_optimizer_step=6
exact_descendant_lineage_proof=1
committed_history_chain_verified=1
n8_exact_parent_gate_relaxed=0
production_authority=0
activation_authority=0
migration_capture_authority=1
```

BaseTrain descendant admission emits:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_N8_DESCENDANT_SOURCE_ADMISSION_11A_R4
```

## 26. Final SSOT

```text
Original Physical N2 Promotion
  gen5 / step5 / cursor19

-> exact promoted active-state digest

Sealed legacy source committed step5

-> exact parentTrainingStateDigest edge

Sealed legacy source committed + active step6

-> R4 typed descendant source authority

11A-B0 evidence-only seed

-> R3 exact eight-step capture horizon

R4 derived scheduler horizon step14

-> isolated BaseTrain N8 descendant run

-> runtime-observed exact +8/+8/+64 final identity

-> dynamic checkpoint publication

-> replay / trajectory evidence
```

No original N2 identity is rewritten. No global N8 gate is weakened. The alternate source role is admitted only for one exact sealed descendant whose physical lineage is proven from retained authority artifacts.