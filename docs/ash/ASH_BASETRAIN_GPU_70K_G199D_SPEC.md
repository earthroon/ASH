# ASH-BASETRAIN-GPU-70K-G199D

PatchId: `ASH-BASETRAIN-GPU-70K-G199D`

Title: BaseTrain Optimizer Shadow Step Boundary

SourcePatchId: `ASH-BASETRAIN-GPU-70K-G198D`

Summary:

G199D adds the next BaseTrain boundary after G198D. The current default path is contract-only unless an explicit runtime envelope is provided to the Rust binary. The detailed spec is included in the baked archive under `specs/ASH_BASETRAIN_GPU_70K_G199D_SPEC.md`.

Binary:

`ash_basetrain_gpu_70k_g199d_optimizer_shadow_step`

Generated JSON outputs are written locally by the Rust binary through `--out-dir`.

Next: `ASH-BASETRAIN-GPU-70K-G200D`
