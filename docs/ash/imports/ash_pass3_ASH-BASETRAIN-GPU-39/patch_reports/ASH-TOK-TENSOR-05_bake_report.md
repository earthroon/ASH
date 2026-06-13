# ASH-TOK-TENSOR-05 Bake Report

## Summary

Baked full snapshot readback guard on top of ASH-TOK-TENSOR-04. This patch changes the default full snapshot route from unguarded snapshot collection to explicit-gate snapshot collection.

## Modified Runtime Files

- `crates/base_train/src/config.rs`
- `crates/base_train/src/checkpoint.rs`
- `crates/base_train/src/training.rs`
- `crates/base_train/src/lib.rs`
- `crates/base_train/src/pipeline.rs`

## Added Receipt Files

- `crates/model_core/src/ash_tok_tensor_05_basetrain_full_snapshot_guard.rs`
- `crates/model_core/src/bin/ash_tok_tensor_05_basetrain_full_snapshot_guard.rs`
- `ASH_TOK_TENSOR_05_FULL_SNAPSHOT_GUARD_RECEIPT.json`
- `ASH_TOK_TENSOR_05_FULL_SNAPSHOT_GUARD_CONTRACT.json`
- `ASH_TOK_TENSOR_05_STATIC_CHECKS.txt`
- `ASH_TOK_TENSOR_05_LOCAL_VALIDATION.txt`

## Closed

- `collect_full_checkpoint_snapshots` before save guard
- full embedding/lm_head/layer CPU readback without gate
- unconditional full snapshot execution

## Preserved

- adapter checkpoint path
- atlas group delta config path
- group receipt config path

## Verdict

```txt
PASS_ASH_TOK_TENSOR_05_BASETRAIN_FULL_SNAPSHOT_GUARD_NO_UNCONDITIONAL_FULL_READBACK
```
