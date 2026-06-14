# ASH-BASETRAIN-GPU-64A SPEC

## Patch ID

`ASH-BASETRAIN-GPU-64A`

## Title

Runtime Candidate Default Promotion / Active Non-Default Binding To CAS-Protected Default Binding Seal

## Seal

No Silent Default Swap / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-64A` consumes the `ASH-BASETRAIN-GPU-63A` scoped active non-default binding and promotes it into a CAS-protected active default runtime binding.

This patch transitions `ActiveNonDefault` to `ActiveDefault` only when the default pointer compare-and-swap guard passes.

GPU-64A must not silently overwrite an existing default binding. GPU-64A must not perform loss, backward, optimizer, gradient, or weight mutation.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-62A-R1` | installed non-default runtime binding registry entry SSOT |
| `ASH-BASETRAIN-GPU-63A` | scoped active non-default runtime binding SSOT |
| `ASH-BASETRAIN-GPU-64A` | CAS-protected active default binding and default pointer SSOT |
| `ASH-BASETRAIN-GPU-65A` | post-promotion default runtime smoke, not part of GPU-64A |

### Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_ROLLBACK_SNAPSHOT.json
```

### Optional Current Default Pointer SSOT

```text
artifacts/ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json
```

If the pointer exists, GPU-64A must compare its current `default_binding_id` with `--expected-current-default-binding-id`. If the pointer does not exist, the actual previous default binding id is `null` and the expected value must also be `null`.

### Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json
artifacts/ASH_BASETRAIN_GPU_64A_DEFAULT_PROMOTION_ROLLBACK_SNAPSHOT.json
artifacts/ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json
artifacts/ASH_BASETRAIN_GPU_64A_DEFAULT_POINTER_CAS_RECEIPT.json
```

### State Ownership

```text
state ownership:
artifacts/ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json
artifacts/ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json

rollback ownership:
artifacts/ASH_BASETRAIN_GPU_64A_DEFAULT_PROMOTION_ROLLBACK_SNAPSHOT.json

receipt ownership:
artifacts/ASH_BASETRAIN_GPU_64A_DEFAULT_POINTER_CAS_RECEIPT.json

SSOT existence:
missing before GPU-64A execution; exists after GPU-64A PASS.

reproducibility:
reproducible only if the same GPU-63A active binding, receipt, rollback snapshot, and expected current default pointer condition are used. If the actual default pointer changes, CAS must block.
```

---

## 3. Required 63A Input Facts

GPU-64A must validate:

```text
activation_receipt.patch_id == ASH-BASETRAIN-GPU-63A
activation_receipt.pass == true
activation_receipt.verdict == PASS
activation_receipt.scoped_activation.active_binding_written == true
activation_receipt.rollback_snapshot.rollback_snapshot_written == true

active_binding.active_binding_id == ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000
active_binding.binding_state == ActiveNonDefault
active_binding.previous_binding_state == InstalledNonDefault
active_binding.runtime_active_apply == true
active_binding.runtime_default_apply == false
active_binding.runtime_auto_bind == false
active_binding.production_attach == false
active_binding.production_default_apply == false
active_binding.live_inference_attach == false
active_binding.logits_adopted == false
active_binding.final_logits_claimed == false
active_binding.vocab_compatibility_verified == false
active_binding.payload_sha256 == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
active_binding.source_binding_id == ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000
active_binding.source_route_id == ash-basetrain-gpu-60-runtime-candidate-route-0000
active_binding.source_surface_id == ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000
```

---

## 4. CAS Default Pointer Contract

GPU-64A compares:

```text
expected_previous_default_binding_id
actual_previous_default_binding_id
```

PASS only if:

```text
expected_previous_default_binding_id == actual_previous_default_binding_id
```

If the current default pointer file is missing:

```text
actual_previous_default_binding_id == null
```

If mismatch:

```text
BLOCK DEFAULT_POINTER_CAS_MISMATCH
```

and GPU-64A must not write the new default pointer.

If an existing default pointer is present but no expected current value was supplied:

```text
BLOCK DEFAULT_POINTER_EXPECTED_VALUE_REQUIRED
```

---

## 5. Default Promotion Policy

GPU-64A may set:

```text
binding_state == ActiveDefault
runtime_default_apply == true
runtime_active_apply == true
default_pointer_write == true
```

GPU-64A must keep:

```text
production_attach == false
live_inference_attach == false
runtime_auto_bind == false
logits_adopted == false
final_logits_claimed == false
vocab_compatibility_verified == false
loss/backward/optimizer/weight_mutation == false
```

This promotes the runtime default pointer artifact only. It does not run live inference, generate text, or train.

---

## 6. PASS Conditions

```text
active_binding_exists == true
activation_receipt_exists == true
activation_rollback_exists == true
activation_receipt.patch_id == ASH-BASETRAIN-GPU-63A
activation_receipt.pass == true
activation_receipt.verdict == PASS
active_binding.binding_state == ActiveNonDefault
active_binding.runtime_active_apply == true
active_binding.runtime_default_apply == false
active_binding.production_attach == false
active_binding.live_inference_attach == false
active_binding.payload_sha256 matches expected digest
actual_previous_default_binding_id is recorded
expected_previous_default_binding_id is recorded
expected_previous_default_binding_id == actual_previous_default_binding_id
cas_compare_result == PASS
cas_swap_executed == true
rollback_snapshot_written == true
active_default_binding_written == true
default_pointer_written == true
receipt_written == true
binding_state == ActiveDefault
runtime_default_apply == true
runtime_active_apply == true
runtime_auto_bind == false
production_attach == false
live_inference_attach == false
loss/backward/optimizer/weight_mutation == false
silent_default_swap_used == false
silent_correction_used == false
```

---

## 7. BLOCK Conditions

| Code | Meaning |
|---|---|
| `MISSING_ACTIVE_BINDING` | GPU-63A active binding missing |
| `MISSING_ACTIVATION_RECEIPT` | GPU-63A activation receipt missing |
| `MISSING_ACTIVATION_ROLLBACK` | GPU-63A rollback snapshot missing |
| `ACTIVATION_RECEIPT_NOT_PASS` | GPU-63A receipt not PASS |
| `ACTIVE_BINDING_ID_MISMATCH` | active binding id mismatch |
| `SOURCE_BINDING_ID_MISMATCH` | source binding id mismatch |
| `ROUTE_ID_MISMATCH` | source route id mismatch |
| `SURFACE_ID_MISMATCH` | source surface id mismatch |
| `PAYLOAD_DIGEST_MISMATCH` | payload digest mismatch |
| `SOURCE_BINDING_STATE_INVALID` | source binding state is not ActiveNonDefault |
| `SOURCE_NOT_ACTIVE` | source runtime active apply is not true |
| `SOURCE_ALREADY_DEFAULT` | source runtime default apply is already true |
| `SOURCE_PRODUCTION_ATTACH_DETECTED` | source production attach is true |
| `SOURCE_LIVE_INFERENCE_ATTACH_DETECTED` | source live inference attach is true |
| `DEFAULT_POINTER_EXPECTED_VALUE_REQUIRED` | existing default pointer exists but expected previous value was omitted |
| `DEFAULT_POINTER_CAS_MISMATCH` | expected previous default does not equal actual previous default |
| `DEFAULT_POINTER_READ_FAILED` | existing default pointer could not be read |
| `DEFAULT_POINTER_WRITE_FAILED` | CAS-guarded default pointer write failed |
| `ACTIVE_DEFAULT_BINDING_WRITE_FAILED` | active default binding write failed |
| `ROLLBACK_SNAPSHOT_WRITE_FAILED` | rollback snapshot write failed |
| `SILENT_DEFAULT_SWAP_DETECTED` | default pointer overwrite without CAS |
| `PRODUCTION_ATTACH_DETECTED` | production attach attempted |
| `RUNTIME_AUTO_BIND_DETECTED` | runtime auto bind attempted |
| `LIVE_INFERENCE_ATTACH_DETECTED` | live inference attach attempted |
| `LOGITS_ADOPTION_DETECTED` | logits adoption attempted |
| `FINAL_LOGITS_CLAIM_DETECTED` | final logits claim attempted |
| `VOCAB_COMPATIBILITY_CLAIM_DETECTED` | vocab compatibility claim attempted |
| `FORBIDDEN_TRAINING_PATH_DETECTED` | loss/backward/optimizer/weight mutation attempted |
| `GPU_OPERATION_DETECTED` | GPU operation attempted |
| `SILENT_CORRECTION_DETECTED` | silent correction used |
| `RECEIPT_WRITE_FAILED` | receipt write failed |

---

## 8. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_64a_default_promotion -- `
  --active-binding .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json `
  --activation-receipt .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_RECEIPT.json `
  --activation-rollback .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_ROLLBACK_SNAPSHOT.json `
  --current-default-pointer .\artifacts\ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json `
  --expected-current-default-binding-id null `
  --expected-active-binding-id ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000 `
  --expected-source-binding-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000 `
  --expected-route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --promotion-policy-id ash-basetrain-gpu-64a-cas-protected-default-promotion-policy `
  --default-pointer-id ash-basetrain-gpu-runtime-default-pointer-0000 `
  --active-default-binding-id ash-basetrain-gpu-64a-active-default-runtime-binding-0000 `
  --rollback-snapshot-id ash-basetrain-gpu-64a-default-promotion-rollback-snapshot-0000 `
  --out-active-default-binding .\artifacts\ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json `
  --out-default-pointer .\artifacts\ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json `
  --out-rollback .\artifacts\ASH_BASETRAIN_GPU_64A_DEFAULT_PROMOTION_ROLLBACK_SNAPSHOT.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_64A_DEFAULT_POINTER_CAS_RECEIPT.json
```

---

## 9. Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_64a_default_promotion.rs
crates/base_train/src/bin/ash_basetrain_gpu_64a_default_promotion.rs
```

Update `lib.rs`:

```rust
pub mod ash_basetrain_gpu_64a_default_promotion;
```

Update `Cargo.toml`:

```toml
[[bin]]
name = "ash_basetrain_gpu_64a_default_promotion"
path = "src/bin/ash_basetrain_gpu_64a_default_promotion.rs"
```

---

## 10. Next Stage

If GPU-64A PASS:

```text
ASH-BASETRAIN-GPU-65A
Default Runtime Pointer Smoke / CAS-Promoted Default Binding Readonly Runtime Route Probe Seal
No Generation No Loss No Backward No Optimizer
```

If GPU-64A BLOCKED due to CAS/default pointer shape:

```text
ASH-BASETRAIN-GPU-64A-R1
Default Pointer CAS Shape Rebind / Expected Previous Binding And Rollback Snapshot Closure Seal
```