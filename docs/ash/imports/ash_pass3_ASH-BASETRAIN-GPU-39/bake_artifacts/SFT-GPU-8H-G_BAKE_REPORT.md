# SFT-GPU-8H-G Bake Report

## Status
PASS_STATIC / runtime not executed in this environment.

## Added
- `lm_head_vocab_atlas_gpu_profiler.rs`
- `lm_head_vocab_atlas_gpu_export.rs`
- GPU export/readback/timing config blocks
- adapter export and train-step seal wiring after 8H-F update

## Runtime expected
- `PASS_GPU_PARALLEL_TRAIN_STEP_SEAL`
- `adapter_manifest.json` written
- `adapter_model.safetensors` written
- `logits_readback=false`
- `full_weight_readback=false`
