# SFT-GPU-BUILD-01 Bake Report

## Summary
SFT-GPU-BUILD-01 patches the OBS-07 baked tree to target the sherpa-excluded GPU-SFT cargo closure path:

```powershell
cargo check -p ash_core -p lora_train -p burn_webgpu_backend
```

This patch does not modify sherpa-rs-sys and does not claim full workspace closure or native GPU runtime completion.

## Patched Areas
- Import closure for ASH_30_AUDIT_STATUS and metric resolution invariant helper.
- HardNegativeReplayBuffer SSOT disambiguation to `crate::hard_negative_replay::AshHardNegativeReplayBuffer`.
- Borrow/type inference/shadowing fixes.
- GPU-SFT config guard field restoration.
- Timing probe device fingerprint drift repair via timing probe seal.
- Move/borrow fixes through clone or precomputed booleans.

## No Silent Guard Weakening
- Runtime model fingerprint validation preserved.
- Current pointer before/after guard validation preserved.
- Device fingerprint matching preserved.
- Hard negative replay records were not converted between replay buffer schemas.

## Local Verification Required
Run on target machine:

```powershell
cargo check -p ash_core -p lora_train -p burn_webgpu_backend
cargo test -p ash_core sft_gpu_obs_07 -- --nocapture
cargo test -p ash_core sft_gpu_run_13 -- --nocapture
```
