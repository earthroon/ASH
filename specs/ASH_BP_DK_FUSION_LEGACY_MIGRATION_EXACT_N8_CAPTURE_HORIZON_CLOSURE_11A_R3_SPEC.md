# ASH-BP-DK-FUSION-LEGACY-MIGRATION-EXACT-N8-CAPTURE-HORIZON-CLOSURE-11A-R3

## Purpose

Close the horizon contradiction between the 11A legacy-migration capture schedule and the existing BaseTrain N8 physical admission contract.

```text
Legacy Resume Source /
Exact N8 Physical Window /

REPLAY_ONLY
requestedGenerationCount = 8 /

No Two-Step N8 Fiction /
No BaseTrain N8 Gate Relaxation /
No Synthetic Resume-Cut Role /

11A Schedule Horizon
==
BaseTrain Production Optimizer Step Horizon
==
8
```

R3 changes 11A capture-horizon ownership only. It does not modify BaseTrain N8 semantics, the canary branch runner, the 11A-R2 Muon-lineage contract, or the 11A-B0 seed authority.

## Contradiction closed

The existing 11A branch runner maps:

```text
schedule.requestedGenerationCount
-> --production-loop-optimizer-steps
```

The existing BaseTrain N8 admission requires exactly:

```text
--production-loop-optimizer-steps 8
```

Therefore the earlier `REPLAY_ONLY` two-generation physical smoke was not an executable N8 topology. A request of `2` would reach BaseTrain as a two-step N8 run and fail with the existing exact-eight gate.

R3 rejects that contradiction in 11A before child launch.

## Physical horizon SSOT

```text
BaseTrain exact N8 physical contract = 8 optimizer steps
```

11A does not define a second N8 length.

For R3:

```text
requestedGenerationCount
== physicalOptimizerStepHorizon
== effectiveProductionLoopOptimizerSteps
== 8
```

The common-args surface remains forbidden from carrying `--production-loop-optimizer-steps`, so the branch schedule remains the only horizon authority supplied to the existing branch runner.

## Admission

Before any child BaseTrain process is launched, 11A-R3 requires:

```text
generationCount == 8
```

Failure:

```text
ASH_BP_DK_LEGACY_MIGRATION_EXACT_N8_CAPTURE_HORIZON_REQUIRED
```

This preserves the existing BaseTrain failure:

```text
BASETRAIN_N8_EXACTLY_EIGHT_OPTIMIZER_STEPS_REQUIRED
```

as a downstream invariant rather than using it as normal 11A input validation.

## REPLAY_ONLY

The first physical migration capture target is:

```text
captureProfile = REPLAY_ONLY
requestedGenerationCount = 8
captureHorizonMode = EXACT_N8_WINDOW
```

The prior `generation-count 2` smoke is superseded for physical N8 execution. Historical R1/R2 artifacts are preserved and are not rewritten.

## Promotion-ready profile boundary

R3 applies the same exact-eight physical window preflight to all 11A physical captures because the current branch runner performs one BaseTrain invocation and BaseTrain's N8 contract is exact-eight.

`PROMOTION_READY_OBSERVED` must additionally satisfy its existing 08A qualification and recommendation-guard requirements. R3 does not fabricate a multi-window promotion runner. If an existing recommendation guard requires a horizon larger than one exact N8 window, that profile remains inadmissible until a separate explicit multi-window authority exists.

## Source authority

Current source lineage:

```text
sourceRun = n8_perf_20260820_002426
sourceTrainingGeneration = 6
sourceOptimizerGeneration = 6
sourceCheckpointDigest = d4dcc266fe4e9c3691176e0041f736dc1809b90c04dabb358403a9a2568041b2
```

The source checkpoint remains read-only. R3 preserves the existing pre/post checkpoint authority digest mutation gate.

No arithmetic final-checkpoint identity is fabricated. The final generation/optimizer identity is observed from the child runtime output.

## Legacy restart barrier

The already sealed legacy restart barrier remains unchanged:

```text
legacyRestartBarrierDigest = 80f450c27ae356c9ae03e5d45e6f4e14a1d59556f74c1b705abd70b85aa6ddc6
15C-R2 unresolvedPendingStateCount = 0
15A-R1 legacy restart barrier = PASS
```

R3 does not mutate or reseal that barrier.

## Seed authority

The already sealed 11A-B0 evidence-only seed remains unchanged.

Required semantic authority remains:

```text
historicalSeedRecovered = false
migrationEvidenceAuthority = true
productionAuthority = false
activationAuthority = false
immutableSeed = true
canonicalValidationPassed = true
readyFor11aReplayOnly = true
```

R3 does not rewrite, reapprove, or activate the seed.

## Model identity

The current source run physically records:

```text
modelSpecId = model_tinyllama_1p1b_v5_48259
runtimeModelSpecSemanticDigest = 48d0b3af664cacfb079725101b359dc221cc33121efbdc359b4dedc5e65e7256
```

The existing 11A model-spec path parity check remains in force. R3 does not add a second model-spec authority.

## Muon lineage preservation

11A-R2 semantics are unchanged:

```text
EXISTING
-> RESUME_EXISTING

LEGACY_ABSENT
-> INITIALIZE_EPHEMERAL_NEW_LINEAGE

PARTIAL
-> FAIL
```

Generic common args remain forbidden from owning `--admit-tensorcube-local-muon-new-lineage`.

## Common-args ownership

11A continues to reject operator common args containing:

```text
--output-dir
--resume-training-state
--r6-parent-r5-run-dir
--production-loop-optimizer-steps
--basetrain-storage-root
--atlas-plan-output-dir
```

11A continues to require:

```text
--admit-production-multistep-loop
--admit-n8-long-horizon-continuity
--admit-tensorcube-local-muon-production-callsite
```

The existing branch runner remains the sole owner of the physical step flag and supplies:

```text
--production-loop-optimizer-steps <schedule.requestedGenerationCount>
```

R3 guarantees that this value is `8` before the runner is invoked.

## Capture receipt revision

Capture receipt advances from:

```text
ash.bp_dk.fusion_legacy_migration.evidence_capture.r2
```

to:

```text
ash.bp_dk.fusion_legacy_migration.evidence_capture.r3
```

Capture patch identity advances to:

```text
ASH-BP-DK-FUSION-LEGACY-MIGRATION-EXACT-N8-CAPTURE-HORIZON-CLOSURE-11A-R3
```

The internal 11A seed-authority receipt remains R2-owned because R3 does not change its semantics.

## New receipt fields

```text
captureHorizonRevision
physicalOptimizerStepHorizon
effectiveProductionLoopOptimizerSteps
exactN8HorizonParity
syntheticResumeCutCount
```

Required values:

```text
captureHorizonRevision = ash.bp_dk.fusion_legacy_migration.exact_n8_capture_horizon.r3
requestedGenerationCount = 8
physicalOptimizerStepHorizon = 8
effectiveProductionLoopOptimizerSteps = 8
exactN8HorizonParity = true
syntheticResumeCutCount = 0
```

Receipt validation fails closed on any drift:

```text
ASH_BP_DK_LEGACY_MIGRATION_CAPTURE_HORIZON_EFFECTIVE_ARG_MISMATCH
```

## No synthetic cut role

R3 does not introduce:

```text
2-step migration cut
4-step migration cut
fake resume leg
migration-only partial N8 window
parallel N8 horizon CLI
```

`syntheticResumeCutCount` is sealed as zero for R3.

## Evidence semantics

A successful physical capture still requires the existing isolated 11A evidence lineage and final heads:

```text
bp_dk_fusion_objective_long_horizon_trajectory_head.json
bp_dk_fusion_policy_calibration_replay_evidence_head.json
```

`REPLAY_ONLY` capture completion is distinct from downstream promotion sufficiency. `promotionReady=false` remains a valid result for an evidence-only replay capture.

## Implementation surface

R3 changes only:

```text
crates/base_train/src/bp_delta_k_fusion_legacy_migration_seed_policy_evidence_capture.rs
crates/base_train/src/bin/ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a.rs
tools/validate_ash_bp_dk_fusion_legacy_migration_exact_n8_capture_horizon_closure_11a_r3_static.py
```

Unchanged:

```text
crates/base_train/src/bin/base_train.rs
crates/base_train/src/bp_delta_k_fusion_policy_candidate_canary_qualification.rs
11A-B0 seed bootstrap
15C-R2 storage classifier
N8 scheduler
optimizer kernels
08-BASE attribution
```

## Regression tests

R3 adds focused Rust regression tests:

```text
exact_n8_capture_horizon_11a_r3_replay_only_eight_is_admitted
exact_n8_capture_horizon_11a_r3_replay_only_two_is_rejected_before_child_launch
```

The positive case admits exactly eight. The negative case proves the old two-generation fiction is rejected before child execution.

## Static validation

Bake-side static validation:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EXACT_N8_CAPTURE_HORIZON_CLOSURE_11A_R3_STATIC 22/22
```

Parent B0 static validation also remains:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_SEED_AUTHORITY_BOOTSTRAP_11A_B0_STATIC 17/17
```

The bake environment has no Rust toolchain. Windows Rust compilation and regression execution remain the type/borrow/runtime authority.

## Windows acceptance

```text
cargo check --locked -p base_train --bin ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a
cargo test --locked -p base_train --lib exact_n8_capture_horizon_11a_r3 -- --nocapture
cargo build --release --locked -p base_train --bin ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a
```

Physical acceptance requires a `REPLAY_ONLY` invocation with:

```text
--generation-count 8
```

and expects:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EXACT_N8_CAPTURE_HORIZON_CLOSURE_11A_R3
requested_generation_count=8
physical_optimizer_step_horizon=8
effective_production_loop_optimizer_steps=8
exact_n8_horizon_parity=1
synthetic_resume_cut_count=0
```

## Prohibitions

```text
No Two-Step N8 Fiction
No BaseTrain N8 Gate Relaxation
No Synthetic Resume-Cut Role
No Common-Args Horizon Override
No Parallel Horizon Knob
No Source Checkpoint Rewrite
No Seed Authority Rewrite
No Managed Production Activation
No Muon Lineage Semantic Change
No Final Checkpoint Identity Guess
```

## Final SSOT

```text
Legacy Resume Source
-> 11A-B0 Evidence-Only Seed
-> 11A-R3 Exact N8 Preflight
-> schedule.requestedGenerationCount = 8
-> existing branch runner
-> BaseTrain --production-loop-optimizer-steps 8
-> existing BaseTrain exact-N8 gate
-> isolated evidence capture
-> trajectory/replay heads
```

There is one physical N8 horizon authority: eight optimizer steps.
