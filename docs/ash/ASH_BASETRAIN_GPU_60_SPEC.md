# ASH-BASETRAIN-GPU-60 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-60`

## Title

Forward Candidate Post-Approval Bind Preflight / Approved Surface To Explicit Runtime Candidate Route Seal

## Seal

No Runtime Default Apply / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-60` consumes the successful `ASH-BASETRAIN-GPU-59` operator approval gate and creates an explicit runtime candidate route preflight envelope.

GPU-60 proves that the approved surface has a route envelope for a later runtime dryrun stage. It does not activate the route, make it default, adopt logits, claim final logits, verify vocabulary compatibility, compute loss, run backward, create optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-59` | explicit operator approval envelope SSOT |
| `ASH-BASETRAIN-GPU-60` | post-approval runtime candidate route preflight SSOT |
| `ASH-BASETRAIN-GPU-61` | runtime route dryrun, not part of GPU-60 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json
artifacts/ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json
artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json
```

Required GPU-59 facts:

```text
patch_id == ASH-BASETRAIN-GPU-59
pass == true
operator_decision == approved_for_next_stage
approval_scope == next_stage_preflight_only
surface_state_after_decision == approved_for_next_stage
next_stage_enabled == true
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

---

## 3. Runtime Candidate Route Policy

Default route policy:

```json
{
  "route_policy_id": "ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply",
  "route_policy_kind": "approved_surface_to_runtime_candidate_route_policy",
  "required_source_patch": "ASH-BASETRAIN-GPU-59",
  "required_operator_decision": "approved_for_next_stage",
  "required_surface_state": "approved_for_next_stage",
  "route_scope": "runtime_candidate_preflight_only",
  "allow_runtime_default_apply": false,
  "allow_runtime_auto_bind": false,
  "allow_logits_adoption": false,
  "allow_final_logits_claim": false,
  "allow_vocab_compatibility_claim": false,
  "allow_loss": false,
  "allow_backward": false,
  "allow_optimizer": false,
  "allow_weight_mutation": false
}
```

GPU-60 may create a route envelope. GPU-60 must not activate the route.

---

## 4. Inputs

| Argument | Default |
|---|---|
| `--gpu59-receipt` | `artifacts/ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json` |
| `--approval-envelope` | `artifacts/ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json` |
| `--gpu58-receipt` | `artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json` |
| `--surface-descriptor` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json` |
| `--expected-surface-id` | `ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000` |
| `--expected-policy-id` | `ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1` |
| `--expected-approval-envelope-id` | `ash-basetrain-gpu-59-operator-approval-envelope-0000` |
| `--expected-operator-decision` | `approved_for_next_stage` |
| `--expected-approval-scope` | `next_stage_preflight_only` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--route-id` | `ash-basetrain-gpu-60-runtime-candidate-route-0000` |
| `--route-kind` | `approved_surface_runtime_candidate_route` |
| `--route-state` | `preflight_only` |
| `--route-scope` | `runtime_candidate_preflight_only` |
| `--route-policy-id` | `ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply` |
| `--allow-runtime-default-apply` | `false` |
| `--allow-runtime-auto-bind` | `false` |
| `--allow-logits-adoption` | `false` |
| `--allow-final-logits-claim` | `false` |
| `--allow-vocab-claim` | `false` |
| `--allow-loss` | `false` |
| `--allow-backward` | `false` |
| `--allow-optimizer` | `false` |
| `--allow-weight-mutation` | `false` |
| `--out-route` | `artifacts/ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json` |

---

## 5. Outputs

GPU-60 writes two JSON artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json
```

GPU-60 must not write runtime apply markers, runtime default route markers, active runtime bindings, adopted logits artifacts, final logits artifacts, vocab compatibility artifacts, loss receipts, gradients, optimizer receipts, delta candidate packets, checkpoints, or new raw payload bytes.

---

## 6. PASS Conditions

GPU-60 PASS requires:

```text
gpu59_pass == true
gpu58_pass == true
operator_decision == approved_for_next_stage
approval_scope == next_stage_preflight_only
approval_envelope_id matches expected approval envelope id
surface_id matches expected surface id
policy_id matches expected policy id
payload_sha256 matches expected digest
route_id is non-empty
route_state == preflight_only
route_scope == runtime_candidate_preflight_only
runtime_candidate_route_created == true
runtime_auto_bind == false
runtime_default_apply == false
runtime_apply_allowed == false
logits_adoption_allowed == false
final_logits_claimed == false
vocab_compatibility_verified == false
loss/backward/optimizer/weight_mutation == false
```

---

## 7. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_60_forward_candidate_post_approval_bind_preflight -- `
  --gpu59-receipt .\artifacts\ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json `
  --approval-envelope .\artifacts\ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json `
  --gpu58-receipt .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json `
  --surface-descriptor .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-policy-id ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1 `
  --expected-approval-envelope-id ash-basetrain-gpu-59-operator-approval-envelope-0000 `
  --expected-operator-decision approved_for_next_stage `
  --expected-approval-scope next_stage_preflight_only `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --route-kind approved_surface_runtime_candidate_route `
  --route-state preflight_only `
  --route-scope runtime_candidate_preflight_only `
  --route-policy-id ash-basetrain-gpu-60-runtime-candidate-route-policy-no-default-apply `
  --out-route .\artifacts\ASH_BASETRAIN_GPU_60_RUNTIME_CANDIDATE_ROUTE_ENVELOPE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_60_FORWARD_CANDIDATE_POST_APPROVAL_BIND_PREFLIGHT.json
```

---

## 8. Next Stage

After GPU-60 PASS:

```text
ASH-BASETRAIN-GPU-61
Forward Candidate Runtime Route Dryrun /
Candidate Route Envelope To Non-Default Runtime Binding Probe Seal
No Runtime Default Apply No Loss No Backward No Optimizer
```
