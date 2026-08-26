# ASH-BP-DK-FUSION-LEGACY-MIGRATION-SEED-AUTHORITY-BOOTSTRAP-11A-B0

## Purpose

Create a new, explicitly reviewed BP-DK migration seed authority when the historical approved seed artifact is not recoverable. B0 does not reconstruct or claim recovery of the missing seed.

```text
05-compatible candidate
-> explicit operator review
-> existing canonical policy validation
-> immutable seed snapshot
-> evidence-only seed authority receipt
-> 11A-R2 REPLAY_ONLY 2-generation handoff
```

## Identity

```text
patchId = ASH-BP-DK-FUSION-LEGACY-MIGRATION-SEED-AUTHORITY-BOOTSTRAP-11A-B0
reviewSchema = ash.bp_dk.fusion_legacy_migration.seed_bootstrap_operator_review.r1
receiptSchema = ash.bp_dk.fusion_legacy_migration.seed_authority_bootstrap.r1
authorityScope = LEGACY_MIGRATION_EVIDENCE_ONLY
PASS = PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_SEED_AUTHORITY_BOOTSTRAP_11A_B0
```

## Authority boundary

The resulting seed has exactly:

```text
historicalSeedRecovered = false
migrationEvidenceAuthority = true
productionAuthority = false
activationAuthority = false
immutableSeed = true
canonicalValidationPassed = true
readyFor11aReplayOnly = true
```

B0 never creates or changes:

```text
active/bp_dk_fusion_active_policy.json
bp_dk_fusion_active_policy_binding.json
bp_dk_fusion_policy_startup_binding.json
```

## SSOT ownership

```text
candidate body             -> operator-supplied candidate JSON
policy validation/digest   -> AshBpDkFusionFissionPolicy::validate/canonical_digest
operator approval          -> B0 operator_review.json
source checkpoint          -> checkpoint_authority_digest
legacy migration admission -> existing typed legacy restart barrier
managed production state   -> managed policy root, read-only witness
final seed                 -> authority/seed_policy.json
B0 receipt                 -> authority/seed_authority_receipt.json
```

Operator review does not replace policy validation. Policy validation does not replace operator approval.

## 05-compatible policy contract

B0 reuses `AshBpDkFusionFissionPolicy` unchanged. Required semantic fields are:

```text
revision
fuseCosineMin
fuseInformationMax
fuseMaterialMin
fuseDeltaKMax
fuseConfirmGenerations
fissionCosineFloor
fissionInformationMin
fissionMaterialFloor
fissionDeltaKMin
fissionConfirmGenerations
cooldownGenerations
```

The existing validator remains authoritative for finite/range/hysteresis/confirmation rules. B0 introduces no second policy validator and no new policy digest algorithm.

## Candidate provenance

Supported explicit origins:

```text
OPERATOR_PROPOSED
REVIEWED_08A_DERIVED_CANDIDATE
```

`REVIEWED_08A_DERIVED_CANDIDATE` only identifies candidate provenance. It does not auto-promote an 08A fixture. The B0 binary contains no hard-coded threshold values.

## Explicit operator review

The binary provides a `review` subcommand. Decisions are:

```text
APPROVE_MIGRATION_EVIDENCE_ONLY
REJECT
```

An approved review must bind:

```text
candidatePolicyDigest == candidate canonical digest
productionAuthorityGranted = false
migrationEvidenceAuthorityGranted = true
operatorIdentity exact
reviewReason non-empty
reviewedAt non-empty
reviewDigest valid
```

A rejected review can exist as an audit artifact, but `bootstrap` must reject it.

## Legacy restart barrier binding

B0 validates the existing barrier and requires:

```text
legacyUnbound = true
pendingStateCount = 0
trainerQuiescent = true
durableCheckpointComplete = true
checkpointPolicyBindingPresent = false
replayHeadPresent = false
```

Barrier operator identity must equal B0 operator identity. Barrier source checkpoint digest must equal a freshly computed source checkpoint authority digest.

Optional CLI pins:

```text
--expected-source-checkpoint-digest
--expected-barrier-digest
```

must match exactly when supplied.

## Read-only gates

Source checkpoint authority digest is measured before and after B0:

```text
sourceCheckpointMutationCount = 0
```

The managed policy root is tree-digested before and after B0:

```text
managedAuthorityMutationCount = 0
```

The managed active pointer must be absent both before and after B0. The B0 output root must be outside both source checkpoint and managed policy root.

## Output layout

```text
<output-root>/
  candidate/candidate_policy.json
  review/operator_review.json
  authority/seed_policy.json
  authority/seed_authority_receipt.json
```

Outputs are immutable. An existing path is accepted only if the serialized bytes are identical. Different content at the same path fails closed.

## Canonical parity

Required:

```text
candidate canonical digest
== operatorReview.candidatePolicyDigest
== seed canonical digest
== seedAuthorityReceipt.seedPolicyDigest
```

Candidate and seed snapshots are parsed and validated again after materialization.

## Receipt

`ash.bp_dk.fusion_legacy_migration.seed_authority_bootstrap.r1` records:

```text
patchId
authorityScope
sourceCheckpoint/sourceCheckpointDigest
sourceTrainingGeneration/sourceOptimizerGeneration
legacyRestartBarrier/legacyRestartBarrierDigest
candidatePolicyPath/candidatePolicyDigest/candidatePolicySnapshotDigest
operatorReviewPath/operatorReviewDigest
seedPolicyPath/seedPolicyRevision/seedPolicyDigest/seedPolicySnapshotDigest
operatorIdentity
historicalSeedRecovered
migrationEvidenceAuthority
productionAuthority
activationAuthority
immutableSeed
canonicalValidationPassed
sourceCheckpointMutationCount
managedAuthorityMutationCount
readyFor11aReplayOnly
createdAt
receiptDigest
```

`createdAt` is bound to the explicit review time, preserving idempotency for identical inputs.

## Idempotency

Identical candidate, review, source, barrier, operator identity, managed-root state and output root must return the same seed and receipt digest.

Different content at an existing authority path fails with:

```text
ASH_BP_DK_MIGRATION_SEED_EXISTING_AUTHORITY_CONFLICT
```

No overwrite or silent revision replacement is allowed.

## Fail-closed conditions

```text
candidate missing or invalid
review missing/schema invalid/digest invalid
review candidate digest mismatch
review rejected
operator identity drift
production authority requested
legacy barrier mismatch
source checkpoint mismatch
managed active pointer already exists
source checkpoint mutation
managed authority mutation
candidate source mutation
review source mutation
candidate/seed body drift
candidate/seed canonical digest drift
immutable authority conflict
```

## Explicit prohibitions

```text
No Historical Seed Reconstruction
No Hidden Default Policy
No Test Fixture Auto-Promotion
No Threshold Guessing In B0 Binary
No Production Authority Grant
No Activation Authority Grant
No Managed Pointer Creation
No Checkpoint Mutation
No Cross-Run Seed Copy
No Silent Review Approval
No Seed Overwrite
```

## Current physical lineage

The current source was already sealed before B0:

```text
sourceRun = n8_perf_20260820_002426
sourceTrainingGeneration = 6
sourceOptimizerGeneration = 6
sourceCheckpointDigest = d4dcc266fe4e9c3691176e0041f736dc1809b90c04dabb358403a9a2568041b2
legacyRestartBarrierDigest = 80f450c27ae356c9ae03e5d45e6f4e14a1d59556f74c1b705abd70b85aa6ddc6
15C-R2 unresolvedPendingStateCount = 0
15A-R1 legacy restart barrier = PASS
```

These observed values are not baked defaults in B0.

## 11A-R2 handoff

After B0 PASS, 11A receives:

```text
--seed-policy <B0-output>/authority/seed_policy.json
--capture-profile replay-only
--generation-count 2
```

No 08A qualification receipt is required for this first REPLAY_ONLY smoke. B0 does not perform 12 recommendation, 13 review, 14 qualification, or 15 managed activation.

## Regression fixtures

Positive/idempotent fixture requires valid candidate, approved evidence-only review, exact barrier/source and mutation-zero managed authority. Expected:

```text
migrationEvidenceAuthority = true
productionAuthority = false
activationAuthority = false
readyFor11aReplayOnly = true
second identical bootstrap -> identical receiptDigest
```

Negative fixture mutates `candidatePolicyDigest` after review sealing and must fail review validation.

## Implementation surface

Added:

```text
crates/base_train/src/bp_delta_k_fusion_legacy_migration_seed_authority_bootstrap.rs
crates/base_train/src/bin/ash_bp_dk_fusion_legacy_migration_seed_authority_bootstrap_11a_b0.rs
tools/validate_ash_bp_dk_fusion_legacy_migration_seed_authority_bootstrap_11a_b0_static.py
```

Registered only in:

```text
crates/base_train/src/lib.rs
crates/base_train/Cargo.toml
```

Unchanged:

```text
11A evidence-capture runtime
15 activation runtime
N8 scheduler/optimizer
08-BASE attribution
checkpoint writer
```

## Validation

Bake-side static validation:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_SEED_AUTHORITY_BOOTSTRAP_11A_B0_STATIC 17/17
```

Windows Rust authority:

```text
cargo check --locked -p base_train --bin ash_bp_dk_fusion_legacy_migration_seed_authority_bootstrap_11a_b0
cargo test --locked -p base_train --lib seed_authority_bootstrap_11a_b0 -- --nocapture
cargo build --release --locked -p base_train --bin ash_bp_dk_fusion_legacy_migration_seed_authority_bootstrap_11a_b0
```

## Final SSOT

A missing historical seed is not reconstructed. A new 05-compatible candidate becomes migration authority only after explicit digest-bound operator approval and the existing canonical policy validator both accept it. The resulting seed is immutable, evidence-only, non-production and non-activation authority. Source checkpoint and managed production authority remain mutation-zero. Only this sealed seed is handed to 11A-R2 REPLAY_ONLY to start a new forward evidence lineage.
