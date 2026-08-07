# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C5

## Layer Weight Build Staging Slot / Private Incomplete-Block Authority / Wave Decode Result Intake / Sequential Module Material Commit / Per-Role Source·Decoded Buffer Drop / Complete Nine-Role Seal / Atomic Decoder Block Construction / Failure-to-RecoveryRequired Boundary / No Partial Block Runtime Exposure / No Second Runtime Weight Authority Seal

> Parent physical SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C4-D1` physical PASS  
> Parent planner result for current Layer-2 canary: `roles=9 / waves=3 / lanes=9 / budget=268435456 / peak planned transient=218120192`  
> Parent plan transport: `decoder-weight-atlas-wave`  
> Parent active runtime transport: `checkpoint-resolved-full-layer-loader`  
> C5 scope: private staged material construction and atomic complete-block candidate construction  
> Canonical runtime weight owner: `BaseTrainLayerWeightResidencySlot`  
> C5 runtime publication: `FORBIDDEN`  
> C5 canonical loader adoption: `BLOCKED`  
> C5 Layer-2 rebind adoption: `BLOCKED`  
> Proof ledger: `HOLD` until physical C5 PASS

---

# 0. C5 purpose

C4-D1 proves that the real Layer-2 checkpoint metadata can be deterministically planned as three decoder-weight payload waves containing nine lanes under the configured 256 MiB host-transient ownership budget.

C4-D1 does **not** move payload bytes.

C5 is the first boundary allowed to execute the decoder-weight payload plan in a private construction context.

C5 must prove the following without changing runtime weight authority:

```text
C4 plan
  -> exact checkpoint span read
  -> parallel lane decode within one wave
  -> source byte owner release
  -> sequential device material commit
  -> decoded f32 owner release
  -> per-wave completion fence
  -> next wave
  -> exact nine-role complete seal
  -> private complete decoder block candidate
  -> candidate dropped without runtime publication
```

The central C5 invariant is:

> Incomplete decoder-weight material may exist only inside the private staging authority. No incomplete block, incomplete material set, or partial role set may become a resident runtime decoder block.

---

# 1. Current parent code truth

The current active R6-R7 rebind path is:

```text
rebind_resident_decoder_layer()
  -> arm_eviction()
  -> take_armed_bundle()
  -> drop(source bundle)
  -> device.poll(Wait)
  -> mark_vacant()
  -> load_base_train_atlas_wave_02_r6_r7_decoder_block_weights()
  -> load_base_train_atlas_wave_02_r6_r6_decoder_block()
  -> read all nine checkpoint tensors
  -> decode all nine to Vec<f32>
  -> R6R6ActualDecoderBlockWeightValues
  -> build_r6_r7_actual_decoder_block_for_layer()
  -> build_r6_r6_actual_decoder_block()
  -> adopt()
```

`load_base_train_atlas_wave_02_r6_r6_decoder_block()` currently retains a `Vec<Vec<f32>>` equivalent of all nine decoded tensors before it constructs `R6R6ActualDecoderBlockWeightValues`.

`build_r6_r6_actual_decoder_block()` then converts those vectors into:

```text
2 x AshRmsNorm
7 x AshLinear
```

and returns one `R6R6ActualDecoderBlockBundle`.

The current R6-R7 runtime slot already has the correct destructive-failure boundary:

```text
Resident
  -> EvictionArmed
  -> VacantForRebind
  -> target build/adoption succeeds -> Resident
  -> target build/adoption fails    -> RecoveryRequired
```

C5 must preserve that runtime state machine. It does not replace it.

---

# 2. C5 admission boundary

C5 promotes:

```text
DecoderWeightAtlasWavePlan
  IMPLEMENTED_CANDIDATE_PLAN_ONLY
```

to:

```text
LayerWeightBuildStagingSlot
  IMPLEMENTED_PRIVATE_CANDIDATE

DecoderWeightAtlasWave private payload execution
  IMPLEMENTED_CANDIDATE_NOT_ADOPTED
```

C5 still keeps:

```text
canonical runtime decoder-weight transport
  = checkpoint-resolved-full-layer-loader

canonical runtime weight slot adoption from wave build
  = BLOCKED

Layer-2 wave rebind
  = BLOCKED / C6
```

A C5 PASS must not be interpreted as C6, C7, or C8 admission.

---

# 3. State ownership matrix

## 3.1 Checkpoint authority

Owner:

```text
BaseTrainAtlasWave02R5CheckpointTensorSetAuthority
```

Owns:

```text
tensor inventory
shard identity
byte spans
dtype
shape
element count
checkpoint-set digest
```

C5 must not create a second safetensors inventory parser.

## 3.2 Planner authority

Owner:

```text
DecoderWeightAtlasWavePlan
```

Owns:

```text
nine-role registry binding
three-wave plan for current fixture
lane identities
checkpoint span identities
byte-budget plan
commit ordinals
fence requirements
plan digest
```

The planner does not own payload.

## 3.3 Private staging authority

New owner:

```text
LayerWeightBuildStagingSlot
```

Owns only incomplete and complete-but-unpublished device materials for one target layer and one C4 plan digest.

It is **not** a runtime decoder weight authority.

It must not implement:

```text
acquire_execution_lease()
bundle()
forward()
execute()
adopt_runtime()
replace_resident()
```

No execution API may accept a staging slot.

## 3.4 Runtime weight authority

Unchanged owner:

```text
BaseTrainLayerWeightResidencySlot
```

Only this slot may publish the active `R6R6ActualDecoderBlockBundle` to the layer-forward path.

C5 must not mutate this slot during the private staging canary.

## 3.5 Hidden authority

Unchanged owner:

```text
LayerHiddenAuthoritySlot
```

C5 must not mutate hidden state.

---

# 4. New staging state machine

Required state enum or equivalent:

```rust
pub enum LayerWeightBuildStagingState {
    Empty,
    Building,
    CompleteNineRoles,
    SealedComplete,
    Consumed,
    Aborted,
}
```

Allowed transitions:

```text
Empty
  -> Building

Building
  -> Building
  -> CompleteNineRoles
  -> Aborted

CompleteNineRoles
  -> SealedComplete
  -> Aborted

SealedComplete
  -> Consumed
  -> Aborted

Consumed
  -> terminal

Aborted
  -> terminal
```

Forbidden transitions:

```text
Aborted -> Building
Consumed -> Building
Consumed -> SealedComplete
SealedComplete -> Building
CompleteNineRoles -> Building new target
```

One staging slot is single-use and bound to one target layer, one checkpoint-set digest, and one C4 plan digest.

Silent reset/reuse is forbidden.

---

# 5. Staging identity

Each staging slot must be sealed with immutable identity fields before the first payload read:

```text
schemaVersion
patchId
buildRevision
modelInstanceId
trainingSessionId
routeId
targetLayer
checkpointSetDigest
c4PlanDigest
packingPolicyDigest
roleRegistryDigest
spanBindingDigest
canonicalCommitOrderDigest
expectedWaveCount
expectedLaneCount
expectedRoleCount
operationId
```

Current fixture expectations:

```text
targetLayer = 2
expectedWaveCount = 3
expectedLaneCount = 9
expectedRoleCount = 9
```

No field may be inferred from runtime state when the C4 plan already owns it.

---

# 6. Private material layout

The staging slot must not retain checkpoint source bytes or decoded `Vec<f32>` after a role material commit.

The private payload owner is device-side tensor material.

Recommended internal layout:

```rust
struct LayerWeightBuildStagingMaterials {
    input_norm: Option<Tensor<InferenceBackend, 1>>,
    q_proj: Option<Tensor<InferenceBackend, 2>>,
    k_proj: Option<Tensor<InferenceBackend, 2>>,
    v_proj: Option<Tensor<InferenceBackend, 2>>,
    o_proj: Option<Tensor<InferenceBackend, 2>>,
    post_attn_norm: Option<Tensor<InferenceBackend, 1>>,
    gate_proj: Option<Tensor<InferenceBackend, 2>>,
    up_proj: Option<Tensor<InferenceBackend, 2>>,
    down_proj: Option<Tensor<InferenceBackend, 2>>,
}
```

The exact type name may differ, but the ownership semantics must match.

A generic `Vec<Vec<f32>>`, `HashMap<Role, Vec<f32>>`, or nine decoded host vectors stored inside the staging slot is forbidden.

---

# 7. Why device material is the staging payload

C5 must not preserve all nine decoded host arrays until final block construction.

That would recreate the parent full-layer-loader memory shape and defeat the C4 wave budget.

Required lifetime:

```text
source checkpoint bytes
  local lane owner only

  -> decode

decoded Vec<f32>
  lane result / current material commit only

  -> Tensor::from_data / equivalent device materialization

device Tensor material
  private staging owner

source bytes owner = released
decoded Vec owner = released
```

C5 may claim Rust ownership release.

C5 must **not** claim that allocator RSS, pinned staging memory, driver upload memory, or physical VRAM was immediately freed solely because a Rust value was dropped.

---

# 8. Exact decode implementation reuse

C5 must not fork the F16/BF16/F32 scalar decode rules.

Current R6-R6 code already owns:

```text
dtype width
F16 -> f32 decode
BF16 -> f32 decode
F32 little-endian decode
finite-value validation
element-count validation
```

C5 must extract or reuse a single Rust decode helper so the existing full-layer loader and new C5 wave decoder share one decode SSOT.

Recommended internal helper surface:

```rust
pub(crate) fn read_checkpoint_tensor_f32(
    authority: &BaseTrainAtlasWave02R5CheckpointTensorSetAuthority,
    tensor: &BaseTrainAtlasWave02R5R6TensorAuthority,
) -> Result<DecodedCheckpointTensorF32>
```

or equivalent.

The helper may expose a receipt containing:

```text
tensor key
tensor identity digest
source payload bytes
decoded element count
decoded f32 bytes
source read count = 1
nonfinite count = 0
decoded payload digest
```

A second independent decode implementation is forbidden.

---

# 9. Wave execution contract

C5 consumes C4 waves in exact `wave_ordinal` order.

For each wave:

```text
1. validate previous-wave fence requirement
2. validate all lane plans
3. parallel read/decode lane payloads
4. join every lane
5. fail entire wave if any lane failed
6. sort successful lane results by lane ordinal
7. sequentially material-commit each role into private staging
8. release decoded host owner after each commit
9. wait per-wave completion fence
10. seal wave execution receipt
11. require zero source/decoded host owners before next wave
```

No lane from wave N+1 may begin payload read before wave N's completion boundary is satisfied.

---

# 10. Parallel lane decode

Parallelism is limited by the C4 plan.

Current fixture:

```text
parallel_decode_worker_count = 4
max_lanes_per_wave = 4
```

C5 must not spawn more payload workers than the plan allows.

Recommended execution primitive:

```text
scoped Rust worker threads / bounded worker pool
```

JavaScript, TypeScript, browser workers, Node workers, Python workers, and external helper processes are forbidden in the canonical decoder-weight path.

Each lane must bind exactly:

```text
wave ordinal
lane ordinal
role
registry ordinal
commit ordinal
checkpoint span digest
tensor identity digest
tensor key
dtype
shape
element count
source payload bytes
decoded f32 bytes
lane plan digest
```

Any mismatch fails closed before material commit.

---

# 11. Decode wave two-phase behavior

A wave has two phases:

```text
Phase A: parallel decode
Phase B: sequential material commit
```

No material from the current wave may be committed until **all** lane decodes in the wave have succeeded.

Reason:

```text
lane 0 decode success
lane 1 decode failure
```

must not leave a half-committed current wave merely because lane 0 finished first.

Previous successfully sealed waves may already exist in staging. If a later wave fails, the entire staging slot transitions to `Aborted` and all private materials are dropped.

No partial staging state may be reused.

---

# 12. Source byte owner release

Inside each lane worker:

```text
read exact half-open checkpoint span
  -> source byte owner acquired

decode to Vec<f32>
  -> source + decoded owners may coexist

validate decoded result
  -> source byte owner released before lane result leaves worker

return decoded result only
```

Required receipt counters:

```text
checkpointSourceReadCount = 1 per lane
sourceBufferOwnerAcquireCount = 1 per lane
sourceBufferOwnerReleaseCount = 1 per lane
sourceBufferOwnerLiveAfterLaneReturn = 0
```

C5 must not return `Vec<u8>` source payload from lane workers.

---

# 13. Decoded f32 owner release

The lane result may contain one decoded `Vec<f32>`.

The sequential material commit must consume it by value.

Required ownership flow:

```text
DecodedRolePayload { values: Vec<f32> }
  -> materialize_role(values)
  -> TensorData::new(values, shape)
  -> Tensor::from_data(...)
  -> private staging material inserted
  -> no decoded Vec owner remains in staging/executor
```

Required counters:

```text
decodedBufferOwnerAcquireCount = 1 per lane
decodedBufferOwnerReleaseCount = 1 per lane
decodedBufferOwnerLiveAfterRoleCommit = 0
```

Again, these are ownership receipts, not allocator/driver physical-free claims.

---

# 14. Host transient ownership ledger

C5 introduces an ownership ledger for source-byte and decoded-f32 host payloads.

Recommended counters:

```text
currentSourceOwnedBytes
currentDecodedOwnedBytes
currentHostTransientOwnedBytes
peakSourceOwnedBytes
peakDecodedOwnedBytes
peakHostTransientOwnedBytes
sourceOwnerAcquireCount
sourceOwnerReleaseCount
decodedOwnerAcquireCount
decodedOwnerReleaseCount
```

Required invariants:

```text
peakHostTransientOwnedBytes <= C4 max_host_transient_bytes
currentSourceOwnedBytes == 0 at every wave boundary
currentDecodedOwnedBytes == 0 at every wave boundary
currentHostTransientOwnedBytes == 0 at every wave boundary
sourceOwnerAcquireCount == 9
sourceOwnerReleaseCount == 9
decodedOwnerAcquireCount == 9
decodedOwnerReleaseCount == 9
```

C5 may report observed ownership peak.

It must not label that value as process RSS or physical system-memory peak.

---

# 15. Material commit order vs final block order

C4 has two distinct orders:

```text
registry ordinal
0 InputLayerNorm
1 Q
2 K
3 V
4 O
5 PostAttentionNorm
6 Gate
7 Up
8 Down

canonical commit ordinal
0 InputLayerNorm
1 PostAttentionNorm
2 Q
3 K
4 V
5 O
6 Gate
7 Up
8 Down
```

The C4 packing plan is generated in registry order.

Therefore C5 must **not** hold decoded Q/K/V host arrays until PostAttentionNorm arrives merely to satisfy global commit ordinal.

C5 defines two explicit orders:

```text
materialIntakeOrder
  = wave ordinal -> lane ordinal

finalBlockExtractionOrder
  = canonical commit ordinal 0..8
```

`materialIntakeOrder` controls when decoded host payload is turned into private device material.

`finalBlockExtractionOrder` controls deterministic extraction of the nine already-materialized device tensors when the complete block is constructed.

These orders must never be aliased.

---

# 16. Sequential module-material commit

Within each wave, role materials are committed sequentially in deterministic lane order after the whole wave decoded successfully.

For every role:

```text
validate staging state == Building
validate target layer
validate plan digest
validate wave/lane identity
validate tensor identity
validate role not previously committed
validate expected rank/shape
consume decoded Vec
create device Tensor material
store exactly one typed material field
seal role material receipt
release decoded owner
```

No two threads may mutate staging materials concurrently.

Parallelism belongs to checkpoint read/decode only.

Private staging mutation is single-writer.

---

# 17. Role material receipt

Each material commit must produce a serializable receipt that does not serialize tensor payload.

Minimum fields:

```text
targetLayer
waveOrdinal
laneOrdinal
role
registryOrdinal
commitOrdinal
tensorKey
tensorIdentityDigest
spanDigest
lanePlanDigest
dtype
shape
elementCount
sourcePayloadBytes
decodedF32Bytes
decodedPayloadDigest
deviceMaterialRank
deviceMaterialShape
sourceOwnerReleased
decodedOwnerReleased
runtimePublicationCount = 0
executionLeaseCount = 0
materialReceiptDigest
```

No raw checkpoint bytes or decoded f32 payload may be embedded in the receipt.

---

# 18. Duplicate-role prevention

The staging slot must reject:

```text
same role committed twice
same tensor identity committed to two roles
same lane committed twice
role from another target layer
role from another plan digest
role not present in the current wave
wave ordinal replay
lane ordinal replay
```

Recommended metadata owners:

```text
BTreeSet<DecoderWeightRole>
BTreeSet<String> tensor identity digests
BTreeSet<(waveOrdinal, laneOrdinal)>
```

No last-writer-wins behavior is allowed.

---

# 19. Wave completion fence

C4 plans one completion fence per payload wave.

C5 executes that contract.

After the last material commit for wave N:

```text
device.poll(wgpu26::PollType::Wait)
```

or the canonical same-device completion primitive must complete before wave N+1 decode begins.

Required wave receipt:

```text
waveOrdinal
laneCount
allLaneDecodeSucceeded
materialCommitCount
sourceOwnerLiveBytesAfterCommit
decodedOwnerLiveBytesAfterCommit
completionFenceWaitCount = 1
completionFenceSatisfied = true
nextWaveDecodeAdmitted = true only after fence
waveExecutionDigest
```

C5 must not claim a GPU fence before a real wait/completion call occurs.

---

# 20. Cross-wave payload overlap

C5 requires:

```text
crossWaveHostPayloadOverlapCount = 0
```

Before the next wave begins:

```text
source host owners from previous wave = 0
decoded host owners from previous wave = 0
previous wave fence = satisfied
```

Private device materials from previous waves remain in the staging slot. They are not counted as host payload overlap.

C5 does not yet claim physical VRAM non-overlap because the staged device materials intentionally accumulate until the complete block is assembled.

---

# 21. No mega atlas

C5 must not allocate or construct a monolithic decoder-weight mega-atlas.

Required:

```text
megaAtlasCreateCount = 0
megaAtlasByteCount = 0
```

The staging slot contains independently typed role materials, not one concatenated weight buffer.

---

# 22. Complete nine-role seal

After all planned waves complete, staging may transition:

```text
Building -> CompleteNineRoles
```

only when all of the following are true:

```text
committed role count = 9
role set == exact DecoderWeightRole registry
registry ordinal coverage = 0..8
commit ordinal coverage = 0..8
wave execution count == plan.wave_count
lane execution count == 9
all planned lane digests consumed exactly once
all tensor identity digests match C4 plan
all material shapes match role contracts
host source owners = 0
host decoded owners = 0
cross-wave overlap count = 0
mega-atlas count = 0
runtime publication count = 0
```

The complete seal must produce:

```text
completeRoleSetDigest
materialReceiptSetDigest
waveExecutionSetDigest
stagingCompleteDigest
```

No tensor payload is serialized into those digests.

---

# 23. SealedComplete transition

`CompleteNineRoles` is structural completeness.

`SealedComplete` additionally requires:

```text
C4 plan digest revalidated
checkpoint-set digest revalidated
target layer revalidated
canonical extraction order revalidated
no runtime weight mutation observed
no hidden mutation observed
no active staging mutation in progress
```

Only `SealedComplete` may be consumed for final block construction.

---

# 24. Complete material extraction

The staging slot must expose no individual material getters.

Forbidden:

```text
get_q_proj()
get_input_norm()
borrow_partial_materials()
clone_partial_materials()
```

The only payload-producing extraction API is a consuming operation on a sealed-complete slot:

```rust
consume_complete_materials(self) -> Result<CompleteDecoderWeightMaterials>
```

or equivalent.

The call must:

```text
require state == SealedComplete
move all nine device materials out exactly once
transition staging identity to Consumed
leave no reusable material owner behind
```

---

# 25. CompleteDecoderWeightMaterials

The complete material carrier is private construction input, not runtime authority.

Recommended shape:

```rust
pub struct CompleteDecoderWeightMaterials {
    pub selected_layer: u32,
    pub input_norm: Tensor<InferenceBackend, 1>,
    pub post_attn_norm: Tensor<InferenceBackend, 1>,
    pub q_proj: Tensor<InferenceBackend, 2>,
    pub k_proj: Tensor<InferenceBackend, 2>,
    pub v_proj: Tensor<InferenceBackend, 2>,
    pub o_proj: Tensor<InferenceBackend, 2>,
    pub gate_proj: Tensor<InferenceBackend, 2>,
    pub up_proj: Tensor<InferenceBackend, 2>,
    pub down_proj: Tensor<InferenceBackend, 2>,
    pub hidden_size: usize,
    pub intermediate_size: usize,
    pub num_heads: usize,
    pub num_kv_heads: usize,
    pub head_dim: usize,
    pub norm_eps: f64,
    pub checkpoint_tensor_set_digest: String,
    pub tensor_identity_digests: Vec<String>,
    pub staging_complete_digest: String,
}
```

Exact module/type naming may differ.

It must contain device materials, not nine decoded host vectors.

---

# 26. Model-core construction boundary

`AshLinear::from_checkpoint_tensor()` and `AshRmsNorm::from_checkpoint_tensor()` are currently `pub(crate)` inside `model_core`.

C5 must preserve dependency direction rather than duplicating internal model construction logic in `base_train`.

Recommended model-core surface:

```rust
pub fn build_r6_r9_actual_decoder_block_from_materials(
    materials: CompleteDecoderWeightMaterials,
) -> Result<R6R6ActualDecoderBlockBundle>
```

or an equivalent model-core-owned constructor.

The constructor must wrap already-device-resident tensors into the exact existing module types.

It must not re-upload checkpoint payload from host `Vec<f32>`.

---

# 27. Atomic decoder block construction

From runtime authority perspective, block construction is atomic:

```text
partial staging materials
  NOT A BLOCK

complete sealed staging materials
  -> consume all nine
  -> construct one AshDecoderBlock
  -> construct one R6R6ActualDecoderBlockBundle
```

There is never a publicly reachable:

```text
AshDecoderBlock with 3/9 weights
AshDecoderBlock with missing projection
R6R6ActualDecoderBlockBundle with partial modules
```

A complete bundle may exist privately only after the nine-role seal.

---

# 28. Existing bundle contract preservation

The private C5-built candidate must preserve the existing `R6R6ActualDecoderBlockBundle` contract:

```text
actual_decoder_block_instance_count = 1
linear_module_count = 7
norm_module_count = 2
runtime_lora_set_count = 1
trainable_lora_slot_count = 0
checkpoint_weight_upload_count = 9
selected_layer = target layer
checkpoint_tensor_set_digest = parent checkpoint digest
```

`runtime_loras` remains the existing empty prepared runtime-LoRA set for this BaseTrain route unless a separate SSOT changes it.

C5 must not silently invent a new LoRA binding path.

---

# 29. Block identity

The C5 private candidate must generate the same structural module identity contract as the legacy builder for the same:

```text
checkpoint set
target layer
hidden size
intermediate size
attention head count
KV head count
head dim
norm epsilon
7 linear modules
2 norm modules
```

If the existing `module_identity_digest` formula is retained, C5 must reuse it rather than define a second incompatible identity formula.

Equality of structural module identity does **not** by itself prove numerical weight parity.

Numerical execution parity remains C7.

---

# 30. C5 private candidate policy

For the first C5 physical gate, the private build target remains the C4 fixture target:

```text
target layer = 2
```

The parent runtime may already have Layer 2 resident from C3/C4.

C5 may construct a second **private candidate resource set** for the same layer only for this staging gate, but it must never become a second runtime authority.

Required distinctions:

```text
privateStagingSlotCount = 1
privateCompleteBlockCandidateCount <= 1
runtimePublishedBlockCount = 0
runtimeWeightAuthorityCreatedCount = 0
runtimeExecutionLeaseCreatedCount = 0
```

The private candidate must be dropped after its receipt is sealed.

C5 must not retain it for next-layer prefetch.

---

# 31. No second runtime weight authority

The following must remain exact before and after the C5 private canary:

```text
BaseTrainLayerWeightResidencySlot pointer digest
resident layer index
residency generation
transition serial
resident decoder block count
resident checkpoint weight tensor count
active execution lease count
```

C5 must capture runtime weight snapshots before and after private staging and require equality.

The staging slot may own device weight materials, but it must report:

```text
runtimeWeightAuthorityCount = 0
runtimePublicationCount = 0
executionLeaseCount = 0
```

Private resource ownership is not runtime authority ownership.

---

# 32. Hidden authority immutability

C5 must also snapshot and revalidate hidden authority.

Required equality before/after:

```text
hidden pointer digest
hidden layer index
hidden generation
hidden transition serial
hidden buffer identity
hidden active lease count
```

C5 performs no forward execution.

---

# 33. No partial runtime exposure

No staging state below `SealedComplete` may cross into:

```text
BaseTrainLayerWeightResidencySlot
R6-R8 layer executor
Headwise attention
QKV projection
OProj
FFN
runtime LoRA binding
hidden authority
```

C5 must not add an overload that accepts staging materials in `execute_resident_decoder_layer_from_session()`.

The runtime executor continues to accept only an execution lease from the canonical runtime weight slot.

---

# 34. Failure classes

C5 distinguishes at least:

```text
PlanBindingFailure
CheckpointReadFailure
CheckpointDecodeFailure
DecodeNonFiniteFailure
WaveJoinFailure
MaterialShapeFailure
MaterialCommitFailure
WaveFenceFailure
DuplicateRoleFailure
CompleteSealFailure
AtomicBlockConstructionFailure
RuntimeAuthorityMutationDetected
```

All C5 private-canary failures fail closed.

No synthetic tensor fallback is allowed.

---

# 35. Staging abort behavior

On any C5 private staging failure:

```text
staging state -> Aborted
all private staged materials -> dropped
private complete block candidate -> absent or dropped
runtime weight slot -> unchanged
hidden authority -> unchanged
```

The staging slot must not be reset and retried in place.

A retry requires a new operation ID and new staging slot.

---

# 36. RecoveryRequired boundary

The runtime `RecoveryRequired` state belongs to `BaseTrainLayerWeightResidencySlot`, not the private staging slot.

The exact escalation boundary is:

```text
before runtime slot reaches VacantForRebind
  -> staging failure = private abort
  -> runtime RecoveryRequired transition FORBIDDEN

runtime slot is VacantForRebind and source bundle has been destructively removed
  -> target build/adoption failure = mark_recovery_required REQUIRED
```

C5 private canary executes on the **pre-vacancy side** of this boundary.

Therefore C5 expected runtime counters are:

```text
recoveryRequiredTransitionCount = 0
runtimeWeightMutationCount = 0
```

C5 must nevertheless publish the boundary contract so C6 cannot silently choose a different failure policy.

---

# 37. Future C6 integration contract

C6 may reuse the C5 staging executor inside the destructive R6-R7 rebind transaction.

When C6 does so:

```text
arm eviction
-> take source bundle
-> poll completion
-> mark VacantForRebind
-> execute C5 wave staging build
-> complete nine-role seal
-> atomic block construction
-> adopt complete block
```

If any C5 build step fails after `VacantForRebind`, C6 must invoke:

```text
BaseTrainLayerWeightResidencySlot::mark_recovery_required()
```

No fallback to the old full-layer loader is allowed in the same destructive transaction.

C5 itself does not wire this adoption.

---

# 38. No silent fallback

C5 forbids:

```text
wave lane failure -> load whole layer with legacy loader
material commit failure -> rebuild all nine Vec<f32>
complete seal failure -> skip missing role
block construction failure -> random-initialize missing module
fence failure -> continue next wave
runtime mutation detected -> ignore and continue
```

The old full-layer loader remains active only because C5 has not yet been adopted into the runtime route.

It is not a failure fallback for a C5 operation.

---

# 39. No next-layer prefetch

C5 private canary is not a prefetch feature.

Forbidden:

```text
keep Layer-3 staging alive while Layer-2 runs
cache next staging slot
background future-layer decode
parallel layer N and N+1 staging
```

The private Layer-2 canary slot is dropped at the end of C5.

Prefetch remains zero.

---

# 40. No all-layer residency

C5 must not create staging slots for all checkpoint layers.

Required:

```text
activeLayerWeightBuildStagingSlotCount <= 1
activeTargetLayerCount <= 1
```

The C5 canary is one layer, one plan, one staging slot.

---

# 41. No payload readback

C5 reads checkpoint payload from disk to host and uploads material to the GPU.

It must not read GPU weight payload back to host.

Required distinction:

```text
checkpointPayloadReadCount = 9
GPUWeightPayloadReadbackCount = 0
```

The generic word `payload_readback` in terminal output must continue to mean GPU/product readback, not checkpoint file input.

---

# 42. No checkpoint mutation

C5 is read-only with respect to checkpoint files and tensor metadata.

Required:

```text
checkpointMutationCount = 0
weightFileWriteCount = 0
checkpointMetadataMutationCount = 0
```

---

# 43. Wave execution evidence

Recommended per-wave typed receipt:

```rust
pub struct LayerWeightBuildWaveExecutionReceipt {
    pub wave_ordinal: u32,
    pub wave_plan_digest: String,
    pub lane_count: u32,
    pub lane_execution_digests: Vec<String>,
    pub source_read_count: u32,
    pub decode_count: u32,
    pub material_commit_count: u32,
    pub source_owner_release_count: u32,
    pub decoded_owner_release_count: u32,
    pub host_source_owned_bytes_after_wave: u64,
    pub host_decoded_owned_bytes_after_wave: u64,
    pub completion_fence_wait_count: u32,
    pub completion_fence_satisfied: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Exact names may vary.

---

# 44. Staging receipt

Recommended top-level typed receipt:

```rust
pub struct LayerWeightBuildStagingReceipt {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,
    pub target_layer: u32,
    pub checkpoint_set_digest: String,
    pub c4_plan_digest: String,
    pub wave_count: u32,
    pub lane_count: u32,
    pub role_count: u32,
    pub role_material_receipt_digests: Vec<String>,
    pub wave_execution_receipt_digests: Vec<String>,
    pub complete_role_set_digest: String,
    pub staging_complete_digest: String,
    pub observed_peak_host_transient_owned_bytes: u64,
    pub source_owner_acquire_count: u32,
    pub source_owner_release_count: u32,
    pub decoded_owner_acquire_count: u32,
    pub decoded_owner_release_count: u32,
    pub material_commit_count: u32,
    pub completion_fence_wait_count: u32,
    pub runtime_publication_count: u32,
    pub runtime_weight_authority_count: u32,
    pub execution_lease_count: u32,
    pub cross_wave_payload_overlap_count: u32,
    pub mega_atlas_create_count: u32,
    pub gpu_weight_payload_readback_count: u32,
    pub final_state: LayerWeightBuildStagingState,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 45. Private block candidate receipt

The final C5 private candidate construction receipt must bind:

```text
stagingCompleteDigest
C4 plan digest
checkpoint-set digest
target layer
nine tensor identity digests
actual decoder block receipt digest
module identity digest
private candidate count = 1
runtime publish count = 0
runtime authority count = 0
candidate dropped after receipt = true
```

The candidate receipt must not imply runtime adoption.

---

# 46. Artifact receipt wave isolation

C5 proof artifacts remain serialized through:

```text
ArtifactReceiptParallelStreamingWaveMap
```

C5 decoder-weight payload waves are not artifact receipt waves.

Recommended artifact receipt sections:

```text
artifact wave 0 identity-and-parent
artifact wave 1 plan-and-staging-identity
artifact wave 2 host-ownership-ledger
artifact wave 3 payload-wave-execution-summary
artifact wave 4 nine-role-complete-seal
artifact wave 5 private-block-candidate
artifact wave 6 runtime-authority-immutability-and-recovery-boundary
```

No payload tensor content is serialized.

---

# 47. Digest hierarchy

Required independent digests:

```text
C4 planDigest
C4 planWaveCollectionDigest
laneExecutionDigest per lane
roleMaterialReceiptDigest per role
waveExecutionDigest per payload wave
completeRoleSetDigest
stagingCompleteDigest
privateBlockCandidateReceiptDigest
C5 finalReceiptDigest
ArtifactReceiptWaveMapDigest
```

No one digest may be renamed and reused as another authority.

---

# 48. Deterministic lane-result merge

Parallel decode completion order is nondeterministic.

C5 must not use thread completion order as semantic order.

After joining one wave:

```text
sort by lane ordinal
validate exact expected lane ordinal set
then sequentially material-commit
```

Duplicate/missing lane ordinals fail closed.

---

# 49. Deterministic failure aggregation

If multiple decode lanes fail, C5 must produce deterministic failure selection.

Recommended rule:

```text
collect lane failures
sort by lane ordinal
report lowest failing lane as primary error
bind all failing lane ordinals into failure receipt
```

Thread scheduling order must not change the primary failure identity.

---

# 50. Role-shape materialization contract

Device material rank/shape must match C4 role shape.

Required:

```text
InputLayerNorm          Tensor rank 1 [H]
PostAttentionLayerNorm  Tensor rank 1 [H]
QProj                   Tensor rank 2 [QD, H]
KProj                   Tensor rank 2 [KVD, H]
VProj                   Tensor rank 2 [KVD, H]
OProj                   Tensor rank 2 [H, QD]
GateProj                Tensor rank 2 [I, H]
UpProj                  Tensor rank 2 [I, H]
DownProj                Tensor rank 2 [H, I]
```

No transpose is silently inserted unless the existing checkpoint/model contract explicitly requires it.

---

# 51. Query projection dimension honesty

C4 correctly derives:

```text
QD = num_attention_heads * head_dim
KVD = num_key_value_heads * head_dim
```

C5 must preserve those dimensions.

It must not silently replace `QD` with `hidden_size` solely because the current fixture happens to make them equal.

---

# 52. Device lineage

All staged materials must be created on the same canonical Burn/WGPU device lineage as the parent runtime session.

Required identity binding:

```text
same process
same WGPU device
same queue lineage
same Burn device
```

C5 must not create a second WGPU device merely for staging.

---

# 53. Staging material publication prohibition

Private materials must not be stored in global/static registries.

Forbidden:

```text
lazy_static staging tensor registry
global Arc material map
cross-session staging cache
checkpoint-layer material cache
```

Staging lifetime is one C5 operation.

---

# 54. Runtime slot strong ownership

C5 must not alter the `Arc` strong-owner contract inside `BaseTrainLayerWeightResidencySlot`.

The runtime resident bundle remains owned exactly as before.

The private C5 candidate is not inserted into that `Arc` and must not affect `slot_owned_strong_reference_count`.

---

# 55. Atomic candidate construction failure

If complete material extraction succeeds but final `R6R6ActualDecoderBlockBundle` construction fails:

```text
private materials are consumed/dropped
staging is terminal
runtime weight slot remains unchanged
hidden authority remains unchanged
no partial block is published
```

The operation fails.

There is no fallback reconstruction through the full-layer loader inside the same C5 operation.

---

# 56. C5 physical canary ordering

Recommended same-process gate ordering:

```text
1. execute admitted C3/C4-D1 parent
2. capture runtime weight pointer/counts
3. capture hidden pointer/counts
4. re-run/validate C4 plan for Layer 2
5. create fresh private LayerWeightBuildStagingSlot
6. execute C4 wave 0
7. execute C4 wave 1
8. execute C4 wave 2
9. complete nine-role seal
10. seal staging complete
11. consume staging into complete materials
12. construct one private decoder block candidate
13. seal private candidate receipt
14. drop private candidate
15. poll completion as needed
16. recapture runtime weight pointer/counts
17. recapture hidden pointer/counts
18. require exact runtime authority equality
19. emit C5 final receipt and PASS token
```

---

# 57. C5 must not re-run forward

C5 does not need to execute the private candidate through Layer 2.

Forward numerical parity belongs to C7.

Required:

```text
privateCandidateForwardCount = 0
privateCandidateHiddenCommitCount = 0
```

This keeps C5 focused on construction authority and lifetime closure.

---

# 58. C5 terminal line

Recommended physical terminal line:

```text
[r6-r9-c5-layer-weight-build-staging]
target_layer=2
plan_waves=3
lanes=9
roles=9
checkpoint_reads=9
decodes=9
material_commits=9
source_owner_release=9
decoded_owner_release=9
peak_host_owned=<observed>
wave_fence_waits=3
complete_nine_role_seal=1
private_block_candidate=1
private_candidate_forward=0
runtime_publish=0
runtime_weight_authority=0
runtime_weight_pointer_unchanged=1
hidden_pointer_unchanged=1
recovery_required_transition=0
cross_wave_overlap=0
mega_atlas=0
gpu_weight_readback=0
staging_digest=<digest>
candidate_digest=<digest>
proof_ledger=HOLD
```

---

# 59. PASS token

Recommended:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C5_LAYER_WEIGHT_BUILD_STAGING_SLOT_C4_D1_PHYSICAL_PARENT_PRIVATE_INCOMPLETE_BLOCK_AUTHORITY_C4_THREE_WAVE_NINE_LANE_PLAN_BOUND_PARALLEL_WAVE_DECODE_RESULT_INTAKE_SINGLE_WRITER_SEQUENTIAL_DEVICE_MATERIAL_COMMIT_PER_ROLE_SOURCE_BUFFER_OWNER_RELEASE_PER_ROLE_DECODED_BUFFER_OWNER_RELEASE_HOST_TRANSIENT_OWNERSHIP_LEDGER_WITHIN_C4_BUDGET_PER_WAVE_COMPLETION_FENCE_EXACT_NINE_ROLE_COMPLETE_SEAL_CANONICAL_FINAL_BLOCK_EXTRACTION_ORDER_ATOMIC_PRIVATE_DECODER_BLOCK_CONSTRUCTION_NO_PARTIAL_BLOCK_RUNTIME_EXPOSURE_NO_SECOND_RUNTIME_WEIGHT_AUTHORITY_NO_RUNTIME_PUBLICATION_RUNTIME_WEIGHT_POINTER_UNCHANGED_HIDDEN_POINTER_UNCHANGED_PRE_VACANCY_FAILURE_PRIVATE_ABORT_POST_VACANCY_FAILURE_RECOVERY_REQUIRED_BOUNDARY_SEALED_NO_MEGA_ATLAS_ZERO_CROSS_WAVE_PAYLOAD_OVERLAP_ZERO_GPU_WEIGHT_READBACK_CANONICAL_RUNTIME_LOADER_REMAINS_CHECKPOINT_RESOLVED_FULL_LAYER_LOADER_WAVE_REBIND_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

This PASS token admits the private staging/build boundary only.

---

# 60. CLI policy

Recommended additions:

```text
--require-r6-r9-c5-layer-weight-build-staging true
--r6-r9-c5-staging-target-layer 2
--require-r6-r9-c5-private-staging-authority true
--require-r6-r9-c5-wave-decode-execution true
--require-r6-r9-c5-sequential-material-commit true
--require-r6-r9-c5-per-role-source-owner-release true
--require-r6-r9-c5-per-role-decoded-owner-release true
--require-r6-r9-c5-complete-nine-role-seal true
--require-r6-r9-c5-atomic-private-block-construction true
--allow-r6-r9-c5-runtime-publication false
--allow-r6-r9-c5-runtime-weight-authority false
--allow-r6-r9-c5-private-candidate-forward false
--allow-r6-r9-c5-partial-block-exposure false
--allow-r6-r9-c5-mega-atlas false
--allow-r6-r9-c5-cross-wave-payload-overlap false
--allow-r6-r9-c5-silent-full-layer-fallback false
```

The C4 byte-budget/worker/lane flags remain authoritative and are reused rather than duplicated.

---

# 61. Expected implementation files

Recommended new base-train staging implementation:

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r9_c5_layer_weight_build_staging.rs
```

Recommended shared checkpoint decode helper extraction if required:

```text
crates/base_train/src/base_train_atlas_wave_02_r6_checkpoint_tensor_decode.rs
```

Existing full-layer loader may be refactored to call the same helper without changing its external behavior:

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
```

Base-train exports:

```text
crates/base_train/src/lib.rs
```

Model-core complete-material constructor:

```text
crates/model_core/src/actual_decoder_block_split_forward.rs
crates/model_core/src/lib.rs
```

Coordinator/gate:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_forward_coordinator.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs
```

CLI:

```text
specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args
```

---

# 62. Explicitly unchanged runtime files

C5 must not semantically alter the active adoption state machine in:

```text
crates/model_core/src/base_train_layer_weight_residency_authority.rs
```

unless a compile-only shared type import is required.

C5 must not rebind the active R6-R7 loader call in:

```text
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r7_layer_weight_residency.rs
```

Canonical wave rebind is C6/C8 work.

---

# 63. WGSL boundary

C5 introduces no new WGSL algorithm.

Required:

```text
WGSL semantic changed file count = 0
```

Checkpoint decode and material staging are Rust/Burn/WGPU host-side construction work.

---

# 64. Static compile-surface requirements

Required checks before physical run:

```text
LayerWeightBuildStagingState = present
LayerWeightBuildStagingSlot = present
private material storage contains no Vec<f32> fields = true
private material storage contains no Vec<u8> fields = true
C4 plan digest binding = present
C4 lane plan digest binding = present
single-writer staging material commit = present
parallel decode workers bounded by C4 policy = present
wave join before material commit = present
lane results sorted by lane ordinal = present
per-wave fence wait = present
host ownership ledger = present
complete nine-role seal = present
consuming complete-material extraction = present
partial material getters = absent
runtime execution lease API on staging = absent
runtime adoption API on staging = absent
private candidate forward = absent
same-device material creation = present
shared checkpoint decode helper = present or existing decode SSOT reused
second dtype decoder = absent
silent full-layer fallback = absent
mega-atlas creation = absent
cross-wave payload overlap = forbidden
GPU weight readback = absent
```

---

# 65. Runtime authority static audit

C5 code must contain no call from the private staging canary to:

```text
BaseTrainLayerWeightResidencySlot::arm_eviction
BaseTrainLayerWeightResidencySlot::take_armed_bundle
BaseTrainLayerWeightResidencySlot::mark_vacant
BaseTrainLayerWeightResidencySlot::adopt
BaseTrainLayerWeightResidencySlot::mark_recovery_required
```

Those calls remain runtime transaction authority.

C5 only documents the future post-vacancy recovery boundary.

---

# 66. C5 physical PASS requirements

For the current Layer-2 fixture, physical PASS requires:

```text
parent C4-D1 = PASS
C4 target layer = 2
C4 plan waves = 3
C4 lanes = 9
C4 roles = 9
staging slots created = 1
checkpoint source reads = 9
decodes = 9
nonfinite decoded values = 0
material commits = 9
source owner releases = 9
decoded owner releases = 9
observed peak host-owned transient <= 268435456
wave fence waits = 3
wave fence failures = 0
cross-wave host payload overlap = 0
mega-atlas create = 0
complete role seal = 1
private complete block candidate = 1
private candidate forward = 0
runtime publication = 0
runtime weight authority creation = 0
runtime execution lease creation = 0
runtime weight pointer/counts before == after
hidden pointer/counts before == after
recovery-required transition = 0
GPU weight payload readback = 0
checkpoint mutation = 0
```

---

# 67. What C5 PASS proves

C5 PASS proves:

```text
real checkpoint payload can be consumed according to the C4 plan
parallel wave decode works under the private build boundary
host source/decoded ownership is released per role
staged device materials accumulate without partial runtime publication
all nine exact roles can be sealed
one complete private decoder block can be constructed atomically
runtime weight and hidden authorities remain unchanged
pre-vacancy failure policy is private abort
post-vacancy recovery escalation boundary is explicitly fixed for C6
```

---

# 68. What C5 PASS does not prove

C5 PASS does **not** prove:

```text
wave-built block forward numerical parity
Layer-2 hidden output parity
wave-built block canonical runtime adoption
source Layer-1 eviction + wave Layer-2 adoption transaction
post-vacancy recovery path physically exercised
performance improvement
physical process RSS reduction
physical VRAM reduction
all 22 layers progressive execution
final norm / LM head
forward loss
backward
optimizer
production inference
```

Those remain later gates.

---

# 69. Admission matrix after C5 PASS

```text
R6-R6 live body                              = ADMITTED
R6-R7 layer-weight residency                 = ADMITTED
R6-R8 layer-1 forward                        = ADMITTED
R6-R9-C1 Layer-2 single-step                 = ADMITTED
R6-R9-C2 coordinator evidence truth          = ADMITTED
R6-R9-C3 wave-domain split                   = ADMITTED
R6-R9-C4 decoder-weight wave planner         = ADMITTED_PLANNER_ONLY
R6-R9-C4-D1 root collection closure          = ADMITTED
R6-R9-C5 private staging/build               = ADMITTED_PRIVATE_CANDIDATE on PASS

DecoderWeightAtlasWave planning              = ADMITTED
DecoderWeightAtlasWave private payload build = ADMITTED_CANDIDATE on PASS
DecoderWeightAtlasWave runtime transport     = BLOCKED
Layer-2 wave rebind canary                    = BLOCKED / C6
wave-loader execution parity                 = BLOCKED / C7
canonical wave-loader adoption               = BLOCKED / C8
progressive N-layer promotion                = BLOCKED / C9
full N-layer execution                       = BLOCKED
final RMSNorm / LM head                      = BLOCKED
forward loss                                 = BLOCKED
backward                                     = BLOCKED
optimizer                                    = BLOCKED
production inference                         = BLOCKED
proof ledger                                 = HOLD
```

---

# 70. Next boundary

After C5 physical PASS:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C6

Layer-2 Decoder Weight Wave Rebind Canary /
Source Layer-1 Execution Completion Binding /
Destructive Weight-1 Eviction /
VacantForRebind Boundary /
C4 Plan-Bound C5 Staging Execution /
Nine-Role Atomic Block Adoption /
Weight Generation 1 -> 2 /
Failure -> RecoveryRequired /
No Legacy Full-Layer Fallback /
No Parallel Runtime Weight Authority Seal
```

C6 is the first patch allowed to insert the C5-built block into `BaseTrainLayerWeightResidencySlot` as the canonical runtime weight authority for the target layer.

---

# 71. Architecture seal

> C5 creates one private, single-use staging authority between checkpoint payload and runtime block authority. Decoder-weight wave lanes may decode in parallel, but staging mutation remains single-writer; each decoded payload is immediately converted into typed device material and its host ownership is released; only an exact nine-role sealed set may be consumed to construct one private complete decoder block; and nothing incomplete or complete from C5 becomes runtime weight authority until C6 crosses the explicit `VacantForRebind -> adopt / RecoveryRequired` transaction boundary.
