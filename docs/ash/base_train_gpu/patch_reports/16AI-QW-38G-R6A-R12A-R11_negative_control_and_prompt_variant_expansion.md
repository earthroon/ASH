# 16AI-QW-38G-R6A-R12A-R11 — Negative Control and Prompt Variant Expansion

## Status
BAKED_STATIC

## Intent
This patch expands the guarded attenuation validation surface after R10A verified the default-off / explicit-enable / preflight-fallback switch hygiene.

## Scope
- Adds R11 artifact-driven validation runner.
- Reads R10A guarded runtime smoke receipt and R10 candidate registry.
- Reuses R9 primary repeat validation as the primary repeat SSOT.
- Writes prompt variant and negative control matrices.
- Does not generate missing validation prompts silently.
- If prompt variant or negative control sets are absent, records explicit SKIPPED results and blocks HIGH confidence.

## Guard
- runtime_default_apply: false
- requires_explicit_enable: true
- production_safe_confirmed: false
- root_cause_confirmed: false
- checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask unchanged.
