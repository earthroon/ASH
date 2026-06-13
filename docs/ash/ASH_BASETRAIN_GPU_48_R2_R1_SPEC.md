# ASH-BASETRAIN-GPU-48-R2-R1 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-48-R2-R1`

## Title

Payload Digest Contract Rebind / GPU40 Matrix Digest As Explicit Payload Hash Seal

## Seal

No GPU Replay / No Loss / No Backward / No Optimizer / No Weight Mutation

---

## 1. Purpose

`ASH-BASETRAIN-GPU-48-R2-R1` rebinds the final payload digest contract discovered after `ASH-BASETRAIN-GPU-48-R2`.

R2 recovered exact GPU segment output artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_48_R2_SEGMENT_000_EXACT_GPU_OUTPUT.bin
artifacts/ASH_BASETRAIN_GPU_48_R2_SEGMENT_001_EXACT_GPU_OUTPUT.bin
```

Each segment matched the GPU-40 exact segment output digest. The concatenated 2048-byte payload matched GPU-40 `matrix_digest_hex`, not the GPU-41/42/44/45/47 projection lineage digest. Therefore, R2-R1 uses GPU-40 `matrix_digest_hex` as the explicit payload hash SSOT and preserves the projection lineage digest separately.

---

## 2. SSOT

### 2.1 State Ownership

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-40` | exact segment output digests and matrix payload digest |
| `ASH-BASETRAIN-GPU-48-R2` | local exact segment output `.bin` artifacts |
| `ASH-BASETRAIN-GPU-41` | stitch order and projection lineage digest |
| `ASH-BASETRAIN-GPU-42` | operator approval lineage digest |
| `ASH-BASETRAIN-GPU-44` | forward boundary input lineage contract |
| `ASH-BASETRAIN-GPU-45` | buffer descriptor lineage contract |
| `ASH-BASETRAIN-GPU-47` | upload descriptor lineage contract |
| `ASH-BASETRAIN-GPU-48-R2-R1` | payload digest contract rebind and final payload materialization |
| `ASH-BASETRAIN-GPU-48` | actual payload upload execution |

### 2.2 SSOT Presence

SSOT exists.

Payload hash SSOT:

```text
GPU40 segmented_dispatch_matrix.matrix_digest_hex
= 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

Segment hash SSOT:

```text
segment 0:
2054f472b2abe75563fc192dd18d0521d58761580f657308fcfdc02464641892

segment 1:
be68f5bcf4b62709412ad5b7b1a1b321e7fccfbb6180c8f6a34be5e8a5af822b
```

Projection lineage digest:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

The projection lineage digest must be preserved as lineage evidence, but must not be used as the final payload file hash.

### 2.3 Reproducibility

R2-R1 is reproducible if:

```text
sha256(segment_000 || segment_001) == GPU40 matrix_digest_hex
```

No GPU replay is required.

---

## 3. Inputs

Required receipts:

```text
--gpu40-receipt artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json
--gpu41-receipt artifacts/ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json
--gpu42-receipt artifacts/ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json
--gpu44-receipt artifacts/ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json
--gpu45-receipt artifacts/ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json
--gpu47-receipt artifacts/ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json
--r2-receipt artifacts/ASH_BASETRAIN_GPU_48_R2_EXACT_SEGMENT_OUTPUT_PAYLOAD_RECOVERY_OR_REPLAY.json
```

Required segment artifacts:

```text
--segment-0 artifacts/ASH_BASETRAIN_GPU_48_R2_SEGMENT_000_EXACT_GPU_OUTPUT.bin
--segment-1 artifacts/ASH_BASETRAIN_GPU_48_R2_SEGMENT_001_EXACT_GPU_OUTPUT.bin
```

Outputs:

```text
--out-payload artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin
--out-receipt artifacts/ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json
```

---

## 4. PASS Conditions

```text
segment_0.byte_len == 1024
segment_0.sha256 == 2054f472b2abe75563fc192dd18d0521d58761580f657308fcfdc02464641892
segment_1.byte_len == 1024
segment_1.sha256 == be68f5bcf4b62709412ad5b7b1a1b321e7fccfbb6180c8f6a34be5e8a5af822b
payload.byte_len == 2048
payload.f32_count == 512
payload.sha256 == GPU40 matrix_digest_hex
payload.sha256 == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
projection_lineage_digest_used_as_payload_hash == false
```

---

## 5. Forbidden Paths

R2-R1 must not perform:

```text
GPU replay
GPU upload
GPU dispatch
GPU readback
bind group creation
pipeline creation
shader creation
loss
backward
optimizer
weight mutation
full tensor load
unselected group load
CPU reference substitution
random payload
zero payload
placeholder payload
digest-only reconstruction
silent correction
```

R2-R1 may only read receipts and R2 segment artifacts, and may only write the final GPU-48 payload and its R2-R1 receipt.

---

## 6. Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_48_r2_r1_payload_digest_contract_rebind.rs
crates/base_train/src/bin/ash_basetrain_gpu_48_r2_r1_payload_digest_contract_rebind.rs
crates/base_train/src/lib.rs
crates/base_train/Cargo.toml
```

---

## 7. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_48_r2_r1_payload_digest_contract_rebind -- `
  --gpu40-receipt .\artifacts\ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json `
  --gpu41-receipt .\artifacts\ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json `
  --gpu42-receipt .\artifacts\ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json `
  --gpu44-receipt .\artifacts\ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json `
  --gpu45-receipt .\artifacts\ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --r2-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_EXACT_SEGMENT_OUTPUT_PAYLOAD_RECOVERY_OR_REPLAY.json `
  --segment-0 .\artifacts\ASH_BASETRAIN_GPU_48_R2_SEGMENT_000_EXACT_GPU_OUTPUT.bin `
  --segment-1 .\artifacts\ASH_BASETRAIN_GPU_48_R2_SEGMENT_001_EXACT_GPU_OUTPUT.bin `
  --out-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --out-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_R1_PAYLOAD_DIGEST_CONTRACT_REBIND.json
```

---

## 8. Next Stage

After R2-R1 PASS, rerun GPU-48.

## 9. PASS Meaning

R2-R1 PASS means only that the final 2048-byte GPU-48 payload artifact was created from verified R2 exact GPU segment artifacts, and its payload hash was correctly rebound to GPU-40 matrix digest. It does not mean GPU-48 upload, forward execution, or training succeeded.
