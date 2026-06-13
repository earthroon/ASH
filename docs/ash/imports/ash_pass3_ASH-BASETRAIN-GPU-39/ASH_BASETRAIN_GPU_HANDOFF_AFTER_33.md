# ASH-BASETRAIN-GPU HANDOFF AFTER 33

## SSOT

```txt
LATEST_CONFIRMED_PASS = ASH-BASETRAIN-GPU-33
LATEST_VERDICT = PASS_ASH_BASETRAIN_GPU_33_LOSS_SCALAR_TO_LOGITS_GRADIENT_BINDING_AUDIT_STABLE_LOSS_CANDIDATE_CPU_GRADIENT_GPU_WRITTEN_CANDIDATE_PARITY_CLOSURE_NO_BACKWARD_NO_OPTIMIZER
NEXT_PATCH = ASH-BASETRAIN-GPU-34
NEXT_PATCH_KIND = Selected Atlas Group Gradient Scope Contract / Single Group Only No Full Model Gradient Seal
```

## 33 closed

- Stable loss from 26: `7.624625205993652`
- Raw logits payload digest: `856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052`
- CPU candidate digest from 30: `4a9f3db1bb85a18497a99b42b7eb0b19394bbaee68b751a968f1ae22b97ba1d8`
- GPU write closure digest from 32: `4a9f3db1bb85a18497a99b42b7eb0b19394bbaee68b751a968f1ae22b97ba1d8`
- Binding chain digest: `431c13f73a8a111d9492ee30beb1dbe034c63120403d4c140d7d48a61826836a`

## Important guard

```txt
payload_digest != candidate_digest
payload_digest_to_candidate_lineage_created = true
new_gpu_write_executed = false
gpu_compute_dispatch_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
runtime_1p1b_training_claimed = false
```

## Next

```txt
ASH-BASETRAIN-GPU-34
Selected Atlas Group Gradient Scope Contract /
Single Group Only No Full Model Gradient Seal
```
