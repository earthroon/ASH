# ASH-BASETRAIN-GPU 인계사항 — AFTER 32 / NEXT 33

## 0. SSOT

```txt
LATEST_PATCH = ASH-BASETRAIN-GPU-32
SOURCE_CONFIRMED_PASS = ASH-BASETRAIN-GPU-31
EXPECTED_VERDICT = PASS_ASH_BASETRAIN_GPU_32_GPU_LOGITS_GRADIENT_WRITE_CLOSURE_WRITTEN_CANDIDATE_PERSISTENCE_DIGEST_AND_REPLAY_STABILITY_AUDIT_NO_BACKWARD_NO_OPTIMIZER
NEXT_PATCH = ASH-BASETRAIN-GPU-33
NEXT_PATCH_KIND = Loss Scalar To Logits Gradient Binding Audit / No Backward No Optimizer
```

## 1. 32 목적

31에서 성공한 CPU candidate -> GPU logits-gradient buffer write/readback을 3회 replay하여 digest/stats 안정성을 닫는다.
GPU object persistence가 아니라 contract/digest/stats persistence만 주장한다.

```txt
gpu_buffer_handle_reused_from_31 = false
runtime_buffer_object_persistence_claimed = false
buffer_contract_reconstructed_from_receipts = true
```

## 2. 32에서 열린 것

```txt
repeated_gpu_candidate_write_executed = true
repeated_gpu_written_readback_executed = true
replay_digest_stability_matrix_created = true
replay_stats_stability_matrix_created = true
write_closure_pass_receipt_created = true
```

## 3. 계속 닫힌 것

```txt
gpu_compute_dispatch_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
```

## 4. Operator Command

```powershell
cd "D:\1111113232\DUST\1\ash_pass3"
$env:CARGO_BUILD_JOBS="1"
$env:CARGO_INCREMENTAL="0"
$env:RUSTFLAGS="-C debuginfo=0"
$env:ASH_BASETRAIN_GPU_30_CPU_LOGITS_GRADIENT_CANDIDATE_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_30_cpu_logits_gradient_candidate.f32le.bin"
$env:ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH="D:\1111113232\DUST\1\ash_pass3\target\ash_basetrain_gpu_21_raw_2048_logits.f32le.bin"
cargo build -p base_train --bin ash_basetrain_gpu_32_gpu_logits_gradient_write_closure --jobs 1
cargo run --jobs 1 -p base_train --bin ash_basetrain_gpu_32_gpu_logits_gradient_write_closure
```
