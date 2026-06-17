# ASH-BASETRAIN-GPU-70K-G12 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G12
Forward Output Surface Validation /
Controlled Dispatch Output Numeric Sanity Boundary
No Backward No Optimizer No Delta Commit
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G11` controlled minimal forward smoke dispatch receipt and forward output surface receipt to validate a bounded numeric smoke surface.

G12 is an output-surface validation patch. It may check output byte length, digest lineage, dtype/shape boundary, finite/NaN/Inf numeric sanity, and limited range summary. It must not reexecute dispatch, create shaders, create bind groups, materialize semantic logits, select tokens, decode text, compute loss, run backward, create gradients, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent upload smoke: `ASH-BASETRAIN-GPU-70K-G8`
- Parent forward boundary: `ASH-BASETRAIN-GPU-70K-G9`
- Parent forward gate: `ASH-BASETRAIN-GPU-70K-G10`
- Parent dispatch smoke: `ASH-BASETRAIN-GPU-70K-G11`
- Current patch: `ASH-BASETRAIN-GPU-70K-G12`
- Next patch: `ASH-BASETRAIN-GPU-70K-G13`
- New permission candidate: forward output surface numeric sanity validation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g12_forward_output_surface_validation.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g12_forward_output_surface_validation.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G12_FORWARD_OUTPUT_SURFACE_VALIDATION.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_OUTPUT_NUMERIC_SANITY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_OUTPUT_DTYPE_SHAPE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_OUTPUT_DIGEST_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_NO_LOGITS_LOSS_BACKWARD_OPTIMIZER_DELTA_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G12_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- semantic logits dumps
- token decode outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G12 runtime probe

- G11 forward smoke receipt read
- G11 forward output surface audit read
- output surface metadata validation
- bounded output readback scan when available
- output byte length check
- output digest lineage check
- dtype/shape boundary check
- finite/NaN/Inf scan
- min/max/mean_abs numeric summary
- numeric sanity verdict creation

## Forbidden in G12

- payload file reopen
- selected input bytes reread
- full tensor load
- forward dispatch reexecution
- shader module creation
- bind group creation
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G12_FORWARD_OUTPUT_SURFACE_VALIDATION_READY_NO_LOCAL_OUTPUT_NUMERIC_RUNTIME_CLAIM
```

The baked ZIP contains the G12 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc`, concrete G11 runtime PASS evidence, concrete output readback bytes, and GPU execution evidence were unavailable, so no local compile claim or output numeric validation runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G12_FORWARD_OUTPUT_SURFACE_VALIDATION
```

G12 reaches runtime PASS only when a concrete G11 controlled minimal forward smoke dispatch receipt is accepted, the forward output surface exists, output bytes are bounded, output digest lineage is preserved, finite/NaN/Inf numeric sanity checks pass, and no semantic logits materialization, token selection, text decode, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim occurs.

## Next

```text
ASH-BASETRAIN-GPU-70K-G13
Forward Output Semantic Surface Gate /
Numeric Surface To Logit Candidate Boundary
No Token Selection No Loss No Backward
```
