# ASH text qwave patch v3

This overlay connects the text density gate scaffold to `NativeWgpuModel`.

Included:
- `burn_webgpu_backend::TextDensityGateRuntime` with a real compute pipeline, bind group, uniform buffer, and probe dispatch
- `NativeWgpuModel::configure_text_density_gate(...)`
- runtime wiring so `text_qwave_hints` configures the native WebGPU model before generation
- repetition window / penalty routing inside `NativeWgpuModel` using the bound density result

Current scope:
- The bind group is real and dispatches a small probe shader.
- The main Burn inference graph is not yet patched to consume the uniform directly inside attention/matmul kernels.
- Because Burn 0.20 does not expose stable raw wgpu handles for active tensors, this patch keeps the GPU density gate on a side-car compute seam and feeds the selected route back into native generation heuristics.
