# ASH-BP-DK-FUSION-LEGACY-MIGRATION-EPHEMERAL-MUON-LINEAGE-ADMISSION-11A-R2

## Patch identity

```text
ASH-BP-DK-FUSION-LEGACY-MIGRATION-
EPHEMERAL-MUON-LINEAGE-ADMISSION-11A-R2
```

Build revision intent:

```text
bp-dk-fusion-legacy-migration-ephemeral-muon-lineage-admission-11a-r2
```

This revision supersedes the physical-admission semantics of 11A-R1 while preserving its explicit seed-policy, isolated capture, 11/12 evidence, and downstream 12/13/14/15A authority boundaries.

## Physical contradiction closed by R2

The generation-5 legacy source was physically inspected and has neither canonical TensorCube Local Muon momentum sidecar:

```text
tensorcube_local_muon_momentum.f32.bin                    absent
tensorcube_local_muon_momentum_manifest.json             absent
```

11A-R1 simultaneously required the TensorCube Local Muon production callsite and rejected `--admit-tensorcube-local-muon-new-lineage` under every circumstance. Existing Muon runtime semantics require the new-lineage admission when both durable momentum sidecars are absent. Therefore R1 was structurally valid but physically inadmissible for this source.

R2 fixes only the ownership of that new-lineage admission.

## Source Muon lineage classification

R2 reads the two canonical Muon sidecars only from the active committed source state directory returned by the existing checkpoint authority witness.

```text
momentum present + manifest present -> EXISTING
momentum absent  + manifest absent  -> LEGACY_ABSENT
exactly one present                 -> PARTIAL
```

`PARTIAL` is a hard failure:

```text
ASH_BP_DK_LEGACY_MIGRATION_PARTIAL_MUON_LINEAGE
```

R2 never repairs or synthesizes the missing half of a partial lineage.

## Admission authority

Generic `common-args-json` remains forbidden from carrying:

```text
--admit-tensorcube-local-muon-new-lineage
```

If present there, R2 fails with:

```text
ASH_BP_DK_LEGACY_MIGRATION_COMMON_ARGS_OWN_LINEAGE_AUTHORITY
```

The source-state classifier is the single admission authority.

### EXISTING

```text
captureMuonLineageMode       = RESUME_EXISTING
captureMuonLineageProvenance = SOURCE_RESUME
new-lineage admission        = false
```

### LEGACY_ABSENT

```text
captureMuonLineageMode       = INITIALIZE_EPHEMERAL_NEW_LINEAGE
captureMuonLineageProvenance = LEGACY_MIGRATION_11A_GENESIS
new-lineage admission        = true
```

In the `LEGACY_ABSENT` case the 11A orchestrator clones the operator common-argument list and appends `--admit-tensorcube-local-muon-new-lineage` exactly to the effective isolated capture arguments. It does not mutate the operator common-args file.

## Effective argument binding

The R1 `commonArgsDigest` remains the digest of the operator-provided argument list for compatibility and audit.

R2 additionally records:

```text
effectiveCaptureArgsDigest
```

The existing canary schedule now binds the effective argument digest, because those are the actual arguments executed by the branch runner.

The existing `execute_training_branch_with_env()` path is reused unchanged. R2 does not add another process launcher and does not modify the canary runner itself.

## Meaning of ephemeral

`EPHEMERAL` does not mean memory-only.

It means the newly created Muon lineage is scoped to the isolated 11A migration evidence branch and has no production authority. The branch may durably write canonical Muon momentum and manifest sidecars inside its own training state.

The immutable legacy source checkpoint must remain unchanged.

## Capture durability proof

For a completed capture the final committed capture state must contain both canonical Muon sidecars. Otherwise R2 fails with:

```text
ASH_BP_DK_LEGACY_MIGRATION_CAPTURE_MUON_LINEAGE_NOT_DURABLE
```

For a `LEGACY_ABSENT` source, a completed capture must prove:

```text
captureMuonLineageInitialized       = true
captureMuonMomentumCreatedCount     = 1
captureMuonManifestCreatedCount     = 1
```

For an `EXISTING` source, those genesis counters remain zero.

## Source read-only witness

R2 reclassifies and re-digests the source Muon sidecars after the branch completes.

The receipt adds:

```text
sourceMuonLineageClass
sourceMuonMomentumPresent
sourceMuonManifestPresent
sourceMuonMomentumDigest
sourceMuonManifestDigest
sourceMuonMutationCount
productionMuonAuthorityMutationCount
```

The pre-managed source checkpoint is the only source-side Muon production-lineage witness available to this migration step, so the production Muon mutation counter is sealed from the same source-sidecar mutation witness.

Both counters must remain zero.

Hard failures include:

```text
ASH_BP_DK_LEGACY_MIGRATION_SOURCE_MUON_LINEAGE_MUTATED
ASH_BP_DK_LEGACY_MIGRATION_PRODUCTION_MUON_AUTHORITY_MUTATED
```

## Receipt schema

Seed authority remains:

```text
ash.bp_dk.fusion_legacy_migration.seed_policy_authority.r1
```

Capture receipt advances to:

```text
ash.bp_dk.fusion_legacy_migration.evidence_capture.r2
```

New capture fields include:

```text
effectiveCaptureArgsDigest
sourceMuonLineageClass
captureMuonLineageMode
captureMuonLineageProvenance
captureMuonNewLineageAdmission
sourceMuonMomentumPresent
sourceMuonManifestPresent
sourceMuonMomentumDigest
sourceMuonManifestDigest
captureMuonMomentumPresent
captureMuonManifestPresent
captureMuonLineageInitialized
captureMuonMomentumCreatedCount
captureMuonManifestCreatedCount
sourceMuonMutationCount
productionMuonAuthorityMutationCount
```

## Evidence and promotion semantics preserved

R2 does not change:

```text
explicit operator-approved 05-compatible seed policy
seed policy canonical validation and digest
legacy restart barrier admission
legacy source read-only checkpoint witness
managed active pointer absence gate
managed authority mutation-zero gate
REPLAY_ONLY profile
PROMOTION_READY_OBSERVED profile
08A physical qualification validation
09 RECORD_OBSERVED evidence
10 objective OBSERVE evidence
11 trajectory head
12 replay head
12 build_policy_calibration_recommendation() evidence sufficiency
12 recommendation ownership
13 operator review ownership
14 bounded qualification ownership
15A first managed authority bootstrap ownership
```

No AdamW-only fallback is introduced. R2 preserves the Muon/HiMuon production topology that the later evidence is intended to qualify.

## Current approved seed remains unchanged

The operator-approved migration seed remains the existing R1 seed artifact and is not regenerated by this patch.

R2 contains no hard-coded seed threshold values and does not auto-promote the 08A test fixture into migration authority.

## Implementation surface

The R2 overlay changes exactly four files relative to the already-applied 11A-R1 overlay:

```text
crates/base_train/src/bp_delta_k_fusion_legacy_migration_seed_policy_evidence_capture.rs
crates/base_train/src/bin/ash_bp_dk_fusion_legacy_migration_seed_policy_evidence_capture_11a.rs
tools/validate_ash_bp_dk_fusion_legacy_migration_ephemeral_muon_lineage_admission_11a_r2_static.py
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

No scheduler, activation, canary runner, `lib.rs`, or `Cargo.toml` change is required in R2. The R1 module/binary registration remains authoritative.

No generated artifacts, manifests, `*.sha256`, or Python cache files are included in the overlay.

## Static validation

R2-specific static validation observed on the R1 overlay tree:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EPHEMERAL_MUON_LINEAGE_ADMISSION_11A_R2_STATIC 116/116
```

The bake environment has no Rust toolchain. Windows Release CF1 remains the compilation, type, borrow, and full cumulative-validator authority before physical execution.

## CF1 order

The R1 validator entry is superseded by the R2 validator while preserving functional order:

```text
11 trajectory
-> 11A-R2 legacy migration capture
-> 12 recommendation
-> 13 review
-> 14 canary
-> 15 activation
-> 15A/15B/15C
-> 16 ... 21
```

## First physical target

Use the generation-5 legacy source and the already approved seed policy.

The first target is a fresh isolated two-generation `REPLAY_ONLY` smoke.

Expected R2 truth for the current source:

```text
sourceMuonLineageClass       = LEGACY_ABSENT
captureMuonLineageMode       = INITIALIZE_EPHEMERAL_NEW_LINEAGE
captureMuonLineageProvenance = LEGACY_MIGRATION_11A_GENESIS
captureMuonNewLineageAdmission = 1
```

A valid completed smoke additionally requires:

```text
child process exit = 0
sourceCheckpointMutationCount = 0
sourceMuonMutationCount = 0
managedAuthorityMutationCount = 0
productionMuonAuthorityMutationCount = 0
captureMuonMomentumPresent = true
captureMuonManifestPresent = true
captureMuonLineageInitialized = true
trajectory head exists
replay head exists
```

`promotionReady=false` is expected for the two-generation REPLAY_ONLY smoke and is not a failure.

## Promotion tokens

Structural validator:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EPHEMERAL_MUON_LINEAGE_ADMISSION_11A_R2_STATIC
```

Physical lineage success is surfaced by the 11A CLI as R2 lineage fields. Promotion-ready observed capture additionally emits:

```text
PASS_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EPHEMERAL_MUON_LINEAGE_PHYSICAL_11A_R2
PROMOTE_ASH_BP_DK_FUSION_LEGACY_MIGRATION_EPHEMERAL_MUON_LINEAGE_ADMISSION_11A_R2
```

## Final SSOT

```text
A pre-BP-DK legacy checkpoint with no canonical Muon momentum sidecars has no resumable historical Muon lineage.

11A-R2 does not fabricate one and does not silently fall back to a different optimizer topology.

The active source slot is classified from the canonical momentum/manifest pair. A complete existing pair resumes. A completely absent pair authorizes the 11A orchestrator, and only the 11A orchestrator, to add the existing new-lineage admission to the isolated capture branch. A partial pair fails closed.

The new Muon lineage begins forward from the immutable legacy source and is durable only inside the migration evidence branch until later policy review and qualification explicitly promote a downstream state.

Generic common arguments never own lineage creation. The executed effective arguments are separately digested and sealed.

The legacy source, managed production policy authority, and source-side Muon authority remain mutation-zero.

R2 changes lineage admission ownership only. Seed-policy meaning, BP-DeltaK evidence mathematics, recommendation, review, qualification, and first managed-authority bootstrap responsibilities remain unchanged.
```