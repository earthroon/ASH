# ASH-FT-18 BAKED

Patch: `ASH-FT-18`

Title: `Shadow Candidate Controlled Token Decode Smoke / No Generation No Sequence Commit Seal`

Base dependency: `PASS_ASH_FT17_SHADOW_CANDIDATE_TOKEN_DECODE_GATE_PREFLIGHT_NO_TEXT_OUTPUT_NO_GENERATION`

Expected pass:

```txt
PASS_ASH_FT18_SHADOW_CANDIDATE_CONTROLLED_TOKEN_DECODE_SMOKE_NO_GENERATION_NO_SEQUENCE_COMMIT
```

## Scope

ASH-FT-18 opens exactly one controlled single-token decode for the FT-16 selected token id `34196` after FT-17 decode-gate preflight has passed.

It permits:

- read FT-16 token id selection receipts
- read FT-17 decode gate receipts
- verify tokenizer manifest/vocab paths
- controlled token decode/string lookup for selected token id `34196`
- write token decode, decoded surface, sequence-commit guard, no-generation guard, and main receipt

It forbids:

- decoded text output
- token surface printing by default
- sequence commit
- prompt/output append
- generation loop
- sampling
- user prompt inference
- runtime default apply
- checkpoint alias rebind
- promotion
- train

## CLI

```powershell
cargo run --bin ash_ft18_shadow_candidate_controlled_token_decode_smoke -- `
  --tokenizer-manifest "tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --tokenizer-vocab "tokenizer_v5\artifacts\tokenizer_v5.vocab" `
  --ft16-selector-execution "artifacts\ash_ft\ash_ft16_selector_execution_receipt.json" `
  --ft16-token-id-range "artifacts\ash_ft\ash_ft16_token_id_range_receipt.json" `
  --ft16-reserved-token-policy "artifacts\ash_ft\ash_ft16_reserved_token_policy_receipt.json" `
  --ft17-decode-gate-plan "artifacts\ash_ft\ash_ft17_token_decode_gate_plan.json" `
  --ft17-tokenizer-lookup-preflight "artifacts\ash_ft\ash_ft17_tokenizer_lookup_preflight.json" `
  --ft17-decode-policy "artifacts\ash_ft\ash_ft17_decode_policy_receipt.json" `
  --ft17-special-token-guard "artifacts\ash_ft\ash_ft17_special_token_decode_guard.json" `
  --ft17-no-text-output-guard "artifacts\ash_ft\ash_ft17_no_text_output_guard.json" `
  --model-vocab-size 48259 `
  --tokenizer-vocab-size 48259 `
  --selected-token-id 34196 `
  --decode-mode controlled_single_token_decode `
  --allow-token-decode true `
  --allow-token-string-lookup true `
  --allow-token-surface-preview false `
  --allow-decoded-text-output false `
  --allow-sequence-commit false `
  --allow-special-token-decode false `
  --generation false `
  --sampling false `
  --user-prompt false `
  --runtime-default-apply false `
  --checkpoint-alias-rebind false `
  --promotion false `
  --worker-stack-mb 128 `
  --out-decode-plan "artifacts\ash_ft\ash_ft18_controlled_decode_plan.json" `
  --out-token-decode "artifacts\ash_ft\ash_ft18_token_decode_receipt.json" `
  --out-decoded-surface "artifacts\ash_ft\ash_ft18_decoded_token_surface_receipt.json" `
  --out-sequence-commit-guard "artifacts\ash_ft\ash_ft18_sequence_commit_guard.json" `
  --out-no-generation-guard "artifacts\ash_ft\ash_ft18_no_generation_guard.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-18_receipt.json"
```

## Notes

The default output does not print the decoded token surface. It records length and SHA256 only. Use `--allow-token-surface-preview true` only when a later audit explicitly wants the surface exposed.
