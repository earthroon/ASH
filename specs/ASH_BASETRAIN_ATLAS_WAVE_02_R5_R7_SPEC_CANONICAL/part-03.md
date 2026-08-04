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

The binding range must contain exactly one decoded tensor and may not alias another selected tensor unless an explicit immutable atlas suballocation authority proves non-overlap.

## 10.5 Lease lifetime

The lease must remain alive until:

```text
all command buffers using it are submitted
all compact readbacks are complete
all receipts are sealed
```

Dropping a source owner while a borrowed view remains live is forbidden.

---

# 11. Token fixture authority

R5-R7 does not perform text tokenization. It consumes an explicit numeric token fixture whose IDs are already within the R5-R6 vocabulary domain.

Rev.1 fixture requirements:

```text
batch_size              1
sequence_length         4
row_valid_lengths       [3]
position_ids            [0, 1, 2, 3]
valid token IDs         all < 48259
one masked token slot   required
```

A canonical example is:

```text
token_ids               [1, 328, 336, 0]
row_valid_lengths       [3]
position_ids            [0, 1, 2, 3]
```

The exact fixture bytes and digest must be pinned in a versioned JSON file. The semantic meaning of token IDs is not required for R5-R7 admission.

Required negative fixtures:

```text
token ID = 48259
row_valid_length > sequence_length
position ID >= max_position_embeddings
position cardinality mismatch
masked slot with nonzero output
```

---

# 12. GPU selected-layer forward graph

The admitted graph is exactly:

```text
actual embedding weight
  + token IDs
    -> embedding hidden

embedding hidden
  + actual input RMSNorm weight
    -> normalized hidden

normalized hidden
  + actual Q/K/V projection weights
    -> Q, K, V

Q, K
  + position IDs
  + rope_theta
  + NeoXHalfSplit
    -> Q_rope, K_rope

Q_rope, K_rope, V
  + causal mask
  + row-valid-length mask
  + 32Q:4KV GQA mapping
    -> context
```

Dispatch count for the selected surface is expected to be five:

```text
embedding
RMSNorm
QKV projection
NeoX RoPE
attention oracle
```

A fused implementation is permitted only after a separate parity proof. R5-R7 rev.1 uses explicit stage receipts.

---

# 13. Actual embedding adoption

The embedding stage must consume the actual R5-R6 tensor:

```text
model.embed_tokens.weight
```

Required proof:

```text
binding tensor identity digest equals R5-R6
resident decode digest equals lease receipt
vocab stride = hidden_size
masked rows are exact zero
out-of-range token fixture is rejected before dispatch
embedding readback equals CPU reference exactly in f32 representation
```

The embedding output for valid rows should be bit-identical to the decoded resident rows because the stage performs a direct indexed copy.

---

# 14. Actual RMSNorm adoption

The RMSNorm stage must consume:

```text
model.layers.L.input_layernorm.weight
```

The formula is:

```text
mean_square = sum(x_i * x_i) / hidden_size
inverse_rms = 1 / sqrt(mean_square + rms_norm_eps)
y_i = x_i * inverse_rms * weight_i
```

The epsilon must come from R5-R6 config authority. No shader literal or fallback is allowed.

Required proof:

```text
rms_norm_eps bits exact
actual norm tensor identity exact
masked rows exact zero
CPU-f64 reference from same decoded source
finite output count exact
```
