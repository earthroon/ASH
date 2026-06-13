# ASH Tokenizer V4 Binding

This project tree includes the tokenizer V4 draft contract and migration tooling bound into the Ash main project.

## Bound artifacts
- `tokenizer_manifest_clean_v4.draft.json`
- `specs/tokenizer_spec_v4.toml`
- `specs/model_spec_1p1b_v2.toml`
- `specs/runtime_profile_v2.toml`
- `tools/tokenizer/ash_full_v4_manifest_generator.py`
- `tools/tokenizer/ash_v3_to_v4_migrate.py`
- `tools/tokenizer/v4_candidate_tokens.example.json`

## Important status
- `runtime_profile.toml` remains the current default runtime profile.
- `runtime_profile_v2.toml` is bound and runnable as an alternate profile.
- `tokenizer_manifest_clean_v4.draft.json` is still a draft scaffold, not a trained final tokenizer artifact.
- Prompt template `dust_system_guard_ko` is bound into the native host helpers so `runtime_profile_v2.toml` does not dangle.

## Suggested switch order
1. Build the final V4 tokenizer manifest.
2. Run V3 to V4 embedding/lm_head migration.
3. Point launch scripts or CLI runs to `specs/runtime_profile_v2.toml`.
4. Promote `runtime_profile_v2.toml` to the default only after validation.
