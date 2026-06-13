# ASH-BASETRAIN-GPU-37O Acceptance Report

## Patch

ASH-BASETRAIN-GPU-37O
Selected Group Row-Block Window Sum Diagnostic Kernel / Multi-Sample Arithmetic Smoke No Forward Seal

## Static baked status

BLOCKED_37N_RECEIPT_NOT_FOUND

This baked placeholder is expected because live upstream receipts are not bundled.
The runtime must be executed with:

- artifacts/ASH_BASETRAIN_GPU_37N_SELECTED_GROUP_ROW_BLOCK_MULTI_WORD_DIAGNOSTIC_KERNEL.json
- artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json

## Opened in 37O

- bounded File::open / SeekFrom::Start / read_exact
- queue.write_buffer
- dispatch_workgroups
- copy_buffer_to_buffer
- map_async/readback
- u32 bitcast XOR checksum
- u32 wrapping sum
- min/max word diagnostic
- arithmetic guard word

## Still closed

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

## Expected PASS

PASS_ASH_BASETRAIN_GPU_37O_SELECTED_GROUP_ROW_BLOCK_WINDOW_SUM_DIAGNOSTIC_KERNEL_MULTI_SAMPLE_ARITHMETIC_SMOKE_NO_FORWARD
