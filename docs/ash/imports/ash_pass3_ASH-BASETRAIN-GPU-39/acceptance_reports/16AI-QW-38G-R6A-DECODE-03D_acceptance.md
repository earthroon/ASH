# 16AI-QW-38G-R6A-DECODE-03D Acceptance

## Status
STATIC_BAKE_DEFINED_NOT_RUN

## Accepted static surface
- `DynamicSamplerMode` default-off gate added.
- Controlled / strict-controlled gate decision added.
- Applied config overlay data structure added.
- Min-p unsupported backend guard added.
- Rollback / safe-stop / EOS candidate non-execution contract added.
- JSONL receipt and summary writer added.
- Sampler parity append chain now invokes DECODE-03D receipt hook after DECODE-03C.

## Runtime acceptance pending
- `cargo check -p model_core`
- `cargo test -p model_core decode03d_*`
- Controlled run with DECODE-03A/03B/03C receipts enabled
- Confirmation that `behavior_change` only occurs under controlled gate
- Confirmation that rollback/safe-stop/EOS candidates remain unexecuted

## Next patch candidate
16AI-QW-38G-R6A-SALAD-02 — Word Salad Online Detector Seal
