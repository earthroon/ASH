# BP-DK-CHECKPOINT-R1

## GPU HOT SNAPSHOT CAPTURE

```text
+ MULTI-PARAMETER SNAPSHOT TABLE
+ BOUNDED DOUBLE-WINDOW READBACK
+ NO PER-PARAMETER CHECKPOINT QUEUE SUBMIT
+ NO PER-PARAMETER CHECKPOINT MAP
+ NO PER-PARAMETER POLL WAIT
+ SAME-ENCODER CANDIDATE-STATE CAPTURE
+ POLL-BASED WINDOW RETIREMENT
+ PENDING GENERATION / ARC IDENTITY PRESERVATION
+ HOST DURABILITY FINALIZER SEPARATION
+ EXACT PAYLOAD OFFSET / SHA / MANIFEST PRESERVATION
```

## Parent

Direct parent:

```text
TENSORCUBE-CONSUME-R2
ASH_PASS3_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_CONSUME_PLANE_CODE_ONLY.zip
SHA-256 a2812495deb125a764ee7d112e1d69ad8d32a965b45b30ae82f2999cf43723cd
```

## Physical problem

The legacy transactional BP-DK candidate snapshot performs, for every parameter:

```text
create readback
create encoder
copy state
queue.submit
map_async
device.poll(Wait)
consume
unmap
```

R1 closes that checkpoint-only serialized barrier chain.

## Generation-scoped capture authority

`TensorCubeBpDkLocalObserver` now owns a generation-scoped hot-capture runtime.

New public types:

```text
TensorCubeBpDkCheckpointCaptureSpecR1
TensorCubeBpDkCheckpointCaptureReceiptR1
```

The capture table is armed from canonical Muon parameter IDs and exact tile counts before observation.

Rows are sorted by parameter ID and freeze:

```text
parameter_id
tile_count
payload_offset
byte_length
window_index
window_offset
```

Payload offsets retain the existing checkpoint serialization order.

## Bounded double-window capture

The canonical snapshot is partitioned across at most two `MAP_READ | COPY_DST` buffers.

Parameters are never split across windows in this R1 implementation.

The two windows are allocated only to their exact used bytes and remain bounded by the WGPU max-buffer limit.

No aggregate full-snapshot host `Vec<u8>` is introduced.

## Same-encoder hot copy

All three Local observer candidate-state producer paths use one capture hook:

```text
observe(...)
encode_segmented_phys_r2(...)
observe_segmented_r2(...)
```

After candidate-state compute, the same command encoder receives:

```text
candidate_state -> assigned checkpoint window range
```

For PHYS-R2 externally-owned encoders the window Arc is retained in the encoded resource holds.

Thus hot-captured rows add no checkpoint-only per-parameter queue submission.

## Pending identity preservation

At hot capture, R1 retains the exact candidate-state `Arc<wgpu::Buffer>` witness.

At finalization it rechecks:

```text
pending source optimizer generation exact
pending target BP generation exact
Arc::ptr_eq(current pending buffer, witnessed buffer)
```

No early commit, pending take, or generation resolution is introduced.

The existing source-optimizer / target-BP `(N-1, N)` contract remains unchanged.

## Missing/inherited rows

Rows not hot-captured are not sent through the legacy per-parameter snapshot loop.

All missing rows are copied by one aggregate fallback command encoder/submission.

ActiveVerified therefore freezes:

```text
per_parameter_submit_count = 0
```

## Window map / retirement

R1 issues `map_async` once per physical window.

Completion is driven with:

```text
device.poll(PollType::Poll)
receiver.try_recv()
```

The ActiveVerified finalizer contains no `PollType::Wait`.

Receipt requirements:

```text
per_parameter_map_count = 0
blocking_wait_count = 0
window_count <= 2
```

This R1 maps/drains the completed windows at durability-finalizer time. True window recycle/drain overlap with continuing parameter compute is deliberately deferred to a later performance revision.

## Runtime mode

Environment:

```text
ASH_BP_DK_CHECKPOINT_R1_MODE
```

Modes:

```text
OFF
OBSERVE_ONLY
ACTIVE_VERIFIED
```

### OFF

The legacy `for_each_candidate_state_snapshot_mapped_r3h_cf4()` remains authoritative.

### OBSERVE_ONLY

A separate shadow durability finalizer is not materialized in this bake. It fails closed:

```text
E_BPDK_CHECKPOINT_R1_OBSERVE_ONLY_SHADOW_FINALIZER_NOT_MATERIALIZED
```

No silent fallback.

### ACTIVE_VERIFIED

`for_each_candidate_checkpoint_capture_r1()` is authoritative. The legacy per-parameter mapped candidate snapshot is not used.

## Host durability finalizer

The existing checkpoint serializer remains authoritative.

Mapped window bytes are streamed directly into the payload file. The existing:

```text
parameter SHA-256
payload SHA-256
payload offsets
payload lengths
payload sync_all
manifest construction
manifest write
restore schema
```

are preserved.

Capture completion and durability completion are emitted separately:

```text
[ASH-BPDK-CHECKPOINT-R1][capture]
[ASH-BPDK-CHECKPOINT-R1][durability-finalizer]
```

## Changed files

```text
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
MOD tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_bpdk_pending_snapshot_static.py
MOD tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_cf1_bpdk_generation_binding_static.py
ADD tools/validate_ash_bpdk_checkpoint_r1_gpu_hot_capture_static.py
```

Delta:

```text
MOD 4
ADD 1
DEL 0
```

## Source SHA-256

```text
45b971011a48768568692a1e95b0f9c0eb8bc922de5e1c5405e067633dc6bff9  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
5ff891d879313175a27f0fafced64462d483abb0e5aae2d19541767f14fbe535  crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
f9009f908d73a9a9a4434b53c312370b95080eb5bbd6914b39f7ecd7697d3e43  tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_bpdk_pending_snapshot_static.py
c17fb183802684cc97910e56e64bccdc0c5dfb2ee8a94d19fa2f95d970b9eb10  tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_cf1_bpdk_generation_binding_static.py
311d3ab962f97ebc2ec87636aa2377ac65da36f873c58ffae6d0d968251f7ff6  tools/validate_ash_bpdk_checkpoint_r1_gpu_hot_capture_static.py
```

## Static qualification

```text
PASS_BP_DK_CHECKPOINT_R1_GPU_HOT_CAPTURE_STATIC checks=46
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_SNAPSHOT_STATIC checks=37
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_STATIC checks=32
```

Rust toolchain is unavailable in the bake environment.

```text
SOURCE       APPLIED
STATIC       PASS
ARCHIVE CRC  PASS
COMPILE      NOT RUN
TEST         NOT RUN
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNMEASURED
```

## Artifacts

Overlay:

```text
ASH_BPDK_CHECKPOINT_R1_GPU_HOT_SNAPSHOT_CAPTURE_OVERLAY_CODE_ONLY.zip
SHA-256 ac6d760db532ea59aa75d322bc07fa9a936de5ef098e7ddad5f552fa7d130cf4
FILES 5
CRC PASS
```

Full:

```text
ASH_PASS3_BPDK_CHECKPOINT_R1_GPU_HOT_SNAPSHOT_CAPTURE_CODE_ONLY.zip
SHA-256 29f5c73edd85bdf650b09bf4880794908e550f12a4d274fb22593f1621db5492
FILES 8445
CRC PASS
```

Both exclude specs/, artifacts/, manifests/, Markdown, __pycache__, and *.pyc.

## Physical acceptance

Run with:

```text
ASH_BP_DK_CHECKPOINT_R1_MODE=ACTIVE_VERIFIED
```

Required capture receipt:

```text
windows <= 2
same_encoder_parameters > 0
per_parameter_submits = 0
per_parameter_maps = 0
blocking_waits = 0
pending_generation_exact = true
pending_arc_identity_exact = true
capture_complete = true
admitted = true
```

Then durability finalizer must report:

```text
capture_complete=true
durability_complete=true
manifest_schema_preserved=true
admitted=true
```

Checkpoint payload SHA and restore compatibility must remain exact.

## Final law

> BP-DK candidate-state capture joins the GPU hot execution lineage by appending exact state copies to the candidate producer encoders.

> ActiveVerified checkpoint persistence no longer reconstructs observer state with parameter-by-parameter submit/map/Wait barriers.

> Missing/inherited rows use one bounded aggregate fallback submission.

> Pending generation and buffer identity remain unresolved and exact until the existing transaction authority commits or aborts them.

> GPU capture completeness never implies filesystem durability completeness. Only the existing host durability finalizer may sync and publish the checkpoint.

> True compute/capture/host-drain overlap is a later performance revision; this R1 closes the serialized per-parameter checkpoint barrier topology first.
