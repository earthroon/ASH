# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C3

## Wave Domain Authority Split / Artifact Receipt Wave Naming Isolation / Embedding Row Micro-Atlas Wave Naming Isolation / Decoder Weight Atlas Wave Reserved Authority / Receipt Wave·Payload Wave Semantic Separation / No Cross-Domain PASS Borrowing / No Ambiguous Wave SSOT Seal

> Parent physical SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C2` physical PASS  
> Parent execution route: BaseTrain FullPrefill / Layer-2 single-step canary  
> Parent runtime evidence: typed child evidence + per-step completion digest  
> Scope: wave-domain naming, ownership, receipt semantics, PASS/admission isolation  
> Runtime decoder math: unchanged  
> Checkpoint loader algorithm: unchanged  
> Weight residency state machine: unchanged  
> Hidden authority state machine: unchanged  
> New decoder-weight streaming implementation: **NOT introduced in C3**  
> Full N-layer execution: `BLOCKED`  
> Final RMSNorm / LM head: `BLOCKED`  
> Forward loss / backward / optimizer / production inference: `BLOCKED`  
> Proof ledger: `HOLD` until C3 physical/static closure

---

# 0. Why C3 exists

R6-R9 C2 physically proves Layer 2 execution and promotes real child evidence into coordinator truth.

However the current codebase uses the word `wave` for at least three semantically different domains:

```text
1. Artifact receipt construction wave
   - parallel lane JSON fragment construction
   - deterministic streaming merge
   - no model payload movement

2. Embedding row micro-atlas payload wave
   - checkpoint-backed token embedding rows
   - bounded row tile payload
   - parallel row decode/read
   - sequential upload/dispatch/reuse

3. Decoder weight atlas wave
   - future layer-weight payload streaming domain
   - currently NOT implemented
   - currently NOT admitted
```

If these domains remain aliased under a generic `wave` name, a PASS in one domain can be misread as proof for another domain.

C3 therefore creates an explicit **wave-domain authority split** before any decoder-weight wave transport is implemented.

---

# 1. C3 primary seal

After C3, the unqualified word:

```text
wave
```

must never be sufficient to identify a runtime authority, artifact authority, payload authority, PASS state, or receipt field.

Every wave-bearing type, function, receipt field, terminal token, manifest field, and PASS token must bind one of the following explicit domains:

```text
ArtifactReceiptWave
EmbeddingRowMicroAtlasWave
DecoderWeightAtlasWave
```

The first two are existing domains.

The third is a **reserved authority name only** in C3.

---

# 2. Canonical wave-domain registry

Introduce a canonical enum or equivalent sealed registry owned by the R6-R9/C3 evidence layer.

Recommended Rust surface:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum BaseTrainWaveDomain {
    ArtifactReceipt,
    EmbeddingRowMicroAtlas,
    DecoderWeightAtlas,
}
```

Canonical string IDs:

```text
artifact-receipt-wave
embedding-row-micro-atlas-wave
decoder-weight-atlas-wave
```

Recommended schema IDs:

```text
ash.basetrain.wave.artifact_receipt.v1
ash.basetrain.wave.embedding_row_micro_atlas.v1
ash.basetrain.wave.decoder_weight_atlas.reserved.v1
```

The decoder-weight schema remains `reserved` in C3 and must not be emitted as an active transport receipt.

---

# 3. Domain ownership matrix

## 3.1 Artifact Receipt Wave

Owner:

```text
artifact serialization / receipt-construction layer
```

Canonical existing implementation:

```text
AtlasParallelStreamingWaveMap
```

C3 semantic rename target:

```text
ArtifactReceiptParallelStreamingWaveMap
```

or equivalent explicit domain wrapper around the existing builder.

Responsibilities:

```text
parallel lane fragment construction
deterministic lane join
deterministic wave merge
lexicographic key ordering
duplicate-key rejection
receipt/manifest object assembly
```

Must not own:

```text
checkpoint payload bytes
GPU buffer residency
embedding rows
decoder weights
hidden tensors
weight slots
module creation
GPU execution authority
```

---

## 3.2 Embedding Row Micro-Atlas Wave

Owner:

```text
R6-R6 token embedding row micro-atlas runtime
```

Existing physical behavior already admitted by parent lineage:

```text
micro_atlas_waves = 8
micro_atlas_peak_bytes = 32768
mega_atlas_create = 0
```

Canonical C3 naming:

```text
EmbeddingRowMicroAtlasWavePlan
EmbeddingRowMicroAtlasWaveReceipt
EmbeddingRowMicroAtlasWaveOrdinal
EmbeddingRowMicroAtlasLaneOrdinal
EmbeddingRowMicroAtlasPeakBytes
```

Responsibilities:

```text
embedding-row checkpoint span selection
bounded row grouping
parallel row decode/read
sequential upload/dispatch
slot reuse after completion
embedding-row payload byte accounting
```

Must not own:

```text
RMSNorm decoder weights
Q/K/V decoder weights
OProj decoder weights
MLP gate/up/down weights
whole decoder block construction
R6-R9 coordinator artifact receipt construction
```

---

## 3.3 Decoder Weight Atlas Wave

C3 state:

```text
RESERVED / NOT IMPLEMENTED / NOT ADMITTED
```

Future owner:

```text
C4 DecoderWeightAtlasWavePlan
```

Reserved responsibilities:

```text
layer-local decoder-weight tensor planning
checkpoint tensor role classification
bounded payload-byte budgeting
parallel checkpoint decode/read lanes
sequential canonical module commit
wave completion fencing
staging ownership handoff
```

C3 must not implement any of these behaviors yet.

Forbidden in C3:

```text
creating decoder-weight streaming buffers
parallel decoding decoder weights
changing rebind loader transport
changing weight residency cardinality
adding partial decoder block staging
promoting decoder-weight PASS
claiming Layer 2 used decoder-weight atlas waves
```

---

# 4. Receipt Wave vs Payload Wave semantic split

C3 introduces a hard semantic distinction:

```text
Receipt Wave
  = metadata/artifact assembly schedule

Payload Wave
  = actual checkpoint/model byte movement schedule
```

Artifact receipt waves are always:

```text
receipt wave
```

Embedding micro-atlas waves are always:

```text
payload wave
```

Future decoder-weight atlas waves will also be:

```text
payload wave
```

A receipt wave may describe a payload wave, but it is not itself a payload wave.

A payload wave may produce receipts, but its receipt builder is not the payload transport authority.

Required invariant:

```text
receipt construction PASS
!= payload transport PASS
```

---

# 5. No cross-domain PASS borrowing

C3 forbids PASS inheritance across wave domains.

Examples of forbidden reasoning:

```text
ArtifactReceiptWave PASS
  therefore DecoderWeightAtlasWave PASS

EmbeddingRowMicroAtlasWave PASS
  therefore decoder weights are wave-streamed

Layer-2 forward PASS
  therefore decoder-weight atlas transport PASS

receipt wave count > 0
  therefore payload wave count > 0
```

Required independent admission fields:

```text
artifactReceiptWaveAdmission
embeddingRowMicroAtlasWaveAdmission
decoderWeightAtlasWaveAdmission
```

For C3 expected state:

```text
artifactReceiptWaveAdmission = ADMITTED
embeddingRowMicroAtlasWaveAdmission = ADMITTED_BY_PARENT_LINEAGE
decoderWeightAtlasWaveAdmission = RESERVED_BLOCKED
```

The exact string values may be normalized, but the three authorities must remain independent.

---

# 6. C3 runtime truth state

C3 must preserve the physically admitted C2 execution facts:

```text
checkpoint layers = 22 for current physical profile
completed steps = 1
source weight layer = 1
target weight layer = 2
weight generation = 1 -> 2
input hidden layer = 2
output hidden layer = 3
hidden generation = 2 -> 3
runtime compared scalar count = 65536 from BQH checked product
mismatch = 0
nonfinite = 0
payload readback = 0
step completion digest = present
```

None of those facts may be relabeled as decoder-weight wave evidence.

---

# 7. Artifact Receipt Wave naming isolation

The current R6-R9 artifact builder is functionally correct but semantically too generic if named only:

```text
AtlasParallelStreamingWaveMap
```

C3 must introduce explicit artifact-domain naming at the public/receipt boundary.

Recommended options:

```rust
pub type ArtifactReceiptParallelStreamingWaveMap = AtlasParallelStreamingWaveMap;
```

or a direct rename if no compatibility surface requires the old name.

Preferred long-term name:

```text
ArtifactReceiptParallelStreamingWaveMap
```

Associated names should also carry artifact identity:

```text
ArtifactReceiptWave
ArtifactReceiptWaveLane
ArtifactReceiptWaveOrdinal
ArtifactReceiptWaveMapSchema
ArtifactReceiptWaveMapRevision
ArtifactReceiptWaveDigest
```

Do not use a bare:

```text
waveMap
waveCount
laneCount
waveDigest
```

in new C3 receipt surfaces where the domain is not self-evident.

---

# 8. Embedding Row Micro-Atlas naming isolation

Existing R6-R6 terminal surfaces such as:

```text
micro_atlas_waves
micro_atlas_peak_bytes
```

must acquire explicit domain aliases or replacement fields in C3 evidence surfaces:

```text
embeddingRowMicroAtlasWaveCount
embeddingRowMicroAtlasPeakPayloadBytes
embeddingRowMicroAtlasMegaAtlasCreateCount
```

Compatibility terminal text may retain legacy names temporarily, but C3 admission must read the explicit domain names.

Recommended typed evidence:

```rust
pub struct EmbeddingRowMicroAtlasWaveEvidence {
    pub wave_count: u32,
    pub peak_payload_bytes: u64,
    pub mega_atlas_create_count: u32,
    pub payload_readback_count: u32,
    pub pass: bool,
    pub evidence_digest: String,
}
```

If equivalent evidence already exists under another type, C3 may adapt it rather than duplicate runtime truth.

---

# 9. Decoder Weight Atlas reserved authority

Introduce a non-executable reserved authority record.

Recommended:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DecoderWeightAtlasWaveReservedAuthority {
    pub domain: BaseTrainWaveDomain,
    pub schema: &'static str,
    pub implementation_state: &'static str,
    pub admission: &'static str,
}
```

Required C3 values:

```text
domain = DecoderWeightAtlas
schema = ash.basetrain.wave.decoder_weight_atlas.reserved.v1
implementation_state = RESERVED_NOT_IMPLEMENTED
admission = BLOCKED
```

This record exists solely to prevent ambiguous future ownership.

It must not contain:

```text
wave count
lane count
payload bytes
decode worker count
commit count
GPU module count
PASS=true
```

because those values are not yet observed.

---

# 10. Weight loader semantic honesty

C3 must explicitly classify the existing R6-R7 decoder-block loader as:

```text
legacy/current full-layer checkpoint loader
```

not:

```text
decoder-weight atlas wave loader
```

Current implementation truth remains:

```text
one decoder layer resident at a time
nine checkpoint weight tensors per resident decoder block
no all-layer preload
no next-layer prefetch
```

But within the layer construction path, decoder weights are not yet proven to use the future parallel/sequential decoder-weight atlas wave transport.

Required receipt truth:

```text
decoderWeightTransportMode = checkpoint-resolved-full-layer-loader
decoderWeightAtlasWaveImplemented = false
decoderWeightAtlasWaveAdmission = BLOCKED
```

C3 must prevent a later generic `wave=true` field from accidentally reclassifying this loader.

---

# 11. C3 typed domain evidence

Recommended aggregate:

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct R6R9WaveDomainAuthorityEvidence {
    pub artifact_receipt_wave: ArtifactReceiptWaveAuthorityEvidence,
    pub embedding_row_micro_atlas_wave: EmbeddingRowMicroAtlasWaveAuthorityEvidence,
    pub decoder_weight_atlas_wave: DecoderWeightAtlasWaveReservedAuthority,
    pub no_cross_domain_pass_borrowing: bool,
    pub no_ambiguous_wave_authority: bool,
    pub evidence_digest: String,
}
```

Each child domain evidence must carry its own digest.

C3 aggregate digest ordering:

```text
artifact receipt wave digest
-> embedding row micro-atlas wave digest
-> decoder weight reserved authority digest
-> no-cross-domain-pass flag
-> no-ambiguous-wave flag
-> C3 aggregate digest
```

---

# 12. Digest separation

The following digests are different authorities and must never be reused as aliases:

```text
artifactReceiptWaveMapDigest
embeddingRowMicroAtlasWaveEvidenceDigest
decoderWeightAtlasReservedAuthorityDigest
r6r9StepCompletionDigest
r6r9C3WaveDomainAuthorityDigest
```

Forbidden:

```text
waveDigest = one digest reused for all domains
artifact digest copied as payload digest
embedding payload digest copied as decoder-weight digest
step completion digest renamed to decoder weight wave digest
```

---

# 13. Artifact receipt wave map metadata

C3-preserved artifact receipt builder metadata should become domain-explicit.

Recommended:

```text
artifactReceiptWaveMap.schema
artifactReceiptWaveMap.revision
artifactReceiptWaveMap.waveCount
artifactReceiptWaveMap.laneCount
artifactReceiptWaveMap.mergeOrder
artifactReceiptWaveMap.digest
```

Merge order remains:

```text
wave ordinal
-> lane ordinal
-> lexicographic key
```

This metadata proves only receipt construction determinism.

---

# 14. Embedding payload wave metadata

Embedding wave evidence should expose payload-specific semantics:

```text
embeddingRowMicroAtlasWave.waveCount
embeddingRowMicroAtlasWave.rowsPerWave
embeddingRowMicroAtlasWave.parallelDecodeWorkerCount
embeddingRowMicroAtlasWave.peakPayloadBytes
embeddingRowMicroAtlasWave.megaAtlasCreateCount
embeddingRowMicroAtlasWave.payloadReadbackCount
embeddingRowMicroAtlasWave.evidenceDigest
```

If some of these values are not currently available as typed evidence, C3 may mark them `UNOBSERVED_IN_C3` rather than fabricate them.

Parent physical facts already observed and safe to promote:

```text
waveCount = 8
peakPayloadBytes = 32768
megaAtlasCreateCount = 0
payloadReadbackCount = 0
```

Any unobserved worker cardinality must remain unasserted unless sourced from runtime receipt/config authority.

---

# 15. Decoder-weight reserved metadata

C3 final receipt must contain a clearly non-runtime reserved block:

```text
decoderWeightAtlasWave.domain = decoder-weight-atlas-wave
decoderWeightAtlasWave.schema = ash.basetrain.wave.decoder_weight_atlas.reserved.v1
decoderWeightAtlasWave.implementationState = RESERVED_NOT_IMPLEMENTED
decoderWeightAtlasWave.admission = BLOCKED
decoderWeightAtlasWave.passBorrowedFromArtifactReceiptWave = false
decoderWeightAtlasWave.passBorrowedFromEmbeddingRowWave = false
```

No runtime counters are allowed in this block.

---

# 16. Coordinator receipt changes

C3 extends the C2 final receipt with a wave-domain authority section.

Required fields:

```text
waveDomainAuthorityDigest
artifactReceiptWaveDomainId
artifactReceiptWaveAdmission
artifactReceiptWaveMapDigest
embeddingRowMicroAtlasWaveDomainId
embeddingRowMicroAtlasWaveAdmission
embeddingRowMicroAtlasWaveEvidenceDigest
decoderWeightAtlasWaveDomainId
decoderWeightAtlasWaveImplementationState
decoderWeightAtlasWaveAdmission
crossDomainPassBorrowCount
ambiguousWaveAuthorityCount
```

Expected C3 values:

```text
crossDomainPassBorrowCount = 0
ambiguousWaveAuthorityCount = 0
```

---

# 17. Per-step receipt changes

The C2 per-step completion receipt must continue to describe actual layer execution.

C3 may add:

```text
artifactReceiptConstructionDomain = artifact-receipt-wave
embeddingPayloadWaveDomain = embedding-row-micro-atlas-wave
decoderWeightPayloadWaveDomain = decoder-weight-atlas-wave
decoderWeightPayloadWaveAdmission = BLOCKED
```

But it must not claim that the current layer-2 weight rebind used decoder-weight atlas waves.

Required:

```text
layer2DecoderWeightTransportMode = checkpoint-resolved-full-layer-loader
```

---

# 18. Manifest changes

C3 local manifest is metadata-only proof publication and remains built through the artifact receipt wave map.

Minimum new fields:

```text
waveDomainAuthorityDigest
artifactReceiptWaveAdmission
embeddingRowMicroAtlasWaveAdmission
decoderWeightAtlasWaveAdmission
crossDomainPassBorrowCount = 0
ambiguousWaveAuthorityCount = 0
```

Manifest construction must not be called a payload wave.

---

# 19. Terminal log contract

Recommended C3 terminal line:

```text
[r6-r9-c3-wave-domain-authority]
artifact_receipt_wave=ADMITTED
artifact_receipt_wave_map_digest=<digest>
embedding_row_micro_atlas_wave=ADMITTED_BY_PARENT_LINEAGE
embedding_wave_count=8
embedding_peak_payload_bytes=32768
embedding_mega_atlas_create=0
decoder_weight_atlas_wave=RESERVED_BLOCKED
decoder_weight_transport_mode=checkpoint-resolved-full-layer-loader
cross_domain_pass_borrow=0
ambiguous_wave_authority=0
wave_domain_digest=<digest>
proof_ledger=HOLD
```

Do not print a bare:

```text
wave=PASS
```

---

# 20. PASS token contract

Recommended C3 PASS token:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C3_WAVE_DOMAIN_AUTHORITY_SPLIT_C2_PHYSICAL_PARENT_ARTIFACT_RECEIPT_WAVE_NAMING_ISOLATED_EMBEDDING_ROW_MICRO_ATLAS_PAYLOAD_WAVE_NAMING_ISOLATED_DECODER_WEIGHT_ATLAS_WAVE_RESERVED_NOT_IMPLEMENTED_BLOCKED_RECEIPT_WAVE_PAYLOAD_WAVE_SEMANTIC_SPLIT_NO_CROSS_DOMAIN_PASS_BORROWING_NO_AMBIGUOUS_WAVE_SSOT_CURRENT_LAYER2_DECODER_WEIGHT_TRANSPORT_CLASSIFIED_CHECKPOINT_RESOLVED_FULL_LAYER_LOADER_ATLAS_PARALLEL_RECEIPT_WAVE_PRESERVED_ZERO_PAYLOAD_READBACK_ZERO_MISMATCH_ZERO_NONFINITE_FULL_N_LAYER_FINAL_NORM_LM_HEAD_FORWARD_LOSS_BACKWARD_OPTIMIZER_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

This PASS token admits only the domain split.

It does not admit decoder-weight wave transport.

---

# 21. CLI policy additions

Recommended additions:

```text
--require-r6-r9-wave-domain-authority-split
true

--require-r6-r9-artifact-receipt-wave-domain
true

--require-r6-r9-embedding-row-micro-atlas-wave-domain
true

--require-r6-r9-decoder-weight-atlas-wave-reserved
true

--allow-r6-r9-cross-domain-pass-borrow
false

--allow-r6-r9-ambiguous-wave-authority
false
```

These flags are assertions only.

They must not select alternate execution implementations.

---

# 22. Static naming audit

C3 must scan the active R6-R6 through R6-R9 route for ambiguous new wave identifiers.

Forbidden new public/receipt identifiers:

```text
WavePlan
WaveReceipt
WaveEvidence
waveCount
waveDigest
waveAdmission
wavePass
```

unless the enclosing type/name already contains one explicit domain:

```text
ArtifactReceipt
EmbeddingRowMicroAtlas
DecoderWeightAtlas
```

Private local loop variables such as `wave_index` may remain if their enclosing function/type is domain-explicit.

---

# 23. Legacy compatibility policy

C3 may temporarily retain legacy internal names where renaming would cause excessive churn, but only under explicit compatibility aliases.

Example:

```rust
#[deprecated(note = "Use ArtifactReceiptParallelStreamingWaveMap")]
pub type AtlasParallelStreamingWaveMap = ArtifactReceiptParallelStreamingWaveMap;
```

If deprecation is too disruptive for C3, the old type may remain internal while all new exported receipt/evidence surfaces use the explicit artifact-domain name.

No legacy generic name may become a new SSOT.

---

# 24. State ownership

C3 does not move runtime state ownership.

```text
Checkpoint tensor inventory
  = checkpoint authority

Weight residency
  = BaseTrainLayerWeightResidencySlot

Hidden state
  = LayerHiddenAuthoritySlot

Layer execution truth
  = R6R8LayerExecutionEvidence

Coordinator step truth
  = R6R9StepCompletionEvidence

Artifact receipt wave authority
  = ArtifactReceiptParallelStreamingWaveMap

Embedding row payload-wave authority
  = R6-R6 embedding micro-atlas runtime/evidence

Decoder weight payload-wave authority
  = RESERVED only, no runtime owner yet
```

C4 is the first patch allowed to create the actual decoder-weight wave planning authority.

---

# 25. No hidden authority creation

C3 must not create any second weight state.

Forbidden:

```text
DecoderWeightAtlasWave object owning resident decoder block
DecoderWeightAtlasWave object owning current weight generation
DecoderWeightAtlasWave object owning hidden generation
ArtifactReceiptWave object owning runtime GPU buffers
EmbeddingRowMicroAtlasWave object becoming general decoder weight loader
```

Domain naming is not state transfer.

---

# 26. Failure behavior

C3 fails closed if:

```text
artifact receipt wave evidence digest missing
embedding row micro-atlas evidence digest missing where required
artifact and embedding digest are equal by accidental aliasing without explicit proof
reserved decoder-weight authority reports PASS
cross-domain pass borrow count != 0
ambiguous wave authority count != 0
current decoder-weight transport mode claims atlas-wave without C4 implementation
receipt wave metadata is used as payload-wave proof
payload-wave metadata is used as receipt construction proof
```

Failure does not roll back Layer 2 runtime authority.

C3 proof failure means:

```text
runtime authority state remains whatever C2 committed
C3 admission = HOLD
proof ledger = HOLD
```

---

# 27. Required changed files

Expected semantic changes:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_artifact_wave_map.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r6_runtime.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

Potential supporting changes only if existing evidence ownership requires them:

```text
crates/model_core/src/base_train_atlas_wave_02_r6_r5_body_splice.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
```

C3 must not widen into decoder-weight loader transport changes.

---

# 28. Files explicitly outside C3 semantic scope

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r7_layer_weight_loader.rs
crates/model_core/src/base_train_layer_weight_residency_authority.rs
actual decoder weight module construction
WGSL kernels
TensorCube kernels
Headwise math
checkpoint format
optimizer
backward
```

If a compile-only import/alias closure is required, treat it as C3-D1 rather than silently widening C3 semantics.

---

# 29. Static validation contract

Minimum checks:

```text
C3 patch ID present = true
C3 build revision present = true
BaseTrainWaveDomain or equivalent sealed registry = present
artifact receipt wave explicit domain = present
embedding row micro-atlas wave explicit domain = present
decoder weight atlas reserved authority = present
receipt wave / payload wave semantic split = present
artifact receipt wave admission independent = true
embedding row wave admission independent = true
decoder weight wave admission independent = true
decoder weight wave implementation state = RESERVED_NOT_IMPLEMENTED
decoder weight wave PASS = absent
cross-domain PASS borrow count = 0
ambiguous wave authority count = 0
current decoder weight transport mode = checkpoint-resolved-full-layer-loader
R6-R9 fixed 65536 factual authority = 0
R6-R9 synthetic dispatch arithmetic = 0
R6-R9 json! artifact construction = 0
recursion_limit workaround = 0
Atlas parallel receipt merge determinism = preserved
C2 step completion digest = preserved
C2 pointer/generation lineage = preserved
WGSL semantic changed file count = 0
.sha256 distributed sidecar count = 0
```

---

# 30. Physical validation

C3 does not require new numerical decoder parity beyond the already-admitted C2 behavior.

Physical rerun still must prove C2 remains intact while C3 domain evidence is emitted.

Required runtime values for current profile:

```text
checkpoint_layers = 22
completed_steps = 1
source_weight_layer = 1
target_weight_layer = 2
weight_generation = 1 -> 2
input_hidden_layer = 2
output_hidden_layer = 3
hidden_generation = 2 -> 3
compared = runtime-derived 65536
mismatch = 0
nonfinite = 0
payload_readback = 0
```

Plus C3:

```text
artifact receipt wave admission = ADMITTED
embedding row micro-atlas wave admission = ADMITTED_BY_PARENT_LINEAGE
decoder weight atlas wave = RESERVED_BLOCKED
cross-domain pass borrow = 0
ambiguous wave authority = 0
wave-domain authority digest = present
```

---

# 31. Physical command

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args"
```

---

# 32. Admission matrix after C3 PASS

```text
R6-R6 live body                         = ADMITTED
R6-R7 layer-weight residency            = ADMITTED
R6-R8 layer-1 forward                   = ADMITTED
R6-R9-C1 Layer-2 single-step            = ADMITTED
R6-R9-C2 coordinator evidence truth     = ADMITTED
R6-R9-C3 wave domain authority split    = ADMITTED on C3 PASS

ArtifactReceiptWave                     = ADMITTED
EmbeddingRowMicroAtlasWave              = ADMITTED_BY_PARENT_LINEAGE
DecoderWeightAtlasWave                  = RESERVED_BLOCKED

R6-R9 full N-layer execution            = BLOCKED
LayerWeightBuildStagingSlot             = BLOCKED / C5
Final RMSNorm / LM head                 = BLOCKED
Forward loss                            = BLOCKED
Backward                                = BLOCKED
Optimizer                               = BLOCKED
Production inference                    = BLOCKED
Proof ledger                            = HOLD
```

---

# 33. Next boundary

After C3 PASS:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4

Decoder Weight Atlas Wave Plan /
Canonical Nine Weight Role Registry /
Checkpoint Tensor Span Binding /
Byte-Budget Wave Packing /
Parallel Decode Lane Plan /
Sequential Canonical Commit Order /
Per-Wave Fence Boundary /
No Mega Atlas /
No Cross-Wave Payload Overlap /
No Runtime Weight Authority Duplication Seal
```

C4 is the first patch allowed to turn:

```text
DecoderWeightAtlasWave = RESERVED
```

into:

```text
DecoderWeightAtlasWavePlan = IMPLEMENTED_CANDIDATE
```

It still must not become canonical runtime authority until later C6/C7/C8 gates.

---

# 34. One-line architecture seal

> C3 separates the word `wave` into three non-interchangeable authorities: artifact receipt waves build proof objects, embedding row micro-atlas waves move embedding payload, and decoder weight atlas waves remain reserved until C4; no PASS, digest, count, or ownership may cross those domain boundaries by implication.
