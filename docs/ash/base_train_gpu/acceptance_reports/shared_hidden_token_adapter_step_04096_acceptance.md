# Shared Hidden Token Adapter Acceptance Seal

## SSOT

- Feature store manifest: `D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_full_gpu_cap192\feature_store_work\feature_store_manifest.json`
- Candidate safetensors: `D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_train_from_feature_store_4096step\artifacts\shared_hidden_token_adapter\classifier_shared_hidden_token_head_step_04096.adapter.safetensors`
- Candidate metadata: `D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_train_from_feature_store_4096step\artifacts\shared_hidden_token_adapter\classifier_shared_hidden_token_head_step_04096.adapter.json`
- Training log: `target\LORA_TRAIN_FEATURE_STORE_4096STEP.log`

## Confirmed State

- Feature store shards: `2519`
- Candidate step: `4096`
- Trained tokens: `786432`
- Observed loaded shard: `52/2519`
- Final loss: `0.002024`
- Checkpoint written: `true`
- bridge_dump_only: `false`
- bridge.extract_only: `false`

## Decision

The 4096-step checkpoint is sealed as an evaluation candidate.

Full 221,628-step training is intentionally deferred until evaluation confirms that the near-zero loss is useful generalization rather than overfitting.

## Acceptance Status

`candidate_pending_eval`
