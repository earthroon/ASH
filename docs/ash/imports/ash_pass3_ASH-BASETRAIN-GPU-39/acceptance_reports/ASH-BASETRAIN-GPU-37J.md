# ASH-BASETRAIN-GPU-37J Acceptance

## Selected Group Row-Block Bind Group Candidate / Verified Pipeline To Resource Binding No Dispatch Seal

- Input SSOT: `artifacts/ASH_BASETRAIN_GPU_37I_SELECTED_GROUP_ROW_BLOCK_COMPUTE_PIPELINE_CANDIDATE.json`
- PASS status: `PASS_ASH_BASETRAIN_GPU_37J_SELECTED_GROUP_ROW_BLOCK_BIND_GROUP_CANDIDATE_VERIFIED_PIPELINE_TO_RESOURCE_BINDING_NO_DISPATCH`
- Opens: GPU device, shader module, bind group layout, pipeline layout, compute pipeline, GPU input buffer, diagnostic buffer, actual bind group.
- Seals: source file read, row-block read, F32 decode, queue upload, readback, dispatch, forward, backward, optimizer, mutation.
- Receipt layout: JSON atlas tiled parallel sections, no giant `json!` root macro.
