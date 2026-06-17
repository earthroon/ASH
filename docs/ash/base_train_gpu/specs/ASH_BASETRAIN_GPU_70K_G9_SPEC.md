# ASH-BASETRAIN-GPU-70K-G9 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G9
Single Selected Group Forward Boundary Probe /
Uploaded Slice Buffer To Minimal Forward Surface
No Backward No Optimizer No Delta Commit
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G8` selected-slice GPU upload/readback parity evidence to create a single-selected-group minimal forward surface descriptor.

G9 is a forward-boundary probe, not a forward execution patch. It may establish the minimal input surface and lineage checks for one selected group, but it must not execute full model forward, multi-group forward, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claims.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent read probe: `ASH-BASETRAIN-GPU-70K-G5`
- Parent typed-view probe: `ASH-BASETRAIN-GPU-70K-G6`
- Parent upload candidate: `ASH-BASETRAIN-GPU-70K-G7`
- Parent upload smoke: `ASH-BASETRAIN-GPU-70K-G8`
- Current patch: `ASH-BASETRAIN-GPU-70K-G9`
- Next patch: `ASH-BASETRAIN-GPU-70K-G10`
- New permission candidate: single-selected-group minimal forward surface descriptor only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g9_single_selected_group_forward_boundary_probe.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g9_single_selected_group_forward_boundary_probe.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G9_SINGLE_SELECTED_GROUP_FORWARD_BOUNDARY_PROBE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_MINIMAL_FORWARD_SURFACE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_UPLOADED_BUFFER_HANDOFF_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_NO_BACKWARD_OPTIMIZER_DELTA_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G9_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- runtime benchmark reports

## Allowed in G9 runtime probe

- G4-R2 freeze receipt read
- G5 bounded-read receipt read
- G6 typed-view receipt read
- G7 upload-candidate receipt read
- G8 upload/readback parity receipt read
- selected tensor key lineage check across G5 through G8
- expected bytes and upload size consistency check
- readback digest and source digest consistency check
- minimal forward surface descriptor creation
- uploaded buffer handoff audit
- no-backward/no-optimizer/no-delta audit

## Forbidden in G9

- payload file reopen
- selected bytes reread
- full tensor load
- tensor value materialization
- full model forward
- multi-group forward
- loss computation
- backward
- gradient materialization
- optimizer state creation
- optimizer step
- delta materialization
- delta commit
- checkpoint mutation
- weight mutation
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G9_SINGLE_SELECTED_GROUP_FORWARD_BOUNDARY_PROBE_READY_NO_LOCAL_FORWARD_BOUNDARY_RUNTIME_CLAIM
```

The baked ZIP contains the G9 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and a concrete G8 runtime PASS receipt were unavailable, so no local compile claim or forward-boundary runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G9_SINGLE_SELECTED_GROUP_FORWARD_BOUNDARY_PROBE
```

G9 reaches runtime PASS only when a concrete G8 selected-slice GPU upload/readback parity PASS receipt is accepted, selected tensor identity and byte-size lineage remain consistent across G5 through G8, and a single-selected-group minimal forward surface descriptor is created without payload reread, tensor value materialization, full model forward, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G10
Controlled Minimal Forward Surface Execution Candidate /
Single Selected Group Input Surface To Forward Smoke Gate
No Backward No Optimizer No Delta Commit
```
