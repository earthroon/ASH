# 16AI-QW-BUILD-05 — R12A-R1 Infer Binary Target Resolution / Runner Artifact Handoff Seal

## Status
STATIC_PASS_INFER_BINARY_TARGET_RESOLUTION_BAKED

## SSOT
- Previous build status: cargo build passed, then runner failed at `infer_only.exe not found`.
- Failure class: binary artifact handoff mismatch, not Rust compile failure.
- Old runner expectation: `target/debug/infer_only.exe` or `target/release/infer_only.exe`.
- Restored target contract: runtime example target `infer_only`, release-first path `target/release/examples/infer_only.exe`.

## Changes
- Replaced R12A-R1 runner workspace `cargo build` handoff with explicit `cargo build --release --manifest-path .\crates\runtime\Cargo.toml --example infer_only`.
- Runner now resolves `target/release/examples/infer_only.exe` first and `target/debug/examples/infer_only.exe` second.
- Runner writes BUILD-05 handoff receipt, binary inventory, and binary handoff manifest before execution.
- Runner separates build pass, binary found, run started, and run exit code.
- Runner preserves R12A-R1 hidden capture env gates and mutation prohibitions.

## Guard
- R12A-R1 hidden capture code unchanged.
- native_wgpu final_norm/projection logic unchanged.
- tokenizer/safetensors/lm_head/final_norm/ban_mask unchanged.
- No fake success when binary is missing.

## Next
Run:

```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R1_trace_capture_expansion.ps1 -Build
```

If the infer-only binary runs, evaluate `workspace/qw38g_r6a_r12a_r1_trace_capture_expansion_receipt.json` for capture coverage.
