# ASH-BASETRAIN-GPU-37G-R1 Bake Report

## Summary

Patched ASH-BASETRAIN-GPU-37G to repair the 37F verified readback digest binding path.

## Before

37G required:

```txt
source_binding.combined_row_block_gpu_upload_readback_smoke_digest_hex
source_binding.gpu_upload_readback_execution_digest_hex
```

This caused:

```txt
BLOCKED_37F_COMBINED_GPU_UPLOAD_READBACK_SMOKE_DIGEST_MISSING
```

## After

37G-R1 now reads verified digest SSOT from:

```txt
gpu_upload_readback_smoke_summary.combined_row_block_gpu_upload_readback_smoke_digest_hex
gpu_upload_readback_smoke_summary.gpu_upload_readback_execution_digest_hex
gpu_upload_readback_smoke_summary.combined_gpu_readback_source_byte_digest_hex
gpu_upload_readback_smoke_summary.cpu_source_payload_raw_sha256_hex
gpu_upload_readback_smoke_summary.gpu_readback_byte_digest_hex
```

And cross-checks:

```txt
gpu_readback_digest_receipt.cpu_source_payload_raw_sha256_hex
gpu_readback_digest_receipt.gpu_readback_raw_sha256_hex
gpu_readback_digest_receipt.combined_gpu_readback_source_byte_digest_hex
```

## Boundary

No source shard read, no GPU runtime call, no shader, no pipeline, no bind group, no dispatch, no forward, no backward, no optimizer, no mutation.

## Local execution

Cargo is not available in the baking container; local build/run must be performed by the operator environment.
