# ASH-BP-DK-FUSION-LEGACY-MIGRATION-SEED-POLICY-AND-EVIDENCE-CAPTURE-11A-R1

## Patch identity

```text
ASH-BP-DK-FUSION-LEGACY-MIGRATION-
SEED-POLICY-AND-EVIDENCE-CAPTURE-11A-R1
```

This patch opens a new forward BP-ΔK evidence lineage from a pre-BP-ΔK legacy checkpoint. It does not reconstruct or fabricate historical 05-12 evidence.

Functional placement:

```text
11 long-horizon trajectory
-> 11A legacy migration capture bridge
-> 12 calibration recommendation
-> 13 operator review
-> 14 bounded canary qualification
-> 15A first managed authority bootstrap
```

Physical safety parents remain the already validated 15A/15B/15C legacy migration and Windows authority closures.

## Proven source condition

The migration source used to motivate 11A is a generation-5 legacy checkpoint whose active slot has no BP-ΔK observer state, bridge state, planner state, 07 post-update ledger, 09 counterfactual ledger, 10 objective ledger, 11 trajectory head, 12 replay head, or managed checkpoint-policy binding.

Therefore 11A treats the source as PRE-BP-DK LEGACY and creates new evidence forward from the immutable source checkpoint.

## Authority boundary

11A requires an explicit operator-supplied 05-compatible seed policy.

The seed policy is parsed as `AshBpDkFusionFissionPolicy`, validated through the existing policy validator, and sealed by the existing canonical policy digest. 11A contains no hard-coded policy thresholds and does not promote test/08A fixtures into migration authority.

The seed authority scope is:

```text
LEGACY_MIGRATION_EVIDENCE_ONLY
productionAuthority = false
```

The seed is an evidence baseline, not an active production policy.

## Legacy restart barrier admission

11A requires the physical 15C legacy restart barrier. The typed barrier must validate and must prove:

```text
legacyUnbound = true
pendingStateCount = 0
trainerQuiescent = true
durableCheckpointComplete = true
checkpointPolicyBindingPresent = false
replayHeadPresent = false
```

The barrier source-checkpoint digest must equal a freshly computed `checkpoint_authority_digest()` for the migration source. Operator identity and authority domain must also match.

## Read-only legacy source

11A never writes, repairs, renames, deletes, or normalizes the source checkpoint.

Before and after the capture it recomputes the source checkpoint authority witness. A digest change is a hard failure:

```text
ASH_BP_DK_LEGACY_MIGRATION_SOURCE_CHECKPOINT_MUTATED
```

The active legacy slot is additionally required to remain free of canonical BP-ΔK authority sidecars before capture.

## Managed production authority isolation

11A receives the managed policy root only as a read-only witness.

The active production pointer must be absent before capture. The managed authority tree is digested before and after capture. Any policy-root or active-pointer mutation is a hard failure.

The output root must not be inside either the legacy source checkpoint or the managed policy root.

11A writes only to its isolated output root.

## Output layout

```text
<output-root>/
  admission/
    seed_policy.json
    seed_authority_receipt.json

  evidence/
    counterfactual_physical/        # promotion-ready profile only

  capture/
    runtime/
    storage/
    logs/
    atlas-plan/                     # only when the common args request it

  capture_receipt.json
```

The operator seed file itself remains immutable. A canonical JSON snapshot is written to `admission/seed_policy.json` and becomes the exact policy path supplied to the capture branch.

## Existing BaseTrain branch runner reuse

11A does not implement a second process runner. It reuses the existing 14 canary `execute_training_branch_with_env()` path.

That existing runner owns:

```text
--output-dir
--resume-training-state
--production-loop-optimizer-steps
--basetrain-storage-root
--atlas-plan-output-dir
```

It also applies the canonical BP-ΔK evidence environment:

```text
ASH_BP_DK_FUSION_PLANNER_MODE=ACTIVE
ASH_BP_DK_FUSION_POLICY_PATH=<immutable seed snapshot>
ASH_BP_DK_FUSION_OBJECTIVE_LONG_HORIZON_TRAJECTORY_MODE=DECISION_AND_UPDATE
ASH_BP_DK_FUSION_POLICY_CALIBRATION_RECOMMENDATION_MODE=CAPTURE
```

Common arguments may not contain orchestrator-owned output/resume/storage flags. They must retain the existing production multistep, N8 continuity, and TensorCube local-Muon production-callsite admissions.

The broad flag:

```text
--admit-tensorcube-local-muon-new-lineage
```

is explicitly rejected because it also owns Muon momentum lineage and exceeds 11A migration authority.

## Capture profiles

11A supports two explicit profiles.

### REPLAY_ONLY

Runs the isolated branch with planner ACTIVE, trajectory DECISION_AND_UPDATE, and calibration CAPTURE. No 08A receipt is required.

This profile is valid for creating 11/12 lineage but is not eligible for `promotionReady=true` in 11A.

### PROMOTION_READY_OBSERVED

Adds the existing observed evidence path:

```text
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=OBSERVE
ASH_BP_DK_ACTIVE_FUSION_08A_QUALIFICATION_RECEIPT_PATH=<validated 08A receipt>
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_PHYSICAL_RECEIPT_ROOT=<output-root>/evidence/counterfactual_physical
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_EFFECT_LEDGER_MODE=RECORD_OBSERVED
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_MODE=OBSERVE
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_BATCH_SOURCE=TRAINING_BATCH_REPLAY
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_STOCHASTIC_POLICY=DETERMINISTIC_NO_STOCHASTICITY
```

The 08A receipt is validated with the existing physical-execution validator before the child process starts.

The requested generation count must be at least the active 12 recommendation guard's `minTrajectoryGenerations` value. When no custom guard is supplied, the existing default recommendation policy is used.

## Evidence heads

A completed capture must publish both canonical heads in the final committed capture slot:

```text
bp_dk_fusion_objective_long_horizon_trajectory_head.json
bp_dk_fusion_policy_calibration_replay_evidence_head.json
```

Missing trajectory or replay heads are hard failures.

All replay generations in the captured head must use the exact seed-policy digest for `seedPolicyParity=true`.

## Promotion sufficiency

11A does not implement a second evidence-sufficiency formula. It directly calls the existing 12 `build_policy_calibration_recommendation()` function with the captured replay head, trajectory head, seed policy, and selected recommendation guard.

The resulting `evidenceSufficiency` provides:

```text
replayGenerationCount
trajectoryPairStateCount
counterfactualObservedCount
objectiveObservedCount
objectiveQualifiedCount
segmentPure
currentReplayParityVerified
confidence
```

`promotionReady=true` is possible only for the PROMOTION_READY_OBSERVED profile and requires:

```text
confidence = SUPPORTED or STRONGLY_SUPPORTED
segmentPure = true
currentReplayParityVerified = true
seedPolicyParity = true
trajectoryPairStateCount > 0
```

A successful physical capture that does not meet this bar is a valid:

```text
CAPTURE_COMPLETE_EVIDENCE_INSUFFICIENT
```

state, not corruption.

## No automatic downstream decision

11A does not write a 12 recommendation artifact, does not perform 13 operator review, does not run 14 qualification, and does not call the 15A managed-authority bootstrap.

Its responsibility ends at a valid evidence checkpoint and capture receipt.

## CLI

New executable:

```text
ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a
```

Required inputs:

```text
--source-checkpoint
--legacy-restart-barrier
--seed-policy
--base-train-binary
--model-spec-path
--common-args-json
--generation-count
--capture-profile
--operator-id
--authority-domain
--managed-policy-root
--output-root
```

Optional inputs:

```text
--active-fusion-08a-qualification-receipt
--recommendation-policy
```

The 08A receipt becomes mandatory when `capture-profile=promotion-ready-observed`.

## Receipts

Seed authority receipt schema:

```text
ash.bp_dk.fusion_legacy_migration.seed_policy_authority.r1
```

Capture receipt schema:

```text
ash.bp_dk.fusion_legacy_migration.evidence_capture.r1
```

The capture receipt records process completion, evidence checkpoint, trajectory and replay digests, 12-compatible evidence sufficiency, seed-policy parity, promotion readiness, and source/production/seed mutation counters.

## Mutation gates

A valid capture receipt requires all of these to remain zero:

```text
sourceCheckpointMutationCount
productionPolicyMutationCount
productionActivePointerMutationCount
managedAuthorityMutationCount
seedSourceMutationCount
```

Capture-branch state under the isolated output root is expected to mutate and is not production authority.

## CF1 order

11A is inserted into the BP-ΔK validator dependency chain as:

```text
11
-> 11A
-> 12
-> 13
-> 14
-> 15
-> 15A
-> 15B
-> 15C
-> 16 ... 21
```

## Baked implementation surface

The lightweight overlay contains six files:

```text
crates/base_train/src/bp_delta_k_fusion_legacy_migration_seed_policy_evidence_capture.rs
crates/base_train/src/bin/ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a.rs
crates/base_train/src/lib.rs
crates/base_train/Cargo.toml
tools/validate_ash_bp_dk_fusion_legacy_migration_seed_policy_and_evidence_capture_11a_r1_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

No `*.sha256`, generated artifact bundle, manifest bundle, or Python cache is included.

11A does not modify the 15C activation source or the N8 scheduler, so there is no downstream activation/scheduler parent-SHA fanout in this patch.

## Static validation

Observed on the cumulative 15C + latest N8 tree:

```text
11 trajectory:                                      145/145 PASS
11A migration capture:                             124/124 PASS
12 recommendation:                                 227/227 PASS
13 operator review:                                247/247 PASS
14 candidate canary:                               347/347 PASS
15 explicit production activation:                 281/281 PASS
15A legacy restart barrier closure:                153/153 PASS
15B Windows lock durability recovery:               93/93 PASS
15C transaction marker classification:             105/105 PASS
16 production soak/rollback:                       177/177 PASS
17 production long horizon:                        PASS
18 recalibration bridge:                           PASS
19 evidence calibration adoption:                  230/230 PASS
20 production-aware recommendation:                237/237 PASS
21 operator review/adoption:                       265/265 PASS
N8 HiMuon production hotpath:                       86/86 PASS
N8 phase wall-time attribution:                     77/77 PASS
N8 deferred durable writeback:                     118/118 PASS
```

The bake environment does not contain a Rust toolchain, so Windows Release CF1 remains the compile/type/borrow authority before physical capture.

## Promotion states

Valid evidence but insufficient for 12→13 promotion:

```text
HOLD_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EVIDENCE_INSUFFICIENT_FOR_12_TO_13_PROMOTION_11A_R1
```

Promotion-sufficient physical capture:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_PROMOTION_EVIDENCE_SUFFICIENCY_11A_R1
PROMOTE_ASH_BP_DK_FUSION_LEGACY_MIGRATION_SEED_POLICY_AND_EVIDENCE_CAPTURE_11A_R1
```

## Final SSOT

```text
A pre-BP-DK legacy checkpoint has no historical BP-DK evidence authority to recover.

11A starts a new, explicitly identified migration evidence lineage forward from the immutable legacy checkpoint.

The operator supplies the 05-compatible seed policy. 11A validates and seals it as evidence-only authority and never grants it production authority.

The legacy source checkpoint and managed production authority remain read-only.

11A reuses the existing BaseTrain/canary branch execution path and the existing 12 recommendation evidence-sufficiency calculation. It does not create parallel planner, trajectory, replay, or promotion mathematics.

REPLAY_ONLY captures lineage. PROMOTION_READY_OBSERVED additionally captures the existing 08/09/10 observed evidence path.

Capture success and promotion sufficiency are separate states.

12 owns recommendation, 13 owns operator review, 14 owns bounded qualification, and 15A owns first managed production authority bootstrap.
```
