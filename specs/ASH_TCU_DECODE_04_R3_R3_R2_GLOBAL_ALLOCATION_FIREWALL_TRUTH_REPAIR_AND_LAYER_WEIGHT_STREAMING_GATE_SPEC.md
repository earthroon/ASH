# ASH-TCU-DECODE-04-R3-R3-R2 SPEC

## GLOBAL_ALLOCATION_FIREWALL_TRUTH_REPAIR_AND_LAYER_WEIGHT_STREAMING_GATE

```text
patch_id=ASH-TCU-DECODE-04-R3-R3-R2_GLOBAL_ALLOCATION_FIREWALL_TRUTH_REPAIR_AND_LAYER_WEIGHT_STREAMING_GATE
parent_execution_id=decode04r3r3-f9b2fb6c901fb5ba8381
parent_status=PASS_ASH_TCU_DECODE_04_R3_R3_OVERLAY_AWARE_FINAL_PROJECTION_INPUT_RECOVERY_AND_R2_PARITY_RERUN_GATE
parent_verdict=decode04_r3_r3_overlay_repaired_final_projection_recovered_burn_tensorcube_tile0_parity_pass
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
parent_numerical_parity_valid=true
parent_allocation_firewall_sealed=false
production_authority=false
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R3_R3_R2_GLOBAL_ALLOCATION_FIREWALL_TRUTH_REPAIR_AND_LAYER_WEIGHT_STREAMING_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R3_R3_R2_GLOBAL_ALLOCATION_FIREWALL_TRUTH_REPAIR_AND_LAYER_WEIGHT_STREAMING_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R3_R3_R2_GLOBAL_ALLOCATION_FIREWALL_TRUTH_REPAIR_AND_LAYER_WEIGHT_STREAMING_GATE
PASS_VERDICT=decode04_r3_r3_r2_global_allocation_truth_sealed_layer_weight_streaming_parity_pass
```

R3-R3 numerical recovery remains valid. Its global allocation claim is classified UNSEALED because the same run logged 46,137,344-byte FFN allocations while claiming a 16,777,216-byte single-allocation ceiling.

## Runtime owner

The canonical R3-R3-R2 binary must not call the monolithic `NativeWgpuModel` full-layer bootstrap. It owns a bounded raw-WGPU stream arena after one device bootstrap.

```text
full_transformer_gpu_bootstrap_count=0
full_checkpoint_payload_scan_count=0
full_checkpoint_copy_count=0
full_checkpoint_sha256_recompute_count=0
embedding_mode=single_row_range_read
lm_head_mode=tile0_only
```

## Global allocation truth

All explicit buffers created by the canonical stream arena are registered before creation and released before final sealing.

Required observed owners:

```text
staging_slot_0
staging_slot_1
weight_tile
input_activation
output_activation
output_readback
linear_params
```

The device-bootstrap runtime's private infrastructure is explicitly outside this receipt and must be labeled exempt. The receipt may not call that hidden scope observed.

```text
observer_active=true
physical_allocation_scope=canonical_stream_arena_after_device_bootstrap
bootstrap_runtime_internal_allocations=explicitly_exempt_and_not_claimed
event_replay_matches_receipt=true
```

Hard limits:

```text
max_single_requested_bytes<=8388608
max_stream_arena_live_bytes<=67108864
allocation_request_gt_8388608_count=0
allocation_request_16777216_count=0
allocation_request_46137344_count=0
allocation_request_395337728_count=0
```

## Allocation event and lease receipt

Every physical allocation records:

```text
allocation_id
owner_kind
owner_id
requested_bytes
released
```

Every logical weight tile lease records:

```text
lease_id
layer_index
operator_role
tile_index
source_bytes
staging_slot
released
```

Final conditions:

```text
unreleased_transformer_weight_lease_count=0
max_live_transformer_layer_count<=1
max_live_operator_group_count<=1
allocation_event_digest=<sha256>
lease_event_digest=<sha256>
```

## Safetensors streaming

The checkpoint is opened through a bounded header and range reader.

```text
header_parse_count=1
full_file_materialization_count=0
range_read_only=true
```

The exact-four overlay remains the only owner of:

```text
model.layers.20.post_attention_layernorm.weight
model.layers.21.input_layernorm.weight
model.layers.21.post_attention_layernorm.weight
model.norm.weight
```

```text
overlay_resolved_tensor_count=4
base_resolved_target_tensor_count=0
silent_fallback_count=0
```

## Canonical stream arena

```text
staging_slot_count=2
staging_slot_capacity_bytes=8388608
weight_tile_capacity_bytes=8388608
max_input_elements=5632
max_output_elements=2048
```

A single reusable raw-WGPU linear pipeline consumes row-major f32 tiles. Each tile is uploaded into alternating staging slots, copied to the bounded weight buffer, dispatched, read back, and its logical lease released before the next operator group.

## Attention streaming

```text
q_proj_shape=[2048,2048]
q_tile_shape=[1024,2048]
q_tile_count=2
k_proj_shape=[256,2048]
k_tile_count=1
v_proj_shape=[256,2048]
v_tile_count=1
o_proj_shape=[2048,2048]
o_tile_shape=[1024,2048]
o_tile_count=2
```

For the canonical smoke token, sequence length is one and position is zero. Therefore the attention softmax has one element and RoPE at position zero is identity. GQA context is the exact repeated V head mapping.

## FFN streaming

Logical gate/up grouping:

```text
intermediate_size=5632
logical_group_channels=1024
logical_group_count=6
full_gate_up_tile_shape=[1024,2048]
full_gate_up_tile_bytes=8388608
tail_gate_up_tile_shape=[512,2048]
tail_gate_up_tile_bytes=4194304
```

Physical down projection clarification:

Safetensors stores down projection as contiguous row-major `[2048,5632]`. Input-channel slices would require strided range reads. The canonical implementation therefore uses contiguous output-row tiles without changing the mathematical result.

```text
down_projection_physical_tiling=contiguous_output_row_tiles
down_tile_shape=[256,5632]
down_tile_count=8
down_tile_bytes=5767168
```

This physical clarification supersedes only the down-projection tile axis in the long-form draft. The 8MiB ceiling, logical six-group SwiGLU evaluation, deterministic accumulation, and parity requirements remain unchanged.

## Layer lifecycle

For each layer 0 through 21:

```text
read input norm
RMSNorm
stream Q/K/V
construct exact seq1 GQA context
stream O
residual add
read post-attention norm
RMSNorm
stream gate/up logical groups
SiLU(gate)*up
stream down output-row tiles
residual add
release all layer weight leases
seal layer receipt
```

```text
layer_count=22
layer_stream_pass_count=22
max_live_transformer_layer_count=1
max_live_operator_group_count=1
```

## Recovery preservation

```text
final_norm_output_nonzero_count=2048
final_projection_input_nonzero_count=2048
final_projection_input_digest=final_norm_output_digest
non_finite_count=0
```

## Projection parity

The parent R3-R3 Burn/TensorCube tile0 parity must be PASS. The new streaming runtime additionally compares its raw-WGPU LM-head tile0 output with a same-input same-RHS CPU f32 reference.

```text
parent_burn_tensorcube_parity_pass=true
current_gpu_cpu_compared_element_count=1024
current_gpu_cpu_mismatch_count=0
current_gpu_cpu_non_finite_pair_count=0
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
```

This gate claims preservation of the parent Burn/TensorCube route plus current streamed GPU/reference parity. It does not relabel the CPU reference as Burn.

## Artifacts

```text
manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r2_local_manifest_latest.json
allocation_trace=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r2_allocation_trace_latest.jsonl
layer_stream_trace=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r2_layer_stream_trace_latest.json
parity_receipt=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_r2_parity_receipt_latest.json
manifest_schema=ash_tensorcube_decode04_r3_r3_r2_global_allocation_and_layer_stream_v1
```

## Authority firewall

```text
production_checkpoint_replacement_count=0
default_pointer_change_count=0
sampler_use_count=0
token_commit_count=0
kv_cache_persist_count=0
runtime_output_changed=false
decode05_authorized=false
```

## Binary

```text
ash_tcu_decode_04_r3_r3_r2_global_allocation_firewall_truth_repair_and_layer_weight_streaming_gate
```

## Exit codes

```text
0=PASS allocation truth and layer streaming sealed
2=HOLD incomplete GPU, staging, I/O, telemetry, or readback evidence
1=FAIL allocation, lease, parity, recovery, or authority violation
```

## Promotion boundary

PASS authorizes R4 fused final RMSNorm, grouped LM-head and top-k shadow implementation. It does not authorize production checkpoint replacement, production route switching, sampler changes, token commit, KV persistence, or DECODE-05 promotion.
