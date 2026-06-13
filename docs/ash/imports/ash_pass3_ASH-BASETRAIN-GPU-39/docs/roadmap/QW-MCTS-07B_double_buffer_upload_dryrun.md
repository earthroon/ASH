# QW-MCTS-07B — Double Buffer Atlas Upload Dry-run / No Queue Write Seal

## SSOT

- 상태 귀속 위치: `crates/model_core/src/qw_mcts_double_buffer_upload_dryrun.rs`
- 입력 SSOT: `QwMcts06AtlasBackendBridgePayloadBatch`, `QwMcts07aDoubleBufferLeasePlan`
- 출력 SSOT: `QwMcts07bStagingUploadPlan`, `QwMcts07bNoQueueWriteReceipt`
- 재현 가능성: deterministic byte layout, no time-dependent hash payload

## Contract

`QW-MCTS-07B` computes upload byte layouts and range descriptors for double-buffer atlas payloads. Each `[16,16]` f32 payload is sealed as 256 f32 values / 1024 bytes with 256-byte alignment. It validates upload offsets, length alignment, capacity, and overlap while remaining dry-run only.

## Hard bans

- No `wgpu::Buffer` creation.
- No `queue.write_buffer`.
- No `queue.submit`.
- No command encoder.
- No compute pass.
- No GPU dispatch.
- No backend resource mutation.
- No value, node selection, pruning, or runtime authority.
- No training mutation or Arrow export.

## Required invariants

- `matrix_f32_count == 256`
- `matrix_byte_len == 1024`
- `upload_alignment_bytes == 256`
- `payload_layout_count == payload_count`
- `upload_range_count == assignment_count`
- `all_offsets_aligned == true`
- `all_lengths_aligned == true`
- `no_range_overlap == true`
- `all_ranges_within_capacity == true`
- `dryrun_only == true`
- `queue_write_used == false`

## Next

Recommended next patch: `QW-MCTS-08` explicit queue write only / no dispatch, or an optional command candidate seal if an extra dry-run is desired.
