# SFT-GPU-4 Static Validation Result

- status: `PASS_STATIC`
- passed: `23/23`

## Gates
- [x] gpu smoke module exists
- [x] WGPU backend required
- [x] lm_head direct-line validation exists
- [x] module_lora artifact validation exists
- [x] SFT mask stats validate before smoke
- [x] IGNORE_INDEX filtered before CE
- [x] response-only selected batch used
- [x] real base lm_head weight accepted
- [x] Burn autodiff loss backward exists
- [x] optimizer step exists
- [x] LoRA B norm change gate exists
- [x] NaN Inf finite gate exists
- [x] CPU training steps recorded zero
- [x] training.rs routes response-only artifact log to module_lora/lm_head
- [x] training.rs loads full checkpoint lm_head weights
- [x] training.rs calls smoke runner
- [x] training.rs removed SFT-GPU-3 deferred bail
- [x] training.rs writes smoke checkpoint manifest entry
- [x] lib exports gpu smoke module
- [x] docs updated
- [x] acceptance report exists
- [x] no duplicated direct report fragment corruption
- [x] only expected direct eval_entries declarations

## Execution Limitation

This sandbox does not provide `cargo`/`rustc`, so Rust compilation and runtime WGPU smoke execution were not run here. The baked package is statically validated only; run the cargo command in the target Windows/Rust/WGPU environment for final PASS.