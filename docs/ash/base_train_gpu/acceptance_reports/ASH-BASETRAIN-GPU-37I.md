# ASH-BASETRAIN-GPU-37I Acceptance Report

## 확정
- Patch: ASH-BASETRAIN-GPU-37I
- Purpose: 37H WGSL shader module candidate to compute pipeline candidate.
- Allowed runtime calls: request_adapter, request_device, create_shader_module, create_bind_group_layout, create_pipeline_layout, create_compute_pipeline.
- Forbidden runtime calls: source file read, GPU buffer creation, queue upload, readback, actual bind group creation, dispatch, forward, backward, optimizer, mutation.
- Static bake status: BLOCKED_37H_RECEIPT_NOT_FOUND until local 37H PASS receipt is provided.

## 상태 귀속 위치
- crates/base_train

## SSOT 존재 여부
- Required input SSOT: artifacts/ASH_BASETRAIN_GPU_37H_SELECTED_GROUP_ROW_BLOCK_SHADER_MODULE_COMPILE_CANDIDATE.json
- Live upstream receipt is intentionally not included in the baked ZIP.

## 재현 가능성
- Same 37H PASS receipt and same WGSL source should produce the same pipeline layout/descriptor contract digests, excluding GPU environment metadata.
