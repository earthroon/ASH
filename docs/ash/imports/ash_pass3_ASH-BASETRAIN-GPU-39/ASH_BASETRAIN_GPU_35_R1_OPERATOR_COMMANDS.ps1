cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

# Manifest-bound route. Remove this env var to verify blocked-safe route.
$env:ASH_BASETRAIN_GPU_SELECTED_GROUP_MANIFEST_PATH="D:\1111113232\DUST\1\ash_pass3\target\selected_atlas_group_slot_0_manifest.json"

cargo build -p base_train --bin ash_basetrain_gpu_35_r1_selected_group_manifest_binding --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_35_r1_cargo_build.log"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_35_r1_selected_group_manifest_binding 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_35_r1_selected_group_manifest_binding.log"
