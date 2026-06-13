# 16AI-QW-38G-R6A-BUILD-00
## Cargo Workspace Check / Rust Compilation Readiness Seal

## 1. 확정

- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Preceded by: `16AI-QW-38G-R6A-CLOSURE-04`
- Closure-04 static integrity preflight: `True`
- Cargo available in bake environment: `False`
- Rustc available in bake environment: `False`
- Build readiness status: `BLOCKED_ENVIRONMENT`

This BUILD-00 bake does **not** claim Cargo compile PASS because `cargo` and `rustc` were not available in the bake environment.

## 2. 실행 시도

| Command | Executed | Status/Reason |
|---|---:|---|
| `cargo metadata --format-version 1` | `False` | `cargo_not_found` |
| `cargo check --workspace --all-targets` | `False` | `cargo_not_found` |
| `cargo test --workspace --no-run` | `False` | `cargo_not_found` |
| `cargo fmt --all -- --check` | `False` | `cargo_not_found` |

## 3. Static crate classification

- Workspace members: `17`
- Default/active members: `15`
- Legacy non-default members: `1`
- Other non-default members: `1`
- Static path dependency errors: `1`

`cargo check --workspace --all-targets` includes non-default workspace members. This report records that fact instead of silently excluding legacy crates.

## 4. 명시적 미수행

- runtime decode: `false`
- model forward: `false`
- sampling: `false`
- subtitle export: `false`
- translation quality eval: `false`
- performance benchmark: `false`

## 5. 산출물

- `workspace/build_00_cargo_metadata.json`
- `workspace/build_00_cargo_check_report.json`
- `workspace/build_00_crate_classification_report.json`
- `workspace/build_00_compile_repair_log.json`
- `workspace/build_00_static_build_receipt.json`
- `tools/run_build_00_cargo_checks.py`

## 6. Next

Recommended next patch: `16AI-QW-38G-R6A-BUILD-00-R1` after running in a Rust/Cargo-enabled environment.
