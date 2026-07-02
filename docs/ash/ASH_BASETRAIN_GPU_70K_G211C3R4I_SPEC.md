# ASH-BASETRAIN-GPU-70K-G211C3R4I

## Clean Attribution Decision Ledger / R4E Mixed Loss Rejection Seal / No Runtime Splice No Promotion Reopen

Seal: Clean Attribution Decision Ledger Only / R4E Mixed Loss Rejection Seal Only / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4I` consumes the G211C3R4H clean attribution outputs as its primary input authority and preserves the G211C3 `STOP_PERF_LOSS` result.

`70K-G211C3R4I` may only pass when R4H PASS is present, `recheck_verdict = B5_CLEAN_RESIDUAL_LOW`, `recheck_class = B5_CLEAN_RESIDUAL_LOW`, `b5_clean_residual_present = false`, `b5_clean_residual_low = true`, `r4e_mixed_attribution_recovered = false`, `r4e_mixed_attribution_rejected = true`, `r4e_mixed_attribution_held_for_r4i = false`, R4F poll/map contamination context exists, R4G poll/map isolation context exists, R4E mixed attribution context exists, C3 STOP_PERF_LOSS context exists, parity remains pass, timestamp stability is retained, promotion stop is retained, and no G211C4 entry packet exists.

`70K-G211C3R4I` must not mutate TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write or modify model weights, must not write checkpoints, must not execute optimizer or training steps, must not implement TensorCube kernel optimization, must not rewrite a production WGSL kernel, must not change production tile/workgroup/padding policy, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4H
Odd Tail Padding Recheck /
Post Poll-Map Clean Attribution /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_ODD_TAIL_PADDING_RECHECK.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_CLEAN_DISPATCH_ATTRIBUTION_MATRIX.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_ODD_TAIL_PADDING_PRESSURE_MATRIX.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_B5_RESIDUAL_SUMMARY.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_R4E_MIXED_ATTRIBUTION_RECHECK_AUDIT.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_NEXT_ENTRY_PACKET_G211C3R4I.json
artifacts/g211c3r4h/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4H.txt
```

Reference evidence:

```text
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_READBACK_POLL_MAP_SPLIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_ATTRIBUTION_NORMALIZATION.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_CONTAMINATION_RATIO_SUMMARY.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_R4E_VERDICT_RETENTION_AUDIT.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_R1_NEXT_GATE_READER_HOTFIX.json
artifacts/g211c3r4f/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4F.txt
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_POLL_MAP_WAIT_ISOLATION.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_READBACK_FREE_DISPATCH_MATRIX.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_R4E_ATTRIBUTION_RECOVERY_AUDIT.json
artifacts/g211c3r4g/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4G.txt
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_KERNEL_TILE_PADDING_ATTRIBUTION.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_ATTRIBUTION_SUMMARY.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_R1_ACCEPT_PAIR_HOTFIX.json
artifacts/g211c3r4e/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4E.txt
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_TENSORCUBE_MICROBENCH_BASELINE.json
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_PROMOTION_STOP_PACKET.json
artifacts/g211c3/PASS_ASH_BASETRAIN_GPU_70K_G211C3.txt
```

Forbidden evidence:

```text
artifacts/g211c3/ASH_BASETRAIN_GPU_70K_G211C3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r2/ASH_BASETRAIN_GPU_70K_G211C3R2_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r3/ASH_BASETRAIN_GPU_70K_G211C3R3_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4a/ASH_BASETRAIN_GPU_70K_G211C3R4A_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4b/ASH_BASETRAIN_GPU_70K_G211C3R4B_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4c/ASH_BASETRAIN_GPU_70K_G211C3R4C_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4e/ASH_BASETRAIN_GPU_70K_G211C3R4E_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4f/ASH_BASETRAIN_GPU_70K_G211C3R4F_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4g/ASH_BASETRAIN_GPU_70K_G211C3R4G_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4h/ASH_BASETRAIN_GPU_70K_G211C3R4H_NEXT_ENTRY_PACKET_G211C4.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_NEXT_ENTRY_PACKET_G211C4.json
```

## Purpose

G211C3R4I seals the clean attribution decision ledger. It rejects the R4E `SETUP_AND_KERNEL_MIXED_LOSS` attribution as current authority after R4F poll/map contamination detection, R4G poll/map isolation, and R4H B5 clean residual recheck.

G211C3R4I proves only this:

```text
C3 STOP_PERF_LOSS remains active
R4E SETUP_AND_KERNEL_MIXED_LOSS was the pre-clean attribution
R4F found POLL_MAP_CONTAMINATION_DOMINANT
R4G isolated POLL_MAP_WAIT and recovered readback-free dispatch
R4H found B5_CLEAN_RESIDUAL_LOW
R4H rejected R4E mixed attribution
R4I preserves no runtime splice
R4I preserves no promotion reopen
R4I preserves no G211C4 entry
R4I routes to R4J, not G211C4
```

## Ledger Classes

```text
R4E_MIXED_LOSS_REJECTED_BY_CLEAN_ATTRIBUTION
POLL_MAP_CONTAMINATION_PRIMARY_CAUSE
B5_CLEAN_RESIDUAL_LOW_CONFIRMED
MEASUREMENT_HYGIENE_CLOSEOUT_REQUIRED
ROUTE_POLICY_REVIEW_REQUIRED
PROMOTION_STOP_RECONCILED
LEDGER_INCOMPLETE
LEDGER_CONTRADICTION_DETECTED
LEDGER_PARITY_FAILED
LEDGER_TIMESTAMP_UNSTABLE
INCONCLUSIVE
```

## Ledger Verdict Values

```text
R4E_MIXED_LOSS_REJECTED
POLL_MAP_CONTAMINATION_SEALED
B5_CLEAN_RESIDUAL_LOW_SEALED
PROMOTION_STOP_RECONCILED
MEASUREMENT_HYGIENE_CLOSEOUT_REQUIRED
ROUTE_POLICY_REVIEW_REQUIRED
LEDGER_INCOMPLETE
LEDGER_CONTRADICTION_DETECTED
LEDGER_PARITY_FAILED
LEDGER_TIMESTAMP_UNSTABLE
INCONCLUSIVE
```

Preferred safe verdict:

```text
R4E_MIXED_LOSS_REJECTED
```

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4i_clean_attribution_decision_ledger.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4i_clean_attribution_decision_ledger
```

Optional args:

```text
--g211c3-dir artifacts/g211c3
--g211c3r2-dir artifacts/g211c3r2
--g211c3r3-dir artifacts/g211c3r3
--g211c3r4a-dir artifacts/g211c3r4a
--g211c3r4b-dir artifacts/g211c3r4b
--g211c3r4c-dir artifacts/g211c3r4c
--g211c3r4d-dir artifacts/g211c3r4d
--g211c3r4d-r2-dir artifacts/g211c3r4d_r2
--g211c3r4e-dir artifacts/g211c3r4e
--g211c3r4f-dir artifacts/g211c3r4f
--g211c3r4g-dir artifacts/g211c3r4g
--g211c3r4h-dir artifacts/g211c3r4h
--out-dir artifacts/g211c3r4i
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4I_CLEAN_ATTRIBUTION_DECISION_LEDGER
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4I
ledger_verdict=<...>
ledger_class=<...>
r4e_mixed_loss_final_state=REJECTED
r4e_mixed_loss_rejected=<true|false>
poll_map_contamination_sealed=<true|false>
b5_clean_residual_low_sealed=<true|false>
c3_stop_perf_loss_retained=<true|false>
promotion_stop_reconciled=<true|false>
route_policy_review_required=<true|false>
measurement_hygiene_closeout_required=<true|false>
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4J
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4i` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_CLEAN_ATTRIBUTION_DECISION_LEDGER.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_R4E_MIXED_LOSS_REJECTION_SEAL.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_MEASUREMENT_CONTAMINATION_LINEAGE.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_PROMOTION_STOP_RECONCILIATION.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_ROUTE_POLICY_RECOMMENDATION.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_NEXT_ENTRY_PACKET_G211C3R4J.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_BAKE_MANIFEST.json
artifacts/g211c3r4i/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4I.txt
```

Forbidden output:

```text
artifacts/g211c3r4i/ASH_BASETRAIN_GPU_70K_G211C3R4I_NEXT_ENTRY_PACKET_G211C4.json
```

## PASS Criteria

```text
PASS-01 R4H PASS marker found
PASS-02 R4H recheck_verdict = B5_CLEAN_RESIDUAL_LOW
PASS-03 R4H recheck_class = B5_CLEAN_RESIDUAL_LOW
PASS-04 R4H b5_clean_residual_present=false
PASS-05 R4H b5_clean_residual_low=true
PASS-06 R4H r4e_mixed_attribution_recovered=false
PASS-07 R4H r4e_mixed_attribution_rejected=true
PASS-08 R4H r4e_mixed_attribution_held_for_r4i=false
PASS-09 R4F poll/map contamination context found
PASS-10 R4G poll/map isolation context found
PASS-11 R4E mixed attribution context found
PASS-12 C3 STOP_PERF_LOSS context found
PASS-13 G211C4 entry packet absent
PASS-14 clean attribution decision ledger written
PASS-15 R4E mixed loss rejection seal written
PASS-16 measurement contamination lineage written
PASS-17 promotion stop reconciliation written
PASS-18 route policy recommendation written
PASS-19 ledger verdict selected exactly once
PASS-20 ledger class selected exactly once
PASS-21 promotion stop retained
PASS-22 runtime_splice_allowed=false
PASS-23 promotion_allowed=false
PASS-24 G211C3R4J entry packet generated
PASS-25 G211C4 entry packet not generated
PASS-26 forbidden mutation seal passed
PASS-27 PASS marker printed
```

## PASS Meaning

PASS means G211C3R4I sealed the clean attribution decision ledger, rejected R4E mixed loss as current authority, preserved C3 STOP_PERF_LOSS, and routed to R4J without runtime splice, promotion reopen, or G211C4 entry.

PASS does not mean TensorCube is faster. PASS does not mean TensorCube timing hygiene is fully complete. PASS does not mean TensorCube optimization has been applied. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed. PASS does not mean runtime splice is allowed. PASS does not mean TensorCore is used.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4I clean attribution decision ledger

- Add clean attribution decision ledger gate
- Require R4H B5_CLEAN_RESIDUAL_LOW as entry authority
- Seal R4E SETUP_AND_KERNEL_MIXED_LOSS rejection
- Record R4F/R4G poll-map contamination lineage
- Reconcile R4E rejection with C3 STOP_PERF_LOSS
- Emit route policy recommendation without promotion reopen
- Route to G211C3R4J measurement hygiene closeout
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
