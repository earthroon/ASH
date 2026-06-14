# ASH-BASETRAIN-GPU-61 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-61`

## Title

Forward Candidate Runtime Route Dryrun / Candidate Route Envelope To Non-Default Runtime Binding Probe Seal

## Seal

No Runtime Default Apply / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-61` consumes the successful `ASH-BASETRAIN-GPU-60` runtime candidate route envelope and performs a non-default runtime binding dryrun.

GPU-61 proves that the approved runtime candidate route can be represented as a non-default dryrun binding descriptor. It does not install the binding, make the route default, attach the route to live inference, adopt logits, claim final logits, verify vocabulary compatibility, compute loss, run backward, create optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-60` | post-approval runtime candidate route preflight SSOT |
| `ASH-BASETRAIN-GPU-61` | non-default runtime binding dryrun descriptor SSOT |
| `ASH-BASETRAIN-GPU-62` | shadow runtime registry candidate preflight, not part of GPU-61 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json
artifacts/ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json
artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json
```

Required GPU-60 facts:

```text
patch_id == ASH-BASETRAIN-GPU-60
pass == true
runtime_candidate_route_created == true
route_id == ash-basetrain-gpu-60-runtime-candidate-route-0000
route_kind == approved_surface_runtime_candidate_route
route_state == preflight_only
route_scope == runtime_candidate_preflight_only
route_policy_id == ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply
runtime_auto_bind == false
runtime_default_apply == false
runtime_apply_allowed == false
logits_adoption_allowed == false
final_logits_claimed == false
vocab_compatibility_verified == false
loss/backward/optimizer/weight_mutation == false
```

Candidate digest SSOT:

```text
2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

The candidate digest remains identity/evidence only in GPU-61. GPU-61 must not use the digest as permission to apply the route.

---

## 3. Runtime Binding Dryrun Policy

Default policy:

```json
{
  "binding_policy_id": "ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-policy",
  "binding_policy_kind": "non_default_runtime_binding_dryrun_policy",
  "required_source_patch": "ASH-BASETRAIN-GPU-60",
  "required_route_state": "preflight_only",
  "required_route_scope": "runtime_candidate_preflight_only",
  "binding_scope": "dryrun_non_default_runtime_candidate_only",
  "binding_state": "dryrun_candidate",
  "allow_runtime_default_apply": false,
  "allow_runtime_auto_bind": false,
  "allow_runtime_active_apply": false,
  "allow_live_inference_attach": false,
  "allow_logits_adoption": false,
  "allow_final_logits_claim": false,
  "allow_vocab_compatibility_claim": false,
  "allow_loss": false,
  "allow_backward": false,
  "allow_optimizer": false,
  "allow_weight_mutation": false
}
```

---

## 4. Inputs

| Argument | Default |
|---|---|
| `--gpu60-receipt` | `artifacts/ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json` |
| `--route-envelope` | `artifacts/ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json` |
| `--gpu59-receipt` | `artifacts/ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json` |
| `--gpu58-receipt` | `artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json` |
| `--expected-route-id` | `ash-basetrain-gpu-60-runtime-candidate-route-0000` |
| `--expected-route-kind` | `approved_surface_runtime_candidate_route` |
| `--expected-route-state` | `preflight_only` |
| `--expected-route-scope` | `runtime_candidate_preflight_only` |
| `--expected-route-policy-id` | `ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply` |
| `--expected-surface-id` | `ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--binding-id` | `ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000` |
| `--binding-kind` | `non_default_runtime_candidate_binding_dryrun` |
| `--binding-state` | `dryrun_candidate` |
| `--binding-scope` | `dryrun_non_default_runtime_candidate_only` |
| `--binding-policy-id` | `ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-policy` |
| `--runtime-slot-id` | `shadow-runtime-candidate-slot-0000` |
| `--runtime-slot-state` | `candidate_only` |
| `--allow-runtime-default-apply` | `false` |
| `--allow-runtime-auto-bind` | `false` |
| `--allow-runtime-active-apply` | `false` |
| `--allow-live-inference-attach` | `false` |
| `--allow-logits-adoption` | `false` |
| `--allow-final-logits-claim` | `false` |
| `--allow-vocab-claim` | `false` |
| `--allow-loss` | `false` |
| `--allow-backward` | `false` |
| `--allow-optimizer` | `false` |
| `--allow-weight-mutation` | `false` |
| `--out-binding` | `artifacts/ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_61_FORWARD_CANDIDATE_RUNTIME_ROUTE_DRYRUN.json` |

---

## 5. Outputs

GPU-61 writes two JSON artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json
artifacts/ASH_BASETRAIN_GPU_61_FORWARD_CANDIDATE_RUNTIME_ROUTE_DRYRUN.json
```

GPU-61 must not write runtime default apply markers, runtime active binding markers, live inference binding markers, adopted logits artifacts, final logits artifacts, vocab compatibility artifacts, loss receipts, gradients, optimizer receipts, delta candidate packets, checkpoints, or new raw payload bytes.

---

## 6. PASS Conditions

GPU-61 PASS requires:

```text
gpu60_pass == true
gpu59_pass == true
route_envelope_exists == true
route_id matches expected route id
route_kind == approved_surface_runtime_candidate_route
route_state == preflight_only
route_scope == runtime_candidate_preflight_only
route_policy_id matches expected route policy id
surface_id matches expected surface id
payload_sha256 matches expected digest
binding_id is non-empty
binding_state == dryrun_candidate
binding_scope == dryrun_non_default_runtime_candidate_only
runtime_slot_state == candidate_only
runtime_binding_dryrun_created == true
runtime_binding_installed == false
runtime_auto_bind == false
runtime_default_apply == false
runtime_active_apply == false
live_inference_attach == false
logits_adoption_allowed == false
final_logits_claimed == false
vocab_compatibility_verified == false
loss/backward/optimizer/weight_mutation == false
```

---

## 7. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_61_forward_candidate_runtime_route_dryrun -- `
  --gpu60-receipt .\artifacts\ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json `
  --route-envelope .\artifacts\ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json `
  --gpu59-receipt .\artifacts\ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json `
  --gpu58-receipt .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json `
  --expected-route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --expected-route-kind approved_surface_runtime_candidate_route `
  --expected-route-state preflight_only `
  --expected-route-scope runtime_candidate_preflight_only `
  --expected-route-policy-id ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --binding-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000 `
  --binding-kind non_default_runtime_candidate_binding_dryrun `
  --binding-state dryrun_candidate `
  --binding-scope dryrun_non_default_runtime_candidate_only `
  --binding-policy-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-policy `
  --runtime-slot-id shadow-runtime-candidate-slot-0000 `
  --runtime-slot-state candidate_only `
  --out-binding .\artifacts\ASH_BASETRAIN_GPU_61_RUNTIME_BINDING_DRYRUN_DESCRIPTOR.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_61_FORWARD_CANDIDATE_RUNTIME_ROUTE_DRYRUN.json
```

---

## 8. Next Stage

After GPU-61 PASS:

```text
ASH-BASETRAIN-GPU-62
Forward Candidate Runtime Binding Registry Preflight /
Dryrun Binding Descriptor To Shadow Registry Candidate Seal
No Runtime Default Apply No Loss No Backward No Optimizer
```
