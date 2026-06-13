# SFT-GPU-ACCEPT-01 Acceptance Report

## Source State
- train_from_features_completed: expected before acceptance
- lm_head_vocab_atlas_pass: preserved by existing `lm_head_vocab_atlas` PASS gate
- streaming_ce: preserved by existing training report
- full_vocab_buffer: expected false in training log
- full_logits_buffer: expected false in training log
- adapter_model_exists: checked by ACCEPT-01 receipt
- adapter_manifest_exists: checked by ACCEPT-01 receipt
- runtime_delta_passed: checked before acceptance receipt generation

## Failure Source
- acceptance_phase_entered: `one-shot direct-line acceptance`
- generation_hygiene_pass: read from `GenerationHygieneReport.pass`
- parent_device_lost_detected: classified from prompt/runtime failure strings
- device_lost_count: written to `generation_hygiene_acceptance_receipt.json`
- existing_device_lost_count: written when failure text contains `existing-device`

## Policy
- exit_policy: `GenerationHygieneAcceptanceConfig.exit_policy`
- isolate_device_per_prompt: recorded policy only in ACCEPT-01; real retry/session rebuild is deferred
- retry_on_device_lost: recorded as requested; no silent retry is claimed in ACCEPT-01
- device_lost_retry_limit: recorded config value
- fresh_device_retry_on_existing_device_lost: recorded config value
- preserve_artifact_on_acceptance_failure: default true
- treat_device_lost_as_artifact_failure: default false

## Receipt
- receipt_path: `workspace/lora_runs/<run>/artifacts/lm_head_lora/generation_hygiene_acceptance_receipt.json`
- final_outcome_class: `passed`, `failed_device_lost`, `failed_bootstrap`, `failed_empty_output`, `soft_failed_isolated`, etc.
- process_should_fail: computed from exit policy and artifact/runtime delta success
- artifact_preserved: true when adapter exists and preserve policy is enabled
- artifact_quarantined: false for device lost under default policy
- train_success_preserved: adapter + manifest + runtime delta SSOT remains true even when acceptance fails

## Tests
- Added: `cargo test -p lora_train --test generation_hygiene_acceptance_device_isolation -- --nocapture`
- Existing guard to rerun: `cargo test -p lora_train --test sft_gpu_hidden_source_manifest_binding -- --nocapture`

## Runtime
- command: `cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1`
- expected ACCEPT-01 behavior: generation hygiene device lost writes receipt and soft-fails under smoke policy instead of misclassifying train artifact failure

## Result
- accept_01_passed: source patched; local compile/test not executed in this container because Rust/Cargo is unavailable
- remaining_issue: ACCEPT-02 should implement real fresh-device prompt session retry; ACCEPT-03 should remove CPU materialized last-row fallback from generation hygiene
