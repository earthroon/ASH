# BUILD-ENV-00 Rust Toolchain Installation Instructions

Patch: `16AI-QW-38G-R6A-BUILD-ENV-00`  
Domain SSOT: `en_to_ko_translation_subtitle_machine`

This document is an instruction artifact only. It does not claim Rust was installed.
Run the commands in an environment where installing Rust is allowed, then re-run the probe.

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

## Optional components

```bash
rustup component add rust-src
rustup component add llvm-tools-preview
```

`rust-src` and `llvm-tools-preview` are not required for BUILD-ENV-00. Keep them optional unless a later native/runtime/profiling patch requires them.
