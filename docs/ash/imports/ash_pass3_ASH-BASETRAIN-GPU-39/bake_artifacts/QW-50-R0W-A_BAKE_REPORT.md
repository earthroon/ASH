# QW-50-R0W-A Bake Report

Status: PASS_STATIC

## Scope
- Rust-owned DecodeState generated-prefix duplication inspector added.
- Python analyzer/validator/probe was not added.
- Python remains injector-only by contract.
- Prefix fix was not applied.

## Runtime
- cargo check: NOT RUN - cargo unavailable in this environment.
- Vulkan runtime inference: NOT RUN - cargo unavailable in this environment.
- Static validation: PASS_STATIC.

## Mutation Policy
- decode policy mutation: false
- guard policy mutation: false
- LoRA scale mutation: false
- model weight mutation: false
- token ban added: false
- prefix fix applied: false
- python trace mutation: false
- python receipt mutation: false

## Added Rust Surfaces
- crates/model_core/src/decode_prefix_inspector.rs
- crates/runtime/src/infer/qw50_r0w_a_prefix_trace.rs
- crates/runtime/src/bin/qw50_r0w_a_prefix_probe.rs
- crates/runtime/src/bin/qw50_r0w_a_validate.rs

## Runtime Command
```powershell
cargo build --release --manifest-path .\crates\runtime\Cargo.toml --bin qw50_r0w_a_prefix_probe
cargo build --release --manifest-path .\crates\runtime\Cargo.toml --bin qw50_r0w_a_validate
```
