# 16AI-QW-38G-R6A-R12A-R10 — Guarded Attenuation Runtime Candidate

## Status
STATIC_BAKED_GUARDED_ATTENUATION_RUNTIME_CANDIDATE

## What changed
- Added a model_core runtime attenuation candidate registry module.
- Added default-off candidate constants for `HEAD2_TARGET_DIRECTION_ORTHOGONAL_ONLY`.
- Added preflight data structures and preflight check helper.
- Added R10 runner that reads R9 receipt and writes registry/guard/preflight/limited-scope artifacts.

## Guard
- runtime_default_apply: false
- requires_explicit_enable: true
- negative_control_missing warning preserved
- prompt_variant_missing warning preserved
- checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask unchanged
