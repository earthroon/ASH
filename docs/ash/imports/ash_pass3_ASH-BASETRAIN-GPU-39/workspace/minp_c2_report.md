# 16AI-QW-38G-R6A-MINP-C2 Report

## Scope
QWave / ΔK token score source provider seal. This patch adds a token-id aligned static score snapshot provider. It does not implement dynamic context scoring.

## SSOT
- Semantic score source SSOT: `model_core::semantic_prior_scores::SemanticPriorScoreSnapshot`
- Score basis: `token_static_prior_v1`

## Implemented
- `semantic_prior_scores.rs` module
- `SemanticPriorProviderConfig`
- `SemanticPriorScoreSnapshot`
- `build_semantic_prior_score_snapshot(vocab, config)`
- token static QWave heuristic
- token static ΔK heuristic
- NaN/Inf -> 0.0 policy
- score clamp to [-1.0, 1.0]
- `GenerationSamplingConfig.semantic_score_snapshot`
- CPU oracle snapshot lookup via `sample_with_cpu_oracle`
- GPU score buffer supply through `to_gpu_sampling_config()`
- fixture receipts and acceptance artifacts

## Non-scope
- dynamic context QWave
- dynamic context ΔK
- semantic prior default enable
- LoRA/training changes
- tokenizer/vocab/lm_head surgery

## Execution
Static patch only in this environment. Cargo/WGSL runtime validation is NOT_RUN.
