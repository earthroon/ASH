# ASH-BASETRAIN-GPU-48-R2 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-48-R2`

## Title

**GPU40 Exact Segment Output Byte Artifact Recovery Or Replay Execution Seal / Exact GPU Readback Segment Bytes To Explicit 2048 Byte Payload Artifact**

## Seal

**No Loss / No Backward / No Optimizer / No Weight Mutation**

---

# 1. Purpose

`ASH-BASETRAIN-GPU-48-R2` recovers or replays the exact GPU readback segment bytes validated by `ASH-BASETRAIN-GPU-40`, writes those bytes as local segment artifacts, concatenates the verified segment artifacts in `ASH-BASETRAIN-GPU-41` stitch order, and writes the final `2048` byte payload artifact required by `ASH-BASETRAIN-GPU-48`.

R1 proved that CPU reference replay can match the CPU reference digest but cannot safely claim the exact GPU output digest. R2 therefore uses exact GPU readback bytes as the payload SSOT.

---

# 2. SSOT

## 2.1 State ownership

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-40` | segment dispatch matrix, source byte ranges, exact GPU output digests |
| `ASH-BASETRAIN-GPU-41` | stitch source map, ascending segment order, final projection digest |
| `ASH-BASETRAIN-GPU-42` | operator-approved projection digest |
| `ASH-BASETRAIN-GPU-44` | forward-boundary input contract |
| `ASH-BASETRAIN-GPU-45` | buffer materialization descriptor |
| `ASH-BASETRAIN-GPU-47` | upload descriptor candidate |
| `ASH-BASETRAIN-GPU-48-R2` | local exact segment artifacts and final payload artifact |
| `ASH-BASETRAIN-GPU-48` | actual payload upload execution |

## 2.2 SSOT presence

SSOT exists.

Primary execution SSOT is:

```text
artifacts/ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json
```

GPU-40 expected exact segment digests:

```text
segment 0: 2054f472b2abe75563fc192dd18d0521d58761580f657308fcfdc02464641892
segment 1: be68f5bcf4b62709412ad5b7b1a1b321e7fccfbb6180c8f6a34be5e8a5af822b
```

Final approved projection digest:

```text
dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
```

## 2.3 Reproducibility

R2 is reproducible only when the local GPU/driver/runtime reproduces the exact GPU-40 readback bytes. If replayed segment bytes do not match GPU-40 segment `output_digest_hex`, the patch must fail closed.

---

# 3. Required local artifacts on PASS

```text
artifacts/ASH_BASETRAIN_GPU_48_R2_SEGMENT_000_EXACT_GPU_OUTPUT.bin
artifacts/ASH_BASETRAIN_GPU_48_R2_SEGMENT_001_EXACT_GPU_OUTPUT.bin
artifacts/ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin
artifacts/ASH_BASETRAIN_GPU_48_R2_EXACT_SEGMENT_OUTPUT_PAYLOAD_RECOVERY_OR_REPLAY.json
```

Segment artifact contract:

```text
byte_len == 1024
f32_count == 256
sha256 == GPU-40 segment output_digest_hex
```

Final payload contract:

```text
byte_len == 2048
f32_count == 512
layout == segment_000 || segment_001
sha256 == approved projection digest
```

---

# 4. Inputs

```text
--gpu40-receipt
--gpu41-receipt
--gpu42-receipt
--gpu44-receipt
--gpu45-receipt
--gpu47-receipt
--out-dir
--out-payload
--out-receipt
--backend
--strict-adapter-match
--strict-selected-group
--max-segment-source-bytes
--max-output-bytes
--recover-existing-segment-artifacts
--force-gpu-replay
--write-segment-artifacts
--write-payload-artifact
```

Default command:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_48_r2_gpu40_exact_segment_output_payload_recovery -- `
  --gpu40-receipt .\artifacts\ASH_BASETRAIN_GPU_40_MULTI_ROW_BLOCK_MATVEC_SEGMENTED_DISPATCH_MATRIX.json `
  --gpu41-receipt .\artifacts\ASH_BASETRAIN_GPU_41_PROJECTION_SEGMENT_STITCH_REVIEW_GATE.json `
  --gpu42-receipt .\artifacts\ASH_BASETRAIN_GPU_42_PROJECTION_CANDIDATE_REVIEW_APPROVAL_GATE.json `
  --gpu44-receipt .\artifacts\ASH_BASETRAIN_GPU_44_FORWARD_BOUNDARY_EXECUTION_PREFLIGHT.json `
  --gpu45-receipt .\artifacts\ASH_BASETRAIN_GPU_45_FORWARD_BOUNDARY_BUFFER_MATERIALIZATION_CANDIDATE.json `
  --gpu47-receipt .\artifacts\ASH_BASETRAIN_GPU_47_FORWARD_BOUNDARY_GPU_BUFFER_UPLOAD_CANDIDATE.json `
  --out-dir .\artifacts `
  --out-payload .\artifacts\ASH_BASETRAIN_GPU_48_SELECTED_GROUP_PAYLOAD.bin `
  --out-receipt .\artifacts\ASH_BASETRAIN_GPU_48_R2_EXACT_SEGMENT_OUTPUT_PAYLOAD_RECOVERY_OR_REPLAY.json `
  --strict-selected-group true `
  --max-segment-source-bytes 262144 `
  --max-output-bytes 2048
```

---

# 5. Allowed operations

R2 may perform GPU replay/readback only for exact segment byte recovery.

Allowed:

- Read GPU-40 segment source ranges only.
- Create WGPU adapter/device/queue.
- Create storage/readback buffers.
- Queue-write the segment payload and deterministic input vector.
- Dispatch the bounded MatVec kernel once per segment.
- Copy output buffer to readback buffer.
- Map/read exact segment output bytes.
- Write segment `.bin` artifacts.
- Concatenate verified segment artifacts.
- Write final payload `.bin`.
- Write R2 runtime receipt.

---

# 6. Forbidden operations

Forbidden:

- Full tensor load.
- Unselected group/range load.
- Logits adoption.
- Model forward adoption.
- Loss computation.
- Backward/gradient computation.
- Optimizer creation or step.
- Weight mutation.
- Delta candidate creation.
- Training commit.
- CPU reference bytes substitution.
- Dummy/random/zero payload.
- Digest-only reconstruction.
- Silent correction.

---

# 7. PASS criteria

R2 PASS requires:

```text
segment_000_artifact.sha256 == 2054f472b2abe75563fc192dd18d0521d58761580f657308fcfdc02464641892
segment_001_artifact.sha256 == be68f5bcf4b62709412ad5b7b1a1b321e7fccfbb6180c8f6a34be5e8a5af822b
payload.byte_len == 2048
payload.sha256 == dbf7b568c05326e791861276d645e5237917e52a8bf77d30c7f4a5133dba8128
forbidden_path_flags.loss_used == false
forbidden_path_flags.backward_used == false
forbidden_path_flags.optimizer_used == false
forbidden_path_flags.weight_mutation_used == false
```

---

# 8. BLOCKED criteria

Representative fail codes:

```text
MISSING_GPU40_RECEIPT
GPU40_SEGMENT_CONTRACT_INVALID
GPU41_STITCH_MAP_MISMATCH
SEGMENT_SOURCE_RANGE_INVALID
SEGMENT_SOURCE_DIGEST_MISMATCH
GPU_ADAPTER_UNAVAILABLE
GPU_DEVICE_UNAVAILABLE
GPU_REPLAY_READBACK_FAILED
SEGMENT_OUTPUT_BYTE_COUNT_MISMATCH
SEGMENT_OUTPUT_DIGEST_MISMATCH
FINAL_PAYLOAD_DIGEST_MISMATCH
SEGMENT_ARTIFACT_WRITE_FAILED
PAYLOAD_WRITE_FAILED
```

---

# 9. PASS meaning

R2 PASS means only:

> Exact GPU-40 segment output bytes were recovered or replayed, written to local segment artifacts, concatenated in GPU-41 stitch order, and sealed as the `2048` byte GPU-48 payload artifact.

R2 PASS does not mean GPU-48 upload succeeded. GPU-48 must be rerun after R2 PASS.
