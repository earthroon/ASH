Implementation rules:

```text
selected_layer must be explicit
selected_layer < num_hidden_layers
selected_layer must match every selected tensor key
resident group ID must derive from selected_layer
receipt must record selected_layer
no hidden default
no clamping
no fallback
```

Canonical group ID:

```text
aw02.layer{selected_layer}.prefill_bundle
```

---

# 8. Physical payload read authority

R5-R7 must not open arbitrary tensor paths supplied independently by the user or CLI.

The loader receives only:

```text
R5-R6 checkpoint root
R5-R6 shard authority
R5-R6 tensor authority
```

For each selected tensor:

1. Resolve the shard path under the sealed checkpoint root.
2. Verify the resolved path remains under that root.
3. Verify shard byte count and SHA-256 against R5-R6.
4. Seek to the exact `absolute_file_start`.
5. Read exactly `payload_bytes`.
6. Reject short read, extra range read, overflow or range escape.
7. Decode only that tensor range.

The forward path must not:

```text
scan the checkpoint directory
reparse the full index
recompute tensor names heuristically
open an unlisted shard
read the whole checkpoint into RAM
read LM head, O projection or MLP tensors
mutate checkpoint bytes
```

---

# 9. BF16 and F16 decode authority

## 9.1 Accepted source dtypes

R5-R7 accepts only the dtype physically sealed by R5-R6:

```text
BF16
F16
```

F32 is not part of the R5-R7 half-decode promotion gate. A separate counter-profile may prove F32 later, but it must not silently bypass this patch's BF16/F16 proof obligation.

All five selected tensors must use one consistent physical dtype unless a later explicit per-role mixed-dtype authority is introduced.

## 9.2 Canonical runtime representation

The current R5 shaders consume `array<f32>`. Therefore R5-R7's canonical resident representation is:

```text
IEEE-754 little-endian f32
```

Decode rules:

```text
BF16 -> f32 by exact high-16-bit expansion
F16  -> f32 by IEEE-754 binary16 conversion
NaN payloads remain NaN and are rejected by finite-value admission
Inf values are rejected
negative zero is preserved through decode receipt
subnormal values follow one pinned software conversion rule
```

The decode rule ID must be versioned, for example:

```text
ash.aw02.r5.r7.decode.bf16_to_f32.v1
ash.aw02.r5.r7.decode.f16_to_f32.ieee_rne.v1
```

## 9.3 Atlas parallel streaming-wave decode and upload

The loader must decode in bounded pages and publish them through an explicit Atlas Parallel Streaming Wave authority. A single serial host expansion or a whole-tensor `Vec<f32>` is forbidden.

Rev.2 canonical vocabulary upload profile:

```text
source page bytes          4,194,304
pages per wave            4
parallel decode workers   4
wave readback policy      every wave
resident representation   f32
atlas allocation count    1
```

The vocabulary embedding tensor is uploaded as ordered parallel waves:

```text
R5-R6 embedding physical range
  -> page plan
  -> up to four concurrent exact-range readers
  -> BF16/F16/F32 to f32 page decode
  -> ordered atlas subrange writes
  -> bounded per-wave GPU readback
  -> wave digest equality
  -> immutable embedding resident lease
```

The implementation must preserve page order at publication even when page decode completes out of order. Each wave seals the first page index, page count, source byte range, atlas byte range, source-page digests, decoded-page digests and readback digest.

The layer RMSNorm and Q/K/V tensors use the same atlas streaming-wave engine. Their pages may form fewer waves because their payloads are smaller.

`lm_head.weight` is not uploaded by R5-R7 because this patch has no logits authority. Its R5-R6 inventory authority remains valid, but `lm_head_upload_count` must equal zero.

The requested wgpu device limits for the R5-R7 physical gate must explicitly adopt the adapter-supported `max_buffer_size` and `max_storage_buffer_binding_size`; silently accepting WebGPU default limits and then splitting authority across an unsealed parallel buffer is forbidden.

The loader must decode bounded pages directly into resident atlas upload pages.

Required counters:

```text
host_full_tensor_materialization_count = 0
checkpoint_whole_file_materialization_count = 0
atlas_page_count > 0
parallel_decode_wave_count > 0
bounded_wave_readback_count = atlas_wave_count
source_range_reopen_count = 0 after lease publication
```

The embedding tensor may be fully resident on the GPU, but its expanded f32 representation must not first exist as one full host `Vec<f32>`.

## 9.4 Decode witnesses

For every tensor, the gate must verify:

```text
source element count
source byte count
decoded element count
decoded f32 byte count
page ordering
wave ordering
parallel completion reorder recovery
source stream digest
decoded stream digest
wave readback digest
first element witness
middle element witness
last element witness
finite count
NaN count = 0
Inf count = 0
```

A counterfactual decoder must be rejected:

```text
BF16 bytes interpreted as F16
F16 bytes interpreted as BF16
byte-swapped half values
truncated final page
page reorder without canonical reassembly
wave reorder
silent zero fill
```

---

# 10. Resident tensor upload and lease provenance

## 10.1 Upload phase and forward phase are distinct

R5-R7 has two explicit phases.

```text
Phase A: checkpoint range read, decode, buffer creation, upload, lease publication
Phase B: selected-layer forward using only published resident views
```

After Phase A publishes the lease set, Phase B must observe:

```text
checkpoint_open_count                  0
checkpoint_payload_read_bytes          0
weight_buffer_create_count             0
weight_queue_write_count               0
weight_queue_write_bytes               0
resident_to_replacement_copy_count     0
```

## 10.2 Same lineage requirement

All five resident tensor leases must share:

```text
checkpointSetDigest
runtimeHolderId
deviceEpoch
queueEpoch
sourceWeightGeneration
atlasResidencyGeneration
slotIndex
groupId
```

A mixed-generation set is invalid even when every individual tensor has a correct shape and digest.

## 10.3 Atlas allocation and vocabulary wave authority

All five selected tensors occupy one immutable, non-overlapping f32 atlas allocation. Each tensor receives a 256-byte aligned suballocation and its own binding range. The embedding range is populated exclusively through the parallel streaming-wave path.

Required atlas counters:

```text
atlas_buffer_create_count             1
atlas_tensor_suballocation_count      5
atlas_page_count                      > 0
atlas_wave_count                      > 0
parallel_decode_wave_count            = atlas_wave_count
bounded_wave_readback_count           = atlas_wave_count
host_full_tensor_materialization_count 0
lm_head_upload_count                  0
```

## 10.4 Buffer identity

Each resident lease must seal:

```text
buffer label
buffer usage
allocation byte length
binding byte offset
binding byte length
runtime buffer identity digest
upload stream digest
tensor identity digest
```

