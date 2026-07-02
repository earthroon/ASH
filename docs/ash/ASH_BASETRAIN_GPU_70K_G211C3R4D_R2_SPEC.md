# ASH-BASETRAIN-GPU-70K-G211C3R4D-R2

## Reuse Recovery Delta Sign Audit / Setup Dominance Verdict Consistency Seal / No Timing Rerun No Artifact Rewrite

Seal: Verdict Consistency Audit Only / No Timing Rerun / No R4D Artifact Rewrite / No Runtime Splice / No Promotion Reopen.

## SSOT

`70K-G211C3R4D-R2` consumes existing `G211C3R4D` setup overhead isolation receipts as its input authority. It does not rerun GPU timing, does not issue dispatch, and does not rewrite any `artifacts/g211c3r4d` file.

`70K-G211C3R4D-R2` exists because `G211C3R4D` produced:

```text
setup_split_verdict=SETUP_OVERHEAD_DOMINANT
setup_overhead_class=SETUP_OVERHEAD_DOMINANT
reuse_recovery_delta=-1.259650
```

The audit checks whether the negative `reuse_recovery_delta` can coexist with the dominant setup verdict, whether the sign convention is aligned with the R4D spec, and whether R4E may proceed with a note or must block until another repair gate.

`70K-G211C3R4D-R2` must not mutate the TensorCube runtime route, must not change `tensorcube_runtime_splice`, must not generate a G211C4 entry packet, must not replace decode output, must not write model weights or checkpoints, must not execute optimizer/training steps, must not rewrite WGSL, must not change tile/workgroup layout, must not rerun promotion, and must not claim TensorCore usage, speedup, production readiness, or production acceleration.

## Predecessor

```text
ASH-BASETRAIN-GPU-70K-G211C3R4D
Pipeline And Bind Group Reuse Split /
Setup Overhead Isolation Probe /
No Runtime Splice No Promotion Reopen
```

Required predecessor evidence:

```text
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_OVERHEAD_ISOLATION_PROBE.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_PIPELINE_BIND_GROUP_REUSE_MATRIX.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_SETUP_COMPONENT_SPLIT.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_REUSE_RECOVERY_SUMMARY.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_TIMESTAMP_STABILITY_AUDIT.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_FORBIDDEN_MUTATION_SEAL.json
artifacts/g211c3r4d/ASH_BASETRAIN_GPU_70K_G211C3R4D_NEXT_ENTRY_PACKET_G211C3R4E.json
artifacts/g211c3r4d/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D.txt
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
```

## Purpose

G211C3R4D-R2 proves only this:

```text
R4D PASS marker and receipts were found
R4D setup verdict/class/reuse delta were read from receipts
reuse_recovery_delta sign convention was audited
setup dominance consistency was classified
R4E entry policy was selected
no timing rerun was executed
no GPU dispatch was executed
no R4D artifact was rewritten
runtime splice and promotion remained closed
G211C4 entry remained absent
```

G211C3R4D-R2 does not prove that R4D timing is correct. It only seals the interpretation boundary before R4E.

## Reuse Recovery Delta Definition

Canonical definition:

```text
reuse_recovery_delta = hot_dispatch_speedup_ratio - cold_all_speedup_ratio
```

Interpretation:

```text
reuse_recovery_delta > 0: candidate improves relative to baseline after setup reuse
reuse_recovery_delta = 0: setup reuse does not change relative candidate position
reuse_recovery_delta < 0: candidate becomes worse relative to baseline after setup reuse
```

If the R4D artifacts indicate the reversed convention, R4D-R2 must record:

```text
reuse_delta_sign_policy=IMPLEMENTATION_REVERSED_FROM_SPEC
canonical_reuse_recovery_delta=<derived hot-cold value>
reported_reuse_recovery_delta=<R4D value>
```

No silent correction is allowed. R4D-R2 may write a derived canonical value into its own audit artifact, but it must not rewrite R4D receipts.

## Consistency Classes

R4D-R2 must select exactly one consistency class:

```text
CONSISTENT_SETUP_DOMINANCE_BY_DOMINANCE_RATIO
CONSISTENT_SETUP_DOMINANCE_WITH_REVERSED_DELTA_SIGN
INCONSISTENT_DOMINANT_VERDICT_NEGATIVE_RECOVERY
INCOMPLETE_EVIDENCE_DOMINANT_NOT_DISPROVEN
INCOMPLETE_EVIDENCE_DOMINANT_NOT_VERIFIABLE
BLOCKED_BY_PARITY_OR_TIMESTAMP
BLOCKED_BY_FORBIDDEN_MUTATION
INCONCLUSIVE
```

`CONSISTENT_SETUP_DOMINANCE_BY_DOMINANCE_RATIO` is allowed when `setup_dominance_ratio >= 0.50`, timestamp is stable, and parity passes. In this case a negative recovery delta may coexist with the setup dominant verdict only because the verdict is driven by setup dominance ratio rather than recovery direction.

`CONSISTENT_SETUP_DOMINANCE_WITH_REVERSED_DELTA_SIGN` is allowed when reported delta is negative, canonical delta is positive, the implementation sign is reversed from the spec, and setup dominance ratio is sufficient.

`INCOMPLETE_EVIDENCE_DOMINANT_NOT_DISPROVEN` is allowed when negative recovery raises a warning but component evidence exists and dominance cannot be disproven from available receipts.

`INCOMPLETE_EVIDENCE_DOMINANT_NOT_VERIFIABLE` blocks R4E because the dominant verdict cannot be independently checked.

## Audit Verdict Values

R4D-R2 must produce exactly one audit verdict:

```text
R4D_R2_CONSISTENCY_CONFIRMED
R4D_R2_CONSISTENCY_CONFIRMED_WITH_SIGN_NOTE
R4D_R2_CONSISTENCY_WARNING_R4E_ALLOWED
R4D_R2_CONSISTENCY_WARNING_R4E_BLOCKED
R4D_R2_INCOMPLETE_EVIDENCE_R4E_ALLOWED
R4D_R2_INCOMPLETE_EVIDENCE_R4E_BLOCKED
R4D_R2_BLOCKED_BY_FORBIDDEN_MUTATION
R4D_R2_BLOCKED_BY_INPUT_INCOMPLETE
INCONCLUSIVE
```

## R4E Entry Policy

R4D-R2 must select exactly one R4E policy:

```text
ALLOW_R4E_CONFIRMED
ALLOW_R4E_WITH_SIGN_NOTE
ALLOW_R4E_WITH_CONSISTENCY_WARNING
ALLOW_R4E_WITH_INCOMPLETE_EVIDENCE_NOTE
BLOCK_R4E_UNTIL_R4D_R3
BLOCK_R4E_FOR_FORBIDDEN_MUTATION
BLOCK_R4E_FOR_INPUT_INCOMPLETE
```

When R4E is allowed with a note, R4E must treat R4D setup dominance as context rather than sole attribution authority. R4E must independently inspect kernel, tile, padding, and utilization evidence.

## Local Rust Binary

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g211c3r4d_r2_reuse_delta_sign_audit.rs
```

Suggested command from ASH root:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g211c3r4d_r2_reuse_delta_sign_audit
```

Alternative command from `crates/base_train`:

```powershell
cargo run --bin ash_basetrain_gpu_70k_g211c3r4d_r2_reuse_delta_sign_audit
```

Optional arguments:

```text
--g211c3r4c-dir artifacts/g211c3r4c
--g211c3r4d-dir artifacts/g211c3r4d
--out-dir artifacts/g211c3r4d_r2
--r4e-entry-policy auto
```

Allowed `--r4e-entry-policy` values:

```text
auto
allow-with-warning
block-on-inconsistency
```

Expected stdout marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_REUSE_DELTA_SIGN_AUDIT
```

Expected stdout fields:

```text
patch_id=ASH-BASETRAIN-GPU-70K-G211C3R4D-R2
timing_rerun_executed=false
artifact_rewrite_executed=false
r4d_setup_split_verdict=SETUP_OVERHEAD_DOMINANT
r4d_setup_overhead_class=SETUP_OVERHEAD_DOMINANT
reported_reuse_recovery_delta=<float>
reuse_delta_sign_policy=<...>
consistency_class=<...>
audit_verdict=<...>
r4e_entry_policy=<...>
runtime_splice_allowed=false
promotion_allowed=false
g211c4_entry_generated=false
next_gate=ASH-BASETRAIN-GPU-70K-G211C3R4E
```

## Required Outputs

The baked package must not contain prebaked `artifacts/g211c3r4d_r2` outputs. The local Rust gate generates them when the operator runs the binary.

```text
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_REUSE_DELTA_SIGN_AUDIT.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_SETUP_DOMINANCE_CONSISTENCY_SEAL.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_R4E_ENTRY_POLICY.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_FORBIDDEN_REWRITE_SEAL.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_NEXT_ENTRY_PACKET_G211C3R4E.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_LOCAL_BAKE_VALIDATION.json
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_BAKE_MANIFEST.json
artifacts/g211c3r4d_r2/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D_R2.txt
```

Forbidden output:

```text
artifacts/g211c3r4d_r2/ASH_BASETRAIN_GPU_70K_G211C3R4D_R2_NEXT_ENTRY_PACKET_G211C4.json
```

Forbidden rewrite targets:

```text
artifacts/g211c3r4d/*.json
artifacts/g211c3r4d/PASS_ASH_BASETRAIN_GPU_70K_G211C3R4D.txt
```

## PASS Criteria

```text
PASS-01 R4D PASS marker found
PASS-02 R4D main receipt found
PASS-03 R4D reuse recovery summary found or equivalent fields found
PASS-04 setup_split_verdict found
PASS-05 setup_overhead_class found
PASS-06 reuse_recovery_delta found
PASS-07 timing_rerun_executed=false
PASS-08 gpu_dispatch_executed=false
PASS-09 artifact_rewrite_executed=false
PASS-10 R4D artifacts are not modified
PASS-11 R4D verdict is not overwritten
PASS-12 reuse delta sign policy selected exactly once
PASS-13 consistency class selected exactly once
PASS-14 audit verdict selected exactly once
PASS-15 R4E entry policy selected exactly once
PASS-16 forbidden rewrite seal written
PASS-17 setup dominance consistency seal written
PASS-18 R4E entry policy written
PASS-19 G211C3R4E entry packet generated if allowed by policy
PASS-20 G211C4 entry packet not generated
PASS-21 runtime_splice_allowed=false
PASS-22 promotion_allowed=false
PASS-23 PASS marker printed
```

## PASS Meaning

PASS means R4D-R2 audited the sign and consistency of the R4D setup dominance verdict without rerunning timing and without rewriting R4D artifacts.

PASS does not mean R4D timing is correct. PASS does not mean setup overhead dominance is fully proven unless the consistency class explicitly confirms it. PASS does not mean TensorCube is faster. PASS does not mean promotion is reopened. PASS does not mean G211C4 is allowed.

## Recommended Commit Message

```text
ASH-BASETRAIN-GPU-70K-G211C3R4D-R2 reuse delta sign audit

- Add R4D-R2 verdict consistency audit gate
- Read existing R4D setup overhead receipts without timing rerun
- Audit reuse recovery delta sign convention
- Check setup dominance verdict consistency against available dominance evidence
- Emit R4E entry policy with warning or block semantics
- Preserve existing R4D artifacts without rewrite
- Preserve no runtime splice, no G211C4 entry, no production route, no promotion
```
