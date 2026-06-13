# BUILD-ENV-01 Next Rerun Handoff

Patch: `16AI-QW-38G-R6A-BUILD-ENV-01`  
Domain SSOT: `en_to_ko_translation_subtitle_machine`

## Local/Cargo probe

```bash
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/provision_rust_toolchain.py --local-provision-check
```

## BUILD-00-R1 rerun

```bash
python3 tools/run_build_00_r1_cargo_environment_rerun.py
```

## Decode QA/RUN Rust tests

```bash
cargo test -p tokenizer_core --test decode_qa_05_control_token_guard
cargo test -p tokenizer_core --test decode_qa_06_byte_utf8_guard
cargo test -p tokenizer_core --test decode_qa_07_linebreak_guard
cargo test -p tokenizer_core --test decode_qa_08_degeneration_guard
cargo test -p tokenizer_core --test decode_qa_09_termination_guard
cargo test -p tokenizer_core --test decode_qa_10_subtitle_smoke
cargo test -p tokenizer_core --test decode_qa_11_regression_matrix
cargo test -p tokenizer_core --test decode_qa_12_quality_closure
cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain
```

## RUN-00 bin execution

```bash
cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain
```

## Status policy

```text
CI template generated does not mean CI executed.
Cargo unavailable does not mean compile failed.
Rust guard tests not run must remain NOT_RUN_CARGO_UNAVAILABLE.
Python orchestration must not substitute Rust guard results.
```
