# ASH-BASETRAIN-GPU-35-R2C-R1 Buildfix Report

## Status

Buildfix baked.

## Source diagnostic

`locator_tile()` requires `serde_json::Value` for `extra_a_value`, but `EXPECTED_GROUP_ID` was passed as `&str`.

```rust
"expected_selected_group_id", EXPECTED_GROUP_ID
```

## Fix

```rust
"expected_selected_group_id", Value::from(EXPECTED_GROUP_ID)
```

The unused parentheses warning in `confidence()` was also removed.

## Contract

No semantic change.

- No operator manifest write
- No target manifest write
- No selected group manifest materialization
- No weight load
- No GPU buffer allocation
- No backward
- No optimizer
- No safetensors mutation
