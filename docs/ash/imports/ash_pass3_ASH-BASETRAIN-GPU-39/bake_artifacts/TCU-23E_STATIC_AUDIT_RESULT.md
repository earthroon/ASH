# TCU-23E Static Audit Result

Status: `PASS_STATIC_TCU_23E_WITH_NATIVE_TESTS_NOT_RUN`

## Static checks

- TCU-23E timing probe module exists.
- TCU-23E burn_webgpu_backend tests exist.
- TCU-23E orchestrator report and audit bin exist.
- TCU-23E runtime JSON outputs exist.
- `benchmark_mode_enabled = true` appears only inside benchmark guard context.
- `benchmark_result_is_advisory_only = true` is present.
- `fastest_kernel_selection_allowed = false` is present.
- `production_dispatch_allowed = false` is present.
- `sft_pass1_replacement_allowed = false` is present.
- `runtime_inference_replacement_allowed = false` is present.
- `backend_policy_connection_allowed = false` is present.
- `subgroup_fast_path_enabled = false` is present.
- `creates_contiguous_16x16_tile = false` is present.
- Readback-free boundary is represented by `readback_enabled = false` and `output_validation_enabled = false`.

## Not run

Native Rust build/test was not run because `cargo` / `rustc` are unavailable in this container.
