# 16AI-6W-6 Suppression Policy Shadow Commit

## Purpose

Register the byte-token suppression policy for `token_id=171` / `<0x63>` as a shadow-only policy after W5 controlled replay passes.

This step does not enable the default runtime path. It only writes a shadow policy registry that can be inspected and used by later shadow replay stages.

## Contract

- `activation_mode=shadow-only`
- `default_runtime_enabled=false`
- `default_sampler_mutated=false`
- `output_mutated=false`
- `runtime_default_committed=false`
- `global_default_commit=false`
- `gpu_default=false`
- `new_token_ids_created=false`
- `embedding_resize_required=false`

## Source gates

- `16AI-6W-5 = PASS_CONTROLLED_SUPPRESSION_REPLAY`
- `16AI-6W-4 = PASS_SUPPRESSION_POLICY_DRY_COMMIT_GATE`
- `16AI-6W-3 = PASS_SUPPRESSION_DRY_RUN_REPLAY`
- `16AI-6W-2 = PASS_BYTE_TOKEN_SUPPRESSION_CANDIDATE_GATE`
- `16AI-6W-1 = PASS_BYTE_TOKEN_LOGIT_ATTRIBUTION`
- `16AI-6V-5-R3 = PASS_DECODER_OUTPUT_SANITY_GATE`

## Output registry

`artifacts/byte_token_suppression_shadow_policy_registry.json`

## Expected seal

```txt
[16AI-6W-6][seal] SUPPRESSION_POLICY_SHADOW_COMMIT_RECORDED status=PASS_SUPPRESSION_POLICY_SHADOW_COMMIT generation=false checkpoint_required=false gpu_execution=false shadow_policy_commit=true activation_mode=shadow-only global_default_commit=false gpu_default=false default_runtime_enabled=false default_sampler_mutated=false output_mutated=false runtime_default_committed=false token_ids_mutated=false vocab_augmented=false new_token_ids_created=false embedding_resize_required=false
```
