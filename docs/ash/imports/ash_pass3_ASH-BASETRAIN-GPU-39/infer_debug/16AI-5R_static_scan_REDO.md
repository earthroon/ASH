# 16AI-5R Static Scan REDO

## 확정

- Source file exists: yes
- Source path: `crates/model_core/src/bin/af16ai5_wrapper_quality_compare.rs`
- Runner scripts exist:
  - `scripts/run_16AI_5R_wrapper_quality_compare.sh`
  - `scripts/run_16AI_5R_wrapper_quality_compare.ps1`

## Required markers
- PASS marker: `chatml_lite_excluded=true`
- PASS marker: `generation_connected_default=false`
- PASS marker: `fallback_cpu_reference=true`
- PASS marker: `attention_native=false`
- PASS marker: `kv_cache_native=false`
- PASS marker: `quality_score`
- PASS marker: `byte_token_leak`
- PASS marker: `special_marker_leak`
- PASS marker: `spaced_korean`
- PASS marker: `high_repetition`
- PASS marker: `weak_word_boundary`
- PASS marker: `best_wrapper`
- PASS marker: `plain,dialogue-ko,instruction-ko`
- PASS marker: `--vocab-limit`
- PASS marker: `--fail-fast`

## 판단불가

- `cargo` is not installed in this execution container, so Rust compile/runtime validation could not be executed here.
- Current checkpoint `tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors` is not present in the uploaded 16AI-4 zip, so generation runtime acceptance remains PENDING.
