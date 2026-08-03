# ASH-BASETRAIN-ATLAS-WAVE-01

## Native Runtime Borrowed Device·Queue Authority /
## Checkpoint Safetensors Atlas Residency /
## Triple-Ring Slot Ownership /
## Transaction-Digest Runtime Binding /
## Same-Device Generation Fence /
## No Secondary Adapter·Device Creation /
## No Host Full-Tensor Materialization /
## No Forward Execution Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-01`  
> Build revision: `ATLAS-WAVE-01-borrowed-runtime-atlas-residency-v1`  
> Direct parent: `ASH-BASETRAIN-ATLAS-WAVE-00`  
> Parent state: `PASS_ASH_BASETRAIN_ATLAS_WAVE_00_..._PREPARED_ONLY_..._SEALED`  
> Physical lineage parent: `ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01`  
> Implementation SSOT: attached `ASH-BASETRAIN-ATLAS-WAVE-00-R1` body  
> Existing runtime handle authority: `burn_webgpu_backend::NativeWgpuRuntimeHandles`  
> Step transaction state ceiling: `Prepared` unchanged  
> GPU mutation authority: borrowed-device buffer allocation, bounded checkpoint-range upload, bounded upload verification only  
> Forward, loss, backward, optimizer, delta, apply, commit authority: none

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-01` binds one already sealed AW-00 training-step transaction to the exact native WGPU device and queue already owned by the live ASH runtime, validates the checkpoint Safetensors topology against the AW-00 model-source authority, and establishes a physically uploaded three-slot Atlas residency ring.

This patch does not execute a model layer.

Its job is narrower and more structural:

```text
AW-00 prepared transaction
  -> borrow existing NativeWgpuRuntimeHandles
  -> bind parent transaction digest to runtime holder identity
  -> stream-verify checkpoint identity and Safetensors header
  -> join tensor-group manifest + atlas-group plan + sequential-load plan
  -> allocate exactly three same-device Atlas slot arenas
  -> read exact bounded checkpoint byte ranges
  -> upload raw slice bytes through the borrowed queue
  -> verify upload visibility with bounded readback
  -> seal slot ownership and residency generation
  -> publish AW-02 residency handoff
  -> stop before bind group, pipeline, shader, or forward dispatch
```

AW-01 is the point where the Atlas route first owns real checkpoint bytes on the actual runtime GPU.

It is not the point where those bytes may influence attention output.

---

# 1. Source-grounded problem statement

## 1.1 AW-00 already reserves the binding fields but does not bind them

Current source:

```text
crates/model_core/src/base_train_atlas_wave_generation_fence.rs
```

The AW-00 fence already contains:

```rust
pub atlas_residency_generation: Option<u64>,
pub runtime_binding_state: BaseTrainRuntimeBindingState,
pub device_epoch: Option<u64>,
pub queue_epoch: Option<u64>,
```

AW-00 correctly seals these as:

```text
runtime_binding_state       UnboundPrepared
atlas_residency_generation  None
device_epoch                None
queue_epoch                 None
```

No production function currently derives a same-device bound child fence from this parent.

AW-01 must add that operation without mutating or replacing the AW-00 parent transaction receipt.

## 1.2 The correct native runtime handle authority already exists

Current source:

```text
crates/burn_webgpu_backend/src/device_handles.rs
```

Existing public authority:

```rust
pub struct NativeWgpuRuntimeHandles {
    pub device: Arc<RuntimeWgpuDevice>,
    pub queue: Arc<RuntimeWgpuQueue>,
    pub source: &'static str,
}
```

The raw-access path resolves Burn and raw WGPU access to the same concrete WGPU 26 device and queue types.

Existing extraction:

```rust
try_extract_runtime_handles(device: &WgpuDevice)
try_build_same_device_raw_bridge(device: &WgpuDevice)
supports_same_device_raw_bridge(device: &WgpuDevice)
```

AW-01 must borrow this authority. It must not create an adjacent runtime.

## 1.3 G202D proves handle identity but is not an Atlas residency owner

Current source:

```text
crates/burn_webgpu_backend/src/base_train_g202d_shared_runtime_probe.rs
```

G202D records:

```text
runtime_holder_id
device_identity_digest
queue_identity_digest
same_device_handle
same_queue_handle
```

Its identity derives from the exact `Arc` pointers held by `NativeWgpuRuntimeHandles`.

This is valid parent evidence for AW-01 runtime provenance. It does not own Atlas buffers, checkpoint ranges, triple-ring slots, or a live BaseTrain transaction.

AW-01 may reuse its pointer-identity convention. It must not relabel the G202D probe receipt as a live residency coordinator.

## 1.4 G39 is physically useful evidence but creates a secondary device

Current source:

```text
crates/base_train/src/ash_basetrain_gpu_39_atlas_upload_ring_buffer_slot_lease_release.rs
```

The existing implementation executes:

```rust
let instance = wgpu::Instance::default();
instance.request_adapter(...)
adapter.request_device(...)
```

It then creates buffers, uploads a bounded row block, dispatches a matvec, and reads output back.

This proves an isolated upload-ring experiment. It violates AW-01 runtime authority because it creates a new instance, adapter, device, and queue outside the live ASH runtime.

The following G39 concepts may be adopted semantically:

```text
slot lease
release-before-reuse
bounded file-range read
payload digest
physical upload visibility
```

The following G39 runtime path is forbidden in AW-01:

```text
wgpu::Instance creation
request_adapter
request_device
standalone queue
forward matvec dispatch
```

## 1.5 G49 validates selected-group metadata but performs no residency upload

Current source:

```text
crates/base_train/src/ash_basetrain_gpu_70k_g49_selected_atlas_group_materialization.rs
```

G49 validates the presence of:

```text
tensor-group manifest
atlas-group plan
sequential-load plan
selected group ID
tensor keys
byte-range metadata
dtype and shape metadata
```

Its canonical receipt deliberately keeps these counters false:

```text
full_safetensors_payload_read
gpu_weight_uploaded
gpu_buffer_written
gpu_dispatch_executed
model_forward_executed
```

AW-01 must consume the same metadata classes but replace the evidence-only candidate with a typed, live, same-device residency owner.

## 1.6 G104 claims train-spine rebind through receipts, not live handles

Current source:

```text
crates/base_train/src/ash_basetrain_gpu_70k_g104_r2_b_atlas_upload_ring_rebind_to_train_spine.rs
```

G104 reads G39/G40 evidence and opens booleans such as:

```text
atlas_upload_ring_rebound_to_train_spine
parallel_sequential_upload_lifecycle_verified
slot_lease_release_lifecycle_verified
train_upload_spine_ready
```

It does not hold:

```text
NativeWgpuRuntimeHandles
wgpu::Buffer ownership
live slot leases
checkpoint slice addresses
AW-00 transaction digest
runtime holder identity
```

AW-01 must not consume a boolean rebind claim as physical authority. It must own the live objects and emit receipts from those objects.

---

# 2. Scope

## 2.1 In scope

```text
AW-00 transaction digest consumption
Immutable parent transaction preservation
Borrowed native device and queue binding
Runtime holder, device, and queue identity receipts
Device epoch and queue epoch binding
Checkpoint full-file streaming digest verification
Safetensors header-only topology parsing
Tensor-group manifest exact digest verification
Atlas-group plan exact digest verification
Sequential-load plan exact digest verification
Manifest-to-header tensor-key join
Exact tensor payload byte-range validation
Bounded reusable host byte staging
Raw checkpoint byte upload without typed full-tensor construction
Exactly three Atlas residency slots
Slot arena allocation and deterministic address mapping
Slot lease, fill, resident-ready, retire, and reuse lifecycle
Upload submission ordering
Bounded upload readback parity
Residency generation sealing
Same-device generation fence child receipt
AW-02 residency handoff receipt
Rust-generated runtime artifacts and manifest
Static no-secondary-device source checks
No-forward physical gate
```

## 2.2 Out of scope

```text
New WGPU instance creation
New adapter request
New device request
New queue creation
Device-loss recovery or replacement device creation
Checkpoint mutation
Safetensors rewrite or finalization
Full checkpoint payload retention in host memory
Typed full-tensor Vec<f32>, Vec<f16>, or ndarray materialization
Burn tensor reconstruction from checkpoint weights
Bind group creation
Pipeline creation
Shader module creation
Compute or render dispatch
Embedding lookup
RMSNorm
Q, K, or V projection
RoPE execution
Headwise attention
TensorCube Stage10, Stage11, or Stage12
Residual or MLP execution
Logits or loss
Backward
Gradient accumulation
Optimizer state creation or write
G206D delta consumption
Inactive weight application
Resident weight mutation
Pointer swap
Training cursor mutation
Decode route mutation
Quality or convergence claim
```

AW-01 PASS means the real checkpoint can be moved through a bounded same-device Atlas residency wave under one sealed transaction.

It does not mean a model forward has executed.

---

# 3. Authority and dependency map

## 3.1 Canonical owners

| State or contract | Canonical owner | Allowed mutation | Forbidden owner |
|---|---|---|---|
| AW-00 parent transaction schema | `model_core` | none | backend, gate |
| AW-01 pure receipt schemas | `model_core` | seal/validate only | backend-local GPU code |
| Native device/queue handles | `burn_webgpu_backend` | existing runtime only | `base_train`, gate |
| Backend buffer/upload ABI | `burn_webgpu_backend` | borrowed handles only | `model_core` imports into backend |
| Live residency coordinator | `base_train` | slot lifecycle only | `orchestrator_local` |
| Checkpoint range reader | `base_train` | bounded staging buffer only | model layers |
| Slot writer lease | `base_train` coordinator | one slot owner at a time | backend/gate |
| Verification artifacts | `orchestrator_local` | evidence writes only | live runtime owner |

Required dependency direction:

```text
burn_webgpu_backend
        ^
        |
model_core
        ^
        |
base_train
        ^
        |
orchestrator_local
```

The backend module introduced by AW-01 must use backend-local input and output structs. It must not import `model_core`.

## 3.2 Parent transaction immutability

The AW-00 transaction is consumed by digest.

Forbidden:

```text
editing the parent transaction in place
changing the parent receipt digest
raising BaseTrainAtlasWaveStepState above Prepared
replacing the parent generation fence
reusing the AW-00 writer lease as a slot lease
```

Required child relation:

```text
AW-00 transaction receipt digest
  -> AW-01 runtime binding receipt
  -> AW-01 checkpoint residency receipt
  -> AW-01 residency handoff receipt
```

Every AW-01 receipt must bind the exact parent transaction digest.

---

# 4. AW-01 state model

## 4.1 Residency state is distinct from training-step state

The AW-00 training state remains:

```text
BaseTrainAtlasWaveStepState::Prepared
```

AW-01 adds a separate residency state:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum BaseTrainAtlasWaveResidencyState {
    Unbound,
    RuntimeBound,
    CheckpointVerified,
    PlansJoined,
    RingAllocated,
    UploadWaveActive,
    ResidencyHandoffReady,
    Invalidated,
}
```

Canonical transitions:

```text
Unbound
  -> RuntimeBound
  -> CheckpointVerified
  -> PlansJoined
  -> RingAllocated
  -> UploadWaveActive
  -> ResidencyHandoffReady
```

Any device/queue epoch mismatch, transaction mismatch, checkpoint mismatch, slot alias, or upload parity failure transitions to:

```text
Invalidated
```

No transition from `Invalidated` is admitted in AW-01.

## 4.2 State ceiling

The maximum admitted state after PASS is:

```text
AW-00 training state     Prepared
AW-01 residency state    ResidencyHandoffReady
```

The word `Ready` means ready to be consumed by a later AW-02 forward patch. It is not forward authority.

---

# 5. Runtime binding authority

## 5.1 Runtime identity receipt

New pure schema:

```rust
pub struct BaseTrainAtlasWaveRuntimeIdentityReceipt {
    pub patch_id: String,
    pub build_revision: String,
    pub parent_transaction_digest: String,

    pub runtime_handle_source: String,
    pub runtime_holder_id: String,
    pub device_identity_digest: String,
    pub queue_identity_digest: String,

    pub device_epoch: u64,
    pub queue_epoch: u64,

    pub native_handles_present: bool,
    pub same_device_arc_identity: bool,
    pub same_queue_arc_identity: bool,
    pub raw_bridge_available: bool,

    pub new_instance_create_count: u32,
    pub new_adapter_request_count: u32,
    pub new_device_request_count: u32,
    pub new_queue_create_count: u32,

    pub receipt_digest: String,
}
```

Required values:

```text
native_handles_present          true
same_device_arc_identity        true
same_queue_arc_identity         true
raw_bridge_available            true
new_instance_create_count       0
new_adapter_request_count       0
new_device_request_count        0
new_queue_create_count          0
```

## 5.2 Identity derivation

The live coordinator receives one `&NativeWgpuRuntimeHandles`.

Identity uses the same physical convention already proven by G202D:

```text
runtime_holder_id
  sha256(source || Arc::as_ptr(device) || Arc::as_ptr(queue))

device_identity_digest
  sha256("aw01-device" || source || Arc::as_ptr(device))

queue_identity_digest
  sha256("aw01-queue" || source || Arc::as_ptr(queue))
```

These are process-local identity receipts. They are not stable checkpoint identities and must not be compared across process restarts.

## 5.3 Device and queue epochs

Epochs are supplied by the existing runtime holder or a dedicated BaseTrain binding adapter.

Required:

```text
device_epoch > 0
queue_epoch > 0
all slot arenas bind the same device_epoch
all upload submissions bind the same queue_epoch
parent transaction digest remains constant
```

Forbidden:

```text
invent epoch 0 as a default
derive epoch from wall-clock time
silently reset an epoch after device loss
bind one slot to a different runtime holder
```

A changed runtime pointer or epoch invalidates the whole AW-01 coordinator.

---

# 6. Same-device generation fence

## 6.1 Bound child fence

AW-01 adds a pure function that consumes the AW-00 unbound fence and returns a child fence:

```rust
pub fn bind_atlas_wave_generation_fence_same_device(
    parent: &BaseTrainAtlasWaveGenerationFence,
    runtime: &BaseTrainAtlasWaveRuntimeIdentityReceipt,
    atlas_residency_generation: u64,
) -> Result<BaseTrainAtlasWaveGenerationFence>
```

Required child fields:

```text
model_instance_id                              identical to parent
checkpoint_digest                              identical to parent
source_weight_generation                       identical to parent
source_optimizer_state_generation              identical to parent
source_training_cursor_generation              identical to parent
expected_candidate_weight_generation           identical to parent
expected_candidate_optimizer_state_generation  identical to parent
expected_candidate_training_cursor_generation  identical to parent
atlas_schedule_digest                          identical to parent
runtime_binding_state                          BoundSameDevice
atlas_residency_generation                     Some(nonzero)
device_epoch                                   Some(runtime.device_epoch)
queue_epoch                                    Some(runtime.queue_epoch)
```

The parent fence digest is retained separately in the runtime binding receipt.

## 6.2 Generation classes must not be collapsed

Distinct counters:

```text
source weight generation
source optimizer-state generation
source training-cursor generation
atlas residency generation
device epoch
queue epoch
slot lease generation
upload submission serial
```

Forbidden aliases:

```text
residency generation == candidate weight generation by convention
slot lease generation == weight generation
queue epoch == upload submission serial
process timestamp == device epoch
```

The source weight generation remains immutable for the entire AW-01 upload wave.

---

# 7. Checkpoint identity and Safetensors topology

## 7.1 Checkpoint identity receipt

```rust
pub struct BaseTrainAtlasWaveCheckpointIdentityReceipt {
    pub parent_transaction_digest: String,
    pub checkpoint_path: String,
    pub expected_checkpoint_digest: String,
    pub observed_checkpoint_digest: String,
    pub checkpoint_file_bytes: u64,

    pub safetensors_header_len: u64,
    pub safetensors_header_digest: String,
    pub safetensors_data_section_start: u64,
    pub tensor_count: u32,
    pub metadata_entry_present: bool,

    pub streaming_digest_buffer_bytes: u64,
    pub whole_file_retained_in_memory: bool,
    pub full_payload_deserialized: bool,
    pub receipt_digest: String,
}
```

Required:

```text
observed_checkpoint_digest == expected_checkpoint_digest
whole_file_retained_in_memory == false
full_payload_deserialized == false
```

## 7.2 Full-file digest is streaming, not materialization

Checkpoint SHA-256 may read every file byte once during admission, but only through a reusable bounded byte buffer.

Canonical maximum:

```text
streaming_digest_buffer_bytes <= 8 MiB
```

This operation is permitted because it does not retain the payload or construct tensors.

Forbidden:

```rust
fs::read(checkpoint_path)
Vec<u8> sized to checkpoint_file_bytes
SafeTensors::deserialize(&whole_checkpoint_bytes)
checkpoint mmap retained as a model-wide host tensor owner
```

## 7.3 Header-only parsing

Canonical read order:

```text
read exact first 8 bytes
  -> little-endian u64 header length
  -> validate header length and file bounds
  -> read exact header JSON bytes
  -> parse tensor names, dtype, shape, data_offsets
  -> derive absolute payload ranges
```

For a tensor entry with Safetensors offsets `[start, end)`:

```text
absolute_start = 8 + header_len + start
absolute_end   = 8 + header_len + end
```

Required validation:

```text
start < end
absolute_end <= checkpoint_file_bytes
dtype byte width known
shape product does not overflow
shape product * dtype width == end - start
all tensor keys unique
payload ranges do not overlap illegally
```

Metadata entries are never treated as tensors.

---

# 8. Manifest and plan join

## 8.1 Authoritative inputs

AW-01 consumes the exact paths and digests already sealed in:

```text
BaseTrainModelSourceAuthority::CheckpointAtlas
```

Required inputs:

```text
tensor_group_manifest_path
tensor_group_manifest_digest
atlas-group-plan_path
atlas-group_plan_digest
sequential_load_plan_path
sequential_load_plan_digest
```

Each file is re-read and digest-verified.

No path scan, filename heuristic, or single-candidate inference is admitted in the canonical path.

## 8.2 Typed joined slice

```rust
pub struct BaseTrainAtlasWaveCheckpointSlice {
    pub group_id: String,
    pub group_order: u32,
    pub wave_order: u32,

    pub tensor_key: String,
    pub dtype: String,
    pub shape: Vec<u64>,

    pub tensor_absolute_start: u64,
    pub tensor_absolute_end: u64,
    pub slice_absolute_start: u64,
    pub slice_absolute_end: u64,

    pub logical_element_start: u64,
    pub logical_element_count: u64,

    pub slot_segment_index: u32,
    pub slot_byte_offset: u64,
    pub upload_byte_len: u64,
    pub padded_byte_len: u64,

    pub source_slice_digest: String,
    pub address_digest: String,
}
```

## 8.3 Join invariants

Required:

```text
every plan tensor key exists in the Safetensors header
every admitted tensor key belongs to exactly one authoritative group
every slice lies inside its tensor payload range
every slice length aligns to dtype width
wave order is total and deterministic
group order is total and deterministic
slot addresses do not overlap inside one resident group
padded bytes are zero and excluded from source digest
no unplanned tensor is read
no missing planned tensor is ignored
```

Forbidden:

```text
implicit group selection
lexical reordering when plan order is present
whole-tensor fallback when slice metadata is missing
fabricated dtype or shape
fabricated offset 0
latest checkpoint substitution
```

---

# 9. Host byte movement authority

## 9.1 Permitted staging form

AW-01 permits a bounded reusable raw-byte staging buffer.

```rust
pub struct BaseTrainAtlasWaveHostStagingPolicy {
    pub max_staging_bytes: u64,
    pub buffer_count: u32,
    pub raw_bytes_only: bool,
    pub typed_tensor_materialization_allowed: bool,
    pub full_checkpoint_retention_allowed: bool,
}
```

Canonical values:

```text
max_staging_bytes                   configurable, hard-capped by gate
buffer_count                        1 or 2
raw_bytes_only                      true
typed_tensor_materialization_allowed false
full_checkpoint_retention_allowed   false
```

## 9.2 “No full tensor materialization” definition

Allowed:

```text
read exact raw checkpoint range into reusable Vec<u8>
upload raw f16, bf16, or f32 bytes unchanged
read one complete very small tensor as raw bytes when the plan explicitly contains one bounded slice
stream full-file SHA-256 through a reusable buffer
```

Forbidden:

```text
construct full Vec<f32> for a checkpoint tensor
construct full Burn Tensor from the checkpoint slice
retain all slices of a group in host memory simultaneously
retain the full checkpoint payload
call tensor.data().to_vec() for the checkpoint owner
byte-swap or numerically transform weights on the host
```

The semantic boundary is typed tensor ownership, not whether one bounded raw slice happens to cover a small tensor.

## 9.3 Lifetime

Canonical slice lifetime:

```text
seek/read exact range
  -> source digest
  -> queue upload
  -> optional bounded readback compare
  -> zero or release staging bytes
```

No staging payload survives the slice transaction.

---

# 10. Triple-ring slot SSOT

## 10.1 Exactly three slots

```rust
pub const BASETRAIN_ATLAS_WAVE_SLOT_COUNT: usize = 3;
```

No configuration may reduce or increase the slot count in AW-01.

Canonical semantic roles:

```text
CurrentResident  group available for the next consumer patch
NextPrefetch     next ordered group being filled or ready
Retiring         previous group awaiting completion proof and release
```

The role is not permanently tied to a physical index.

## 10.2 Physical slot state

```rust
pub enum BaseTrainAtlasWaveSlotState {
    Empty,
    LeaseAcquired,
    Filling,
    UploadSubmitted,
    UploadVerified,
    ResidentReady,
    RetirePending,
    Released,
    Poisoned,
}
```

```rust
pub struct BaseTrainAtlasWaveSlotLease {
    pub slot_index: u32,
    pub slot_lease_generation: u64,
    pub owner_transaction_digest: String,
    pub runtime_holder_id: String,
    pub device_epoch: u64,
    pub queue_epoch: u64,
    pub source_weight_generation: u64,
    pub atlas_residency_generation: u64,
    pub group_id: Option<String>,
    pub state: BaseTrainAtlasWaveSlotState,
    pub lease_digest: String,
}
```

## 10.3 Slot arena topology

A physical slot owns one deterministic arena topology:

```rust
pub struct BaseTrainAtlasWaveSlotArena {
    pub slot_index: u32,
    pub segment_count: u32,
    pub segment_capacity_bytes: Vec<u64>,
    pub total_capacity_bytes: u64,
    pub storage_alignment_bytes: u64,
    pub runtime_holder_id: String,
    pub device_epoch: u64,
    pub queue_epoch: u64,
    pub arena_digest: String,
}
```

All three slots must have identical segment topology.

Segmentation respects the borrowed adapter limits:

```text
max_buffer_size
max_storage_buffer_binding_size
min_storage_buffer_offset_alignment
max_storage_buffers_per_shader_stage
```

AW-01 records these limits but creates no bind group.

## 10.4 Canonical lifecycle

```text
Empty or Released
  -> LeaseAcquired
  -> Filling
  -> UploadSubmitted
  -> UploadVerified
  -> ResidentReady
  -> RetirePending
  -> Released
```

Forbidden transitions:

```text
Filling -> ResidentReady without submission
UploadSubmitted -> Released without completion proof
ResidentReady -> Filling without release
Poisoned -> LeaseAcquired
one slot leased to two groups
one group resident in two slots under the same residency generation
```

## 10.5 Release-before-reuse

A slot may be reused only after:

```text
all queue writes for the slot are ordered
all verification copies are submitted
queue completion or device poll confirms visibility
all bounded readback maps are unmapped
slot owner releases the lease
```

Wall-clock TTL is not a completion proof.

---

# 11. Backend-local residency ABI

## 11.1 Backend input

New backend module:

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_01_residency.rs
```

Backend-local input example:

```rust
pub struct BaseTrainAtlasWave01BackendSliceInput<'a> {
    pub slot_index: u32,
    pub segment_index: u32,
    pub slot_byte_offset: u64,
    pub source_bytes: &'a [u8],
    pub source_slice_digest: &'a str,
    pub runtime_holder_id: &'a str,
    pub device_epoch: u64,
    pub queue_epoch: u64,
}
```

The backend does not receive model semantics, optimizer state, or `model_core` receipt types.

## 11.2 Allowed GPU operations

```text
borrow existing Device
borrow existing Queue
query borrowed Device limits
create exactly the ring arena buffers and bounded readback buffers
queue.write_buffer into an owned slot range
create command encoder for copy-only verification
copy_buffer_to_buffer for bounded readback
queue.submit copy-only command buffers
map bounded readback range
unmap bounded readback range
destroy or drop AW-01-owned buffers on coordinator teardown
```

## 11.3 Forbidden GPU operations

```text
wgpu::Instance::default or Instance::new
request_adapter
request_device
creating a replacement queue
shader module creation
pipeline layout creation
compute pipeline creation
render pipeline creation
bind group creation
compute pass creation
render pass creation
dispatch_workgroups
draw
indirect execution
resident weight mutation after ResidentReady
```

## 11.4 Upload visibility receipt

```rust
pub struct BaseTrainAtlasWave01BackendUploadReceipt {
    pub slot_index: u32,
    pub segment_index: u32,
    pub slot_byte_offset: u64,
    pub uploaded_bytes: u64,
    pub source_slice_digest: String,
    pub readback_slice_digest: String,
    pub byte_parity: bool,
    pub nonzero_payload_observed: bool,
    pub queue_submit_serial: u64,
    pub runtime_holder_id: String,
    pub device_epoch: u64,
    pub queue_epoch: u64,
    pub receipt_digest: String,
}
```

Canonical verification gate mode performs full parity for each bounded slice.

Production adoption may later introduce a separately specified lower-overhead verification policy. AW-01 itself does not silently downgrade verification.

---

# 12. Upload-wave ordering

## 12.1 Deterministic wave

Let groups be ordered by the authoritative sequential-load plan:

```text
G0, G1, ..., G(n-1)
```

Canonical physical slot selection:

```text
slot_index = wave_order mod 3
```

The coordinator may overlap file read, queue upload, and prior-slot retirement only when ownership and submission ordering remain explicit.

## 12.2 No hidden parallel authority

Parallel I/O or queue preparation is permitted only as an implementation detail beneath the same total wave order.

Required:

```text
receipt order == sequential-load-plan order
slot lease order deterministic
queue submit serial monotonic
same transaction digest on every group
same source weight generation on every group
```

Forbidden:

```text
hash-map discovery order
completion-order artifact publication
latest-ready group substitution
skipping a large group without a HOLD
loading multiple source generations in one ring
```

## 12.3 Canonical gate rehearsal and handoff seed

The physical gate performs:

```text
all admitted groups
  upload -> verify -> retire/reuse
```

After full-wave validation, it performs a deterministic seed handoff:

```text
slot 0  first group ResidentReady
slot 1  second group ResidentReady or Empty when absent
slot 2  Empty
```

This handoff proves the future consumer shape. The gate process may release resources after writing evidence. A serialized receipt is not a live GPU handle.

---

# 13. Residency handoff contract

```rust
pub struct BaseTrainAtlasWave01ResidencyHandoffReceipt {
    pub patch_id: String,
    pub build_revision: String,
    pub parent_transaction_digest: String,
    pub runtime_binding_digest: String,
    pub bound_generation_fence_digest: String,
    pub checkpoint_identity_digest: String,
    pub joined_plan_digest: String,
    pub ring_topology_digest: String,
    pub upload_wave_digest: String,

    pub source_weight_generation: u64,
    pub atlas_residency_generation: u64,
    pub device_epoch: u64,
    pub queue_epoch: u64,

    pub current_resident_group_id: String,
    pub current_resident_slot_index: u32,
    pub next_prefetch_group_id: Option<String>,
    pub next_prefetch_slot_index: Option<u32>,

    pub resident_slot_address_digests: Vec<String>,
    pub forward_execution_admitted: bool,
    pub handoff_state: String,
    pub receipt_digest: String,
}
```

Required:

```text
forward_execution_admitted  false
handoff_state               ResidencyHandoffReady
```

The receipt exposes address digests and semantic identities, not serializable WGPU handle values.

The live AW-02 caller must receive the in-process coordinator object separately and verify receipt parity.

---

# 14. Runtime and mutation firewall

## 14.1 Allowed nonzero counters

```text
borrowed_runtime_handle_count
gpu_slot_arena_buffer_create_count
bounded_readback_buffer_create_count
checkpoint_stream_read_bytes
safetensors_header_read_bytes
planned_payload_slice_read_bytes
queue_write_count
queue_write_bytes
copy_only_encoder_count
copy_buffer_to_buffer_count
queue_submit_count
bounded_map_read_count
slot_lease_acquire_count
slot_lease_release_count
```

## 14.2 Required zero counters

```text
new_wgpu_instance_count
new_adapter_request_count
new_device_request_count
new_queue_create_count
full_checkpoint_host_retention_count
typed_full_tensor_materialization_count
unplanned_payload_read_count
shader_module_create_count
bind_group_create_count
pipeline_create_count
compute_pass_create_count
render_pass_create_count
forward_dispatch_count
embedding_lookup_count
qkv_projection_count
rope_execution_count
headwise_attention_count
tensorcube_dispatch_count
logits_materialization_count
loss_compute_count
backward_execution_count
gradient_write_count
optimizer_state_write_count
optimizer_step_count
delta_materialization_count
resident_weight_write_count
weight_commit_count
training_cursor_write_count
pointer_swap_count
checkpoint_write_count
checkpoint_finalize_count
route_promotion_count
decode_route_mutation_count
quality_claim_count
silent_fallback_count
```

## 14.3 Resident immutability

After a slot reaches `ResidentReady`, AW-01 may only:

```text
borrow identity metadata
mark RetirePending
release after completion proof
```

AW-01 must not overwrite bytes in a `ResidentReady` slot.

---

# 15. Failure and HOLD taxonomy

## 15.1 Runtime binding failures

```text
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_PARENT_TRANSACTION_INVALID
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_PARENT_TRANSACTION_NOT_PREPARED
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_NATIVE_RUNTIME_HANDLES_MISSING
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_RAW_BRIDGE_UNAVAILABLE
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_RUNTIME_HOLDER_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_DEVICE_EPOCH_MISSING
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_QUEUE_EPOCH_MISSING
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SECONDARY_DEVICE_CREATION_DETECTED
```

## 15.2 Checkpoint and plan failures

```text
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_CHECKPOINT_MISSING
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_CHECKPOINT_DIGEST_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SAFETENSORS_HEADER_INVALID
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_TENSOR_RANGE_OUT_OF_BOUNDS
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_TENSOR_SIZE_DTYPE_SHAPE_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_MANIFEST_DIGEST_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_ATLAS_PLAN_DIGEST_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SEQUENTIAL_PLAN_DIGEST_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_PLAN_TENSOR_KEY_MISSING
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_UNPLANNED_TENSOR_READ
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLICE_RANGE_INVALID
```

## 15.3 Ring and upload failures

```text
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_COUNT_NOT_THREE
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_ARENA_TOPOLOGY_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_DOUBLE_LEASE
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_OWNER_TRANSACTION_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_GENERATION_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_ADDRESS_ALIAS
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_SLOT_REUSE_BEFORE_RELEASE
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_UPLOAD_SOURCE_DIGEST_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_UPLOAD_READBACK_DIGEST_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_QUEUE_SUBMISSION_ORDER_MISMATCH
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_RUNTIME_EPOCH_CHANGED
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_HOST_FULL_TENSOR_MATERIALIZATION_DETECTED
ERR_ASH_BASETRAIN_ATLAS_WAVE_01_FORWARD_EXECUTION_DETECTED
```

A failure invalidates the coordinator and releases only resources whose completion status is known.

No fallback to a fresh device, CPU model, random initialization, or generic attention is admitted.

---

# 16. Physical verification gate

## 16.1 Binary

```text
ash_basetrain_atlas_wave_01_physical_gate
```

The gate must execute against the real existing native runtime bootstrap used by current BaseTrain physical gates.

A pure JSON fixture without a borrowed WGPU device and queue is insufficient for PASS.

## 16.2 Positive proof set

Minimum positive assertions: `64`.

Required classes:

```text
AW-00 parent receipt replay
parent transaction state Prepared
parent digest byte preservation
native runtime handle extraction
same device Arc identity
same queue Arc identity
raw bridge availability
nonzero device and queue epochs
bound child generation-fence replay
checkpoint streaming digest parity
Safetensors header topology parity
manifest digest parity
atlas plan digest parity
sequential plan digest parity
exact tensor-key join
exact payload range validation
three-slot topology equality
slot address non-aliasing
bounded staging limit
raw-byte upload parity
queue serial monotonicity
release-before-reuse
all-group wave-order parity
seed residency handoff
zero forward authority
Rust artifact readback verification
```

## 16.3 Negative controls

Minimum negative controls: `96`.

Required classes:

```text
wrong parent transaction digest
parent state above Prepared
wrong checkpoint digest
truncated Safetensors header
header length beyond file
unknown dtype
overflowing shape product
data offset outside file
overlapping tensor range
missing manifest
wrong manifest digest
missing tensor key
fabricated slice offset
slice outside tensor range
unplanned tensor read
staging buffer over budget
whole checkpoint fs::read attempt
typed full-tensor Vec construction sentinel
slot count 2
slot count 4
different slot topology
double slot lease
slot address overlap
reuse before release
mixed source weight generation
mixed transaction digest
mixed runtime holder
changed device epoch
changed queue epoch
source/readback digest mismatch
new WGPU instance sentinel
request_adapter sentinel
request_device sentinel
shader module sentinel
bind group sentinel
pipeline sentinel
compute pass sentinel
forward dispatch sentinel
logits/loss/backward/optimizer sentinel
checkpoint write sentinel
route mutation sentinel
silent fallback sentinel
```

## 16.4 Static source closure

The gate scans AW-01 canonical modules and fails on:

```text
wgpu::Instance::default
wgpu::Instance::new
request_adapter(
request_device(
AshModel::new(
build_hybrid_train_model(
grouped_query_attention(
create_shader_module(
create_compute_pipeline(
create_bind_group(
begin_compute_pass(
dispatch_workgroups(
fs::read(checkpoint
SafeTensors::deserialize(&whole
```

Static scanning supplements physical counters. It does not replace them.

---

# 17. Rust-generated artifacts

No runtime manifest or runtime evidence artifact is included pre-generated in the code package.

The Rust gate writes atomically to:

```text
workspace/runtime/basetrain/atlas_wave/01/
```

Required artifacts:

```text
01_parent_transaction_receipt.json
02_runtime_identity_receipt.json
03_bound_generation_fence_receipt.json
04_checkpoint_identity_receipt.json
05_safetensors_header_receipt.json
06_manifest_plan_join_receipt.json
07_host_staging_policy_receipt.json
08_triple_ring_topology_receipt.json
09_slot_lifecycle_receipt.json
10_upload_wave_receipt.json
11_same_device_fence_receipt.json
12_residency_handoff_receipt.json
13_mutation_firewall_receipt.json
14_static_source_closure_receipt.json
15_artifact_write_receipt.json
ash_basetrain_atlas_wave_01_local_manifest.json
```

Each entry records:

```text
semantic artifact ID
relative path
byte count
SHA-256
atomic rename completed
readback digest verified
parent transaction digest
runtime binding digest where applicable
```

The artifact-write receipt is written last and includes the ordered digest of the preceding artifacts.

---

# 18. Implementation surface

## 18.1 New model-core files

```text
crates/model_core/src/base_train_atlas_wave_01_runtime_binding.rs
crates/model_core/src/base_train_atlas_wave_01_checkpoint_residency.rs
crates/model_core/src/base_train_atlas_wave_01_ring_contract.rs
```

## 18.2 New backend file

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_01_residency.rs
```

Backend-local only. No `model_core` dependency may be added to `burn_webgpu_backend`.

## 18.3 New BaseTrain files

```text
crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
crates/base_train/src/base_train_atlas_wave_01_plan_join.rs
crates/base_train/src/base_train_atlas_wave_01_residency_coordinator.rs
```

## 18.4 New gate files

```text
crates/orchestrator_local/src/base_train_atlas_wave_01_cli_registry.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_01_physical_gate.rs
specs/cli/ash_basetrain_atlas_wave_01.args
```

## 18.5 Modified roots

```text
crates/model_core/src/lib.rs
crates/base_train/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

The patch must add all module declarations and public exports in the same bake. A gate-only generation advance is forbidden.

---

# 19. CLI contract

Required response-file keys:

```text
repo-root
aw00-runtime-artifact
checkpoint
checkpoint-sha256
tensor-group-manifest
tensor-group-manifest-sha256
atlas-group-plan
atlas-group-plan-sha256
sequential-load-plan
sequential-load-plan-sha256
source-weight-generation
source-optimizer-generation
source-cursor-generation
atlas-residency-generation
device-epoch
queue-epoch
max-host-staging-bytes
max-slot-bytes
upload-verification-mode
runtime-output-dir
```

Canonical values:

```text
upload-verification-mode  FullBoundedSliceReadback
slot-count                implicit constant 3, not a CLI override
forward-execution         absent and forbidden
```

Unknown keys fail closed.

---

# 20. Gate contract

```text
slot count                                      3 exact
parent transaction state                       Prepared exact
parent transaction mutation count              0
new instance create count                      0
new adapter request count                      0
new device request count                       0
new queue create count                         0
full checkpoint host retention count           0
typed full-tensor materialization count         0
unplanned payload read count                    0
shader module create count                      0
bind group create count                         0
pipeline create count                           0
compute pass create count                       0
forward dispatch count                          0
loss count                                      0
backward count                                  0
optimizer count                                 0
delta materialization count                     0
weight mutation count                           0
checkpoint mutation count                       0
route mutation count                            0
positive assertions                            64 minimum
negative controls                               96 minimum
runtime artifacts                               15 plus local manifest
artifact readback verification                  all PASS
```

---

# 21. PASS, HOLD, and FAIL tokens

## 21.1 PASS

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_01_NATIVE_RUNTIME_BORROWED_DEVICE_QUEUE_AUTHORITY_CHECKPOINT_SAFETENSORS_ATLAS_RESIDENCY_TRIPLE_RING_SLOT_OWNERSHIP_TRANSACTION_DIGEST_RUNTIME_BINDING_SAME_DEVICE_GENERATION_FENCE_NO_SECONDARY_ADAPTER_DEVICE_CREATION_NO_HOST_FULL_TENSOR_MATERIALIZATION_BOUNDED_RAW_SLICE_UPLOAD_READBACK_PARITY_RELEASE_BEFORE_REUSE_RESIDENCY_HANDOFF_READY_NO_SHADER_NO_BIND_GROUP_NO_PIPELINE_NO_FORWARD_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER_NO_DELTA_NO_WEIGHT_WRITE_NO_CURSOR_WRITE_NO_POINTER_SWAP_NO_CHECKPOINT_WRITE_NO_ROUTE_PROMOTION_NO_DECODE_MUTATION_SEALED
```

## 21.2 Typed HOLD

```text
HOLD_ASH_BASETRAIN_ATLAS_WAVE_01_<REASON_CODE>
```

A HOLD writes diagnostic artifacts but does not write the canonical PASS manifest.

## 21.3 FAIL

```text
FAIL_ASH_BASETRAIN_ATLAS_WAVE_01_AUTHORITY_OR_INTEGRITY_VIOLATION_<REASON_CODE>
```

Authority violations such as secondary device creation, parent transaction mutation, mixed runtime epochs, or forward execution are FAIL, not HOLD.

---

# 22. Direct execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_01_physical_gate `
  -- `
  "@specs/cli/ash_basetrain_atlas_wave_01.args"
```

Expected revision:

```text
ATLAS-WAVE-01-borrowed-runtime-atlas-residency-v1
```

---

# 23. Completion state

After PASS:

```text
AW-00 step transaction
  Prepared
  byte-identical parent receipt preserved

Native runtime
  BorrowedSameDevice
  BorrowedSameQueue
  NoSecondaryRuntime

Checkpoint
  StreamingDigestVerified
  SafetensorsHeaderVerified
  PlanJoinVerified

Atlas residency
  TripleRingAllocated
  BoundedRawSlicesUploaded
  UploadReadbackParityBound
  ReleaseBeforeReuseBound
  ResidencyHandoffReady

Forward authority
  Forbidden
```

Next patch:

```text
ASH-BASETRAIN-ATLAS-WAVE-02

Actual Batch Embedding Residency /
Layer-Scoped QKV Projection Input Binding /
Headwise Training Prefill Live Dispatch /
Causal·Padding·Position·RoPE Receipt Consumption /
TensorCube Candidate Handoff /
No Loss·Backward·Optimizer Seal
```

AW-02 must consume both the live in-process AW-01 coordinator and the sealed residency handoff receipt. It may not reconstruct Atlas residency from JSON alone.
