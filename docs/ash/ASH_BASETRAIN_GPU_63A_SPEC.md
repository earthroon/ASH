# ASH-BASETRAIN-GPU-63A SPEC

## Patch ID

`ASH-BASETRAIN-GPU-63A`

## Title

Runtime Candidate Scoped Activation / Installed Non-Default Binding To Test-Traffic Active Binding Seal

## Seal

No Default Apply / No Production Attach / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-63A` consumes the `ASH-BASETRAIN-GPU-62A-R1` installed non-default runtime binding registry entry and creates a scoped active non-default runtime binding for test or canary traffic only.

This patch transitions the candidate from `InstalledNonDefault` to `ActiveNonDefault` under an explicit scoped activation policy.

GPU-63A must not promote the binding to default, attach it to production inference, claim final logits, claim vocabulary compatibility, compute loss, run backward, create optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-61` | dryrun runtime binding descriptor SSOT |
| `ASH-BASETRAIN-GPU-62A-R1` | installed non-default runtime binding registry entry SSOT |
| `ASH-BASETRAIN-GPU-63A` | scoped active non-default runtime binding SSOT |
| `ASH-BASETRAIN-GPU-64A` | default promotion / CAS rollback SSOT, not part of GPU-63A |

### Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_REGISTRY_ENTRY.json
artifacts/ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_INSTALL_RECEIPT.json
```

### Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_ROLLBACK_SNAPSHOT.json
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_RECEIPT.json
```

### State Ownership

```text
state ownership:
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json

SSOT existence:
missing before GPU-63A execution; exists after GPU-63A PASS.

reproducibility:
reproducible from the same GPU-62A-R1 registry entry, install receipt, activation policy id, active binding id, activation scope, route id, canary session id, and rollback snapshot id.
```

---

## 3. Required 62A-R1 Input Facts

GPU-63A must validate:

```text
install_receipt.patch_id == ASH-BASETRAIN-GPU-62A-R1
install_receipt.pass == true
install_receipt.verdict == PASS

registry_entry.registry_entry_id == ash-basetrain-gpu-62a-runtime-binding-registry-entry-0000
registry_entry.installed_binding_id == ash-basetrain-gpu-62a-installed-non-default-runtime-binding-0000
registry_entry.binding_state == InstalledNonDefault
registry_entry.runtime_binding_installed == true
registry_entry.runtime_default_apply == false
registry_entry.runtime_active_apply == false
registry_entry.runtime_auto_bind == false
registry_entry.live_inference_attach == false
registry_entry.logits_adopted == false
registry_entry.final_logits_claimed == false
registry_entry.vocab_compatibility_verified == false
registry_entry.payload_sha256 == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
registry_entry.source_binding_id == ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000
registry_entry.source_route_id == ash-basetrain-gpu-60-runtime-candidate-route-0000
registry_entry.source_surface_id == ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000
```

---

## 4. Scoped Activation Policy

Default policy:

```json
{
  "activation_policy_id": "ash-basetrain-gpu-63a-scoped-active-non-default-policy",
  "activation_policy_kind": "test_traffic_active_non_default_binding_policy",
  "required_source_patch": "ASH-BASETRAIN-GPU-62A-R1",
  "required_source_binding_state": "InstalledNonDefault",
  "target_binding_state": "ActiveNonDefault",
  "activation_scope": "test_traffic_only",
  "allow_canary_runtime_route": true,
  "allow_test_traffic_attach": true,
  "allow_production_attach": false,
  "allow_runtime_default_apply": false,
  "allow_runtime_auto_bind": false,
  "allow_default_pointer_write": false,
  "allow_logits_adoption": false,
  "allow_final_logits_claim": false,
  "allow_vocab_compatibility_claim": false,
  "allow_loss": false,
  "allow_backward": false,
  "allow_optimizer": false,
  "allow_weight_mutation": false
}
```

Allowed activation scopes:

```text
test_traffic_only
canary_runtime_only
operator_scoped_probe_only
```

Forbidden scopes:

```text
production
production_default
global
default_runtime
live_inference_default
```

---

## 5. Outputs

GPU-63A writes:

```text
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_ROLLBACK_SNAPSHOT.json
artifacts/ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_RECEIPT.json
```

No `.sha256` sidecar files.

---

## 6. Must Not Write

GPU-63A must not write runtime default pointer files, production route attach files, live inference attach markers, adopted logits artifacts, final logits artifacts, vocab compatibility artifacts, loss receipts, gradient receipts, optimizer receipts, delta candidate packets, weight checkpoints, new raw payload binaries, full tensor artifacts, or unselected group artifacts.

---

## 7. Must Not Mutate

GPU-63A must not mutate GPU-55 raw payload artifacts, GPU-57 surface descriptors, GPU-58 shape policy descriptors, GPU-59 approval envelopes, GPU-60 route envelopes, GPU-61 dryrun descriptors, GPU-62A registry entries, or GPU-62A install receipts.

GPU-63A creates a new scoped active binding artifact. It does not rewrite the GPU-62A registry entry.

---

## 8. PASS Conditions

```text
registry_entry_exists == true
install_receipt_exists == true
install_receipt.patch_id == ASH-BASETRAIN-GPU-62A-R1
install_receipt.pass == true
install_receipt.verdict == PASS
registry_entry.binding_state == InstalledNonDefault
registry_entry.runtime_binding_installed == true
registry_entry.runtime_default_apply == false
registry_entry.runtime_active_apply == false
registry_entry.live_inference_attach == false
registry_entry.logits_adopted == false
registry_entry.final_logits_claimed == false
registry_entry.vocab_compatibility_verified == false
activation_scope in [test_traffic_only, canary_runtime_only, operator_scoped_probe_only]
rollback_snapshot_written == true
active_binding_written == true
receipt_written == true
binding_state == ActiveNonDefault
previous_binding_state == InstalledNonDefault
runtime_active_apply == true
runtime_default_apply == false
runtime_auto_bind == false
production_attach == false
live_inference_attach == false
logits_adopted == false
final_logits_claimed == false
vocab_compatibility_verified == false
loss/backward/optimizer/weight_mutation == false
silent_correction_used == false
```

---

## 9. BLOCK Conditions

| Code | Meaning |
|---|---|
| `MISSING_REGISTRY_ENTRY` | GPU-62A registry entry missing |
| `MISSING_INSTALL_RECEIPT` | GPU-62A install receipt missing |
| `INSTALL_RECEIPT_NOT_PASS` | GPU-62A-R1 receipt not PASS |
| `REGISTRY_ENTRY_ID_MISMATCH` | registry entry id mismatch |
| `INSTALLED_BINDING_ID_MISMATCH` | installed binding id mismatch |
| `SOURCE_BINDING_ID_MISMATCH` | source binding id mismatch |
| `ROUTE_ID_MISMATCH` | route id mismatch |
| `SURFACE_ID_MISMATCH` | surface id mismatch |
| `PAYLOAD_DIGEST_MISMATCH` | payload digest mismatch |
| `SOURCE_BINDING_STATE_INVALID` | source binding state is not InstalledNonDefault |
| `SOURCE_BINDING_NOT_INSTALLED` | runtime binding installed is not true |
| `SOURCE_ALREADY_ACTIVE` | source already has runtime active apply true |
| `SOURCE_DEFAULT_APPLY_DETECTED` | source has runtime default apply true |
| `SOURCE_LIVE_INFERENCE_ATTACH_DETECTED` | source has live inference attach true |
| `SOURCE_LOGITS_ADOPTION_DETECTED` | source has logits adopted true |
| `ACTIVATION_SCOPE_INVALID` | activation scope is production/global/default or unknown |
| `ACTIVE_BINDING_ID_EMPTY` | active binding id empty |
| `ACTIVATION_POLICY_ID_EMPTY` | activation policy id empty |
| `ROLLBACK_SNAPSHOT_ID_EMPTY` | rollback snapshot id empty |
| `ROLLBACK_SNAPSHOT_WRITE_FAILED` | rollback snapshot write failed |
| `ACTIVE_BINDING_WRITE_FAILED` | active binding write failed |
| `PRODUCTION_ATTACH_DETECTED` | production attach attempted |
| `RUNTIME_DEFAULT_APPLY_DETECTED` | runtime default apply attempted |
| `RUNTIME_AUTO_BIND_DETECTED` | runtime auto bind attempted |
| `DEFAULT_POINTER_WRITE_DETECTED` | default pointer write attempted |
| `LIVE_INFERENCE_ATTACH_DETECTED` | live inference attach attempted |
| `LOGITS_ADOPTION_DETECTED` | logits adoption attempted |
| `FINAL_LOGITS_CLAIM_DETECTED` | final logits claim attempted |
| `VOCAB_COMPATIBILITY_CLAIM_DETECTED` | vocab compatibility claim attempted |
| `FORBIDDEN_TRAINING_PATH_DETECTED` | loss/backward/optimizer/weight mutation attempted |
| `GPU_OPERATION_DETECTED` | GPU operation attempted |
| `SILENT_CORRECTION_DETECTED` | silent correction used |
| `RECEIPT_WRITE_FAILED` | receipt write failed |

---

## 10. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_63a_scoped_activation -- `
  --registry-entry .\artifacts\ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_REGISTRY_ENTRY.json `
  --install-receipt .\artifacts\ASH_BASETRAIN_GPU_62A_RUNTIME_BINDING_INSTALL_RECEIPT.json `
  --expected-registry-entry-id ash-basetrain-gpu-62a-runtime-binding-registry-entry-0000 `
  --expected-installed-binding-id ash-basetrain-gpu-62a-installed-non-default-runtime-binding-0000 `
  --expected-source-binding-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000 `
  --expected-route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --activation-policy-id ash-basetrain-gpu-63a-scoped-active-non-default-policy `
  --active-binding-id ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000 `
  --activation-scope test_traffic_only `
  --test-traffic-route-id ash-basetrain-gpu-63a-test-traffic-route-0000 `
  --canary-session-id ash-basetrain-gpu-63a-canary-session-0000 `
  --canary-sample-ratio 0.0 `
  --rollback-snapshot-id ash-basetrain-gpu-63a-scoped-activation-rollback-snapshot-0000 `
  --out-active-binding .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVE_BINDING.json `
  --out-rollback .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_ROLLBACK_SNAPSHOT.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_63A_SCOPED_ACTIVATION_RECEIPT.json
```

---

## 11. Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_63a_scoped_activation.rs
crates/base_train/src/bin/ash_basetrain_gpu_63a_scoped_activation.rs
```

Update `lib.rs`:

```rust
pub mod ash_basetrain_gpu_63a_scoped_activation;
```

Update `Cargo.toml`:

```toml
[[bin]]
name = "ash_basetrain_gpu_63a_scoped_activation"
path = "src/bin/ash_basetrain_gpu_63a_scoped_activation.rs"
```

---

## 12. Next Stage

If GPU-63A PASS:

```text
ASH-BASETRAIN-GPU-64A
Runtime Candidate Default Promotion /
Active Non-Default Binding To CAS-Protected Default Binding Seal
No Silent Default Swap No Loss No Backward No Optimizer
```

If GPU-63A BLOCKED due to scope, route, or activation shape:

```text
ASH-BASETRAIN-GPU-63A-R1
Scoped Activation Shape Rebind /
Canary Route Policy And Rollback Snapshot Receipt Closure Seal
```
