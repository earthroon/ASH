# ASH-BASETRAIN-GPU-36D Acceptance Report

## Patch

**ASH-BASETRAIN-GPU-36D**  
Bounded Weight Slice Row Sample Continuity Probe / Row Boundary Sanity To Adjacent Window Continuity No Full Tensor No GPU Upload Seal

## SSOT

Input SSOT is the explicit ASH-BASETRAIN-GPU-36C row alignment receipt.

The 36D runner also follows the 36C `source_binding.f32_window_sanity_receipt_path` and verifies the upstream 36B receipt digest before using its `read_plan_ref.source_shard_path`. This avoids inventing a source path because the current 36C receipt does not preserve `source_shard_path` inline.

## Static Baked Result

`BLOCKED_36C_RECEIPT_NOT_FOUND`

This is the expected sealed result inside the bake container because no local 36C PASS receipt is supplied to the runner.

## Expected Local PASS

`PASS_ASH_BASETRAIN_GPU_36D_BOUNDED_WEIGHT_SLICE_ROW_SAMPLE_CONTINUITY_PROBE_ROW_BOUNDARY_SANITY_TO_ADJACENT_WINDOW_CONTINUITY_NO_FULL_TENSOR_NO_GPU_UPLOAD`

## Required Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_36d_bounded_weight_slice_row_sample_continuity_probe -- --row-alignment-receipt .\artifacts\ASH_BASETRAIN_GPU_36C_BOUNDED_WEIGHT_SLICE_ROW_ALIGNMENT_PROBE.json
```

## Adjacent Window Plan

Expected policy from current 36C PASS receipt:

- `first_suffix_adjacent`: row 0, byte 4096..8192, offset 395365760, len 4096
- `middle_prefix_flank`: row 24129, byte 0..2048, offset 593026432, len 2048
- `middle_suffix_flank`: row 24129, byte 6144..8192, offset 593032576, len 2048
- `last_prefix_adjacent`: row 48258, byte 0..4096, offset 790691200, len 4096

Total adjacent read budget: 12288 bytes.

## Guards

- No full selected group slice read
- No full tensor load
- No full tensor stats
- No safetensors header parse
- No mmap
- No GPU upload
- No forward/backward/optimizer
- No checkpoint or safetensors mutation

## Rust Control Flow Policy

Use `match` and lookup tables actively; minimize `if` usage.

## Live Receipt Overwrite Guard

The ZIP does not include live input receipt paths for R3B, 36, 36A, 36B, or 36C.
