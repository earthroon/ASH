from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, cond):
    checks.append((name, bool(cond)))

pass1 = ROOT / 'crates/lora_train/src/lm_head_vocab_atlas_gpu_pass1.rs'
atlas = ROOT / 'crates/lora_train/src/lm_head_vocab_atlas.rs'
lib = ROOT / 'crates/lora_train/src/lib.rs'
accept = ROOT / 'acceptance_reports/SFT-GPU-8H-C_pass1_gpu_tile_group_projection_partial_logsumexp.md'

pass1_s = pass1.read_text(encoding='utf-8') if pass1.exists() else ''
atlas_s = atlas.read_text(encoding='utf-8') if atlas.exists() else ''
lib_s = lib.read_text(encoding='utf-8') if lib.exists() else ''
accept_s = accept.read_text(encoding='utf-8') if accept.exists() else ''

check('lm_head_vocab_atlas_gpu_pass1.rs exists', pass1.exists())
check('GpuLmHeadVocabAtlasPass1Config exists', 'struct GpuLmHeadVocabAtlasPass1Config' in pass1_s)
check('GpuLmHeadVocabAtlasPass1Layout exists', 'struct GpuLmHeadVocabAtlasPass1Layout' in pass1_s)
check('GpuLmHeadVocabAtlasPass1Buffers exists', 'struct GpuLmHeadVocabAtlasPass1Buffers' in pass1_s)
check('GpuLmHeadVocabAtlasPass1Report exists', 'struct GpuLmHeadVocabAtlasPass1Report' in pass1_s)
check('build_gpu_pass1_partial_buffers exists', 'fn build_gpu_pass1_partial_buffers' in pass1_s or 'pub fn build_gpu_pass1_partial_buffers' in pass1_s)
check('validate_pass1_no_full_logits exists', 'fn validate_pass1_no_full_logits' in pass1_s or 'pub fn validate_pass1_no_full_logits' in pass1_s)
check('stage_vocab_weight_group exists', 'fn stage_vocab_weight_group' in pass1_s or 'pub fn stage_vocab_weight_group' in pass1_s)
check('stage_lora_b_group exists', 'fn stage_lora_b_group' in pass1_s or 'pub fn stage_lora_b_group' in pass1_s)
check('run_gpu_pass1_tile_group_projection exists', 'fn run_gpu_pass1_tile_group_projection' in pass1_s or 'pub fn run_gpu_pass1_tile_group_projection' in pass1_s)
check('partial_max_shape contract exists', 'partial_max_shape' in pass1_s and '[cfg.group_count, cfg.active_tokens]' in pass1_s)
check('partial_sum_exp_shape contract exists', 'partial_sum_exp_shape' in pass1_s)
check('partial_target_logit_shape contract exists', 'partial_target_logit_shape' in pass1_s)
check('partial_target_seen_shape contract exists', 'partial_target_seen_shape' in pass1_s)
check('full logits guard exists', 'forbidden full logits' in pass1_s and 'partial_bytes >= full_logits_bytes' in pass1_s)
check('logits readback guard exists', 'forbid_logits_readback=true requires readback_policy=loss_and_report_only' in pass1_s)
check('group weight staging guard exists', 'group weight staging exceeds max_group_weight_bytes' in pass1_s)
check('module exported from lib.rs', 'pub mod lm_head_vocab_atlas_gpu_pass1;' in lib_s)
check('lm_head_vocab_atlas imports pass1 module', 'lm_head_vocab_atlas_gpu_pass1' in atlas_s)
check('8H-C branch writes pass1 report', 'write_gpu_pass1_report' in atlas_s)
check('8H-C branch creates partial buffers', 'build_gpu_pass1_partial_buffers' in atlas_s)
check('8H-C branch stages first group', 'stage_vocab_weight_group' in atlas_s and 'stage_lora_b_group' in atlas_s)
check('PASS_PASS1_BUFFER_AND_STAGING_SEAL log exists', 'PASS_PASS1_BUFFER_AND_STAGING_SEAL' in atlas_s)
check('8H-C explicit bail exists', 'actual pass1 GPU projection kernel is scheduled for SFT-GPU-8H-C2' in atlas_s)
check('acceptance report exists', accept.exists())
check('acceptance mentions full logits forbidden', 'full logits buffer forbidden' in accept_s)

failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if failed:
    raise SystemExit(f"[FAIL_STATIC] SFT-GPU-8H-C static validation failed: {failed}")
print(f"[PASS_STATIC] SFT-GPU-8H-C pass1 GPU tile group projection + partial logsumexp seal ({len(checks)} checks)")
