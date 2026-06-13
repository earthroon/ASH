# ASH-BASETRAIN-GPU-03R1 Bake Report

## Result

Baked the metadata-based byte estimate repair execution over the `ASH-BASETRAIN-GPU-05B` repair plan.

## Created Artifacts

```txt
ASH_BASETRAIN_GPU_03R1_REPAIRED_UPLOAD_CANDIDATE.json
ASH_BASETRAIN_GPU_03R1_BYTE_ESTIMATE_REPAIR_RECEIPT.json
ASH_BASETRAIN_GPU_03R1_REPAIR_DIFF.json
ASH_BASETRAIN_GPU_03R1_SOURCE_HASH_AUDIT.json
ASH_BASETRAIN_GPU_03R1_TENSOR_SHAPE_REGISTRY_DERIVATION.json
ASH_BASETRAIN_GPU_03R1_NO_GPU_BUFFER_WRITE_CONTRACT.json
ASH_BASETRAIN_GPU_03R1_STATIC_CHECKS.txt
ASH_BASETRAIN_GPU_03R1_LOCAL_VALIDATION.txt
ASH_BASETRAIN_GPU_03R1_ZIP_INTEGRITY.txt
```

## Repair Summary

```txt
chunk_id = block_0000_attention_chunk_0000
metadata_source_used = tensor_shape_registry_from_model_spec_v5_48259
row_range = [0, 2048]
hidden_range = [0, 2048]
repaired_estimated_bytes = 16777216
```

## Closed Paths

```txt
gpu_buffer_write_executed=false
wgpu_queue_write_executed=false
gpu_upload_executed=false
wgpu_compute_dispatch_executed=false
group_local_forward_executed=false
group_optimizer_step_executed=false
safetensors_mutation_present=false
checkpoint_finalization_present=false
```

## Notes

This patch does not read tensor payloads and does not use a safetensors full load. It derives the repair registry from the bundled `specs/model_spec_v5_48259.toml` and records that derivation separately to avoid silent shape injection.

`cargo` compile validation is not claimed in this bake environment.
