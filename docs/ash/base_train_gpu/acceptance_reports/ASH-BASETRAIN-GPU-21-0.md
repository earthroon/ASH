# ASH-BASETRAIN-GPU-21-0 Acceptance

## Patch

ASH-BASETRAIN-GPU-21-0  
Raw Logits Payload Export / Window 2048 Readback Bytes Materialization For Local Loss Smoke No Loss No Backward No Optimizer Seal

## SSOT

- Source SSOT: ASH-BASETRAIN-GPU-21-R1 failure route rebind PASS.
- Runtime digest SSOT: ASH-BASETRAIN-GPU-18 raw_2048_logits_readback_bytes SHA256 digest.
- Payload target: `target/ash_basetrain_gpu_21_raw_2048_logits.f32le.bin`.

## State owner

`ASH-BASETRAIN-GPU-21-0 raw logits payload export receipt`

## Scope

Opened:

- 21-R1 route validation.
- Source-18 digest evidence validation.
- Runtime 2048 dispatch/readback replay.
- 8192-byte raw f32le logits payload file write.
- Payload digest sidecar write.
- Payload handoff for 21 loss-smoke rerun.

Closed:

- Loss compute.
- Softmax / log-softmax / cross entropy / NLL.
- Backward.
- Gradient buffer.
- Optimizer.
- Delta/materialized apply.
- Weight commit.
- Safetensors mutation.

## Required PASS

- `payload_file_written = true`
- `payload_bytes = 8192`
- `payload_element_count = 2048`
- `payload_digest_match_source_18 = true`
- `loss_computed = false`
- `backward_executed = false`
- `optimizer_step_executed = false`
- `safetensors_mutation_present = false`
- `violation_mask = 0`

## Expected PASS verdict

```txt
PASS_ASH_BASETRAIN_GPU_21_0_RAW_LOGITS_PAYLOAD_EXPORT_WINDOW_2048_READBACK_BYTES_MATERIALIZATION_FOR_LOCAL_LOSS_SMOKE_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER
```

## Local run status

Not executed in this bake environment. `cargo` is not installed here. Local Windows build/run remains the runtime SSOT.
