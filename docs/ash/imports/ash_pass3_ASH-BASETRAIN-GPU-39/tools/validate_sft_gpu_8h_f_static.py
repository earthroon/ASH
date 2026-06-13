from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def require(name, cond):
    if not cond:
        raise SystemExit(f"[FAIL] {name}")
    checks.append(name)
    print(f"[PASS] {name}")

update = ROOT / 'crates/lora_train/src/lm_head_vocab_atlas_gpu_update.rs'
entry = ROOT / 'crates/lora_train/src/lm_head_vocab_atlas.rs'
lib = ROOT / 'crates/lora_train/src/lib.rs'
config = ROOT / 'crates/lora_train/src/config.rs'
json_cfg = ROOT / 'configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json'
accept = ROOT / 'acceptance_reports/SFT-GPU-8H-F_partial_gradient_reduce_update_kernel.md'

require('lm_head_vocab_atlas_gpu_update.rs exists', update.exists())
ut = update.read_text(encoding='utf-8')
et = entry.read_text(encoding='utf-8')
lt = lib.read_text(encoding='utf-8')
ct = config.read_text(encoding='utf-8')
js = json_cfg.read_text(encoding='utf-8')

require('GpuGradientReduceUpdateConfig exists', 'struct GpuGradientReduceUpdateConfig' in ut)
require('GpuGradientReduceUpdateLayout exists', 'struct GpuGradientReduceUpdateLayout' in ut)
require('GpuGradientReduceUpdateBuffers exists', 'struct GpuGradientReduceUpdateBuffers' in ut)
require('GpuGradientReduceUpdateReport exists', 'struct GpuGradientReduceUpdateReport' in ut)
require('validate_gradient_reduce_update_policy exists', 'fn validate_gradient_reduce_update_policy' in ut)
require('build_gpu_gradient_reduce_update_buffers exists', 'fn build_gpu_gradient_reduce_update_buffers' in ut)
require('dispatch_gradient_reduce_update_kernel exists', 'fn dispatch_gradient_reduce_update_kernel' in ut)
require('cpu_reference_gradient_reduce_update exists', 'fn cpu_reference_gradient_reduce_update' in ut)
require('update_mode=sgd_smoke guard exists', 'update_mode != "sgd_smoke"' in ut)
require('grad_lora_mid reduce loop exists', 'grad_lora_mid[dst] += grad_lora_mid_partial[src]' in ut)
require('grad_A matmul contract exists', 'grad_a[r * cfg.hidden_size + h] = sum' in ut)
require('LoRA A update exists', '*dst -= cfg.learning_rate * *grad' in ut)
require('lora_a_delta_norm report exists', 'lora_a_delta_norm' in ut)
require('lora_b_delta_norm report exists', 'lora_b_delta_norm' in ut)
require('update_applied=true report exists', 'update_applied: true' in ut)
require('PASS_GRADIENT_REDUCE_UPDATE_KERNEL_SMOKE exists', 'PASS_GRADIENT_REDUCE_UPDATE_KERNEL_SMOKE' in ut and 'PASS_GRADIENT_REDUCE_UPDATE_KERNEL_SMOKE' in et)
require('module exported in lib.rs', 'pub mod lm_head_vocab_atlas_gpu_update;' in lt)
require('entry imports update module', 'lm_head_vocab_atlas_gpu_update' in et)
require('entry calls dispatch_gradient_reduce_update_kernel', 'dispatch_gradient_reduce_update_kernel' in et)
require('config struct LmHeadVocabAtlasGpuUpdateConfig exists', 'struct LmHeadVocabAtlasGpuUpdateConfig' in ct)
require('config nested update field exists', 'pub update: LmHeadVocabAtlasGpuUpdateConfig' in ct)
require('JSON update block exists', '"update"' in js and '"mode": "sgd_smoke"' in js)
require('acceptance report exists', accept.exists())
print(f"[PASS_STATIC] SFT-GPU-8H-F partial gradient reduce + update kernel ({len(checks)} checks)")
