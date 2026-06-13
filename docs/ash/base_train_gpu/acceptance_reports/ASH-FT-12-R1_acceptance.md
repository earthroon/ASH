# ASH-FT-12-R1 Acceptance

## Checks

- `crates/model_core/src/lib.rs` contains `pub mod ash_ft12_shadow_candidate_runtime_bind_dryrun;`
- `lib.rs` contains FT-12 `pub use` exports
- FT-12 bin imports via direct module path
- Cargo bin target exists
- no runtime artifacts are packaged
- no `target/` output is packaged

## Expected compile closure

```powershell
cargo run --bin ash_ft12_shadow_candidate_runtime_bind_dryrun -- --help
```

Then run the original FT-12 command.
