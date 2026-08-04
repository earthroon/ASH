NEG-K-USING-Q-WIDTH
NEG-QK-COMMON-DISPATCH-COUNT
NEG-V-ROTATED

NEG-KNOWN-NEOX-EXPECTED-INTERLEAVED
NEG-KNOWN-COUNTERFACTUAL-NONDISCRIMINATING
NEG-KNOWN-POSITION-ZERO-NONIDENTITY

NEG-PRODUCTION-ADMISSION
NEG-PROOF-LEDGER-PROMOTION
NEG-R6-ADMISSION
```

A negative control passes only when the mutated candidate is rejected for the intended reason.

Unexpected acceptance fails the physical gate.

---

# 20. Failure taxonomy

Suggested hard failures:

```text
AW02R5R5ParentR5R4ManifestMissing
AW02R5R5ParentR5R4DigestMismatch
AW02R5R5ParentR5R4PassTokenMismatch

AW02R5R5CheckpointConfigMissing
AW02R5R5CheckpointConfigDigestMismatch
AW02R5R5CheckpointConfigParseFailed
AW02R5R5CheckpointRopeThetaMissing
AW02R5R5CheckpointRopeThetaInvalid
AW02R5R5CheckpointRopeThetaAliasConflict
AW02R5R5CheckpointModelFamilyMissing
AW02R5R5CheckpointRopeScalingUnsupported

AW02R5R5ConventionRegistryMissing
AW02R5R5ConventionRegistryDigestMismatch
AW02R5R5ConventionRegistryNoMatch
AW02R5R5ConventionRegistryAmbiguous
AW02R5R5ConventionRecordDigestMismatch
AW02R5R5ExternalSourceEvidenceMismatch
AW02R5R5ExternalSourceRevisionUnpinned

AW02R5R5PairingLayoutMissing
AW02R5R5PairingLayoutUnknown
AW02R5R5PairMapInvalid
AW02R5R5PairMapDigestMismatch
AW02R5R5FrequencyFormulaMismatch
AW02R5R5SignConventionMismatch

AW02R5R5RopeAuthorityLineageMismatch
AW02R5R5ModelSpecRopeMismatch
AW02R5R5GeometryRopeMismatch
AW02R5R5SequenceRopeMismatch
AW02R5R5BackendRopeParamsMismatch
AW02R5R5PipelineSelectionMismatch

AW02R5R5KnownVectorCpuNeoXMismatch
AW02R5R5KnownVectorCpuInterleavedMismatch
AW02R5R5KnownVectorGpuNeoXMismatch
AW02R5R5KnownVectorGpuInterleavedMismatch
AW02R5R5KnownVectorCounterfactualUnexpectedPass
AW02R5R5ThetaMutationUnexpectedPass

AW02R5R5QueryRopeParityMismatch
AW02R5R5KeyRopeParityMismatch
AW02R5R5ContextParityMismatch
AW02R5R5QueryHeadDomainMismatch
AW02R5R5KeyHeadDomainMismatch
AW02R5R5PaddingNonZero
AW02R5R5LiveHandoffConventionMismatch

AW02R5R5ProductionAdmissionForbidden
AW02R5R5ProofLedgerPromotionForbidden
AW02R5R5R6AdmissionForbidden
```

---

# 21. Tolerance contract

## 21.1 Known-vector CPU-f64

The sealed decimal known vector is compared in f64.

```text
absolute tolerance 1e-12
relative tolerance 1e-12
NaN count          0
Inf count          0
```

## 21.2 GPU f32 versus CPU-f64

Initial fixture tolerance:

```text
absolute tolerance 2e-5
relative tolerance 2e-5
NaN count          0
Inf count          0
```

The gate records maximum absolute and relative errors per stage.

Tolerance must not be widened automatically after a failure.

## 21.3 Position-zero identity

Position zero is exact except signed-zero normalization policy.

Required:

```text
output bits == input bits
```

If the implementation canonicalizes `-0.0` to `+0.0`, that policy must be explicit and separately tested.

---

# 22. Live handoff contract

`BaseTrainAtlasWave02R5LiveHandoff` gains or binds:

```text
rope convention digest
pairing layout ID
pair map digest
frequency formula ID
rotary dimension
Q RoPE byte length
K RoPE byte length
```

Required invariants:

```text
Q RoPE byte length == batch × seq × Q width × 4
K RoPE byte length == batch × seq × KV width × 4
Q convention digest == K convention digest
Q pairing layout == K pairing layout
Q rotary dimension == K rotary dimension
```

The handoff does not become a new writer of the convention. It carries the authority digest.

---

# 23. Production admission boundary

R5-R5 remains a synthetic physical closure.

It proves:

```text
pinned external config parsing
versioned convention resolution
checkpoint theta consumption
NeoX half-split physical execution
interleaved convention separation
unequal Q/K head-domain rotation
known-vector discrimination
CPU-f64 external-convention parity
```

It does not prove:

```text
full TinyLlama checkpoint tensor loading
all 22 transformer layers
BF16 production numerical parity
production tokenizer-to-loss path
backward pass
optimizer update
checkpoint writeback
long-context scaling
KV cache decode parity
production throughput
production memory residency
```

Required final states:

```text
productionAdmission       BLOCKED
proofLedgerAdmission      HOLD
R6Admission               BLOCKED
```

No receipt may use `productionReady=true`.

---

# 24. CLI contract

Suggested args file:

```text
specs/cli/ash_basetrain_atlas_wave_02_r5_r5.args
```

Required arguments:

```text
--repo-root
--parent-r5-r4-manifest
--parent-r5-r4-manifest-sha256
--checkpoint-config-snapshot
--checkpoint-config-sha256
--rope-convention-registry
--rope-convention-registry-sha256
--external-source-evidence
--external-source-evidence-sha256
--known-vector-fixture
--known-vector-fixture-sha256
--runtime-output-dir
--expected-adapter-subgroup-size=32
--absolute-tolerance=0.00002
--relative-tolerance=0.00002
--production-admission=deny
--proof-ledger-admission=hold
--r6-admission=blocked
```

Forbidden CLI authority:

```text
--rope-theta=10000
--pairing-layout=neox
--rotary-dim=4
```

These values must come from external evidence and the registry, not operator choice.

Diagnostic override flags may exist only in a negative-control binary that cannot emit the production-form PASS token.

---

# 25. Code-change map

Expected implementation surface:

```text
crates/model_core/src/spec.rs
  extend RopeSection with explicit optional convention fields

crates/model_core/src/base_train_atlas_wave_sequence_authority.rs
  seal pairing, pair-map, formula, sign and external convention digests

crates/base_train/src/base_train_atlas_wave_02_r5_r3_geometry_authority.rs
  bind external convention into geometry digest
  add R5-R5 synthetic external convention fixture constructor

crates/base_train/src/base_train_atlas_wave_02_r5_cpu_reference.rs
  add explicit NeoX and interleaved CPU-f64 reference paths
  remove implicit adjacent-only authority

crates/base_train/src/base_train_atlas_wave_02_r5_live_handoff.rs
  carry convention identity and Q/K RoPE byte cardinality

