# ASH-BP-DK-FUSION-LEGACY-RESTART-BARRIER-TRANSACTION-MARKER-CLASSIFICATION-15C-R1

## Patch identity

```text
ASH-BP-DK-FUSION-LEGACY-RESTART-BARRIER-
TRANSACTION-MARKER-CLASSIFICATION-15C-R1

Committed Transaction Residue Classification /
Canonical Staging Marker Recognition /
Read-Only Legacy Checkpoint Inspection /
Unresolved Transient Hard-Fail Preservation /
Double-Buffer Historical Slot Acceptance /
Commit-Lineage Evidence Binding /
Storage Quiescence Semantic Repair /
Activation 15 Shared Classifier Preservation Seal
```

Build revision:

```text
bp-dk-fusion-legacy-restart-barrier-transaction-marker-classification-15c-r1
```

Parents:

```text
ASH-BP-DK-FUSION-POLICY-EXPLICIT-PRODUCTION-ACTIVATION-15
ASH-BP-DK-FUSION-POLICY-LEGACY-RESTART-BARRIER-CLOSURE-15A-R1
ASH-BP-DK-FUSION-MANAGED-TRAINER-AUTHORITY-WINDOWS-LOCK-DURABILITY-RECOVERY-15B-R1
```

15C changes storage-quiescence classification only. Activation policy authority, LEGACY_UNBOUND migration semantics, and the 15B managed-trainer authority lock remain unchanged.

## Observed physical blocker

After 15B removed the Windows lock/durability blocker, the legacy restart barrier advanced to:

```text
ASH_BP_DK_FUSION_LEGACY_RESTART_BARRIER_PENDING_STORAGE_STATE
```

The source checkpoint contained:

```text
slot_a/transaction.staging.json   active slot
slot_b/transaction.staging.json   inactive slot
```

The previous shared scanner counted every filename containing `.partial`, `.tmp`, or `.staging` as unresolved pending storage. This made the canonical `transaction.staging.json` marker indistinguishable from an unfinished transient file.

The trainer, however, writes `transaction.staging.json` as a canonical transaction witness and does not delete that file when the staging guard is marked committed. Therefore committed double-buffer slots can retain canonical staging witnesses after the transaction lineage has already closed.

## Core invariant

```text
COMMITTED_TRANSACTION_RESIDUE != UNRESOLVED_PENDING_STORAGE
```

15C does not exempt `.staging` files by name. It replaces substring-only classification with semantic transaction-lineage validation.

The exact canonical filename:

```text
transaction.staging.json
```

is eligible for committed-residue classification. Unknown `.staging` files, `.partial` files, and `.tmp` files remain unresolved pending storage.

## Canonical writer schema

15C moves the canonical staging payload into the trainer-side shared typed contract:

```text
AshTrainingTransactionStagingMarker
ASH_TRAINING_TRANSACTION_STAGING_FILENAME
```

The marker owns the existing writer fields:

```text
state
sourceSlot
candidateSlot
sourceGeneration
candidateGeneration
sourceOptimizerStep
candidateOptimizerStep
microbatchCount
```

Validation preserves the existing scheduler contract:

```text
state == STAGING
sourceSlot in {GENESIS_CACHE, slot_a, slot_b}
candidateSlot in {slot_a, slot_b}
sourceSlot != candidateSlot
candidateGeneration == sourceGeneration + 1
candidateOptimizerStep == sourceOptimizerStep + 1
microbatchCount == R6_ACCUMULATION
```

The scheduler now serializes this shared typed marker instead of rebuilding an independent ad-hoc JSON object.

## Shared storage-quiescence classifier

The old raw `count_pending_state_markers()` behavior is replaced by a shared semantic classifier used by both the normal Activation-15 barrier and the Legacy Restart Barrier.

The classifier records:

```text
observedPartialCount
observedTmpCount
observedStagingCount
committedTransactionResidueCount
unresolvedPendingStateCount
```

Receipt ABI remains stable. Existing `pendingStateCount` maps to:

```text
unresolvedPendingStateCount
```

rather than the number of filenames containing a transient-looking substring.

## Marker dispatch

Classification priority is:

```text
filename contains .partial
    -> unresolved pending

filename contains .tmp
    -> unresolved pending

filename exactly transaction.staging.json
    -> semantic transaction classifier

other filename contains .staging
    -> unresolved pending
```

15C therefore does not weaken generic transient-file protection.

## Canonical staging location

Committed-residue classification is available only for canonical markers directly under a canonical double-buffer slot:

```text
training_state/slot_a/transaction.staging.json
training_state/slot_b/transaction.staging.json
```

Unexpected nesting or noncanonical slot ownership cannot be promoted to committed residue.

## Commit-lineage evidence chain

A canonical staging marker is classified as committed residue only when its existing transaction lineage is proven consistent.

The classifier verifies, without mutating the source checkpoint:

```text
1. transaction.staging.json parses through the shared typed writer schema
2. marker validates
3. marker candidateSlot matches the containing slot
4. candidate generation/optimizer step are not future relative to active state
5. transaction.validated.json exists and is consistent
6. transaction.ready_for_commit.json exists and is consistent
7. validated packed-state manifest digest matches the physical packed_state_manifest.json SHA-256
8. committed_training_state_step_<candidateOptimizerStep>.json exists
9. committed history generation/step/slot/manifest identity matches the marker lineage
10. committed training-state digest is recomputed and verified
11. source committed history is verified when sourceSlot is slot_a or slot_b
12. active/historical lineage rules are satisfied
```

`transaction.validated.json` or `transaction.ready_for_commit.json` alone is not final commit authority.

## Active-slot classification

A candidate in the current active slot is committed residue only when:

```text
candidate generation == active generation
candidate optimizer step == active optimizer step
candidate slot == active slot
candidate manifest digest == active manifest digest
active_training_state.json SHA-256 == corresponding committed history SHA-256
```

Active-slot location alone does not prove pending or committed state.

## Historical inactive-slot classification

An inactive-slot candidate may be committed historical residue only when the complete commit lineage is valid and:

```text
candidate generation < active generation
candidate optimizer step < active optimizer step
```

Inactive-slot location alone is never treated as safe.

## Hard-fail preservation

The following remain unresolved pending storage:

```text
unknown *.staging files
*.partial files
*.tmp files
malformed canonical staging JSON
invalid staging schema
noncanonical marker location
candidate-slot mismatch
missing validated/ready/manifest/committed-history evidence
manifest digest mismatch
generation or optimizer-step mismatch
invalid committed training-state digest
future-generation transaction marker
incomplete source history
```

No timestamp or file age is used as commit authority.

## Read-only legacy checkpoint contract

15C performs classification only.

It must not:

```text
remove
rename
rewrite
touch
normalize
repair
```

any source checkpoint file.

In particular, the existing `transaction.staging.json` files remain physically unchanged when the legacy barrier is evaluated.

## Diagnostic truth

The shared classifier emits:

```text
[ASH-BP-DK-FUSION-STORAGE-QUIESCENCE-15C]
observedPartialCount=<n>
observedTmpCount=<n>
observedStagingCount=<n>
committedTransactionResidueCount=<n>
unresolvedPendingStateCount=<n>
```

For the currently observed gen5 checkpoint, a successful physical classification is expected only if both slot lineages prove committed:

```text
observedStagingCount=2
committedTransactionResidueCount=2
unresolvedPendingStateCount=0
```

The specification does not assume that result without physical lineage verification.

## Parent semantics preserved

15C does not change:

```text
Activation-15 candidate qualification
operator review
normal managed activation barrier semantics
15A LEGACY_UNBOUND = binding absent + replay absent
15A partial-policy-state hard fail
legacy source checkpoint read-only rule
revision-1 legacy managed bootstrap semantics
15B R2 owner identity
15B R1 fail-closed compatibility
15B stale lock quarantine
15B bounded reacquisition
15B Windows durability mode
```

## Implementation surface

The baked overlay contains 12 files:

```text
crates/base_train/src/bp_delta_k_fusion_policy_explicit_production_activation.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs

tools/validate_ash_bp_dk_fusion_policy_explicit_production_activation_15_static.py
tools/validate_ash_bp_dk_fusion_managed_trainer_authority_windows_lock_durability_recovery_15b_r1_static.py
tools/validate_ash_bp_dk_fusion_legacy_restart_barrier_transaction_marker_classification_15c_r1_static.py
tools/validate_ash_bp_dk_fusion_policy_production_soak_and_rollback_health_16_static.py
tools/validate_ash_bp_dk_fusion_policy_production_long_horizon_stability_17_static.py
tools/validate_ash_bp_dk_fusion_policy_production_evidence_recalibration_bridge_18_static.py
tools/validate_ash_bp_dk_fusion_policy_production_calibration_adoption_19_static.py
tools/validate_ash_bp_dk_fusion_policy_production_aware_recommendation_20_static.py
tools/validate_ash_bp_dk_fusion_policy_production_operator_review_and_adoption_21_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

No `*.sha256`, generated artifact tree, manifest bundle, or Python cache is included.

The scheduler change is rebased on the current N8 HiMuon production-hotpath scheduler rather than an older archive copy.

## Source hash fanout

Activation policy source:

```text
15B parent:
1e110a99c0087db2ad25bd98397ed70bf6f8722a89140ae061688220a6f69bc8

15C:
066f3ae28c116e11fbbfa701b736ed84354798cbf13e3683d5a57e4c9ff07a20
```

Scheduler source:

```text
HiMuon parent:
1725aef6fe06fbbc1c9936a42d8b91bc256c3a2ea249e5f439284ee651b791f3

15C:
bd6e16f44816c0422b4e0829aed82461921b305b9e6066e949410dcce05a3e5c
```

Exact occurrence rebaking produced:

```text
activation-source SHA pins -> validators 16, 17, 18
scheduler-source SHA pins  -> validators 16, 17, 18, 19, 20, 21
```

No unrelated downstream SHA is changed.

## CF1 order

The compile-chain order is now:

```text
14
-> 15
-> 15A
-> 15B
-> 15C
-> 16
-> 17
-> 18
-> 19
-> 20
-> 21
```

## Static evidence

Observed on the reconstructed cumulative source tree:

```text
Activation 15:                                  281/281 PASS
Legacy Restart Barrier Closure 15A:             153/153 PASS
Windows Lock Durability Recovery 15B:             93/93 PASS
Transaction Marker Classification 15C:           105/105 PASS
Production Soak/Rollback 16:                     177/177 PASS
Production Long Horizon 17:                      225/225 PASS
Production Recalibration Bridge 18:              298/298 PASS
Production Calibration Adoption 19:              230/230 PASS
Production Aware Recommendation 20:              237/237 PASS
Production Operator Review/Adoption 21:          265/265 PASS
N8 HiMuon Production Hotpath Bind:                 86/86 PASS
N8 Phase Wall-Time Attribution:                    77/77 PASS
N8 Deferred Durable Writeback:                    118/118 PASS
```

The bake environment does not contain the Rust toolchain. Windows Release CF1 remains authoritative for compile/type/borrow validation and physical runtime evidence.

## Physical acceptance

The Windows physical run must prove:

```text
Release CF1 PASS
fresh Activation-15 release binary
current gen5 canonical staging marker count = 2
both marker payloads parse through the canonical writer schema
slot_a transaction lineage is proven or explicitly fails
slot_b transaction lineage is proven or explicitly fails
no source checkpoint mutation occurs
seal-legacy-restart-barrier exits 0 only when unresolvedPendingStateCount == 0
barrier receipt exists on success
managed-trainer authority lock is absent after command return
pendingStateCount == 0 on successful barrier
legacyUnbound == true on successful barrier
```

Before and after the barrier, source staging markers and checkpoint authority inputs must remain byte-identical.

## Promotion state

Structural token:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_RESTART_BARRIER_TRANSACTION_MARKER_CLASSIFICATION_STRUCTURAL_15C_R1
```

Physical token:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_RESTART_BARRIER_TRANSACTION_MARKER_CLASSIFICATION_PHYSICAL_15C_R1
```

Final promotion:

```text
PROMOTE_ASH_BP_DK_FUSION_LEGACY_RESTART_BARRIER_TRANSACTION_MARKER_CLASSIFICATION_15C_R1
```

Until Windows physical validation succeeds:

```text
HOLD_ASH_BP_DK_FUSION_LEGACY_RESTART_BARRIER_TRANSACTION_MARKER_CLASSIFICATION_PHYSICAL_REQUIRED_15C_R1
```

## Final SSOT

```text
A transaction marker is not pending merely because its filename contains .staging.

The canonical transaction.staging.json marker is a transaction-state witness. Its meaning is resolved through the existing trainer transaction schema and committed checkpoint lineage.

A canonical staging marker may be classified as committed residue only when the committed transaction, slot identity, generation/optimizer identity, packed-state manifest, and committed-history digest are proven consistent.

Active and inactive slots are evaluated by evidence, not by location alone.

Unknown staging files, partial files, temporary files, malformed markers, missing commit evidence, slot drift, generation drift, manifest drift, and future-generation markers remain unresolved pending storage and block the barrier.

The source legacy checkpoint remains strictly read-only. 15C classifies existing state and never repairs, deletes, renames, or normalizes it.

Both normal Activation-15 and Legacy Restart Barrier use the same storage-quiescence classifier.

pendingStateCount means unresolved durable-storage state, not the number of filenames containing a transient-looking substring.

Activation-15 policy authority, 15A LEGACY_UNBOUND migration semantics, and 15B managed-trainer authority semantics remain unchanged.
```
