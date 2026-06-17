# ASH-BASETRAIN-GPU-70K-G10 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G10
Controlled Minimal Forward Surface Execution Candidate /
Single Selected Group Input Surface To Forward Smoke Gate
No Backward No Optimizer No Delta Commit
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G9` single-selected-group minimal forward surface descriptor to create a controlled minimal forward smoke gate candidate.

G10 is a forward-smoke gate candidate patch, not a forward execution patch. It may validate input surface lineage, runtime handoff requirements, and no-backward/no-optimizer/no-delta boundaries, but it must not create shaders, bind groups, dispatch kernels, execute forward, materialize logits, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent read probe: `ASH-BASETRAIN-GPU-70K-G5`
- Parent typed-view probe: `ASH-BASETRAIN-GPU-70K-G6`
- Parent upload candidate: `ASH-BASETRAIN-GPU-70K-G7`
- Parent upload smoke: `ASH-BASETRAIN-GPU-70K-G8`
- Parent forward boundary: `ASH-BASETRAIN-GPU-70K-G9`
- Current patch: `ASH-BASETRAIN-GPU-70K-G10`
- Next patch: `ASH-BASETRAIN-GPU-70K-G11`
- New permission candidate: controlled minimal forward smoke gate candidate only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g10_controlled_minimal_forward_surface_execution_candidate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g10_controlled_minimal_forward_surface_execution_candidate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G10_CONTROLLED_MINIMAL_FORWARD_SURFACE_EXECUTION_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_FORWARD_SMOKE_GATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_FORWARD_INPUT_BINDING_INTENT_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_RUNTIME_HANDOFF_REQUIREMENT_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_NO_BACKWARD_OPTIMIZER_DELTA_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G10_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- forward output dumps
- logits dumps
- loss reports
- runtime benchmark reports

## Allowed in G10 runtime probe

- G4-R2 freeze receipt read
- G5 bounded-read receipt read
- G6 typed-view receipt read
- G7 upload-candidate receipt read
- G8 upload/readback parity receipt read
- G9 forward-boundary receipt read
- G9 minimal-forward-surface audit read
- selected tensor key and digest lineage verification
- input bytes consistency check
- controlled forward smoke gate descriptor creation
- runtime handoff requirement audit
- no-backward/no-optimizer/no-delta audit

## Forbidden in G10

- payload file reopen
- selected bytes reread
- full tensor load
- tensor value materialization
- shader module creation
- bind group creation
- dispatch execution
- actual forward execution
- logits materialization
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G10_CONTROLLED_MINIMAL_FORWARD_SURFACE_EXECUTION_CANDIDATE_READY_NO_LOCAL_FORWARD_GATE_RUNTIME_CLAIM
```

The baked ZIP contains the G10 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G9/G8 runtime PASS evidence were unavailable, so no local compile claim or controlled forward-smoke gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G10_CONTROLLED_MINIMAL_FORWARD_SURFACE_EXECUTION_CANDIDATE
```

G10 reaches runtime PASS only when a concrete G9 single-selected-group minimal forward surface descriptor is accepted, G8 upload/readback parity lineage remains intact, and a controlled minimal forward smoke gate candidate is created without payload reread, tensor value materialization, shader creation, bind group creation, dispatch, actual forward execution, logits materialization, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G11
Controlled Minimal Forward Smoke Execution /
Single Selected Group Forward Gate To Dispatch Receipt
No Backward No Optimizer No Delta Commit
```
