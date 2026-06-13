# ASH-BASETRAIN-GPU-37Q Acceptance Report

## Patch

ASH-BASETRAIN-GPU-37Q

Selected Group Row-Block Multi-Workgroup Reduction Diagnostic Kernel / Cross-Workgroup Partial Readback Seal

## Static Baked Verdict

`BLOCKED_37P_RECEIPT_NOT_FOUND`

This baked artifact intentionally does not include local PASS receipts for 37P or 37F. Runtime execution requires the operator's local PASS receipt files.

## Opens

- bounded `File::open` / `SeekFrom::Start` / `read_exact`
- `queue.write_buffer`
- `dispatch_workgroups(4, 1, 1)`
- `copy_buffer_to_buffer`
- `map_async` / readback
- `@builtin(workgroup_id)` based partial output
- `var<workgroup>` shared memory
- `workgroupBarrier`
- per-workgroup partial xor checksum
- per-workgroup partial wrapping sum
- per-workgroup partial min / max
- per-workgroup partial guard word

## Closes

- cross-workgroup final reduction
- full tensor load
- full selected group read
- f32 arithmetic correctness claim
- forward
- hidden state materialization
- logits materialization
- backward
- optimizer
- delta candidate
- checkpoint write
- safetensors mutation
