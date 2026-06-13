# BUILD-ENV-02 External Runner Execution Handoff

## SSOT
- domain_ssot: `en_to_ko_translation_subtitle_machine`
- current status: `EXTERNAL_RUNNER_TEMPLATE_READY_NOT_EXECUTED`
- runtime_ready_decode_confirmed: `false`

## Execute in Cargo/Rust environment

```bash
rustc --version
cargo --version
rustup show
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/run_build_00_r1_cargo_environment_rerun.py
cargo test -p tokenizer_core --test decode_qa_05_control_token_guard
cargo test -p tokenizer_core --test decode_qa_06_byte_utf8_guard
cargo test -p tokenizer_core --test decode_qa_07_linebreak_guard
cargo test -p tokenizer_core --test decode_qa_08_degeneration_guard
cargo test -p tokenizer_core --test decode_qa_09_termination_guard
cargo test -p tokenizer_core --test decode_qa_10_subtitle_smoke
cargo test -p tokenizer_core --test decode_qa_11_regression_matrix
cargo test -p tokenizer_core --test decode_qa_12_quality_closure
cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain
cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain
```

## Promotion rules

- PASS external runner and guard chain: `DECODE-RUN-01`
- `sherpa-rs` missing path: `BUILD-00-R2`
- tokenizer_core compile error: `BUILD-01`
- guard mismatch: `DECODE-RUN-00-R1`

Do not set `runtime_ready_decode_confirmed = true` without executed cargo test and cargo run receipts.
