# BUILD-ENV-01 Recheck Commands

Run from the repository root after Rust is installed.

```bash
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/provision_rust_toolchain.py --local-provision-check
python3 tools/run_build_00_r1_cargo_environment_rerun.py
```

Then execute the decode guard chain if Cargo check or tokenizer_core-only execution is available.

```bash
cargo test -p tokenizer_core --test decode_run_00_runtime_guard_chain
cargo run -p tokenizer_core --bin decode_run_00_runtime_guard_chain
```

Expected branches:

```text
1. Toolchain unavailable -> BUILD-ENV-02 or external CI execution
2. Toolchain available + sherpa-rs path failure -> BUILD-00-R2
3. Toolchain available + tokenizer_core compile failure -> BUILD-01
4. Guard chain executed PASS -> DECODE-RUN-01
5. Guard chain executed mismatch -> DECODE-RUN-00-R1
```
