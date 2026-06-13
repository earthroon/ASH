# ASH-BASETRAIN-GPU-37K Acceptance Report

## Patch

Selected Group Row-Block Bound Resource Upload Candidate / Verified Bind Group To Payload Upload No Dispatch Seal

## Static baked status

`BLOCKED_37J_RECEIPT_NOT_FOUND`

This is expected for the baked artifact because live upstream PASS receipts are not included in the ZIP.

## Required runtime inputs

- `artifacts/ASH_BASETRAIN_GPU_37J_SELECTED_GROUP_ROW_BLOCK_BIND_GROUP_CANDIDATE.json`
- `artifacts/ASH_BASETRAIN_GPU_37F_SELECTED_GROUP_ROW_BLOCK_GPU_UPLOAD_READBACK_SMOKE.json`

## PASS target

`PASS_ASH_BASETRAIN_GPU_37K_SELECTED_GROUP_ROW_BLOCK_BOUND_RESOURCE_UPLOAD_CANDIDATE_VERIFIED_BIND_GROUP_TO_PAYLOAD_UPLOAD_NO_DISPATCH`

## Opened in 37K

- bounded `File::open` / `SeekFrom::Start` / `read_exact` for the three 37F representative payload segments
- payload assembly and raw SHA256 verification
- GPU adapter/device request
- shader module, bind group layout, pipeline layout, compute pipeline recreation
- input storage buffer and diagnostic output buffer creation
- `queue.write_buffer` to input storage buffer
- actual bind group creation

## Still sealed

- full tensor read/load
- F32 decode
- CPU tensor view materialization
- copy buffer command
- readback/map
- dispatch
- forward/backward/optimizer/mutation

## SSOT

- 37J PASS receipt: resource binding / bind group SSOT
- 37F PASS receipt: representative payload bytes / digest SSOT
