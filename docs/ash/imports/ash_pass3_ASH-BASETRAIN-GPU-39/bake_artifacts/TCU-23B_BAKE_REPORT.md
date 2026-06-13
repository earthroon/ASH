# TCU-23B Bake Report

## Commit

`TCU-23B — TensorCube 8x8 MicroTile WGSL Parity Runner / CPU Reference Comparison`

## Input SSOT

`ash_pass3_TCU-23A_tensorcube_8x8_atlas_microtile_kernel_consolidation_baked.zip`

## Output ZIP

`ash_pass3_TCU-23B_tensorcube_8x8_microtile_wgsl_parity_runner_baked.zip`

## Summary

TCU-23B adds a parity-runner layer over the TCU-23A 8x8 atlas microtile layout. The new layer generates deterministic 8x8 fixtures, packs/unpacks them through the Vec4F32 atlas layout, computes CPU scalar reference output, and records WGSL vec4/workgroup runner states separately from parity failures.

## Safety Seals

```text
production_dispatch_allowed = false
sft_pass1_replacement_allowed = false
runtime_inference_replacement_allowed = false
subgroup_fast_path_enabled = false
creates_contiguous_16x16_tile = false
```

## Result

`PASS_STATIC_TCU_23B_WITH_NATIVE_TESTS_NOT_RUN`

The bake completed file generation and static audit. Native Rust/GPU execution was not performed in this environment.
