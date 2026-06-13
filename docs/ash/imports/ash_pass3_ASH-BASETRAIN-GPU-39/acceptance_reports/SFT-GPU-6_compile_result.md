# SFT-GPU-6 Compile / Runtime Result

## Status

NOT_RUN_IN_SANDBOX

## Reason

The execution sandbox used for this bake does not provide `cargo`, `rustc`, or a WGPU runtime device. Therefore, compile and runtime smoke could not be executed here.

## Local Verification Command

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Expected SFT-GPU-6 Logs

```txt
[lora_train][artifact] reload_ok=true ...
[lora_train][runtime_delta] artifact_family=module_lora target_key=lm_head runtime_loader=model_core::load_runtime_lora_attachments execution_mode=runtime_loader_plus_lm_head_delta_equivalence
[lora_train][runtime_delta] adapter load_ok=true attach_ok=true logits_off_shape=[..., ...] logits_on_shape=[..., ...]
[lora_train][runtime_delta] delta_max_abs=... delta_mean_abs=... nonzero=... reload_reproducible=true
[lora_train][runtime_delta] PASS
```

## Expected Artifacts

```txt
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/adapter_manifest.json
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/adapter_model.safetensors
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/adapter_runtime.json
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/runtime_delta_report.json
workspace/lora_runs/<run_name>/artifacts/lm_head_lora/runtime_delta_report.md
```
