# ASH-BASETRAIN-GPU-36G Acceptance

## Patch

ASH-BASETRAIN-GPU-36G  
Bounded Row View Read Smoke / Row View Plan To Limited Full Row Bytes No Full Tensor No GPU Upload Seal

## Input SSOT

- `artifacts/ASH_BASETRAIN_GPU_36F_CPU_TENSOR_VIEW_CANDIDATE_MATERIALIZATION_PREFLIGHT.json`
- Must be an explicit operator-provided 36F PASS receipt.
- The baked ZIP intentionally does not include this live-path input receipt.

## PASS contract

- 36F receipt is PASS.
- `materialization_preflight.decision == READY_FOR_BOUNDED_ROW_VIEW_READ_PLAN`.
- `candidate_ref` validates F32, shape `[48259, 2048]`, row stride `8192`, and file-absolute byte range.
- `bounded_row_view_plan` contains exactly 3 full-row targets.
- Only the 3 planned rows are read.
- Total bounded row read bytes is `24576`.
- Each row read is exact and has a row byte SHA256 digest.
- Combined row byte read digest is generated.
- Bounded row read smoke digest is generated.
- Combined bounded row view read smoke digest is generated.

## Closed boundary

- No F32 decode.
- No CPU tensor view materialization.
- No full selected group slice read.
- No full tensor load.
- No full tensor stats.
- No safetensors header parse.
- No mmap materialization.
- No GPU upload.
- No forward/backward/optimizer.
- No checkpoint write.
- No safetensors mutation.

## Expected PASS status

`PASS_ASH_BASETRAIN_GPU_36G_BOUNDED_ROW_VIEW_READ_SMOKE_ROW_VIEW_PLAN_TO_LIMITED_FULL_ROW_BYTES_NO_FULL_TENSOR_NO_GPU_UPLOAD`

## Static baked status

`BLOCKED_36F_RECEIPT_NOT_FOUND`
