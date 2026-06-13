# ASH-BASETRAIN-GPU-37R-R1 Bake Report

## Summary

Fixed Rust compile error E0106 in the 37R parity gate binary by adding an explicit lifetime to `str_value`.

## Changed

```rust
fn str_value(value: &Value, key: &str) -> Option<&str>
```

became:

```rust
fn str_value<'a>(value: &'a Value, key: &str) -> Option<&'a str>
```

The returned `&str` is borrowed from `value`, not from `key`.

## Not Changed

- GPU readback parity logic
- u32 word exact parity policy
- CPU reference comparison contract
- forward adoption guard
- optimizer guard
- weight mutation guard

## Container Validation

The container environment does not include `cargo/rustc`, so local cargo build was not executed here. Static source inspection confirms the lifetime signature was rewritten.
