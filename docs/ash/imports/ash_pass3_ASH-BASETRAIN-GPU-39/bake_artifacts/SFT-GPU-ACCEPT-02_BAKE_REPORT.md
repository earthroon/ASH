# SFT-GPU-ACCEPT-02 Bake Report

## Patch

SFT-GPU-ACCEPT-02 — Generation Hygiene Subprocess Isolation / Native Crash Receipt Seal

## SSOT

- Acceptance receipt: `generation_hygiene_acceptance_receipt.json`
- Child report: `generation_hygiene_report.json`
- Child logs: `generation_hygiene_child_stdout.log`, `generation_hygiene_child_stderr.log`
- Child config snapshot: `generation_hygiene_child_config.json`

## Implemented

- Added subprocess isolation path for generation hygiene acceptance.
- Added child CLI mode: `--generation-hygiene-child --config <path> --runtime-attachment <path> --artifact-dir <path>`.
- Parent process now spawns a generation hygiene child when `generation_hygiene_acceptance.isolation_mode = "subprocess"`.
- Parent writes/captures child stdout/stderr logs.
- Parent classifies Windows native crash code `0xc0000005` / `-1073741819` as `windows_status_access_violation`.
- Parent creates a synthetic generation hygiene failure report if the child crashes before writing a report.
- Acceptance receipt now records subprocess metadata:
  - `isolation_mode`
  - `parent_survived`
  - `child_spawned`
  - `child_exit_code`
  - `native_crash_detected`
  - `native_crash_kind`
  - `child_timed_out`
  - child report/log/config paths
- Native child crash maps to `native_crashed_isolated` and preserves the adapter artifact.
- Downstream base-vs-LoRA quality eval is skipped after child native crash / timeout to avoid re-entering unstable native generation in the parent process.
- Added skipped quality eval report writer for post-acceptance instability.
- Added regression test file: `crates/lora_train/tests/generation_hygiene_subprocess_isolation.rs`.
- Updated config defaults and smoke config with subprocess isolation controls.

## Config additions

```json
{
  "generation_hygiene_acceptance": {
    "isolation_mode": "subprocess",
    "child_timeout_ms": 120000,
    "preserve_artifact_on_child_crash": true,
    "native_crash_is_soft_acceptance_failure": true,
    "write_native_crash_receipt": true,
    "max_child_retry": 0
  }
}
```

## Validation

Cargo validation was not executed in this environment because `cargo` is not installed in the container. Static file/bracket sanity checks were performed on modified Rust files.

## Expected runtime behavior

```txt
[lora_train][acceptance] spawning generation hygiene child timeout_ms=120000 ...
[lora_train][acceptance_child] exit_code=0xc0000005 native_crash=true kind=windows_status_access_violation timed_out=false
[lora_train][acceptance] child crash isolated; parent_survived=true ...
[lora_train][quality_eval] skipped_after_acceptance_child_unstable native_crash=true timed_out=false artifact_preserved=true
```

## Final status

Baked with source changes and receipt/test scaffolding. Local Cargo build/test must be run on the user machine.
