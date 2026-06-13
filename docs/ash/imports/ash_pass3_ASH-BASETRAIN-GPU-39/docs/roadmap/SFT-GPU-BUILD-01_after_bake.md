# After SFT-GPU-BUILD-01

## Immediate next command

```powershell
cargo check -p ash_core -p lora_train -p burn_webgpu_backend
```

## If BUILD-01 closes ash_core
Proceed to:

```powershell
cargo test -p ash_core sft_gpu_obs_07 -- --nocapture
cargo test -p ash_core sft_gpu_obs_06 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
cargo test -p lora_train gpu_candidate_apply_plan -- --nocapture
cargo test -p burn_webgpu_backend gpu_candidate_apply_plan_signals -- --nocapture
```

## If more compile errors appear
Create BUILD-02 only from the new compiler layer. Do not resume OBS-08 until the GPU-SFT cargo closure is clean.

## Deferred
- sherpa-rs-sys CMake generator repair
- full workspace cargo check
- native GPU train runtime evidence
- ASH runtime inference stream evidence
