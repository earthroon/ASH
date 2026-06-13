# BUILD-ENV-01 Rust Toolchain Installation Instructions

Patch: `16AI-QW-38G-R6A-BUILD-ENV-01`  
Domain SSOT: `en_to_ko_translation_subtitle_machine`

This document is an instruction artifact only. It does not claim Rust was installed.
Install Rust in a local or CI environment, then re-run the probes and BUILD-00-R1.

## Windows PowerShell

```powershell
winget install --id Rustlang.Rustup -e
rustup toolchain install stable
rustup default stable
rustup component add rustfmt
rustup component add clippy
cargo --version
rustc --version
```

## macOS / Linux

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup toolchain install stable
rustup default stable
rustup component add rustfmt
rustup component add clippy
cargo --version
rustc --version
```

## Important boundary

Python may probe the environment and write receipts. Python must not replace Rust decode guard execution.
