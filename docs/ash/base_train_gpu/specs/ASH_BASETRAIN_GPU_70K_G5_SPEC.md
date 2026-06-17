# ASH-BASETRAIN-GPU-70K-G5 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G5
Selected Slice Payload Read Probe /
Bounded Byte Range Read From G4 Source Contract
No Full Tensor Load No GPU Upload No Forward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G4-R2` current-head freeze as the SSOT anchor and introduce the runtime probe that can read exactly one bounded selected byte range from the G4 source contract.

This patch is the first payload-contact step, but only at byte-slice level. It does not decode a tensor and does not upload anything to GPU.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Source contract lineage: `ASH-BASETRAIN-GPU-70K-G4-R1`
- Current patch: `ASH-BASETRAIN-GPU-70K-G5`
- Next patch: `ASH-BASETRAIN-GPU-70K-G6`
- New runtime permission candidate: bounded selected-slice payload read

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g5_selected_slice_payload_read_probe.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g5_selected_slice_payload_read_probe.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G5_SELECTED_SLICE_PAYLOAD_READ_PROBE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G5_BOUNDED_READ_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G5_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G5_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G5_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G5_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- runtime benchmark reports

## Allowed in G5 runtime probe

- G4-R2 freeze receipt read
- G4-R2 next matrix read
- G4-R1 contract metadata read
- payload file size check
- `seek(start)`
- `read_exact(end - start)`
- slice-scoped SHA256 digest
- first/last 16-byte hex preview as non-decode evidence

## Forbidden in G5

- full file read
- full tensor load
- safetensors full deserialize
- typed tensor decode
- tensor value materialization
- GPU buffer creation
- GPU upload
- bind group creation
- shader dispatch
- forward
- backward
- optimizer
- delta materialization
- checkpoint mutation
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G5_SELECTED_SLICE_PAYLOAD_READ_PROBE_READY_NO_LOCAL_PAYLOAD_EXECUTION_CLAIM
```

The baked ZIP contains the G5 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and the local safetensors payload were unavailable, so no local compile claim or runtime-read PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G5_SELECTED_SLICE_PAYLOAD_READ_PROBE
```

G5 reaches runtime PASS only when the operator runs the baked probe with a concrete G4-R1 contract and payload file, resolves exactly one selected tensor byte range, reads only that bounded byte slice, and emits a slice-scoped digest without decode, GPU upload, forward, backward, optimizer, checkpoint mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G6
Selected Slice Shape DType Decode Probe /
Bounded Payload Bytes To Typed Tensor View Candidate
No GPU Upload No Forward No Weight Mutation
```
