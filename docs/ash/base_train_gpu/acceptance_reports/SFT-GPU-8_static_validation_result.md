# SFT-GPU-8 Static Validation Result

## Status

PASS_STATIC 25 / 25

## Checked

- `crates/lora_train/src/quality_fixture.rs`
- `crates/lora_train/src/base_vs_lora_report.rs`
- `crates/lora_train/src/lib.rs`
- `crates/lora_train/src/training.rs`
- `fixtures/sft_gpu_quality_fixture_ko.json`
- `docs/A_SFT_GPU_DIRECT_LINE.md`
- `acceptance_reports/SFT-GPU-8_base_vs_lora_sample_report_quality_eval_fixture_pack.md`
- `acceptance_reports/SFT-GPU-8_compile_result.md`

## Gates

- [x] quality fixture pack type exists
- [x] default Korean quality fixture file exists
- [x] greedy decode / KV reset fixture guards exist
- [x] base-vs-lora report type exists
- [x] runtime generation smoke path is reused
- [x] base output is recorded
- [x] LoRA output is recorded
- [x] replacement character metric exists
- [x] suspicious byte marker metric exists
- [x] Hangul char-split metric exists
- [x] repetition metric exists
- [x] JSON/Markdown sample reports are declared
- [x] JSON/Markdown summary reports are declared
- [x] fixture copy path is emitted
- [x] `lib.rs` exports the new modules
- [x] `training.rs` calls `run_base_vs_lora_quality_eval()` after SFT-GPU-7 acceptance
- [x] checkpoint/eval entries record SFT-GPU-8 output paths
- [x] resume source updated to `direct_jsonl_sft_gpu8_base_vs_lora_quality_eval`

## Runtime Status

Not executed in this sandbox because `cargo`, `rustc`, and WGPU runtime access were unavailable.
