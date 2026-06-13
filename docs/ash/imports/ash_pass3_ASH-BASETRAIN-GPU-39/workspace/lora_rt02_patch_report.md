# 16AI-QW-38G-R6A-LORA-RT-02

## Status

- patch: `16AI-QW-38G-R6A-LORA-RT-02`
- title: `Domain Adapter Runtime Logit Delta Hook / Shared Hidden Head Apply Seal`
- status: `STATIC_BAKED_PENDING_LOCAL_CARGO_CHECK`

## Implemented

- Added domain adapter runtime fields to `StandardInferRequest` and resolved request state.
- Added `NativeWgpuModel::configure_shared_hidden_head_domain_adapter(...)`.
- Added safetensors loading for `adapter.shared_hidden_token_head.lora_A`, `lora_B`, and `alpha`.
- Added CPU reference logit delta application at the final hidden projection boundary.
- Forced CPU logits materialization when the domain adapter is active, so delta is applied before repetition penalty and sampler postprocessors.
- Added apply receipt and delta trace emission.
- Embedded RT-02 apply receipt into orchestrator output/response when `domainAdapterApplyReceiptPath` is supplied.

## Seal

Base checkpoint, tokenizer, base safetensors, lm_head, final_norm, and persistent ban mask are not modified.

## Build Note

Cargo is not available in the bake container, so local `cargo check -p orchestrator_local --bin orchestrator_local --message-format short` is required.
