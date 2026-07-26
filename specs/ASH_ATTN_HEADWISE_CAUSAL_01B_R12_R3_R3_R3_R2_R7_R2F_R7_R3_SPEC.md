# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R3

## Guarded Order-Stratified Relative Authority / Asymmetric Reference-Predecessor Contamination / Candidate-First Production Representativeness / Dual-Stratum Noninferiority Seal

## 0. State

```text
SPEC_ID=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R3
PARENT_SPEC=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7
PARENT_ADDENDUM=R2F-R7-R2_SENTINEL_ORDER_AUTHORITY_ADDENDUM
RUN_MODE=seal-only-v1
DEFAULT_VERDICT=HOLD
RUNTIME_AUTHORITY=Rust-only
STATISTICS_AUTHORITY=raw-paired-samples
ORDER_AUTHORITY=dual-stratum-relative-noninferiority-v1
PRODUCTION_REPRESENTATIVE_STRATUM=candidate-first-ba-v1
REFERENCE_PREDECESSOR_STRATUM=reference-first-ab-v1
```

Forbidden: shader mutation, dispatch geometry mutation, numerical or performance threshold widening, raw-sample filtering, selective rerun, candidate-first-only promotion, reference-first suppression, legacy absolute-order value deletion, production route mutation, payload readback, and candidate output commit.

## 1. Observed failure and attribution

R2F-R7-R2 completed the guarded 8,192-pair population and passed structural validity, combined all-bucket noninferiority, long-KV improvement, epoch validity, raw-sample authority, isolation, rollback, and 520/520 inherited negative controls. The remaining HOLD dimension was the legacy absolute AB/BA order-bias gate.

Canonical order mapping:

```text
AB=reference_then_candidate
BA=candidate_then_reference
```

The reference route performs 32 single-query-head dispatches, while the candidate performs one GQA4 dispatch call. Candidate AB therefore inherits an asymmetric reference predecessor workload that production does not execute. The absolute AB/BA duration difference remains diagnostic, but cannot be the sole guarded order authority.

## 2. Unchanged population and scheduling

```text
8 buckets
32 global rounds
32 pairs per bucket visit
1024 pairs per bucket
8192 guarded pairs
AB=512 per bucket
BA=512 per bucket
AB=4096 global
BA=4096 global
```

The existing `mirrored-pair-query-slot-deconfounded-ab-ba-v2` schedule and order function remain unchanged. No samples are rerun or replaced.

## 3. Statistical surfaces

R7-R3 derives four surfaces from retained raw samples:

1. Combined candidate/reference relative surface.
2. AB reference-first candidate/reference relative surface.
3. BA candidate-first candidate/reference relative surface.
4. Absolute predecessor-effect diagnostic surface.

For each raw sample:

```text
ratio=candidate_duration/reference_duration
```

Combined authority retains the existing parameters:

```text
paired-sign-upper-bound-v1
alpha=0.05
margin=1.05
minimum effective pairs=512
median<=1.05
p95<=1.10
```

AB and BA each require:

```text
raw pairs=512
effective pairs>=256
paired-sign upper-tail probability<=0.05
median ratio<=1.05
p95 ratio<=1.10
```

## 4. Dual-stratum authority

Per bucket:

```text
dual_stratum_noninferiority_pass=
  combined_noninferiority_pass
  AND ab_noninferiority_pass
  AND ba_noninferiority_pass
  AND raw_sample_balance_pass
```

Global order authority requires every bucket to pass the combined, AB, and BA relative surfaces, exact 4096/4096 AB/BA global balance, the existing query-slot deconfounding proof, and epoch validity.

Combined PASS may not hide AB or BA failure. BA may not replace AB. Candidate-first-only promotion is forbidden.

## 5. Candidate-first production representativeness

BA is designated `candidate-first-ba-v1` because the candidate executes without the synthetic 32-dispatch reference predecessor. This designation is semantic and diagnostic. Final promotion still requires AB, BA, and combined noninferiority.

```text
candidate_first_production_representativeness_pass=
  guarded_ba_noninferiority_pass
  AND guarded_ab_ba_balance_pass
  AND query_slot_deconfounding_pass
  AND epoch_validity_pass
```

## 6. Reference-predecessor contamination diagnostics

The following values remain published per bucket:

```text
candidate_ab_median_ns
candidate_ba_median_ns
reference_ab_median_ns
reference_ba_median_ns
candidate_predecessor_penalty_signed_ratio=candidate_ab/candidate_ba-1
candidate_predecessor_penalty_abs_ratio
reference_successor_effect_signed_ratio=reference_ba/reference_ab-1
reference_successor_effect_abs_ratio
candidate_predecessor_contamination_observed
asymmetric_reference_predecessor_contamination_observed
```

The legacy fields remain unchanged:

```text
order_bias_pass
reference_order_bias_signed_ratio
candidate_order_bias_signed_ratio
reference_order_bias_ratio
candidate_order_bias_ratio
```

R7-R3 additionally publishes:

```text
legacy_absolute_order_bias_pass=order_bias_pass
legacy_absolute_order_bias_diagnostic_only=true
```

The raw legacy result must never be overwritten to true.

## 7. Final guarded authority

```text
guarded_order_validity_pass=
  guarded_dual_stratum_noninferiority_pass
  AND guarded_ab_ba_balance_pass
  AND guarded_query_slot_deconfounding_pass

guarded_measurement_validity_pass=
  guarded_order_validity_pass
  AND guarded_epoch_validity_pass
  AND guarded_raw_sample_authority_pass
```

Production-route shadow eligibility still requires structural validity, kernel continuity, combined noninferiority, long-KV improvement, dual-stratum authority, isolation, active-route identity, and rollback.

## 8. Per-bucket receipt

Each `Gqa4GuardedBucketReceipt` publishes combined, AB, and BA raw/effective counts; sign-test probability; success fraction; median and p95 ratios; independent pass values; dual-stratum pass; predecessor diagnostics; retained legacy absolute-order fields; raw balance; epoch validity; full-head comparison; guard counters; and all raw samples.

## 9. Global receipt

`HeadwiseGqa4R2fReceipt` publishes:

```text
order_authority_policy
production_representative_stratum
reference_predecessor_stratum
guarded_combined_noninferiority_pass
guarded_ab_noninferiority_pass
guarded_ba_noninferiority_pass
guarded_dual_stratum_noninferiority_pass
guarded_ab_raw_sample_count
guarded_ba_raw_sample_count
guarded_ab_ba_balance_pass
candidate_first_production_representativeness_pass
reference_predecessor_contamination_receipt_pass
legacy_absolute_order_bias_all_bucket_pass
legacy_absolute_order_bias_diagnostic_only
```

A separate order-stratified statistics artifact is emitted from the same raw receipt.

## 10. Strict CLI extension

Exact values:

```text
--gqa4-r2f-order-authority-policy dual-stratum-relative-noninferiority-v1
--gqa4-r2f-production-representative-stratum candidate-first-ba-v1
--gqa4-r2f-reference-predecessor-policy asymmetric-contamination-diagnostic-v1
--gqa4-r2f-stratum-statistics-source raw-order-partitioned-paired-samples-v1
--gqa4-r2f-stratum-minimum-raw-pairs 512
--gqa4-r2f-stratum-minimum-effective-pairs 256
--gqa4-r2f-legacy-absolute-order-policy diagnostic-only-retained-v1
```

Required Boolean keys:

```text
--require-gqa4-r2f-combined-relative-noninferiority true
--require-gqa4-r2f-ab-relative-noninferiority true
--require-gqa4-r2f-ba-relative-noninferiority true
--require-gqa4-r2f-dual-stratum-noninferiority true
--require-gqa4-r2f-ab-ba-raw-balance true
--require-gqa4-r2f-query-slot-stratum-balance true
--require-gqa4-r2f-candidate-first-production-representativeness true
--require-gqa4-r2f-reference-predecessor-diagnostic true
--require-gqa4-r2f-legacy-absolute-order-retention true
--require-gqa4-r2f-legacy-absolute-order-nonauthoritative true
--forbid-gqa4-r2f-candidate-first-only-promotion true
--forbid-gqa4-r2f-stratum-sample-filtering true
--forbid-gqa4-r2f-stratum-selective-rerun true
```

The R7-R3 registry extension is exactly 20 unique required keys.

## 11. Negative controls

R7-R3 adds twelve ten-control groups:

```text
AB/BA semantic mapping
combined relative authority
AB relative authority
BA relative authority
dual-stratum conjunction
raw stratum balance
effective-pair population
candidate-first representativeness
reference-predecessor diagnostics
legacy order retention
legacy order nonauthority
stratum no-filter/no-rerun
```

```text
parent R2E-R7 controls=260
R7-R3 current controls=380
combined authority=640
```

## 12. PASS

PASS requires strict CLI sealing; exact parent authority; preflight; 384-pair continuity sentinel; workload economy; matched output/downstream contracts; full overwrite; guard map/finalizer; GPU decision/downstream; 8,192 retained guarded samples; 4,096 AB and 4,096 BA samples; all-bucket combined, AB, BA, and dual-stratum noninferiority; exact balance; query-slot deconfounding; epoch validity; candidate-first representativeness; predecessor diagnostic receipt; legacy field retention with diagnostic-only authority; long-KV requirements; zero filtering/rerun/readback/commit/consumer/route mutation; isolation; rollback; active-route identity; and 640/640 combined negative controls.

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R3_GUARDED_DUAL_STRATUM_RELATIVE_AUTHORITY_AND_REFERENCE_PREDECESSOR_CONTAMINATION_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R3_DUAL_STRATUM_NONINFERIORITY_OR_SHADOW_ELIGIBILITY_NOT_PROVEN
```

## 13. Final seal

```text
combined relative noninferiority
+ reference-first AB relative noninferiority
+ candidate-first BA relative noninferiority
+ exact AB/BA and query-slot balance
+ retained absolute predecessor-effect diagnostics
+ unchanged 8192-pair guarded population
= order-robust promotion evidence without misattributing synthetic predecessor load to candidate regression
```
