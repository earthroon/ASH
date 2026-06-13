# SSOT CubeTensor runtime seam implementation

Base: `ash_pass3 (12).zip`

Implemented:
- `vendor_fork_scaffold/burn-fusion-local/src/raw_access.rs`
  - real `TensorPrimitive::Float(...)` handling
  - derives `(primitive.id, primitive.stream)` from the fusion tensor
  - resolves `CubeTensor<WgpuRuntime>` through the existing resolved primitive registry
- `vendor_fork_scaffold/burn-fusion-local/src/resolved_primitive_override.rs`
  - reduced private-interface warning by making `Entry` and snapshot entries `pub(crate)`

Intentionally unchanged:
- `vendor_fork_scaffold/burn-wgpu-local/src/raw_access.rs` remains fail-closed because the local crate still cannot safely reinterpret the external buffer type without finishing the wgpu version-alignment work.

Meaning:
- Native trace submit path is alive.
- Fusion primitive -> CubeTensor seam is no longer a pure stub.
- Zero-copy raw borrow still depends on the remaining buffer-type alignment work in `burn-wgpu-local`.
