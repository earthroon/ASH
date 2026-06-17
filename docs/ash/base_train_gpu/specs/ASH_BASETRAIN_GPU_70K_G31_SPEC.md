# ASH-BASETRAIN-GPU-70K-G31 Brief Spec

## Patch

```text
ASH-BASETRAIN-GPU-70K-G31
Output Stability Ledger Replay Gate /
Stability Ledger To Deterministic Display Replay Candidate
No Loss No Backward No Optimizer
```

## Purpose

Use the `ASH-BASETRAIN-GPU-70K-G30` display surface regression audit and output stability ledger to create an output stability ledger replay gate and deterministic display replay candidate.

G31 is a replay gate and replay candidate patch, not a replay execution, display surface write/rewrite, new final output, training, loss, backward, optimizer, model-delta, checkpoint, or weight mutation patch. It may accept the output stability ledger, accept the display surface regression audit, accept the display surface digest replay audit, create an output stability ledger replay gate, and create a deterministic display replay candidate. It must not emit a new final output, write or rewrite the display surface, create loss targets, compute loss, run backward, run optimizer, materialize or commit model deltas, mutate checkpoints, mutate weights, or claim model quality.

## SSOT

- Domain: `subtitle_translation_assist`
- Parent freeze: `ASH-BASETRAIN-GPU-70K-G4-R2`
- Parent display surface seal: `ASH-BASETRAIN-GPU-70K-G29`
- Parent output stability ledger: `ASH-BASETRAIN-GPU-70K-G30`
- Current patch: `ASH-BASETRAIN-GPU-70K-G31`
- Next patch: `ASH-BASETRAIN-GPU-70K-G32`
- New permission candidate: output stability ledger replay gate and deterministic display replay candidate creation only

## Included in baked ZIP

- `crates/base_train/src/ash_basetrain_gpu_70k_g31_output_stability_ledger_replay_gate.rs`
- `crates/base_train/src/bin/ash_basetrain_gpu_70k_g31_output_stability_ledger_replay_gate.rs`
- `specs/ASH_BASETRAIN_GPU_70K_G31_OUTPUT_STABILITY_LEDGER_REPLAY_GATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_DETERMINISTIC_DISPLAY_REPLAY_CANDIDATE.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_OUTPUT_STABILITY_LEDGER_LINEAGE_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_REPLAY_CANDIDATE_DIGEST_PROJECTION_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_NO_SURFACE_REWRITE_LOSS_BACKWARD_OPTIMIZER_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_REPLAY_GATE_POLICY_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_FORBIDDEN_CLAIM_AUDIT.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_STATIC_CHECKS.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_BAKE_MANIFEST.json`
- `specs/ASH_BASETRAIN_GPU_70K_G31_LOCAL_BAKE_VALIDATION.json`

## Explicitly not included in baked ZIP

- This markdown spec
- `docs/`
- `*.sha256` sidecars
- `*.md` markdown files
- full safetensors payloads
- training dataset payloads
- model checkpoints
- new final text outputs
- display surface write outputs
- display surface rewrite outputs
- loss reports
- gradient dumps
- optimizer state dumps
- model delta packets
- weight dumps
- runtime benchmark reports

## Allowed in G31 runtime probe

- G30 output stability ledger read
- G30 display surface regression audit read
- G30 display surface digest replay audit read
- G29 display surface seal audit read
- output stability ledger acceptance check
- display surface regression audit acceptance check
- display surface digest replay audit acceptance check
- output stability ledger replay gate creation
- deterministic display replay candidate creation
- no-surface-write/no-loss/no-backward/no-optimizer boundary audit

## Forbidden in G31

- new final output emission
- display surface write
- display surface rewrite
- display surface mutation
- loss target creation
- loss computation
- loss backward
- backward execution
- gradient materialization
- optimizer state creation
- optimizer step
- model delta materialization
- model delta commit
- checkpoint mutation
- weight mutation
- runtime default adoption
- model quality claim
- training claim

## Bake status

```text
SOURCE_BAKED_ASH_BASETRAIN_GPU_70K_G31_OUTPUT_STABILITY_LEDGER_REPLAY_GATE_READY_NO_LOCAL_DETERMINISTIC_DISPLAY_REPLAY_RUNTIME_CLAIM
```

The baked ZIP contains the G31 source/runtime probe surface and metadata receipts. In the current bake environment, `cargo`/`rustc` and concrete G30 runtime PASS evidence were unavailable, so no local compile claim or output stability ledger replay gate runtime PASS claim is made.

## Runtime acceptance target

```text
PASS_ASH_BASETRAIN_GPU_70K_G31_OUTPUT_STABILITY_LEDGER_REPLAY_GATE
```

G31 reaches runtime PASS only when the G30 output stability ledger is accepted, the G30 display surface regression audit is accepted, the display surface digest replay audit is accepted, an output stability ledger replay gate is created, and a deterministic display replay candidate is created without new final output emission, display surface write, display surface rewrite, loss target creation, loss computation, backward, optimizer, model delta commit, checkpoint mutation, weight mutation, or model-quality claim.

## Next

```text
ASH-BASETRAIN-GPU-70K-G32
Deterministic Display Replay Execution Smoke /
Replay Candidate To Display Surface Replay Receipt
No Loss No Backward No Optimizer
```
