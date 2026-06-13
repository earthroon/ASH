# ASH-BASETRAIN-GPU 인계사항 — AFTER 28 / NEXT 29

작성 기준: 2026-06-10
프로젝트 루트(선배 로컬): `D:\1111113232\DUST\1\ash_pass3`

## 0. SSOT 고정

```txt
LATEST_CONFIRMED_SOURCE = ASH-BASETRAIN-GPU-27 PASS
CURRENT_PATCH = ASH-BASETRAIN-GPU-28
CURRENT_PATCH_KIND = Gradient Buffer Allocation Candidate / Contracted Logits Gradient Buffer Allocation No Backward No Optimizer Seal
NEXT_PATCH = ASH-BASETRAIN-GPU-29
NEXT_PATCH_KIND = Gradient Buffer Zero Init And Boundary Readback Audit / Allocated Logits Gradient Candidate Buffer Zero State Verification No Gradient Value No Backward No Optimizer Seal
```

## 1. 28 목적

28은 27에서 계약된 logits-gradient candidate buffer를 실제 GPU allocation candidate로 여는 패치다.
단, gradient write / gradient value computation / backward / optimizer / model weight gradient / body training claim은 모두 닫는다.

## 2. 28 PASS 기대 핵심값

```txt
pass = true
violation_mask = 0
verdict_lut_index = 0
gradient_target = logits_gradient_candidate
gradient_dtype = f32
gradient_shape = [1, 1, 2048]
gradient_element_count = 2048
gradient_bytes = 8192
allocated_buffer_size_bytes = 8192
gradient_buffer_created = true
gradient_buffer_written = false
gradient_value_computed = false
new_compute_dispatch_executed = false
new_queue_submit_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
runtime_1p1b_training_claimed = false
```

## 3. 다음 작업

PASS 시:

```txt
ASH-BASETRAIN-GPU-29
Gradient Buffer Zero Init And Boundary Readback Audit /
Allocated Logits Gradient Candidate Buffer Zero State Verification
No Gradient Value No Backward No Optimizer Seal
```

FAIL 시:

```txt
ASH-BASETRAIN-GPU-28A
Gradient Buffer Allocation Candidate Failure Triage /
Source 27 Contract Buffer Descriptor Allocation Boundary Or Mutation Blocker Detail
No Backward No Optimizer Seal
```

## 4. operator command

```powershell
cd "D:\1111113232\DUST\1\ash_pass3"

$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"

cargo build -p base_train --bin ash_basetrain_gpu_28_gradient_buffer_allocation_candidate --jobs 1 2>&1 | Tee-Object -FilePath ".\target\ash_28_cargo_build.log"

cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_28_gradient_buffer_allocation_candidate 2>&1 | Tee-Object -FilePath ".\target\ash_basetrain_gpu_28_gradient_buffer_allocation_candidate.log"
```
