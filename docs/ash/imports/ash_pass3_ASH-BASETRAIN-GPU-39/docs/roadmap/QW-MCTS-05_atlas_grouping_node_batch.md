# QW-MCTS-05 — Atlas Grouping Node Batch Layout / VTC16 Consumer Seal

## SSOT
- `crates/model_core/src/qw_mcts_atlas_grouping_node_batch.rs`
- Consumes QW-MCTS-00 episode, QW-MCTS-01 reward batch, QW-MCTS-02 HDC batch, QW-MCTS-03 liquid batch, QW-MCTS-04 spike batch.

## Contract
- Atlas group size: 16 nodes.
- Feature channels: 16.
- Matrix shape: `[16, 16]`.
- Tile mode receipt: `Tile16LogicalFromTile8`.
- Reuses existing 8x8 layout.
- Does not create contiguous physical 16x16 tile.

## Forbidden
- GPU dispatch, `wgpu queue.write_buffer`, backend mutation.
- Node selection authority, pruning authority, runtime decode authority, value authority.
- Hard ban, token mask, vocab removal.
- Value Network call/training, model/checkpoint/LoRA/optimizer mutation.
- Training data export, Arrow/Parquet export.

## Next
QW-MCTS-06 — Atlas Grouping Backend Bridge / No GPU Dispatch Seal.
