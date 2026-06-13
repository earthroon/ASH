# ASH-BASETRAIN-GPU-37F Bake Report

## Result

Baked from the 37E ZIP into a 37F candidate ZIP.

## Added files

```text
crates/base_train/src/ash_basetrain_gpu_37f_selected_group_row_block_gpu_upload_readback_smoke.rs
crates/base_train/src/bin/ash_basetrain_gpu_37f_selected_group_row_block_gpu_upload_readback_smoke.rs
acceptance_reports/ASH-BASETRAIN-GPU-37F.md
patch_reports/ASH-BASETRAIN-GPU-37F_bake_report.md
artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
artifacts/ASH_BASETRAIN_GPU_37F_STATIC_CHECKS.txt
artifacts/ASH_BASETRAIN_GPU_37F_STATIC_CHECKS.json
artifacts/ASH_BASETRAIN_GPU_37F_BAKE_MANIFEST.json
```

## Runtime contract

37F requires the local 37E PASS receipt:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_37f_selected_group_row_block_gpu_upload_readback_smoke -- --gpu-upload-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37E_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_SMOKE.json
```

## Guard notes

37F opens actual GPU readback primitives but keeps compute execution sealed:

```text
actual GPU adapter/device/queue: allowed
storage/readback buffer creation: allowed
queue.write_buffer: allowed
copy_buffer_to_buffer: allowed
map_async: allowed
compute shader/pipeline/bind group/dispatch: forbidden
F32 decode: forbidden
forward/backward/optimizer/mutation: forbidden
```

## Digest note

37E's `combined_gpu_upload_source_byte_digest_hex` is a receipt-chain digest over segment digests, not the raw payload SHA. 37F therefore records both:

```text
combined_gpu_readback_source_byte_digest_hex: 37E-compatible segment-chain digest
cpu_source_payload_raw_sha256_hex: raw contiguous source payload SHA
...gpu_readback_raw_sha256_hex: raw GPU readback SHA
```

The PASS comparison is made on the raw CPU source payload digest versus the raw GPU readback digest, while the 37E-compatible chain digest is also preserved for SSOT continuity.

## Container build status

`cargo` / `rustc` are not available in this container, so cargo build/run is not verified here.
