# ASH-VENDOR-BUFFER-AUTHORITY-INVENTORY-00

## Current GPU Buffer Authority Inventory / Vendor-Fork Allocation Census / Optimizer Hotpath Movement Ledger

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-VENDOR-BUFFER-AUTHORITY-INVENTORY-00` |
| Role | behavior-preserving inventory / observation layer |
| Parent runtime | current ASH vendor fork + TensorCube Muon/HiMuon + R5 AdamW |
| Runtime optimization | forbidden in A00 |
| Buffer reuse | forbidden in A00 |
| Submission completion authority | explicitly absent; A01 owns it |
| Default observer mode | `Off` |
| Diagnostic observer mode | `Observe` |
| Physical GPU promotion | not part of A00 static closure |
| Next patch | `ASH-VENDOR-WGPU-SUBMISSION-EPOCH-LEASE-01` |

A00 answers one question only:

> What GPU bytes exist now, what do they mean, who owns their meaning, how were they created or borrowed, what range is visible, how do they cross host/device boundaries, and where does synchronization occur?

A00 does **not** answer whether a logical release means a physical range can be reused. That question is reserved for A01.

---

## 1. Core invariant

```text
Logical lifetime
!=
GPU completion lifetime
```

Therefore A00 may record:

```text
AllocationObserved
BorrowObserved
LogicalViewCreated
HostInit
HostWrite
DeviceCopyScheduled
ReadbackCopyScheduled
MapReadRequested
QueueSubmitObserved
PollWaitObserved
LogicalReleaseObserved
StorageDeallocObserved
```

but it must never claim:

```text
safe_to_reuse
safe_to_recycle
retire_after_submission
last_writer_submission
last_reader_submission
GPUCompleted
```

---

## 2. Mandatory inventory scope

A00 mandatory scope is deliberately finite.

```text
vendor_fork_scaffold/burn-wgpu-local/src/compute/storage.rs
crates/burn_webgpu_backend/src/raw_bridge.rs
crates/burn_webgpu_backend/src/tensorcube_generation_sealed_muon_cache.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
crates/burn_webgpu_backend/src/base_train_r5_optimizer_continue.rs
```

The patch does not attempt to classify every unrelated attention, decoder, TTS, or application buffer in the repository.

---

## 3. Authority dimensions

A buffer is not classified by one coarse `kind` enum. A00 keeps separate dimensions.

### 3.1 Semantic role

```text
Gradient
SourceWeight
MuonSourceMomentum
MuonCandidateWeight
MuonCandidateMomentum
MuonOrthogonalUpdate
AdamWSourceM
AdamWSourceV
AdamWCandidateWeight
AdamWCandidateM
AdamWCandidateV
StructuralDescriptor
SparseRowMap
KernelParams
RuntimeStatus
CompactTelemetry
VendorComputeStorage
ExternalBorrowedTensor
MaterializedExternalAlias
Unknown
```

Promotion requires `Unknown = 0` for mandatory sites.

### 3.2 Logical owner

```text
VendorStorage
RawBridge
LocalMuon
FusedPairMuon
AdamW
GenerationCache
ExternalRuntime
Unknown
```

Logical owner means the subsystem that owns the semantic lifetime, not necessarily the allocator that created the physical `wgpu::Buffer`.

### 3.3 Physical provenance

```text
VendorComputeStorage
DirectCreateBuffer
DirectCreateBufferInit
QueueWriteMaterialized
RawBorrowedExternal
ExternalAliasMaterialized
Unknown
```

A borrowed `RawWgpuBufferLease` must never be promoted to an authoritative ASH-created physical allocation identity unless creation was actually observed.

### 3.4 Lifetime scope

```text
Process
Runtime
Generation
OptimizerStep
ExecutorCall
PhysicalBatch
ReadbackTransaction
ExternalBorrowed
Unknown
```

This is a logical scope only.

### 3.5 Host visibility

```text
NeverMapped
HostInitialized
HostWritten
MapRead
ExternalBorrow
Unknown
```

### 3.6 Readback payload class

```text
None
BulkTensor
CompactStatus
CompactReceipt
Unknown
```

This separation is required because A03/C07 may remove bulk optimizer payload readback while retaining compact receipts.

---

## 4. Allocation and view separation

```text
Physical Allocation
!=
Logical View
```

A `RawWgpuBufferLease` already carries:

```text
Arc<BackendBuffer>
buffer_offset
buffer_size
shape
len_elements
len_bytes
BridgeMode
ActiveTensorRawHandle
```

A00 preserves that contract and records the exposed byte range. It does not add submission lifetime semantics to `RawWgpuBufferLease`.

Borrowed resources use:

```text
PhysicalIdentityConfidence::BorrowedProvenanceOnly
allocation_id = None
```

Created resources observed by the A00 backend observer may receive a process-local monotonic observation ID. That ID is diagnostic only and is not a stable receipt identity across runs.

---

## 5. Current Local Muon inventory

Mandatory Local Muon sites include:

```text
packed-gradient
gradient-pack segment params
params
descriptors
weight
momentum
candidate-weight
candidate-momentum
orthogonal-update
status
candidate-weight-readback
candidate-momentum-readback
update-readback
status-readback
```

Current baseline truth remains explicit:

```text
gradient payload D2H = 0
candidate weight D2H > 0
candidate momentum D2H > 0
orthogonal update D2H > 0
status D2H > 0
per physical batch queue submit > 0
per physical batch poll Wait > 0
```

A00 may observe these facts but must not remove them.

---

## 6. Current fused HiMuon inventory

Mandatory fused-pair sites include:

```text
params
descriptors
source weight
source momentum
candidate weight
candidate momentum
update
status
candidate weight readback
candidate momentum readback
update readback
status readback
```

`FUSED_RIGHT` and `FUSED_DOWN` execution remains owned by the current `TensorCubeFusedPairMuonExecutor`. A00 changes no planner domain, dispatch geometry, shader, bind-group layout, or output authority.

---

## 7. Current AdamW inventory

A00 includes AdamW because later hybrid device commit cannot be measured honestly without its current host/device baseline.

Mandatory sites:

```text
params
weight
m-prev
v-prev
row-map
candidate-weight
candidate-m
candidate-v
status
weight-readback
m-readback
v-readback
status-readback
```

A00 does not change AdamW/Muon disjoint ownership.

---

## 8. Generation-sealed Muon cache inventory

The existing generation-sealed immutable cache remains the semantic cache authority.

A00 observes:

```text
structural cache allocation
resident weight allocation
resident weight queue-write reuse
```

It does not create a competing cache.

Future relationship:

```text
Generation-Sealed Muon Cache
= semantic identity authority

A02 Vendor Buffer Arena
= physical allocation authority
```

---

## 9. Vendor fork storage hook

`burn-wgpu-local` exposes a narrow A00 hook that records only:

```text
allocation_count
requested_bytes
allocated_bytes
deallocation_count
external_alias_materialization_count
external_alias_materialization_bytes
```

It does not import the backend inventory module and therefore does not invert the dependency direction.

The backend may mirror this snapshot when `burn-raw-access-local` is enabled.

---

## 10. Movement ledger

A00 distinguishes:

```text
HostToDeviceInit
HostToDeviceWrite
DeviceToDeviceCopy
DeviceToReadbackCopy
ReadbackToHostMap
ExternalBorrowZeroCopy
```

In implementation these are represented through separate observation calls and counters rather than a single ambiguous byte counter.

Required aggregate dimensions include:

```text
requested allocation bytes
observed allocation bytes
external borrow bytes
host init bytes
host write bytes
device copy bytes
readback copy bytes
map-read bytes
bulk readback bytes
compact readback bytes
queue submit count
poll Wait count
```

A00 must never label its logical byte counters as physical VRAM residency.

---

## 11. Observer runtime rules

Default:

```text
BufferInventoryMode::Off
```

Diagnostic run:

```text
begin_buffer_inventory_observation()
```

Observe mode may add host metadata/counters only.

Forbidden in the observer hotpath:

```text
JSON serialization
disk write
GPU buffer allocation for telemetry
shader dispatch for telemetry
allocator replacement
buffer reuse
```

The bounded host event ring is diagnostic metadata only and is unrelated to the future GPU staging/readback ring of A03.

Overflow must be explicit:

```text
event_ring_overflow_count > 0
```

and promotion requires zero overflow for the measured run.

---

## 12. Static site identity

Every mandatory site uses a deterministic string ID such as:

```text
local_muon.candidate_weight
fused_muon.readback.momentum
adamw.candidate_v
generation_cache.weight_alloc
vendor.storage.alloc
raw_bridge.borrow
```

The site identity is source semantic identity, not a pointer value and not a line number.

---

## 13. Behavior-preserving seal

A00 must not modify:

```text
WGSL source
buffer usage flags
buffer sizes
bind group layouts
pipeline layouts
dispatch workgroups
copy ordering
queue submission ordering
optimizer formulas
candidate values
Muon domain planning
AdamW/Muon ownership
```

The A00 receipt therefore seals:

```text
allocator_replacement = false
buffer_reuse_introduced = false
submission_lifetime_authority_introduced = false
behavior_preserving_observer = true
```

These are scope declarations. Runtime numeric parity still requires a diagnostic execution on the target environment.

---

## 14. Static source validator

The code bake includes:

```text
tools/ash_vendor_buffer_a00_static_validate.py
```

The static validator checks:

```text
mandatory observer hooks exist
mandatory sites are classified
borrowed physical identity is not overclaimed
A01 completion authority is not introduced
WGSL files remain unchanged from the supplied baseline
Cargo.toml files remain unchanged from the supplied baseline
```

The validator must identify itself as:

```text
STATIC_SOURCE_ONLY
```

and must not claim Rust type-check or physical GPU execution.

---

## 15. Runtime reconciliation target

A real A00 diagnostic run should reconcile the observer snapshot with the executor's pre-existing telemetry.

### Local Muon

```text
queue_submit_count
poll_wait_count
map_async_count
readback_buffer_count
descriptor_upload_bytes
weight_upload_bytes
momentum_upload_bytes
candidate_weight_readback_bytes
candidate_momentum_readback_bytes
update_readback_bytes
status_readback_bytes
gradient_payload_readback_bytes
```

### Fused HiMuon

```text
queue_submit_count
poll_wait_count
descriptor_upload_bytes
weight_upload_bytes
momentum_upload_bytes
candidate_weight_readback_bytes
candidate_momentum_readback_bytes
update_readback_bytes
status_readback_bytes
gradient_payload_readback_bytes
```

### AdamW

The current implementation has less explicit movement telemetry, so A00 establishes its first comparable allocation/readback baseline without changing optimizer output.

---

## 16. A01 handoff

A00 exports an A01-oriented lifetime handoff containing:

```text
site_id
semantic_role
expected_lifetime
creation_frequency
requested_bytes_total
gpu_read_observed
gpu_write_observed
copy_src_observed
copy_dst_observed
submit_observed
completion_authority_present = false
```

The final field is deliberately false in A00.

A01 will introduce the missing physical completion axis:

```text
RegistryEpoch
!=
SubmissionEpoch
```

Only after A01 may A02 decide whether a physical range is safe for arena reuse.

---

## 17. A00 promotion gate

A00 may be considered runtime-promotable only when a target diagnostic run proves:

```text
staticInventoryComplete = true
unknownSemanticRoleCount = 0
unknownOwnerCount = 0
unknownProvenanceCount = 0
mandatoryUnregisteredBufferSiteCount = 0
localMuonTelemetryParity = true
fusedMuonTelemetryParity = true
adamwInventoryComplete = true
vendorStorageInventoryComplete = true
rawBridgeInventoryComplete = true
behaviorParityPassed = true
eventRingOverflowCount = 0
allocatorReplacement = false
bufferReuseIntroduced = false
submissionLifetimeAuthorityIntroduced = false
```

A static source pass alone is not a physical runtime promotion.

---

## 18. Failure classes

```text
FAIL_A00_UNKNOWN_BUFFER_ROLE
FAIL_A00_UNKNOWN_LOGICAL_OWNER
FAIL_A00_UNKNOWN_PHYSICAL_PROVENANCE
FAIL_A00_UNREGISTERED_BUFFER_SITE
FAIL_A00_EXISTING_TELEMETRY_MISMATCH
FAIL_A00_BEHAVIOR_PARITY
FAIL_A00_EVENT_OVERFLOW
FAIL_A00_FALSE_PHYSICAL_IDENTITY
FAIL_A00_LIFETIME_OVERCLAIM
```

---

## 19. Authority declaration

Before A00:

> ASH uses vendor storage, raw borrowed leases, generation-sealed Muon cache buffers, Local Muon candidate buffers, fused HiMuon candidate buffers, AdamW candidate buffers, bulk readbacks, and blocking waits, but no single reproducible authority explains their semantic role, owner, provenance, byte range, movement class, and synchronization exposure.

After A00:

> Every mandatory vendor/optimizer site has a deterministic semantic classification and an opt-in runtime observation path. Borrowed resources are not falsely promoted to created physical allocations. Host initialization, queue writes, readback copies, mapping, submissions, and blocking waits are separated in the ledger. A00 changes no optimizer or allocator semantics and explicitly leaves GPU completion authority unresolved for A01.

### Center sentence

> **A00 is not the patch that saves buffers. It is the patch that proves which buffers exist, which bytes move, and which lifetimes are still unknown before ASH is allowed to reuse anything.**
