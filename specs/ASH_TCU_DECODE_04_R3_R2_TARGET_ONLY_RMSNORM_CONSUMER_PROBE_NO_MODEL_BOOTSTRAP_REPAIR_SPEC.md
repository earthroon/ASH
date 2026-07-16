# ASH-TCU-DECODE-04-R3-R2 SPEC

## TARGET_ONLY_RMSNORM_CONSUMER_PROBE_NO_MODEL_BOOTSTRAP_REPAIR

```text
patch_id=ASH-TCU-DECODE-04-R3-R2_TARGET_ONLY_RMSNORM_CONSUMER_PROBE_NO_MODEL_BOOTSTRAP_REPAIR
parent_patch=ASH-TCU-DECODE-04-R3_CONTIGUOUS_TAIL_NORM_WEIGHT_PROVENANCE_AND_REPAIR_GATE
parent_execution_id=decode04r2-9937058fbd1e064ae888
parent_status=PASS_ASH_TCU_DECODE_04_R2_FINAL_PROJECTION_INPUT_ORIGIN_DIAGNOSTIC
parent_verdict=decode04_r2_final_norm_output_degenerate
parent_root_cause_class=final_norm_output_degenerate
parent_route_digest=1b9009ff7216b57f6bcabeb0eb39d9c8d5e99019601f40de052166ff8f138327
model_bootstrap_allowed=false
generation_pass_allowed=false
production_checkpoint_pointer_change_allowed=false
```

## Supersession

The prior bounded-vocab-atlas probe hotfix is non-canonical. It retained general model bootstrap and is rejected. R3-R2 owns only exact-four RMSNorm repair verification through a target-only GPU probe.

## Status

```text
PASS=PASS_ASH_TCU_DECODE_04_R3_R2_TARGET_ONLY_RMSNORM_CONSUMER_PROBE_NO_MODEL_BOOTSTRAP_REPAIR
HOLD=HOLD_ASH_TCU_DECODE_04_R3_R2_TARGET_ONLY_RMSNORM_CONSUMER_PROBE_NO_MODEL_BOOTSTRAP_REPAIR
FAIL=FAIL_ASH_TCU_DECODE_04_R3_R2_TARGET_ONLY_RMSNORM_CONSUMER_PROBE_NO_MODEL_BOOTSTRAP_REPAIR
```

## Exact repair set

```text
model.layers.20.post_attention_layernorm.weight
model.layers.21.input_layernorm.weight
model.layers.21.post_attention_layernorm.weight
model.norm.weight
```

```text
checkpoint_tensor_count=201
repair_target_count=4
non_target_tensor_count=197
norm_tensor_count=45
healthy_norm_peer_count=41
target_shape=[2048]
target_dtype=f32
target_bytes=8192
target_host_materialized_bytes=32768
original_target_digest=9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47
replacement_target_digest=fc3bd1e348ef843a5052596a42863c169d54cc3c352449596039497873862155
```

## Candidate and provenance modes

```text
repair_candidate_mode=fresh|adopt-existing
provenance_mode=canonical-source|genesis-unit-scale-consensus
```

Fresh mode atomically creates a new quarantine checkpoint. Adopt-existing mode revalidates all 201 tensors, all four target payloads, all 197 non-target payload digests and original checkpoint immutability before adoption.

Genesis consensus requires 41 healthy norm peers to be bit-exact f32 one, the four exact targets to be bit-exact zero, no additional zero norm tensor, and operator decision `approve-exact-four-tail-norm-unit-scale-reconstruction`.

## Runtime owner and forbidden operations

```text
device_bootstrap_count=1
native_wgpu_model_bootstrap_count=0
ash_model_construction_count=0
embedding_load_count=0
lm_head_load_count=0
transformer_weight_load_count=0
vocab_atlas_build_count=0
generation_pass_count=0
vocab_projection_count=0
tensorcube_dispatch_count=0
sampler_use_count=0
token_commit_count=0
kv_cache_persist_count=0
unrelated_checkpoint_tensor_gpu_upload_count=0
```

The canonical binary must not import or construct `NativeWgpuModel`. Only the four target payload ranges may be decoded into host f32 vectors for GPU use.

## Target-only probe

Each target is probed sequentially with one production `AshRmsNorm<Wgpu>` consumer and one CPU `rms_norm_vec` diagnostic oracle.

```text
consumer_probe_count=4
parallel_probe_count=1
max_live_target_weight_count=1
max_live_probe_input_count=1
max_live_probe_output_count=1
absolute_tolerance=0.001
relative_tolerance=0.001
hard_absolute_ceiling=0.01
cpu_gpu_mismatch_count=0
```

Canonical input digests:

```text
layer_20_post_attention_layernorm=dddea0cac0c4fd6b7abd35e283bdb16c8e21101d8dddbe5f178f8462436577b3
layer_21_input_layernorm=77e577ed0084a130d7572e0fce1af205654b9b14cf2f9fce960ad13f15294259
layer_21_post_attention_layernorm=f294a4dbe83ae775585c450ff803e4f7d45574cbea3e05a612cab11886cb459a
final_norm=5143088969fbddaa210c19ece5695e6d237de67080162bd77cbe02f45e2d0661
```

## Allocation firewall

```text
max_single_allocation_bytes=1048576
max_probe_owned_peak_bytes=4194304
allocation_request_395337728_count=0
allocation_request_ge_8388608_count=0
```

Probe panic or allocation inability becomes typed HOLD. CPU-only PASS, full-model fallback and vocab-atlas fallback are forbidden.

## Binary and manifest

```text
binary=ash_tcu_decode_04_r3_r2_target_only_rmsnorm_consumer_probe_no_model_bootstrap_repair
manifest=workspace/runtime/tensorcube/ash_tensorcube_decode_04_r3_r2_local_manifest_latest.json
manifest_schema=ash_tensorcube_decode04_r3_r2_local_manifest_v1
```

## Exit codes

```text
0=PASS target-only repaired-checkpoint probe sealed
2=HOLD incomplete parent, candidate, provenance, device or probe evidence
1=FAIL invariant, parity, target-range, allocation or authority violation
```

## Promotion boundary

R3-R2 PASS authorizes only an R2 rerun with the repaired checkpoint. Production checkpoint replacement and DECODE-05 remain forbidden until repaired R2 and original DECODE-04 parity both pass.