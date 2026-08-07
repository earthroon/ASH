# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6

## Layer-2 Decoder Weight Wave Rebind Canary / Source Layer-1 Execution Completion Binding / Destructive Weight-1 Eviction / VacantForRebind Boundary / C4 Plan-Bound C5 Staging Execution / Nine-Role Atomic Block Adoption / Weight Generation 1 -> 2 / Failure -> RecoveryRequired / No Legacy Full-Layer Fallback / No Parallel Runtime Weight Authority Seal

> Admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C5` physical PASS  
> Same-invocation execution-source parent: fresh `R6-R8` Layer-1 execution session  
> Source runtime: resident weight layer 1 / generation 1, hidden layer 2 / generation 2  
> Target runtime: resident weight layer 2 / generation 2, hidden layer 2 / generation 2 unchanged  
> Target Layer-2 forward: `BLOCKED`  
> Canonical generalized wave-loader adoption: `BLOCKED`  
> Proof ledger: `HOLD` until physical C6 PASS

---

# 1. Purpose

C5 proved the real Layer-2 checkpoint payload can be consumed through the C4 three-wave / nine-lane plan, converted into nine device materials, sealed as a complete private role set, and constructed into one private decoder block candidate while publishing no runtime weight authority.

C6 is the first patch allowed to cross the runtime weight ownership boundary.

The one-step C6 canary is:

```text
fresh R6-R8 source session
  weight Layer1 / generation1
  hidden Layer2 / generation2
  actual Layer1 execution complete

-> bind source execution completion
-> preflight C4 Layer2 plan from metadata only
-> begin exclusive destructive rebind
-> exclusively remove Layer1 source bundle
-> drop source bundle
-> same-device completion wait
-> mark VacantForRebind
-> execute admitted C5 staging only after vacancy
-> 3 waves / 9 lanes / 9 roles
-> complete nine-role seal
-> construct one complete Layer2 decoder block
-> atomically adopt through BaseTrainLayerWeightResidencySlot
-> resident weight Layer2 / generation2
-> hidden remains Layer2 / generation2
```

C6 does not execute the newly adopted Layer-2 block. That execution parity belongs to C7.

---

# 2. Parent lineage is split deliberately

C6 has two parent meanings and they must not be conflated.

```text
Feature-admission parent
  = C5 physical PASS

Same-invocation destructive transaction source
  = fresh R6-R8 session
```

The C5 physical test session cannot be reused as the C6 source transaction because the prior C1/C2 lineage already rebound runtime weights to Layer 2 before C5 private staging was exercised.

C6 must therefore call the fresh R6-R8 source-session entry point and begin with:

```text
weight slot state                = Resident
resident layer                   = 1
residency generation             = 1
hidden layer                     = 2
hidden generation                = 2
active weight execution leases   = 0
resident decoder blocks          = 1
resident checkpoint tensors      = 9
slot-owned strong references     = 1
```

Silent reuse of an already-Layer2 C5/C4 coordinator session is forbidden.

---

# 3. Runtime SSOT

Canonical runtime weight owner remains:

```text
BaseTrainLayerWeightResidencySlot
```

Canonical hidden owner remains:

```text
LayerHiddenAuthoritySlot
```

C5 staging is construction authority only. It does not become a parallel runtime authority.

After C6 success there must still be exactly one runtime resident decoder block and exactly nine resident checkpoint weight tensors.

---

# 4. Source Layer-1 execution completion binding

Destructive eviction may not begin merely because the weight pointer says `Resident(layer=1)`.

C6 must bind the transition to the actual completed R6-R8 Layer-1 execution.

Introduce a typed source completion binding equivalent to:

```rust
pub struct R6R9C6SourceExecutionCompletionBinding {
    pub source_layer_index: u32,
    pub source_weight_pointer_digest: String,
    pub source_weight_generation: u64,
    pub source_weight_transition_serial: u64,
    pub source_block_identity_digest: String,
    pub source_execution_evidence_digest: String,
    pub source_final_receipt_digest: String,
    pub output_hidden_pointer_digest: String,
    pub output_hidden_generation: u64,
    pub output_hidden_completion_token_digest: String,
    pub output_hidden_shape_bqh: [u32; 3],
    pub payload_readback_count: u64,
    pub mismatch_count: u64,
    pub non_finite_count: u64,
    pub pass: bool,
    pub binding_digest: String,
}
```

For the canary:

```text
source layer                    = 1
source weight generation        = 1
output hidden layer             = 2
output hidden generation        = 2
mismatch                        = 0
nonfinite                       = 0
payload readback                = 0
pass                            = true
```

The binding must cross-check actual R6-R8 typed execution evidence, final receipt digest, source weight pointer, output hidden pointer, hidden completion token and semantic BQH shape.

The binding digest becomes the `last_execution_completion_digest` passed into the destructive weight transaction and must be preserved through EvictionArmed, VacantForRebind, RecoveryRequired if entered, and final adopted Resident pointer.

No C4 plan digest, C5 staging digest, hidden pointer digest, or artifact digest may be silently substituted for source execution completion.

---

# 5. C4 Layer-2 plan preflight before destruction

Before mutating runtime weight state, C6 computes or validates the Layer-2 C4 plan using checkpoint metadata only.

Current physical fixture requires:

```text
target layer                    = 2
roles                           = 9
lanes                           = 9
waves                           = 3
max host transient budget       = 268435456
parallel decode workers         = 4
max lanes per wave              = 4
mega atlas planned              = 0
cross-wave payload overlap      = 0
runtime weight authority plan   = 0
```

Plan failure occurs before the destructive boundary and leaves source runtime state unchanged.

No C5 checkpoint payload reads, decoder materialization, or target staging may occur during this metadata-only preflight.

C4 plan digest, plan-wave collection digest, role registry digest, span binding digest and canonical commit-order digest are captured before source eviction.

---

# 6. Legacy-compatible target tensor-set digest SSOT

The runtime pointer field `layer_tensor_set_digest` must keep the exact existing R6-R6/R6-R7 meaning.

Canonical formula:

```text
SHA256(serde_json({
  selectedLayer,
  checkpointSetDigest,
  tensorKeys,
  tensorIdentityDigests
}))
```

C6 must not invent a new digest formula.

One shared Rust helper must own the formula and both the existing full-layer authority and C6 wave path must call that helper.

For C6, tensor keys and identity digests are collected from the exact nine C4 role bindings in canonical registry order `0..8`.

No legacy full-layer payload load may be executed merely to obtain the digest.

---

# 7. Atomic exclusive destructive begin

The older R6-R7 sequence exposes separate calls:

```text
arm_eviction()
take_armed_bundle()
```

C6 must not create a new canary path that can strand the slot as `EvictionArmed` if exclusive bundle extraction fails.

C6 requires a rollback-safe atomic primitive equivalent to:

```rust
pub fn begin_exclusive_destructive_rebind(
    &self,
    expected_generation: u64,
    expected_pointer_digest: &str,
    source_layer_index: u32,
    target_layer_index: u32,
    operation_id: &str,
    last_execution_completion_digest: &str,
) -> Result<BaseTrainLayerWeightDestructiveBegin>
```

with a result equivalent to:

```rust
pub struct BaseTrainLayerWeightDestructiveBegin {
    pub armed_pointer: BaseTrainLayerWeightResidencyPointer,
    pub source_bundle: R6R6ActualDecoderBlockBundle,
}
```

While holding the residency mutex, it must validate:

```text
state == Resident
resident layer == 1
target layer == source + 1
residency generation == 1
pointer digest == expected pointer
active execution lease count == 0
resident bundle exists
resident bundle selected layer == source layer
Arc strong_count == 1
operation id not previously committed
source completion digest is valid
```

It then prepares the EvictionArmed pointer and exclusively extracts the source `Arc` bundle.

If `Arc::try_unwrap` or equivalent exclusive extraction fails before ownership transfer completes:

```text
resident bundle restored
original Resident pointer retained
no published transition serial advance
no RecoveryRequired transition
no target staging
```

The operation fails pre-destructively.

---

# 8. Exact destructive boundary

For C6 the operational destructive boundary is:

```text
successful exclusive source-bundle extraction from BaseTrainLayerWeightResidencySlot
```

After this point the runtime slot no longer owns the source Layer-1 decoder block.

Source rollback is forbidden after successful extraction.

This boundary is stricter and more precise than treating `VacantForRebind` alone as the first destructive instant.

---

# 9. Source teardown and fence

After successful extraction C6 validates the source bundle is Layer 1 and matches the bound block identity, then relinquishes the source Rust owner.

The canary performs the canonical same-device completion wait before opening target staging:

```text
device.poll(wgpu26::PollType::Wait)
```

or the exact canonical same-device completion primitive for the runtime.

C6 may claim source Rust owner release and observed runtime-slot ownership count zero.

It must not claim immediate physical VRAM reclamation solely from Rust drop.

If the completion wait fails after exclusive source extraction, the transaction is destructive and must escalate to RecoveryRequired.

---

# 10. VacantForRebind boundary

Only after source owner release and teardown completion may C6 call the canonical vacancy transition.

Expected vacancy state:

```text
state                            = VacantForRebind
resident layer                   = None
target layer                     = Some(2)
residency generation             = 1
resident decoder blocks          = 0
resident checkpoint tensors      = 0
active execution leases          = 0
actual decoder block identity    = None
runtime LoRA digest              = None
last execution completion digest = C6 source completion binding digest
```

Hidden state remains Layer 2 / generation 2.

---

# 11. No target payload before vacancy

C6 must prove:

```text
C5 checkpoint reads before VacantForRebind = 0
C5 decodes before VacantForRebind          = 0
C5 material commits before vacancy         = 0
```

C4 metadata planning is allowed before vacancy because it performs no target payload execution.

Target staging begins only after the vacancy pointer and zero-resident counts are physically observed.

---

# 12. C5 staging reuse, not reimplementation

C6 must call the admitted C5 private staging implementation directly or via a thin transaction wrapper.

The C6 orchestrator must not duplicate checkpoint decode, host ownership ledger, lane scheduling, material commit or nine-role seal logic.

Expected C5 facts remain:

```text
plan waves                 = 3
lanes                      = 9
roles                      = 9
checkpoint reads           = 9
decodes                    = 9
material commits           = 9
source owner releases      = 9
decoded owner releases     = 9
wave fence waits           = 3
complete nine-role seal    = 1
cross-wave host overlap    = 0
mega atlas                 = 0
GPU weight readback        = 0
observed host ownership peak <= C4 budget
```

The staging operation ID is deterministically derived from the rebind operation ID and C4 plan identity. No timestamps, random UUIDs, pointer addresses or worker-scheduling order may enter canonical digests.

---

# 13. Nine-role atomic target block

Only after the C5 complete nine-role seal may C6 accept the complete Layer-2 decoder block candidate.

Required candidate facts:

```text
selected layer                         = 2
actual decoder block instances         = 1
linear modules                         = 7
norm modules                           = 2
runtime LoRA sets                      = 1
trainable LoRA slots                   = 0
checkpoint tensor payload reads        = 9
checkpoint weight uploads              = 9
checkpoint tensor-set digest           = source checkpoint-set digest
module identity digest length          = 64
```

No partial role set may be passed to runtime adoption.

C5's outer candidate/staging receipt digest must not be substituted for the actual decoder block module identity digest.

---

# 14. Atomic runtime adoption

The only runtime publication point is the existing canonical:

```text
BaseTrainLayerWeightResidencySlot::adopt(...)
```

C6 adopts one complete Layer-2 block from `VacantForRebind`.

Expected post-adopt runtime pointer:

```text
state                            = Resident
resident layer                   = Some(2)
target layer                     = None
residency generation             = 2
layer tensor-set digest          = shared target authority digest
layer tensor identity count      = 9
actual decoder block identity    = C5-built module identity digest
runtime LoRA binding digest      = C5 candidate runtime LoRA digest
last execution completion digest = source completion binding digest
operation id                     = C6 rebind operation id
```

Generation relation:

```text
adopted generation = source generation + 1 = 2
```

Pointer lineage must preserve:

```text
armed.previous_pointer_digest   == source.pointer_digest
vacant.previous_pointer_digest  == armed.pointer_digest
adopted.previous_pointer_digest == vacant.pointer_digest
```

Transition serials must advance monotonically according to the runtime state machine; hardcoded serial values are not semantic authority.

---

# 15. No parallel runtime weight authority

Runtime resident-count waveform must be:

```text
source Resident: blocks=1, tensors=9, slot strong owners=1
Vacant:          blocks=0, tensors=0, slot strong owners=0
target Resident: blocks=1, tensors=9, slot strong owners=1
```

Required:

```text
peak runtime resident decoder block count = 1
peak runtime resident weight tensor count  = 9
source-target runtime authority overlap    = 0
```

C5 private staging resources are construction resources and are not runtime weight authority, but C6 additionally orders target staging after source runtime removal to avoid intentional source-runtime/staging overlap in the canary.

C6 must not equate this ownership statement with a physical VRAM-overlap measurement.

---

# 16. Hidden state immutability

C6 is a weight rebind gate only.

Before source destruction, capture the current R6-R8 output hidden pointer. After target adoption require exact equality of:

```text
hidden pointer digest
layer index = 2
hidden generation = 2
transition serial
buffer identity
completion token
semantic BQH shape
active hidden execution leases = 0
```

C6 produces no Layer-3 hidden state.

---

# 17. No target forward

The newly adopted Layer-2 block must not execute in C6.

Required C6 target counters:

```text
target Layer2 forward          = 0
input norm dispatch            = 0
QKV projection                 = 0
Stage10 candidate              = 0
Stage11 candidate              = 0
Stage12 candidate              = 0
OProj                          = 0
MLP gate                       = 0
MLP up                         = 0
MLP down                       = 0
hidden commit                  = 0
```

Parent R6-R8 Layer-1 execution counters remain parent evidence and must not be attributed to the adopted Layer-2 block.

Wave-built Layer-2 execution parity is C7.

---

# 18. Failure policy before the destructive boundary

Failures before successful exclusive source extraction include source evidence mismatch, stale pointers, active leases, plan preflight failure, operation-id conflict, or inability to obtain exclusive source ownership.

Required outcome:

```text
source runtime remains Resident Layer1 / generation1
source bundle remains slot-owned
hidden remains Layer2 / generation2
RecoveryRequired transition count = 0
C5 checkpoint reads = 0
```

No destructive state change is published.

---

# 19. Failure policy after the destructive boundary

After successful exclusive source extraction, every failure before successful target adoption is destructive.

Examples:

```text
source teardown fence failure
vacancy transition failure after extraction
C5 checkpoint read/decode/material failure
C5 wave fence failure
C5 complete seal failure
private block construction failure
target tensor-set provenance failure
adopt precondition failure
```

Required action:

```text
attempt BaseTrainLayerWeightResidencySlot::mark_recovery_required(...)
return failure
```

Source rollback is forbidden.

No legacy target full-layer fallback is permitted.

No source rebuild is permitted.

Recovery escalation must work from whichever post-extraction no-bundle state is current, including `EvictionArmed` with no resident bundle and `VacantForRebind`.

---

# 20. Recovery escalation failure

If the original post-destructive error occurs and `mark_recovery_required()` itself fails, C6 must return an explicit terminal failure equivalent to:

```text
R6R9C6RecoveryEscalationFailed
```

and preserve both the original failure and recovery-transition failure in diagnostic evidence.

The canary must not pretend the runtime is safely recoverable when the recovery seal could not be established.

---

# 21. No legacy full-layer loader or fallback

The C6 active target path must have zero call edges to:

```text
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
load_base_train_atlas_wave_02_r6_r6_decoder_block
rebind_resident_decoder_layer    // existing generalized legacy full-layer rebind
```

Those functions may remain in the repository for historical/parent gates, but C6 may not use them for target Layer 2.

Required success receipts:

```text
legacy full-layer loader invocation = 0
legacy full-layer fallback          = 0
source rebuild                      = 0
```

Failure handlers must contain no fallback call to those routes.

---

# 22. Same-device lineage

Source runtime, C5 staging and target adopted block remain on the same canonical process/device lineage:

```text
same process
same WGPU device
same queue lineage
same Burn WgpuDevice
```

C6 must not create a second WGPU device for target staging.

---

# 23. No prefetch or multi-layer widening

C6 is exactly one rebind step:

```text
source layer = 1
target layer = 2
max rebind steps = 1
```

Forbidden:

```text
Layer3 auto continuation
next-layer prefetch
all-layer preload
parallel layer staging
persistent target staging after canary
```

The canary ends immediately after successful Layer-2 adoption.

---

# 24. C6 transaction receipt

Introduce a typed transaction receipt equivalent to:

```rust
pub struct R6R9C6WaveRebindTransactionReceipt {
    pub patch_id: String,
    pub build_revision: String,
    pub operation_id: String,
    pub source_layer: u32,
    pub target_layer: u32,
    pub source_execution_completion_binding_digest: String,
    pub source_weight_pointer_digest: String,
    pub source_weight_generation: u64,
    pub c4_plan_digest: String,
    pub c4_plan_wave_collection_digest: String,
    pub c5_staging_receipt_digest: String,
    pub c5_staging_complete_digest: String,
    pub target_tensor_set_authority_digest: String,
    pub target_block_identity_digest: String,
    pub armed_pointer_digest: String,
    pub vacant_pointer_digest: String,
    pub adopted_pointer_digest: String,
    pub adopted_generation: u64,
    pub legacy_full_layer_loader_invocation_count: u32,
    pub legacy_full_layer_fallback_count: u32,
    pub source_rebuild_count: u32,
    pub source_target_runtime_authority_overlap_count: u32,
    pub runtime_adopt_count: u32,
    pub target_forward_count: u32,
    pub hidden_mutation_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

No tensor payload is serialized into the receipt.

---

# 25. Digest hierarchy

Keep distinct:

```text
R6-R8 execution evidence digest
R6-R8 final receipt digest
C6 source completion binding digest
C4 plan digest
C4 plan-wave collection digest
C5 staging receipt digest
C5 staging complete digest
C5 candidate/block module identity digest
C6 target tensor-set authority digest
armed pointer digest
vacant pointer digest
adopted pointer digest
C6 transaction receipt digest
C6 final receipt digest
ArtifactReceiptWaveMap digest
```

No digest aliasing is allowed.

---

# 26. Artifact receipt wave isolation

C6 evidence continues to use `ArtifactReceiptParallelStreamingWaveMap` for metadata serialization only.

Artifact receipt waves are not decoder-weight payload waves.

All root keys must remain globally unique under the artifact map. Duplicate-key fail-closed behavior must not be weakened.

Recommended artifact sections:

```text
sourceExecutionCompletionBinding
c4DecoderWeightPlanBinding
c6DestructiveEviction
c5StagingExecutionBinding
c6TargetWeightAdoption
c6RecoveryBoundary
c6HiddenImmutability
c6NoLegacyFallback
```

---

# 27. CLI contract

C6 requires the following hard policy:

```text
--require-r6-r9-c6-layer2-wave-rebind true
--r6-r9-c6-source-layer 1
--r6-r9-c6-target-layer 2
--r6-r9-c6-max-rebind-steps 1
--require-r6-r9-c6-source-execution-completion-binding true
--require-r6-r9-c6-exclusive-destructive-eviction true
--require-r6-r9-c6-vacant-before-staging true
--require-r6-r9-c6-c5-staging-after-vacancy true
--require-r6-r9-c6-nine-role-atomic-adoption true
--require-r6-r9-c6-generation-one-to-two true
--require-r6-r9-c6-recovery-after-destructive-failure true
--allow-r6-r9-c6-legacy-full-layer-loader false
--allow-r6-r9-c6-legacy-full-layer-fallback false
--allow-r6-r9-c6-source-rebuild false
--allow-r6-r9-c6-target-forward false
--allow-r6-r9-c6-hidden-mutation false
--allow-r6-r9-c6-parallel-runtime-weight-authority false
--allow-r6-r9-c6-next-layer-prefetch false
```

Existing C4 byte-budget / worker / lane policy and C5 staging policy remain authoritative and are reused.

---

# 28. Implementation surface

Expected semantic files:

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
crates/model_core/src/base_train_layer_weight_residency_authority.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c6_layer2_wave_rebind.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

WGSL semantic changes are forbidden in C6.

Core/runtime/model behavior remains Rust/WGPU host logic. No JS/TS/Python canonical execution path is introduced.

---

# 29. Static closure requirements

Before physical run require at minimum:

```text
fresh R6-R8 source session call = present
source completion typed binding = present
source completion digest carried into runtime transition = present
C4 plan preflight before destructive begin = present
atomic exclusive destructive begin = present
active lease check = present
Arc strong_count == 1 check = present
exclusive extraction rollback to Resident on pre-extraction failure = present
successful extraction defined as destructive boundary = present
source bundle drop = present
same-device completion wait = present
VacantForRebind before C5 staging = present
C5 admitted staging executor reused = present
new duplicate staging implementation = absent
shared target tensor-set digest helper = used by legacy and C6
exact nine target tensor identities = present
runtime adopt only after complete C5 candidate = present
generation 1 -> 2 = checked
pointer previous-digest chain = checked
runtime LoRA digest = checked
runtime final block count = 1
runtime final tensor count = 9
runtime authority overlap = 0
legacy R6-R7 target loader call = 0
legacy R6-R6 target loader call = 0
legacy generalized rebind call = 0
legacy fallback handler = 0
source rebuild call = 0
hidden exact equality before/after = required
target Layer2 execution call = 0
WGSL semantic changed files = 0
```

---

# 30. Physical success requirements

A successful C6 physical run must end with:

```text
source layer                        = 1
target layer                        = 2
source generation                   = 1
target generation                   = 2
source completion bound             = 1
destructive source eviction         = 1
vacant boundary                     = 1
staging after vacancy               = 1
plan waves                          = 3
lanes                               = 9
roles                               = 9
checkpoint reads                    = 9
decodes                             = 9
material commits                    = 9
complete nine-role seal             = 1
runtime adopt                       = 1
runtime resident blocks             = 1
runtime resident weight tensors     = 9
runtime authority overlap           = 0
legacy full-layer loader            = 0
legacy fallback                     = 0
source rebuild                      = 0
hidden layer                        = 2
hidden generation                   = 2
hidden pointer unchanged            = 1
target forward                      = 0
recovery-required transition        = 0 on success path
GPU weight readback                 = 0
```

Success-only C6 PASS does not physically exercise the destructive failure branch. A later controlled C6-D1 failure-injection gate may prove RecoveryRequired physically.

---

# 31. Expected terminal line

```text
[r6-r9-c6-layer2-wave-rebind]
source_layer=1
target_layer=2
source_generation=1
target_generation=2
source_completion_bound=1
destructive_source_eviction=1
vacant_boundary=1
staging_after_vacancy=1
plan_waves=3
lanes=9
roles=9
checkpoint_reads=9
decodes=9
material_commits=9
complete_nine_role_seal=1
runtime_adopt=1
runtime_resident_blocks=1
runtime_resident_weight_tensors=9
runtime_authority_overlap=0
legacy_full_layer_loader=0
legacy_fallback=0
source_rebuild=0
hidden_layer=2
hidden_generation=2
hidden_pointer_unchanged=1
target_forward=0
recovery_required_transition=0
gpu_weight_readback=0
source_completion_digest=<digest>
c4_plan_digest=<digest>
c5_staging_digest=<digest>
target_tensor_set_digest=<digest>
adopted_pointer_digest=<digest>
proof_ledger=HOLD
```

---

# 32. PASS meaning

C6 PASS admits only the one-step Layer1 -> Layer2 wave-built runtime rebind canary.

It proves:

```text
fresh completed Layer1 execution can bind destructive weight eviction
Layer1 runtime weight authority can be exclusively removed
VacantForRebind can be reached before target staging
real Layer2 checkpoint payload can be wave-staged after vacancy
one exact complete wave-built Layer2 block can be atomically adopted
runtime weight generation advances exactly 1 -> 2
hidden Layer2 state survives unchanged
no legacy full-layer target loader participates
no source rollback participates
no second runtime weight authority is published
```

It does not prove:

```text
wave-built Layer2 forward numerical parity
Layer3 hidden correctness
destructive failure branch physically exercised
canonical generalized wave-loader adoption
progressive 22-layer execution
physical RAM/VRAM reduction
performance improvement
final RMSNorm / LM head
forward loss
backward
optimizer
production inference
```

---

# 33. Admission matrix after physical C6 PASS

```text
R6-R6 live body                              = ADMITTED
R6-R7 layer-weight residency                 = ADMITTED
R6-R8 Layer-1 forward                        = ADMITTED
R6-R9-C1 historical Layer-2 step             = ADMITTED
R6-R9-C2 coordinator evidence truth          = ADMITTED
R6-R9-C3 wave-domain split                   = ADMITTED
R6-R9-C4 decoder-weight wave planner         = ADMITTED_PLANNER_ONLY
R6-R9-C4-D1 plan collection closure          = ADMITTED
R6-R9-C5 private staging/build               = ADMITTED_PRIVATE_CANDIDATE
R6-R9-C6 Layer1 -> Layer2 wave rebind canary = ADMITTED_RUNTIME_REBIND_CANARY on PASS

DecoderWeightAtlasWave planning              = ADMITTED
DecoderWeightAtlasWave private build         = ADMITTED
DecoderWeightAtlasWave runtime adoption      = ADMITTED_CANARY_ONLY on PASS
wave-built Layer2 execution parity           = BLOCKED / C7
canonical generalized wave-loader adoption   = BLOCKED / C8
progressive N-layer promotion                = BLOCKED / C9
full N-layer execution                       = BLOCKED
final RMSNorm / LM head                      = BLOCKED
forward loss / backward / optimizer          = BLOCKED
production inference                         = BLOCKED
proof ledger                                 = HOLD
```

---

# 34. Next boundary

After physical C6 PASS:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C7

Layer-2 Wave-Built Decoder Execution Parity /
Adopted Wave Block Execution Lease /
Exact Input Hidden-2 Binding /
Actual Input RMSNorm·QKV·Headwise·OProj·MLP Route /
Legacy-Loader Reference Non-Authority Oracle /
Hidden-3 Full-Surface Parity /
Dispatch Evidence Parity /
Zero Mismatch·Nonfinite /
No Weight Reload·No Rebuild /
No Payload Readback Seal
```

C7 is the first gate allowed to execute the C6-adopted wave-built Layer-2 block and commit Hidden 3.

---

# Architecture seal

> C6 starts from a fresh physically completed Layer-1 runtime state, binds that execution completion to an exclusive destructive weight transition, removes Layer 1 before any target payload staging, crosses an explicit VacantForRebind boundary, executes the admitted C4/C5 three-wave nine-role build without any legacy full-layer fallback, and publishes exactly one complete Layer-2 block through the existing runtime weight SSOT with generation 1 -> 2 while Hidden 2 remains untouched; after exclusive source extraction, every unsuccessful target path must terminate in RecoveryRequired or a transparently reported recovery-escalation failure.