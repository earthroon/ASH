# ASH-BASETRAIN-GPU-04R2 Bake Report

## Confirmed

`04R2` was baked as an actual GPU upload execution boundary using the `04R1` readiness receipt as SSOT.
The source artifact was ready, but runtime prerequisites were not available in this environment.

```txt
artifact_ready_from_04r1 = true
actual_wgpu_device_available = false
actual_wgpu_queue_available = false
external_shard_refs_resolvable = false
```

## Result

Actual upload was blocked before shard payload read, GPU buffer create, and queue.write_buffer.

```txt
actual_tensor_payload_read_executed = false
gpu_buffer_created = false
wgpu_queue_write_executed = false
actual_gpu_buffer_state_created = false
```

## Verdict

```txt
FAIL_ASH_BASETRAIN_GPU_04R2_RUNTIME_BLOCKED_NO_ACTUAL_WGPU_DEVICE_OR_SHARD_REF
```
