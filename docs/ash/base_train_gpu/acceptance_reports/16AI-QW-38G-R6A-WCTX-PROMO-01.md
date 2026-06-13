# 16AI-QW-38G-R6A-WCTX-PROMO-01

## Runtime Adapter Evidence Interface / No Mock Shape Promotion Seal

### SSOT

- Domain: `en_to_ko_translation_subtitle_machine`
- Previous boundary: `WCTX-PROMO-00`
- This patch defines the interface-only entry point for real runtime adapter evidence.

### Contract

`PROMO-01` does not promote mock shape evidence into runtime evidence. It defines the runtime adapter evidence interface and keeps all execution paths closed.

Required invariant:

```txt
can_forward_dry_probe = true
forward_executed = false
mock_shape_promotion_allowed = false
real_runtime_adapter_required = true
```

### Positive surface

- `NativeWgpuModelAdapter` may be declared as interface-only evidence.
- `CpuReferenceModelAdapter` may be declared as interface-only evidence.
- `ExternalProcessBackendAdapter` may be declared as interface-only evidence.
- Capability flags may say that the adapter can later encode/forward/emit top-k.

### Forbidden surface

- mock shape registered as real runtime adapter
- static fixture registered as real runtime adapter
- receipt-only evidence registered as real runtime adapter
- synthetic evidence registered as real runtime adapter
- MOCK-20 shape reused as adapter identity
- MOCK-20 shape reused as RT-00 forward receipt
- encode / forward / logits / top-k / decode execution
- candidate text creation
- preview queue insert
- runtime apply
- weight commit

### Expected status

```txt
PASS_WCTX_PROMO_01_RUNTIME_ADAPTER_EVIDENCE_INTERFACE_NO_MOCK_SHAPE_PROMOTION
```

### Build mode

This baked artifact is produced in static mode because the current container has no `cargo` or `rustc`.

```txt
BAKED_STATIC_NO_CARGO
```
