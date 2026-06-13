from pathlib import Path
root = Path(__file__).resolve().parents[1]
checks = []
def check(name, cond):
    checks.append((name, bool(cond)))
prof = root / "crates/lora_train/src/lm_head_vocab_atlas_gpu_profiler.rs"
exp = root / "crates/lora_train/src/lm_head_vocab_atlas_gpu_export.rs"
config = root / "crates/lora_train/src/config.rs"
entry = root / "crates/lora_train/src/lm_head_vocab_atlas.rs"
conf_json = root / "configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json"
text_prof = prof.read_text() if prof.exists() else ""
text_exp = exp.read_text() if exp.exists() else ""
text_cfg = config.read_text() if config.exists() else ""
text_entry = entry.read_text() if entry.exists() else ""
text_json = conf_json.read_text() if conf_json.exists() else ""
check("lm_head_vocab_atlas_gpu_profiler.rs exists", prof.exists())
check("lm_head_vocab_atlas_gpu_export.rs exists", exp.exists())
check("GpuVocabAtlasTimingEvent exists", "GpuVocabAtlasTimingEvent" in text_prof)
check("GpuVocabAtlasTimingSummary exists", "GpuVocabAtlasTimingSummary" in text_prof)
check("GpuReadbackDisciplineReport exists", "GpuReadbackDisciplineReport" in text_exp)
check("validate_readback_discipline exists", "validate_readback_discipline" in text_exp)
check("GpuVocabAtlasAdapterExportReport exists", "GpuVocabAtlasAdapterExportReport" in text_exp)
check("validate_gpu_adapter_export exists", "validate_gpu_adapter_export" in text_exp)
check("GpuVocabAtlasTrainStepSealReport exists", "GpuVocabAtlasTrainStepSealReport" in text_exp)
check("adapter_manifest_written report exists", "adapter_manifest_written" in text_exp)
check("adapter_model_written report exists", "adapter_model_written" in text_exp)
check("PASS_GPU_PARALLEL_TRAIN_STEP_SEAL exists", "PASS_GPU_PARALLEL_TRAIN_STEP_SEAL" in text_exp)
check("logits_readback=false report exists", "logits_readback: false" in text_exp or "logits_readback=false" in text_entry)
check("full_weight_readback=false report exists", "full_weight_readback: false" in text_exp or "full_weight_readback=false" in text_entry)
check("Gpu export config exists", "LmHeadVocabAtlasGpuExportConfig" in text_cfg)
check("Readback discipline config exists", "LmHeadVocabAtlasReadbackDisciplineConfig" in text_cfg)
check("GPU timing profiler config exists", "LmHeadVocabAtlasGpuTimingProfilerConfig" in text_cfg)
check("config JSON export block exists", '"export"' in text_json and '"adapter_format"' in text_json)
check("config JSON readback discipline block exists", '"readback_discipline"' in text_json)
check("config JSON gpu timing profiler block exists", '"gpu_timing_profiler"' in text_json)
check("entry calls export", "export_gpu_vocab_atlas_adapter" in text_entry)
check("entry writes G reports", "write_gpu_vocab_atlas_g_reports" in text_entry)
check("acceptance report exists", (root / "acceptance_reports/SFT-GPU-8H-G_timing_profiler_adapter_export_no_readback.md").exists())
failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if failed:
    raise SystemExit(f"[FAIL_STATIC] SFT-GPU-8H-G failed checks: {failed}")
print(f"[PASS_STATIC] SFT-GPU-8H-G timing profiler / adapter export / no-readback discipline ({len(checks)} checks)")
