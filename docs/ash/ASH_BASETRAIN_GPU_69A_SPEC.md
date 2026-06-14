# ASH-BASETRAIN-GPU-69A SPEC

## Patch ID

ASH-BASETRAIN-GPU-69A

## Title

Default Runtime Model Input Packet Readonly Forward Preflight / Tensor Envelope To Forward Candidate Seal

## Seal

No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Purpose

GPU-69A consumes the GPU-68A model input packet envelope and creates a readonly forward candidate envelope. This patch is forward preflight only. It creates a forward-readiness candidate contract and does not execute forward, materialize logits, decode, sample, generate, compute loss, run backward, create optimizer state, mutate weights, acquire GPU, or dispatch GPU work.

## Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_67A_TOKENIZER_ENCODE_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
```

## Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json
```

## Known 68A Input Facts

```text
model_input_packet_stage == tensor_envelope_only_pre_forward
model_input_batch_size == 1
model_input_sequence_len == 52
model_input_shape == [1, 52]
model_input_token_id_dtype == u32
model_input_layout == batch_major_sequence
model_input_shape_verified == true
model_input_tensor_materialized == false
model_forward_used == false
token_ids_candidate_count == 52
token_ids_candidate_sha256 == a3ed47dc961578a7e43a667bbd318d656ef76f682d8325221dfb4e43c4ac05cc
token_ids_within_vocab_cap == true
```

## Readonly Forward Candidate Contract

GPU-69A writes a readonly forward candidate envelope with:

```text
readonly_forward_candidate_stage == forward_candidate_pre_execution_only
forward_candidate_mode == readonly_pre_execution
readonly_forward_preflight_used == true
readonly_forward_candidate_created == true
forward_execution_allowed_next_stage == true
model_forward_executed == false
logits_materialized == false
logits_adopted == false
final_logits_claimed == false
```

This envelope is not logits, decoded text, a sampled token, a generated sequence, loss, gradients, optimizer state, or weight delta.

## Builder Contract

GPU-69A must use atlas grouped builders, serde_json::Map, match-based validation gates, lookup-table allowed forward modes, lookup-table allowed dtype/layout values, lookup-table forbidden flags, and small object builders. It must not use one giant JSON macro object, manual JSON string assembly, recursion limit patching, or silent correction.

Required builder symbols:

```text
forward_source_group
forward_route_group
forward_token_candidate_group
forward_model_input_group
forward_attention_position_group
forward_candidate_mode_group
forward_forbidden_group
receipt_header_group
contract_validation_group
input_digests_group
forbidden_flag_pairs
allowed_forward_mode_table
allowed_dtype_table
allowed_layout_table
object
atlas_merge
```

## PASS Conditions

```text
model_input_packet_exists == true
model_input_preflight_receipt_exists == true
token_id_candidate_exists == true
tokenizer_encode_receipt_exists == true
resolved_route_view_exists == true
model_input_receipt.patch_id == ASH-BASETRAIN-GPU-68A
model_input_receipt.pass == true
model_input_receipt.verdict == PASS
model_input_packet.model_input_packet_stage == tensor_envelope_only_pre_forward
model_input_packet.model_input_batch_size == 1
model_input_packet.model_input_sequence_len == 52
model_input_packet.model_input_shape == [1, 52]
model_input_packet.model_input_token_id_dtype == u32
model_input_packet.model_input_layout == batch_major_sequence
model_input_packet.model_input_shape_verified == true
model_input_packet.model_input_tensor_materialized == false
token_candidate.token_ids_candidate_count == 52
token_candidate.token_ids_candidate_sha256 == a3ed47dc961578a7e43a667bbd318d656ef76f682d8325221dfb4e43c4ac05cc
token_candidate.token_ids_within_vocab_cap == true
route_lineage_complete == true
route_lineage_match == true
forward_candidate_mode == readonly_pre_execution
readonly_forward_candidate_created == true
model_forward_executed == false
logits_materialized == false
decode_used == false
sampling_used == false
generation_used == false
loss_used == false
backward_used == false
optimizer_used == false
weight_mutation_used == false
gpu_dispatch_used == false
readonly_forward_candidate_envelope_written == true
receipt_written == true
```

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_69a_readonly_forward_preflight -- `
  --model-input-packet .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json `
  --model-input-preflight-receipt .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_PREFLIGHT_RECEIPT.json `
  --token-id-candidate .\artifacts\ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json `
  --tokenizer-encode-receipt .\artifacts\ASH_BASETRAIN_GPU_67A_TOKENIZER_ENCODE_PREFLIGHT_RECEIPT.json `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --expected-model-input-packet-envelope-id ash-basetrain-gpu-68a-model-input-packet-envelope-0000 `
  --expected-token-id-candidate-envelope-id ash-basetrain-gpu-67a-token-id-candidate-envelope-0000 `
  --expected-resolved-route-view-id ash-basetrain-gpu-65a-resolved-default-route-view-0000 `
  --expected-token-ids-candidate-sha256 a3ed47dc961578a7e43a667bbd318d656ef76f682d8325221dfb4e43c4ac05cc `
  --expected-token-count 52 `
  --expected-model-input-batch-size 1 `
  --expected-model-input-sequence-len 52 `
  --expected-model-input-token-id-dtype u32 `
  --expected-model-input-layout batch_major_sequence `
  --forward-candidate-mode readonly_pre_execution `
  --readonly-forward-candidate-envelope-id ash-basetrain-gpu-69a-readonly-forward-candidate-envelope-0000 `
  --out-forward-candidate .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json
```

## Next Stage

ASH-BASETRAIN-GPU-70A / Default Runtime First Readonly Forward Smoke / Forward Candidate To Logits Probe Seal
