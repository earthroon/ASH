# QW-TOK-FORGE-01-S2-R2 Acceptance

Status: BAKED_STATIC

Expected local command:

```powershell
$root = "D:\1111113232\DUST\1\ash_pass3"
$exe = "$root\target\debug\qw_tok_forge01_embed_lmhead_bootstrap.exe"
$s2r2log = "$root\artifacts\qw_tok_forge01_s2_r2_rebind.log"

& $exe `
  --model-spec "$root\specs\model_spec_v5_48259.toml" `
  --tokenizer "$root\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --corpus-pack "$root\artifacts\qw_tok_forge01_s2_encoded_corpus_pack.bin" `
  --rebind-existing-corpus-pack-evidence `
  --verify-qwc-pack-header `
  --verify-qwc-token-range `
  --detect-s2-receipt-clobber `
  --no-corpus-reencode `
  --no-checkpoint-read `
  --no-checkpoint-write `
  2>&1 | Tee-Object -FilePath $s2r2log
```

Expected runtime receipts:

- `artifacts/qw_tok_forge01_s2_r2_existing_pack_rebind_receipt.json`
- `artifacts/qw_tok_forge01_s2_r2_pack_header_receipt.json`
- `artifacts/qw_tok_forge01_s2_r2_token_range_rebind_receipt.json`
- `artifacts/qw_tok_forge01_s2_r2_pack_hash_receipt.json`
- `artifacts/qw_tok_forge01_s2_r2_receipt_clobber_receipt.json`
- `artifacts/qw_tok_forge01_s2_r2_no_reencode_no_training_receipt.json`

The baked zip must not include runtime `artifacts/*.json` payloads.
