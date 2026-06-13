# BUILD-ENV-00 Recheck Commands

Run from the repository root after Rust is installed.

```bash
python3 tools/provision_rust_toolchain.py --verify --emit-receipt
python3 tools/run_build_00_r1_cargo_environment_rerun.py
```

Expected next branches:

```text
1. Toolchain available + cargo check passes -> 16AI-QW-38G-R6A-DECODE-18
2. Toolchain available + sherpa-rs path failure -> 16AI-QW-38G-R6A-BUILD-00-R2
3. Toolchain still unavailable -> keep BUILD-ENV-00 as BLOCKED_TOOLCHAIN_UNAVAILABLE
```
