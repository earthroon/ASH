# ASH-TCU-DECODE-04-R4

## FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE

```text
patch_id=ASH-TCU-DECODE-04-R4_FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE
parent_status=PASS_ASH_TCU_DECODE_04_R3_R3_R3_CHECKPOINT_RANGE_COALESCING_ASYNC_PREFETCH_AND_UPLOAD_OVERLAP_GATE
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
production_authority=false
```

## Runtime ownership

R4 reuses the sealed R3-R3-R3 forward and receives a bounded tail state:

```text
pre_final_hidden=2048 f32
parent_final_norm_output=2048 f32
parent_lm_head_group0_weights=1024x2048 f32
```

The ordinary R3-R3-R3 API still returns only its receipt. The tail-state API is consumed only by R4.

## Fused final RMSNorm

```text
final_hidden_upload_count=1
final_norm_weight_source=exact_four_overlay_target_3_model.norm.weight
base_final_norm_weight_use_count=0
compared_element_count=2048
absolute_tolerance=0.0005
relative_tolerance=0.0005
hard_absolute_ceiling=0.005
mismatch_count=0
```

The normalized hidden remains GPU-resident for all LM-head groups.

## LM-head group geometry

```text
vocab_size=48259
hidden_size=2048
group_rows=1024
group_count=48
full_group_count=47
tail_group_rows=131
full_group_bytes=8388608
total_lm_head_bytes=395337728
```

Coverage is exactly rows `0..48259` with no missing or duplicate row. Group 0 reuses the parent tile0 weight payload, so R4 adds only 47 checkpoint reads.

```text
parent_range_read_count=220
additional_lm_head_range_read_count=47
target_total_range_read_count=267
hard_total_range_read_count<=280
```

## GPU top-k graph

For every group:

```text
bounded weight upload
-> 1024-row-or-tail projection
-> GPU local top-k 64
-> write local result into 48x64 GPU history
-> deterministic GPU global merge
```

No group logits are accumulated into a full-vocabulary surface.

After the forward merge, the 64-entry global result is snapshotted. The same 48 local-top-k surfaces are merged in reverse group order on GPU. Forward and reverse IDs and values must match.

```text
topk_k=64
primary_order=logit_descending
secondary_order=token_id_ascending
local_topk_pass_count=48
global_merge_count=48
forward_reverse_topk_id_match=true
forward_reverse_topk_value_match=true
```

## CPU streaming reference

The CPU reference consumes one group at a time and keeps only local/global top-k. It never materializes 48,259 logits.

```text
gpu_cpu_topk_id_mismatch_count=0
gpu_cpu_topk_rank_mismatch_count=0
gpu_cpu_topk_value_mismatch_count=0
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
```

Group 0 GPU logits are compared with the parent tile0 reference:

```text
parent_tile0_compared_element_count=1024
parent_tile0_mismatch_count=0
```

## Allocation firewall

```text
max_single_gpu_allocation_bytes<=8388608
peak_live_gpu_bytes<=67108864
max_live_lm_head_group_count<=1
unreleased_lm_head_group_lease_count=0
full_lm_head_allocation_request_count=0
full_vocab_logits_allocation_request_count=0
full_vocab_logits_readback_count=0
topk_readback_count=1
```

The only final readback contains:

```text
parent tile0 logits=4096 bytes
forward top-k=512 bytes
reverse top-k=512 bytes
```

## Performance gate

```text
r4_tail_stage_total_ms<=10000
end_to_end_total_runtime_ms<=45000
soft_r4_tail_target_ms=5000
soft_end_to_end_target_ms=38000
```

A single run remains provisional performance evidence.

## Authority firewall

```text
sampler_use_count=0
token_commit_count=0
kv_cache_persist_count=0
production_checkpoint_replacement_count=0
runtime_output_changed=false
decode05_authorized=false
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R4_FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R4_FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R4_FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE
PASS_VERDICT=decode04_r4_fused_final_rmsnorm_grouped_lm_head_streaming_topk_parity_pass
```

## Artifacts

```text
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_local_manifest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_rmsnorm_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_lm_head_group_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_lm_head_stream_trace_latest.jsonl
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_topk_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_decode_04_r4_allocation_receipt_latest.json
```

PASS authorizes only R4-R1 sampler-shadow adapter work. It does not authorize sampler adoption, token commit, production route switching, KV persistence or DECODE-05 promotion.
