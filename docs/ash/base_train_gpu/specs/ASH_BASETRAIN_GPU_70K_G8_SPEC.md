# ASH-BASETRAIN-GPU-70K-G8 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G8
Selected Slice GPU Upload Execution Smoke /
Staging Buffer Candidate To GPU Buffer Readback Parity
No Forward No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G7` staging descriptor candidate as the parent evidence and execute the first selected-slice GPU upload smoke when runtime preconditions are satisfied.

G8 is the first GPU-contact execution stage in the 70K-G line. It may create a GPU device/queue, upload only the bounded selected slice bytes, copy the buffer to a readback buffer, and verify digest parity. It must not create shaders, bind groups, dispatch kernels, run forward, run backward, run optimizer, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent read probe: `ASH-BASETRAIN-GPU-70K-G5`
- Parent typed-view probe: `ASH-BASETRAIN-GPU-70K-G6`
- Parent upload candidate: `ASH-BASETRAIN-GPU-70K-G7`
- Current patch: `ASH-BASETRAIN-GPU-70K-G8`
- Next patch: `ASH-BASETRAIN-GPU-70K-G9`
- New permission candidate: selected-slice GPU upload and readback parity smoke only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g8_selected_slice_gpu_upload_execution_smoke.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g8_selected_slice_gpu_upload_execution_smoke.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G8_SELECTED_SLICE_GPU_UPLOAD_EXECUTION_SMOKE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G8_GPU_READBACK_PARITY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G8_UPLOAD_EXECUTION_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G8_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G8_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G8_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G8_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- full GPU capture dumps
- runtime benchmark reports

## Allowed in G8 runtime probe

- G4-R2 freeze receipt read
- G5 bounded-read receipt read
- G6 typed-view receipt read
- G7 upload-candidate receipt read
- selected byte-range bounded reread for upload source only
- reread digest verification against parent selected-slice digest
- GPU instance/adapter/device/queue probe
- upload buffer creation
- readback buffer creation
- `queue.write_buffer` for selected slice only
- `copy_buffer_to_buffer`
- `queue.submit`
- `map_async` readback
- readback SHA256 parity check

## Forbidden in G8

- full tensor load
- full safetensors deserialize
- unbounded payload read
- tensor semantic decode
- shader module creation
- bind group creation
- shader dispatch
- forward
- backward
- optimizer
- delta materialization
- checkpoint mutation
- weight mutation
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G8_SELECTED_SLICE_GPU_UPLOAD_EXECUTION_SMOKE_READY_NO_LOCAL_GPU_UPLOAD_RUNTIME_CLAIM
```

The baked ZIP contains the G8 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc`, a concrete G7 runtime PASS receipt, a payload path, and GPU runtime execution evidence were unavailable, so no local compile claim or GPU upload/readback PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G8_SELECTED_SLICE_GPU_UPLOAD_EXECUTION_SMOKE
```

G8 reaches runtime PASS only when a concrete G7 upload-candidate PASS receipt is accepted, the selected bounded payload bytes are reread without full tensor load, the reread digest matches the parent selected-slice digest, the exact selected bytes are uploaded to a GPU buffer, copied to a readback buffer, mapped back, and verified by digest parity without shader creation, bind group creation, dispatch, forward, backward, optimizer, weight mutation, checkpoint mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G9
Single Selected Group Forward Boundary Probe /
Uploaded Slice Buffer To Minimal Forward Surface
No Backward No Optimizer No Delta Commit
```
