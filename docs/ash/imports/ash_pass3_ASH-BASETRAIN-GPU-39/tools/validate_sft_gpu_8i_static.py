from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
checks = []
def require(path, text, label):
    p = ROOT / path
    ok = p.exists() and text in p.read_text(encoding='utf-8', errors='ignore')
    checks.append((ok, label))

def require_file(path, label):
    checks.append(((ROOT / path).exists(), label))

require_file('crates/lora_train/src/lm_head_vocab_atlas_gpu_adamw.rs','adamw module exists')
require_file('crates/lora_train/src/lm_head_vocab_atlas_gpu_multistep.rs','multistep module exists')
require_file('crates/lora_train/src/lm_head_vocab_atlas_gpu_checkpoint.rs','checkpoint module exists')
require('crates/lora_train/src/config.rs','LmHeadVocabAtlasMultiStepTrainConfig','multi step config exists')
require('crates/lora_train/src/config.rs','LmHeadVocabAtlasAdamWConfig','adamw config exists')
require('crates/lora_train/src/config.rs','LmHeadVocabAtlasTrainGuardConfig','guard config exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_adamw.rs','GpuAdamWStateCpu','AdamW state exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_multistep.rs','run_gpu_vocab_atlas_multistep_train_from_seal','multistep runner exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_checkpoint.rs','optimizer_state.safetensors','optimizer state path exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_checkpoint.rs','training_state.json','training state path exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_multistep.rs','loss_trace.json','loss trace path exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_multistep.rs','PASS_ADAMW_MULTISTEP_TRAIN_LOOP','pass string exists')
require('crates/lora_train/src/lm_head_vocab_atlas.rs','run_gpu_vocab_atlas_multistep_train_from_seal','entry calls multistep')
require('configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json','"multi_step_train"','config contains multi_step_train')
require_file('acceptance_reports/SFT-GPU-8I_adamw_multistep_train_loop.md','acceptance report exists')

failed=[label for ok,label in checks if not ok]
for ok,label in checks:
    print(('[PASS]' if ok else '[FAIL]'), label)
if failed:
    raise SystemExit('FAILED: '+', '.join(failed))
print('[PASS_STATIC] SFT-GPU-8I AdamW / multi-step train loop (%d checks)' % len(checks))
