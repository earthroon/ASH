# ASH-BASETRAIN-GPU-70K-G84-R2-A

Patch card for G84-R2-A direct selected group assembly commit.

Source: ASH-BASETRAIN-GPU-70K-G83-R2
Target: PASS_ASH_BASETRAIN_GPU_70K_G84_R2_A_DIRECT_SELECTED_GROUP_ASSEMBLY_COMMIT

This source/spec bake adds the Rust module and binary for the G84-R2-A local run. Runtime receipt JSON is not included in the ZIP. The Rust binary is expected to create the ten G84-R2-A receipts under the selected out-dir during cargo run.

Archive policy: no Python files, no PowerShell files, no sha256 sidecars, no artifacts directory, no target directory, and no prebaked G84 runtime receipt JSON.
