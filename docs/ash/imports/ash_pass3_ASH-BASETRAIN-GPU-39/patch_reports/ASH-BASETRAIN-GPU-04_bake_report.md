# ASH-BASETRAIN-GPU-04 Bake Report

- Patch: `ASH-BASETRAIN-GPU-04`
- Title: `Atlas Group Shard GPU Upload Execution / Upload Candidate To GPU Buffer State No Forward No Optimizer Seal`
- Verdict: `PASS_ASH_BASETRAIN_GPU_04_ATLAS_GROUP_SHARD_GPU_UPLOAD_EXECUTION_UPLOAD_CANDIDATE_TO_GPU_BUFFER_STATE_NO_FORWARD_NO_OPTIMIZER`
- Runtime mode: `contract_fixture_not_run_external_shard_refs_no_wgpu_device`
- Upload groups: 2
- Upload chunks: 3
- Zero estimated byte chunks: 1

## Boundary

GPU upload execution path and GPU buffer state artifact were baked. Actual WGPU queue write was not executed in the sandbox.
