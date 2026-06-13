# ASH-BASETRAIN-GPU-37M Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-37M`

`Selected Group Row-Block Diagnostic Dispatch Regression / Repeated Dispatch Determinism And Readback Stability Seal`

## Source SSOT

- Primary input: `artifacts/ASH_BASETRAIN_GPU_37L_SELECTED_GROUP_ROW_BLOCK_DISPATCH_SMOKE.json`
- Payload input: `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## Intent

37M promotes the 37L single dispatch smoke into a bounded repeated dispatch regression. It repeats the same representative payload upload, compute dispatch, diagnostic copy, map/readback, and word0 validation path.

## Opened Gates

- Bounded `File::open` / `SeekFrom::Start` / `read_exact`
- `queue.write_buffer`
- `dispatch_workgroups`
- `copy_buffer_to_buffer`
- `map_async` / readback
- Repeated dispatch/readback rounds

## Closed Gates

- Full tensor load
- Full selected group read
- F32 tensor decode
- CPU tensor view materialization
- `read_to_end`
- Runtime mmap materialization
- Forward
- Backward
- Optimizer
- Delta candidate
- Checkpoint write
- Safetensors mutation

## Expected PASS

```txt
PASS_ASH_BASETRAIN_GPU_37M_SELECTED_GROUP_ROW_BLOCK_DIAGNOSTIC_DISPATCH_REGRESSION_REPEATED_DISPATCH_DETERMINISM_AND_READBACK_STABILITY
```

## Default Regression Plan

```txt
repeat_count = 8
min_repeat_count = 2
max_repeat_count = 32
workgroup_size_x = 256
dispatch_x = 5144
readback_bytes_per_round = 16
```

## Static Bake Result

```txt
STATIC_CHECK_PASS
```

The baked static receipt is intentionally blocked because the local 37L/37F PASS receipts are not included in the package.
