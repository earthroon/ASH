# 16AI Quality Matrix Bake Report

## SSOT

- Prior seal: 16AF-G5 real prompt/wrapper CPU reference and native FFN candidate output match PASS.
- Native FFN is excluded as the primary suspect for current generation quality issues.
- 16AI shifts the investigation to tokenizer, prompt wrapper, and sampling/conditioning.
- generation_connected_default remains false.
- CPU reference fallback remains preserved.
- attention_native=false and kv_cache_native=false remain unchanged.

## Added

- `crates/model_core/src/bin/af16ai_quality_matrix.rs`
- `scripts/run_16AI_quality_matrix.ps1`
- `scripts/run_16AI_quality_matrix.sh`

## Runner modes

- `--mode tokenizer`: fast tokenizer/wrapper roundtrip audit only.
- `--mode generation`: CPU reference vs native FFN candidate generation compare for the selected wrappers/sampling presets.
- `--mode all`: tokenizer audit plus generation matrix.

## Default safety

The default mode is `tokenizer` so the runner does not accidentally launch a multi-hour CPU/native generation matrix.
Generation mode must be requested explicitly with `--mode generation` or `--mode all`.

## Output files

- `infer_debug/16AI_quality_matrix.json`
- `infer_debug/16AI_quality_matrix.md`
- `acceptance_reports/16AI_acceptance.md`

## Toolchain status

The bake environment did not contain `cargo`/`rustc`, so local compile/runtime validation is pending.
