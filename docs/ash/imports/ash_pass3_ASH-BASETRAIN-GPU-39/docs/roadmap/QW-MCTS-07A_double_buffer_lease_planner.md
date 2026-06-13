# QW-MCTS-07A — Double Buffer Atlas Lease Planner / No Queue Submit Seal

## SSOT

- 상태 귀속 위치: `crates/model_core/src/qw_mcts_double_buffer_lease_planner.rs`
- 입력 SSOT: `QwMcts06AtlasBackendBridgePayloadBatch`
- 출력 SSOT: `QwMcts07aDoubleBufferLeasePlan`, `QwMcts07aNoQueueSubmitReceipt`
- 재현 가능성: deterministic fixture, no time-dependent hash payload

## Contract

`QW-MCTS-07A` creates a descriptor-only A/B atlas buffer lease plan. It assigns QW-MCTS-06 backend payloads to `CpuPrepare` buffer slots, reserves the alternate buffer as `GpuReserved`, increments swap epoch, and seals stale reuse detection.

It must not create GPU buffers, queue writes, queue submits, command encoders, compute passes, backend mutations, runtime authority, pruning authority, or training/export side effects.

## Required invariants

- `buffer_count == 2`
- `cpu_prepare_buffer_index != gpu_reserved_buffer_index`
- `next_epoch == current_epoch + 1`
- `stale_reuse_guard_active == true`
- `all_payloads_assigned == true`
- `queue_submit_used == false`
- `wgpu_queue_write_used == false`
- `gpu_dispatch_used == false`
- `command_encoder_used == false`
- `compute_pass_used == false`
- `backend_resource_mutation_used == false`

## Next

`QW-MCTS-07B` should calculate upload dry-run byte layout while still blocking queue writes.
