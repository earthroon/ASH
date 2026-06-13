# 16AI-3 Acceptance — PENDING LOCAL RUN

## Acceptance Criteria

- AC-16AI-3-1: `model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml` uses checkpoint/tokenizer SSOT dimensions.
- AC-16AI-3-2: `vocab_size=48259`.
- AC-16AI-3-3: `hidden_size=2048`.
- AC-16AI-3-4: `intermediate_size=5632`.
- AC-16AI-3-5: checkpoint embedding/lm_head row counts match spec vocab size on 16AI-2 rerun.
- AC-16AI-3-6: checkpoint embedding/lm_head hidden dim matches spec hidden size on 16AI-2 rerun.
- AC-16AI-3-7: special-token fragmentation is not silently fixed or hidden in this commit.
- AC-16AI-3-8: generation defaults and CPU fallback remain unchanged.

## Current status
Source bake complete. Runtime/local audit rerun pending.
