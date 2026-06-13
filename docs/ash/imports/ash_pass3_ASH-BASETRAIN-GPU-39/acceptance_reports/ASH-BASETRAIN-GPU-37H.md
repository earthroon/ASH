# ASH-BASETRAIN-GPU-37H Acceptance Report

## Patch

Selected Group Row-Block Shader Module Compile Candidate / Dispatch Candidate To WGSL Contract No Dispatch Seal

## Contract

Consumes `ASH_BASETRAIN_GPU_37G_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_PROMOTION_GATE.json`.

- Requires 37G PASS.
- Requires dispatch candidate ready.
- Requires verified payload bytes `5267456`.
- Requires verified F32 sample count `1316864`.
- Requires workgroup size `256`, dispatch x `5144`, padding `0`.
- Creates WGSL binding contract and entrypoint contract.
- Opens actual GPU adapter/device and creates shader module.
- Does not create GPU buffers.
- Does not create compute pipeline.
- Does not create bind group.
- Does not dispatch.
- Does not run forward/backward/optimizer/mutation.

## Expected PASS

`PASS_ASH_BASETRAIN_GPU_37H_SELECTED_GROUP_ROW_BLOCK_SHADER_MODULE_COMPILE_CANDIDATE_DISPATCH_CANDIDATE_TO_WGSL_CONTRACT_NO_DISPATCH`
