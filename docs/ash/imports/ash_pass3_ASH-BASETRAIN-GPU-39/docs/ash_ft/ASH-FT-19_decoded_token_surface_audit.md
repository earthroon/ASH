# ASH-FT-19 Decoded Token Surface Audit

ASH-FT-19 is the first post-FT-18 surface audit stage. FT-18 proved that the selected token id can be decoded in a controlled single-token boundary. FT-19 does not display the decoded token. It classifies the surface and decides whether a later explicit preview gate may be opened.

## Boundary

- `allow_token_surface_read = true`
- `allow_raw_token_surface_print = false`
- `allow_token_surface_preview = false`
- `allow_decoded_text_output = false`
- `allow_sequence_commit = false`
- `generation = false`
- `sampling = false`
- `user_prompt = false`
- `runtime_default_apply = false`
- `checkpoint_alias_rebind = false`
- `promotion = false`

## Surface policy

FT-19 creates policy only. It does not execute preview.

- Invalid UTF-8: blocked
- Empty surface: blocked
- Special-like surface: blocked
- Control character: escaped preview candidate only
- Whitespace-only: escaped preview candidate only
- Printable normal: safe preview candidate

## Runtime entry

```powershell
cargo run --bin ash_ft19_decoded_token_surface_audit -- `
  --tokenizer-manifest "tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --tokenizer-vocab "tokenizer_v5\artifacts\tokenizer_v5.vocab" `
  --ft18-token-decode "artifacts\ash_ft\ash_ft18_token_decode_receipt.json" `
  --ft18-decoded-surface "artifacts\ash_ft\ash_ft18_decoded_token_surface_receipt.json" `
  --ft18-sequence-commit-guard "artifacts\ash_ft\ash_ft18_sequence_commit_guard.json" `
  --ft18-no-generation-guard "artifacts\ash_ft\ash_ft18_no_generation_guard.json" `
  --ft18-receipt "artifacts\ash_ft\ASH-FT-18_receipt.json" `
  --selected-token-id 34196 `
  --allow-token-surface-read true `
  --allow-raw-token-surface-print false `
  --allow-token-surface-preview false `
  --allow-decoded-text-output false `
  --allow-sequence-commit false `
  --generation false `
  --sampling false `
  --user-prompt false `
  --runtime-default-apply false `
  --checkpoint-alias-rebind false `
  --promotion false `
  --out-audit-plan "artifacts\ash_ft\ash_ft19_surface_audit_plan.json" `
  --out-surface-audit "artifacts\ash_ft\ash_ft19_decoded_token_surface_audit.json" `
  --out-safe-preview-policy "artifacts\ash_ft\ash_ft19_safe_preview_policy_receipt.json" `
  --out-sequence-commit-guard "artifacts\ash_ft\ash_ft19_sequence_commit_guard.json" `
  --out-no-generation-guard "artifacts\ash_ft\ash_ft19_no_generation_guard.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-19_receipt.json"
```
