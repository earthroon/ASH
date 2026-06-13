# MODELCORE-COMPILE-16A — Shared Hidden Token Adapter Checkpoint Acceptance / Eval Seal

## Purpose

Seal the `shared_hidden_token_adapter` checkpoint produced at step 4096 as the current evaluation candidate, using the user's provided run output as SSOT.

This patch does not trigger a full 221,628-step run. It records the existing successful 4096-step run and adds a runtime acceptance-report writer so future feature-store training runs emit the same acceptance surface automatically.

## SSOT

- Feature store manifest: `workspace/lora_runs/tinyllama_1p1b_v5_guarded_dump_full_gpu_cap192/feature_store_work/feature_store_manifest.json`
- Candidate checkpoint: `workspace/lora_runs/tinyllama_1p1b_v5_guarded_train_from_feature_store_4096step/artifacts/shared_hidden_token_adapter/classifier_shared_hidden_token_head_step_04096.adapter.safetensors`
- Candidate metadata: `workspace/lora_runs/tinyllama_1p1b_v5_guarded_train_from_feature_store_4096step/artifacts/shared_hidden_token_adapter/classifier_shared_hidden_token_head_step_04096.adapter.json`
- Training log: `target/LORA_TRAIN_FEATURE_STORE_4096STEP.log`

## Confirmed State

- source shards: `2519`
- feature-store ingest: passed
- multi-shard training: passed
- observed loaded shard: `52/2519`
- train steps: `4096`
- trained tokens: `786432`
- final loss: `0.002024`
- checkpoint_written: `true`
- bridge_dump_only: `false`
- bridge.extract_only: `false`

## Changed Files

- `crates/lora_train/src/training.rs`
- `acceptance_reports/shared_hidden_token_adapter_step_04096_acceptance.json`
- `acceptance_reports/shared_hidden_token_adapter_step_04096_acceptance.md`

## Runtime Changes

- Added `SharedHiddenAdapterAcceptanceReport`.
- Added `write_shared_hidden_adapter_acceptance_report(...)`.
- Records:
  - candidate step
  - trained batches/tokens
  - final loss and finite/threshold pass state
  - checkpoint paths
  - source feature-store manifest
  - source shard count
  - observed max loaded shard
  - `bridge_dump_only` and `bridge.extract_only` state
  - acceptance status
- Emits:
  - `[acceptance][candidate] ... status=candidate_pending_eval ...`
  - `acceptance_reports/shared_hidden_token_adapter_step_<step>_acceptance.json`
  - `acceptance_reports/shared_hidden_token_adapter_step_<step>_acceptance.md`

## Decision

The 4096-step checkpoint is sealed as an evaluation candidate.

Full 221,628-step training remains intentionally deferred until evaluation confirms the near-zero loss is useful generalization rather than overfitting.

## Acceptance Status

`candidate_pending_eval`

## Pass Criteria

- Existing feature-store manifest is reused.
- No bridge dump path is re-entered.
- `bridge_dump_only=false`.
- `bridge.extract_only=false`.
- `checkpoint_written=true`.
- `final_loss` is finite.
- `final_loss <= 0.01`.
- Acceptance report is generated.

## Fail Conditions

- `bridge_dump_only=true` returns.
- Feature store regeneration is attempted.
- Compact GPU teacher is re-entered during train ingest.
- `checkpoint_written=false`.
- `final_loss` is NaN/inf.
- Acceptance report is missing.
