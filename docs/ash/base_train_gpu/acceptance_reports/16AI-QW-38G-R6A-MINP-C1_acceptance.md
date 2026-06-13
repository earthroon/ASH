# Acceptance — 16AI-QW-38G-R6A-MINP-C1

## Result

STATIC_PASS

## Static checks

- generation_semantic_prior_config_exists: PASS
- generation_sampling_has_semantic_prior_field: PASS
- generation_to_gpu_passes_semantic_prior: PASS
- cpu_oracle_semantic_scores_interface: PASS
- cpu_oracle_uses_weighted_logit: PASS
- cpu_trace_has_bias_stats: PASS
- gpu_semantic_prior_config_exists: PASS
- gpu_config_has_score_buffers: PASS
- gpu_uniform_has_semantic_fields: PASS
- gpu_dispatch_allocates_score_buffers: PASS
- topk_uses_weighted_logit: PASS
- topp_uses_weighted_logit: PASS
- select_uses_weighted_score: PASS
- legacy_zero_source_fallback: PASS
- runtime_semantic_prior_config_exists: PASS
- runtime_env_gate_exists: PASS

## Execution checks

- cargo check: NOT_RUN
- cargo test: NOT_RUN
- rustfmt: NOT_RUN
- WebGPU runtime parity: NOT_RUN

## Acceptance note

This is accepted as a static bake only. Runtime promotion requires actual QWave/ΔK score source buffers plus SAMPLER-04 strict readiness.
