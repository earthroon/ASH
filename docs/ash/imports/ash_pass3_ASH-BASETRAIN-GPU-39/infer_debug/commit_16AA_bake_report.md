# Commit 16AA — CubeCL Timestamp Query / Profiler Runtime Seal

## Scope

This bake targets the WGPU device bootstrap path used by `model_core_native_existing_device`.

The prior 16Y path successfully reached:

- `native-vocab-atlas` tile build
- `native-embedding-row-gather`

The next failure was a CubeCL/WGPU QueryProfiler panic:

```text
Device::create_query_set
TIMESTAMP_QUERY required but not enabled
cubecl_wgpu::compute::timings::QueryProfiler::register_profile_device
```

## Patched file

- `crates/burn_webgpu_backend/src/existing_device_bootstrap.rs`

## Changes

- Added timestamp-query feature probe on the selected adapter.
- Requests `wgpu::Features::TIMESTAMP_QUERY` for the native existing-device bootstrap when the adapter supports it.
- Added explicit 16AA telemetry logs:
  - `[16AA][timestamp-query] ...`
  - `[16AA][runtime-options] ...`
- Added environment escape hatch to avoid requesting TIMESTAMP_QUERY:
  - `ASH_DISABLE_TIMESTAMP_QUERY=1`
  - `ASH_NATIVE_DISABLE_TIMESTAMP_QUERY=1`
  - `ASH_DISABLE_NATIVE_TIMESTAMP_QUERY=1`

## Default policy

Default behavior is now:

```text
adapter supports TIMESTAMP_QUERY + env does not disable it
→ request TIMESTAMP_QUERY at device creation
```

This is intentional because the observed CubeCL QueryProfiler path requires the feature to be enabled.

## Expected pass signal

```text
[16AA][timestamp-query] source=model_core_native_existing_device adapter_supported=true requested=true disabled_by_env=false ...
[16AA][runtime-options] source=model_core_native_existing_device runtime_options=default timestamp_query_feature_requested=true
```

Then the old panic should disappear:

```text
Device::create_query_set
TIMESTAMP_QUERY required but not enabled
```

## Known limitation

If the adapter does not support TIMESTAMP_QUERY, this patch will log `adapter_supported=false` and will not request the feature. In that case the remaining fix is a CubeCL QueryProfiler feature-gate/local vendor patch, because environment disables did not stop QueryProfiler in the observed run.

## Build status

Cargo is not available in the bake container, so this is a static code bake. Local `cargo build` is still the SSOT.
