# MODELCORE-COMPILE-16 - Full LoRA Dump Runtime Seal

## Purpose

Add a local full runtime seal for LoRA dump generation.

This commit does not modify Rust source. It adds a PowerShell runner and compile/runtime documentation for the full dump gate.

## Changed Files

- scripts/run_lora_dump_full.ps1
- docs/compile/lora_dump_full_runtime_seal.md
- patch_reports/MODELCORE_COMPILE_16_FULL_DUMP_RUNTIME_SEAL.md

## Runtime Script

`scripts/run_lora_dump_full.ps1` performs these steps:

1. Resolve the repository root.
2. Verify the full config exists.
3. Optionally require the smoke summary to exist and report `PASS`.
4. Run `scripts/validate_lora_dump_paths.ps1` against the full config.
5. Verify `training.bridge_dump_only=true`.
6. Verify `bridge.enabled=true`.
7. Verify `training.planned_layers` matches the command argument.
8. Reject accidental smoke-scale full runs.
9. Execute:

```powershell
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_full.json" 6
```

10. Write `target/MODELCORE_COMPILE_16_lora_dump_full.log`.
11. Scan the log for compile/runtime failure patterns.
12. Verify output directories and artifact files exist.
13. Write `target/MODELCORE_COMPILE_16_lora_dump_full_summary.json`.

## Non-Goals

- No Rust source changes.
- No model_core compile repair.
- No lora_train compile repair.
- No config path mutation.
- No smoke runtime mutation.
- No full dump quality scoring.
- No warning hygiene sweep.

## Prohibited Shortcuts Avoided

- Did not claim PASS in the bake environment.
- Did not execute against missing local Windows data paths.
- Did not treat smoke config as full config.
- Did not silently accept smoke-scale max sample values.
- Did not modify configs to fit the bake environment.

## Validation

Local full runtime command:

```powershell
.\scripts\run_lora_dump_full.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3"
```

Strict command requiring prior smoke summary:

```powershell
.\scripts\run_lora_dump_full.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3" -RequireSmokeSummary
```

Expected summary:

```text
target/MODELCORE_COMPILE_16_lora_dump_full_summary.json
status=PASS
```
