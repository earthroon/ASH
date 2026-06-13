# 16AI-QW-38A Bake Report

## Target

`16AI-QW-38A — Reserved Token Raw Logit Attractor Audit / Base LM Head Distribution Seal`

## Baked From

`ash_pass3_16AI-QW-35E-R1_runner_stability_baked.zip`

## Changed Files

- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38A_reserved_attractor.ps1`
- `scripts/summarize_16AI_QW_38A_raw_topk.py`
- `scripts/audit_16AI_QW_38A_lm_head_rows.py`
- `acceptance_reports/16AI-QW-38A_reserved_token_raw_logit_attractor.md`
- `patch_reports/16AI-QW-38A_native_wgpu.diff`
- `target/16AI-QW-38A_static_validation.json`

## Applied Changes

- Added env-gated raw top-k tracing behind `ASH_RAW_TOPK_TRACE=1`.
- Added token metadata loading from tokenizer manifest and generation banlist.
- Added per-step `[16AI-QW-38A][raw_topk]` stderr lines.
- Added `workspace/qw38a_raw_topk_trace.jsonl` JSONL output.
- Added raw top-k summary generation script.
- Added lm_head / embedding row norm audit script for target tokens.
- Added PowerShell runner using `Start-Process` so cargo warnings do not break the runner as PowerShell `NativeCommandError`.

## Non-Mutations

- No safetensors mutation.
- No tokenizer mutation.
- No banlist mutation.
- No LoRA mutation.
- No prompt template default change.
- No sampler default change.

## Validation

Static validation only in this environment. Rust `cargo check` was not run because `cargo` is unavailable in the container.

Run locally:

```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\16AI-QW-38A_model_core_check.log"
cargo check -p runtime 2>&1 | Tee-Object ".\target\16AI-QW-38A_runtime_check.log"
```

Runtime probe:

```powershell
.\scripts\run_16AI_QW_38A_reserved_attractor.ps1
```
