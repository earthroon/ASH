# ASH-TCU-K7N-D1R7 SPEC

## Multi-Shape Performance Matrix

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`
- Parent: `d1r6r3-5a2fe5dce27ea58871b0`
- Catalog: `ash_tcu_k7n_d1r7_shape_catalog_v1`
- Required cells: `21`
- PASS: `PASS_ASH_TCU_K7N_D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX_21_OF_21_ADMITTED_PARITY_VALID_PAIRED_MATRIX_NO_BOUNDED_OR_CATASTROPHIC_REGRESSION_NO_OUTPUT_COMMIT_NO_ROUTE_PROMOTION`

D1R7 extends the D1R6-R3 equal-cadence paired contract across a sealed shape catalog. It grants no production route or output authority.

## 2. Parent SSOT

```text
execution_id=d1r6r3-5a2fe5dce27ea58871b0
measurement_valid=true
sync_cadence_equivalent=true
measured_pair_count=2048
paired_comparative_validity=valid_common_mode_environment_drift
performance_classification=non_regression_common_mode_drift
overall_paired_ratio=0.9923791597887865
paired_ratio_p05=0.7878787878787878
output_authority=burn
runtime_output_changed=false
shadow_output_committed=false
production_promotion_authorized=false
```

R3 remains single-shape evidence. No R3 ratio is reused as a D1R7 cell result.

## 3. Audit-Only Route Boundary

The existing D1R2 bundle remains `full_tile_only=true` and `ragged_tail_allowed=false`. D1R7 must not silently weaken that contract.

D1R7 therefore uses an audit-only owned bundle with the canonical K7N WGSL, `VocabAtlasStrideAwareRhsAbi`, explicit bind-group and pipeline layouts, the authoritative Burn Device and Queue, and strict same-device raw-buffer leases.

```text
production_route_authorized=false
route_mutation_count=0
Registry_write_count=0
```

## 4. Canonical Shape Catalog

```text
S00_CONTROL_M1_N16_K4
S01_M2_N16_K4
S02_M15_N16_K4
S03_M16_N16_K4
S04_M17_N16_K4
S05_M1_N1_K4
S06_M1_N15_K4
S07_M1_N17_K4
S08_M1_N31_K4
S09_M1_N32_K4
S10_M1_N33_K4
S11_M1_N16_K1
S12_M1_N16_K3
S13_M1_N16_K5
S14_M1_N16_K15
S15_M1_N16_K16
S16_M1_N16_K17
S17_M2_N17_K5
S18_M15_N31_K15
S19_M16_N32_K16
S20_M17_N33_K17
```

No cell may be added, removed, reordered or replaced at runtime.

## 5. Geometry and Layout

```text
workgroup=16x16x1
dispatch_x=ceil_div(N,16)
dispatch_y=ceil_div(M,16)
dispatch_z=1
```

The K panel extent is loaded from `CandidateLogicalTileGeometry::canonical()` and validated. The current canonical extent is `4`; no fallback is allowed.

```text
LHS storage/logical=[M,K], stride=[K,1]
RHS storage=[N,K], stride=[K,1]
RHS logical=[K,N], stride=[1,K]
materialized_transpose=false
output logical=[M,N]
```

## 6. Fixture Authority

Control uses the D1R5 fixture and digest:

```text
a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200
```

Non-control cells use `ash_tcu_k7n_d1r7_fixture_generator_v1`:

```text
lhs[m,k]=(((m*17+k*7)%31)-15)/16
rhs[n,k]=(((n*13+k*5)%29)-14)/16
```

Required preparation state:

```text
primitive_handle_map_hits=42
primitive_handle_map_misses=0
raw_borrows=42
bridge_host_upload_fallbacks=0
timed_region_host_upload_count=0
```

## 7. Admission and Tail Safety

Every cell validates dimensions, checked allocation sizes, dispatch limits, canonical K-panel availability, RHS stride-aware representation, output-tail and reduction-tail bounds, runtime authority and audit-only route ownership.

Output tails are active when `M%16!=0 || N%16!=0`. Reduction tails are active when `K%canonical_k_tile_extent!=0`.

The canonical shader must retain M/N bounds checks, `k_index < params.k`, and canonical four-lane panel progression. No logical out-of-range read or write is allowed.

## 8. Guard and Parity Preflight

Every audit output allocation appends 16 guard words with pattern `0x7FC12345`.

Control:

```text
exact_bit_match_count=16
exact_bit_mismatch_count=0
failing_element_count=0
Burn digest=control digest
TensorCube digest=control digest
guard mutation count=0
```

Non-control:

```text
absolute_error<=1e-5 OR relative_error<=1e-5
NaN mismatch count=0
infinity mismatch count=0
failing element count=0
guard mutation count=0
```

Parity and guard readback occur before warmup. Performance output readback remains zero.

## 9. Equal-Cadence Timing

Burn authority:

```text
burn_cubecl_matmul_fixture_path
cubecl_compute_client_device_profile_scope
one profile span per operation
external marker timing=false
```

TensorCube authority:

```text
canonical_compute_pass_timestamp_scope
one dispatch per operation
one timestamp pair per operation
```

Required cadence:

```text
Burn operations per sync interval=1
TensorCube operations per sync interval=1
Burn in-flight depth=1
TensorCube in-flight depth=1
sync_cadence_equivalent=true
```

## 10. Matrix Schedule

```text
warmup pairs per shape=128
matrix rounds=32
pairs per shape per round=64
measured pairs per shape=2048
total measured pairs=43008
```

Pair order alternates Burn-first and TensorCube-first. Shape order rotates every two rounds and reverses on odd rounds. Result-dependent ordering, selected reruns and artificial pair delays are forbidden.

## 11. Comparative SSOT and Stability

For each pair:

```text
R_j=Burn_gpu_ns/TensorCube_gpu_ns
D_j=ln(Burn_gpu_ns)-ln(TensorCube_gpu_ns)
```

`D_j` is authoritative.

Per shape:

```text
scaled_log_MAD<=0.13976194237515863
paired_drift_ratio<=1.20
pair_order_bias_ratio<=1.15
matrix_position_bias_ratio<=1.15
```

Absolute stability remains separate. If both absolute paths are unstable, common-mode validity requires log-latency correlation at least `0.90`, matching drift direction, and all paired gates passing.

## 12. Performance Classification

```text
overall_paired_ratio=exp(median(32 batch median log ratios))
paired_ratio_p05=nearest-rank p05 of 2048 pair ratios
```

Non-regression:

```text
overall_paired_ratio>=0.6666666666666666
paired_ratio_p05>=0.5
```

Catastrophic regression:

```text
overall_paired_ratio<0.5
OR paired_ratio_p05<0.3333333333333333
```

Eligible states are `non_regression_absolute_stable`, `non_regression_common_mode_drift`, and `resolution_limited`.

## 13. Control Lineage Guard

```text
parent_control_ratio=0.9923791597887865
exp(abs(ln(D1R7_control_ratio)-ln(parent_control_ratio)))<=1.20
```

## 14. Matrix PASS

```text
shape catalog count=21
admitted shape count=21
parity-passed shape count=21
measurement-valid shape count=21
eligible shape count=21
bounded regression shape count=0
catastrophic regression shape count=0
total measured pair count=43008
control parent ratio drift<=1.20
performance output readback count=0
```

A matrix aggregate cannot override a failed cell. Cell evidence is written before the final verdict.

## 15. Isolation

```text
shadow_output_commit_authorized=false
shadow_output_committed=false
production_promotion_authorized=false
production_route_enabled=false
route_mutation_count=0
Registry_write_count=0
output_authority=burn
runtime_output_changed=false
```

## 16. Artifacts

Immutable root:

```text
artifacts/tensorcube/k7n_d1r7/<execution_id>/
```

Required evidence includes parent receipt, source evidence, catalog, fixture registry, admission and dispatch matrices, parity and guard matrices, matrix schedule, raw pairs, shape batches and statistics, position bias, common-mode matrix, cell classifications, category summaries, matrix receipt, isolation seal, protected-state guard, eligibility, verdict, report, final seal and local manifest.

## 17. PASS Boundary

```text
matrix_valid=true
matrix_eligible=true
admitted_shape_count=21
parity_passed_shape_count=21
measurement_valid_shape_count=21
eligible_shape_count=21
bounded_regression_shape_count=0
catastrophic_regression_shape_count=0
total_measured_pair_count=43008
performance_output_readback_count=0
shadow_output_committed=false
production_promotion_authorized=false
output_authority=burn
runtime_output_changed=false
```

D1R7 PASS authorizes only a separate promotion-review or rollback specification. It does not authorize production routing, Burn replacement, generalized speedup claims or production readiness.
