# Ash V4 Contract Switch Draft Pack

This pack contains draft switch-over files aligned to the uploaded V3 project layout.

Included:
- tokenizer_manifest_clean_v4.draft.json
- tokenizer_spec_v4.toml
- model_spec_1p1b_v2.toml
- runtime_profile_v2.toml

Notes:
- This is an SSOT draft pack, not a final train-ready tokenizer artifact.
- `tokenizer_manifest_clean_v4.draft.json` preserves reserved IDs 0..31 from V3 and extends reserved tokens through ID 71.
- `vocab_size` is set to 56832 across tokenizer and model specs.
- `runtime_profile_v2.toml` points to the V4 draft manifest and switches the default prompt template to `dust_system_guard_ko`.
- Final rollout still requires:
  1. actual tokenizer build,
  2. full vocab population,
  3. embedding/lm_head resize,
  4. runtime prompt template implementation,
  5. A/B validation.
