# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2

## Lexical Rust Function Extraction /
## Interleaved Dual-Kernel Pair Matrix /
## Direct Kernel-to-Kernel Sign Test /
## Thermal-Drift-Resistant Crossover Seal

---

## 0. Identity

```text
patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2
parent_patch_id=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3
parent_build_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R1
runtime_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r2.runtime_artifact.v1
manifest_schema=ash.attn.headwise.causal.01b.r12.r3.r3.r2.local_manifest.v1
public_abi_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2
attention_kernel_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R10
micro_atlas_guard_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R2
manifest_builder_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R1
route_probe_revision=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R2
promotion_scope=incremental_decode_only
```

This revision repairs measurement and static-analysis truth. It does not change attention math, finite classification, the 8x256 micro-atlas topology, device-token authority, downstream staging ownership, or performance thresholds.

---

## 1. Parent HOLD binding

Required parent files:

```text
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_runtime_artifact.json
workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_local_manifest.json
```

Allowed parent failures are limited to:

```text
guarded_performance_true_round_non_regression
1024_gqa2_tiled_admission
crossover_neighbor_stability
static_truth_checks
canonical_negative_truth:StaticTruthFailure
```

The parent must retain production, finite-guard, policy and negative-control safety, report 9 performance buckets, 580 executed controls, zero control failures and zero model-quality claims.

---

## 2. Truth-domain separation

```text
LexicalStaticTruth
DirectKernelProbeTruth
ProductionPerformanceTruth
PromotionTruth
```

The direct probe compares the two Atlas kernels only. Production compares the LUT-selected Atlas route against Reference. Static truth cannot alter a printed metric verdict. Candidate-versus-Reference probability cannot authorize a kernel crossover.

---

## 3. Lexical Rust extraction

Required executable APIs:

```rust
fn rust_lexical_code_mask(source: &str) -> Result<Vec<u8>>;
fn extract_rust_function_by_name<'a>(
    source: &'a str,
    function_name: &str,
) -> Result<&'a str>;
```

The scanner distinguishes code, line comments, nested block comments, normal and byte strings, raw and raw-byte strings with arbitrary hash count, and character literals. Function names are matched as exact Rust identifiers following a code-state `fn` token. Braces alter body depth only in code state.

Required failures:

```text
missing exact function -> error
multiple exact functions -> error
unterminated lexical state -> error
unterminated body -> error
negative brace depth -> error
```

Raw substring function-boundary extraction is forbidden.

Twenty-five fixtures cover ordinary/public/attributed/generic functions, where clauses, nested blocks, string and comment decoys, character braces, prefix identifiers, duplicates, missing functions and unterminated states.

```text
lexical_fixture_count=25
lexical_fixture_fail_count=0
lexical_wrong_function_selection_count=0
```

Static inspection must select the real `main`, probe, combine, manifest merge, model route, backend fused route and decision-encode functions.

---

## 4. Direct-kernel probe

```text
kernel_a=subgroup32_single_q_head_v1
kernel_b=subgroup32_gqa2_long_kv_tiled_v1
probe_buckets=512,768,896,1024,1152,1280,1536,2048
```

Reference is excluded from timed crossover pairs. Numerical parity against Reference is checked separately.

Probe epoch 0 is ascending. Probe epoch 1 is descending. Per bucket:

```text
warmup_pairs_total=128
measurement_pairs_total=1024
measurement_rounds_total=32
pairs_per_round=32
pairs_per_epoch=512
rounds_per_epoch=16
```

---

## 5. Interleaved AB/BA pair matrix

```text
AB = Single then GQA2
BA = GQA2 then Single
```

Each pair binds identical logical Q/K/V values, sequence length, causal policy, guard policy and runtime profile. Across both epochs and each bucket:

```text
AB_pairs=512
BA_pairs=512
```

Each receipt records epoch, bucket, round, pair index, order, input digest, both durations, signed delta and ratio.

```text
signed_delta_ns = gqa2_ns - single_ns
```

The two kernels use independent candidate/downstream slot families. Slot and timestamp aliasing are fail-closed.

---

## 6. Direct statistics

The probe derives from matched GQA2-versus-Single pairs:

```text
single and GQA2 median/p95/p99
gqa2_to_single median/p95/p99 ratios
gqa2_faster_pair_count
single_faster_pair_count
tie_pair_count
direct_sign_test_probability
direct_tail_regression_probability
```

Ties use the larger of 1 ns or 0.1 percent of the larger paired duration. The one-sided sign test uses `single_faster_pair_count` as the count where GQA2 is slower. Tail testing uses the same pair identities where either kernel is at or above its own p90.

Reference-derived probabilities are forbidden in crossover admission.

---

## 7. Order and thermal gates

AB and BA ratios remain separately visible:

```text
abs(ab_median_ratio - ba_median_ratio) <= 0.03
```

Ascending and descending epoch ratios also remain separately visible:

```text
abs(epoch_a_median_ratio - epoch_b_median_ratio) <= 0.05
```

A failed order or thermal gate is a visible HOLD component. Averaging may not hide it.

---

## 8. GQA2 admission and crossover

Ordinary admission requires parity, guard and token success plus:

```text
gqa2_to_single_median_ratio <= 1.00
gqa2_to_single_p95_ratio <= 1.00
direct_sign_test_probability <= 0.05
direct_tail_regression_probability <= 0.05
order_bias_pass=true
thermal_epoch_consistency_pass=true
```

The known 1024 bucket additionally requires:

```text
gqa2_to_single_p95_ratio <= 0.95
```

The crossover must be monotonic. For the baked 1024 boundary:

```text
896 -> Single or statistical tie
1024 -> GQA2 admitted
1152 -> GQA2 admitted
```

---

## 9. Route LUT authority

```text
1..1023 -> subgroup32_single_q_head_v1
1024..u32::MAX -> subgroup32_gqa2_long_kv_tiled_v1
```

The baked LUT is admitted only if corrected runtime evidence supports it. Runtime mutation, latency or temperature feedback, nearest-band fallback and the legacy 1536 threshold are forbidden.

```text
legacy_threshold_route_count=0
route_replay_mismatch_count=0
```

---

## 10. Production mirrored epochs

Production starts only after probe telemetry, timestamps and statistics are resolved and route admission is frozen.

Mandatory buckets:

```text
8,16,32,64,128,256,512,1024,2048
```

Production epoch 0 is ascending and epoch 1 descending. Every bucket receives 512 pairs per epoch and 1024 combined pairs. Reference-first and Atlas-first rounds are balanced.

The combined receipt uses both epochs. Median values combine both epoch medians. Tail ratio and regression probability use the conservative worse epoch so a favorable epoch cannot conceal failure.

Unchanged thresholds:

```text
median_ratio<=1.00
p95_ratio<=1.05
paired_regression_probability<=0.05
geometric_mean_median_ratio<=0.95
worst_bucket_median_ratio<=1.00
performance_bucket_fail_count=0
```

Printed bucket pass remains metric truth only.

---

## 11. Explicit 1024 and 2048 closure

1024 must select the GQA2 tiled kernel through the production LUT and pass unchanged Atlas/reference thresholds.

2048 records both epochs and the combined result:

```text
seq_2048_epoch_p0_median_ratio
seq_2048_epoch_p1_median_ratio
seq_2048_epoch_p0_p95_ratio
seq_2048_epoch_p1_p95_ratio
seq_2048_combined_median_ratio
seq_2048_combined_p95_ratio
```

```text
abs(epoch_p0_median_ratio - epoch_p1_median_ratio) <= 0.05
combined_2048_metric_pass=true
```

---

## 12. Preserved guard and ownership contracts

```text
micro_atlas_group_count=8
heads_per_group=4
scalars_per_group=256
Stage A workgroup_size=64
Stage A values_per_lane=4
Stage A per-element global atomic count=0
Stage B workgroup_size=32
hot_path_map_async_count=0
hot_path_blocking_poll_count=0
hot_path_host_guard_decision_count=0
output_value_readback_count=0
overlapping_candidate_downstream_range_count=0
rejected_candidate_downstream_visibility_count=0
```

Every forced and production route executes the micro-atlas guard, device-token finalizer and indirect downstream staging gate.

---

## 13. Negative controls and manifest

R12-R3-R3-R2 re-executes 580 inherited controls and adds 100:

```text
lexical_extraction=25
pair_matrix=25
direct_statistics=25
thermal_production=25
total=680
```

```text
negative_control_executed_count=680
negative_control_skipped_count=0
negative_control_fail_count=0
```

The R12-R3-R3-R1 bounded manifest builder remains mandatory:

```text
artifact_group_count=6
manifest_deep_json_macro_count=0
duplicate_key_count=0
```

The public flat artifact lookup ABI remains unchanged. Runtime artifacts are generated under `workspace/runtime/attention/` and excluded from the source bake.

---

## 14. Required source changes

```text
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_causal_01b_r12_r3_r3_r2_gate.rs
crates/orchestrator_local/Cargo.toml
specs/ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R2_SPEC.md
```

The R10 attention kernels and backend route implementation remain unchanged. The public ABI revision advances so this gate cannot run against the old unpaired measurement build.

---

## 15. PASS boundary

PASS requires exact parent binding, all lexical fixtures and static checks, 8 probe buckets with two mirrored epochs and balanced AB/BA pairs, direct sign/tail truth, zero order/thermal probe failures, strict 1024 admission, monotonic and stable crossover, LUT replay, 9 production buckets with mirrored epochs, 1024 and 2048 closure, unchanged performance thresholds, preserved guard/zero-wait/output ownership, all 680 controls, artifact/source digest binding and zero model-quality claims.

PASS proves corrected static extraction and measurement truth for the bound runtime profile. It does not prove universal cross-adapter crossover, runtime-adaptive routing, native indirect o_proj matmul, zero invocation of the existing Burn o_proj call, transactional KV rollback, canonical full-model decode, prefill/chunked promotion or quality improvement.

---

## 16. Canonical run

```powershell
$env:CARGO_TARGET_DIR="target-ash-attn-01b-r12-r3-r3-r2"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_causal_01b_r12_r3_r3_r2_gate `
  -- `
  --repo-root . `
  --parent-artifact workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_runtime_artifact.json `
  --parent-manifest workspace/runtime/attention/ash_attn_headwise_causal_01b_r12_r3_r3_local_manifest.json `
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
  --route-policy deterministic-bucket-lut-v2 `
  --probe-kernels single-query-head,gqa2-long-kv-tiled `
  --probe-buckets 512,768,896,1024,1152,1280,1536,2048 `
  --probe-epoch-order ascending,descending `
  --probe-pair-order interleaved-ab-ba `
  --probe-pairs 1024 `
  --probe-rounds 32 `
  --probe-pairs-per-round 32 `
  --require-direct-kernel-sign-test true `
  --require-direct-tail-sign-test true `
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
  --performance-mode paired-gpu-timestamp-mirrored-epochs `
  --production-epoch-order ascending,descending `
  --warmup-iterations 128 `
  --measurement-pairs 1024 `
  --measurement-rounds 32 `
  --internal-canary-prefills 0 `
  --internal-canary-decode-steps 1024 `
  --fault-injection true `
  --require-rollback true `
  --negative-control-mode executed `
  --minimum-live-negative-controls 40 `
  --expected-negative-controls 680 `
  --require-rollback-anchor true `
  --require-authority-commit-order true `
  --full-source-hash true `
  --out-dir workspace/runtime/attention
```

PASS token:

```text
PASS_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R2_LEXICAL_RUST_FUNCTION_EXTRACTION_INTERLEAVED_DUAL_KERNEL_PAIR_MATRIX_DIRECT_KERNEL_TO_KERNEL_SIGN_TEST_THERMAL_DRIFT_RESISTANT_CROSSOVER_1024_GQA2_ADMISSION_DETERMINISTIC_ROUTE_LUT_INCREMENTAL_ONLY_MICRO_ATLAS_GUARD_PRESERVED_ZERO_HOT_PATH_HOST_WAIT_NO_OUTPUT_VALUE_READBACK_NO_RUNTIME_ADAPTIVE_ROUTING_NO_PREFILL_PROMOTION_NO_CHUNKED_PROMOTION_NO_TRANSACTIONAL_ROLLBACK_OVERCLAIM_NO_MODEL_QUALITY_OVERCLAIM
```

HOLD token:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R2_LEXICAL_EXTRACTION_PAIR_MATRIX_DIRECT_SIGN_TEST_OR_THERMAL_CROSSOVER_CLOSURE_INCOMPLETE
```
