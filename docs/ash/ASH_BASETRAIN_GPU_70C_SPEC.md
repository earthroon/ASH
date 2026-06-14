# ASH-BASETRAIN-GPU-70C SPEC

## Patch ID
ASH-BASETRAIN-GPU-70C

## Title
A-SFT Batched Hidden Provider Readonly Smoke / Forward Candidate To Hidden Probe Receipt Seal

## Seal
No Decode / No Sampling / No Generation / No Loss / No Backward / No Optimizer

## Purpose
GPU-70C consumes the GPU-70B native forward path selection envelope and executes only the selected `a_sft_batched_hidden_provider` path as a readonly smoke. The output is a hidden probe envelope. It is not logits, decoded text, sampling state, generation state, loss, gradients, optimizer state, or weight mutation.

GPU-70C must not execute `native_atlas_ffn_single_token`; that path remains reserved for GPU-70D.

## Input SSOT
```text
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
The runtime checkpoint is operator-local and may be absent from the baked ZIP. If the runtime model spec or checkpoint is missing, GPU-70C blocks with `ASFT_RUNTIME_INPUT_MISSING` and does not fake a hidden probe.

## Output SSOT
```text
artifacts/ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_PROBE.json
artifacts/ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_SMOKE_RECEIPT.json
```

## State Ownership
GPU-70C owns the A-SFT hidden provider smoke receipt, hidden probe envelope, hidden shape metadata, hidden finite-check result, hidden probe digest, and A-SFT provider backend evidence.

GPU-70C does not own the 70B path selection envelope, 69A readonly forward candidate, 68A model input packet, 67A token candidate, 65A resolved route view, native atlas FFN execution, FFN output probe, logits probe, decode, sampling, generation, loss, backward, optimizer, weight mutation, or production attach state.

## Required Upstream Facts
GPU-70C requires GPU-70B PASS and selected paths containing `a_sft_batched_hidden_provider` and `native_atlas_ffn_single_token`. GPU-70C requires GPU-70B execution flags to remain false: `forward_executed`, `hidden_provider_executed`, `ffn_probe_executed`, and `logits_materialized`.

GPU-70C requires GPU-69A readonly forward candidate to remain pre-execution only, GPU-68A model input shape `[1, 52]`, and GPU-67A token id candidate count `52`.

## A-SFT Hidden Provider Contract
Expected source path:
```text
crates/lora_train/src/a_sft_batched_hidden_provider.rs
```
Expected provider family:
```text
ASftBatchedHiddenProvider
ASftBatchedHiddenProvider::NativeWgpuBatched
NativeWgpuModel::from_full_checkpoints_with_vocab_atlas
forward_hidden_padded_batch
```
GPU-70C may use `NativeWgpuModel` only as a readonly hidden provider backend. GPU-70C must not claim logits, LM-head execution, decode, generation, loss, backward, optimizer, or weight mutation.

## Hidden Probe Policy
The hidden probe is metadata-only by default. It records shape, finite check, NaN/Inf counts, hidden digest, provider runtime label, and write receipt. It must not dump full hidden tensors by default.

Required hidden probe envelope ID:
```text
ash-basetrain-gpu-70c-asft-hidden-provider-probe-0000
```
Required backend:
```text
native_wgpu_batched
```
No silent CPU/reference fallback is allowed. If fallback is required or detected, GPU-70C blocks with `SILENT_HIDDEN_BACKEND_FALLBACK`.

## CLI
```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70c_asft_hidden_provider_smoke -- `
  --native-forward-path-selection .\artifacts\ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION.json `
  --native-forward-path-selection-receipt .\artifacts\ASH_BASETRAIN_GPU_70B_NATIVE_FORWARD_PATH_SELECTION_RECEIPT.json `
  --readonly-forward-candidate .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_CANDIDATE_ENVELOPE.json `
  --readonly-forward-preflight-receipt .\artifacts\ASH_BASETRAIN_GPU_69A_READONLY_FORWARD_PREFLIGHT_RECEIPT.json `
  --model-input-packet .\artifacts\ASH_BASETRAIN_GPU_68A_MODEL_INPUT_PACKET_ENVELOPE.json `
  --token-id-candidate .\artifacts\ASH_BASETRAIN_GPU_67A_TOKEN_ID_CANDIDATE_ENVELOPE.json `
  --resolved-route-view .\artifacts\ASH_BASETRAIN_GPU_65A_RESOLVED_DEFAULT_ROUTE_VIEW.json `
  --expected-native-forward-path-selection-id ash-basetrain-gpu-70b-native-forward-path-selection-0000 `
  --expected-readonly-forward-candidate-envelope-id ash-basetrain-gpu-69a-readonly-forward-candidate-envelope-0000 `
  --expected-model-input-packet-envelope-id ash-basetrain-gpu-68a-model-input-packet-envelope-0000 `
  --expected-token-id-candidate-envelope-id ash-basetrain-gpu-67a-token-id-candidate-envelope-0000 `
  --expected-selected-path a_sft_batched_hidden_provider `
  --expected-token-count 52 `
  --expected-model-input-batch-size 1 `
  --expected-model-input-sequence-len 52 `
  --hidden-provider-backend native_wgpu_batched `
  --hidden-probe-policy metadata_only_with_digest `
  --hidden-probe-envelope-id ash-basetrain-gpu-70c-asft-hidden-provider-probe-0000 `
  --model-spec .\specs\model_spec_v5_48259.toml `
  --checkpoint .\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors `
  --hidden-size 2048 `
  --out-hidden-probe .\artifacts\ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_PROBE.json `
  --out .\artifacts\ASH_BASETRAIN_GPU_70C_ASFT_HIDDEN_PROVIDER_SMOKE_RECEIPT.json
```

## PASS Conditions
GPU-70C PASS requires all input SSOT files, GPU-70B receipt PASS, selected path `a_sft_batched_hidden_provider`, backend `native_wgpu_batched`, successful readonly hidden provider smoke, hidden probe created, hidden shape verified, finite check PASS, zero NaN/Inf, non-empty hidden digest, and all forbidden paths remaining false.

## BLOCK Conditions
```text
MISSING_NATIVE_FORWARD_PATH_SELECTION
MISSING_NATIVE_FORWARD_PATH_SELECTION_RECEIPT
MISSING_READONLY_FORWARD_CANDIDATE
MISSING_READONLY_FORWARD_PREFLIGHT_RECEIPT
MISSING_MODEL_INPUT_PACKET
MISSING_TOKEN_ID_CANDIDATE
MISSING_RESOLVED_ROUTE_VIEW
NATIVE_FORWARD_PATH_SELECTION_RECEIPT_NOT_PASS
NATIVE_FORWARD_PATH_SELECTION_ID_MISMATCH
ASFT_HIDDEN_PROVIDER_NOT_SELECTED
NATIVE_ATLAS_FFN_SELECTION_MISSING
UPSTREAM_EXECUTION_ALREADY_PERFORMED
UPSTREAM_LOGITS_ALREADY_MATERIALIZED
FORWARD_CANDIDATE_ID_MISMATCH
FORWARD_EXECUTION_NOT_ALLOWED
READONLY_FORWARD_PREFLIGHT_RECEIPT_NOT_PASS
MODEL_INPUT_PACKET_ID_MISMATCH
MODEL_INPUT_SHAPE_MISMATCH
TOKEN_ID_CANDIDATE_ID_MISMATCH
TOKEN_ID_COUNT_MISMATCH
ASFT_HIDDEN_BACKEND_UNSUPPORTED
HIDDEN_PROBE_POLICY_UNSUPPORTED
SILENT_HIDDEN_BACKEND_FALLBACK
FORBIDDEN_RUNTIME_FLAG_ENABLED
ASFT_RUNTIME_INPUT_MISSING
ASFT_MODEL_SPEC_LOAD_FAILED
TOKEN_ID_RANGE_INVALID
HIDDEN_PROVIDER_SMOKE_FAILED
HIDDEN_FINITE_CHECK_FAILED
HIDDEN_PROBE_WRITE_FAILED
RECEIPT_WRITE_FAILED
```

## Implementation Files
```text
crates/base_train/src/ash_basetrain_gpu_70c_asft_hidden_provider_smoke.rs
crates/base_train/src/bin/ash_basetrain_gpu_70c_asft_hidden_provider_smoke.rs
```

## Cargo Surface
```toml
lora_train = { path = "../lora_train" }

[[bin]]
name = "ash_basetrain_gpu_70c_asft_hidden_provider_smoke"
path = "src/bin/ash_basetrain_gpu_70c_asft_hidden_provider_smoke.rs"
```

## Static Checks
GPU-70C static checks require module/bin/lib/Cargo surfaces, `lora_train` dependency, atlas grouped builder, map builder, hidden backend/policy checks, match validation, no large `json!`, no recursion-limit attribute, A-SFT provider smoke execution call, native atlas FFN forbidden flag, hidden probe output declared, logits/decode/sampling/generation/loss/backward/optimizer/weight mutation forbidden, and no `.sha256` sidecars.

## Next Stage
If GPU-70C PASS:
```text
ASH-BASETRAIN-GPU-70D
Native Atlas FFN Single Token Readonly Smoke / Hidden Probe To FFN Output Probe Seal
```
If GPU-70C blocks due to runtime binding:
```text
ASH-BASETRAIN-GPU-70C-R1
A-SFT Hidden Provider Runtime Binding Rebind / Explicit Native WGPU Backend No Silent Fallback Seal
```
