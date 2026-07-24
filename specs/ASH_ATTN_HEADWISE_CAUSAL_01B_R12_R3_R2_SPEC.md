# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2

## Micro-Atlas Guard Group Map /
## Tile-Local Finite Summary /
## Device-Token Final Reduction /
## Guard Tail-Latency Recovery Seal

---

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3
parent_build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R1
parent_runtime_schema=ash.attn.headwise.causal.01b.r12.r3.runtime_artifact.v1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r2.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
finite_classification_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R1
device_decision_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
promotion_scope=incremental_decode_only
```

R12-R3-R2 preserves the R10 attention kernels, R12-R1 IEEE-754 classification, R12-R3 device-native decision token, and R12-R3-R1 pooled-buffer alias safety. It replaces the global per-element atomic finite summary with an eight-entry headwise micro-atlas group map.

---

## 1. Parent binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_local_manifest.json
```

Required parent state:

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R1
pass=false
status=HOLD
production_pass=true
guard_pass=true
policy_pass=true
negative_control_pass=true
performance_pass=false
negative_control_count=420
negative_control_fail_count=0
```

Allowed failed components are limited to:

```text
guarded_performance_true_round_non_regression
static_truth_checks
canonical_negative_truth:StaticTruthFailure
```

No finite-classification, device-token, alias-safety, output-readback, or downstream-visibility failure is admissible.

---

## 2. Micro-atlas topology SSOT

```text
query_head_count=32
head_dimension=64
logical_scalar_count=2048
micro_atlas_group_count=8
heads_per_group=4
scalars_per_group=256
```

Ownership:

```text
group 0 -> heads  0..3  -> scalars    0..255
group 1 -> heads  4..7  -> scalars  256..511
group 2 -> heads  8..11 -> scalars  512..767
group 3 -> heads 12..15 -> scalars  768..1023
group 4 -> heads 16..19 -> scalars 1024..1279
group 5 -> heads 20..23 -> scalars 1280..1535
group 6 -> heads 24..27 -> scalars 1536..1791
group 7 -> heads 28..31 -> scalars 1792..2047
```

Required:

```text
group_overlap_count=0
group_gap_count=0
group_out_of_bounds_count=0
each_head_owned_once=true
each_scalar_owned_once=true
```

---

## 3. Stage A: tile-local finite summary

Shader:

```text
crates/burn_webgpu_backend/src/shaders/headwise_guard_micro_atlas_map.wgsl
```

Execution:

```text
workgroup_size=64
dispatch_workgroups=8
values_per_lane=4
```

Each lane owns:

```text
group_begin + lane
group_begin + lane + 64
group_begin + lane + 128
group_begin + lane + 192
```

Lane-private classification fields:

```text
visited_count
non_finite_count
nan_count
positive_infinity_count
negative_infinity_count
max_abs_bits
error_bits
```

The workgroup reduction is:

```text
64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1
```

Counters use addition, errors use bitwise OR, and finite maximum magnitude uses unsigned maximum over positive float bit patterns.

Forbidden in Stage A:

```text
per-element atomicAdd to a shared global summary
per-element atomicMax to a shared global summary
shared global finite-result fan-in
```

Required:

```text
stage_a_per_element_global_atomic_count=0
stage_a_group_unique_write_count=8
```

Only lane zero writes each group entry and writes the completion marker last.

---

## 4. Group-map ABI

Each entry contains twenty `u32` words and occupies 80 bytes:

```text
schema_version
group_id
head_begin
head_count
scalar_begin
scalar_count
visited_count
non_finite_count
nan_count
positive_infinity_count
negative_infinity_count
max_abs_bits
candidate_nonce_lo
candidate_nonce_hi
slot_index
slot_generation_lo
slot_generation_hi
completion_marker
error_bits
reserved
```

Canonical map size:

```text
8 entries * 80 bytes = 640 bytes
```

The persistent map uses `STORAGE | COPY_SRC | COPY_DST` and may not alias the candidate output, downstream staging, decision token, indirect arguments, or telemetry state.

---

## 5. Stage B: device-token final reduction

Shader:

```text
crates/burn_webgpu_backend/src/shaders/headwise_guard_micro_atlas_finalize.wgsl
```

Execution:

```text
workgroup_size=32
dispatch_workgroups=1
lanes 0..7 consume entries 0..7
lanes 8..31 contribute identity summaries
```

The finalizer produces totals, completion/failure masks, NaN and infinity group masks, first failed group, and aggregate error bits.

Expected completion mask:

```text
0x000000ff
```

Authority formula:

```text
authority_granted =
  completion_mask == 0xff
  && failure_mask == 0
  && total_visited == 2048
  && all non-finite totals == 0
  && candidate nonce exact
  && slot index exact
  && slot generation exact
  && aggregate error bits == 0
  && device fault latch not set
```

Success writes exact indirect dimensions. Failure writes `[0,0,0]` and latches the first device failure.

---

## 6. Device-token ABI

The token contains 28 `u32` words and occupies 112 bytes. The first three words remain the indirect dispatch arguments at byte offset zero. Added fields include:

```text
micro_atlas_group_count
group_completion_mask
group_failure_mask
nan_group_mask
positive_infinity_group_mask
negative_infinity_group_mask
first_failed_group
```

`DeviceGuardDecisionToken` remains the downstream authority SSOT. Host telemetry is evidence only.

---

## 7. Command ordering

One encoder records:

```text
clear group-map buffer
clear decision-token buffer
clear guarded downstream staging
attention compute pass
micro-atlas map compute pass
device-token finalizer compute pass
guarded downstream indirect-copy pass
copy compact token into telemetry ring
queue.submit once
```

Required per candidate:

```text
command_encoder_count=1
queue_submit_count=1
attention_dispatch_count=1
micro_atlas_map_dispatch_count=1
micro_atlas_finalize_dispatch_count=1
downstream_indirect_dispatch_count=1
```

---

## 8. Alias and zero-wait preservation

Candidate and downstream staging may occupy non-overlapping slices of one pooled backing buffer. Both downstream-pass bindings use storage read-write. Host byte-range validation rejects overlap before submit.

Required:

```text
overlapping_candidate_downstream_range_count=0
unified_candidate_downstream_storage_usage=true
hot_path_map_async_count=0
hot_path_blocking_poll_count=0
hot_path_blocking_receive_count=0
hot_path_host_guard_decision_count=0
output_value_readback_count=0
```

Telemetry drains only outside candidate timing.

---

## 9. Fault localization

A non-finite value must identify its owning group. For example, a NaN at head 17 belongs to group 4 and must produce:

```text
nan_group_mask includes 0x10
group_failure_mask includes 0x10
first_failed_group=4
authority_granted=false
indirect dispatch=[0,0,0]
downstream staging remains zero
```

Fixtures cover NaN, positive infinity, and negative infinity in every group, multi-group failures, incomplete maps, nonce mismatch, and generation mismatch.

---

## 10. Bucket verdict truth

The printed bucket `pass` field reports metric truth only:

```text
bucket_metric_pass =
  median_ratio <= 1.00
  && p95_ratio <= 1.05
  && paired_regression_probability <= 0.05
```

Operational, static, negative-control, and promotion truth remain separate and still participate in the global verdict.

Required:

```text
bucket_log_truth_mismatch_count=0
```

---

## 11. Performance protocol

```text
buckets=8,16,32,64,128,256,512,1024,2048
warmup_iterations=128
measurement_rounds=32
pairs_per_round=32
measurement_pairs_per_bucket=1024
reference_first_rounds=16
atlas_first_rounds=16
```

Thresholds remain unchanged:

```text
bucket median_ratio<=1.00
bucket p95_ratio<=1.05
paired_regression_probability<=0.05
geometric_mean_median_ratio<=0.95
worst_bucket_median_ratio<=1.00
performance_bucket_fail_count=0
```

---

## 12. Negative controls

R12-R3-R2 re-executes 420 inherited controls and adds 80 controls:

```text
group_topology=20
tile_reduction=20
finalizer=20
performance_truth=20
total=500
```

Required:

```text
negative_control_count=500
negative_control_executed_count=500
negative_control_skipped_count=0
negative_control_fail_count=0
unexpected_failure_code_count=0
unintended_downstream_visibility_count=0
unintended_authority_grant_count=0
```

---

## 13. Source changes

```text
crates/burn_webgpu_backend/src/headwise_guard_decision.rs
crates/burn_webgpu_backend/src/shaders/headwise_guard_micro_atlas_map.wgsl
crates/burn_webgpu_backend/src/shaders/headwise_guard_micro_atlas_finalize.wgsl
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r3_r2_gate.rs
crates/orchestrator_local/Cargo.toml
```

---

## 14. Runtime artifacts

Rust generates the R12-R3-R2 runtime artifact, manifest, parent/scope/policy receipts, topology and bucket-truth receipts, guard and authority receipts, measurement catalogs, 500-control evidence, static checks, claim boundary, and verdict under `workspace/runtime/attention/`.

Runtime artifacts and manifests are excluded from the source bake.

---

## 15. PASS formula

```text
PASS =
  exact R12-R3-R1 HOLD parent binding
  && R10 attention kernel unchanged
  && device-token authority and alias safety preserved
  && topology == 8 groups * 4 heads * 64 dimensions
  && Stage A == 8 dispatches * 64 lanes * 4 values
  && Stage A per-element global atomic count == 0
  && Stage A unique group writes == 8 per candidate
  && Stage B workgroup size == 32 and dispatch count == 1
  && valid completion mask == 0xff and failure mask == 0
  && rejected candidate downstream visibility count == 0
  && all hot-path host-wait counters == 0
  && output-value readback count == 0
  && bucket-log truth mismatch count == 0
  && all nine performance buckets pass unchanged thresholds
  && all 500 controls pass
  && static checks and artifact digests pass
  && model-quality claim count == 0
```

PASS grants `AtlasProductionDeviceGuardedStagingScoped`. It does not prove native indirect o_proj matmul, zero invocation of the existing Burn o_proj call, zero telemetry readback over the whole session, transactional KV rollback, canonical 22-layer decode E2E, full-prefill production, chunked production, or quality improvement.

---

## 16. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r3-r2"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r2_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --verdict-scope incremental-only `
  --promote-full-prefill false `
  --promote-incremental-decode true `
  --promote-chunked-decode false `
  --require-same-device true `
  --require-qkv-zero-copy true `
  --require-output-zero-copy true `
  --forbid-output-value-readback true `
  --forbid-output-host-upload true `
  --guard-mode device-native-micro-atlas-token `
  --guard-map-mode headwise-micro-atlas `
  --guard-map-group-count 8 `
  --guard-map-heads-per-group 4 `
  --guard-map-dimensions-per-head 64 `
  --guard-map-workgroup-size 64 `
  --guard-map-values-per-lane 4 `
  --guard-finalizer-workgroup-size 32 `
  --decision-token-ring-capacity 4 `
  --telemetry-ring-capacity 4096 `
  --require-device-native-decision true `
  --require-gpu-gated-o-proj true `
  --require-gpu-gated-residual true `
  --require-zero-hot-path-host-wait true `
  --require-async-telemetry-drain true `
  --require-zero-per-element-global-atomics true `
  --performance-mode paired-gpu-timestamp `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --expected-negative-controls 500 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R2_MICRO_ATLAS_GUARD_GROUP_MAP_TILE_LOCAL_FINITE_SUMMARY_DEVICE_TOKEN_FINAL_REDUCTION_GUARD_TAIL_LATENCY_RECOVERY_ZERO_PER_ELEMENT_GLOBAL_ATOMICS_ZERO_HOT_PATH_HOST_WAIT_INCREMENTAL_ONLY_NO_OUTPUT_VALUE_READBACK_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_DIRECT_OPROJ_ZERO_INVOCATION_OVERCLAIM_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R2_MICRO_ATLAS_GROUP_MAP_FINAL_REDUCTION_OR_TAIL_LATENCY_RECOVERY_INCOMPLETE
```
