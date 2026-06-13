# LORA_DUMP_BOOTSTRAP_E0382_FIX

## SSOT
- Error source: `crates/burn_webgpu_backend/src/existing_device_bootstrap.rs`
- Rust error: `E0382 borrow of moved value: adapter`
- Failing pattern: `adapter` was moved into `WgpuSetup`, then borrowed again through `adapter.get_info().backend`.

## Applied changes
1. Captured `let backend = adapter.get_info().backend;` before moving `adapter` into `WgpuSetup`.
2. Replaced `let mut registry_registered = false;` followed by immediate overwrite with cfg-split initialization:
   - `burn-raw-access-local`: register handles and initialize to `true`
   - non-feature build: initialize immutable `false`

## Verification
- Static source inspection completed.
- Local `cargo check` could not be executed in this container because `cargo` is not installed here.

## Expected result
- The reported `E0382` compile failure should be removed.
- The `registry_registered` unused assignment warning in `burn_webgpu_backend` should also be removed.
- Vendor fork warnings in `burn-fusion-local` are not fatal and were not changed in this patch.
