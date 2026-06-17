# ASH-BASETRAIN-GPU-70K-G13 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G13
Forward Output Semantic Surface Gate /
Numeric Surface To Logit Candidate Boundary
No Token Selection No Loss No Backward
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G12` numeric output surface validation receipt to create a descriptor-only semantic surface gate and logit candidate boundary.

G13 is a semantic surface gate patch, not a token selection or decode patch. It may rebind a validated numeric output surface as a descriptor-only logit candidate boundary, but it must not materialize semantic logits, claim a token distribution, perform top-k/argmax/sampling, select tokens, decode text, compute loss, run backward, create gradients, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent dispatch smoke: `ASH-BASETRAIN-GPU-70K-G11`
- Parent numeric surface: `ASH-BASETRAIN-GPU-70K-G12`
- Current patch: `ASH-BASETRAIN-GPU-70K-G13`
- Next patch: `ASH-BASETRAIN-GPU-70K-G14`
- New permission candidate: descriptor-only logit candidate boundary creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g13_forward_output_semantic_surface_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g13_forward_output_semantic_surface_gate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G13_FORWARD_OUTPUT_SEMANTIC_SURFACE_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_LOGIT_CANDIDATE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_SEMANTIC_SURFACE_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_NO_TOKEN_SELECTION_LOSS_BACKWARD_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_OUTPUT_LINEAGE_REBIND_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G13_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- delta packets
- semantic logits dumps
- token selection dumps
- token decode outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G13 runtime probe

- G12 output validation receipt read
- G12 numeric sanity audit read
- output surface metadata read
- numeric sanity pass check
- output digest lineage check
- semantic surface gate descriptor creation
- logit candidate boundary descriptor creation
- descriptor-only semantic boundary seal

## Forbidden in G13

- output bytes semantic materialization into real logits
- token distribution claim
- top-k selection
- argmax selection
- sampling
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G13_FORWARD_OUTPUT_SEMANTIC_SURFACE_GATE_READY_NO_LOCAL_SEMANTIC_GATE_RUNTIME_CLAIM
```

The baked ZIP contains the G13 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G12 runtime PASS evidence were unavailable, so no local compile claim or semantic surface gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G13_FORWARD_OUTPUT_SEMANTIC_SURFACE_GATE
```

G13 reaches runtime PASS only when a concrete G12 numeric output surface validation receipt is accepted, output digest lineage is preserved, and a descriptor-only logit candidate boundary is created without semantic logits materialization, top-k selection, argmax selection, sampling, token selection, text decode, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G14
Logit Candidate Shape Range TopK Preflight /
Descriptor Only Candidate To Selection Gate
No Token Commit No Decode No Loss
```
