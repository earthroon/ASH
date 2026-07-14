# ASH-TCU-K7N-D1R12-R5-R3A SPEC

## Targeted S05 Affected-Share Gate Audit

## 1. Patch Identity

```text
ASH-TCU-K7N-D1R12-R5-R3A_TARGETED_S05_AFFECTED_SHARE_GATE_AUDIT
```

PASS marker:

```text
PASS_ASH_TCU_K7N_D1R12_R5_R3A_TARGETED_S05_AFFECTED_SHARE_GATE_AUDIT_EVIDENCE_CLASSIFIED_PARENT_POLICY_IMMUTABLE
```

Failure marker:

```text
FAIL_ASH_TCU_K7N_D1R12_R5_R3A_TARGETED_S05_AFFECTED_SHARE_GATE_AUDIT_RUNTIME_EVIDENCE_OR_PROTECTED_STATE_VIOLATION
```

## 2. Required Parents

```text
R4 execution=d1r12-r4-69c1e6aec6a09d5506f1
R4 outcome=non_coverage_policy_regression_persists

R5-R1 execution=d1r12-r5-r1-7a8b3d1656b3d6213586
R5-R1 outcome=cardinality_aliasing_confirmed

R5-R2 execution=d1r12-r5-r2-c3396b7fd36a7f5b0a1e
R5-R2 outcome=semantic_repair_completed
```

## 3. Target Route

```text
route_id=ash.tensorcube.k7n.d1r9.shadow.s05_m1_n1_k4.568e107d07767a58
shape_id=S05_M1_N1_K4
parent_classification=conditional_hold
authoritative_red_bucket_count=2
amber_bucket_count=12
affected_effective_traffic_share=0.0174244486795535
classification_causal_gate=affected_effective_traffic_share
varied_red_domain_count=3
single_axis_corroborated_domain_count=0
```

The two authoritative-red buckets are resolved from the immutable R4 canonical bucket evidence and assigned by canonical lexical order. Axis values must not be guessed or hardcoded.

## 4. Gate Semantics

```text
route_wide_min_red_bucket_count=2
route_wide_min_affected_share=0.40
route_wide_min_dimension_count=2
single_bucket_weight_cap=0.25
```

The affected share does not cause the latency regression. It is the route-wide qualifier that prevents promotion from `conditional_hold` to `confirmed_hold` under the unchanged R2 policy.

## 5. Controls

Resolve three distinct non-red controls from the same route and same shape:

```text
control_a=nearest proximal non-red to target A
control_b=nearest distinct proximal non-red to target B
shared_control=minimize maximum Hamming distance to both targets
```

Selection priority is Hamming distance, health class, parent sample count, traffic share and canonical lexical order. Exact Hamming-1 controls are preferred but not assumed.

Forbidden:

```text
cross-route fallback
cross-shape fallback
target reuse
control duplication
red or invalid control selection
measurement-result-dependent selection
```

## 6. Replay Budget

```text
per target warm steady pairs=64
per target queue-isolated pairs=32
per target parent-matched nominal-contention pairs=64
pairs per target=160

target pairs=320
control pairs=96
total pairs=416
Burn-first pairs=208
TensorCube-first pairs=208
process epochs=13
```

The parent process spawns child segments under:

```text
workspace/runtime/tensorcube/.staging/<execution_id>/segments/
```

All evidence is produced by local Rust. The parent verifies plan digest, segment digest, pair continuity, request uniqueness, sample counts and parity before artifact promotion.

## 7. Persistence and Measurement

Each target receives independent warm, isolated and nominal cohort health classification using the unchanged R2 policy.

```text
persistent = warm red and (isolated red or nominal red)
cohort_conditional = at least one production-relevant cohort red but persistent rule not met
not_reproduced = warm, isolated and nominal all not red
```

Required outputs:

```text
s05_red_bucket_a_persistence
s05_red_bucket_b_persistence
s05_measurement_validity
s05_control_authoritative_red_count
```

## 8. Effective-Weight Provenance

Reconstruct:

```text
target A effective weight + target B effective weight
= 0.0174244486795535
```

Audit exact sum, duplicate contribution IDs, diagnostic-only leakage, non-authoritative leakage, unknown owners and dimension-expanded multiplication.

## 9. Bucket Independence

Independence requires distinct canonical keys, parent receipt digests, request-key sets, sample receipt sets and effective-weight contribution IDs, with zero raw measurement aliasing and both targets persistent.

Allowed states:

```text
independent
non_independent
insufficient
```

`varied_red_domain_count=3` is not by itself proof of independence.

## 10. Normalized Outcomes

Exactly one:

```text
persistent_independent_affected_share_regression
persistent_non_independent_red_evidence
affected_share_aggregation_overreach
historical_s05_red_not_reproduced
s05_control_spillover
s05_measurement_indeterminate
```

Every conclusive outcome is non-committing and authorizes R5-R4 reconciliation only.

## 11. R5-R4 Branch Contract

Required latest files:

```text
ash_tensorcube_k7n_d1r12_r5_r3a_branch_summary_latest.json
ash_tensorcube_k7n_d1r12_r5_r3a_final_seal_latest.json
ash_tensorcube_k7n_d1r12_r5_r3a_local_manifest_latest.json
```

The branch summary must include the execution ID, selected outcome, normalized S05 state, target/control counts, both target persistence states, affected-share reconstruction, duplicate count, control red count, independence state, measurement validity, recommendation, classification change counts and Burn output authority.

## 12. Protected State

Required:

```text
parent artifact rewrite count=0
route classification change count=0
bucket classification change count=0
policy mutation count=0
threshold mutation count=0
effective-weight mutation count=0
registry mutation count=0
route epoch change count=0
TensorCube authoritative output count=0
production output commit count=0
output_authority=burn
runtime_output_changed=false
```

## 13. Implementation Surface

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r12_r5_r3a_s05_affected_share_gate_audit.rs
crates/model_core/src/vocab_atlas_shadow_s05_affected_share_gate_audit_contract.rs
crates/orchestrator_local/src/ash_tcu_k7n_d1r12_r5_r3a_s05_affected_share_gate_audit_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r12_r5_r3a_s05_affected_share_gate_audit.rs
```

Registration files:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

Normal crate exports and separate backend/model crate-root fingerprint seals are required. Direct backend or model source inclusion is forbidden.

## 14. Exit Codes

```text
conclusive normalized state=0
measurement indeterminate=5
runtime or parity failure=6
parent mismatch=7
protected-state violation=70
```

## 15. Next State

```text
ASH-TCU-K7N-D1R12-R5-R4_PARALLEL_GATE_EVIDENCE_RECONCILIATION
```

R5-R3A does not mutate S05 classification or authorize production promotion.