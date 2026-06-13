# 16AF-G1a Ownership Fix Bake Report

## 확정

16AF-G runner build failed with Rust E0382 because `ReferenceModel::try_enable_native_atlas_ffn_generation_candidate` consumed `self` and returned `Result<Self>`. In the runner, the `Err` branch could skip reassignment, so `model` was considered moved before `greedy_generate`.

## 패치

- `try_enable_native_atlas_ffn_generation_candidate(mut self, ...) -> Result<Self>`
- changed to `try_enable_native_atlas_ffn_generation_candidate(&mut self, ...) -> Result<()>`
- runner match updated from `Ok(enabled) => model = enabled` to `Ok(()) => ...`
- unused `started` warning reduced by renaming to `_started`

## 보존

- `generation_connected_default=false`
- `fallback_cpu_reference=true`
- `attention_native=false`
- `kv_cache_native=false`
- candidate gate remains default false

## 판단불가

Local Rust/WGPU build was not executed in this container.
