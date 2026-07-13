# ASH-TCU-K7N-D1R8 SPEC

## Promotion Review and Shadow Route Decision

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R8_PROMOTION_REVIEW_AND_SHADOW_ROUTE_DECISION`
- Parent execution: `d1r7-a55d32dd45c9f21cdf02`
- Review PASS:

```text
PASS_ASH_TCU_K7N_D1R8_PROMOTION_REVIEW_AND_SHADOW_ROUTE_DECISION_EVIDENCE_RECONCILED_DECISION_SEALED_NO_ROUTE_MUTATION_NO_OUTPUT_COMMIT
```

- Review FAIL:

```text
FAIL_ASH_TCU_K7N_D1R8_PROMOTION_REVIEW_AND_SHADOW_ROUTE_DECISION_EVIDENCE_INVALID_OR_DECISION_UNSEALED
```

D1R8 is a CPU-side evidence review. It performs no GPU benchmark, shadow dispatch, route mutation, Registry write, output commit, shader mutation or model-weight mutation.

## 2. Parent SSOT

Required D1R7 state:

```text
shape_catalog_count=21
admitted_shape_count=21
parity_passed_shape_count=21
measurement_valid_shape_count=21
eligible_shape_count=21
bounded_regression_shape_count=0
catastrophic_regression_shape_count=0
total_measured_pair_count=43008
control_parent_ratio_drift=1.038422123652415
shape_ratio_geometric_median=1.0176140315959048
worst_shape_by_median_ratio=S15_M1_N16_K16
worst_shape_by_p05_ratio=S15_M1_N16_K16
performance_output_readback_count=0
output_authority=burn
runtime_output_changed=false
shadow_output_committed=false
production_promotion_authorized=false
```

D1R8 must load and reconcile the D1R7 local manifest, final seal, matrix receipt, 21 full cell receipts, parity matrix, guard matrix, shape statistics, category summaries and canonical shape catalog.

The D1R7 manifest's immutable artifact hashes must match current bytes. The full cell artifact must serialize identically to the cell vector inside the matrix receipt.

## 3. Review PASS Is Not Promotion

D1R8 PASS means:

```text
parent evidence reconciled
21 policy bands assigned
control and S15 explicitly reviewed
one decision selected
review artifacts sealed
no runtime mutation occurred
```

It does not mean:

```text
production route enabled
TensorCube output authoritative
Burn output replaced
full-vocabulary parity proven
end-to-end speedup proven
```

## 4. Decision Enum

Exactly one decision is sealed:

```text
promote_observed_shapes_shadow_all
promote_observed_shapes_shadow_partial
hold_for_additional_evidence
rollback_tensorcube_candidate
```

Outcome markers:

```text
DECISION_ASH_TCU_K7N_D1R8_PROMOTE_OBSERVED_SHAPES_SHADOW_ALL
DECISION_ASH_TCU_K7N_D1R8_PROMOTE_OBSERVED_SHAPES_SHADOW_PARTIAL
DECISION_ASH_TCU_K7N_D1R8_HOLD_FOR_ADDITIONAL_EVIDENCE
DECISION_ASH_TCU_K7N_D1R8_ROLLBACK_TENSORCUBE_CANDIDATE
```

## 5. Promotion Policy Bands

### Green

A cell is `promotion_green` only when:

```text
D1R7 cell eligible=true
classification is non-regression absolute-stable or common-mode-drift
resolution_limited=false
overall_paired_ratio>=0.95
paired_ratio_p05>=0.75
scaled_log_MAD<=0.09531017980432493
paired_drift_ratio<=1.10
pair_order_bias_ratio<=1.10
matrix_position_bias_ratio<=1.10
parity_passed=true
guard_passed=true
```

Green cells are eligible for an exact-signature shadow recommendation only.

### Amber

A cell is `promotion_amber` when it passed D1R7 but misses one or more stricter green headroom gates, including resolution-limited cells. Amber cells remain on the holdlist and cannot enter the whitelist.

### Red

A cell is `promotion_red` when admission, parity, guard, measurement validity, D1R7 non-regression, the median safety floor `2/3`, or the p05 safety floor `0.5` fails.

A red cell selects candidate rollback. Missing evidence fails the review and does not silently synthesize a rollback decision.

## 6. Exact Shape Signature

Every whitelist entry owns an exact signature containing:

```text
shape_id
M/N/K
LHS shape and stride
RHS storage shape
RHS logical shape and stride
output shape
dtype
workgroup
dispatch
canonical K tile extent
shader digest
ABI digest
pipeline-layout digest
```

Range promotion is forbidden. A future route must not interpret the 21 observed cells as `M<=17`, `N<=33`, `K<=17` or as a dispatch-equivalent range.

## 7. Control Review

Required control:

```text
S00_CONTROL_M1_N16_K4
```

Required correctness:

```text
exact_bit_match_count=16
exact_bit_mismatch_count=0
failing_element_count=0
control_digest_match=true
```

Policy boundaries:

```text
parent ratio drift<=1.10: green lineage
1.10<parent ratio drift<=1.20: amber lineage
parent ratio drift>1.20: rollback
```

## 8. S15 Worst-Cell Review

Required shape:

```text
S15_M1_N16_K16
```

D1R8 records its:

```text
overall paired ratio
paired p05 ratio
Burn and TensorCube median GPU ns
Burn and TensorCube p95 GPU ns
scaled log MAD
paired drift
pair-order bias
matrix-position bias
absolute stability
common-mode status
resolution-limited status
maximum absolute and relative error
maximum ULP distance
guard mutation count
```

S15 enters a whitelist only when its policy band is green.

## 9. Category Coverage

Required categories:

```text
control
aligned_output
output_tail
reduction_tail
multi_dispatch_x
multi_dispatch_y
composite_tail
```

A category is covered only by at least one green exact-signature cell. Amber cells cannot satisfy category coverage.

## 10. Decision Rules

### All observed shapes shadow

```text
green_shape_count=21
amber_shape_count=0
red_shape_count=0
resolution_limited_shape_count=0
all categories covered
control lineage green
```

### Partial observed-shape shadow

```text
green_shape_count>=1
red_shape_count=0
all categories covered
control cell green
```

The whitelist contains green cells only. Amber cells remain on the holdlist.

### Hold

Selected when there are no red cells, but green coverage, control headroom or category coverage is incomplete.

### Rollback

Selected when any red cell exists or the control lineage crosses the rollback boundary.

D1R8 itself applies none of these decisions.

## 11. Full-Vocabulary Boundary

Required review state:

```text
full_vocabulary_parity_available=false
maximum_authorized_scope=exact_signature_non_authoritative_shadow_only
```

The absence of full-vocabulary evidence does not erase the D1R7 matrix, but it forbids production output authority and generalized performance claims.

## 12. Runtime Authority and Isolation

Required sealed state:

```text
gpu_benchmark_count=0
shadow_dispatch_count=0
route_mutation_authorized=false
route_mutation_count=0
route_epoch_change_count=0
Registry_write_count=0
output_commit_count=0
output_authority=burn
runtime_output_changed=false
operator_approval_required=true
operator_approval_recorded=false
```

Protected hashes cover D1R7 evidence, Registry state when present, canonical K7N WGSL, RHS ABI, pipeline-layout source and Burn baseline source. Only D1R8 review artifacts may change.

## 13. Required Source Files

Backend review modules:

```text
tensorcube_k7n_d1r8_parent_evidence.rs
tensorcube_k7n_d1r8_shape_signature.rs
tensorcube_k7n_d1r8_policy_band.rs
tensorcube_k7n_d1r8_control_review.rs
tensorcube_k7n_d1r8_s15_review.rs
tensorcube_k7n_d1r8_category_coverage.rs
tensorcube_k7n_d1r8_shadow_whitelist.rs
tensorcube_k7n_d1r8_risk_register.rs
tensorcube_k7n_d1r8_decision.rs
tensorcube_k7n_d1r8_decision_receipt.rs
tensorcube_k7n_d1r8_contract_audit.rs
tensorcube_k7n_d1r8_verdict.rs
```

Model contract:

```text
crates/model_core/src/vocab_atlas_shadow_route_decision_contract.rs
```

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r8_promotion_review_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r8_promotion_review_and_shadow_route_decision.rs
```

## 14. Required Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r8/<execution_id>/
```

Latest mirrors include:

```text
parent_evidence_index
parent_digest_reconciliation
model_contract
source_identity
cell_policy_bands
control_review
s15_worst_cell_review
category_coverage
shadow_whitelist
shadow_holdlist
shadow_rollback_list
risk_register
full_vocabulary_boundary
decision_trace
decision_receipt
zero_route_mutation
protected_state_guard
state
report
verdict
final_seal
local_manifest
```

## 15. Review PASS Boundary

```text
parent evidence valid=true
reviewed_shape_count=21
cell policy bands complete=true
control review complete=true
S15 review complete=true
category coverage complete=true
decision count=1
decision receipt written=true
decision trace written=true
route_mutation_authorized=false
route_mutation_count=0
output_authority=burn
runtime_output_changed=false
operator_approval_required=true
operator_approval_recorded=false
```

## 16. Review PASS Verdict

```text
the_d1r7_twenty_one_shape_admission_parity_guard_and_equal_cadence_performance_evidence_was_reconciled_without_parent_evidence_drift_each_shape_was_assigned_a_deterministic_promotion_policy_band_the_control_and_s15_worst_cell_were_explicitly_reviewed_exact_signature_category_coverage_and_full_vocabulary_boundaries_were_recorded_and_one_shadow_route_decision_was_sealed_without_route_mutation_output_commit_burn_authority_change_or_production_claim
```

## 17. Next State

- All or partial shadow decision authorizes drafting only `ASH-TCU-K7N-D1R9_SHADOW_ROUTE_EXACT_SIGNATURE_APPLY`.
- Hold authorizes drafting only `ASH-TCU-K7N-D1R8-R1_ADDITIONAL_EVIDENCE_PLAN`.
- Rollback authorizes drafting only `ASH-TCU-K7N-D1R9_TENSORCUBE_CANDIDATE_ROLLBACK_APPLY`.

No next patch runs automatically.

## 18. Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r8_promotion_review_and_shadow_route_decision -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r7-execution d1r7-a55d32dd45c9f21cdf02 `
  --require-parent-shape-catalog-count 21 `
  --require-parent-admitted-shape-count 21 `
  --require-parent-parity-passed-shape-count 21 `
  --require-parent-measurement-valid-shape-count 21 `
  --require-parent-eligible-shape-count 21 `
  --require-parent-bounded-regression-shape-count 0 `
  --require-parent-catastrophic-regression-shape-count 0 `
  --require-parent-total-measured-pair-count 43008 `
  --require-parent-control-ratio-drift 1.038422123652415 `
  --require-parent-shape-ratio-geometric-median 1.0176140315959048 `
  --require-parent-worst-median-shape S15_M1_N16_K16 `
  --require-parent-worst-p05-shape S15_M1_N16_K16 `
  --require-parent-output-authority burn `
  --require-shape-receipt-count 21 `
  --require-green-median-ratio-at-least 0.95 `
  --require-green-p05-ratio-at-least 0.75 `
  --require-green-scaled-log-mad-at-most 0.09531017980432493 `
  --require-green-paired-drift-ratio-at-most 1.10 `
  --require-green-pair-order-bias-ratio-at-most 1.10 `
  --require-green-matrix-position-bias-ratio-at-most 1.10 `
  --review-control-cell S00_CONTROL_M1_N16_K4 `
  --require-control-green-parent-ratio-drift-at-most 1.10 `
  --require-control-rollback-parent-ratio-drift-over 1.20 `
  --review-worst-cell S15_M1_N16_K16 `
  --record-shadow-output-authority burn `
  --require-operator-approval-recorded false `
  --require-d1r7-pass `
  --require-parent-runtime-output-unchanged `
  --load-parent-manifest `
  --load-parent-final-seal `
  --load-parent-cell-receipts `
  --load-parent-parity-matrix `
  --load-parent-guard-matrix `
  --load-parent-shape-statistics `
  --load-parent-category-summaries `
  --require-parent-digests-exact `
  --reject-duplicate-shape-receipts `
  --reject-unknown-shape-receipts `
  --reconcile-parent-matrix-summary `
  --require-all-parent-cells-admitted `
  --require-all-parent-cells-parity-passed `
  --require-all-parent-cells-guard-passed `
  --require-all-parent-cells-measurement-valid `
  --require-zero-parent-bounded-regressions `
  --require-zero-parent-catastrophic-regressions `
  --classify-promotion-policy-bands `
  --reject-resolution-limited-green-cell `
  --require-s15-explicit-policy-band `
  --compute-promotion-category-coverage `
  --build-exact-shape-shadow-whitelist `
  --reject-range-based-shape-promotion `
  --record-full-vocabulary-parity-unavailable `
  --select-single-shadow-route-decision `
  --write-risk-register `
  --write-decision-trace `
  --write-decision-receipt `
  --require-operator-approval `
  --require-no-gpu-benchmark `
  --require-no-shadow-dispatch `
  --require-no-route-mutation `
  --require-no-route-epoch-change `
  --require-no-registry-write `
  --require-no-output-commit `
  --verify-d1r7-evidence-unchanged `
  --verify-k7n-shader-unchanged `
  --verify-k7n-abi-unchanged `
  --verify-pipeline-layout-unchanged `
  --verify-burn-output-authority `
  --verify-model-weights-unchanged `
  --write-final-seal `
  --no-runtime-output-change `
  --no-production-claim `
  --require-category control `
  --require-category aligned_output `
  --require-category output_tail `
  --require-category reduction_tail `
  --require-category multi_dispatch_x `
  --require-category multi_dispatch_y `
  --require-category composite_tail `
  --allow-decision promote_observed_shapes_shadow_all `
  --allow-decision promote_observed_shapes_shadow_partial `
  --allow-decision hold_for_additional_evidence `
  --allow-decision rollback_tensorcube_candidate
```
