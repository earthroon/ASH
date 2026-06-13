from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
checks = []
def check(name, cond):
    checks.append((name, bool(cond)))

qe = ROOT/'crates/lora_train/src/lm_head_vocab_atlas_quality_eval.rs'
pg = ROOT/'crates/lora_train/src/lm_head_vocab_atlas_promotion_gate.rs'
config = (ROOT/'crates/lora_train/src/config.rs').read_text(encoding='utf-8')
atlas = (ROOT/'crates/lora_train/src/lm_head_vocab_atlas.rs').read_text(encoding='utf-8')
conf_json = json.loads((ROOT/'configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json').read_text(encoding='utf-8'))
check('lm_head_vocab_atlas_quality_eval.rs exists', qe.exists())
check('lm_head_vocab_atlas_promotion_gate.rs exists', pg.exists())
qet = qe.read_text(encoding='utf-8') if qe.exists() else ''
pgt = pg.read_text(encoding='utf-8') if pg.exists() else ''
for token in ['LmHeadVocabAtlasQualityEvalConfig','LmHeadVocabAtlasQualityMetricsConfig','LmHeadVocabAtlasPromotionGateConfig']:
    check(f'{token} exists in config', token in config)
for token in ['QualityEvalPrompt','LmHeadQualityEvalReport','run_lm_head_quality_eval','quality_eval_report.json']:
    check(f'{token} exists', token in qet)
for token in ['AdapterPromotionGateReport','run_adapter_promotion_gate','promotion_gate_report.json','promotion_status.json','PASS_PROMOTION_GATE']:
    check(f'{token} exists', token in pgt)
check('entry calls run_lm_head_quality_eval', 'run_lm_head_quality_eval' in atlas)
check('entry calls run_adapter_promotion_gate', 'run_adapter_promotion_gate' in atlas)
check('config has quality_eval', 'quality_eval' in conf_json.get('lm_head_vocab_atlas', {}))
check('eval prompt set exists', (ROOT/'configs/eval_prompts/ash_sft_lm_head_quality_eval_ko.jsonl').exists())
check('acceptance report exists', (ROOT/'acceptance_reports/SFT-GPU-8J_quality_eval_promotion_gate.md').exists())
failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(('[PASS] ' if ok else '[FAIL] ') + name)
if failed:
    print(f'[FAIL_STATIC] SFT-GPU-8J quality eval / promotion gate failed {len(failed)} checks')
    sys.exit(1)
print(f'[PASS_STATIC] SFT-GPU-8J quality eval / promotion gate ({len(checks)} checks)')
