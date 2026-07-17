# ASH-TCU-DECODE-04-R3-R3-R3

## CHECKPOINT_RANGE_COALESCING_ASYNC_PREFETCH_AND_UPLOAD_OVERLAP_GATE

```text
patch_id=ASH-TCU-DECODE-04-R3-R3-R3_CHECKPOINT_RANGE_COALESCING_ASYNC_PREFETCH_AND_UPLOAD_OVERLAP_GATE
parent_execution_id=decode04r3r3r2-0fe4fd19011814e6b9c4
parent_status=PASS_ASH_TCU_DECODE_04_R3_R3_R2_GLOBAL_ALLOCATION_FIREWALL_TRUTH_REPAIR_AND_LAYER_WEIGHT_STREAMING_GATE
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
parent_range_read_count=615
parent_total_runtime_ms=37304.092
production_authority=false
```

## Canonical contract

The safetensors header is parsed once. Tensor and tile ranges are indexed by absolute payload offset and coalesced only inside execution-compatible phases. Coalesced members retain exact offsets, sizes and digests. Gap bytes may be read but are never consumed as tensor payload.

```text
max_coalesce_gap_bytes=65536
max_coalesced_span_bytes=33554432
read_amplification_ratio<=1.05
checkpoint_range_read_count<615
member_byte_parity=true
```

The host prefetch scheduler is bounded and uses fixed reusable slots.

```text
io_backend=bounded_blocking_thread_fixed_host_slots
host_prefetch_slot_count=3
host_prefetch_slot_capacity_bytes=33554432
max_inflight_read_count<=2
max_queued_read_count=3
max_prefetch_layer_distance<=1
max_prefetched_future_span_count<=1
```

The parent 8MiB GPU allocation firewall and two-slot staging ring remain active.

```text
gpu_staging_slot_count=2
gpu_staging_slot_capacity_bytes=8388608
max_single_gpu_allocation_bytes=8388608
max_gpu_stream_arena_live_bytes=67108864
allocation_request_gt_8388608_count=0
```

Overlap is true only when measured intervals intersect.

```text
io_compute_overlap_ms=max(0,min(read_end,compute_end)-max(read_start,compute_start))
upload_compute_overlap_ms=max(0,min(upload_end,compute_end)-max(upload_start,compute_start))
timestamp_evidence_complete=true
overlapped_operator_group_count>0
slot_epoch_violation_count=0
```

## Preserved parent invariants

```text
layer_count=22
layer_stream_pass_count=22
max_live_transformer_layer_count<=1
max_live_operator_group_count<=1
unreleased_transformer_weight_lease_count=0
overlay_resolved_tensor_count=4
base_resolved_target_tensor_count=0
final_projection_input_nonzero_count=2048
parent_burn_tensorcube_parity_pass=true
current_gpu_cpu_mismatch_count=0
runtime_output_changed=false
```

## Performance gate

```text
target_checkpoint_range_read_count<=220
target_cold_runtime_ms<=30000
target_warm_runtime_ms<=15000
target_overlap_ratio>=0.60
current_total_runtime_ms<37304.092
```

A single-run result is provisional. A sealed cold or warm claim requires an explicit cache protocol or a multi-run median.

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R3_R3_R3_CHECKPOINT_RANGE_COALESCING_ASYNC_PREFETCH_AND_UPLOAD_OVERLAP_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R3_R3_R3_CHECKPOINT_RANGE_COALESCING_ASYNC_PREFETCH_AND_UPLOAD_OVERLAP_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R3_R3_R3_CHECKPOINT_RANGE_COALESCING_ASYNC_PREFETCH_AND_UPLOAD_OVERLAP_GATE
PASS_VERDICT=decode04_r3_r3_r3_checkpoint_ranges_coalesced_prefetch_upload_overlap_parity_pass
```

## Artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r3_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r3_range_coalescing_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r3_io_trace_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r3_overlap_trace_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r3_layer_receipts_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r3_parity_receipt_latest.json
```

PASS authorizes only R4 shadow work. Production route switching, checkpoint rewriting, sampler changes, token commit, KV persistence and DECODE-05 promotion remain forbidden.
