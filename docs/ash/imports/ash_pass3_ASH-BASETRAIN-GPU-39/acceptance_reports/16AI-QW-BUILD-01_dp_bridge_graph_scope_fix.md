# 16AI-QW-BUILD-01 — Hangul QWave DP Bridge Graph Scope Fix / Build Unblock Seal

## SSOT
- Base ZIP: `ash_pass3_16AI-QW-34_qwave_canary_telemetry_monitor_baked.zip`
- Patch target: `crates/tokenizer_core/src/hangul_qwave_dp_bridge.rs`
- Warning cleanup target: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs`

## Fixed
- Repaired undefined `graph` reference in QWave DP bridge continuity reward calculation.
- The calculation now uses the existing `sentence_graph` parameter, which is already the function-local SSOT for `QWaveSentenceTransitionGraph`.

## Guard
- QWave continuity reward was preserved.
- No silent fallback to zero.
- No deletion of `mean_binding`.
- No tokenizer/token id/vocab/embedding mutation.

## Validation
- Static validation: PASS
- Native cargo test: NOT_RUN in this container because `cargo`/`rustc` are unavailable.

## Recommended local verification
```bash
cargo test -p tokenizer_core hangul_qwave
cargo test -p tokenizer_core hangul_qwave_dp_bridge
cargo test -p lora_train qwave
```
