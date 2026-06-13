# 16AI-6-0 Static Scan

## 확정

- Source file exists: yes
- Source path: `crates/model_core/src/bin/af16ai6_0_fragmentation_baseline.rs`
- Runner scripts exist:
  - `scripts/run_16AI_6_0_fragmentation_baseline.sh`
  - `scripts/run_16AI_6_0_fragmentation_baseline.ps1`

## Required markers

- PASS marker: `fragmentation_baseline=true`
- PASS marker: `assembly_mode=off`
- PASS marker: `generation=false`
- PASS marker: `checkpoint_required=false`
- PASS marker: `chatml_lite_excluded=true`
- PASS marker: `plain,dialogue-ko,instruction-ko`
- PASS marker: `suspicious_char_split`
- PASS marker: `spaced_korean`
- PASS marker: `wrapper_label_fragmented`
- PASS marker: `fragmentation_score`
- PASS marker: `quality_score`
- PASS marker: `token_path`
- PASS marker: `char_analysis`
- PASS marker: `--case-file`
- PASS marker: `--emit-token-path`
- PASS marker: `--emit-char-analysis`
- PASS marker: `--fail-fast`

## 판단불가

- `cargo` is not installed in this execution container, so Rust compile/runtime validation could not be executed here.
- 16AI-6-0 does not require checkpoint or generation runtime; actual tokenizer baseline values remain PENDING until the binary is run in the user's Rust environment.
