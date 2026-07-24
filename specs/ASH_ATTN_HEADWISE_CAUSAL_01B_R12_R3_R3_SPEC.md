# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3

## Dual-Kernel Crossover Probe /
## 1024 GQA2 Tiled Admission /
## Deterministic Bucket Route LUT /
## Short-KV Tail-Latency Closure Seal

---

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
parent_runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r2.runtime_artifact.v1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
micro_atlas_guard_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
route_policy_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3
promotion_scope=incremental_decode_only
```

R12-R3-R3 does not change attention math, finite classification, device decision-token authority, the 8x256 micro-atlas guard, or performance thresholds. It replaces the authoritative `seq_kv >= 1536` route condition with a deterministic, digest-bound route LUT and proves the crossover with direct dual-kernel measurements.

---

## 1. Parent binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r2_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r2_local_manifest.json
```

Required parent state:

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
pass=false
status=HOLD
production_pass=true
guard_pass=true
policy_pass=true
negative_control_pass=true
static_pass=true
performance_pass=false
negative_control_count=500
negative_control_fail_count=0
failed_components=[guarded_performance_true_round_non_regression]
```

The parent must show exactly one failed mandatory bucket, `seq_kv=1024`, while 512 and 2048 pass.

---

## 2. Kernel candidates

```text
kernel_a=subgroup32_single_q_head_v1
workgroup_size=32
query_heads_per_workgroup=1
shared_kv_tile=false

kernel_b=subgroup32_gqa2_long_kv_tiled_v1
workgroup_size=64
query_heads_per_workgroup=2
shared_kv_tile=true
```

Both are R10 kernels and must preserve the same attention math and numerical contract.

---

## 3. Route authority SSOT

The production route authority is:

```text
HEADWISE_ATLAS_INCREMENTAL_ROUTE_LUT
```

Source:

```text
crates/burn_webgpu_backend/src/headwise_route_lut.rs
```

The legacy constant `HEADWISE_ATLAS_LONG_KV_THRESHOLD=1536` may remain for diagnostics or negative controls but must be unreachable from the promoted production dispatch path.

Forbidden route inputs:

```text
current candidate timing
previous candidate timing
rolling latency average
telemetry feedback
GPU utilization
clock estimate
temperature
guard result from a previous token
```

The same `seq_kv` under the same source/runtime binding must always select the same kernel.

---

## 4. Canonical LUT candidate

```text
seq_kv 1..1023
  -> subgroup32_single_q_head_v1

seq_kv 1024..u32::MAX
  -> subgroup32_gqa2_long_kv_tiled_v1
```

The LUT is immutable after initialization and covers `1..u32::MAX` without gaps or overlaps. `seq_kv=0` is an explicit error.

Required topology:

```text
band_count=2
first_band_min=1
last_band_max=u32::MAX
band_gap_count=0
band_overlap_count=0
band_unsorted_count=0
exact_match_count_per_lookup=1
```

---

## 5. Probe and production separation

Probe-only API:

```text
dispatch_native_qkv_into_output_device_guarded_forced_route
```

Production API:

```text
dispatch_native_qkv_into_output_device_guarded
```

The probe API accepts an explicit kernel route and emits a forced-route receipt. The production API accepts no route override and resolves the route only through the LUT.

A forced route may never enter the model production path.

---

## 6. Crossover probes

Mandatory buckets:

```text
512,768,896,1024,1152,1280,1536,2048
```

At every bucket, both kernels run with identical:

```text
Q/K/V buffers
candidate and downstream tensor shapes
micro-atlas guard
device decision token
downstream staging gate
warmup count
measurement count
round order
```

Canonical measurement per kernel and bucket:

```text
warmup_iterations=128
measurement_rounds=32
pairs_per_round=32
measurement_pairs=1024
first-kernel rounds=16
second-kernel rounds=16
```

Slow rounds may not be discarded and best-run selection is forbidden.

---

## 7. Probe admission formula

For ordinary crossover buckets:

```text
gqa2_admissible =
  numerical and guard contracts pass
  && gqa2_median <= single_median
  && gqa2_p95 <= single_p95
  && gqa2_regression_probability <= 0.05
```

For `seq_kv=1024`, because the patch exists to close a known tail failure:

```text
gqa2_median / single_median <= 1.00
gqa2_p95 / single_p95 <= 0.95
gqa2_regression_probability <= 0.05
```

The stricter probe p95 ratio does not relax or replace the production Atlas/reference threshold.

---

## 8. Crossover monotonicity and stability

After GQA2 first becomes admissible in the ascending probe catalog, no later probe bucket may become inadmissible.

For the baked 1024 boundary:

```text
896 prefers incumbent single route
1024 admits GQA2
1152 admits GQA2
```

A contradictory or non-monotonic probe result produces HOLD. It does not mutate the source LUT at runtime.

---

## 9. Route receipt

Each selection records:

```text
policy_id
seq_kv
matched_band_index
matched_band_min
matched_band_max
selected_kernel_id
selected_workgroup_size
query_heads_per_workgroup
exact_match_count
legacy_threshold_used
forced_probe_route
route_lut_digest
receipt_digest
```

Production requirements:

```text
exact_match_count=1
legacy_threshold_used=false
forced_probe_route=false
```

---

## 10. Route replay

Replay the LUT for:

```text
8,16,32,64,128,256,512,
768,896,1023,1024,1025,
1152,1280,1536,2048,u32::MAX
```

Each is repeated at least 100 times.

Required:

```text
route_replay_mismatch_count=0
route_lut_digest_mutation_count=0
same_seq_same_route=true
```

---

## 11. Guard preservation

R12-R3-R3 preserves:

```text
micro_atlas_group_count=8
heads_per_group=4
scalars_per_group=256
Stage A workgroup_size=64
Stage A values_per_lane=4
Stage B workgroup_size=32
Stage A per-element global atomic count=0
```

Every forced or production route still executes:

```text
attention
-> micro-atlas finite map
-> device-token finalizer
-> indirect downstream staging gate
```

No kernel route may bypass the guard.

---

## 12. Zero-wait and ownership preservation

Required:

```text
hot_path_map_async_count=0
hot_path_blocking_poll_count=0
hot_path_blocking_receive_count=0
hot_path_host_guard_decision_count=0
output_value_readback_count=0
overlapping_candidate_downstream_range_count=0
rejected_candidate_downstream_visibility_count=0
```

Candidate and downstream pooled slices retain R12-R3-R1 unified storage usage and byte-range overlap rejection.

---

## 13. Production verification

Mandatory production buckets:

```text
8,16,32,64,128,256,512,1024,2048
```

Expected routes:

```text
8..512 -> subgroup32_single_q_head_v1
1024..2048 -> subgroup32_gqa2_long_kv_tiled_v1
```

Every production candidate must use the LUT path, not the forced probe path.

---

## 14. Performance thresholds

Unchanged per bucket:

```text
Atlas/reference median_ratio <= 1.00
Atlas/reference p95_ratio <= 1.05
paired_regression_probability <= 0.05
```

Route-wide:

```text
geometric_mean_median_ratio <= 0.95
worst_bucket_median_ratio <= 1.00
performance_bucket_fail_count=0
```

1024 closure requires:

```text
selected_kernel=subgroup32_gqa2_long_kv_tiled_v1
median_ratio<=1.00
p95_ratio<=1.05
regression_probability<=0.05
bucket_metric_pass=true
```

---

## 15. Negative controls

R12-R3-R3 re-executes 500 inherited controls and adds 80:

```text
crossover_probe=20
lut_topology=20
route_determinism=20
tail_closure_1024=20
total=580
```

Required:

```text
negative_control_count=580
negative_control_executed_count=580
negative_control_skipped_count=0
negative_control_fail_count=0
unexpected_failure_code_count=0
```

---

## 16. Static checks

Executable-code checks must prove:

```text
route LUT module exists
production route calls LUT selector
production route does not inspect legacy threshold
forced route is reachable only through probe API
both R10 kernels are reachable in probe code
route lookup covers 1..u32::MAX
route replay exists
1024 admission formula includes median, p95 and probability
micro-atlas guard remains in both route paths
hot-path waits and output-value readback remain absent
```

Comments, specification text, artifact names, and test names do not satisfy executable checks.

---

## 17. Source changes

```text
crates/burn_webgpu_backend/src/headwise_route_lut.rs
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r3_r3_gate.rs
crates/orchestrator_local/Cargo.toml
specs/ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_SPEC.md
```

---

## 18. Runtime artifacts

Rust generates under `workspace/runtime/attention/`:

```text
ash_attn_headwise_causal_01b_r12_r3_r3_runtime_artifact.json
ash_attn_headwise_causal_01b_r12_r3_r3_local_manifest.json
ash_attn_headwise_causal_01b_r12_r3_r3_parent_binding_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_probe_policy.json
ash_attn_headwise_causal_01b_r12_r3_r3_probe_performance_catalog.json
ash_attn_headwise_causal_01b_r12_r3_r3_probe_winner_catalog.json
ash_attn_headwise_causal_01b_r12_r3_r3_crossover_boundary_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_route_lut.json
ash_attn_headwise_causal_01b_r12_r3_r3_route_replay_receipts.json
ash_attn_headwise_causal_01b_r12_r3_r3_1024_tail_closure_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_performance_catalog.json
ash_attn_headwise_causal_01b_r12_r3_r3_negative_control_registry.json
ash_attn_headwise_causal_01b_r12_r3_r3_negative_control_outcomes.json
ash_attn_headwise_causal_01b_r12_r3_r3_static_checks.json
ash_attn_headwise_causal_01b_r12_r3_r3_claim_boundary_receipt.json
ash_attn_headwise_causal_01b_r12_r3_r3_verdict.json
```

Runtime artifacts and manifests are excluded from the source bake.

---

## 19. PASS formula

```text
PASS =
  exact R12-R3-R2 HOLD binding
  && both kernels execute through identical guarded contracts
  && 8 crossover probes complete
  && 1024 GQA2 admission passes
  && crossover monotonicity passes
  && 896/1024/1152 neighbor stability passes
  && deterministic LUT topology passes
  && legacy threshold production count=0
  && route replay mismatch count=0
  && production 1024 selects GQA2
  && production 1024 passes unchanged thresholds
  && all 9 production buckets pass
  && micro-atlas and device-token gates remain enabled
  && all hot-path wait counters=0
  && output-value readback count=0
  && all 580 negative controls pass
  && static and digest checks pass
  && model-quality claim count=0
```

---

## 20. Claim boundary

PASS grants:

```text
IncrementalDecode -> AtlasProductionDeviceGuardedStagingScoped
Attention route SSOT -> deterministic bucket route LUT
1024 route -> subgroup32_gqa2_long_kv_tiled_v1
Legacy 1536 threshold -> non-authoritative
Runtime-adaptive routing -> forbidden
```

PASS does not prove:

```text
universal crossover across all GPU models
runtime-adaptive routing
native indirect o_proj matmul
zero invocation of the existing Burn o_proj call
transactional KV rollback
canonical full-model decode E2E
full-prefill production
chunked production
model-quality improvement
```

---

## 21. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r3-r3"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r3_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r2_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r2_local_manifest.json `
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
  --route-policy deterministic-bucket-lut `
  --probe-kernels single-query-head,gqa2-long-kv-tiled `
  --probe-buckets 512,768,896,1024,1152,1280,1536,2048 `
  --require-1024-gqa2-admission true `
  --require-monotonic-crossover true `
  --require-stable-crossover-neighbors true `
  --require-legacy-threshold-unreachable true `
  --route-replay-count 100 `
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
  --expected-negative-controls 580 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_DUAL_KERNEL_CROSSOVER_PROBE_1024_GQA2_TILED_ADMISSION_DETERMINISTIC_BUCKET_ROUTE_LUT_SHORT_KV_TAIL_LATENCY_CLOSURE_INCREMENTAL_ONLY_MICRO_ATLAS_GUARD_PRESERVED_ZERO_HOT_PATH_HOST_WAIT_NO_OUTPUT_VALUE_READBACK_NO_RUNTIME_ADAPTIVE_ROUTING_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_DIRECT_OPROJ_ZERO_INVOCATION_OVERCLAIM_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_DUAL_KERNEL_CROSSOVER_1024_ADMISSION_ROUTE_LUT_OR_TAIL_CLOSURE_INCOMPLETE
```
