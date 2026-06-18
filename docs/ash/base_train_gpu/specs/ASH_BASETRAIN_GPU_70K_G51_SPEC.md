# ASH-BASETRAIN-GPU-70K-G51

## Patch

```text
ASH-BASETRAIN-GPU-70K-G51
Group Local Finite Loss Candidate /
Forward Logits Candidate To Finite Loss Candidate Seal
No Backward No Optimizer No Weight Commit
```

## Commit

```text
commit: ASH-BASETRAIN-GPU-70K-G51
title: Group Local Finite Loss Candidate
message: base_train: add group local finite loss candidate from logits candidate
```

## Purpose

G51 consumes the G50 group-local logits candidate and creates a finite loss candidate receipt. This patch opens only the metadata-level loss candidate surface. It does not run backward, write gradients, create or run an optimizer, mutate weights, write checkpoints, decode, sample, or generate text.

## Required SSOT Inputs

```text
specs/ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_LOGITS_CANDIDATE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G50_FORWARD_LOGITS_SHAPE_FINITE_AUDIT.json
artifacts/<local_loss_target_fixture>.json
```

Optional lineage inputs:

```text
specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_RESIDENT_CANDIDATE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_FORWARD_INPUT_PACKET.json
```

G51 must not fabricate a loss target fixture.

## State Ownership

G51 writes only JSON receipts under `specs/`. It does not mutate model weights, optimizer state, checkpoint state, tokenizer state, runtime default route state, or committed training state.

## Source Files

```text
crates/base_train/src/ash_basetrain_gpu_70k_g51_group_local_finite_loss_candidate.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g51_group_local_finite_loss_candidate.rs
```

## Cargo Bin

```toml
[[bin]]
name = "ash_basetrain_gpu_70k_g51_group_local_finite_loss_candidate"
path = "src/bin/ash_basetrain_gpu_70k_g51_group_local_finite_loss_candidate.rs"
```

## Receipts

```text
specs/ASH_BASETRAIN_GPU_70K_G51_LOSS_TARGET_BINDING_CANDIDATE.json
specs/ASH_BASETRAIN_GPU_70K_G51_GROUP_LOCAL_FINITE_LOSS_CANDIDATE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G51_LOGITS_TO_TARGET_COMPAT_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_FINITE_LOSS_VALUE_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_NO_BACKWARD_GRADIENT_WRITE_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_NO_OPTIMIZER_WEIGHT_COMMIT_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_NO_CHECKPOINT_MUTATION_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_NO_DECODE_SAMPLING_GENERATION_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_FORBIDDEN_CLAIM_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G51_STATIC_CHECKS.json
specs/ASH_BASETRAIN_GPU_70K_G51_BAKE_MANIFEST.json
specs/ASH_BASETRAIN_GPU_70K_G51_LOCAL_BAKE_VALIDATION.json
```

## PASS Target

```text
PASS_ASH_BASETRAIN_GPU_70K_G51_GROUP_LOCAL_FINITE_LOSS_CANDIDATE
```

PASS requires G50 PASS lineage, selected group match, explicit loss target fixture read, logits-target compatibility, finite loss candidate metadata, and `boundary_failures=0`.

## Incomplete / Failure States

```text
INCOMPLETE_ASH_BASETRAIN_GPU_70K_G51_LOSS_TARGET_FIXTURE_MISSING
FAIL_ASH_BASETRAIN_GPU_70K_G51_G50_LOGITS_LINEAGE_INVALID
FAIL_ASH_BASETRAIN_GPU_70K_G51_LOGITS_TARGET_SHAPE_MISMATCH
FAIL_ASH_BASETRAIN_GPU_70K_G51_NON_FINITE_LOSS_CANDIDATE
FAIL_ASH_BASETRAIN_GPU_70K_G51_BACKWARD_OR_GRADIENT_BOUNDARY_BREACH
FAIL_ASH_BASETRAIN_GPU_70K_G51_OPTIMIZER_OR_WEIGHT_COMMIT_BOUNDARY_BREACH
FAIL_ASH_BASETRAIN_GPU_70K_G51_CHECKPOINT_MUTATION_BOUNDARY_BREACH
```

## Forbidden Boundaries

```text
decode_executed=false
sampling_executed=false
generation_executed=false
text_output_created=false
token_committed=false
sequence_committed=false
backward_executed=false
gradient_write_executed=false
optimizer_created=false
optimizer_executed=false
optimizer_step_executed=false
weight_mutated=false
checkpoint_written=false
checkpoint_mutated=false
checkpoint_alias_rebound=false
runtime_default_route_mutated=false
training_quality_claim=false
model_improvement_claim=false
```

## Runtime CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g51_group_local_finite_loss_candidate -- `
  --g50-logits-candidate .\specs\ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_LOGITS_CANDIDATE_RECEIPT.json `
  --g50-shape-finite-audit .\specs\ASH_BASETRAIN_GPU_70K_G50_FORWARD_LOGITS_SHAPE_FINITE_AUDIT.json `
  --selected-group-id vocab_row_group__lm_head_weight `
  --loss-target-fixture .\artifacts\<local_loss_target_fixture>.json `
  --out-dir specs
```

Fixture missing smoke:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g51_group_local_finite_loss_candidate -- `
  --g50-logits-candidate .\specs\ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_LOGITS_CANDIDATE_RECEIPT.json `
  --g50-shape-finite-audit .\specs\ASH_BASETRAIN_GPU_70K_G50_FORWARD_LOGITS_SHAPE_FINITE_AUDIT.json `
  --selected-group-id vocab_row_group__lm_head_weight `
  --out-dir specs
```

Expected missing fixture status:

```text
INCOMPLETE_ASH_BASETRAIN_GPU_70K_G51_LOSS_TARGET_FIXTURE_MISSING
```

## Packaging Note

The G51 lightweight bake intentionally excludes predecessor runtime receipt files for G48/G49/G50 to avoid overwriting locally generated runtime PASS evidence when the ZIP is unpacked over an active workspace.

## Next Patch

```text
ASH-BASETRAIN-GPU-70K-G52
Gradient Boundary Preflight /
Finite Loss Candidate To Backward Readiness Audit Seal
No Gradient Write No Optimizer No Weight Commit
```
