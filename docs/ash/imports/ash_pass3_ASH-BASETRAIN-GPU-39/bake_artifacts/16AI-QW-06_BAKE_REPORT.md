# 16AI-QW-06 Bake Report

## Patch

16AI-QW-06 — Sentence QWave Transition Graph / Eojeol-to-Eojeol Flow Seal

## Base

ash_pass3_16AI-QW-05_morph_role_pulse_overlay_baked.zip

## Added / Modified

- `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs`
- `crates/tokenizer_core/tests/hangul_qwave_sentence_graph.rs`
- `acceptance_reports/16AI-QW-06_sentence_qwave_transition_graph.md`
- `acceptance_reports/16AI-QW-06_static_validation_result.md`
- `bake_artifacts/16AI-QW-06_BAKE_REPORT.md`
- `crates/tokenizer_core/src/lib.rs`

## Summary

This bake adds a deterministic Text-QWave sentence graph layer that consumes QW-04 eojeol chains and QW-05 morph pulse overlays. It produces `QWaveSentenceTransitionGraph`, `QWaveSentenceEojeolEdge`, `QWaveSentencePulseCurve`, and `QWaveSentenceGraphReceipt` while preserving token/vocab/backend immutability.

## Guard Summary

- QW-04 and QW-05 receipts are required.
- Eojeol order must be preserved.
- Adjacent eojeol edges are generated without reordering.
- Overlay adjustment is consumed without mutating original chains.
- Tokenizer DP cost mutation is forbidden.
- SFT feature export is forbidden.
- LoRA routing hint creation is forbidden.
- Token id mutation, vocab augmentation, embedding resize, and backend QWave switch are forbidden.

## Runtime Status

Native Rust tests were not executed in this container because `cargo`/`rustc` are unavailable. Static validation was performed and recorded separately.
