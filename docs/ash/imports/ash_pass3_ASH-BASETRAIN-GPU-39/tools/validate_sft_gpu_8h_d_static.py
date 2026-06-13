from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def require(path, needle, label):
    text = (ROOT / path).read_text(encoding='utf-8')
    ok = needle in text
    checks.append((ok, label))

require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'pub struct GpuGlobalCeReduceConfig', 'GpuGlobalCeReduceConfig exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'pub struct GpuGlobalCeReduceReport', 'GpuGlobalCeReduceReport exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'pub fn validate_global_ce_reduce_policy', 'validate_global_ce_reduce_policy exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'pub fn dispatch_global_ce_reduce_kernel', 'dispatch_global_ce_reduce_kernel exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'pub fn cpu_reference_global_ce_reduce', 'cpu_reference_global_ce_reduce exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'target_seen_required_count', 'target_seen_required_count guard exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'target_seen_min', 'target_seen_min report exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'target_seen_max', 'target_seen_max report exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'full_logits_buffer_created: false', 'full_logits_buffer_created=false report exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'logits_readback: false', 'logits_readback=false report exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'mean_loss', 'mean_loss report exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'PASS_GLOBAL_CE_REDUCE_KERNEL_SMOKE', 'PASS_GLOBAL_CE_REDUCE_KERNEL_SMOKE exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'run_global_ce_reduce_fixture_parity', 'fixture parity exists')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs', 'readback_policy != "loss_and_report_only"', 'readback policy guard exists')
require('crates/lora_train/src/lib.rs', 'pub mod lm_head_vocab_atlas_gpu_reduce;', 'lib.rs exports reduce module')
require('crates/lora_train/src/lm_head_vocab_atlas.rs', 'dispatch_global_ce_reduce_kernel', 'entry calls dispatch_global_ce_reduce_kernel')
require('crates/lora_train/src/lm_head_vocab_atlas.rs', 'write_gpu_reduce_report', 'entry writes reduce report')
require('crates/lora_train/src/lm_head_vocab_atlas.rs', 'PASS_GLOBAL_CE_REDUCE_KERNEL_SMOKE', '8H-D reduce smoke log still exists')
require('acceptance_reports/SFT-GPU-8H-D_global_ce_reduce_kernel.md', 'PASS_GLOBAL_CE_REDUCE_KERNEL_SMOKE', 'acceptance report exists')

failed = [label for ok, label in checks if not ok]
for ok, label in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
if failed:
    raise SystemExit(f"[FAIL_STATIC] SFT-GPU-8H-D global CE reduce kernel ({len(failed)} failed): {failed}")
print(f"[PASS_STATIC] SFT-GPU-8H-D global CE reduce kernel ({len(checks)} checks)")
