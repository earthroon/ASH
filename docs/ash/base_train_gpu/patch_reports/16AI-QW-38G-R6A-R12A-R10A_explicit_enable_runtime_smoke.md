# 16AI-QW-38G-R6A-R12A-R10A — Explicit Enable Runtime Smoke

## Status
BAKED_STATIC

## Scope
- Adds R10A explicit-enable runtime switch smoke runner.
- Verifies default-off, explicit-apply, preflight-mismatch, and fallback contract artifacts.
- Does not enable attenuation by default.
- Does not modify checkpoint, tokenizer, safetensors, lm_head, final_norm, or ban mask.

## Files
- `scripts/run_16AI_QW_38G_R6A_R12A_R10A_explicit_enable_runtime_smoke.ps1`
- `crates/model_core/src/qw38g_r6a_r12a_runtime_attenuation_candidate.rs`

## Guard
R10A is a guarded switch smoke. It does not claim production safety or root-cause confirmation.
