# SFT-GPU-ACCEPT-01 Bake Report

## What Changed
- Added `GenerationHygieneAcceptanceConfig` and `AcceptanceExitPolicy` to `LoraTrainConfig`.
- Added `generation_hygiene_acceptance.rs` receipt/classification module.
- Added device-lost / bootstrap / empty-output / timeout classifier.
- Added prompt-level acceptance receipt fields for baseline/candidate errors.
- Added artifact preservation and process-exit policy calculation.
- Wired receipt generation into both feature-store train-from-features path and direct training path.
- Updated smoke config with `generation_hygiene_acceptance` soft-fail policy.
- Added regression tests for device-lost isolation, strict fail preservation, soft fail, classifier separation, and partial prompt count preservation.

## SSOT Boundary
- Train artifact SSOT: `adapter_model.safetensors` + `adapter_manifest.json`.
- Runtime delta SSOT: `runtime_delta_report.json` / runtime delta PASS.
- Acceptance SSOT: `generation_hygiene_acceptance_receipt.json`.

## Non-Goals
- Did not change LoRA training math.
- Did not change hidden source guard.
- Did not claim generation quality improvement.
- Did not claim actual fresh-device retry execution in ACCEPT-01.
- Did not delete/quarantine artifacts on device lost.

## Verification
- JSON config syntax checked with `python3 -m json.tool`.
- Rust/Cargo tests were not executable in this container because `cargo` is not installed.
- Intended tests:
  - `cargo test -p lora_train --test generation_hygiene_acceptance_device_isolation -- --nocapture`
  - `cargo test -p lora_train --test sft_gpu_hidden_source_manifest_binding -- --nocapture`
  - `cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1`

## Runtime Expectation
- If `generation_hygiene` fails with `Parent device is lost` after adapter/runtime delta success:
  - `generation_hygiene_acceptance_receipt.json` is written.
  - `final_outcome_class=soft_failed_isolated` under smoke config.
  - `process_should_fail=false` under smoke config.
  - `artifact_preserved=true`.
  - `artifact_quarantined=false`.
