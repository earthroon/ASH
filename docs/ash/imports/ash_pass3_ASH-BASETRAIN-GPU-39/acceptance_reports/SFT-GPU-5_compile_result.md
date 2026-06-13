# SFT-GPU-5 Compile Result

## Status

NOT RUN in this sandbox.

## Reason

`cargo` and `rustc` are not installed in the execution sandbox, so Rust compilation and WGPU runtime smoke could not be executed here.

## Command to run on the project host

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Expected SFT-GPU-5 logs

```txt
[lora_train][gpu_lm_head_lora] smoke PASS gpu_training_steps=... cpu_training_steps=0
[lora_train][artifact] manifest=.../artifacts/lm_head_lora/adapter_manifest.json adapter=.../artifacts/lm_head_lora/adapter_model.safetensors target_key=lm_head artifact_family=module_lora
[lora_train][artifact] reload_ok=true lora_A_shape=[rank,hidden_size] lora_B_shape=[vocab_size,rank]
```
