# After SFT-GPU-BUILD-03

## Immediate local verification
```powershell
cargo test -p lora_train lm_head_vocab_atlas -- --nocapture
cargo test -p lora_train lm_head_runtime_delta_verify -- --nocapture
```

## If the test fixture layer passes
```powershell
cargo test -p ash_core sft_gpu_obs_07 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
cargo check -p ash_core -p lora_train -p burn_webgpu_backend
```

## If a new layer appears
Proceed with:

```txt
SFT-GPU-BUILD-04 — LoRA Train Test Runtime Assertion Closure / Native GPU Fixture Evidence Seal
```

## Still excluded
- sherpa-rs-sys
- full cargo check --workspace
- native GPU train success claim
