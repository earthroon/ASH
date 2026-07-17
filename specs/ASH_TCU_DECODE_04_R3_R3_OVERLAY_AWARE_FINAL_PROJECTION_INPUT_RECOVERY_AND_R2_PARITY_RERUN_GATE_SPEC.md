# ASH-TCU-DECODE-04-R3-R3 SPEC

## OVERLAY_AWARE_FINAL_PROJECTION_INPUT_RECOVERY_AND_R2_PARITY_RERUN_GATE

```text
patch_id=ASH-TCU-DECODE-04-R3-R3_OVERLAY_AWARE_FINAL_PROJECTION_INPUT_RECOVERY_AND_R2_PARITY_RERUN_GATE
parent_patch=ASH-TCU-DECODE-04-R3-R2-R2_TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH
parent_execution_id=decode04r3r2r2-26256e5426e624cc9a19
parent_status=PASS_ASH_TCU_DECODE_04_R3_R2_R2_TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH
parent_verdict=decode04_r3_r2_r2_exact_four_delta_overlay_grouped_gpu_stream_pass
diagnostic_parent_execution_id=decode04r2-9937058fbd1e064ae888
diagnostic_parent_verdict=decode04_r2_final_norm_output_degenerate
route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
production_authority=false
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R3_R3_OVERLAY_AWARE_FINAL_PROJECTION_INPUT_RECOVERY_AND_R2_PARITY_RERUN_GATE
HOLD=HOLD_ASH_TCU_DECODE_04_R3_R3_OVERLAY_AWARE_FINAL_PROJECTION_INPUT_RECOVERY_AND_R2_PARITY_RERUN_GATE
FAIL=FAIL_ASH_TCU_DECODE_04_R3_R3_OVERLAY_AWARE_FINAL_PROJECTION_INPUT_RECOVERY_AND_R2_PARITY_RERUN_GATE
PASS_VERDICT=decode04_r3_r3_overlay_repaired_final_projection_recovered_burn_tensorcube_tile0_parity_pass
```

PASS proves that the R3-R2-R2 exact-four delta overlay is bound to the real decode runtime view, recovers the formerly degenerate tail norm path, and produces Burn and TensorCube tile-0 projection outputs that satisfy the canonical parity gate. It does not authorize production replacement or token output changes.

## Exact overlay ownership

The overlay owns exactly these four f32 `[2048]` RMSNorm weights:

```text
model.layers.20.post_attention_layernorm.weight
model.layers.21.input_layernorm.weight
model.layers.21.post_attention_layernorm.weight
model.norm.weight
```

```text
overlay_resolved_tensor_count=4
base_resolved_target_tensor_count=0
non_target_overlay_resolution_count=0
silent_fallback_count=0
replacement_payload_digest=fc3bd1e348ef843a5052596a42863c169d54cc3c352449596039497873862155
```

Missing, malformed, duplicate, unknown, or silently base-fallback target resolution is FAIL.

## Runtime recovery

The implementation must use the existing decoder block ordering and production `AshRmsNorm` consumers. A simplified CPU-only or mathematically substituted tail path is forbidden.

Required repaired stages:

```text
layer20_post_attention_norm_output_nonzero_count=2048
layer21_input_norm_output_nonzero_count=2048
layer21_post_attention_norm_output_nonzero_count=2048
final_norm_input_nonzero_count=2048
final_norm_output_nonzero_count=2048
final_projection_input_nonzero_count=2048
final_norm_output_non_finite_count=0
final_projection_input_non_finite_count=0
final_projection_input_digest=final_norm_output_digest
```

Recovery transition:

```text
before.final_norm_output_nonzero_count=0
after.final_norm_output_nonzero_count=2048
final_norm_recovery_transition=true
```

## Bounded model and projection route

The runtime may load the transformer path required to reproduce the final hidden state. Embedding must use row gather. LM-head residency is limited to canonical tile 0.

```text
vocab_size=48259
hidden_size=2048
projection_dtype=f32
tile_index=0
tile_rows=1024
lm_head_resident_tile_count=1
full_lm_head_upload=false
full_embedding_upload=false
full_vocab_logits_materialized=false
```

Forbidden:

```text
395337728-byte LM-head allocation
full LM-head buffer
full-vocab logits buffer
all 48 vocab tiles resident
sampler bootstrap
token commit
persistent KV cache
production checkpoint pointer change
```

## Burn and TensorCube parity

Burn reference and TensorCube shadow must consume the same repaired projection input and the same LM-head tile-0 RHS.

```text
burn_projection_input_digest=tensorcube_projection_input_digest
burn_rhs_source_digest=tensorcube_rhs_source_digest
burn_rhs_runtime_digest=tensorcube_rhs_runtime_digest
source_runtime_rhs_parity=true
projection_input_identity=true
compared_element_count=1024
non_finite_pair_count=0
mismatch_count=0
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
```

Each element passes when absolute or relative tolerance passes, and the global maximum absolute error must not exceed the hard ceiling.

## Allocation and authority firewall

```text
max_single_allocation_bytes=16777216
max_projection_group_resident_bytes=67108864
max_live_lm_head_tile_count=1
full_lm_head_allocation_request_count=0
full_vocab_logits_allocation_request_count=0
sampler_use_count=0
token_commit_count=0
kv_cache_persist_count=0
runtime_output_changed=false
production_checkpoint_replaced=false
default_pointer_changed=false
```

## Inputs and artifacts

```text
r2_parent_manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r2_local_manifest_latest.json
r3_r2_r2_parent_manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r2_r2_local_manifest_latest.json
overlay_payload=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r2_r2_tail_norm_delta_overlay.bin
overlay_manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r2_r2_tail_norm_delta_overlay.json
manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_local_manifest_latest.json
stage_trace=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_stage_trace_latest.json
route_receipt=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r3_projection_route_receipt_latest.json
manifest_schema=ash_tensorcube_decode04_r3_r3_overlay_aware_recovery_parity_v1
```

Artifacts must be written atomically. Full repaired safetensors and production artifacts are forbidden.

## Binary

```text
ash_tcu_decode_04_r3_r3_overlay_aware_final_projection_input_recovery_and_r2_parity_rerun_gate
```

## Exit codes

```text
0=PASS overlay recovery and repaired tile-0 parity sealed
2=HOLD incomplete parent, overlay, GPU, route, completion, or readback evidence
1=FAIL invariant, recovery, parity, allocation, or authority violation
```

## Promotion boundary

R3-R3 PASS authorizes only repaired-overlay shadow parity re-entry and the design or implementation of `ASH-TCU-DECODE-04-R4_FUSED_FINAL_RMSNORM_GROUPED_LM_HEAD_TOPK_GATE`. Production checkpoint replacement, default runtime pointer changes, sampler input changes, token commit, KV persistence, and DECODE-05 promotion remain forbidden.
