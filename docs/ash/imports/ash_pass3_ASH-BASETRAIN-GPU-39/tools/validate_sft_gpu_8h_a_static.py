#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
checks = []

def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')

def require(name: str, condition: bool, detail: str = '') -> None:
    if condition:
        checks.append((True, name, detail))
    else:
        checks.append((False, name, detail))

config_rs = read('crates/lora_train/src/config.rs')
atlas_rs = read('crates/lora_train/src/lm_head_vocab_atlas.rs')
config_json_path = ROOT / 'configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json'
config = json.loads(config_json_path.read_text(encoding='utf-8'))
atlas = config.get('lm_head_vocab_atlas', {})
gpu = atlas.get('gpu_parallel', {})
timing = atlas.get('timing_profiler', {})

require('LmHeadVocabAtlasGpuParallelConfig exists', 'struct LmHeadVocabAtlasGpuParallelConfig' in config_rs)
require('LmHeadVocabAtlasTimingProfilerConfig exists', 'struct LmHeadVocabAtlasTimingProfilerConfig' in config_rs)
require('LmHeadVocabAtlasConfig has forbid_cpu_serial_tile_loop', 'forbid_cpu_serial_tile_loop' in config_rs)
require('LmHeadVocabAtlasConfig has gpu_parallel field', 'gpu_parallel: LmHeadVocabAtlasGpuParallelConfig' in config_rs)
require('LmHeadVocabAtlasConfig has timing_profiler field', 'timing_profiler: LmHeadVocabAtlasTimingProfilerConfig' in config_rs)
require('config projection=gpu_parallel_vocab_atlas', atlas.get('projection') == 'gpu_parallel_vocab_atlas')
require('config gpu_parallel.enabled=true', gpu.get('enabled') is True)
require('config gpu_parallel.required=true', gpu.get('required') is True)
require('config dispatch_mode=tile_group_parallel', gpu.get('dispatch_mode') == 'tile_group_parallel')
require('config ce_reduce_mode=gpu_partial_logsumexp', gpu.get('ce_reduce_mode') == 'gpu_partial_logsumexp')
require('config grad_reduce_mode=gpu_partial_grad_reduce', gpu.get('grad_reduce_mode') == 'gpu_partial_grad_reduce')
require('config update_mode=gpu_reduce_update', gpu.get('update_mode') == 'gpu_reduce_update')
require('config forbid_cpu_serial_tile_loop=true', atlas.get('forbid_cpu_serial_tile_loop') is True)
require('config forbid_cpu_token_vocab_loop=true', gpu.get('forbid_cpu_token_vocab_loop') is True)
require('config forbid_logits_readback=true', gpu.get('forbid_logits_readback') is True)
require('config readback_policy=loss_and_report_only', gpu.get('readback_policy') == 'loss_and_report_only')
require('config timing profiler enabled', timing.get('enabled') is True)
require('validate_gpu_parallel_vocab_atlas_config exists', 'fn validate_gpu_parallel_vocab_atlas_config' in atlas_rs)
require('max_group_weight_bytes guard exists', 'max_group_weight_bytes' in atlas_rs and 'group_weight_bytes' in atlas_rs)
require('forbidden full vocab guard exists', 'recreate forbidden full vocab buffer' in atlas_rs)
require('strict no quiet fallback bail exists', ('GPU parallel runner is not implemented yet' in atlas_rs) or ('actual pass1 GPU projection kernel is scheduled for SFT-GPU-8H-C2' in atlas_rs))
require('config sealed log exists', 'config_sealed=true projection={}' in atlas_rs)

failed = [item for item in checks if not item[0]]
for ok, name, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{(' - ' + detail) if detail else ''}")

if failed:
    print(f"\n[FAIL_STATIC] SFT-GPU-8H-A GPU parallel config seal failed {len(failed)} checks")
    sys.exit(1)

print(f"\n[PASS_STATIC] SFT-GPU-8H-A GPU parallel config seal ({len(checks)} checks)")
