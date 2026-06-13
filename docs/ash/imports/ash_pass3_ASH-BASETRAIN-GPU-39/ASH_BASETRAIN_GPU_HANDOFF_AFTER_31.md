# ASH-BASETRAIN-GPU 인계사항 — AFTER 31 / NEXT 32

작성 기준: 2026-06-10
프로젝트 루트(선배 로컬): `D:\1111113232\DUST\1\ash_pass3`

## 0. SSOT 고정

```txt
LATEST_CONFIRMED_PASS = ASH-BASETRAIN-GPU-30
LATEST_BAKED_ZIP = ash_pass3_ASH-BASETRAIN-GPU-30_cpu_logits_gradient_formula_receipt_baked.zip
CURRENT_PATCH = ASH-BASETRAIN-GPU-31
NEXT_PATCH = ASH-BASETRAIN-GPU-32
NEXT_PATCH_KIND = GPU Logits Gradient Write Closure / Written Candidate Persistence Digest And Replay Stability Audit No Backward No Optimizer Seal
```

## 1. 31 목적

31은 30의 CPU logits-gradient candidate를 GPU logits-gradient candidate buffer에 write하고 readback digest로 검증하는 smoke 패치다.

```txt
31 = GPU write smoke
31 != GPU compute dispatch
31 != backward
31 != optimizer
31 != model weight gradient
31 != body training claim
```

## 2. 중요 SSOT 보정

```txt
gpu_buffer_handle_reused_from_28 = false
gpu_buffer_handle_reused_from_29 = false
runtime_buffer_object_persistence_claimed = false
buffer_contract_reconstructed_from_receipts = true
```

28/29의 GPU buffer handle은 프로세스 내부 객체이므로 31에서 재사용한다고 주장하지 않는다. 31은 28/29 descriptor contract와 30 candidate digest를 재바인딩하여 런타임 buffer를 새로 만든다.

## 3. 31 PASS 기대값

```txt
candidate_digest = 4a9f3db1bb85a18497a99b42b7eb0b19394bbaee68b751a968f1ae22b97ba1d8
gpu_written_candidate_digest_match = true
gpu_compute_dispatch_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
runtime_1p1b_training_claimed = false
```

## 4. 다음 패치

```txt
ASH-BASETRAIN-GPU-32
GPU Logits Gradient Write Closure /
Written Candidate Persistence Digest And Replay Stability Audit
No Backward No Optimizer Seal
```
