# 16AI-QW-38G-R6A-WCTX-PROMO-02

## Runtime Identity Evidence Bind / Model Tokenizer Checkpoint Config Hash Seal

### SSOT

- Domain: `en_to_ko_translation_subtitle_machine`
- Previous boundary: `WCTX-PROMO-00`
- Previous adapter interface: `WCTX-PROMO-01`
- This patch binds adapter identity to model/tokenizer/checkpoint/runtime config hash evidence.

### Contract

`PROMO-02` does not tokenize, forward, decode, emit logits, emit top-k, create candidate text, insert queues, approve, commit, apply, or mutate weights. It only proves that a real runtime adapter identity carries the four required hash anchors and a bundle digest.

Required invariant:

```txt
model_spec_hash_bound = true
tokenizer_spec_hash_bound = true
checkpoint_hash_bound = true
runtime_config_hash_bound = true
identity_bundle_digest_bound = true
forward_executed = false
mock_identity_promotion_allowed = false
```

### Positive surface

- `NativeWgpuModelAdapter` may bind identity hash evidence without execution.
- `CpuReferenceModelAdapter` may bind identity hash evidence without execution.
- `ExternalProcessBackendAdapter` may bind identity hash evidence without execution.
- Capability flags may say the adapter can later encode/forward/emit top-k.

### Forbidden surface

- missing PROMO-00 boundary
- missing PROMO-01 adapter interface
- missing model/tokenizer/checkpoint/runtime config hash
- missing identity bundle digest
- placeholder hash accepted as bound identity
- identity bundle digest mismatch
- mock / fixture / receipt-only / synthetic identity promotion
- MOCK-20 shape reused as identity bundle or any of the four hash anchors
- encode / forward / logits / top-k / decode execution
- candidate text creation
- preview queue insert
- runtime apply
- weight commit

### Expected status

```txt
PASS_WCTX_PROMO_02_RUNTIME_IDENTITY_EVIDENCE_BIND_MODEL_TOKENIZER_CHECKPOINT_CONFIG_HASH_SEAL
```

### Build mode

This baked artifact is produced in static mode because the current container has no `cargo` or `rustc`.

```txt
BAKED_STATIC_NO_CARGO
```
