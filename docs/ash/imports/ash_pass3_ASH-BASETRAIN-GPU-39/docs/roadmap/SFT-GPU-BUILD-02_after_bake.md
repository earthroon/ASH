# SFT-GPU-BUILD-02 After Bake Roadmap

## Immediate Local Check
```powershell
cargo check -p ash_core -p lora_train -p burn_webgpu_backend
```

## If This Passes
```powershell
cargo test -p lora_train lm_head_vocab_atlas -- --nocapture
cargo test -p lora_train lm_head_runtime_delta_verify -- --nocapture
cargo test -p ash_core sft_gpu_obs_07 -- --nocapture
```

## If Another Layer Appears
Proceed with:

```txt
SFT-GPU-BUILD-03 — Remaining Cargo Check Closure / Next Error Layer Seal
```

## Still Excluded
- sherpa-rs-sys
- full workspace closure
- native GPU runtime execution claim
