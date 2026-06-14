# ASH-BASETRAIN-GPU-68A SPEC

## Patch ID

ASH-BASETRAIN-GPU-68A

## Title

Default Runtime Token ID To Model Input Packet Preflight / Token Candidate To Tensor Envelope Seal

## Seal

No Forward / No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Purpose

GPU-68A consumes the GPU-67A token ID candidate envelope and creates a model input packet envelope. This patch creates tensor envelope metadata only. It must not allocate real tensor memory, create GPU buffers, run model forward, create logits, decode, sample, generate, compute loss, run backward, create optimizer state, or mutate weights.

## Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_67A_TOKENIZER_ENCODE_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
```

## Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_PREFLIGHT_RECEIPT.json
```

## State Ownership

GPU-68A owns only the model input packet envelope and model input packet preflight receipt. It does not own default pointer, ActiveDefault binding, resolved route view, tokenizer artifacts, actual model input tensor, forward, logits, decode, or generation state.

## Known 67A Input Values

```text
token_ids_candidate_count == 52
token_ids_candidate_min == 137
token_ids_candidate_max == 48210
token_ids_candidate_sha256 == a3ed47dc961578a7e43a667bbd318d656ef76f682d8325221dfb4e43c4ac05cc
token_ids_within_vocab_cap == true
```

## Model Input Packet Contract

GPU-68A creates this stage only:

```text
model_input_packet_stage == tensor_envelope_only_pre_forward
model_input_batch_size == 1
model_input_sequence_len == 52
model_input_token_id_dtype == u32
model_input_layout == batch_major_sequence
model_input_shape == [1, 52]
attention_mask_policy == metadata_only_all_tokens_attend
position_ids_policy == metadata_only_monotonic_zero_based
model_input_tensor_materialized == false
model_forward_used == false
```

## Metadata Only Token Candidate Policy

If the token ID array is present, GPU-68A validates array count, digest, min, max, and vocab range. If the token ID array is absent, GPU-68A may proceed only when `--allow-token-id-metadata-only true` is supplied. In metadata-only mode the envelope must record:

```text
token_ids_array_present == false
token_ids_metadata_only == true
model_input_tensor_materialized == false
model_forward_used == false
```

## Builder Contract

GPU-68A must use atlas grouped builders, serde_json::Map, match-based validation gates, lookup-table allowed dtype/layout values, lookup-table forbidden flags, and small object builders. It must not use one giant JSON macro object, manual JSON string assembly, recursion limit patching, or silent correction.

Required builder symbols:

```text
model_input_source_group
model_input_route_group
model_input_token_candidate_group
model_input_tensor_envelope_group
model_input_attention_position_group
model_input_forbidden_group
receipt_header_group
contract_validation_group
input_digests_group
forbidden_flag_pairs
allowed_dtype_table
allowed_layout_table
object
atlas_merge
```

## PASS Conditions

```text
token_id_candidate_exists == true
tokenizer_encode_receipt_exists == true
input_envelope_exists == true
resolved_route_view_exists == true
token_candidate.source_patch_id == ASH-BASETRAIN-GPU-67A
token_candidate.token_id_candidate_stage == token_ids_candidate_only
token_candidate.token_ids_candidate_count == 52
token_candidate.token_ids_candidate_sha256 == a3ed47dc961578a7e43a667bbd318d656ef76f682d8325221dfb4e43c4ac05cc
token_candidate.token_ids_candidate_min == 137
token_candidate.token_ids_candidate_max == 48210
token_candidate.token_ids_within_vocab_cap == true
model_input_shape == [1, 52]
model_input_tensor_materialized == false
model_forward_used == false
decode_used == false
sampling_used == false
generation_used == false
loss_used == false
backward_used == false
optimizer_used == false
weight_mutation_used == false
gpu_dispatch_used == false
model_input_packet_envelope_written == true
receipt_written == true
```

## Local Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_68a_model_input_packet_preflight -- `
  --token-id-candidate .\artifacts\ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json `
  --tokenizer-encode-receipt .\artifacts\ASH_BASETRAIN_GPU_67A_TOKENIZER_ENCODE_PREFLIGHT_RECEIPT.json `
  --input-envelope .\artifacts\ASH_BASETRAIN_GPU_66A_DEFAULT_RUNTIME_INPUT_PACKET_ENVELOPE.json `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --expected-token-id-candidate-envelope-id ash-basetrain-gpu-67a-token-id-candidate-envelope-0000 `
  --expected-input-packet-id ash-basetrain-gpu-66a-default-runtime-input-packet-0000 `
  --expected-resolved-route-view-id ash-basetrain-gpu-65a-resolved-default-route-view-0000 `
  --expected-token-ids-candidate-sha256 a3ed47dc961578a7e43a667bbd318d656ef76f682d8325221dfb4e43c4ac05cc `
  --expected-token-count 52 `
  --expected-token-id-min 137 `
  --expected-token-id-max 48210 `
  --expected-vocab-cap 48259 `
  --expected-model-input-batch-size 1 `
  --expected-model-input-sequence-len 52 `
  --model-input-token-id-dtype u32 `
  --model-input-layout batch_major_sequence `
  --allow-token-id-metadata-only true `
  --model-input-packet-envelope-id ash-basetrain-gpu-68a-model-input-packet-envelope-0000 `
  --out-model-input-packet .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_PREFLIGHT_RECEIPT.json
```

## Next Stage

ASH-BASETRAIN-GPU-69A / Default Runtime Model Input Packet Readonly Forward Preflight / Tensor Envelope To Forward Candidate Seal
