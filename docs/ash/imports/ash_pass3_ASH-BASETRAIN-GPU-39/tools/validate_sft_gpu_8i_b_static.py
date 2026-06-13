from pathlib import Path
root = Path(__file__).resolve().parents[1]
checks = []
def ok(name, cond):
    if not cond:
        raise SystemExit(f"[FAIL] {name}")
    checks.append(name)

def read(p): return (root / p).read_text(encoding='utf-8')

ok('lm_head_vocab_atlas_gpu_step.rs exists', (root/'crates/lora_train/src/lm_head_vocab_atlas_gpu_step.rs').exists())
ok('lm_head_vocab_atlas_gpu_buffer_hygiene.rs exists', (root/'crates/lora_train/src/lm_head_vocab_atlas_gpu_buffer_hygiene.rs').exists())
ok('lm_head_vocab_atlas_gpu_loop_report.rs exists', (root/'crates/lora_train/src/lm_head_vocab_atlas_gpu_loop_report.rs').exists())
config = read('crates/lora_train/src/config.rs')
ok('LmHeadVocabAtlasRedispatchConfig exists', 'LmHeadVocabAtlasRedispatchConfig' in config)
ok('LmHeadVocabAtlasBufferClearConfig exists', 'LmHeadVocabAtlasBufferClearConfig' in config)
ok('forbid_reuse_previous_step_partials exists', 'forbid_reuse_previous_step_partials' in config)
ok('forbid_stale_loss_state exists', 'forbid_stale_loss_state' in config)
ok('loss_explosion_factor exists', 'loss_explosion_factor' in config)
step = read('crates/lora_train/src/lm_head_vocab_atlas_gpu_step.rs')
ok('clear_gpu_vocab_atlas_step_buffers used', 'clear_gpu_vocab_atlas_step_buffers' in step)
buf = read('crates/lora_train/src/lm_head_vocab_atlas_gpu_buffer_hygiene.rs')
ok('validate_buffer_hygiene_report used', 'validate_buffer_hygiene_report' in buf)
ok('run_gpu_vocab_atlas_train_step exists', 'run_gpu_vocab_atlas_train_step' in step)
ok('require all pass1 groups check exists', 'pass1_groups_dispatched != report.group_count' in step)
ok('require all pass2 groups check exists', 'pass2_groups_dispatched != report.group_count' in step)
ok('optimizer adamw fallback guard exists', 'optimizer=adamw' in step and 'SGD fallback' in step)
loop = read('crates/lora_train/src/lm_head_vocab_atlas_gpu_loop_report.rs')
ok('PASS_ALL_STEP_GPU_REDISPATCH_LOOP exists', 'PASS_ALL_STEP_GPU_REDISPATCH_LOOP' in loop)
ok('buffer_hygiene_trace.json writer exists', 'buffer_hygiene_trace.json' in loop)
ms = read('crates/lora_train/src/lm_head_vocab_atlas_gpu_multistep.rs')
ok('redispatch report builder used', 'build_redispatch_loop_report' in ms)
ok('write_redispatch_loop_report used', 'write_redispatch_loop_report' in ms)
ok('write_buffer_hygiene_trace used', 'write_buffer_hygiene_trace' in ms)
ok('acceptance report exists', (root/'acceptance_reports/SFT-GPU-8I-B_all_step_gpu_redispatch_loop.md').exists())
print(f"[PASS_STATIC] SFT-GPU-8I-B all-step GPU redispatch loop ({len(checks)} checks)")
