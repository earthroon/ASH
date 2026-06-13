# ASH-TOK-TENSOR-01 Bake Report

## Patch

```txt
ASH-TOK-TENSOR-01
Incomplete Safetensors Artifact Sentinel /
No Full Tensor Load No Row Parity Claim Seal
```

## Files Added

```txt
crates/model_core/src/ash_tok_tensor_01_incomplete_safetensors_sentinel.rs
crates/model_core/src/bin/ash_tok_tensor_01_incomplete_safetensors_sentinel.rs
acceptance_reports/ASH-TOK-TENSOR-01.md
patch_reports/ASH-TOK-TENSOR-01_bake_report.md
ASH_TOK_TENSOR_01_STATIC_CHECKS.txt
ASH_TOK_TENSOR_01_SENTINEL_RECEIPT.json
ASH_TOK_TENSOR_01_BASETRAIN_RISK_CALLSITES.json
ASH_TOK_TENSOR_01_BAKE_MANIFEST.json
```

## Files Modified

```txt
crates/model_core/src/lib.rs
crates/model_core/Cargo.toml
```

## External Asset Packaging Guard

The following source assets are not included in this bake package:

```txt
tokenizer_manifest_v5_final.json
tokenizer_manifest_v5_final.before_manifest_hash_cleanup.json
tokenizer_v5.vocab
tokenizer_v5.model
ash_v5_native_genesis.forge01_smoke.safetensors
```

## No-Execution Seal

```txt
full_safetensors_probe_executed = false
full_tensor_load_executed = false
row_parity_probe_executed = false
model_forward_executed = false
optimizer_step_executed = false
weight_commit_executed = false
```

## Local Validation

`cargo` and `rustc` are not installed in the current container, so compiler validation is not claimed. Static file checks and ZIP integrity checks are included instead.

## Verdict

```txt
PASS_ASH_TOK_TENSOR_01_INCOMPLETE_SAFETENSORS_SENTINEL_NO_FULL_TENSOR_LOAD_NO_ROW_PARITY_CLAIM
```
