# ASH-BASETRAIN-GPU-70K-G6 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G6
Selected Slice Shape DType Decode Probe /
Bounded Payload Bytes To Typed Tensor View Candidate
No GPU Upload No Forward No Weight Mutation
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G5` bounded-read receipt and the G4 source contract metadata to validate whether the selected byte slice can form a typed tensor view candidate.

G6 is a contract-boundary decode probe. It validates dtype/shape byte consistency, but it does not materialize tensor values, does not upload anything to GPU, and does not run forward or training.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent read probe: `ASH-BASETRAIN-GPU-70K-G5`
- Source contract lineage: `ASH-BASETRAIN-GPU-70K-G4-R1`
- Current patch: `ASH-BASETRAIN-GPU-70K-G6`
- Next patch: `ASH-BASETRAIN-GPU-70K-G7`
- New permission candidate: typed tensor view candidate validation

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g6_selected_slice_shape_dtype_decode_probe.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g6_selected_slice_shape_dtype_decode_probe.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G6_SELECTED_SLICE_SHAPE_DTYPE_DECODE_PROBE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G6_TENSOR_VIEW_CANDIDATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G6_DTYPE_SHAPE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G6_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G6_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G6_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G6_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- runtime benchmark reports

## Allowed in G6 runtime probe

- G4-R2 freeze receipt read
- G5 bounded-read receipt read
- G5 bounded-read audit read
- G4 source contract metadata read
- dtype normalization through fixed lookup table
- positive shape dimension check
- checked element-count multiplication
- expected byte-size calculation
- `expected_bytes == G5.read_len` validation
- typed tensor view candidate descriptor creation

## Forbidden in G6

- tensor value materialization
- full tensor load
- full safetensors deserialize
- unsafe transmute route
- low-level cast route
- GPU buffer allocation
- GPU upload
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G6_SELECTED_SLICE_SHAPE_DTYPE_DECODE_PROBE_READY_NO_LOCAL_TYPED_VIEW_RUNTIME_CLAIM
```

The baked ZIP contains the G6 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` were unavailable and the parent G5 receipt is still source-baked without runtime read PASS, so no local compile claim or typed-view runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G6_SELECTED_SLICE_SHAPE_DTYPE_DECODE_PROBE
```

G6 reaches runtime PASS only when a concrete G5 bounded-read PASS receipt is accepted, the source contract provides a recognized dtype and explicit positive shape, and the computed dtype byte width multiplied by checked shape element count exactly matches the G5 bounded read length without tensor value materialization, GPU upload, forward, backward, optimizer, weight mutation, checkpoint mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G7
Selected Slice GPU Upload Candidate /
Typed Tensor View Candidate To Staging Buffer Descriptor
No Bind No Dispatch No Forward
```
