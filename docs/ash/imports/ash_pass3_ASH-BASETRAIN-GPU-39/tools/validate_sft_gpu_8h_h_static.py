from pathlib import Path
root = Path(__file__).resolve().parents[1]
checks = []
def need(path, text=None):
    p = root / path
    ok = p.exists()
    if ok and text is not None:
        ok = text in p.read_text(encoding='utf-8', errors='ignore')
    checks.append((ok, path, text))
need('crates/lora_train/src/lm_head_runtime_delta_verify.rs')
for text in [
    'LmHeadRuntimeDeltaVerifyRequest',
    'LmHeadRuntimeDeltaVerifyReport',
    'run_lm_head_runtime_delta_verify_from_export',
    'PASS_RUNTIME_DELTA_VERIFY',
    'delta_norm',
    'max_abs_delta',
    'require_nonzero_delta',
    'no_silent_fallback',
    'no_target_auto_remap',
    'logits_dumped_to_report: false',
]:
    need('crates/lora_train/src/lm_head_runtime_delta_verify.rs', text)
for text in [
    'RuntimeDeltaVerifyConfig',
    'runtime_delta_verify: Option<RuntimeDeltaVerifyConfig>',
]:
    need('crates/lora_train/src/config.rs', text)
need('crates/lora_train/src/lib.rs', 'pub mod lm_head_runtime_delta_verify;')
need('crates/lora_train/src/lm_head_vocab_atlas.rs', 'run_lm_head_runtime_delta_verify_from_export')
need('configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json', '"runtime_delta_verify"')
need('acceptance_reports/SFT-GPU-8H-H_runtime_delta_verify.md', 'PASS_RUNTIME_DELTA_VERIFY')
failed = [c for c in checks if not c[0]]
for ok, path, text in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {path}" + (f" contains {text!r}" if text else ' exists'))
if failed:
    raise SystemExit(f"[FAIL_STATIC] SFT-GPU-8H-H runtime delta verify ({len(failed)} failed)")
print(f"[PASS_STATIC] SFT-GPU-8H-H runtime delta verify ({len(checks)} checks)")
