# ASH-BASETRAIN-GPU-37R-R1 Acceptance

## Lifetime Specifier Buildfix

- Patch: `ASH-BASETRAIN-GPU-37R-R1`
- Base: `ASH-BASETRAIN-GPU-37R`
- Scope: compile buildfix only
- Target file: `crates/base_train/src/bin/ash_basetrain_gpu_37r_selected_group_row_block_multi_workgroup_reduction_readback_parity_gate.rs`

## Fix

`str_value` now binds its returned `&str` lifetime to the `serde_json::Value` input only:

```rust
fn str_value<'a>(value: &'a Value, key: &str) -> Option<&'a str> {
    value.get(key).and_then(Value::as_str)
}
```

## Contract

- No reduction parity logic change
- No forward adoption
- No optimizer
- No weight mutation
- No tolerance widening
- No receipt schema adoption change

## Expected local command

```powershell
cargo build -p base_train --bin ash_basetrain_gpu_37r_selected_group_row_block_multi_workgroup_reduction_readback_parity_gate
```
