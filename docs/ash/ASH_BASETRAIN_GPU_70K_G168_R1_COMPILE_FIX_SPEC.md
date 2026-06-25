# ASH-BASETRAIN-GPU-70K-G168-R1

## Compile Fix / Duplicate G168 Verdict Variant Removal / No Semantic Expansion

PatchId: `ASH-BASETRAIN-GPU-70K-G168-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G168`

G168-R1 fixes a Rust compile blocker in the G168 repeatability guard.

## Fix

`G168Verdict::BlockedMutationScopeMismatch` was declared twice in the `G168Verdict` enum. Rust rejects duplicate enum variant definitions, and the serde derive surfaced the enum coverage failure during compile.

R1 removes the duplicated variant declaration and keeps the single canonical variant used by the runtime guard:

```rust
_ if input.mutation_scope != MUTATION_SCOPE => G168Verdict::BlockedMutationScopeMismatch,
```

## Scope

No semantic expansion.

No runtime contract change.

No output artifact contract change.

No checkpoint write.

No safetensors write.

No base weight mutation.

No route pointer rewrite.

No training completion claim.

## Expected command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g168_freshinit_tiny_training_repeatability_guard -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G167 `
  --repeatability-mode freshinit-tiny-training-repeat `
  --selected-path freshinit-burn-native-tiny-proof `
  --deferred-path atlas-grouped-sequential-integration-candidate `
  --tiny-step-count 2 `
  --tiny-batch-count 1 `
  --mutation-scope freshinit-tiny-runtime-scoped `
  --compare-mode exact-or-tolerance-bounded `
  --loss-abs-tolerance 0.000001 `
  --grad-norm-abs-tolerance 0.000001 `
  --delta-norm-abs-tolerance 0.000001 `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --route-pointer-write-mode forbid `
  --training-completion-mode hold `
  --deployment-ready-mode hold
```
