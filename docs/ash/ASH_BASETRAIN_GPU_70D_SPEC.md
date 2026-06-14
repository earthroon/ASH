# ASH-BASETRAIN-GPU-70D SPEC

## Patch ID
ASH-BASETRAIN-GPU-70D

## Title
Native Atlas FFN Single Token Readonly Smoke / Hidden Probe To FFN Output Probe Seal

## Seal
No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Purpose
GPU-70D consumes the GPU-70C A-SFT hidden provider probe and executes only the selected `native_atlas_ffn_single_token` path as a readonly FFN smoke. The output is an FFN output probe envelope. It is not LM-head logits, decoded text, sampling state, generation state, loss, gradients, optimizer state, or weight mutation.

GPU-70D must not claim full transformer forward, attention execution, LM-head execution, full model forward, final logits, or runtime adoption.

## Input SSOT
```text
artifacts/ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_PROBE.json
artifacts/ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_SMOKE_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json
artifacts/ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json
artifacts/ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json
```

## Runtime Inputs
Default runtime inputs:
```text
specs/model_spec_v5_48259.toml
tokenizer_v5/artifacts/ash_v5_native_genesis.forge01_smoke.safetensors
```
The runtime checkpoint is operator-local and may be absent from the baked ZIP. If the runtime model spec or checkpoint is missing, GPU-70D blocks with `FFN_RUNTIME_INPUT_MISSING` and does not fake an FFN probe.

## Output SSOT
```text
artifacts/ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_OUTPUT_PROBE.json
artifacts/ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_SMOKE_RECEIPT.json
```

## State Ownership
GPU-70D owns the native atlas FFN smoke receipt, FFN output probe envelope, selected hidden position metadata, hidden input source mode, FFN output shape metadata, FFN finite-check result, FFN output digest, and native atlas FFN backend evidence.

GPU-70D does not own 70C hidden provider probe provenance, 70B path selection, 69A readonly forward candidate, 68A model input packet, 67A token ID candidate, 65A resolved route view, LM-head execution, logits probe, decode, sampling, generation, loss, backward, optimizer, weight mutation, or production attach state.

## Required Upstream Facts
GPU-70D requires GPU-70C PASS with backend `native_wgpu_batched`, runtime label `native_wgpu_padded_hidden`, hidden shape `[1, 52, 2048]`, finite check PASS, zero NaN/Inf, metadata-only hidden probe policy, and all forbidden paths false.

GPU-70D requires GPU-70B selected paths to include `native_atlas_ffn_single_token` and `a_sft_batched_hidden_provider`.

## Hidden Input Source Contract
The GPU-70C hidden probe is metadata-only. GPU-70D must not treat the 70C hidden probe artifact as raw hidden tensor payload.

Default hidden input source mode:
```text
rehydrate_single_position_from_asft_provider
```
Required token position:
```text
selected_token_position_policy == last_non_padding_token
selected_token_position_index == 51
```
For batch size 1 and sequence length 52, index 51 is the final token position.

Forbidden hidden source behavior:
```text
metadata-only hidden probe treated as raw tensor
full hidden tensor dump required
hidden value source invented
hidden input silently zero-filled
hidden input silently randomized
hidden input silently repaired
```
Block code:
```text
HIDDEN_VALUE_SOURCE_INVALID
```

## Native Atlas FFN Contract
Expected source path:
```text
crates/burn_webgpu_backend/src/native_atlas_ffn.rs
```
Expected runtime family:
```text
NativeAtlasFfn16AfDispatcher
NativeAtlasFfn16AfWeights
dispatch_single_token_output_only
gate_weight
up_weight
down_weight
input_hidden
compute pipeline
dispatch_workgroups
queue.submit
readback
```

GPU-70D may execute only a native atlas FFN single-token readonly smoke. It must not claim full transformer block execution, attention execution, LM-head execution, full model forward, final logits, decoded output, training step, or optimizer update.

## FFN Output Probe Policy
The FFN output probe is metadata-only by default. It records output shape, dtype implication, finite check, NaN/Inf counts, FFN output digest, selected hidden input digest, backend evidence, and write receipt.

Required FFN output probe envelope ID:
```text
ash-basetrain-gpu-70d-native-atlas-ffn-output-probe-0000
```
Required backend:
```text
native_atlas_ffn16_af
```

No silent CPU/reference fallback is allowed. If fallback is required or detected, GPU-70D blocks with `SILENT_FFN_BACKEND_FALLBACK`.

## CLI
```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70d_native_atlas_ffn_smoke -- `
  --asft-hidden-provider-probe .\artifacts\ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_PROBE.json `
  --asft-hidden-provider-smoke-receipt .\artifacts\ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_SMOKE_RECEIPT.json `
  --native-forward-path-selection .\artifacts\ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json `
  --native-forward-path-selection-receipt .\artifacts\ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION_RECEIPT.json `
  --readonly-forward-candidate .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json `
  --readonly-forward-preflight-receipt .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json `
  --model-input-packet .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json `
  --token-id-candidate .\artifacts\ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --expected-hidden-probe-envelope-id ash-basetrain-gpu-70c-asft-hidden-provider-probe-0000 `
  --expected-native-forward-path-selection-id ash-basetrain-gpu-70b-native-forward-path-selection-0000 `
  --expected-readonly-forward-candidate-envelope-id ash-basetrain-gpu-69a-readonly-forward-candidate-envelope-0000 `
  --expected-model-input-packet-envelope-id ash-basetrain-gpu-68a-model-input-packet-envelope-0000 `
  --expected-token-id-candidate-envelope-id ash-basetrain-gpu-67a-token-id-candidate-envelope-0000 `
  --expected-selected-path native_atlas_ffn_single_token `
  --expected-token-count 52 `
  --expected-model-input-batch-size 1 `
  --expected-model-input-sequence-len 52 `
  --expected-hidden-size 2048 `
  --selected-token-position-policy last_non_padding_token `
  --selected-token-position-index 51 `
  --hidden-input-source-mode rehydrate_single_position_from_asft_provider `
  --ffn-backend native_atlas_ffn16_af `
  --ffn-probe-policy metadata_only_with_digest `
  --ffn-output-probe-envelope-id ash-basetrain-gpu-70d-native-atlas-ffn-output-probe-0000 `
  --model-spec .\specs\model_spec_v5_48259.toml `
  --checkpoint .\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors `
  --layer-index 0 `
  --out-ffn-output-probe .\artifacts\ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_OUTPUT_PROBE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_70D_NATIVE_ATLAS_FFN_SMOKE_RECEIPT.json
```

## PASS Conditions
GPU-70D PASS requires all input SSOT files, GPU-70C receipt PASS, hidden probe ID match, hidden shape `[1, 52, 2048]`, finite hidden probe, GPU-70B selected path `native_atlas_ffn_single_token`, explicit hidden input source mode, hidden input shape `[2048]`, non-empty hidden input digest, backend `native_atlas_ffn16_af`, successful FFN smoke, readonly FFN mode, FFN output shape `[2048]`, finite FFN output, zero NaN/Inf, non-empty FFN output digest, all forbidden paths false, output probe written, and receipt written.

## BLOCK Conditions
```text
MISSING_ASFT_HIDDEN_PROVIDER_PROBE
MISSING_ASFT_HIDDEN_PROVIDER_SMOKE_RECEIPT
MISSING_NATIVE_FORWARD_PATH_SELECTION
MISSING_NATIVE_FORWARD_PATH_SELECTION_RECEIPT
MISSING_READONLY_FORWARD_CANDIDATE
MISSING_READONLY_FORWARD_PREFLIGHT_RECEIPT
MISSING_MODEL_INPUT_PACKET
MISSING_TOKEN_ID_CANDIDATE
MISSING_RESOLVED_ROUTE_VIEW
HIDDEN_PROVIDER_RECEIPT_NOT_PASS
HIDDEN_PROBE_ID_MISMATCH
HIDDEN_SHAPE_MISMATCH
HIDDEN_FINITE_CHECK_FAILED
HIDDEN_NAN_DETECTED
HIDDEN_INF_DETECTED
NATIVE_ATLAS_FFN_NOT_SELECTED
NATIVE_ATLAS_FFN_BACKEND_MISSING
NATIVE_ATLAS_FFN_BACKEND_UNSUPPORTED
SILENT_FFN_BACKEND_FALLBACK
HIDDEN_INPUT_SOURCE_MODE_UNSUPPORTED
HIDDEN_VALUE_SOURCE_INVALID
HIDDEN_INPUT_REHYDRATION_FAILED
HIDDEN_INPUT_SHAPE_MISMATCH
FFN_RUNTIME_INPUT_MISSING
FFN_MODEL_SPEC_LOAD_FAILED
FFN_WEIGHT_BINDING_FAILED
FFN_SMOKE_FAILED
FFN_OUTPUT_SHAPE_MISMATCH
FFN_OUTPUT_FINITE_CHECK_FAILED
FULL_MODEL_FORWARD_CLAIM_DETECTED
ATTENTION_EXECUTION_DETECTED
LM_HEAD_EXECUTION_DETECTED
LOGITS_MATERIALIZATION_DETECTED
DECODE_DETECTED
SAMPLING_DETECTED
GENERATION_DETECTED
LOSS_BACKWARD_OPTIMIZER_DETECTED
WEIGHT_MUTATION_DETECTED
SILENT_CORRECTION_DETECTED
FFN_OUTPUT_PROBE_WRITE_FAILED
RECEIPT_WRITE_FAILED
```

## Implementation Files
```text
crates/base_train/src/ash_basetrain_gpu_70d_native_atlas_ffn_smoke.rs
crates/base_train/src/bin/ash_basetrain_gpu_70d_native_atlas_ffn_smoke.rs
```

## Cargo Surface
```toml
burn_webgpu_backend = { path = "../burn_webgpu_backend" }
lora_train = { path = "../lora_train" }

[[bin]]
name = "ash_basetrain_gpu_70d_native_atlas_ffn_smoke"
path = "src/bin/ash_basetrain_gpu_70d_native_atlas_ffn_smoke.rs"
```

## Static Checks
GPU-70D static checks require module/bin/lib/Cargo surfaces, `burn_webgpu_backend` and `lora_train` dependencies, atlas grouped builder, map builder, hidden input source mode checks, FFN backend/policy checks, match validation, no large `json!`, no recursion-limit attribute, native atlas FFN smoke execution call, explicit hidden source mode, metadata-only hidden probe not treated as payload, FFN output probe declared, full model/attention/LM-head/logits/decode/sampling/generation/loss/backward/optimizer/weight mutation forbidden, and no `.sha256` sidecars.

## Next Stage
If GPU-70D PASS:
```text
ASH-BASETRAIN-GPU-70E
Hidden Provider And FFN Probe Compatibility Audit / No Logits No Decode Seal
```
If GPU-70D blocks due to hidden adapter:
```text
ASH-BASETRAIN-GPU-70D-R1
Hidden Probe To Native Atlas FFN Input Adapter Rebind / No Silent Hidden Payload Assumption Seal
```
If GPU-70D blocks due to FFN backend binding:
```text
ASH-BASETRAIN-GPU-70D-R2
Native Atlas FFN Runtime Binding Rebind / Explicit Gate Up Down Weight Path Seal
```
