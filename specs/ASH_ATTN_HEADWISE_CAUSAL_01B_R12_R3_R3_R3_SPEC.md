# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3

## In-Encoder Timestamp Query Atlas /
## Pair-Local Single-Submission Matrix /
## Deferred Batched Resolve /
## Combined Raw-Sample Tail Truth Seal

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r3.runtime_artifact.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
micro_atlas_guard_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
lexical_static_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2
measurement_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3
promotion_scope=incremental_decode_only
```

This revision changes the audit measurement engine, not attention math or the production finite-guard contract. It replaces per-sample timestamp submission/readback with a persistent round-local timestamp query atlas and derives combined tail statistics from the complete raw sample population.

## 1. Parent binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r2_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r2_local_manifest.json
```

Allowed parent HOLD components are limited to guarded performance, 1024 GQA2 admission, crossover neighbor/order/thermal truth, the legacy direct-tail sign test, and 2048 thermal closure. Parent lexical/static, guard, ownership, zero-wait and 680-control truth must pass.

## 2. Timestamp query atlas

Per round:

```text
pairs_per_round=32
timestamps_per_pair=4
queries_per_round=128
queue_submits_per_round=1
query_resolves_per_round=1
```

Logical query ownership for pair `p`:

```text
4p+0 route A begin
4p+1 route A end
4p+2 route B begin
4p+3 route B end
```

The query set and resolve buffer persist for a bucket/epoch. Per-sample or per-pair query-set, resolve-buffer, queue-submit and timestamp-readback ownership is forbidden.

## 3. Encode-only route spans

The backend exposes encode-only audit surfaces. They receive an existing command encoder and may not submit, map, poll or wait.

Atlas measured span contains:

```text
selected R10 attention kernel
micro-atlas finite group map
device-token finalizer
indirect guarded downstream staging
```

The audit Reference span uses a raw WGPU reference attention shader with the same logical Q/K/V, causal positions and output shape. It is a measurement reference, not a promoted production route. Numerical parity against the established reference contract is required before timing evidence is admissible.

## 4. Pair-local command matrix

Probe pairs compare Single versus GQA2. Production pairs compare Reference versus LUT-selected guarded Atlas. Both members of one pair are encoded into the same command encoder and submitted in the same round command buffer.

```text
AB/BA or RA/AR pairs per bucket=512/512
combined pairs per bucket=1024
measurement rounds per bucket=32
```

A pair split across encoders or submissions is fail-closed.

## 5. Deferred round resolve

After all 32 pairs are encoded, the same encoder resolves all 128 queries and copies the resolve buffer into one readback-ring slot. The round is submitted once. Readback mapping is scheduled after submission and drained through a bounded ring outside timestamp spans.

```text
timestamp_readback_ring_capacity=4
per_pair_timestamp_readback_count=0
per_sample_timestamp_readback_count=0
wait_inside_timed_span_count=0
wait_between_pair_members_count=0
```

Benchmark drain waits are reported separately and do not alter the production hot-path zero-wait claim.

## 6. Raw sample SSOT

Each pair records epoch, bucket, round, pair index, physical order, route identities, begin/end ticks, decoded nanoseconds, signed delta, ratio and sample digest. Missing, duplicate, invalid or silently discarded samples invalidate the bucket.

Epoch 0 and epoch 1 raw arrays are concatenated. Summary statistics are recalculated from all 1024 samples.

```text
median_method=sorted_midpoint_v1
quantile_method=nearest_rank_v1
p95 index for N=1024 is 972
p99 index for N=1024 is 1013
```

Median-of-medians, average epoch p95, or worst-epoch p95 labeled as combined p95 are forbidden.

## 7. Probe truth

Probe buckets:

```text
512,768,896,1024,1152,1280,1536,2048
```

Epoch 0 is ascending and epoch 1 descending. Direct statistics compare matched GQA2 and Single samples. Reference-derived probability cannot authorize the crossover. The legacy tail sign test remains diagnostic only and has zero admission authority.

Strict 1024 admission requires parity and guard/token truth plus:

```text
combined GQA2/Single median ratio<=1.00
combined GQA2/Single p95 ratio<=0.95
direct paired sign probability<=0.05
order median delta<=0.03
order p95 delta<=0.08
epoch median delta<=0.05
epoch p95 delta<=0.10
```

The deterministic LUT candidate remains `1..1023 Single / 1024.. GQA2`; it is admitted only when corrected evidence supports it.

## 8. Production truth

Production buckets:

```text
8,16,32,64,128,256,512,1024,2048
```

Production uses ascending and descending epochs with matched Reference/Atlas pairs. Combined metrics are recomputed from all raw samples.

Unchanged thresholds:

```text
median_ratio<=1.00
p95_ratio<=1.05
paired_regression_probability<=0.05
geometric_mean_median_ratio<=0.95
worst_bucket_median_ratio<=1.00
performance_bucket_fail_count=0
```

512, 1024 and 2048 receive explicit tail-closure receipts. Epoch stability remains separate from combined metric truth.

## 9. Safety preservation

Required:

```text
micro_atlas_group_count=8
Stage A per-element global atomic count=0
device-token authority=true
hot_path_blocking_wait_count=0
output_value_readback_count=0
candidate/downstream overlap count=0
rejected downstream visibility count=0
```

Timestamp and compact decision-token evidence readback is permitted. Candidate/output tensor value readback remains forbidden.

## 10. Negative controls and manifest

R12-R3-R3-R3 executes 680 inherited controls and 120 new controls:

```text
query_atlas=30
submission_resolve=30
raw_sample_truth=30
tail_authority=30
total=800
```

The bounded six-group manifest builder is preserved. The flat artifact lookup ABI remains authoritative. Runtime artifacts and manifests are excluded from the source bake.

## 11. Source changes

```text
crates/burn_webgpu_backend/src/headwise_atlas.rs
crates/burn_webgpu_backend/src/headwise_guard_decision.rs
crates/burn_webgpu_backend/src/shaders/headwise_reference_attention_measurement.wgsl
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r3_r3_r3_gate.rs
crates/orchestrator_local/Cargo.toml
```

## 12. PASS boundary

PASS requires exact parent binding; timestamp-query feature and valid period; one encoder and one round submission for every pair; zero per-pair/per-sample submit, resolve and timestamp readback; complete 1024-sample raw populations; exact combined statistics; corrected 1024 GQA2 admission; monotonic/stable LUT evidence; all nine production buckets including 512/1024/2048 tails; preserved micro-atlas/device-token/zero-wait/output-ownership truth; all 800 controls; static and digest truth; and zero quality claims.

PASS does not prove universal cross-adapter crossover, zero benchmark drain waits, native indirect o_proj matmul, zero invocation of the existing Burn o_proj call, transactional KV rollback, canonical full-model decode, prefill/chunked production or model-quality improvement.

## 13. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r3-r3-r3"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r3_r3_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r2_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_r2_local_manifest.json `
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
  --static-extractor rust-lexical `
  --require-string-comment-safe-extraction true `
  --timestamp-mode in-encoder-query-atlas `
  --require-timestamp-query-feature true `
  --query-atlas-pairs-per-round 32 `
  --query-atlas-timestamps-per-pair 4 `
  --query-atlas-queries-per-round 128 `
  --timestamp-readback-ring-capacity 4 `
  --timestamp-resolve-mode deferred-round-batch `
  --require-pair-single-encoder true `
  --require-pair-single-submission true `
  --require-per-pair-submit-zero true `
  --require-per-sample-readback-zero true `
  --require-wait-outside-timed-spans true `
  --route-policy deterministic-bucket-lut-v3 `
  --probe-kernels single-query-head,gqa2-long-kv-tiled `
  --probe-buckets 512,768,896,1024,1152,1280,1536,2048 `
  --probe-epoch-order ascending,descending `
  --probe-pair-order interleaved-ab-ba `
  --probe-pairs 1024 `
  --probe-rounds 32 `
  --probe-pairs-per-round 32 `
  --require-direct-kernel-sign-test true `
  --require-legacy-tail-sign-test-unreachable true `
  --require-probe-order-bias-gate true `
  --require-thermal-epoch-consistency true `
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
  --performance-mode in-encoder-query-atlas-combined-raw `
  --production-epoch-order ascending,descending `
  --combined-statistics-source raw-samples `
  --combined-median-method sorted-midpoint-v1 `
  --combined-quantile-method nearest-rank-v1 `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --expected-negative-controls 800 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_IN_ENCODER_TIMESTAMP_QUERY_ATLAS_PAIR_LOCAL_SINGLE_SUBMISSION_MATRIX_DEFERRED_BATCHED_RESOLVE_COMBINED_RAW_SAMPLE_TAIL_TRUTH_1024_GQA2_ADMISSION_DETERMINISTIC_ROUTE_LUT_INCREMENTAL_ONLY_MICRO_ATLAS_GUARD_PRESERVED_ZERO_HOT_PATH_HOST_WAIT_NO_OUTPUT_VALUE_READBACK_NO_RUNTIME_ADAPTIVE_ROUTING_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_TIMESTAMP_QUERY_ATLAS_SINGLE_SUBMISSION_DEFERRED_RESOLVE_OR_COMBINED_TAIL_TRUTH_INCOMPLETE
```
