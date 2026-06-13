# Commit 16Y remaining bake report

Baked commits, in requested order:

1. **16Y-5 — Atlas Runtime Stability / Cache Lifetime Seal**
   - Vocab atlas remains attached to `NativeWgpuModel` instance.
   - Added cache/lifetime telemetry wording: `[native-vocab-atlas-cache] action=build ...`.
   - Atlas projection does not rebuild tiles inside `project_last_hidden_to_logits_vocab_atlas`.

2. **16Y-P — Projection Telemetry / Artifact Seal**
   - Extended `NativeVocabAllocationProbe` with embedding full bytes, row-gather fields, atlas cache action, sampling mode, tile/global top-k fields.
   - Added artifact fields with snake_case names.
   - Added response fields with camelCase names.

3. **16Y-S — GPU Atlas Sampling / Top-K Merge Seal**
   - Added tile top-k candidate helpers and global top-k merge helper.
   - Atlas projection now computes tile argmax and global top-k telemetry from per-tile logits.
   - Downstream sampling compatibility is preserved by reconstructing the final logits row; this is not yet a pure GPU-side heap implementation.

4. **16Y-4 — Embedding Row Gather Staging**
   - Added loader option to skip full embedding upload.
   - Added `model.embed_tokens.weight.placeholder_row_gather` placeholder for row-gather mode.
   - Added NativeWgpuModel row-gather embedding path using prompt/input token ids and CPU checkpoint rows.
   - `embed_tokens_for_decode`, `forward_logits_for_generation`, and `forward_hidden_ids` route through row-gather when enabled.

## Important build note

Cargo is not available in the bake environment, so this ZIP is statically patched only. Local `cargo build` is the final SSOT.

## Known limitation

16Y-S currently keeps compatibility with the existing full-logits downstream sampling path by reconstructing a `[1, vocab]` logits row after tiled projection. It adds tile top-k/global top-k telemetry and merge helpers, but not yet a pure GPU-only candidate heap.
