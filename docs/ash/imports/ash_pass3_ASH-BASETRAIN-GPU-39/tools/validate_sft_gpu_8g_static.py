#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, cond, detail=''):
    checks.append((name, bool(cond), detail))

lm = ROOT / 'crates/lora_train/src/lm_head_vocab_atlas.rs'
config_rs = ROOT / 'crates/lora_train/src/config.rs'
sft = ROOT / 'crates/lora_train/src/sft_feature_store.rs'
model = ROOT / 'crates/lora_train/src/model.rs'
pipeline = ROOT / 'crates/lora_train/src/pipeline.rs'
lib = ROOT / 'crates/lora_train/src/lib.rs'
config_json = ROOT / 'configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json'

lm_s = lm.read_text(encoding='utf-8') if lm.exists() else ''
config_s = config_rs.read_text(encoding='utf-8') if config_rs.exists() else ''
sft_s = sft.read_text(encoding='utf-8') if sft.exists() else ''
model_s = model.read_text(encoding='utf-8') if model.exists() else ''
pipeline_s = pipeline.read_text(encoding='utf-8') if pipeline.exists() else ''
lib_s = lib.read_text(encoding='utf-8') if lib.exists() else ''
try:
    cfg = json.loads(config_json.read_text(encoding='utf-8'))
except Exception as exc:
    cfg = {}
    check('config json parses', False, str(exc))
else:
    check('config json parses', True)

atlas_cfg = cfg.get('lm_head_vocab_atlas', {})
check('lm_head_vocab_atlas.rs exists', lm.exists())
check('lib exports lm_head_vocab_atlas module', 'pub mod lm_head_vocab_atlas;' in lib_s)
check('LmHeadVocabAtlasConfig exists', 'pub struct LmHeadVocabAtlasConfig' in config_s)
check('LoraTrainConfig has lm_head_vocab_atlas field', 'pub lm_head_vocab_atlas: Option<LmHeadVocabAtlasConfig>' in config_s)
check('pipeline build_config_from_specs initializes lm_head_vocab_atlas', 'lm_head_vocab_atlas: None' in pipeline_s)
check('train config enables vocab atlas', atlas_cfg.get('enabled') is True, str(atlas_cfg))
check('train config forbids full vocab buffer', atlas_cfg.get('forbid_full_vocab_buffer') is True)
check('train config forbids full logits buffer', atlas_cfg.get('forbid_full_logits_buffer') is True)
check('train config forbids from_base for lm_head', atlas_cfg.get('forbid_trainable_module_from_base_for_lm_head') is True)
check('sft train_from_features dispatches to vocab atlas trainer', 'run_lm_head_vocab_atlas_lora_train' in sft_s)
check('lm_head legacy from_base guard exists', 'forbids TrainableModuleLoraAdapter::from_base_weight for lm_head' in model_s)
check('vocab tile struct exists', 'pub struct VocabAtlasTile' in lm_s)
check('streaming logsumexp function exists', 'fn update_streaming_logsumexp' in lm_s)
check('full logits policy in report exists', 'forbid_full_logits_buffer' in lm_s)
check('legacy_from_base_used=false report exists', 'legacy_from_base_used: false' in lm_s)
check('target tile capture exists', 'target_seen' in lm_s and 'target_logit' in lm_s)
check('GPU tile matmul path exists', 'matmul(tile.swap_dims(0, 1))' in lm_s)
check('no full Tensor from lm_head in vocab atlas module', 'TensorData::new(lm_head_weight_values' not in lm_s)

failed = [c for c in checks if not c[1]]
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" :: {detail}" if detail and not ok else ''))
print(f"PASS count: {sum(1 for _, ok, _ in checks if ok)}")
if failed:
    print(f"FAIL count: {len(failed)}")
    sys.exit(1)
print('[PASS_STATIC] SFT-GPU-8G lm_head vocab atlas grouped parallel projection / streaming CE seal')
