# ASH-BASETRAIN-GPU 인계사항 — AFTER 27 / NEXT 28

작성 기준: 2026-06-10
프로젝트 루트(선배 로컬): `D:\1111113232\DUST\1\ash_pass3`

## 0. SSOT 고정

```txt
LATEST_CONFIRMED_STATIC_PASS = ASH-BASETRAIN-GPU-27
SOURCE_SSOT = ASH-BASETRAIN-GPU-26 PASS
NEXT_PATCH = ASH-BASETRAIN-GPU-28
NEXT_PATCH_KIND = Gradient Buffer Allocation Candidate / Contracted Logits Gradient Buffer Allocation No Backward No Optimizer Seal
```

## 1. 확정

```txt
STATE_OWNER = ASH-BASETRAIN-GPU-27 GPU backward preflight state
SSOT_EXISTS = true
STATIC_REPRODUCIBLE = yes
LOCAL_RUNTIME_REPRODUCIBLE = USER_LOCAL_SSOT_REQUIRED
```

## 2. 27에서 열린 것

```txt
source_26_validation = true
backward_readiness_validation = true
gradient_buffer_contract_created = true
gradient_write_boundary_contract_created = true
loss_scalar_source_binding_created = true
shader_source_lock_created = true
model_weight_gradient_denylist_created = true
body_training_claim_guard_created = true
```

## 3. 계속 닫힌 경계

```txt
new_gpu_buffer_created = false
new_compute_dispatch_executed = false
new_readback_executed = false
new_loss_computed = false
backward_executed = false
gradient_buffer_created = false
gradient_buffer_written = false
gradient_value_computed = false
optimizer_step_executed = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
model_weight_gradient_contract_created = false
```

## 4. 다음 작업

```txt
ASH-BASETRAIN-GPU-28
Gradient Buffer Allocation Candidate /
Contracted Logits Gradient Buffer Allocation No Backward No Optimizer Seal
```

Expected verdict:

```txt
PASS_ASH_BASETRAIN_GPU_27_GPU_BACKWARD_PREFLIGHT_STABLE_GPU_LOSS_CANDIDATE_TO_GRADIENT_BUFFER_CONTRACT_NO_BACKWARD_NO_OPTIMIZER
```
