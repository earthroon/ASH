# ASH-BASETRAIN-GPU-67A SPEC

## Patch ID

ASH-BASETRAIN-GPU-67A

## Title

Default Runtime Tokenizer Encode Preflight / Input Envelope To Token ID Candidate Seal

## Seal

No Decode / No Sampling / No Generation / No Forward / No Loss / No Backward / No Optimizer

## Purpose

GPU-67A consumes the GPU-66A-R1 pre-tokenization input packet envelope and creates a token ID candidate envelope. This is the first stage that may invoke tokenizer encode. It must not decode, sample, generate, run model forward, materialize model input tensors, compute loss, run backward, create optimizer state, mutate weights, dispatch GPU work, or attach live/production inference.

## Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
artifacts/ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json
```

## Tokenizer Binding SSOT

```text
tokenizer_v5/artifacts/tokenizer_manifest_v5_final.json
tokenizer_v5/artifacts/tokenizer_v5.model
```

The manifest is used for identity, vocab cap, valid token range, and compact summary sealing. The model path is digested as the encode runtime source. GPU-67A must not dump full vocab or full reserved token arrays into receipt output.

Confirmed tokenizer binding facts:

```text
tokenizer_id == tok_v5_48259_candidate
manifest_id == tok_v5_48259_candidate
tokenizer_spec_id == tokenizer_v5
runtime.decode_mode == sentencepiece_like
runtime.valid_token_id_range == [0, 48258]
vocab_size == 48259
```

## Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_67A_TOKENIZER_ENCODE_PREFLIGHT_RECEIPT.json
```

## State Ownership

GPU-67A owns only the token ID candidate envelope and tokenizer encode preflight receipt. It does not own default pointer, ActiveDefault binding, resolved route view, input packet envelope, tokenizer source artifacts, model input tensor, forward, logits, decode, or generation state.

## Candidate Contract

Required candidate state:

```text
tokenizer_encode_used == true
tokenizer_encode_candidate_created == true
token_ids_candidate_materialized == true
token_ids_candidate_count >= 1
token_ids_candidate_sha256 is computed
token_ids_candidate_min >= 0
token_ids_candidate_max <= 48258
token_ids_vocab_cap_checked == true
token_ids_within_vocab_cap == true
token_ids_committed_to_model_input == false
token_tensor_materialized == false
model_input_tensor_materialized == false
model_forward_used == false
```

## Builder Contract

GPU-67A must use atlas grouped builders, serde_json::Map, match-based validation gates, and lookup-table forbidden flags. It must not use one giant serde_json macro object, manual JSON string assembly, or silent correction.

Required builder symbols:

```text
candidate_source_group
candidate_route_group
candidate_input_group
candidate_tokenizer_summary_group
candidate_token_ids_group
candidate_forbidden_group
receipt_header_group
contract_validation_group
input_digests_group
forbidden_flag_pairs
object
atlas_merge
```

## PASS Conditions

```text
input_envelope_exists == true
input_preflight_receipt_exists == true
resolved_route_view_exists == true
route_probe_receipt_exists == true
tokenizer_binding_exists == true
tokenizer_model_exists == true
input_envelope.source_patch_id == ASH-BASETRAIN-GPU-66A-R1
input_envelope.input_packet_stage == pre_tokenization_envelope_only
input_envelope.input_text_sha256 == 0d403caa8f68ccab60a27a4545696cf94bf1bee613efea2d5192a78e032a4efe
input_preflight_receipt.patch_id == ASH-BASETRAIN-GPU-66A-R1
input_preflight_receipt.pass == true
tokenizer_manifest.tokenizer_id == tok_v5_48259_candidate
tokenizer_manifest.manifest_id == tok_v5_48259_candidate
tokenizer_manifest.tokenizer_spec_id == tokenizer_v5
tokenizer_manifest.vocab_size == 48259
tokenizer_manifest.runtime.valid_token_id_range == [0, 48258]
full_vocab_dumped_to_receipt == false
token_ids_candidate_count >= 1
token_ids_within_vocab_cap == true
decode_used == false
sampling_used == false
generation_used == false
model_forward_used == false
loss_used == false
backward_used == false
optimizer_used == false
weight_mutation_used == false
gpu_dispatch_used == false
```

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_67a_tokenizer_encode_preflight -- `
  --input-envelope .\artifacts\ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json `
  --input-preflight-receipt .\artifacts\ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_PREFLIGHT_RECEIPT.json `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --route-probe-receipt .\artifacts\ASH_BASETRAIN_GPU_65A_DEFAULT_RUNTIME_ROUTE_PROBE_RECEIPT.json `
  --tokenizer-binding .\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json `
  --tokenizer-model .\tokenizer_v5\artifacts\tokenizer_v5.model `
  --input-text "ASH default runtime input packet preflight fixture." `
  --expected-input-text-sha256 0d403caa8f68ccab60a27a4545696cf94bf1bee613efea2d5192a78e032a4efe `
  --expected-input-text-byte-len 51 `
  --expected-vocab-cap 48259 `
  --expected-token-id-min 0 `
  --expected-token-id-max 48258 `
  --out-token-id-candidate .\artifacts\ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_67A_TOKENIZER_ENCODE_PREFLIGHT_RECEIPT.json
```

## Next Stage

ASH-BASETRAIN-GPU-68A / Default Runtime Token ID To Model Input Packet Preflight / Token Candidate To Tensor Envelope Seal