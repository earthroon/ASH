# Next patch: vendor fusion alias + raw bridge Arc fix

Applied on top of the latest SSOT base.

## Changes
- `vendor_fork_scaffold/burn-fusion-local/src/raw_access.rs`
  - Rebased `NativeWgpuFusionPrimitive` to `TensorPrimitive<Fusion<CubeBackend<...>>>`
  - Kept the seam fail-closed (`None`) to preserve compile-only bridge behavior.
- `vendor_fork_scaffold/burn-fusion-local/Cargo.toml`
  - Ensured `burn-tensor = "0.20.1"` dependency exists.
- `crates/burn_webgpu_backend/src/raw_bridge.rs`
  - Removed double wrapping (`Arc<Arc<Buffer>>`) by using `borrowed.resource.buffer.clone()` directly.

## Intent
- Match the caller type expected by `burn_webgpu_backend::raw_bridge`.
- Eliminate the `Arc<Arc<Buffer>>` mismatch that appeared after vendor raw-access refactors.
