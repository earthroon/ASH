# ASH-BASETRAIN-GPU-59 SPEC

## Patch ID

`ASH-BASETRAIN-GPU-59`

## Title

Forward Candidate Operator Approval Gate / Shape-Compatible Surface Review To Explicit Human Approval Seal

## Seal

No Runtime Apply / No Logits Adoption / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-59` consumes the successful `ASH-BASETRAIN-GPU-58` surface compatibility gate and records an explicit operator approval decision for the shape-compatible, non-adopted logits surface candidate.

GPU-59 is an operator approval boundary. It may record `approved_for_next_stage`, `hold_review`, or `rejected`, but approval only permits a later preflight stage. Approval must not apply the surface to runtime inference, adopt logits, claim final logits, claim vocabulary compatibility, compute loss, run backward, create optimizer state, or mutate weights.

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-58` | surface shape policy compatibility SSOT |
| `ASH-BASETRAIN-GPU-59` | explicit operator approval envelope SSOT |
| `ASH-BASETRAIN-GPU-60` | post-approval bind preflight, not part of GPU-59 |

Primary input SSOT:

```text
artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json
artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_SHAPE_POLICY.json
artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json
```

Required GPU-58 facts:

```text
patch_id == ASH-BASETRAIN-GPU-58
pass == true
shape_policy_compatible == true
surface_descriptor_exists == true
surface_kind == non_adopted_logits_surface_shape_candidate
surface_state == review_required
payload_sha256 == expected_output_sha256
scalar_type == f32
endianness == little
rank == 1
shape == [512]
element_count == 512
finite_count == 512
nonfinite_count == 0
surface_values_embedded == false
final_logits_claimed == false
vocab_compatibility != verified
logits_adopted == false
runtime_default_apply == false
runtime_adoption_allowed == false
loss/backward/optimizer/weight_mutation == false
```

Candidate digest SSOT:

```text
2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
```

---

## 3. Operator Decision Policy

Default policy:

```json
{
  "policy_id": "ash-basetrain-gpu-59-operator-approval-policy-no-runtime-apply",
  "policy_kind": "explicit_operator_approval_policy",
  "required_source_patch": "ASH-BASETRAIN-GPU-58",
  "required_source_pass": true,
  "required_surface_state_before_decision": "review_required",
  "allowed_operator_decisions": ["approved_for_next_stage", "rejected", "hold_review"],
  "default_operator_decision": "hold_review",
  "allow_runtime_apply": false,
  "allow_logits_adoption": false,
  "allow_final_logits_claim": false,
  "allow_vocab_compatibility_claim": false,
  "allow_loss": false,
  "allow_backward": false,
  "allow_optimizer": false,
  "allow_weight_mutation": false
}
```

Decision meaning:

| Decision | Meaning |
|---|---|
| `approved_for_next_stage` | operator allows the candidate to proceed to the next preflight stage only |
| `hold_review` | operator keeps the candidate in review state |
| `rejected` | operator rejects the candidate; no next-stage promotion |

---

## 4. Inputs

| Argument | Default |
|---|---|
| `--gpu58-receipt` | `artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json` |
| `--shape-policy` | `artifacts/ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_SHAPE_POLICY.json` |
| `--surface-descriptor` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json` |
| `--gpu57-receipt` | `artifacts/ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json` |
| `--gpu56-receipt` | `artifacts/ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json` |
| `--expected-surface-id` | `ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000` |
| `--expected-policy-id` | `ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--expected-surface-state` | `review_required` |
| `--expected-shape-policy-compatible` | `true` |
| `--operator-id` | `operator-local` |
| `--operator-label` | `local-reviewer` |
| `--operator-decision` | `approved_for_next_stage` |
| `--operator-note` | `shape-compatible surface reviewed; no runtime apply` |
| `--approval-scope` | `next_stage_preflight_only` |
| `--approval-envelope-id` | `ash-basetrain-gpu-59-operator-approval-envelope-0000` |
| `--allow-runtime-apply` | `false` |
| `--allow-logits-adoption` | `false` |
| `--allow-final-logits-claim` | `false` |
| `--allow-vocab-claim` | `false` |
| `--allow-loss` | `false` |
| `--allow-backward` | `false` |
| `--allow-optimizer` | `false` |
| `--allow-weight-mutation` | `false` |
| `--out-approval` | `artifacts/ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json` |

---

## 5. Outputs

GPU-59 writes two JSON artifacts:

```text
artifacts/ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json
```

GPU-59 must not write runtime apply markers, adopted logits artifacts, final logits artifacts, vocab compatibility artifacts, loss receipts, gradients, optimizer receipts, delta candidate packets, checkpoints, or new raw payload bytes.

---

## 6. PASS Conditions

GPU-59 PASS requires:

```text
gpu58_pass == true
gpu57_pass == true
gpu56_pass == true
shape_policy_compatible == true
surface_descriptor_exists == true
surface_id matches expected surface id
policy_id matches expected policy id
surface_state_before_decision == review_required
operator_decision is one of allowed decisions
operator_id is non-empty
approval_scope == next_stage_preflight_only
approval_envelope_written == true
runtime_apply_allowed == false
logits_adoption_allowed == false
final_logits_claimed == false
vocab_compatibility_verified == false
loss/backward/optimizer/weight_mutation == false
```

`next_stage_enabled == true` only when `operator_decision == approved_for_next_stage`.

---

## 7. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_59_forward_candidate_operator_approval_gate -- `
  --gpu58-receipt .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_COMPATIBILITY_GATE.json `
  --shape-policy .\artifacts\ASH_BASETRAIN_GPU_58_FORWARD_CANDIDATE_LOGITS_SURFACE_SHAPE_POLICY.json `
  --surface-descriptor .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT_DESCRIPTOR.json `
  --gpu57-receipt .\artifacts\ASH_BASETRAIN_GPU_57_FORWARD_CANDIDATE_LOGITS_SURFACE_PREFLIGHT.json `
  --gpu56-receipt .\artifacts\ASH_BASETRAIN_GPU_56_FORWARD_CANDIDATE_RAW_PAYLOAD_INTEGRITY_AUDIT.json `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-policy-id ash-basetrain-gpu-58-surface-shape-policy-f32x512-rank1 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --operator-id operator-local `
  --operator-label local-reviewer `
  --operator-decision approved_for_next_stage `
  --operator-note "shape-compatible surface reviewed; no runtime apply" `
  --approval-scope next_stage_preflight_only `
  --out-approval .\artifacts\ASH_BASETRAIN_GPU_59_OPERATOR_APPROVAL_ENVELOPE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_59_FORWARD_CANDIDATE_OPERATOR_APPROVAL_GATE.json
```

---

## 8. Next Stage

If `operator_decision == approved_for_next_stage`:

```text
ASH-BASETRAIN-GPU-60
Forward Candidate Post-Approval Bind Preflight /
Approved Surface To Explicit Runtime Candidate Route Seal
No Runtime Default Apply No Loss No Backward No Optimizer
```

If `operator_decision == hold_review`:

```text
ASH-BASETRAIN-GPU-59-R1
Operator Review Continuation / Approval Envelope Recheck No Runtime Apply Seal
```

If `operator_decision == rejected`, there is no next patch.
