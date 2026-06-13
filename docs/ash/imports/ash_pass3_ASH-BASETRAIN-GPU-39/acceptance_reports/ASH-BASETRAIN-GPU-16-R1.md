# ASH-BASETRAIN-GPU-16-R1 Acceptance

## Verdict

PENDING_OPERATOR_LOCAL_CARGO_BUILD

## Acceptance Criteria

- `cargo build -p base_train --bin ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke --jobs 1` no longer reports E0308/E0277 for `target_dispatch_x`.
- Runtime dispatch scope remains ASH-BASETRAIN-GPU-16 window 2048 dispatch smoke only.
- Readback/staging/map_async remain closed.
- Loss/backward/optimizer/mutation remain closed.
