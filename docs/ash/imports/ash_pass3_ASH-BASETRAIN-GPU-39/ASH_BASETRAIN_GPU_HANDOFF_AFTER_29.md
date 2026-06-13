# ASH-BASETRAIN-GPU 인계사항 — AFTER 29 / NEXT 30

작성 기준: 2026-06-10

## 0. SSOT 고정

```txt
LATEST_CONFIRMED_PASS = ASH-BASETRAIN-GPU-29
LATEST_BAKED_ZIP = ash_pass3_ASH-BASETRAIN-GPU-29_gradient_buffer_zero_init_boundary_readback_audit_baked.zip
NEXT_PATCH = ASH-BASETRAIN-GPU-30
NEXT_PATCH_KIND = CPU Logits Gradient Formula Receipt / Local Window Softmax Minus Target Candidate No GPU Write No Backward No Optimizer Seal
```

## 1. 29 목적

```txt
29 = zero-state readback and boundary audit for allocated logits-gradient candidate buffer
29 != gradient value computation
29 != softmax-minus-target computation
29 != backward
29 != optimizer
29 != model weight gradient
```

## 2. 29 핵심 계약

```txt
buffer_size_bytes = 8192
gradient_shape = [1, 1, 2048]
gradient_dtype = f32
zero_digest_scope = raw_8192_zero_bytes
expected_zero_digest_hex = 9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47
queue_submit_scope = zero_state_readback_copy_only
queue_submit_used_for_compute = false
```

## 3. PASS 시 다음 작업

```txt
ASH-BASETRAIN-GPU-30
CPU Logits Gradient Formula Receipt /
Local Window Softmax Minus Target Candidate No GPU Write No Backward No Optimizer Seal
```

## 4. FAIL 시

```txt
ASH-BASETRAIN-GPU-29A
Gradient Buffer Zero Init Boundary Readback Failure Triage /
Readback Size Zero Digest Boundary Or Runtime Copy Blocker Detail No Gradient Value No Backward No Optimizer Seal
```
