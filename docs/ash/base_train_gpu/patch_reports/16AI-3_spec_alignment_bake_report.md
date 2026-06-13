# 16AI-3 Spec Alignment Bake Report

## Seal
16AI-3 — Checkpoint/Tokenizer SSOT Spec Alignment

## Basis
16AI-2 alignment audit selected Option A: checkpoint/tokenizer become the temporary SSOT.

## Changed
- Updated `specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml`.
- Added backup: `specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.pre16AI3_mismatch.toml`.

## Dimension alignment
- `vocab_size`: `56253 -> 48259`
- `hidden_size`: `1024 -> 2048`
- `intermediate_size`: `3072 -> 5632`
- `num_attention_heads`: `16 -> 32`
- `num_key_value_heads`: `8 -> 4`
- `head_dim`: remains `64`
- `num_layers`: remains `14`

## Intent
This patch does not fix special-token fragmentation. It only realigns the spec against the live tokenizer manifest and checkpoint tensor shapes.

## Generation state
- `generation_connected_default=false` remains the operational contract.
- CPU reference fallback remains required.
- Native FFN candidate remains gated.

## Next audit
Run 16AI-2 alignment audit again. Expected hard alignment changes:
- `spec vocab_size` should match manifest/checkpoint rows: `48259`.
- `spec hidden_size` should match checkpoint embedding/lm_head dim: `2048`.
- Special-token fragmentation is still expected to fail until 16AI-4.
