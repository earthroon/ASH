# MODELCORE-COMPILE-15 - Smoke Dump Runtime Seal

## Purpose

Add the smoke LoRA dump runtime seal without changing Rust source code.

## Changed Files

- scripts/run_lora_dump_smoke.ps1
- docs/compile/lora_dump_smoke_runtime_seal.md
- patch_reports/MODELCORE_COMPILE_15_SMOKE_DUMP_RUNTIME_SEAL.md

## Runtime Command

```powershell
.\scripts\run_lora_dump_smoke.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3"
```

Direct equivalent:

```powershell
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6
```

## Script Behavior

- Validates the smoke config paths through `scripts/validate_lora_dump_paths.ps1`.
- Checks that smoke limits remain small.
- Runs the LoRA dump smoke command.
- Captures the runtime log to `target/MODELCORE_COMPILE_15_lora_dump_smoke.log`.
- Scans the log for failure patterns.
- Verifies that at least one smoke artifact file exists under the configured output roots.
- Writes `target/MODELCORE_COMPILE_15_lora_dump_smoke_summary.json` on pass.

## Non-Goals

- No Rust source changes.
- No full dump execution.
- No full dataset validation.
- No artifact quality scoring.
- No performance baseline.
- No config rewrite.

## Pass Criteria

```text
- path validation passes
- cargo run exits 0
- smoke log has no failure pattern
- smoke artifact file count > 0
- smoke summary JSON status=PASS
```

## Bake Environment Status

```text
STATUS: UNVERIFIED_IN_BAKE_ENVIRONMENT
```

The bake environment cannot verify the Windows absolute model/data paths or run the local Cargo runtime. Local execution is the SSOT for PASS.

## Next Commit

```text
MODELCORE-COMPILE-16: Full LoRA Dump Runtime Seal
```
