# 16AI-6V-5 V6 Branch-Local Replay

This commit reads `artifacts/tokenizer_v6_policy_registry.json`, selects only approved branch-local cases, resolves committed ids through V3 facade output with a 6I gated commit fallback, and runs CPU reference generation with `max_new_tokens=1`.

## Contract

- generation=true
- checkpoint_required=true
- gpu_execution=false
- runtime_mode=v6-branch-local
- global_default_commit=false
- gpu_default=false
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false
- embedding_resize_required=false

## Expected approved cases

- ko_descriptive_sentence / dialogue-ko
- ko_particle_short / dialogue-ko
