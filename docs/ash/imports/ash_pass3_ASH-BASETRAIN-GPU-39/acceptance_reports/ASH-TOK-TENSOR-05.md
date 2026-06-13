# ASH-TOK-TENSOR-05 Acceptance Report

## Patch

```txt
ASH-TOK-TENSOR-05
BaseTrain Full Snapshot Guard /
No Unconditional Full Readback Seal
```

## SSOT

`save_full_checkpoint=false` is not permission to collect a full checkpoint snapshot. Full CPU readback requires an explicit `FullSnapshotGate` approval path.

## Accepted State

- `FullSnapshotGate` added to `base_train` runtime config.
- `allow_full_snapshot_readback=false` by default.
- `require_explicit_full_snapshot_approval=true` by default.
- `training.rs` uses `collect_full_checkpoint_snapshots_guarded(...)` only inside `save_full_checkpoint` branches.
- Adapter checkpoint route remains present.
- Atlas group delta and group receipt config fields remain present.
- No safetensors load, row parity probe, model forward, optimizer step, or weight commit is executed by this patch.

## Verdict

```txt
PASS_ASH_TOK_TENSOR_05_BASETRAIN_FULL_SNAPSHOT_GUARD_NO_UNCONDITIONAL_FULL_READBACK
```
