# ASH-BASETRAIN-GPU-24 Bake Report

Baked files:
- crates/base_train/src/ash_basetrain_gpu_24_gpu_local_loss_candidate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_24_gpu_local_loss_candidate.rs
- crates/base_train/src/shaders/ash_basetrain_gpu_24_local_loss_candidate.wgsl
- acceptance_reports/ASH-BASETRAIN-GPU-24.md
- patch_reports/ASH-BASETRAIN-GPU-24_bake_report.md
- ASH_BASETRAIN_GPU_HANDOFF_AFTER_24.md
- ASH_BASETRAIN_GPU_24_OPERATOR_COMMANDS.ps1
- ASH_BASETRAIN_GPU_24_STATIC_CHECKS.txt
- ASH_BASETRAIN_GPU_24_LOCAL_VALIDATION.txt

Contract:
- JSON atlas-map tiling retained.
- Object-level json! macro is not introduced in patch source.
- WGPU local loss candidate dispatch is introduced.
- Backward/optimizer/mutation remain sealed.

Validation note:
Cargo is unavailable in this sandbox, so local build/runtime PASS is judgment-impossible here.
