# 16AI-QW-38G-R6A-MINP-C1 — ΔK-QWave Weighted Min-P Core Sampler Bake Report

## Static status

STATIC_PASS

## Scope

Implemented semantic-prior plumbing and weighted-logit sampler hooks without inventing QWave/ΔK score sources. Missing score sources resolve to zero, so the sampler falls back to vanilla behavior and records the non-effective state.

## Key changes

- Added `SemanticPriorConfig` to `GenerationSamplingConfig`.
- Added `RuntimeSemanticPriorConfig` and `ASH_SEMANTIC_PRIOR*` environment gate.
- Added CPU oracle `SemanticPriorScores` and `sample_with_cpu_oracle_with_semantic_prior`.
- Added GPU `GpuSemanticPriorConfig`, optional qwave/deltak score buffers, and semantic-prior uniform fields.
- Wired WebGPU top-k, top-p/min-p scan, and final select shaders to weighted logits where score sources exist.
- Extended candidate trace entries with `semantic_bias` and `weighted_logit`.

## Important limitation

The bake does **not** generate QWave or ΔK token scores. That remains a future source-provider patch. With no source buffer, C1 is deliberately non-effective and preserves vanilla sampler behavior.

## Execution

`cargo`, `rustc`, `rustfmt`, and WebGPU runtime validation were unavailable in this container, so execution validation is `NOT_RUN`.
