# SFT-GPU-7 Static Validation Result

Status: **PASS_STATIC**

Checks: `38 / 38`

## Checked Items

- [x] `crates/lora_train/src/generation_hygiene.rs` :: `exists`
- [x] `crates/lora_train/src/direct_line_acceptance.rs` :: `exists`
- [x] `crates/lora_train/src/training.rs` :: `exists`
- [x] `crates/lora_train/src/lib.rs` :: `exists`
- [x] `docs/A_SFT_GPU_DIRECT_LINE.md` :: `exists`
- [x] `acceptance_reports/SFT-GPU-7_one_shot_cli_direct_line_acceptance_generation_hygiene_smoke.md` :: `exists`
- [x] `generation_hygiene.rs` :: `GenerationHygieneConfig`
- [x] `generation_hygiene.rs` :: `run_generation_hygiene_smoke`
- [x] `generation_hygiene.rs` :: `count_replacement_chars`
- [x] `generation_hygiene.rs` :: `count_suspicious_byte_markers`
- [x] `generation_hygiene.rs` :: `count_hangul_char_split_patterns`
- [x] `generation_hygiene.rs` :: `max_repeated_char_run`
- [x] `generation_hygiene.rs` :: `max_repeated_bigram_count`
- [x] `generation_hygiene.rs` :: `run_runtime_lora_generation_smoke`
- [x] `generation_hygiene.rs` :: `generation_hygiene_report.json`
- [x] `generation_hygiene.rs` :: `generation_hygiene_report.md`
- [x] `direct_line_acceptance.rs` :: `DirectLineAcceptanceReport`
- [x] `direct_line_acceptance.rs` :: `DirectLineConfigGate`
- [x] `direct_line_acceptance.rs` :: `DirectLineMaskGate`
- [x] `direct_line_acceptance.rs` :: `DirectLineGpuTrainingGate`
- [x] `direct_line_acceptance.rs` :: `DirectLineArtifactGate`
- [x] `direct_line_acceptance.rs` :: `DirectLineRuntimeDeltaGate`
- [x] `direct_line_acceptance.rs` :: `DirectLineGenerationHygieneGate`
- [x] `direct_line_acceptance.rs` :: `build_direct_line_acceptance_report`
- [x] `direct_line_acceptance.rs` :: `write_direct_line_acceptance_report`
- [x] `direct_line_acceptance.rs` :: `direct_line_acceptance.json`
- [x] `direct_line_acceptance.rs` :: `direct_line_acceptance.md`
- [x] `lib.rs` :: `pub mod generation_hygiene;`
- [x] `lib.rs` :: `pub mod direct_line_acceptance;`
- [x] `lib.rs` :: `pub use generation_hygiene`
- [x] `lib.rs` :: `pub use direct_line_acceptance`
- [x] `training.rs` :: `run_generation_hygiene_smoke`
- [x] `training.rs` :: `build_direct_line_acceptance_report`
- [x] `training.rs` :: `write_direct_line_acceptance_report`
- [x] `training.rs` :: `[lora_train][acceptance] running one-shot direct-line acceptance`
- [x] `training.rs` :: `direct_jsonl_sft_gpu7_one_shot_acceptance`
- [x] `training.rs` :: `generation_hygiene_report_json`
- [x] `training.rs` :: `direct_line_acceptance_json`
