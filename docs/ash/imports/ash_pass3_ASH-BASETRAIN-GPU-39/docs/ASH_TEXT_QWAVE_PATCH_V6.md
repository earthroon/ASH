# Ash Text QWave Patch v6

## What changed
- Added a more aggressive vendor seam for `burn-fusion-local` based on `(primitive.id, primitive.stream)` handle-map lookup assumptions.
- Promoted the raw bridge metadata so `ActiveTensorRawHandle` now carries `vendor_access_path`, `primitive_id`, and `stream_id`.
- Extended atlas seam summaries to report handle-map hit/miss counts and per-tensor route tags.

## Intent
This patch is the first version that explicitly models the fusion unwrap step as:

`Fusion primitive -> handle-map lookup keyed by primitive id + stream -> CubeTensor<WgpuRuntime> -> WgpuResource`

The local fork implementation is still fail-closed. Until the fork exposes the actual lookup, the caller falls back to metadata-only host upload instead of pretending raw borrow works.

## Merge notes
- `vendor_fork_scaffold/burn-fusion-local/src/raw_access.rs` is the main 6th-patch seam.
- `crates/burn_webgpu_backend/src/raw_bridge.rs` now consumes the richer borrow metadata.
- `crates/burn_webgpu_backend/src/headwise_atlas.rs` surfaces the seam route back out through atlas summaries.
