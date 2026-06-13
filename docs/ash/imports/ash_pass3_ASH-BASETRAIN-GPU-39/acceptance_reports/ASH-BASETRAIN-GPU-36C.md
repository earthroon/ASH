# ASH-BASETRAIN-GPU-36C Acceptance Report

## Patch

`ASH-BASETRAIN-GPU-36C`

## Title

Bounded Weight Slice Row Alignment Probe / F32 Window Stats To Tensor Row Boundary Sanity No Full Tensor No GPU Upload Seal

## SSOT

Input SSOT is the explicit ASH-BASETRAIN-GPU-36B PASS receipt only:

`artifacts/ASH_BASETRAIN_GPU_36B_BOUNDED_WEIGHT_SLICE_F32_WINDOW_SANITY.json`

The row basis is sealed to `read_plan_ref.read_offset_bytes`. The probe does not use safetensors `data_start` as the row zero basis.

## Scope

- Receipt-only row alignment probe.
- No source safetensors file open.
- No seek/read.
- No bounded window re-read.
- No full tensor load.
- No full tensor stats.
- No GPU upload.
- No forward/backward/optimizer.
- No checkpoint or safetensors mutation.

## Expected PASS

`PASS_ASH_BASETRAIN_GPU_36C_BOUNDED_WEIGHT_SLICE_ROW_ALIGNMENT_PROBE_F32_WINDOW_STATS_TO_TENSOR_ROW_BOUNDARY_SANITY_NO_FULL_TENSOR_NO_GPU_UPLOAD`

## Expected row contract for selected tensor

- `shape = [48259, 2048]`
- `dtype = F32`
- `dtype_width_bytes = 4`
- `row_stride_bytes = 8192`
- `tensor_byte_size_from_rows = 395337728`
- `row_alignment_basis = read_plan_file_absolute_offset`

## Expected bounded window row alignment

- first: row 0 prefix half
- middle: row 24129 prefix half
- last: row 48258 suffix half

## Control flow preference

Rust code should minimize `if` use and prefer `match`, lookup tables, predicate tables, and status tables.

## Static baked status

The static no-argument baked receipt is expected to block with:

`BLOCKED_36B_RECEIPT_NOT_FOUND`

This is valid because local explicit 36B PASS receipt is required for PASS.
