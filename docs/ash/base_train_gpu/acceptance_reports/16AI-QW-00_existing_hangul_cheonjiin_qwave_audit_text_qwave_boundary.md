# 16AI-QW-00 — Existing Hangul/Cheonjiin/QWave Audit / Text-QWave Boundary Seal

## Scope

This seal audits the existing Hangul tensor, Cheonjiin feature row, morph tensor, structure tensor, tokenizer probe chain, and existing QWave backend/audio/asr modules. It defines the boundary for future Text-QWave modules without implementing QWave cells, pulse vectors, syllable transitions, eojeol chains, sentence graphs, token id mutation, vocab augmentation, embedding resize, or backend QWave switching.

## Existing Boundaries

- `crates/tokenizer_core/src/hangul_tensor.rs`
- `crates/tokenizer_core/src/morph_tensor.rs`
- `crates/tokenizer_core/src/structure_tensor.rs`
- `crates/model_core/src/bin/af16ai6b_cheonjiin_structural_probe.rs`
- `crates/model_core/src/bin/af16ai6c_surface_candidate_probe.rs`
- `crates/model_core/src/bin/af16ai6d_vocab_lattice_probe.rs`
- `crates/model_core/src/bin/af16ai6e_dp_token_path_probe.rs`
- `crates/burn_webgpu_backend/src/qwave_*.rs`
- `crates/audio_kernel/src/qwave_pipeline.rs`
- `crates/asr_sidecar/src/qwave.rs`

## Reserved Text-QWave Terms

- `QWaveSyllableCell` reserved for `16AI-QW-01`
- `QWavePulseVector` reserved for `16AI-QW-02`
- `QWaveSyllableTransition` reserved for `16AI-QW-03`
- `QWaveEojeolChain` reserved for `16AI-QW-04`
- `QWaveSentenceTransitionGraph` reserved for `16AI-QW-06`

## Guards

- HangulFeatureRow must exist.
- Cheon/Ji/In fields must exist.
- Morph tensor must exist.
- Structure tensor must exist.
- backend QWave must remain separated from Text-QWave.
- audio/asr QWave must remain separated from Text-QWave.
- Pulse Vector is reserved only.
- QWaveSyllableCell implementation is forbidden in QW-00.
- token id mutation forbidden.
- vocab augmentation forbidden.
- embedding resize forbidden.
- backend QWave switch forbidden.
- runtime tokenizer policy mutation forbidden.

## Acceptance Tests

- existing Hangul tensor boundary detected
- Cheonjiin fields detected
- morph and structure tensors detected
- QWave backend separated from Text-QWave
- Pulse Vector term reserved only
- token id mutation rejected
- vocab augmentation rejected
- embedding resize rejected
- backend QWave switch rejected
- deterministic receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_QW01 until `QWaveSyllableCell` is implemented in the reserved Text-QWave path.
