# ASH-TCU-DECODE-04-R3-R2-R2 SPEC

## TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH

```text
patch_id=ASH-TCU-DECODE-04-R3-R2-R2_TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH
parent_patch=ASH-TCU-DECODE-04-R3-R2_TARGET_ONLY_RMSNORM_CONSUMER_PROBE_NO_MODEL_BOOTSTRAP_REPAIR
parent_execution_id=decode04r2-9937058fbd1e064ae888
parent_verdict=decode04_r2_final_norm_output_degenerate
production_authority=false
```

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R3_R2_R2_TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH
HOLD=HOLD_ASH_TCU_DECODE_04_R3_R2_R2_TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH
FAIL=FAIL_ASH_TCU_DECODE_04_R3_R2_R2_TARGET_NORM_DELTA_ATLAS_PARALLEL_GROUPED_GPU_STREAMING_FAST_PATH
```

PASS proves only that the exact four repaired RMSNorm weights were represented as a bounded delta overlay and consumed by one parallel grouped GPU RMSNorm transaction without full checkpoint scanning, model bootstrap, generation, or production promotion.

## Exact repair set

```text
model.layers.20.post_attention_layernorm.weight
model.layers.21.input_layernorm.weight
model.layers.21.post_attention_layernorm.weight
model.norm.weight
```

```text
target_count=4
target_shape=[2048]
target_dtype=f32
target_bytes_per_tensor=8192
total_target_bytes=32768
source_target_digest=9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47
replacement_target_digest=fc3bd1e348ef843a5052596a42863c169d54cc3c352449596039497873862155
```

## Delta overlay and checkpoint I/O

The immutable base checkpoint owns all non-target tensors. The overlay owns only the four replacement vectors.

```text
non_target_parity_mode=structural_base_fallback
non_target_full_rehash_performed=false
full_repaired_checkpoint_created=false
base_header_read_count=1
base_target_range_read_count=4
base_non_target_range_read_count=0
checkpoint_target_payload_bytes_read=32768
full_checkpoint_payload_scan_count=0
full_checkpoint_sha256_recompute_count=0
full_checkpoint_copy_count=0
```

## Atlas group plan

```text
group_id=decode04_r3_r2_r2_tail_norm_group_0
group_width=4
hidden_size=2048
weight_atlas_shape=[4,2048]
input_atlas_shape=[4,2048]
output_atlas_shape=[4,2048]
staging_ring_slots=2
```

The single command encoder records two staging copies, one grouped RMSNorm dispatch with four workgroups, and one output-atlas readback copy.

```text
device_bootstrap_count=1
queue_submit_count=1
grouped_dispatch_count=1
per_target_dispatch_count=0
readback_count=1
parallel_target_row_count=4
workgroup_count_x=4
workgroup_size_x=256
elements_per_thread=8
```

## Allocation and no-model-bootstrap firewall

```text
weight_atlas_bytes=32768
input_atlas_bytes=32768
output_atlas_bytes=32768
max_single_allocation_bytes=1048576
max_group_owned_gpu_bytes=4194304
allocation_request_395337728_count=0
allocation_request_ge_8388608_count=0
native_wgpu_model_bootstrap_count=0
ash_model_construction_count=0
embedding_load_count=0
transformer_weight_load_count=0
lm_head_load_count=0
vocab_atlas_build_count=0
generation_pass_count=0
vocab_projection_count=0
tensorcube_decode_dispatch_count=0
sampler_use_count=0
token_commit_count=0
kv_cache_persist_count=0
```

## Parity and artifacts

```text
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
cpu_gpu_mismatch_count=0
non_finite_count=0
binary=ash_tcu_decode_04_r3_r2_r2_target_norm_delta_atlas_parallel_grouped_gpu_streaming_fast_path
manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r2_r2_local_manifest_latest.json
manifest_schema=ash_tensorcube_decode04_r3_r2_r2_fast_path_receipt_v1
```

## Exit and promotion boundary

```text
0=PASS exact-four overlay and grouped GPU stream sealed
2=HOLD incomplete parent, overlay, GPU, or bounded completion evidence
1=FAIL invariant, parity, I/O, allocation, or authority violation
```

R3-R2-R2 PASS authorizes only a repaired R2 rerun using a later overlay-aware runtime view or a separately materialized quarantine checkpoint. Production checkpoint replacement, DECODE-04 promotion, and DECODE-05 remain forbidden.