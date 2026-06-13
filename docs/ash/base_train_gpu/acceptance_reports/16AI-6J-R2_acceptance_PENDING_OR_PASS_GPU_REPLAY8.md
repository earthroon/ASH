# 16AI-6J-R2 Acceptance

Status: PENDING_RUNTIME

Scope:
- generation=true
- checkpoint_required=true
- gpu_execution_mode=gpu-shadow
- max_new_tokens=8
- cpu_reference=true
- gpu_native=true
- cpu_fallback=true
- gpu_default=false
- global_default_commit=false
- branch_local_commit=true
- token_ids_mutated=false
- vocab_augmented=false
- new_token_ids_created=false

Expected PASS:
- PASS_GPU_SHADOW_REPLAY8
- eligible_cases >= 1
- cpu_success_count == eligible_cases
- gpu_success_count == eligible_cases
- exact_8_parity_count == eligible_cases
- gpu_error_count = 0
- leak_count = 0
