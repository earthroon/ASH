# ASH-BASETRAIN-GPU-70K-G211C3R4L-R2

## 8x8x4 Route Binding Instrumentation Repair / Kernel Hit Ledger Injection / No Runtime Splice No Promotion Reopen

Seal: Route Binding Instrumentation Repair Only / Kernel Hit Ledger Injection Contract Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4L-R2` consumes the G211C3R4L-R1 kernel utilization audit as its primary input authority. It repairs the evidence contract for the next instrumented probe, but it does not rerun the probe and does not claim speedup.

R4L-R1 established that the R4L clean speedup failure is preserved, but utilization of the intended `TENSORCUBE_8X8X4` kernel was unproven. The safe interpretation is `SPEEDUP_FAILURE_ROUTE_BINDING_UNPROVEN`, not `SPEEDUP_FAILURE_ATTRIBUTABLE_TO_8X8X4`.

`70K-G211C3R4L-R2` may only pass when R4L-R1 PASS is present, `kernel_utilization_verdict = KERNEL_8X8X4_UTILIZATION_UNPROVEN`, `speedup_reinterpretation_class = SPEEDUP_FAILURE_ROUTE_BINDING_UNPROVEN`, `r4l_speedup_verdict_preserved = FRESH_CLEAN_SPEEDUP_NOT_RECOVERED`, `r4l_speedup_recomputed = false`, `r4l_artifacts_rewritten = false`, `expected_kernel_identity = TENSORCUBE_8X8X4`, `all_required_shape_kernel_hits_confirmed = false`, `speedup_failure_attributable_to_8x8x4 = false`, `route_binding_failure_possible = true`, `runtime_splice_allowed = false`, `promotion_allowed = false`, `g211c4_entry_generated = false`, and `next_gate = ASH-BASETRAIN-GPU-70K-G211C3R4L-R2`.

`70K-G211C3R4L-R2` must not rerun benchmark, must not rerun speedup probe, must not recompute speedup ratio, must not rewrite R4L or R4L-R1 artifacts, must not mutate TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not optimize the TensorCube kernel, must not rewrite production WGSL, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup recovery, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4L-R1
8x8x4 Kernel Utilization Audit /
Measured Route Kernel Identity Proof /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_KERNEL_UTILIZATION_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_MEASURED_ROUTE_KERNEL_IDENTITY_PROOF.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_PIPELINE_BIND_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_DISPATCH_HIT_LEDGER.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_FALLBACK_ABSENCE_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_TIMESTAMP_ENVELOPE_AUDIT.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_R4L_SPEEDUP_REINTERPRETATION.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4l_r1/ASH_BASETRAIN_GPU_70K_G211C3R4L_R1_NEXT_ENTRY_PACKET_G211C3R4L_R2.json
artifacts/g211c3r4l_r1/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L_R1.txt
```

Forbidden output:

```text
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4L-R2 injects the missing evidence contract needed before the next fresh clean probe can be meaningfully interpreted. It prepares explicit route binding instrumentation fields, per-shape kernel hit ledger requirements, dispatch identity labels, timestamp envelope target fields, and fallback absence receipts for G211C3R4L-R3.

R4L-R2 proves only this:

```text
R4L-R1 found 8x8x4 utilization unproven
R4L speedup failure remains preserved
R4L speedup was not recomputed
R4L and R4L-R1 artifacts were not rewritten
Route binding evidence contract is ready for R4L-R3
Kernel hit ledger injection contract is ready for R4L-R3
Timestamp envelope target contract is ready for R4L-R3
Fallback absence contract is ready for R4L-R3
Promotion remains closed
Runtime splice remains closed
G211C4 remains closed
```

R4L-R2 does not prove that 8x8x4 was used. R4L-R2 does not prove speedup. R4L-R2 does not repair performance. It repairs observability.

## Required Instrumentation Fields

R4L-R3 must write these fields into runtime receipts and per-shape matrices:

```text
kernel_identity
pipeline_identity
dispatch_identity
shader_module_identity
dispatch_pass_label
measured_interval_role
tile_shape
microtile_shape
workgroup_shape
shape_id
kernel_hit_count
pipeline_bind_count
dispatch_count
fallback_route_used
reference_route_used
scalar_route_used
timestamp_envelope_target
timestamp_envelope_begin_label
timestamp_envelope_end_label
primary_timing_authority
correctness_authority
```

Expected values:

```text
kernel_identity = TENSORCUBE_8X8X4
pipeline_identity = TENSORCUBE_8X8X4_PIPELINE
dispatch_identity = TENSORCUBE_8X8X4_DISPATCH
tile_shape = [8,8,4]
microtile_shape = [8,8,4]
fallback_route_used = false
reference_route_used = false
scalar_route_used = false
timestamp_envelope_target = TENSORCUBE_8X8X4_DISPATCH
```

Per-shape confirmation requirement:

```text
B0 kernel_hit_count >= 1
B1 kernel_hit_count >= 1
B5 kernel_hit_count >= 1
```

## Instrumentation Repair Verdict Values

```text
KERNEL_HIT_LEDGER_INJECTION_READY
ROUTE_BINDING_INSTRUMENTATION_READY
RUNTIME_RECEIPT_FIELD_CONTRACT_READY
TIMESTAMP_ENVELOPE_TARGET_CONTRACT_READY
FALLBACK_ABSENCE_CONTRACT_READY
INSTRUMENTATION_REPAIR_INCOMPLETE
INSTRUMENTATION_REPAIR_CONTRADICTION_DETECTED
INCONCLUSIVE
```

Preferred verdict:

```text
KERNEL_HIT_LEDGER_INJECTION_READY
```

## Instrumentation Repair Classes

```text
ROUTE_BINDING_EVIDENCE_REPAIR_READY
KERNEL_HIT_LEDGER_CONTRACT_READY
TIMESTAMP_ENVELOPE_CONTRACT_READY
FALLBACK_ABSENCE_CONTRACT_READY
R4L_R3_INSTRUMENTED_PROBE_READY
INSTRUMENTATION_REPAIR_INCOMPLETE
INSTRUMENTATION_REPAIR_CONTRADICTION_DETECTED
INCONCLUSIVE
```

Preferred class:

```text
ROUTE_BINDING_EVIDENCE_REPAIR_READY
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4l_r2_route_binding_instrumentation_repair.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4l_r2_route_binding_instrumentation_repair
```

Optional args:

```text
--g211c3r4l-dir artifacts/g211c3r4l
--g211c3r4l-r1-dir artifacts/g211c3r4l_r1
--out-dir artifacts/g211c3r4l_r2
--expected-kernel TENSORCUBE_8X8X4
--expected-tile 8,8,4
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_ROUTE_BINDING_INSTRUMENTATION_REPAIR
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4L-R2
instrumentation_repair_verdict=KERNEL_HIT_LEDGER_INJECTION_READY
instrumentation_repair_class=ROUTE_BINDING_EVIDENCE_REPAIR_READY
r1_kernel_utilization_verdict=KERNEL_8X8X4_UTILIZATION_UNPROVEN
r1_speedup_reinterpretation_class=SPEEDUP_FAILURE_ROUTE_BINDING_UNPROVEN
required_receipt_fields_ready=true
kernel_hit_ledger_injection_ready=true
pipeline_dispatch_identity_contract_ready=true
timestamp_envelope_target_contract_ready=true
fallback_absence_contract_ready=true
r4l_speedup_verdict_preserved=true
r4l_speedup_recomputed=false
r4l_artifacts_rewritten=false
operator_review_required=true
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4L-R3
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4l_r2` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_ROUTE_BINDING_INSTRUMENTATION_REPAIR.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_KERNEL_HIT_LEDGER_INJECTION_PLAN.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_RUNTIME_RECEIPT_FIELD_CONTRACT.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_PIPELINE_DISPATCH_IDENTITY_CONTRACT.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_TIMESTAMP_ENVELOPE_TARGET_CONTRACT.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_FALLBACK_ABSENCE_CONTRACT.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_R4L_R3_INSTRUMENTED_PROBE_ENTRY_PLAN.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_NEXT_ENTRY_PACKET_G211C3R4L_R3.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4l_r2/ASH_BASETRAIN_GPU_70K_G211C3R4L_R2_BAKE_MANIFEST.json
artifacts/g211c3r4l_r2/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4L_R2.txt
```

## PASS Criteria

```text
PASS-01 R4L-R1 PASS marker found
PASS-02 R1 kernel utilization verdict = KERNEL_8X8X4_UTILIZATION_UNPROVEN
PASS-03 R1 speedup reinterpretation class = SPEEDUP_FAILURE_ROUTE_BINDING_UNPROVEN
PASS-04 R4L speedup verdict preserved
PASS-05 R4L speedup not recomputed
PASS-06 R4L artifacts not rewritten
PASS-07 required receipt field contract written
PASS-08 kernel hit ledger injection plan written
PASS-09 pipeline dispatch identity contract written
PASS-10 timestamp envelope target contract written
PASS-11 fallback absence contract written
PASS-12 R4L-R3 instrumented probe entry plan written
PASS-13 instrumentation repair verdict selected exactly once
PASS-14 instrumentation repair class selected exactly once
PASS-15 promotion stop retained
PASS-16 runtime_splice_allowed=false
PASS-17 promotion_allowed=false
PASS-18 G211C3R4L-R3 entry packet generated
PASS-19 G211C4 entry packet not generated
PASS-20 forbidden mutation seal passed
PASS-21 PASS marker printed
```

## PASS Meaning

PASS means R4L-R2 prepared the route binding instrumentation repair contract needed for R4L-R3. It makes future measurements auditable by requiring explicit 8x8x4 kernel identity, pipeline identity, dispatch identity, kernel hit counts, timestamp envelope target, and fallback absence receipts.

PASS does not mean 8x8x4 was used. PASS does not mean speedup recovered. PASS does not mean promotion is allowed. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean production acceleration exists. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4L-R2 route binding instrumentation repair

- Add route binding instrumentation repair gate
- Require R4L-R1 utilization unproven as entry authority
- Define runtime receipt fields for 8x8x4 kernel identity proof
- Add kernel hit ledger injection contract for B0/B1/B5
- Add pipeline and dispatch identity contract
- Add timestamp envelope target contract
- Add fallback absence contract
- Route to G211C3R4L-R3 instrumented fresh clean probe
- Preserve no runtime splice, no production route, no promotion
```
