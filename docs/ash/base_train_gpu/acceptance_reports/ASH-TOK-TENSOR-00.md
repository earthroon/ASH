# ASH-TOK-TENSOR-00 Acceptance Report

```txt
ASH-TOK-TENSOR-00
Tokenizer V5 External Reference Freeze + Cheonjiin/QWave Side-Channel Map /
No Token Id Remap No Vocab Expansion No Asset Vendoring Seal
```

## 확정

`tokenizer_v5` assets are external-reference-only assets. They are not packaged into this bake output.

```txt
final_manifest_is_ssot = true
before_manifest_is_audit_reference = true
before_manifest_allowed_as_ssot = false

vocab_size = 48259
min_token_id = 0
max_token_id = 48258

manifest_hash = 09631187ffe1b964399c95f8c446cb47931db31393d184647260d54390910a59
sentencepiece_model_hash = sha256:01fab65d32069448bbf4f7e85623cb48c78dc2714c20b15362832246902dbf69
sentencepiece_vocab_hash = sha256:f31c975276380ffa462aec87a83b871dadab0bd07c5a6efa64413881c1b5dc16
vocab_hash = sha256:f31c975276380ffa462aec87a83b871dadab0bd07c5a6efa64413881c1b5dc16

final_manifest_file_sha256 = 6e848e6819fde843ebab5af01cc3fbec4984d0a1b0782caa244c05fc6f588dd7
tokenizer_v5_vocab_file_sha256 = f31c975276380ffa462aec87a83b871dadab0bd07c5a6efa64413881c1b5dc16
tokenizer_v5_model_file_sha256 = 01fab65d32069448bbf4f7e85623cb48c78dc2714c20b15362832246902dbf69
before_manifest_file_sha256 = ceb822aaa2a055a536ac0f0f17924c32e85395bee17fec8ad40278dc21883b09
```

Signal tokens are preserved as control flags, not numeric feature carriers.

```txt
<qwave:on> = 58
<delta_k:on> = 60
<morph:on> = 62
<cheon:on> = 64
<ji:on> = 65
<in:on> = 66

signal_tokens_used_as_control_flags = true
signal_tokens_used_as_numeric_feature_carriers = false
signal_tokens_added_again = false
```

Cheonjiin/QWave map:

```txt
X = Ji / ji_support
Y = In / in_bridge
Z = Cheon / cheon_core

tensor_feature_encoded_as_new_token = false
tensor_feature_vocab_injection = false
```

## External safetensors reference

```txt
safetensors_path = D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors
safetensors_external_reference_only = true
safetensors_hash_checked = false
safetensors_tensor_keys_read = false
embedding_row_parity_checked = false
lm_head_row_parity_checked = false
safetensors_packaged_in_zip = false
```

## PASS

```txt
PASS_ASH_TOK_TENSOR_00_EXTERNAL_REFERENCE_VOCAB_FREEZE_CHEONJIIN_QWAVE_MAP_NO_ASSET_VENDORING
```

## WARN

```txt
WARN_ASH_TOK_TENSOR_00_SAFETENSORS_PATH_BOUND_HASH_NOT_CHECKED
WARN_ASH_TOK_TENSOR_00_EXTERNAL_TOKENIZER_ASSETS_NOT_PACKAGED
```

Both warnings are expected. This patch binds external references only and does not open safetensors or package tokenizer assets.

## FAIL guards

```txt
FAIL_FINAL_MANIFEST_MISSING
FAIL_FINAL_MANIFEST_NOT_ALLOWED_AS_SSOT
FAIL_BEFORE_MANIFEST_USED_AS_SSOT
FAIL_VOCAB_SIZE_NOT_48259
FAIL_TOKEN_ID_RANGE_NOT_0_48258
FAIL_TOKEN_ID_REMAP_DETECTED
FAIL_VOCAB_EXPANSION_DETECTED
FAIL_EMBEDDING_ROW_REORDER_DETECTED
FAIL_SIGNAL_TOKEN_USED_AS_NUMERIC_FEATURE_CARRIER
FAIL_TENSOR_FEATURE_ENCODED_AS_TOKEN
FAIL_TOKENIZER_VOCAB_PACKAGED_IN_ZIP
FAIL_TOKENIZER_MODEL_PACKAGED_IN_ZIP
FAIL_SAFETENSORS_PACKAGED_IN_ZIP
FAIL_SAFETENSORS_WEIGHT_MUTATION_EXECUTED
FAIL_GPU_DISPATCH_EXECUTED_TOO_EARLY
FAIL_MODEL_FORWARD_EXECUTED_TOO_EARLY
```
