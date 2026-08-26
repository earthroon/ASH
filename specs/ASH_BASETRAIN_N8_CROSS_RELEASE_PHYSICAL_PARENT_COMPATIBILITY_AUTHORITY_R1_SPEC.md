# ASH-BASETRAIN-N8-CROSS-RELEASE-PHYSICAL-PARENT-COMPATIBILITY-AUTHORITY-R1

## Status

Implementation bake for explicit compatibility admission when an immutable physical N2 parent was produced by one Native CF1 release and is consumed by a different current Native CF1 release.

```text
Exact Physical N2 Parent /
Producer Native CF1 Authority /
Current Consumer Native CF1 Authority /
No Parent State Rewrite /
No N2 Replay By Default /
Exact Model Spec Identity /
Exact Tokenizer Identity /
Exact Dataset Identity /
Packed State ABI Compatibility /
Training State ABI Compatibility /
Optimizer State ABI Compatibility /
Weight Pack Digest Preserved /
Adam M Digest Preserved /
Adam V Digest Preserved /
No Kernel-Math Compatibility Assumption /
No SourceTree-Equality Fiction /
Producer Release Identity /
Consumer Release Identity /
Explicit Cross-Release Admission /
Production Authority False Until Compatibility PASS /
```

## 1. Problem

The current external physical N2 parent is an immutable generation-5 / optimizer-step-5 / cursor-next-19 packed state. Its v2 promotion receipt records the Native CF1 release that produced and promoted it.

At R1 design time the observed producer and consumer release receipt hashes were:

```text
producer = 4d57564521f1404a6b41ced57335fe67f9c6cb19ede86a465e53b84f88b471ea
pre-R1 consumer observation = 9169c958b8da2909fa38e7277b8ebd1b653b4b4c5e3874709f6f3561b1cafe0d
```

R1 itself changes BaseTrain compile inputs. Therefore `9169c9...` becomes pre-R1 history after the bake is applied. Physical execution MUST mint a fresh post-R1 Native CF1 release authority and bind that newly observed receipt as the consumer. The R1 implementation does not hard-code either release hash.

## 2. Authority ownership

```text
Physical N2 bytes
  owned by physical N2 run root

Physical N2 promotion v2
  owns producer provenance and immutable physical payload digests

Producer Native CF1
  owns the release identity that produced N2

Consumer Native CF1
  owns the current BaseTrain executable identity

Cross-Release Compatibility R1
  owns only producer-state -> consumer-loader compatibility
```

R1 does not become training production authority or activation authority.

## 3. Same-release and cross-release behavior

Normal same-release N8 remains unchanged:

```text
promotion.nativeCf1AuthorityReceiptHash
== current NativeCF1ReleaseCompileAuthority.receiptHash
-> existing N8 path
```

A cross-release parent requires explicit R1 authority:

```text
producer receipt hash != consumer receipt hash
AND R1 authority absent
-> ASH_N8_CROSS_RELEASE_COMPATIBILITY_AUTHORITY_REQUIRED

producer receipt hash != consumer receipt hash
AND exact R1 authority valid
-> N8 parent admission may continue
```

Supplying a cross-release authority on a same-release parent is rejected. R1 is also forbidden on legacy-migration-descendant and N8 resume-cut paths in this revision.

## 4. No release identity fiction

A valid R1 authority explicitly records:

```text
producerConsumerReleaseIdentityEqual = false
sourceTreeEqualityRequired = false
sourceTreeEqualityClaimed = false
kernelMathCompatibilityAssumed = false
kernelMathParityClaimed = false
```

State-consumption compatibility does not imply source-tree equality, binary equality, optimizer arithmetic parity, WGSL parity, or GPU intermediate parity.

## 5. Producer Native CF1 proof

R1 loads the exact producer `NativeCF1ReleaseCompileAuthority` and validates its canonical receipt hash.

Required cross-binding:

```text
producer.receiptHash
== promotion.nativeCf1AuthorityReceiptHash

SHA256(producer authority file)
== promotion.nativeCf1AuthorityFileSha256

producer.compileInputManifestDigest
== promotion.nativeCf1CompileInputManifestDigest
== promotion.physicalSourceTreeDigest
```

The producer binary need not still be the current executable. Its immutable authority receipt is historical provenance.

## 6. Consumer Native CF1 proof

R1 loads the exact current consumer `NativeCF1ReleaseCompileAuthority` and fresh-hashes the supplied `base_train.exe`.

Required:

```text
fresh SHA256(base_train.exe)
== consumer.releaseBinarySha256
```

The same exact consumer authority receipt is revalidated again at BaseTrain runtime before N8 parent admission.

After R1 source application the consumer CF1 MUST be freshly re-materialized. Reusing pre-R1 `9169c9...` is forbidden because R1 changed compile inputs.

## 7. Physical parent proof

R1 consumes only promotion schema:

```text
ash.basetrain.physical_n2_promotion.v2
```

Required promotion state:

```text
publicationState = COMMITTED
physicalStateVerified = 1
promotionCommitCount = 1
promotedTrainingGeneration = 5
promotedOptimizerStep = 5
promotedCursorNextBatchOrdinal = 19
allPhysicalPayloadUnderExternalRoot = true
repoPhysicalPayloadCount = 0
promotionPayloadCopyCount = 0
promotionPayloadMutationCount = 0
```

The exact promoted run root is canonicalized and must remain under `physicalStorageRoot`.

The pointer and promotion receipt must agree on:

```text
runRoot
nativeCf1AuthorityReceiptHash
stateKind = R6_PACKED_TRAINING_STATE
```

## 8. Training-state ABI witness

The current consumer validates the parent active state using the current training-state ABI, not a compatibility-only parser.

Required:

```text
schema = ash.basetrain.training_state.v3
trainingGeneration = 5
optimizerStep = 5
gradientAccumulation = 8
accumulatedMicrobatchCount = 8
trainingStateDigest = freshly recomputed canonical logical digest
```

Dataset cursor:

```text
trainingGeneration = 5
optimizerStep = 5
nextBatchOrdinal = 19
cursorDigest = freshly recomputed canonical cursor digest
```

The active state physical SHA256 must exactly equal the promotion receipt's `physicalN2ActiveStateSha256`.

## 9. Exact dataset identity

Dataset identity is byte-exact because the training-state cursor already persists the historical physical manifest SHA256.

Required:

```text
active.datasetCursor.datasetManifestId
== current DatasetManifest.datasetManifestId

active.datasetCursor.datasetManifestSha256
== fresh SHA256(current dataset manifest file)
```

Thus the current dataset manifest bytes are exactly the dataset artifact bound by the physical parent.

The current dataset-builder identity is recomputed from the same SSOT formula used by production BaseTrain and must match the cursor's historical `datasetBuilderIdentity`.

## 10. Tokenizer identity and evidence boundary

The physical parent persists the exact tokenizer lineage identifier:

```text
active.datasetCursor.tokenizerLineageId
== current TokenizerManifest.manifestId
```

The byte-exact dataset manifest also persists:

```text
dataset.lineage.tokenizerSpecId
== current TokenizerManifest.tokenizerSpecId
```

The current tokenizer manifest must additionally pass its own canonical `hashes.manifestHash` self-validation.

R1 therefore admits exact tokenizer lineage identity for state consumption.

R1 DOES NOT claim that the historical producer persisted the raw tokenizer JSON file SHA256. The receipt explicitly records:

```text
tokenizerHistoricalContentDigestClaimed = false
```

This distinction is mandatory and prevents an unobserved raw-file parity claim.

## 11. Model state identity and evidence boundary

The byte-exact producer-bound dataset manifest persists:

```text
dataset.lineage.modelSpecId
```

R1 requires:

```text
dataset.lineage.modelSpecId
== current ModelSpec.modelSpecId
```

R1 then presents the physical packed parameter registry to the current production atlas planner using the current `ModelSpec`. Compatibility requires:

```text
resolvedTensorCount = 201
missingTensorCount = 0
modelPlan.modelSpecId = current ModelSpec.modelSpecId
```

This is an explicit exact state-topology proof. Parameter names, logical shapes, offsets, and packed spans must be consumable by the current model planner.

R1 does not claim historical raw model TOML file equality because that raw producer digest is not carried by the N2 state/promotion chain:

```text
producerModelRawFileDigestClaimed = false
```

Kernel-math-only model configuration parity is not inferred from state topology.

## 12. Packed-state ABI witness

The current typed `PackedRuntimeStateManifestV1` parser and validator are authoritative.

Required:

```text
schema = ash.basetrain.packed_runtime_state.r6a.v1
publicationState = VALIDATED_READY_FOR_CANONICAL_POINTER
trainingGeneration = 5
optimizerStep = 5
parameterCount = 201
dtype = F32
endianness = LITTLE
compression = NONE
```

The current geometry validator must prove:

```text
parameter index continuity
parameter logical shape element count
byte offset continuity
byte length = logical element count * 4
segment geometry
final packed byte span
parameter offset registry digest
packed manifest logical digest
```

The active state aliases for manifest, parameter-set, optimizer-state, and registry digests must exactly match the physical manifest.

## 13. Optimizer-state ABI witness

Adam M/V share the same packed parameter offset registry and logical F32 geometry as weights.

R1 requires:

```text
weightPackBytes == adamMPackBytes == adamVPackBytes
parameterCount = 201
Adam M element type = F32
Adam V element type = F32
shape mismatch count = 0
offset mismatch count = 0
optimizer state semantic mismatch count = 0
```

This proves optimizer-state storage ABI compatibility only. It does not claim producer/consumer AdamW or Muon arithmetic parity.

## 14. Fresh physical payload rehash

Promotion digests are not trusted without fresh observation.

R1 fresh-hashes:

```text
active_training_state.json
packed_state_manifest.json
weight pack
Adam M pack
Adam V pack
```

Required physical payload digests are read from the promotion receipt, never hard-coded.

The observed current parent at design time had:

```text
active state  b1c236c113ca3994796f56f2a05f730557b42bfaa81d278069c1688eb9c58115
manifest      d9872144177d442a17a5b5c36aff8f886d9addee324faeb5be796478e815dc82
weight        13f340c75840f1417f5663c95fc321a89ecd2a56b455b8b288608ea1f9ac6182
Adam M        7e3ae9a74297bacbc47db9b3e68751e12d58ac1351ea9534fb09178e0586242e
Adam V        4a06f712f3a3566ce8ae16713775ef699fe2f627cd8140043ee2e3b54067120d
```

These values are observation notes only. Runtime truth is always read from the selected promotion receipt and freshly rehashed.

## 15. Mutation-zero proof

R1 is read-only with respect to the physical parent.

The active state, packed manifest, weight pack, Adam M pack, and Adam V pack are hashed before compatibility evaluation and again after model-plan validation.

Required:

```text
parentStateMutationCount = 0
packedManifestMutationCount = 0
weightMutationCount = 0
adamMMutationCount = 0
adamVMutationCount = 0
```

The model topology plan is materialized only under the new R1 authority staging directory, never inside the parent run.

## 16. No replay / no migration / no repair

R1 never invokes training, forward, backward, optimizer execution, or N2 rematerialization.

Required receipt counters:

```text
parentStateRewriteCount = 0
stateMigrationCount = 0
compatibilityRepairCount = 0
trainingReplayCount = 0
optimizerReplayCount = 0
gradientReplayCount = 0
```

If compatibility is not provable, R1 fails. It does not repair the state or silently replay N2.

## 17. Authority schema

```text
ash.basetrain.n8.cross_release_physical_parent_compatibility.r1
```

Authority filename:

```text
n8_cross_release_physical_parent_compatibility_authority.json
```

Source role:

```text
CROSS_RELEASE_PHYSICAL_N2_PARENT
```

## 18. Sealer CLI

Binary:

```text
ash_basetrain_n8_cross_release_physical_parent_compatibility_authority_r1
```

Inputs:

```text
--n8-physical-n2-promotion-dir
--producer-native-cf1-release-authority
--consumer-native-cf1-release-authority
--consumer-base-train-binary
--model-spec-path
--tokenizer-manifest-path
--dataset-manifest-path
--output-root
```

The output root is created atomically through a sibling `.partial` directory.

## 19. BaseTrain admission CLI

New current-runtime input:

```text
--n8-cross-release-parent-compatibility-authority <AUTHORITY_JSON>
```

The option is legal only under N8 production-loop admission.

R1 forbids combination with:

```text
--legacy-migration-descendant-source-authority
N8 RAM resume-cut roles
```

## 20. Runtime cross-binding

At N8 runtime the current `base_train.exe`:

1. loads and validates the current Native CF1 authority;
2. fresh-hashes itself and verifies exact release binary identity;
3. validates the N2 promotion and physical parent;
4. obtains the parent producer CF1 receipt hash;
5. compares producer and current consumer receipt hashes;
6. requires R1 only on mismatch;
7. revalidates R1 consumer authority, producer authority, input identities, and physical parent digests;
8. emits the explicit admission PASS token before training proceeds.

## 21. N8 parent binding extension

`N8ParentBinding` now carries:

```text
producerNativeCf1AuthorityReceiptHash
```

For normal promoted parents this field comes directly from the v2 promotion receipt.

Legacy migration descendant binding does not use R1 and does not fabricate a producer CF1 identity.

## 22. Compatibility receipt semantic booleans

R1 deliberately does not collapse all evidence into one `compatible` boolean. The receipt contains independent typed witnesses:

```text
trainingStateAbi
packedStateAbi
optimizerStateAbi
inputIdentity
physicalPayload
```

Top-level admission booleans are valid only after every detailed witness has passed.

## 23. Production authority separation

A valid R1 receipt contains:

```text
crossReleaseParentAdmissionAuthority = true
n8ParentCompatibilityAdmitted = true
productionAuthority = false
activationAuthority = false
```

PASS means only that the immutable parent may be consumed by the exact current BaseTrain release. It does not prove the subsequent N8 execution or checkpoint production result.

## 24. Failure taxonomy

Representative failures:

```text
ASH_N8_CROSS_RELEASE_COMPATIBILITY_AUTHORITY_REQUIRED
ASH_N8_CROSS_RELEASE_PRODUCER_CF1_AUTHORITY_INVALID
ASH_N8_CROSS_RELEASE_CONSUMER_CF1_AUTHORITY_INVALID
ASH_N8_CROSS_RELEASE_CONSUMER_BINARY_IDENTITY_MISMATCH
ASH_N8_CROSS_RELEASE_PRODUCER_CF1_RECEIPT_MISMATCH
ASH_N8_CROSS_RELEASE_PRODUCER_CF1_FILE_MISMATCH
ASH_N8_CROSS_RELEASE_PRODUCER_COMPILE_INPUT_MISMATCH
ASH_N8_CROSS_RELEASE_PHYSICAL_PARENT_IDENTITY_MISMATCH
ASH_N8_CROSS_RELEASE_DATASET_MANIFEST_ID_MISMATCH
ASH_N8_CROSS_RELEASE_DATASET_MANIFEST_DIGEST_MISMATCH
ASH_N8_CROSS_RELEASE_TOKENIZER_LINEAGE_MISMATCH
ASH_N8_CROSS_RELEASE_MODEL_SPEC_LINEAGE_MISMATCH
ASH_N8_CROSS_RELEASE_TOKENIZER_SPEC_LINEAGE_MISMATCH
ASH_N8_CROSS_RELEASE_DATASET_BUILDER_IDENTITY_MISMATCH
ASH_N8_CROSS_RELEASE_TRAINING_STATE_ABI_MISMATCH
ASH_N8_CROSS_RELEASE_PACKED_STATE_ABI_MISMATCH
ASH_N8_CROSS_RELEASE_MODEL_TOPOLOGY_MISMATCH
ASH_N8_CROSS_RELEASE_WEIGHT_DIGEST_MISMATCH
ASH_N8_CROSS_RELEASE_ADAM_M_DIGEST_MISMATCH
ASH_N8_CROSS_RELEASE_ADAM_V_DIGEST_MISMATCH
ASH_N8_CROSS_RELEASE_PARENT_MUTATION_DETECTED
ASH_N8_CROSS_RELEASE_COMPATIBILITY_REPAIR_FORBIDDEN
ASH_N8_CROSS_RELEASE_N2_REPLAY_FORBIDDEN
```

## 25. Unit regression surface

Focused Rust tests:

```text
cross_release_authority_accepts_explicit_abi_compatibility_without_release_identity_fiction
cross_release_authority_rejects_kernel_math_parity_or_state_repair_claims
```

BaseTrain static validation additionally proves:

```text
same-release existing path preserved
cross-release authority required on producer/consumer mismatch
cross-release authority forbidden for legacy descendant
cross-release authority forbidden for resume-cut R1
current consumer binary fresh binding retained
no producer CF1 rewrite
no promotion pointer rewrite
no N2 replay path introduced
```

## 26. PASS tokens

Authority sealer:

```text
PASS_ASH_BASETRAIN_N8_CROSS_RELEASE_PHYSICAL_PARENT_COMPATIBILITY_AUTHORITY_R1
```

BaseTrain runtime admission:

```text
PASS_ASH_BASETRAIN_N8_CROSS_RELEASE_PHYSICAL_PARENT_ADMISSION_R1
```

## 27. Physical execution order

Because R1 changes BaseTrain compile inputs, physical execution MUST follow this order:

```text
apply R1 source
-> static validation
-> cargo check/tests
-> build R1 compatibility sealer binary
-> ensure control-runtime materializer binary exists
-> mint fresh post-R1 Native CF1 authority (this performs final canonical base_train Release build)
-> DO NOT rebuild base_train.exe afterward
-> select exact v2 physical N2 promotion directory
-> seal R1 compatibility authority using producer 4d5756... and fresh post-R1 consumer authority
-> run BaseTrain N8 with both the selected promotion and R1 authority
```

The pre-R1 `9169c9...` consumer authority is not valid for the final post-R1 BaseTrain binary.

## 28. Non-goals

```text
No source-tree equality claim
No kernel-math parity claim
No producer raw model TOML digest claim
No producer raw tokenizer JSON digest claim
No N2 replay
No parent state rewrite
No optimizer-state migration
No compatibility repair
No legacy-descendant ancestry recovery
No production activation
```

## 29. Final SSOT

```text
Producer Native CF1
        ↓ exact promotion provenance
Immutable physical N2 GEN5 / OPT5 / CURSOR19
        ↓ fresh state + payload rehash
Training / Packed / Optimizer ABI witnesses
        ↓
Exact dataset bytes
Exact tokenizer lineage identity
Exact model state topology identity
        ↓
Fresh post-R1 Consumer Native CF1
        ↓ exact current binary identity
Explicit Cross-Release Compatibility Authority
        ↓
N8 parent admission
```

R1 proves that a specific immutable physical state is consumable by one specific current BaseTrain release. It does not pretend that the producer and consumer releases were the same program and does not infer unobserved historical raw-file or kernel-math parity.
