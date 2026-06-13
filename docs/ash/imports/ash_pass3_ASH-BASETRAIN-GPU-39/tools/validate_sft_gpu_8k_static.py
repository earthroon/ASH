#!/usr/bin/env python3
from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, cond):
    checks.append((name, bool(cond)))

src = ROOT / 'crates' / 'lora_train' / 'src'
config = (src / 'config.rs').read_text(encoding='utf-8')
lib = (src / 'lib.rs').read_text(encoding='utf-8')
entry = (src / 'lm_head_vocab_atlas.rs').read_text(encoding='utf-8')
files = {
    'runtime_integration_hardening.rs': src / 'runtime_integration_hardening.rs',
    'runtime_adapter_registry.rs': src / 'runtime_adapter_registry.rs',
    'runtime_generation_hygiene.rs': src / 'runtime_generation_hygiene.rs',
}
for name, path in files.items():
    check(f'{name} exists', path.exists())
all_text = '\n'.join(path.read_text(encoding='utf-8') for path in files.values() if path.exists())
check('RuntimeIntegrationConfig exists', 'pub struct RuntimeIntegrationConfig' in config)
check('RuntimeAttachPolicyConfig exists', 'pub struct RuntimeAttachPolicyConfig' in config)
check('RuntimeAdapterRegistry exists', 'pub struct RuntimeAdapterRegistry' in all_text)
check('RuntimeAdapterRegistryEntry exists', 'pub struct RuntimeAdapterRegistryEntry' in all_text)
check('RuntimeLoraSwitchState exists', 'pub struct RuntimeLoraSwitchState' in all_text)
check('validate_runtime_attach_policy exists', 'fn validate_runtime_attach_policy' in all_text or 'pub fn validate_runtime_attach_policy' in all_text)
check('validate_runtime_switch_state exists', 'validate_runtime_switch_state' in all_text)
check('RuntimeIntegrationHardeningReport exists', 'pub struct RuntimeIntegrationHardeningReport' in all_text)
check('RuntimeGenerationHygieneReport exists', 'pub struct RuntimeGenerationHygieneReport' in all_text)
check('runtime_adapter_registry.json string exists', 'runtime_adapter_registry.json' in all_text or 'runtime_adapter_registry.json' in json.dumps(json.load(open(ROOT / 'configs' / 'ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json')), ensure_ascii=False))
check('silent_fallback_detected guard exists', 'silent_fallback_detected' in all_text)
check('PASS_RUNTIME_INTEGRATION_HARDENING string exists', 'PASS_RUNTIME_INTEGRATION_HARDENING' in all_text + entry)
check('runtime_integration module exported', 'pub mod runtime_integration_hardening;' in lib)
check('runtime_integration config in JSON', 'runtime_integration' in json.load(open(ROOT / 'configs' / 'ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json', encoding='utf-8')))
check('acceptance report exists', (ROOT / 'acceptance_reports' / 'SFT-GPU-8K_runtime_integration_hardening.md').exists())
failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
if failed:
    print(f"[FAIL_STATIC] SFT-GPU-8K runtime integration hardening ({len(failed)} failed)")
    sys.exit(1)
print(f"[PASS_STATIC] SFT-GPU-8K runtime integration hardening ({len(checks)} checks)")
