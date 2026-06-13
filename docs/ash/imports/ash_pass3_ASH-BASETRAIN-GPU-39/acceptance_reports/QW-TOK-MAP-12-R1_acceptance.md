# QW-TOK-MAP-12-R1 Acceptance Report

## Patch

QW-TOK-MAP-12-R1  
Local Value-backed Attention Compute Rerun / Actual QKV Score Softmax Seal

## Result

```txt
PENDING_QW_TOK_MAP12_R1_EMBEDDING_VALUE_PATH_NOT_READY
```

## Confirmed In This Bake

- R1 rerun wrapper was added.
- Strict value-backed dependency gate was added.
- Local checkpoint receipt was added.
- Q/K/V locator receipt was added.
- Q/K/V compute receipt was added but actual compute remains false.
- Attention score receipt was added but actual score compute remains false.
- Mask/softmax receipt was added but softmax remains false.
- Attention context receipt was added but context creation remains false.
- lm_head projection remains false.
- logits creation remains false.
- sampler/generation remain false.
- full block forward claim remains false.
- checkpoint write and weight mutation remain false.

## Dependency Blockers

```json
[
  {
    "patch": "QW-TOK-MAP-08",
    "status": "PENDING_QW_TOK_MAP08_CHECKPOINT_FILE_MISSING",
    "reason": "embedding tensor value path is not PASS"
  },
  {
    "patch": "QW-TOK-MAP-09",
    "status": "PARTIAL_QW_TOK_MAP09_SHAPE_ONLY_BRIDGE",
    "reason": "hidden_states bridge is not value-backed PASS"
  },
  {
    "patch": "QW-TOK-MAP-10",
    "status": "PARTIAL_QW_TOK_MAP10_SHAPE_ONLY_BLOCK_INPUT_CONTRACT",
    "reason": "block input contract is not actual PASS"
  },
  {
    "patch": "QW-TOK-MAP-11",
    "status": "PARTIAL_QW_TOK_MAP11_SHAPE_ONLY_ATTENTION_DRYRUN_CONTRACT",
    "reason": "attention shape dry-run is not fully accepted"
  }
]
```

## Local Rerun Command

```bash
cargo run -p model_core --bin qw_tok_map12_r1_value_backed_attention_compute_rerun --   --map08-report artifacts/qw_tok_map08_embedding_tensor_read_probe_report.json   --map09-report artifacts/qw_tok_map09_transformer_input_bridge_report.json   --map10-report artifacts/qw_tok_map10_first_block_input_contract_report.json   --map11-report artifacts/qw_tok_map11_attention_kernel_dryrun_shape_contract_report.json   --map12-report artifacts/qw_tok_map12_first_attention_compute_probe_report.json   --checkpoint tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors   --backend cpu-limited-probe   --output-mode attention-context-only   --require-value-backed-dependencies   --require-rotary-config   --forbid-lm-head   --forbid-logits   --forbid-generation   --forbid-full-block-forward-claim
```

## Next

After the local dependency chain is value-backed PASS, rerun this patch locally to produce:

```txt
PASS_QW_TOK_MAP12_R1_VALUE_BACKED_ATTENTION_COMPUTE_RERUN
```

Then continue to:

```txt
QW-TOK-MAP-13
First Block Forward Probe / No Logits Seal
```
