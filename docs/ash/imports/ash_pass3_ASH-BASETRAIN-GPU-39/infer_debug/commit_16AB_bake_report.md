# Commit 16AB — Headwise Atlas Raw Bridge Disable Gate Seal

## SSOT

The failing stack is no longer vocab allocation, timestamp query, or tensorcube strict/permissive mode.
The direct failing path is:

```text
HeadwiseAtlasDispatcher::prepare_native_qkv
HeadwiseAtlasDispatcher::dispatch_native_qkv_to_cpu_f32
RawWgpuBufferLease::as_binding_resource
burn_cubecl::kernel::contiguous::into_contiguous_aligned
Using `u64` values requires SHADER_INT64
```

## Implemented

### Request/payload propagation

Added policy fields:

```rust
disable_native_headwise_atlas: bool
disable_native_raw_bridge: bool
disable_native_qkv_bridge: bool
```

Propagated through:

```text
orchestrator_local/src/infer_entry.rs
runtime/src/infer.rs
runtime/src/infer/request_resolution.rs
model_core/src/native_wgpu.rs
```

Camel/snake payload support:

```json
{
  "disableNativeHeadwiseAtlas": true,
  "disableNativeRawBridge": true,
  "disableNativeQkvBridge": true
}
```

```json
{
  "disable_native_headwise_atlas": true,
  "disable_native_raw_bridge": true,
  "disable_native_qkv_bridge": true
}
```

### NativeWgpuModel gates

Added model-level policy storage and gates:

- `atlas_dispatcher` creation is skipped when headwise atlas or qkv bridge is disabled.
- `same_device_raw_bridge()` returns `None` when raw bridge is disabled.
- `try_bridge_last_logits_raw_outcome()` returns `None` before raw bridge use when any 16AB disable flag is active.
- `try_grouped_query_attention_via_atlas()` returns `Ok(None)` before `HeadwiseAtlasDispatcher` use when headwise atlas/qkv bridge is disabled.

## Expected logs

```text
[16AB][policy] disable_headwise_atlas=true disable_raw_bridge=true disable_qkv_bridge=true
[16AB][headwise-atlas] disabled_by_policy=true stage=init
[16AB][raw-bridge] skipped reason=disabled_by_policy label=...
[16AB][headwise-atlas] skipped reason=disabled_by_policy stage=try_grouped_query_attention_via_atlas
```

## Should disappear

```text
HeadwiseAtlasDispatcher::prepare_native_qkv
HeadwiseAtlasDispatcher::dispatch_native_qkv_to_cpu_f32
RawWgpuBufferLease::as_binding_resource
burn_cubecl::kernel::contiguous::into_contiguous_aligned
Using `u64` values requires SHADER_INT64
```

## Included probe

```text
infer_debug/probe_16AB_disable_headwise_raw_bridge_A.jsonl
```

## Validation status

Static patch only. Cargo is not available in this bake container, so local `cargo build -p native_host --bin native_host --release` remains the final SSOT.
