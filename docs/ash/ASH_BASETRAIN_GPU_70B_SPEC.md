# ASH-BASETRAIN-GPU-70B SPEC

## Patch ID

ASH-BASETRAIN-GPU-70B

## Title

Native Runtime Forward Path Selection / Select A-SFT Hidden Provider And Native Atlas FFN Probe Seal

## Seal

No Forward / No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Purpose

GPU-70B consumes the GPU-69A readonly forward candidate envelope and selects the next executable native runtime paths. This patch does not execute forward, does not execute A-SFT hidden provider, does not execute native atlas FFN, and does not materialize hidden, FFN output, or logits. It only creates a path selection envelope for later stages.

Selected paths:

```text
a_sft_batched_hidden_provider
native_atlas_ffn_single_token
```

## Input SSOT

```text
artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
```

## Output SSOT

```text
artifacts/ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json
artifacts/ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION_RECEIPT.json
```

## State Ownership

GPU-70B owns native forward path selection envelope, path selection receipt, selected path IDs, and next-stage execution allowance flags. GPU-70B does not own actual hidden provider execution, actual FFN execution, logits probe, decoded token state, sampling state, generation state, loss/backward/optimizer state, weight mutation state, or production runtime attach state.

## Required 69A Input Facts

```text
patch_id == ASH-BASETRAIN-GPU-69A
verdict == PASS
pass == true
readonly_forward_candidate_stage == forward_candidate_pre_execution_only
forward_candidate_mode == readonly_pre_execution
readonly_forward_preflight_used == true
readonly_forward_candidate_created == true
forward_execution_allowed_next_stage == true
model_forward_executed == false
model_forward_used == false
logits_materialized == false
logits_adopted == false
final_logits_claimed == false
```

## Native Path Inventory Contract

GPU-70B inventories existing native runtime path candidates without executing them. Required selected path candidates:

```text
a_sft_batched_hidden_provider
native_atlas_ffn_single_token
```

Optional observed non-selected candidates:

```text
native_wgpu_model_full_checkpoint
module_local_packed_half_gpu_lease
lm_head_vocab_atlas_gpu_sft
```

Each path record must include path_id, path_kind, source_crate, source_module_hint, selected_for_next_stage, execution_allowed_next_stage, execution_executed, expected_next_patch, and output_kind_next_stage where applicable.

## Selected Path Contract

A-SFT hidden provider path:

```text
path_id == a_sft_batched_hidden_provider
path_kind == batched_hidden_provider
source_crate == lora_train
source_module_hint == a_sft_batched_hidden_provider
expected_next_patch == ASH-BASETRAIN-GPU-70C
output_kind_next_stage == hidden_probe
logits_expected == false
decode_allowed == false
training_allowed == false
```

Native atlas FFN path:

```text
path_id == native_atlas_ffn_single_token
path_kind == native_atlas_ffn_probe
source_crate == burn_webgpu_backend
source_module_hint == native_atlas_ffn
expected_next_patch == ASH-BASETRAIN-GPU-70D
output_kind_next_stage == ffn_output_probe
full_model_forward_claimed == false
logits_expected == false
decode_allowed == false
training_allowed == false
```

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70b_native_forward_path_selection -- `
  --readonly-forward-candidate .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json `
  --readonly-forward-preflight-receipt .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json `
  --model-input-packet .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json `
  --token-id-candidate .\artifacts\ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --expected-readonly-forward-candidate-envelope-id ash-basetrain-gpu-69a-readonly-forward-candidate-envelope-0000 `
  --expected-model-input-packet-envelope-id ash-basetrain-gpu-68a-model-input-packet-envelope-0000 `
  --expected-token-id-candidate-envelope-id ash-basetrain-gpu-67a-token-id-candidate-envelope-0000 `
  --expected-selected-path a_sft_batched_hidden_provider `
  --expected-selected-path native_atlas_ffn_single_token `
  --native-forward-path-selection-id ash-basetrain-gpu-70b-native-forward-path-selection-0000 `
  --out-selection .\artifacts\ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION_RECEIPT.json
```

## PASS Conditions

```text
readonly_forward_candidate_exists == true
readonly_forward_preflight_receipt_exists == true
model_input_packet_exists == true
token_id_candidate_exists == true
resolved_route_view_exists == true
readonly_forward_preflight_receipt.patch_id == ASH-BASETRAIN-GPU-69A
readonly_forward_preflight_receipt.pass == true
readonly_forward_preflight_receipt.verdict == PASS
readonly_forward_candidate.forward_candidate_mode == readonly_pre_execution
readonly_forward_candidate.forward_execution_allowed_next_stage == true
readonly_forward_candidate.model_forward_executed == false
readonly_forward_candidate.logits_materialized == false
selected_path_count == 2
selected_path_ids contains a_sft_batched_hidden_provider
selected_path_ids contains native_atlas_ffn_single_token
selected_paths_match_expected == true
path_inventory_created == true
path_selection_created == true
execution_allowed_next_stage == true
forward_executed == false
hidden_provider_executed == false
ffn_probe_executed == false
logits_materialized == false
decode_used == false
sampling_used == false
generation_used == false
loss_used == false
backward_used == false
optimizer_used == false
weight_mutation_used == false
silent_correction_used == false
selection_written == true
receipt_written == true
```

## BLOCK Conditions

```text
MISSING_READONLY_FORWARD_CANDIDATE
MISSING_READONLY_FORWARD_PREFLIGHT_RECEIPT
MISSING_MODEL_INPUT_PACKET
MISSING_TOKEN_ID_CANDIDATE
MISSING_RESOLVED_ROUTE_VIEW
READONLY_FORWARD_PREFLIGHT_RECEIPT_NOT_PASS
UPSTREAM_FORWARD_ALREADY_EXECUTED
UPSTREAM_LOGITS_ALREADY_MATERIALIZED
SELECTED_PATH_COUNT_MISMATCH
SELECTED_PATH_MISSING_ASFT_HIDDEN_PROVIDER
SELECTED_PATH_MISSING_NATIVE_ATLAS_FFN
SELECTED_PATH_UNSUPPORTED
SELECTED_PATH_DUPLICATE
PATH_SELECTION_SILENT_CORRECTION_DETECTED
FORWARD_EXECUTION_DETECTED
HIDDEN_PROVIDER_EXECUTION_DETECTED
FFN_PROBE_EXECUTION_DETECTED
LOGITS_MATERIALIZATION_DETECTED
DECODE_DETECTED
SAMPLING_DETECTED
GENERATION_DETECTED
LOSS_BACKWARD_OPTIMIZER_DETECTED
WEIGHT_MUTATION_DETECTED
GPU_OPERATION_DETECTED
PRODUCTION_ATTACH_DETECTED
LIVE_INFERENCE_ATTACH_DETECTED
RUNTIME_AUTO_BIND_DETECTED
SELECTION_WRITE_FAILED
RECEIPT_WRITE_FAILED
```

## Static Checks

```text
module_file_exists == true
bin_file_exists == true
lib_export_added == true
cargo_bin_added == true
spec_file_exists == true
atlas_grouped_builder_present == true
map_builder_present == true
lookup_table_selected_paths_present == true
lookup_table_forbidden_flags_present == true
match_validation_present == true
large_json_macro_absent == true
recursion_limit_absent == true
asft_hidden_provider_selected == true
native_atlas_ffn_selected == true
path_selection_only_no_execution_present == true
forward_execution_forbidden == true
hidden_provider_execution_forbidden == true
ffn_probe_execution_forbidden == true
logits_materialization_forbidden == true
decode_forbidden == true
sampling_forbidden == true
generation_forbidden == true
loss_backward_optimizer_forbidden == true
weight_mutation_forbidden == true
no_sha256_sidecar_files_created == true
```

## Next Stage

```text
ASH-BASETRAIN-GPU-70C
A-SFT Batched Hidden Provider Readonly Smoke / Forward Candidate To Hidden Probe Receipt Seal
```

Parallel branch after 70C or after hidden output is available:

```text
ASH-BASETRAIN-GPU-70D
Native Atlas FFN Single Token Readonly Smoke / Hidden Probe To FFN Output Probe Seal
```
