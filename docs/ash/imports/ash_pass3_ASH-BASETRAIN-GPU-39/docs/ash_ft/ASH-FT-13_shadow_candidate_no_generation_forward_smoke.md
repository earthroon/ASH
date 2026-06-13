# ASH-FT-13 Shadow Candidate No-Generation Forward Smoke

ASH-FT-13 sits after ASH-FT-12 runtime metadata bind. It does not generate text. It only produces a bounded synthetic numeric forward smoke receipt so the chain can verify shape, finite status, checksum, and norm summary before any token-level behavior is opened.

This baked implementation deliberately keeps the output as numeric receipts only. No decoded text, next-token selection, sampling loop, KV-cache generation, user prompt inference, runtime default apply, or promotion is allowed.

## Command

```powershell
cargo run --bin ash_ft13_shadow_candidate_no_generation_forward_smoke -- `
  --shadow-candidate "artifacts\ash_ft\staging\ash_ft09_single_group_shadow_candidate.safetensors" `
  --expected-shadow-sha256 auto `
  --ft12-runtime-bind-plan "artifacts\ash_ft\ash_ft12_runtime_bind_plan.json" `
  --ft12-candidate-slot "artifacts\ash_ft\ash_ft12_candidate_slot_receipt.json" `
  --ft12-backend-compatibility "artifacts\ash_ft\ash_ft12_runtime_backend_compatibility.json" `
  --ft12-required-handle-lookup "artifacts\ash_ft\ash_ft12_required_handle_lookup_receipt.json" `
  --ft12-no-decode-guard "artifacts\ash_ft\ash_ft12_no_decode_guard.json" `
  --model-vocab-size 48259 `
  --tokenizer-vocab-size 48259 `
  --hidden-size 2048 `
  --forward-mode synthetic_single_step `
  --batch-size 1 `
  --seq-len 1 `
  --synthetic-token-id 0 `
  --max-forward-elements 262144 `
  --max-output-readback-bytes 1048576 `
  --allow-model-construction true `
  --allow-gpu-upload true `
  --decode false `
  --generation false `
  --sampling false `
  --user-prompt false `
  --runtime-default-apply false `
  --checkpoint-alias-rebind false `
  --promotion false `
  --worker-stack-mb 128 `
  --out-forward-plan "artifacts\ash_ft\ash_ft13_forward_smoke_plan.json" `
  --out-synthetic-input "artifacts\ash_ft\ash_ft13_synthetic_input_receipt.json" `
  --out-output-shape "artifacts\ash_ft\ash_ft13_forward_output_shape_receipt.json" `
  --out-forward-finite "artifacts\ash_ft\ash_ft13_forward_finite_receipt.json" `
  --out-no-decode-sampling-guard "artifacts\ash_ft\ash_ft13_no_decode_sampling_guard.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-13_receipt.json"
```
