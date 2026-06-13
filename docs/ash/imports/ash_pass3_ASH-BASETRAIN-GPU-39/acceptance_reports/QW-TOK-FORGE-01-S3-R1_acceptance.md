# QW-TOK-FORGE-01-S3-R1 Acceptance

Status at bake time: BAKED / LOCAL EXECUTION REQUIRED.

Run locally:

```powershell
$root = "D:\1111113232\DUST\1\ash_pass3"
$exe = "$root\target\debug\qw_tok_forge01_embed_lmhead_bootstrap.exe"
$s3r1log = "$root\artifacts\qw_tok_forge01_s3_r1_rebind.log"

& $exe `
  --model-spec "$root\specs\model_spec_v5_48259.toml" `
  --tokenizer "$root\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json" `
  --checkpoint "$root\tokenizer_v5\artifacts\ash_v5_native_genesis.forge00.safetensors" `
  --corpus-pack "$root\artifacts\qw_tok_forge01_s2_encoded_corpus_pack.bin" `
  --out-checkpoint "$root\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors" `
  --rebind-existing-smoke-evidence `
  --verify-existing-smoke-candidate-hash `
  --detect-runtime-receipt-clobber `
  --no-retrain `
  --no-checkpoint-write `
  2>&1 | Tee-Object -FilePath $s3r1log
```

Expected primary status:

`PASS_QW_TOK_FORGE01_S3_R1_EXISTING_SMOKE_REBIND`
