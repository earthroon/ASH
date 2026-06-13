# ASH-BASETRAIN-GPU-05B Bake Report

## Result

Baked the byte-estimate repair plan over the `ASH-BASETRAIN-GPU-05A` blocker audit.

## Created Artifacts

```txt
ASH_BASETRAIN_GPU_05B_BYTE_ESTIMATE_REPAIR_PLAN.json
ASH_BASETRAIN_GPU_05B_REPAIR_PLAN_RECEIPT.json
ASH_BASETRAIN_GPU_05B_REPAIR_PLAN_CONTRACT.json
ASH_BASETRAIN_GPU_05B_NO_REPAIR_NO_UPLOAD_NO_DISPATCH_CONTRACT.json
ASH_BASETRAIN_GPU_05B_STATIC_CHECKS.txt
ASH_BASETRAIN_GPU_05B_LOCAL_VALIDATION.txt
ASH_BASETRAIN_GPU_05B_ZIP_INTEGRITY.txt
```

## Closed Paths

```txt
repair_execution_executed=false
estimated_bytes_recomputed=false
upload_candidate_mutated=false
gpu_upload_executed=false
wgpu_compute_dispatch_executed=false
group_local_forward_executed=false
group_optimizer_step_executed=false
safetensors_mutation_present=false
checkpoint_finalization_present=false
```

## Notes

This patch intentionally does not repair the zero-byte chunk. It seals the evidence and routes the actual metadata-based recompute to `ASH-BASETRAIN-GPU-03R1`.

`cargo` is not available in this execution runtime, so Rust compile verification is recorded as judgment-unavailable rather than silently claimed.
