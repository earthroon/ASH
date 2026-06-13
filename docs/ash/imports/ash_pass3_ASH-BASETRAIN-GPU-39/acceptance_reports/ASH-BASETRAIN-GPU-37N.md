# ASH-BASETRAIN-GPU-37N Acceptance Report

## Patch

ASH-BASETRAIN-GPU-37N — Selected Group Row-Block Multi-Word Diagnostic Kernel / Payload Window Sample Readback Expansion Seal

## Static Baked Result

`BLOCKED_37M_RECEIPT_NOT_FOUND`

This is the expected static baked state because the live upstream 37M PASS receipt is intentionally not included in the ZIP.

## Required Runtime Inputs

```powershell
--diagnostic-dispatch-regression-receipt .\artifacts\ASH_BASETRAIN_GPU_37M_SELECTED_GROUP_ROW_BLOCK_DIAGNOSTIC_DISPATCH_REGRESSION.json
--gpu-upload-readback-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json
```

## PASS Status

```text
PASS_ASH_BASETRAIN_GPU_37N_SELECTED_GROUP_ROW_BLOCK_MULTI_WORD_DIAGNOSTIC_KERNEL_PAYLOAD_WINDOW_SAMPLE_READBACK_EXPANSION
```

## Opened Scope

- bounded representative source segment read
- payload raw SHA256 verification
- multi-word diagnostic WGSL generation
- expanded diagnostic storage/readback buffer
- queue.write_buffer
- dispatch_workgroups
- copy_buffer_to_buffer
- map_async/readback
- multi-word payload sample match matrix

## Sealed Scope

- full selected group read
- full tensor load
- F32 tensor decode
- CPU tensor view materialization
- forward
- backward
- optimizer
- delta candidate
- checkpoint write
- safetensors mutation

## Default Sample Plan

```text
[0, 1, 2, 3, 1024, 65536, 1048576, 1316863]
```

## Expected Next Patch

ASH-BASETRAIN-GPU-37O — Selected Group Row-Block Window Sum Diagnostic Kernel / Multi-Sample Arithmetic Smoke No Forward Seal
