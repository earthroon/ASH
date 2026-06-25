# ASH-BASETRAIN-GPU-70K-G167-R1

## Compile Fix / Rust Match Guard Syntax Rebind / Hold Mode Parser Warning Cleanup

PatchId: `ASH-BASETRAIN-GPU-70K-G167-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G167`

G167-R1 fixes a Rust compile blocker in the G167 tiny training smoke gate.

## Fixes

```text
_ when <condition> => ...
```

was replaced with valid Rust match guard syntax:

```text
_ if <condition> => ...
```

The duplicate hold-mode match arm that produced an unreachable-pattern warning was also collapsed to a single `hold` parser arm.

## Scope

No semantic expansion.

No artifact output directory included.

No operator approval directory included.

No `.ps1`, `.py`, or `.sha256` files included in the ZIP.

G167 runtime behavior remains:

```text
FreshInit Tiny Multi-Step Training Smoke /
Finite Loss Grad Delta Receipt /
Scoped Runtime Mutation
```

## Cargo run command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g167_freshinit_tiny_multi_step_training_smoke -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G166 `
  --training-smoke-mode freshinit-tiny-multi-step `
  --selected-path freshinit-burn-native-tiny-proof `
  --deferred-path atlas-grouped-sequential-integration-candidate `
  --tiny-step-count 2 `
  --tiny-batch-count 1 `
  --mutation-scope freshinit-tiny-runtime-scoped `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --route-pointer-write-mode forbid `
  --training-completion-mode hold `
  --deployment-ready-mode hold
```
