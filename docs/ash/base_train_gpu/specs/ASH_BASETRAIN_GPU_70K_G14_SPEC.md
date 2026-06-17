# ASH-BASETRAIN-GPU-70K-G14 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G14
Logit Candidate Shape Range TopK Preflight /
Descriptor Only Candidate To Selection Gate
No Token Commit No Decode No Loss
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G13` descriptor-only logit candidate boundary to create a descriptor-only shape/range/top-k preflight and selection gate candidate.

G14 is a preflight patch, not a selection patch. It may check candidate shape, width, vocabulary cap, digest lineage, and numeric range policy, then create a top-k preflight descriptor and selection gate candidate. It must not materialize logits, top-k values, top-k indices, run argmax, run sampling, select tokens, commit tokens, decode text, compute loss, run backward, run optimizer, commit deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent numeric surface: `ASH-BASETRAIN-GPU-70K-G12`
- Parent semantic surface: `ASH-BASETRAIN-GPU-70K-G13`
- Current patch: `ASH-BASETRAIN-GPU-70K-G14`
- Next patch: `ASH-BASETRAIN-GPU-70K-G15`
- New permission candidate: descriptor-only shape/range/top-k preflight and selection gate candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g14_logit_candidate_shape_range_topk_preflight.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g14_logit_candidate_shape_range_topk_preflight.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G14_LOGIT_CANDIDATE_SHAPE_RANGE_TOPK_PREFLIGHT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_LOGIT_CANDIDATE_SHAPE_BOUNDARY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_LOGIT_CANDIDATE_RANGE_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_TOPK_PREFLIGHT_SELECTION_GATE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_OUTPUT_LINEAGE_REBIND_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_NO_TOKEN_COMMIT_DECODE_LOSS_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G14_LOCAL_BAKE_VALIDATION.json`

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
- top-k result dumps
- token selection dumps
- token decode outputs
- loss reports
- gradient dumps
- optimizer state dumps
- runtime benchmark reports

## Allowed in G14 runtime probe

- G13 semantic surface gate receipt read
- G13 logit candidate boundary audit read
- G12 numeric sanity audit read
- output digest lineage check
- candidate shape boundary check
- candidate width and vocabulary cap consistency check
- numeric range policy check
- top-k preflight descriptor creation
- selection gate candidate descriptor creation
- no-token-commit/no-decode/no-loss audit

## Forbidden in G14

- actual logits materialization
- top-k values materialization
- top-k indices materialization
- argmax execution
- sampling execution
- token selection
- token commit
- text decode
- sequence append
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
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G14_LOGIT_CANDIDATE_SHAPE_RANGE_TOPK_PREFLIGHT_READY_NO_LOCAL_TOPK_PREFLIGHT_RUNTIME_CLAIM
```

The baked ZIP contains the G14 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G13 runtime PASS evidence were unavailable, so no local compile claim or top-k preflight runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G14_LOGIT_CANDIDATE_SHAPE_RANGE_TOPK_PREFLIGHT
```

G14 reaches runtime PASS only when the G13 descriptor-only logit candidate boundary is accepted, G12 numeric sanity remains valid, output digest lineage is preserved, candidate shape/range constraints are checked, and a descriptor-only top-k preflight plus selection gate candidate is created without materializing logits, top-k values, top-k indices, argmax, sampling, token selection, token commit, text decode, loss computation, backward, optimizer, delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G15
Controlled Token Selection Candidate Gate /
TopK Preflight Descriptor To Operator Review
No Token Commit No Decode No Loss
```
