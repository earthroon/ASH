# SFT-GPU-STREAM-02 Bake Report

## Patch

SFT-GPU-STREAM-02 - Native GPU LoRA Runtime Inference Streaming / Token Event Seal

## Files changed

- ADD `crates/ash_core/src/sft_gpu_stream_runtime_inference.rs`
- ADD `crates/ash_core/tests/sft_gpu_stream_02_runtime_inference_stream.rs`
- MOD `crates/ash_core/src/lib.rs`
- ADD `acceptance_reports/SFT-GPU-STREAM-02_native_gpu_lora_runtime_inference_streaming.md`
- ADD `bake_artifacts/SFT-GPU-STREAM-02_BAKE_REPORT.md`
- ADD `bake_artifacts/SFT-GPU-STREAM-02_STATIC_VALIDATION.txt`

## Opened

- Runtime smoke receipt intake
- Runtime attach for smoke only
- Runtime token ledger digest recording
- Native GPU runtime backend confirmation
- Runtime LoRA attachment observation
- LoRA logits delta observation

## Closed

- Runtime attach as current
- Production runtime attach
- Slot ready finalization
- ASH synapse binding
- Registry mutation
- Promotion apply
- Current pointer update

## Tests added

- `sft_gpu_stream_02_accepts_native_gpu_lora_runtime_token_stream`
- `sft_gpu_stream_02_rejects_base_only_fallback`
- `sft_gpu_stream_02_holds_when_lora_delta_not_observed`
- `sft_gpu_stream_02_rejects_token_sequence_gap`
- `sft_gpu_stream_02_rejects_device_fingerprint_mismatch`
- `sft_gpu_stream_02_rejects_current_pointer_update_flag`
- `sft_gpu_stream_02_holds_without_artifact_capture_seal`
- `sft_gpu_stream_02_holds_without_step_telemetry_seal`

## Local command to run

```bash
cargo test -p ash_core sft_gpu_stream_02 -- --nocapture
```
