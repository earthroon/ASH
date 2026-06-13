# QW-52A-R1
## Existing Cheonjiin Jaso Stroke Tensor Facade / No Math Rewrite Seal

This patch lifts no new math. It binds existing sources into a reusable Rust facade:

- `tokenizer_core::hangul_tensor::HangulFeatureRow`
- `tokenizer_core::hangul_qwave_cell`
- `tokenizer_core::hangul_qwave_pulse`
- `tokenizer_core::hangul_qwave_transition`
- `model_core::cheonjiin_structural_probe`

## Rust ownership

Rust owns facade construction, trace attachment, receipt evidence, and validation. Python remains injector-only.

## Non-goals

- No new Hangul decomposition
- No new Cheonjiin LUT
- No new QWave phase math
- No new stroke rule table
- No WebGPU shader
- No logits/sampler/token mutation
- No hidden-state fusion
- No adapter projection
