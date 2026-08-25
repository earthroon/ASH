# ASH-BASETRAIN-NATIVE-CF1-BOUND-EXTERNAL-PHYSICAL-N2-REMATERIALIZATION-AND-PROMOTION-REBIND-R1

## 1. Purpose

This revision replaces the lost historical D-drive N2 parent with a newly executed physical N2 run under an explicit external physical storage root and rebinds Physical N2 promotion from the retired legacy CF1 compile receipt to `NativeCF1ReleaseCompileAuthority`.

It does not reconstruct the deleted N2 bytes, rewrite the historical promotion receipt, or synthesize Gen5 state.

Current execution flow:

```text
NativeCF1ReleaseCompileAuthority
  -> existing BaseTrain R6 production multistep execution
  -> new physical N2 run under external storage
  -> physical state and runtime receipt revalidation
  -> Native-CF1-bound promotion
  -> external-root-bound CURRENT_BASETRAIN_PARENT_POINTER
  -> N8
```

Production authority remains false.

## 2. Storage ownership

The repository drive is control-plane storage. Heavy runtime state is physical-data-plane storage.

```text
D:\...\ash_pass3
  source / specs / small receipts / control-runtime authorities

E:\ASH
  physical N2 run
  packed weight state
  Adam M/V state
  N2 promotion
  N8 output
  durable runtime payload
```

Current-path physical execution receives an explicit external root. There is no silent fallback to `workspace/base_train_runs` under the repository.

## 3. Existing R6 is the N2 materializer

No second N2 calculation engine is introduced. The canonical R6 production multistep loop remains the physical state producer.

A new BaseTrain option:

```text
--physical-n2-storage-root <ROOT>
```

activates fail-closed N2 rematerialization storage admission.

The admission requires:

```text
admitProductionMultistepLoop=true
admitN8LongHorizonContinuity=false
r6ParentR5RunDir=Some
resumeTrainingState=None
productionLoopOptimizerSteps=2
gradientAccumulation=8
basetrainStorageRoot == physicalN2StorageRoot
outputDir parent under physicalN2StorageRoot
```

On Windows, the external physical root must be on a different path prefix/drive from the running BaseTrain executable. This prevents a repository-drive heavy-payload fallback.

Successful admission emits:

```text
ASH_BASETRAIN_EXTERNAL_PHYSICAL_N2_STORAGE_ADMISSION_VALID=true
repoPhysicalPayloadCount=0
```

## 4. Source authority

Rematerialization starts from an explicit existing R5 physical parent. It must be the real generation-3 / optimizer-step-3 / cursor-next-3 R5 authority accepted by the existing R6 loader.

No latest-run fallback, zero-filled optimizer state, or reconstructed JSON state is admitted.

The deleted historical Gen5 N2 run is not a source dependency.

## 5. Native CF1 binding

Physical N2 execution uses the current BaseTrain admission input:

```text
--native-cf1-release-authority <PATH>
```

The retired compile receipt is not current authority.

Physical N2 promotion now accepts:

```text
--native-cf1-release-authority <PATH>
--physical-storage-root <ROOT>
```

The legacy promotion option remains parser-visible only for explicit retirement:

```text
--cf1-compile-receipt ...
-> E_LEGACY_CF1_COMPILE_RECEIPT_RETIRED
```

There is no fallback.

## 6. Promotion cross-binding

Promotion loads and validates `NativeCF1ReleaseCompileAuthority` through `ash_core` and independently reads the R6 runtime CF1 receipt from the physical N2 run.

Required equality:

```text
runtimeCF1.sourceTreeDigest
  == nativeCF1.compileInputManifestDigest

runtimeCF1.cargoLockDigest
  == nativeCF1.cargoLockDigest

runtimeCF1.authoritativeBinarySha256
  == nativeCF1.releaseBinarySha256

runtimeCF1.compileReceiptBinarySha256
  == nativeCF1.releaseBinarySha256
```

This replaces the old compile-receipt-v1/v2 parser and Python-validator pass-count dependency.

## 7. External physical root binding

Before promotion, the following existing artifacts are canonicalized and required to remain under the explicit physical storage root:

```text
physical N2 run root
training_state/active_training_state.json
training_state/<slot>/packed_state_manifest.json
weight pack
Adam M pack
Adam V pack
```

Promotion output parent must also be under the same external root.

Promotion does not copy or mutate weight/M/V payloads.

```text
promotionPayloadCopyCount=0
promotionPayloadMutationCount=0
repoPhysicalPayloadCount=0
allPhysicalPayloadUnderExternalRoot=true
```

## 8. Promotion schema

Current schema:

```text
ash.basetrain.physical_n2_promotion.v2
```

Current patch identity:

```text
ASH-BASETRAIN-NATIVE-CF1-BOUND-EXTERNAL-PHYSICAL-N2-REMATERIALIZATION-AND-PROMOTION-REBIND-R1
```

The receipt binds the existing physical-state digests plus:

```text
nativeCf1AuthorityFileSha256
nativeCf1AuthorityReceiptHash
nativeCf1CompileInputManifestDigest
physicalStorageRoot
allPhysicalPayloadUnderExternalRoot
repoPhysicalPayloadCount
promotionPayloadCopyCount
promotionPayloadMutationCount
```

`physicalSourceTreeDigest` must equal the native CF1 compile-input-manifest digest.

## 9. Promotion publication

Promotion remains metadata-only.

```text
physical N2 payload
  -> validate
  -> promotion receipt
  -> promoted parent manifest
  -> CURRENT_BASETRAIN_PARENT_POINTER
```

The pointer records:

```text
physicalStorageRoot
nativeCf1AuthorityReceiptHash
runRoot
activeTrainingStatePath
trainingGeneration
optimizerStep
cursorNextBatchOrdinal
stateKind
```

The physical payload is not recopied into the promotion directory.

The partial promotion directory is a sibling of the final promotion directory, so staging and final publication remain on the same external volume.

## 10. Promotion process exit semantics

A valid promotion is process success.

The historical HOLD token means only that N8 has not yet executed. It is printed after a valid receipt but no longer converted into an exit-1 `bail!`.

This allows the current Rust-native chain to execute:

```text
N2 materialization -> promotion -> N8
```

without treating a valid promotion as a command failure.

## 11. N8 parent admission

N8 reads the v2 promotion receipt and requires:

```text
allPhysicalPayloadUnderExternalRoot=true
repoPhysicalPayloadCount=0
promotionPayloadCopyCount=0
promotionPayloadMutationCount=0
```

It canonicalizes `physicalStorageRoot` and requires the promoted/resume run root to remain under it.

The pointer's:

```text
nativeCf1AuthorityReceiptHash
physicalStorageRoot
runRoot
```

must agree with the promotion receipt and actual resume root.

The existing weight/M/V and active-state digest checks remain authoritative.

## 12. Mandatory gates

```text
PASS_N2R1_EXISTING_R6_IS_SOLE_N2_MATERIALIZER
PASS_N2R1_EXPLICIT_EXTERNAL_PHYSICAL_ROOT
PASS_N2R1_R6_PARENT_IS_EXPLICIT_R5_AUTHORITY
PASS_N2R1_R6_GEN3_OPT3_CURSOR3_SOURCE_LAW_PRESERVED
PASS_N2R1_R6_GEN5_OPT5_CURSOR19_RESULT_LAW_PRESERVED
PASS_N2R1_PHYSICAL_N2_OUTPUT_UNDER_EXTERNAL_ROOT
PASS_N2R1_BASETRAIN_STORAGE_ROOT_EQUALS_PHYSICAL_ROOT
PASS_N2R1_EXTERNAL_DRIVE_DIFFERS_FROM_BINARY_DRIVE_ON_WINDOWS
PASS_N2R1_NATIVE_CF1_RELEASE_AUTHORITY_REQUIRED
PASS_N2R1_ZERO_LEGACY_CF1_PROMOTION_READ
PASS_N2R1_ZERO_LEGACY_CF1_FALLBACK
PASS_N2R1_RUNTIME_CF1_TO_NATIVE_CF1_SOURCE_IDENTITY_EXACT
PASS_N2R1_RUNTIME_CF1_TO_NATIVE_CF1_CARGO_LOCK_EXACT
PASS_N2R1_RUNTIME_CF1_TO_NATIVE_CF1_BINARY_EXACT
PASS_N2R1_ACTIVE_STATE_UNDER_EXTERNAL_ROOT
PASS_N2R1_PACKED_MANIFEST_UNDER_EXTERNAL_ROOT
PASS_N2R1_WEIGHT_PACK_UNDER_EXTERNAL_ROOT
PASS_N2R1_ADAM_M_PACK_UNDER_EXTERNAL_ROOT
PASS_N2R1_ADAM_V_PACK_UNDER_EXTERNAL_ROOT
PASS_N2R1_PROMOTION_OUTPUT_UNDER_EXTERNAL_ROOT
PASS_N2R1_ZERO_PROMOTION_PAYLOAD_COPY
PASS_N2R1_ZERO_PROMOTION_PAYLOAD_MUTATION
PASS_N2R1_PROMOTION_POINTER_EXTERNAL_ROOT_BOUND
PASS_N2R1_N8_PROMOTED_RUN_EXTERNAL_ROOT_BOUND
PASS_N2R1_N8_POINTER_NATIVE_CF1_BINDING
PASS_N2R1_VALID_PROMOTION_EXITS_ZERO
PASS_N2R1_PRODUCTION_AUTHORITY_FALSE
```

## 13. Non-goals

```text
No reconstruction of deleted historical N2 bytes
No rewrite of the old D-drive promotion receipt
No arbitrary latest-run substitution
No synthetic Gen5 state
No second N2 execution engine
No Python CF1 validator
No PowerShell authority producer
No physical payload copy into promotion metadata
No heavy repository-drive fallback
No production activation
```

## 14. Completion truth

Before this revision, Native CF1 admitted the current BaseTrain release binary, but the only promoted N8 parent referenced a deleted D-drive N2 run. Promotion still consumed a legacy CF1 compile receipt ABI.

After this revision, the existing R6 loop can rematerialize a new Gen5 physical N2 directly under an explicit external root such as `E:\ASH`. Promotion consumes the same Native CF1 release authority used by BaseTrain, revalidates the actual R6 runtime receipt and physical packed state, publishes metadata only under the external root, and gives N8 a parent pointer that cannot escape that physical storage root.

The deleted historical D-drive N2 is no longer part of the current execution graph.
