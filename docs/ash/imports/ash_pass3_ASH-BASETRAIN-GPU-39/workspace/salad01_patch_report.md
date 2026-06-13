# 16AI-QW-38G-R6A-SALAD-01 Patch Report

## 확정

`SALAD-01` is baked as a non-destructive inference decode stability patch. It does not mutate checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask files.

## Applied Code Paths

- Added `crates/ash_core/src/decode_stability.rs` with decode profiles and word-salad audit primitives.
- Exported the decode stability module from `ash_core`.
- Wired `SAFE_KOREAN_STABLE_V1` into `derive_gate()` so runtime generation policy is clamped before execution config construction.
- Exposed `decode_profile` and `word_salad_guard` through the runtime `AshGate` event.
- Tightened decision-level decode defaults to the stable profile ceiling.

## 추정

This should reduce sampling-driven salad by lowering temperature/top_p/top_k, increasing repeat penalty, expanding repeat window, and adding double-newline stop. It will not fix greedy-mode salad caused by tokenizer/QWave/SFT/logit drift.

## 판단불가

Local generation quality is not measured in this bake container because cargo/rust runtime is unavailable. Runtime replay on the Windows project directory is required for score comparison.
