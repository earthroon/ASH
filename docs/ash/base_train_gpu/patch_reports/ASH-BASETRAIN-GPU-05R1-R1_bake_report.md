# ASH-BASETRAIN-GPU-05R1-R1 Bake Report

This overlay closes the local compile error where the 05R1 bin imports a module that the `base_train` crate root does not export.

Use `ASH_BASETRAIN_GPU_05R1_R1_OVERLAY_APPLY.ps1`, then `ASH_BASETRAIN_GPU_05R1_R1_VERIFY.ps1`, then rebuild the 05R1 bin.
