# ASH-BASETRAIN-GPU 인계사항 — AFTER 30 / NEXT 31

작성 기준: 2026-06-10

## 0. SSOT 고정

```txt
LATEST_CONFIRMED_PASS = ASH-BASETRAIN-GPU-30
LATEST_BAKED_ZIP = ash_pass3_ASH-BASETRAIN-GPU-30_cpu_logits_gradient_formula_receipt_baked.zip
NEXT_PATCH = ASH-BASETRAIN-GPU-31
NEXT_PATCH_KIND = GPU Logits Gradient Write Smoke / CPU Candidate To Allocated Logits Gradient Buffer Write Verification No Backward No Optimizer Seal
```

## 1. 30 목적

```txt
30 = CPU logits gradient formula receipt
30 = softmax(logits) - one_hot(target) CPU candidate materialization
30 != GPU write
30 != GPU compute dispatch
30 != backward
30 != optimizer
30 != model weight gradient
```

## 2. 30 핵심 계약

```txt
raw_logits_env_key = ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH
expected_payload_digest = 856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052
candidate_shape = [1, 1, 2048]
candidate_dtype = f32
candidate_bytes = 8192
candidate_write_target = cpu_receipt_only
gpu_write_target = none
```

## 3. PASS 시 다음 작업

```txt
ASH-BASETRAIN-GPU-31
GPU Logits Gradient Write Smoke /
CPU Candidate To Allocated Logits Gradient Buffer Write Verification No Backward No Optimizer Seal
```

## 4. FAIL 시

```txt
ASH-BASETRAIN-GPU-30A
CPU Logits Gradient Formula Failure Triage /
Formula Input Binding Numerical Stability Candidate Digest Or No-Write Guard Blocker Detail No GPU Write No Backward No Optimizer Seal
```
