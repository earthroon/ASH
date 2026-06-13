# ASH Text-QWave Patch V5

## Stage 7D: borrowed raw-handle seam promotion

This overlay extends the stage7c/stage7d atlas path so the native WebGPU route can attempt a true borrowed buffer bind instead of always collapsing to metadata-only host uploads.

### What changed

- `crates/burn_webgpu_backend/src/raw_bridge.rs`
  - adds `bridge_native_tensor_f32(...)`
  - adds `buffer_offset` / `buffer_size` to the lease and active seam metadata
  - adds `RawWgpuBufferLease::as_binding_resource()` so bind groups can use offset-aware bindings
  - wires `try_borrow_burn_raw_wgpu_buffer(...)` behind the feature flag `burn-raw-access-local`

- `crates/burn_webgpu_backend/src/headwise_atlas.rs`
  - adds `prepare_native_qkv(...)`
  - adds `dispatch_native_qkv_to_cpu_f32(...)`
  - atlas bind group now uses the lease binding view instead of `as_entire_binding()`

- `crates/model_core/src/lib.rs`
  - native atlas path now calls `dispatch_native_qkv_to_cpu_f32(...)`
  - env gate `ASH_EXPERIMENTAL_NATIVE_RAW_BORROW_REQUIRED`

- `vendor_fork_scaffold/*`
  - local seam crates for the two remaining access layers:
    - `burn-wgpu-local`: actual WgpuResource accessor from `CubeTensor.client + handle`
    - `burn-fusion-local`: fusion unwrap seam for turning the float primitive into a `CubeTensor<WgpuRuntime>`

### Important truth boundary

This is not full zero-copy completion yet.

What is now real:
- once a `CubeTensor<WgpuRuntime>` is available, the accessor can resolve a `WgpuResource` and therefore a real `{ buffer, offset, size }` binding triple.

What still remains:
- unwrapping the fused Burn float primitive into that `CubeTensor<WgpuRuntime>` still needs a local fork seam in `burn-fusion-local`.

So stage7d upgrades the seam from:
- `metadata-only everywhere`

to:
- `real raw WGPU accessor available after fusion unwrap`

### Activation flow

1. keep feature off for safe merge
2. fill the `burn-fusion-local` unwrap seam against the local fork
3. build `burn_webgpu_backend` with feature `burn-raw-access-local`
4. optionally set `ASH_EXPERIMENTAL_NATIVE_RAW_BORROW_REQUIRED=1`
   - atlas route will hard-fail instead of silently falling back when borrowed handles are unavailable
