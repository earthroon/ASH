# QW-MCTS-06 — Atlas Grouping Backend Bridge / No GPU Dispatch Seal

## 확정

QW-MCTS-05의 atlas grouping node batch를 logical VTC16 backend bridge payload로 변환한다. 이 패치는 payload/validation/receipt까지만 생성하며 실제 GPU dispatch, `wgpu queue.write_buffer`, command encoder, compute pass, backend resource mutation은 금지한다.

## 상태 귀속 위치

- 신규 SSOT: `crates/model_core/src/qw_mcts_atlas_backend_bridge.rs`
- 입력 SSOT: `crates/model_core/src/qw_mcts_atlas_grouping_node_batch.rs`
- backend 계약: `Tile16LogicalFromTile8`, 기존 8x8 physical layout 재사용

## Acceptance

- payload_count == group_count
- matrix_shape == [16, 16]
- matrix_row_major_len == 256
- tile_mode_requested == `Tile16LogicalFromTile8`
- uses_existing_tile8x8_layout == true
- creates_contiguous_16x16_tile == false
- creates_new_physical_16x16_kernel == false
- gpu_dispatch_used == false
- wgpu_queue_write_used == false
- command_encoder_used == false
- compute_pass_used == false
- backend_resource_mutation_used == false
- authority/training/export flags false

## Next

QW-MCTS-07A — Double Buffer Atlas Lease Planner / No Queue Submit Seal
