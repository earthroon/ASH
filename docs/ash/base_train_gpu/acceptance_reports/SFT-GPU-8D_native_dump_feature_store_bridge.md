# SFT-GPU-8D Acceptance

## Status

PENDING

## Scope

native_dump -> feature_store_manifest -> train_from_features bridge seal

## Required Contract

- `phase=native_dump` may use the full checkpoint-backed teacher.
- `phase=train_from_features` must not use the full checkpoint-backed teacher.
- native dump writes `feature_store_manifest.json` and feature batch safetensors.
- train-from-features loads the manifest and feeds lm_head LoRA GPU smoke from feature batches.
- prompt loss remains zero and response loss tokens remain positive.

## Gates

- [ ] native_dump config has `phase=native_dump`.
- [ ] train_from_features config has `phase=train_from_features`.
- [ ] native_dump logs full checkpoint teacher only under dump phase.
- [ ] native_dump writes `feature_store_manifest.json`.
- [ ] native_dump writes `lm_head_weight.safetensors` snapshot for train phase.
- [ ] manifest `target_key=lm_head`.
- [ ] manifest `artifact_family=module_lora`.
- [ ] manifest `batch_count > 0`.
- [ ] manifest `total_response_loss_tokens > 0` via feature stats/report.
- [ ] train_from_features loads manifest.
- [ ] train_from_features does not load full checkpoint teacher.
- [ ] feature batch hidden shape matches `hidden_size`.
- [ ] feature batch labels length matches hidden token count.
- [ ] GPU lm_head LoRA smoke consumes feature batches.

## Non-goals

- This commit does not implement Atlas grouped direct hidden provider.
- This commit does not run SFT-GPU-9 experiment matrix.
- This commit does not judge final generation quality.
