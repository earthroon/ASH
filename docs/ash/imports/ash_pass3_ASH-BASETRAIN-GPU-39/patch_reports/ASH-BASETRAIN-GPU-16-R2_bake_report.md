# ASH-BASETRAIN-GPU-16-R2 Bake Report

Patch: ASH-BASETRAIN-GPU-16-R2
Title: Verdict String Rebind / 2048 Dispatch PASS Label Alignment No Runtime Change Seal

## Changed files

- `crates/base_train/src/ash_basetrain_gpu_16_chunk_window_logits_expansion_dispatch_smoke.rs`
- `acceptance_reports/ASH-BASETRAIN-GPU-16-R2.md`
- `patch_reports/ASH-BASETRAIN-GPU-16-R2_bake_report.md`
- `ASH_BASETRAIN_GPU_16_R2_STATIC_CHECKS.txt`
- `ASH_BASETRAIN_GPU_16_R2_LOCAL_VALIDATION.txt`
- `ASH_BASETRAIN_GPU_HANDOFF_AFTER_16_R2.md`

## Rebound label

Old:

`PASS_ASH_BASETRAIN_GPU_16_MINIMAL_MULTI_BUFFER_FORWARD_DISPATCH_SMOKE_EMBED_QPROJ_LMHEAD_READINESS_TO_FIXED_TOKEN_DISPATCH_STATE_NO_BACKWARD_NO_OPTIMIZER`

New:

`PASS_ASH_BASETRAIN_GPU_16_CHUNK_WINDOW_LOGITS_EXPANSION_DISPATCH_SMOKE_WINDOW_2048_CANDIDATE_TO_DISPATCH_STATE_NO_BACKWARD_NO_OPTIMIZER`

## Runtime behavior

No runtime behavior change intended. This bake only rebinds the PASS label and related source doc title.

## Local validation

Container cargo is unavailable here, so local cargo build/run remains operator-side SSOT.
