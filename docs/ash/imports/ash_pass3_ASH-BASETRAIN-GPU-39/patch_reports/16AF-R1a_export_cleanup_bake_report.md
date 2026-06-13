# 16AF-R1a Export Cleanup Bake Report

## SSOT

- Parent: 16AF-R1 storage3 split BGL bake
- Scope: compile fix only
- Generation path: not connected

## Fixed

`crates/burn_webgpu_backend/src/lib.rs` still exported the removed monolithic shader constant:

```rust
SHADER_NATIVE_ATLAS_FFN_16AF
```

16AF-R1 split the native FFN shader into four pass-local WGSL constants:

```rust
SHADER_NATIVE_ATLAS_FFN_16AF_GATE
SHADER_NATIVE_ATLAS_FFN_16AF_UP
SHADER_NATIVE_ATLAS_FFN_16AF_SWIGLU
SHADER_NATIVE_ATLAS_FFN_16AF_DOWN
```

The public export list now matches the split shader SSOT.

## Not changed

- `native_atlas_ffn.rs` compute pass logic unchanged
- storage buffer count split unchanged
- runtime parity runner unchanged
- generation integration remains locked

## Local validation required

Run:

```powershell
cargo run --manifest-path crates/model_core/Cargo.toml --bin af16r_runtime_parity -- --spec "specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" --checkpoint ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors" --layer 0 --threshold 0.001
```

Expected: compile should pass this export error and proceed to runtime validation.
