# ASH_TEXT_QWAVE_PATCH_V4

## What changed
- Expanded `BurnToRawWgpuBridge` so each bridged lease carries an `ActiveTensorRawHandle` seam.
- Added `AtlasTextDensityUniform` and threaded it into `HeadwiseAtlasRuntimeSpec` and `PreparedAtlasInputs`.
- Injected the text-density uniform directly into `headwise_atlas_attention.wgsl` as bind group binding 1.
- `NativeWgpuModel` now forwards configured text-density state into atlas dispatch and uses the same state for repetition control.

## SSOT
- Raw handle seam lives in `burn_webgpu_backend::raw_bridge`.
- Atlas-side density injection lives in `burn_webgpu_backend::headwise_atlas`.
- Native routing lives in `model_core::NativeWgpuModel`.

## Important truth
- Burn public API still does not expose stable raw `wgpu::Buffer` handles, so the new active-tensor seam is currently **metadata-only unless an internal borrow accessor is added later**.
- The atlas shader uniform injection is real and directly wired into the compute bind group.
- This patch does not claim the vec4/f16 packed shader is already selected automatically for Burn tensors; it injects density control into the existing atlas compute path first.
