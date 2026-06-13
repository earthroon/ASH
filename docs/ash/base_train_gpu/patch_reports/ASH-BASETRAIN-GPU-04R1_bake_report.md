# ASH-BASETRAIN-GPU-04R1 Bake Report

## Summary

`ASH-BASETRAIN-GPU-04R1` was baked as a repaired upload candidate readiness re-audit.
It validates the `03R1` repaired candidate as artifact-ready, then keeps actual GPU upload closed.

## Result

```txt
artifact_ready = True
upload_readiness_class = ARTIFACT_READY_RUNTIME_BLOCKED
upload_ready = False
actual_upload_execution_allowed_in_this_patch = false
```

## Boundary

```txt
actual_tensor_payload_read_executed = false
gpu_buffer_created = false
wgpu_queue_write_executed = false
gpu_upload_executed = false
forward_dispatch_executed = false
optimizer_step_executed = false
safetensors_mutation_present = false
```

## Runtime Note

This bake environment does not expose Rust/Cargo/WGPU runtime execution. Therefore `04R1` records `ARTIFACT_READY_RUNTIME_BLOCKED`, not `FULL_READY_FOR_04R2`.
