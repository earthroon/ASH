# Commit 16Y remaining bake report

Included commits:

1. Commit 16Y-5 — Atlas Runtime Stability / Cache Lifetime Seal
   - Vocab atlas is attached to `NativeWgpuModel` instance.
   - Added cache-action telemetry/log wording: build / model-instance lifetime.
   - Atlas is not rebuilt inside `project_last_hidden_to_logits_vocab_atlas` or per tile projection.

2. Commit 16Y-P — Projection Telemetry / Artifact Seal
   - Extended `NativeVocabAllocationProbe` with embedding/full-upload/cache/sampling fields.
   - Added artifact fields for embedding modes, row gather bytes, atlas cache action, sampling mode, tile/global top-k.
   - Added response fields with camelCase counterparts.

3. Commit 16Y-S — GPU Atlas Sampling / Top-K Merge Seal
   - Added tile top-k candidate helpers and global top-k merge helper.
   - Atlas projection now computes tile argmax plus global top-k telemetry from tile logits.
   - Downstream compatibility still reconstructs the full logits row so existing sampling path remains intact.
   - This is a compatibility implementation, not yet a pure GPU-side candidate heap implementation.

4. Commit 16Y-4 — Embedding Row Gather Staging
   - Added loader option to skip full embedding upload.
   - Added `model.embed_tokens.weight.placeholder_row_gather` placeholder for row-gather mode.
   - Added NativeWgpuModel row-gather embedding path using prompt/input token ids and CPU checkpoint rows.
   - `embed_tokens_for_decode`, `forward_logits_for_generation`, and `forward_hidden_ids` route through row-gather when enabled.

Build note:
- Cargo is not available in this environment, so this ZIP is statically patched only.
- Local cargo build remains the SSOT.
