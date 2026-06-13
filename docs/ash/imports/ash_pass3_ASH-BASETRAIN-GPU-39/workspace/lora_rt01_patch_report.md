# 16AI-QW-38G-R6A-LORA-RT-01 — Domain Adapter Runtime Attach / Scale-Gated Logit Delta Seal

## Status

`PASS_STATIC_LORA_RT01_DOMAIN_ADAPTER_PREFLIGHT_BAKED_PENDING_LOCAL_CARGO_BUILD`

## Scope

This bake adds domain adapter manifest/safetensors validation for `shared_hidden_token_head_lora` pilot adapters and embeds an attach receipt into inference output artifacts/responses.

## Important SSOT

The current runtime entrypoint does not yet expose a hidden-state logit-delta hook where `final_logits = base_logits + scale * (alpha / rank) * (B @ (A @ hidden))` can be safely applied. Therefore this bake is honest about the state:

- adapter manifest/safetensors validation: implemented
- scale clamp: implemented
- attach receipt output: implemented
- output artifact embedding: implemented
- actual logit delta application: **not applied yet**
- next hook patch: `16AI-QW-38G-R6A-LORA-RT-02`

When the adapter artifact validates, receipt status is:

`PARTIAL_DOMAIN_ADAPTER_VALIDATED_RUNTIME_DELTA_HOOK_PENDING`

This prevents SSOT pollution by not claiming that logits were modified before the runtime/model_core hook exists.

## Changed files

- `crates/orchestrator_local/src/lib.rs`
- `crates/orchestrator_local/src/infer_entry.rs`
- `crates/orchestrator_local/src/domain_adapter_runtime.rs`
- `workspace/examples/lora_rt01_baseline.ps1`
- `workspace/examples/lora_rt01_scale025.ps1`
- `workspace/examples/lora_rt01_verify.ps1`

## Validation fields

- `domainAdapterAttachReceipt`
- `domainAdapterAttachReceiptPath`
- `domainAdapterRuntimePatchId`
- `domainAdapterId`
- `domainAdapterScale`
- `domainAdapterRuntimeAttachMode`
- `domainAdapterDeltaStats`

## No mutation contract

- `checkpoint_modified = false`
- `tokenizer_modified = false`
- `base_safetensors_modified = false`
- `lm_head_modified = false`
- `final_norm_modified = false`
- `ban_mask_modified = false`
