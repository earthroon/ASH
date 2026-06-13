# 16AI-6V-4 V6 Policy Import from 6H-R2 / 6J-R2

16AI-6V-4 imports the already validated V6 facade, 6H-R2 policy, 6I gated commit, and 6J-R2 GPU shadow replay8 results into a static policy registry:

`artifacts/tokenizer_v6_policy_registry.json`

## Contract

- generation: false
- checkpoint_required: false
- gpu_execution: false
- registry_created: true
- global_default_commit: false
- gpu_default: false
- token_ids_mutated: false
- vocab_augmented: false
- new_token_ids_created: false
- embedding_resize_required: false

## Approved Branch-Local Cases

- `ko_descriptive_sentence/dialogue-ko`
- `ko_particle_short/dialogue-ko`

## Fallback Policy

Unknown, tie, worsened, non-dialogue-ko, and missing-policy cases must fall back to `v5-baseline` with an explicit fallback reason.
