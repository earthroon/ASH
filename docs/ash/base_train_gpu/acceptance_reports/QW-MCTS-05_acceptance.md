# QW-MCTS-05 Acceptance

- PASS: atlas group size is 16.
- PASS: feature channels are 16.
- PASS: matrix shape is [16,16].
- PASS: row-major matrix length is 256 per group.
- PASS: Tile16LogicalFromTile8 consumer receipt is emitted.
- PASS: existing 8x8 layout reuse is true.
- PASS: contiguous physical 16x16 tile creation is false.
- PASS: GPU dispatch, queue write, backend mutation are false.
- PASS: value/node/pruning/runtime authority are false.
- PASS: hard ban, token mask, vocab removal are false.
- PASS: training mutation and Arrow export are false.
