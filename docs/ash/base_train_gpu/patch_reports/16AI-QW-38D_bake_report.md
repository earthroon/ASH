# 16AI-QW-38D Bake Report

## Patch
`16AI-QW-38D — Hidden State to Reserved Row Projection Audit / Final Norm Direction Seal`

## Base
`ash_pass3_16AI-QW-38A_reserved_attractor_baked.zip`

## Files Changed / Added
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38D_hidden_projection.ps1`
- `scripts/summarize_16AI_QW_38D_hidden_projection.py`
- `acceptance_reports/16AI-QW-38D_hidden_projection_audit.md`
- `patch_reports/16AI-QW-38D_native_wgpu.diff`
- `target/16AI-QW-38D_static_validation.json`

## Implementation Notes
- Adds env-gated hidden projection trace after native vocab atlas raw top-k collection.
- Materializes the final last-hidden vector only when `ASH_HIDDEN_PROJECTION_TRACE=1`.
- Compares final hidden vector against lm_head rows for token_id 13, EOS, masked top1, chosen token, and raw top-k candidates.
- Writes JSONL trace and postprocessed summary.
- Does not mutate model weights, tokenizer, safetensors, banlist, or prompt defaults.

## Validation
Static validation only. Cargo is unavailable in the container environment, so local `cargo check` is required.

## Local Check
```powershell
cargo check -p model_core 2>&1 | Tee-Object ".\target\16AI-QW-38D_model_core_check.log"
cargo check -p runtime 2>&1 | Tee-Object ".\target\16AI-QW-38D_runtime_check.log"
```

## Runtime
```powershell
.\scripts\run_16AI_QW_38D_hidden_projection.ps1
```
