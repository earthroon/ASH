from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
checks = []

def require(path, needle, label):
    text = (ROOT / path).read_text(encoding='utf-8')
    ok = needle in text
    checks.append((ok, label))
    if not ok:
        print(f"[FAIL] {label}: missing {needle!r} in {path}")

def require_file(path, label):
    ok = (ROOT / path).exists()
    checks.append((ok, label))
    if not ok:
        print(f"[FAIL] {label}: missing file {path}")

require_file('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'bridge source exists')
require('crates/lora_train/src/lib.rs', 'pub mod lm_head_vocab_atlas_gpu_bridge;', 'bridge module exported')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'pub struct GpuLmHeadVocabAtlasBridgeConfig', 'bridge config struct')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'pub struct GpuLmHeadVocabAtlasBufferLayout', 'buffer layout struct')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'pub struct GpuLmHeadVocabAtlasBridge', 'bridge handle struct')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'pub fn compact_active_sft_rows', 'active row compaction')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'pub fn build_gpu_lm_head_vocab_atlas_bridge', 'bridge builder')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'pub fn validate_gpu_bridge_memory_policy', 'memory policy guard')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'hidden_shape: [cfg.active_tokens, cfg.hidden_size]', 'hidden active shape contract')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'lora_a_shape: [cfg.rank, cfg.hidden_size]', 'lora A shape contract')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'lora_b_shape: [cfg.vocab_size, cfg.rank]', 'lora B shape contract')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'running_max_shape', 'running max buffer')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'running_sum_exp_shape', 'running sum exp buffer')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'target_logit_shape', 'target logit buffer')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'target_seen_shape', 'target seen buffer')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'tile group would recreate forbidden full lm_head weight buffer', 'full vocab buffer guard')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'forbid_full_logits_buffer', 'full logits buffer guard')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'readback_policy=loss_and_report_only', 'readback discipline guard')
require('crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs', 'vocab_atlas_gpu_bridge_report.json', 'bridge report writer')
require('crates/lora_train/src/lm_head_vocab_atlas.rs', 'PASS_GPU_BUFFER_BRIDGE_SEAL', 'runtime bridge seal log')
require('crates/lora_train/src/lm_head_vocab_atlas.rs', 'PASS_GPU_BUFFER_BRIDGE_SEAL', '8H-B explicit bridge pass before 8H-C')
require_file('acceptance_reports/SFT-GPU-8H-B_gpu_buffer_bridge_seal.md', 'acceptance report exists')

failed = [label for ok, label in checks if not ok]
if failed:
    raise SystemExit(f"[FAIL_STATIC] SFT-GPU-8H-B failed {len(failed)} checks")
print(f"[PASS_STATIC] SFT-GPU-8H-B GPU buffer bridge seal ({len(checks)} checks)")
