# ASH-4 Bake Report

## Status
BAKED

## Scope
Baked the Rust-native Curriculum Router / target module planner into `crates/ash_core`.

## Added
- `crates/ash_core/src/curriculum.rs`
- `crates/ash_core/src/bin/ash_curriculum_audit.rs`
- `crates/ash_core/tests/ash_4_curriculum_router.rs`
- `acceptance_reports/ASH-4_curriculum_router.md`

## Contract
- `ash_core` routes training samples to capability ids and target module plans.
- `ash_core` does not execute LoRA training.
- `ash_core` does not call WGPU/Burn/runtime/lora_train.
- Python validator is forbidden.

## Expected Rust commands
```powershell
cargo test -p ash_core ash_4_curriculum_router
cargo run -p ash_core --bin ash_curriculum_audit
```

Expected audit log:
```txt
[ash_core][ASH-4] PASS_ASH_CURRICULUM_ROUTER
```
