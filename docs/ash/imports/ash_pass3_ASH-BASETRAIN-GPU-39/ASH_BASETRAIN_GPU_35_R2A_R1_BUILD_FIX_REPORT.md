# ASH-BASETRAIN-GPU-35-R2A-R1 Build Fix Report

## Fixed compile error

Source compile error:

```txt
error[E0277]: the trait bound `Value: From<i128>` is not satisfied
```

Cause:

```rust
probe.byte_len_delta_from_shape_dtype.map(Value::from).unwrap_or(Value::Null)
```

`serde_json::Value` does not implement `From<i128>`. The delta field is diagnostic detail only, so R1 serializes the i128 delta as a lossless decimal string when present.

Fixed expression:

```rust
probe.byte_len_delta_from_shape_dtype
    .map(|value| Value::String(value.to_string()))
    .unwrap_or(Value::Null)
```

## Semantic boundary

- PATCH_ID unchanged: `ASH-BASETRAIN-GPU-35-R2A`
- Package revision: `35-R2A-R1`
- Logic change: compile-only serialization fix
- No operator manifest creation
- No target manifest write
- No GPU buffer allocation
- No selected group weight load
- No backward
- No optimizer
- No safetensors mutation

## Runtime note

Container cargo/rustc execution was not available here. User local cargo build/run is required.
