# ASH-BASETRAIN-GPU-66A SPEC

## Patch ID

`ASH-BASETRAIN-GPU-66A`

## Title

Default Runtime Input Packet Preflight / Readonly Pointer-Resolved Route To First Input Envelope Seal

## Seal

No Generation / No Decode / No Sampling / No Loss / No Backward / No Optimizer

---

## 1. Purpose

`ASH-BASETRAIN-GPU-66A` consumes the `ASH-BASETRAIN-GPU-65A` readonly default route resolution proof and creates the first default runtime input packet envelope.

GPU-66A is pre-tokenization only. It does not tokenize input text, decode tokens, sample tokens, run model forward, generate text, compute loss, run backward, create optimizer state, or mutate weights.

The intended transition is:

```text
resolved default runtime route
-> first input packet envelope
```

Not:

```text
resolved default runtime route
-> token ids
-> model input tensor
-> forward
-> logits
-> decode
-> generation
```

---

## 2. SSOT

| Layer | Ownership |
|---|---|
| `ASH-BASETRAIN-GPU-64A` | ActiveDefault binding and runtime default pointer SSOT |
| `ASH-BASETRAIN-GPU-65A` | readonly default runtime route resolution proof SSOT |
| `ASH-BASETRAIN-GPU-66A` | default runtime input packet envelope SSOT |
| `ASH-BASETRAIN-GPU-67A` | tokenizer encode preflight, not part of 66A |

### Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
artifacts/ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json
artifacts/ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json
```

### Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_PREFLIGHT_RECEIPT.json
```

GPU-66A owns only the input packet envelope and preflight receipt. It does not own default pointer state, ActiveDefault binding state, route resolution state, tokenizer state, or model input tensor state.

---

## 3. Required 65A Input Facts

GPU-66A must validate the 65A route view:

```text
route_view.resolved_route_view_id == ash-basetrain-gpu-65a-resolved-default-route-view-0000
route_view.resolution_kind == readonly_default_pointer_to_runtime_route_resolution
route_view.readonly_probe == true
route_view.default_pointer_id == ash-basetrain-gpu-runtime-default-pointer-0000
route_view.active_default_binding_id == ash-basetrain-gpu-64a-active-default-runtime-binding-0000
route_view.binding_state == ActiveDefault
route_view.source_active_binding_id == ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000
route_view.source_binding_id == ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000
route_view.source_route_id == ash-basetrain-gpu-60-runtime-candidate-route-0000
route_view.source_surface_id == ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000
route_view.lineage_depth == full_runtime_route_chain
route_view.lineage_complete == true
route_view.payload_sha256 == 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33
route_view.runtime_default_apply == true
route_view.runtime_active_apply == true
route_view.runtime_auto_bind == false
route_view.production_attach == false
route_view.live_inference_attach == false
route_view.generation_used == false
route_view.decode_used == false
route_view.sampling_used == false
route_view.loss_used == false
route_view.backward_used == false
route_view.optimizer_used == false
route_view.weight_mutation_used == false
```

GPU-66A must validate the 65A receipt:

```text
route_probe_receipt.patch_id == ASH-BASETRAIN-GPU-65A
route_probe_receipt.pass == true
route_probe_receipt.verdict == PASS
route_probe_receipt.contract_validation.pointer_target_match == true
route_probe_receipt.contract_validation.route_lineage_match == true
route_probe_receipt.route_resolution.lineage_complete == true
route_probe_receipt.route_resolution.lineage_depth == full_runtime_route_chain
route_probe_receipt.route_resolution.route_view_written == true
```

---

## 4. Input Packet Envelope Contract

GPU-66A creates only an input packet envelope:

```text
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json
```

Required envelope state:

```text
input_packet_kind == default_runtime_first_input_envelope
input_packet_stage == pre_tokenization_envelope_only
input_fixture_kind in [static_text_reference, static_text_inline, operator_supplied_text_fixture]
input_text_sha256 is computed
input_text_byte_len is recorded
tokenization_allowed == false
tokenizer_encode_used == false
token_ids_materialized == false
token_tensor_materialized == false
model_input_tensor_materialized == false
model_forward_used == false
generation_used == false
decode_used == false
sampling_used == false
loss/backward/optimizer/weight_mutation == false
envelope_written == true
```

---

## 5. Inputs

| Argument | Default |
|---|---|
| `--resolved-route-view` | `artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json` |
| `--route-probe-receipt` | `artifacts/ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json` |
| `--default-pointer` | `artifacts/ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json` |
| `--active-default-binding` | `artifacts/ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json` |
| `--expected-resolved-route-view-id` | `ash-basetrain-gpu-65a-resolved-default-route-view-0000` |
| `--expected-default-pointer-id` | `ash-basetrain-gpu-runtime-default-pointer-0000` |
| `--expected-active-default-binding-id` | `ash-basetrain-gpu-64a-active-default-runtime-binding-0000` |
| `--expected-source-active-binding-id` | `ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000` |
| `--expected-source-binding-id` | `ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000` |
| `--expected-route-id` | `ash-basetrain-gpu-60-runtime-candidate-route-0000` |
| `--expected-surface-id` | `ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000` |
| `--expected-output-sha256` | `2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33` |
| `--input-packet-id` | `ash-basetrain-gpu-66a-default-runtime-input-packet-0000` |
| `--input-fixture-id` | `ash-basetrain-gpu-66a-static-text-fixture-0000` |
| `--input-fixture-kind` | `static_text_reference` |
| `--input-text` | `ASH default runtime input packet preflight fixture.` |
| `--out-envelope` | `artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json` |
| `--out` | `artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_PREFLIGHT_RECEIPT.json` |

---

## 6. Outputs

GPU-66A writes:

```text
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_PREFLIGHT_RECEIPT.json
```

No `.sha256` sidecar files.

---

## 7. Must Not Write or Mutate

GPU-66A must not write tokenizer encode artifacts, token id packets, token tensor packets, model input tensor packets, attention masks, position ids, forward receipts, logits artifacts, decoded token artifacts, generated text artifacts, sampling candidate artifacts, loss receipts, gradient receipts, optimizer receipts, delta candidate packets, weight checkpoints, production attach markers, live inference attach markers, runtime auto-bind markers, raw payload binaries, full tensor artifacts, or unselected group artifacts.

GPU-66A must not mutate the runtime default pointer, 64A ActiveDefault binding, 65A route view, or 65A route probe receipt.

---

## 8. Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_66a_default_input_packet_preflight -- `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --route-probe-receipt .\artifacts\ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json `
  --default-pointer .\artifacts\ASH_BASETRAIN_GPU_RUNTIME_DEFAULT_POINTER.json `
  --active-default-binding .\artifacts\ASH_BASETRAIN_GPU_64A_ACTIVE_DEFAULT_BINDING.json `
  --expected-resolved-route-view-id ash-basetrain-gpu-65a-resolved-default-route-view-0000 `
  --expected-default-pointer-id ash-basetrain-gpu-runtime-default-pointer-0000 `
  --expected-active-default-binding-id ash-basetrain-gpu-64a-active-default-runtime-binding-0000 `
  --expected-source-active-binding-id ash-basetrain-gpu-63a-active-non-default-runtime-binding-0000 `
  --expected-source-binding-id ash-basetrain-gpu-61-non-default-runtime-binding-dryrun-0000 `
  --expected-route-id ash-basetrain-gpu-60-runtime-candidate-route-0000 `
  --expected-surface-id ash-basetrain-gpu-57-logits-surface-candidate-identity-copy-0000 `
  --expected-output-sha256 2c2cd128cde79af49eec8824e17d785eb40286968181fae096daf2b0029d6a33 `
  --input-packet-id ash-basetrain-gpu-66a-default-runtime-input-packet-0000 `
  --input-fixture-id ash-basetrain-gpu-66a-static-text-fixture-0000 `
  --input-fixture-kind static_text_reference `
  --input-text "ASH default runtime input packet preflight fixture." `
  --out-envelope .\artifacts\ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_PREFLIGHT_RECEIPT.json
```

---

## 9. Implementation Files

```text
crates/base_train/src/ash_basetrain_gpu_66a_default_input_packet_preflight.rs
crates/base_train/src/bin/ash_basetrain_gpu_66a_default_input_packet_preflight.rs
```

---

## 10. Next Stage

If GPU-66A PASS:

```text
ASH-BASETRAIN-GPU-67A
Default Runtime Tokenizer Encode Preflight / Input Envelope To Token ID Candidate Seal
No Decode No Sampling No Generation No Forward No Loss No Backward No Optimizer
```

If GPU-66A BLOCKED due to envelope shape:

```text
ASH-BASETRAIN-GPU-66A-R1
Input Packet Envelope Shape Rebind / Fixture Hash And Pre-Tokenization Boundary Closure Seal
```