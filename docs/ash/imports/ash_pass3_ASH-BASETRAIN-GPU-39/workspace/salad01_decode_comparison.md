# SALAD-01 Decode Comparison

- Patch: `16AI-QW-38G-R6A-SALAD-01`
- Baseline: `CURRENT_DEFAULT`
- Safe profile: `SAFE_KOREAN_STABLE_V1`
- Runtime inference: not executed in bake container because `cargo`/`rustc` are unavailable.

## Static Result

The code path now clamps decode policy through `derive_gate()` before runtime execution config is built. Local replay must compare same prompt/seed/model between `CURRENT_DEFAULT`, `DEBUG_GREEDY_BASELINE`, and `SAFE_KOREAN_STABLE_V1`.

## Expected Local Replay Pass

- `safe_word_salad_score < baseline_word_salad_score`
- `MAX_NEW_TOKENS` stop decreases
- sentence/EOS/double-newline stop increases
- mutation flags remain false
