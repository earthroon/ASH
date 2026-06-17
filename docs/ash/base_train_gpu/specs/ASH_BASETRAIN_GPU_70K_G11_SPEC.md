# ASH-BASETRAIN-GPU-70K-G11 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G11
Controlled Minimal Forward Smoke Execution /
Single Selected Group Forward Gate To Dispatch Receipt
No Backward No Optimizer No Delta Commit
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G10` controlled minimal forward smoke gate candidate as parent evidence and execute a controlled single-selected-group forward smoke when runtime preconditions are satisfied.

G11 is a forward-smoke execution patch, but only inside the single selected group scope. It may create a shader module, bind group layout, bind group, controlled dispatch, and forward output smoke surface. It must not execute full model forward, multi-group forward, materialize semantic logits, select tokens, decode text, compute loss, run backward, create gradients, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent upload smoke: `ASH-BASETRAIN-GPU-70K-G8`
- Parent forward boundary: `ASH-BASETRAIN-GPU-70K-G9`
- Parent forward gate: `ASH-BASETRAIN-GPU-70K-G10`
- Current patch: `ASH-BASETRAIN-GPU-70K-G11`
- Next patch: `ASH-BASETRAIN-GPU-70K-G12`
- New permission candidate: controlled single-selected-group shader/bind/dispatch smoke only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g11_controlled_minimal_forward_smoke_execution.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g11_controlled_minimal_forward_smoke_execution.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G11_CONTROLLED_MINIMAL_FORWARD_SMOKE_EXECUTION.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_FORWARD_DISPATCH_RECEIPT_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_FORWARD_OUTPUT_SURFACE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_SHADER_BIND_DISPATCH_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_NO_BACKWARD_OPTIMIZER_DELTA_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G11_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G11 runtime probe

- G8/G9/G10 receipt reads
- runtime handoff check
- bounded selected-slice reupload when contiguous buffer handoff is unavailable
- input digest verification
- shader module creation
- bind group layout creation
- bind group creation
- controlled single-selected-group dispatch
- dispatch completion receipt
- forward output smoke surface creation
- optional output readback digest

## Forbidden in G11

- full tensor load
- full safetensors deserialize
- unbounded payload read
- full model forward
- multi-group forward
- semantic logits materialization
- token selection
- text decode
- loss computation
- loss backward
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G11_CONTROLLED_MINIMAL_FORWARD_SMOKE_EXECUTION_READY_NO_LOCAL_FORWARD_DISPATCH_RUNTIME_CLAIM
```

The baked ZIP contains the G11 source/runtime probe surface and metadata receipts. The source contains the gated shader/bind/dispatch smoke path, but in the current bake environment `cargo`/`rustc`, concrete G10/G8 runtime PASS evidence, payload path, and GPU execution evidence were unavailable, so no local compile claim or controlled forward-dispatch runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G11_CONTROLLED_MINIMAL_FORWARD_SMOKE_EXECUTION
```

G11 reaches runtime PASS only when the G10 controlled minimal forward smoke gate is accepted, runtime handoff or bounded reupload supplies the single selected group input surface, a controlled single-selected-group shader/bind/dispatch smoke completes, and a forward output surface receipt is created without full model forward, multi-group forward, semantic logits materialization, token selection, text decode, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G12
Forward Output Surface Validation /
Controlled Dispatch Output Numeric Sanity Boundary
No Backward No Optimizer No Delta Commit
```
