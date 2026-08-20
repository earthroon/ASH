# ASH-BP-DK-FUSION-POLICY-LEGACY-RESTART-BARRIER-CLOSURE-15A-R1

## Patch identity

```text
ASH-BP-DK-FUSION-POLICY-LEGACY-RESTART-BARRIER-CLOSURE-15A-R1

Legacy Unbound Checkpoint Classification /
Replay-Head Absence Explicit Seal /
Policy-Binding Absence Explicit Seal /
Checkpoint-Digest Quiescence Barrier /
No Synthetic Source Policy /
Qualified First Managed Policy Adoption /
Revision-1 Pointer Bootstrap Authority /
Legacy Adoption Intent /
Managed Restart Exact Binding /
Source Checkpoint Read-Only Preservation /
First Managed Generation Closure /
One-Way Legacy->Managed Transition Seal
```

Parent:

```text
ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
```

15A is additive. Normal managed Activation-15 barriers remain replay-bound and normal managed-to-managed policy transitions continue to use `AshBpDkFusionPolicyActivationIntent` and `AshFusionPolicyActivationBarrierReceipt`.

## Problem closed

A pre-managed checkpoint can legitimately contain a durable training state while having neither:

```text
bp_dk_fusion_active_policy_binding.json
bp_dk_fusion_policy_calibration_replay_evidence_head.json
```

The old legacy restart branch required a normal transition intent and normal activation barrier. The normal barrier itself requires replay evidence, and the normal transition intent assumes an already-observed source policy. That creates an unreachable migration path for a true pre-managed checkpoint.

15A does not fabricate the missing historical policy or replay ledger. It introduces a distinct `LEGACY_UNBOUND` authority lane.

## Legacy state classification

`LEGACY_UNBOUND` is accepted only when all of the following are true:

```text
durable checkpoint authority resolves
active training state resolves
packed state manifest resolves
checkpoint policy binding is absent
BP-DK replay head is absent
pending .partial/.tmp/.staging state count is zero
```

State matrix:

```text
binding absent + replay absent -> LEGACY_UNBOUND
binding present + replay present -> already managed, 15A forbidden
exactly one present -> partial policy state, hard failure
```

No source policy digest and no BP generation are invented for `LEGACY_UNBOUND`.

## New schemas

```text
ash.bp_dk.fusion_policy.legacy_restart_barrier.r1
ash.bp_dk.fusion_policy.legacy_policy_adoption_intent.r1
ash.bp_dk.fusion_policy.legacy_authority_bootstrap_receipt.r1
ash.bp_dk.fusion_policy.legacy_restart_closure.r1
```

Core types:

```text
AshBpDkFusionLegacySourceAuthority::LegacyUnbound
AshBpDkFusionLegacyRestartBarrierReceipt
AshBpDkFusionLegacyPolicyAdoptionIntent
AshBpDkFusionLegacyAuthorityBootstrapReceipt
AshBpDkFusionLegacyRestartClosureReceipt
```

## Legacy restart barrier

`seal_legacy_restart_barrier()` executes under the existing managed-trainer authority lock with purpose `LEGACY_RESTART_BARRIER`.

The barrier seals:

```text
source checkpoint digest
last committed training generation
last committed optimizer generation
policy-binding absence
replay-head absence
pending-state count = 0
trainer quiescence
durable-checkpoint completeness
operator identity
```

It does not contain `sourcePolicyDigest` or `lastCommittedBpGeneration`.

`verify_legacy_restart_barrier_current()` re-resolves checkpoint authority and rechecks both absences immediately before restart. A binding or replay head appearing after barrier seal makes the barrier stale.

## First managed policy adoption

A legacy checkpoint does not authorize an arbitrary target policy.

`bootstrap_managed_fusion_policy_authority_from_legacy_unbound()` requires:

```text
valid target policy
valid canary qualification receipt
valid qualification ticket
valid operator review receipt
qualification ticket digest parity
review receipt digest parity
candidate policy digest parity
BoundedTrainingCanary / QualifiedForActivationReview lineage
current legacy barrier still exact
no existing active pointer
```

The target is an explicit qualified adoption, not a claimed continuation of an unobserved historical policy.

The new `AshBpDkFusionLegacyPolicyAdoptionIntent` contains:

```text
sourceAuthority = LEGACY_UNBOUND
source checkpoint digest
source training generation
source optimizer generation
legacy restart barrier digest
target policy revision/digest
qualification/review digests
effective-after optimizer generation
operator identity
```

There is deliberately no source policy digest field.

## Revision-1 active pointer

The legacy bootstrap writes the qualified target into the immutable policy store and creates exactly one revision-1 active pointer:

```text
pointerRevision = 1
previousPointerDigest = null
policyDigest = target policy digest
activationIntentDigest = legacy adoption intent digest
effectiveAfterOptimizerGeneration = legacy source optimizer generation
```

The active pointer is created only when no managed pointer already exists.

Artifacts are stored under:

```text
<policy_root>/policies/<target-policy-digest>.json
<policy_root>/active/bp_dk_fusion_active_policy.json
<policy_root>/bootstrap/legacy/<legacy-intent-digest>/intent.json
<policy_root>/bootstrap/legacy/<legacy-intent-digest>/barrier.json
<policy_root>/bootstrap/legacy/<legacy-intent-digest>/receipt.json
```

The source checkpoint is not modified.

## Managed restart dispatch

`run_managed_base_train_process()` now has two mutually exclusive transition lanes.

```text
managed checkpoint binding present
  -> normal Activation-15 transition intent/barrier when policy changes

checkpoint binding absent
  -> 15A legacy adoption intent + legacy restart barrier
```

Normal transition and legacy transition arguments cannot be mixed.

For the legacy lane, validation requires:

```text
sourceAuthority = LEGACY_UNBOUND
pointer revision = 1
previous pointer = none
pointer activation-intent digest = legacy adoption intent digest
pointer policy = target policy
legacy intent barrier digest = supplied legacy barrier
resume checkpoint digest exact
resume optimizer generation exact
effective-after generation exact
legacy barrier still current
```

The managed launcher remains the only process that injects the ACTIVE planner policy and startup-binding environment.

After child execution, the source legacy barrier is revalidated before the output checkpoint binding is written.

## One-way closure

`close_legacy_restart()` proves the transition completed.

It requires:

```text
source legacy barrier still current
active pointer still revision 1 with no predecessor
output training generation > source training generation
output optimizer generation > source optimizer generation
output checkpoint policy binding exists and matches active pointer
output replay head exists and validates
output replay generations match output checkpoint
output BP generation exists
source mutation count = 0
legacy transition count = 1
```

After a managed output contains its normal checkpoint binding, the legacy lane is no longer valid for that lineage. Future restarts return to normal Activation 15.

## CLI surface

The existing Activation-15 binary gains additive subcommands:

```text
seal-legacy-restart-barrier
bootstrap-legacy-managed-authority
close-legacy-restart
```

`run-managed-production` gains:

```text
--legacy-adoption-intent
--legacy-restart-barrier
```

The existing normal transition arguments remain unchanged.

The PowerShell runner accepts the matching actions:

```text
SealLegacyRestartBarrier
BootstrapLegacyManagedAuthority
CloseLegacyRestart
```

## Failure semantics

Representative hard failures:

```text
ASH_BP_DK_FUSION_LEGACY_RESTART_ALREADY_MANAGED
ASH_BP_DK_FUSION_LEGACY_BARRIER_PARTIAL_POLICY_STATE
ASH_BP_DK_FUSION_LEGACY_RESTART_BARRIER_POLICY_STATE_CHANGED
ASH_BP_DK_FUSION_LEGACY_BOOTSTRAP_ACTIVE_POINTER_ALREADY_EXISTS
ASH_BP_DK_FUSION_LEGACY_BOOTSTRAP_QUALIFICATION_TICKET_DRIFT
ASH_BP_DK_FUSION_LEGACY_BOOTSTRAP_REVIEW_DIGEST_DRIFT
ASH_BP_DK_FUSION_LEGACY_BOOTSTRAP_TARGET_POLICY_DRIFT
ASH_BP_DK_FUSION_LEGACY_RESTART_NORMAL_TRANSITION_MUTUALLY_EXCLUSIVE
ASH_BP_DK_FUSION_LEGACY_RESTART_NORMAL_TRANSITION_FORBIDDEN
ASH_BP_DK_FUSION_MANAGED_LEGACY_RESTART_ADOPTION_INTENT_REQUIRED
ASH_BP_DK_FUSION_MANAGED_LEGACY_RESTART_BARRIER_REQUIRED
ASH_BP_DK_FUSION_LEGACY_RESTART_POINTER_REVISION_NOT_ONE
ASH_BP_DK_FUSION_LEGACY_RESTART_POINTER_HAS_PREVIOUS_AUTHORITY
ASH_BP_DK_FUSION_LEGACY_RESTART_CHECKPOINT_DRIFT
ASH_BP_DK_FUSION_LEGACY_RESTART_EFFECTIVE_BOUNDARY_DRIFT
ASH_BP_DK_FUSION_LEGACY_RESTART_CLOSURE_OUTPUT_BINDING_REQUIRED
ASH_BP_DK_FUSION_LEGACY_RESTART_CLOSURE_OUTPUT_REPLAY_REQUIRED
```

## No semantic changes outside policy authority migration

15A does not change:

- forward/backward math,
- AdamW/Muon/HiMuon math,
- gradient values,
- TensorCube execution,
- scheduler or dataset order,
- checkpoint serialization,
- N8 Deferred Durable Writeback,
- storage publication,
- normal Activation-15 replay-bound barrier semantics.

## Implementation surface

Baked overlay contains 10 files:

```text
crates/ash_core/src/fusion_policy_explicit_production_activation.rs
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs
crates/base_train/src/bin/ash_bp_dk_fusion_policy_explicit_production_activation_15.rs
tools/run_ash_bp_dk_fusion_policy_explicit_production_activation_15.ps1
tools/validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
tools/validate_ash_bp_dk_fusion_policy_legacy_restart_barrier_closure_15a_r1_static.py
tools/validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
tools/validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
tools/validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

Because `base_train.rs` is unchanged, only downstream validators that directly pin Activation-15 source files require parent-SHA rebinding: 16, 17, and 18. The 19-21 lineage remains byte-valid without new SHA edits.

## Static evidence

```text
Activation 15 existing validator:                             275/275 PASS
Legacy Restart Barrier Closure 15A R1:                       153/153 PASS
Production Soak/Rollback 16:                                 177/177 PASS
Production Long Horizon 17:                                  225/225 PASS
Production Recalibration Bridge 18:                          298/298 PASS
Production Calibration Adoption 19:                          230/230 PASS
Production Aware Recommendation 20:                          237/237 PASS
Production Operator Review/Adoption 21:                      265/265 PASS
N8 HiMuon Production Hotpath Bind R1:                          86/86 PASS
N8 Phase Wall-Time Attribution R1:                             77/77 PASS
N8 Deferred Durable Writeback R1:                             PASS
```

The bake environment has no Rust toolchain. Release CF1 in the authoritative Windows checkout remains the compilation/type/borrow and full-fixture authority.

## CF1 order

The new validator is inserted directly after Activation 15 and before 16:

```text
14 -> 15 -> 15A-R1 -> 16 -> 17 -> 18 -> 19 -> 20 -> 21
```

## Promotion tokens

```text
PASS_ASH_BP_DK_FUSION_POLICY_LEGACY_RESTART_BARRIER_STRUCTURAL_15A_R1
PASS_ASH_BP_DK_FUSION_POLICY_LEGACY_UNBOUND_CLASSIFICATION_15A_R1
PASS_ASH_BP_DK_FUSION_POLICY_LEGACY_RESTART_BARRIER_PHYSICAL_15A_R1
PASS_ASH_BP_DK_FUSION_POLICY_LEGACY_FIRST_MANAGED_AUTHORITY_BOOTSTRAP_15A_R1
PASS_ASH_BP_DK_FUSION_POLICY_LEGACY_MANAGED_RESTART_TRANSITION_15A_R1
PASS_ASH_BP_DK_FUSION_POLICY_LEGACY_TO_MANAGED_ONE_WAY_CLOSURE_15A_R1
PROMOTE_ASH_BP_DK_FUSION_POLICY_LEGACY_RESTART_BARRIER_CLOSURE_15A_R1
```

## Final SSOT

```text
A legacy checkpoint is not a checkpoint with a guessed old policy.

LEGACY_UNBOUND means that a durable checkpoint exists while neither a managed BP-DeltaK checkpoint-policy binding nor a BP-DeltaK replay head exists.

The absence of historical policy evidence is sealed as evidence. No historical policy digest, BP generation, replay ledger, or checkpoint binding is synthesized retroactively.

Normal Activation-15 barriers remain replay-bound.

The first managed policy is an explicitly qualified target adoption represented by a dedicated LegacyPolicyAdoptionIntent and exactly one revision-1 active pointer.

The source checkpoint remains immutable. Only a successful new managed run receives the normal checkpoint-policy binding and new replay evidence.

LEGACY_UNBOUND -> MANAGED_BOUND is explicit, digest-bound, one-way, and non-fabricating.
```
