# Commit 16Y-3 — LM Head GPU Atlas Tiling / Argmax Merge Seal

## SSOT

`lm_head.weight [vocab_size, hidden_size]` must not be uploaded as one full GPU tensor when `nativeVocabProjection=gpu_atlas` or when `auto` resolves to `gpu_atlas`.

For the current checkpoint:

```txt
48259 * 2048 * 4 = 395337728 bytes
```

## Included changes

### `crates/model_core/src/reference_checkpoint.rs`

- Added `load_full_checkpoint_into_model_with_lm_head_upload(...)`.
- In atlas mode, `lm_head.weight` full upload is skipped.
- A tiny placeholder `lm_head.weight.placeholder_gpu_atlas` with shape `[1, hidden_size]` is uploaded instead.
- Existing `load_full_checkpoint_into_model(...)` remains as the full-upload compatibility path.

### `crates/model_core/src/native_wgpu.rs`

- Added `NativeVocabAtlas` and `NativeVocabTile`.
- Added `build_native_vocab_atlas(...)`.
- Atlas tiles are built from CPU `full.lm_head` rows:
  - default tile size: caller-provided, expected `1024`
  - tile allocation is checked against `max_single_buffer_bytes`
  - each tile emits `[native-vocab-atlas]` telemetry
- Added `vocab_atlas: Option<NativeVocabAtlas>` to `NativeWgpuModel`.
- Added `from_full_checkpoints_with_vocab_atlas(...)` and `load_toml_with_loras_and_vocab_atlas(...)`.
- `lm_head_vocab_size()` now returns atlas vocab size when atlas is active.
- `project_last_hidden_to_logits(...)` routes through atlas tiles when atlas is active.
- `forward_logits_for_generation(...)` avoids the placeholder lm_head in atlas mode by forwarding hidden states and projecting the last row through vocab atlas tiles.

### `crates/runtime/src/infer.rs`

- Native loader now resolves effective vocab projection before loading the native model.
- If `auto` resolves to `gpu_atlas`, runtime calls `NativeWgpuModel::load_toml_with_loras_and_vocab_atlas(...)`.
- Added 16Y-3 loader telemetry:

```txt
[16Y-3][native-loader] vocab_projection_effective=... use_vocab_atlas=... tile_size=... full_vocab_bytes=... max_single_buffer=...
```

### `crates/orchestrator_local/src/infer_entry.rs`

- Added artifact/response fields:
  - `native_vocab_atlas_tile_count`
  - `native_generated_by_tile_argmax`
  - `nativeVocabAtlasTileCount`
  - `nativeGeneratedByTileArgmax`

## Expected logs

```txt
[16Y-3][native-loader] vocab_projection_effective=gpu_atlas use_vocab_atlas=true tile_size=1024 full_vocab_bytes=395337728 max_single_buffer=268435456
[native-vocab-atlas] tile=0 token_start=0 token_len=1024 hidden=2048 bytes=8388608
...
[native-vocab-atlas] tile=47 token_start=48128 token_len=131 hidden=2048 bytes=1073152
[native-vocab-atlas] built tile_count=48 vocab=48259 hidden=2048 tile_vocab=1024 full_vocab_bytes=395337728
```

## Important limitation

This bake is a conservative atlas integration. It avoids full lm_head upload and routes projection through vocab tiles, but it keeps compatibility with the existing logits pipeline by rebuilding a final last-logits row after tile projection. The helper logs tile-level argmax while preserving downstream penalty/sampling behavior. Full GPU-side top-k merge can be split into a later 16Y-S optimization.

## Validation available in bake environment

No `cargo` binary is available in this container, so compile verification must be done locally.

Static checks performed:

```txt
- native-vocab-atlas symbols present
- lm_head placeholder path present
- runtime loader uses load_toml_with_loras_and_vocab_atlas
- artifact/response telemetry fields present
- modified file brace/paren balance = 0 delta
```

## Local build command

```powershell
cargo build -p base_train --bin checkpoint_smoke_generate --release
cargo build -p base_train --bin checkpoint_text_generate --release
cargo build -p native_host --bin native_host --release
```

## Local test payload

Use the existing 16Y2 payload, or force:

```json
{
  "nativeVocabProjection": "gpu_atlas",
  "nativeVocabTileSize": 1024,
  "nativeAvoidFullVocabGpuUpload": true,
  "nativeMaxSingleGpuBufferBytes": 268435456
}
```
