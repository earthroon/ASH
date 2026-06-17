# ASH-BASETRAIN-GPU-70K-G7 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G7
Selected Slice GPU Upload Candidate /
Typed Tensor View Candidate To Staging Buffer Descriptor
No Bind No Dispatch No Forward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G6` typed tensor view candidate as the parent evidence and create only a GPU staging buffer descriptor candidate.

G7 is not an upload execution patch. It validates size, budget, alignment, usage-plan, and source digest carryover. It must not create a real GPU buffer, must not upload bytes, must not bind, must not dispatch, and must not run forward or training.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent read probe: `ASH-BASETRAIN-GPU-70K-G5`
- Parent typed-view probe: `ASH-BASETRAIN-GPU-70K-G6`
- Current patch: `ASH-BASETRAIN-GPU-70K-G7`
- Next patch: `ASH-BASETRAIN-GPU-70K-G8`
- New permission candidate: GPU staging descriptor candidate only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g7_selected_slice_gpu_upload_candidate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g7_selected_slice_gpu_upload_candidate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G7_SELECTED_SLICE_GPU_UPLOAD_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G7_STAGING_BUFFER_DESCRIPTOR_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G7_UPLOAD_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G7_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G7_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G7_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G7_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- actual GPU capture/log dumps
- runtime benchmark reports

## Allowed in G7 runtime probe

- G4-R2 freeze receipt read
- G5 bounded-read receipt read
- G6 typed-view receipt read
- G6 typed-view audit read
- staging size derivation from G6 expected bytes
- staging budget check
- 4-byte upload alignment check
- usage-plan candidate generation
- source slice digest carryover
- descriptor candidate receipt creation

## Forbidden in G7

- payload bytes reread
- tensor value materialization
- typed value vector allocation
- actual GPU device creation
- actual GPU buffer creation
- queue upload execution
- buffer init execution
- buffer map execution
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G7_SELECTED_SLICE_GPU_UPLOAD_CANDIDATE_READY_NO_LOCAL_GPU_DESCRIPTOR_RUNTIME_CLAIM
```

The baked ZIP contains the G7 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` were unavailable and the parent G6 receipt is still source-baked without typed-view runtime PASS, so no local compile claim or GPU descriptor runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G7_SELECTED_SLICE_GPU_UPLOAD_CANDIDATE
```

G7 reaches runtime PASS only when a concrete G6 typed-view PASS receipt is accepted, the staging descriptor size exactly matches the G6 expected byte length, the alignment and staging budget boundaries are satisfied, and no actual GPU buffer creation, upload, bind, dispatch, forward, backward, optimizer, weight mutation, checkpoint mutation, or model-quality claim occurs.

## Next

```text
ASH-BASETRAIN-GPU-70K-G8
Selected Slice GPU Upload Execution Smoke /
Staging Buffer Candidate To GPU Buffer Readback Parity
No Forward No Backward No Optimizer
```
