# WCTX-PROMO-02 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-PROMO-02`

`Runtime Identity Evidence Bind / Model Tokenizer Checkpoint Config Hash Seal`

## Files added

- `crates/ash_core/src/word_context_promo_02_runtime_identity_evidence_bind.rs`
- `crates/ash_core/src/bin/ash_word_context_promo_02_runtime_identity_evidence_bind.rs`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-PROMO-02.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-PROMO-02_bake_report.md`
- `WCTX_PROMO_02_STATIC_CHECKS.txt`
- `WCTX_PROMO_02_BAKE_MANIFEST.json`

## Files modified

- `crates/ash_core/src/lib.rs`

## Seal

`PROMO-02` binds model/tokenizer/checkpoint/runtime config identity hashes and an identity bundle digest to the runtime adapter interface. It does not execute encode, forward, logits emission, top-k emission, decode, generation, selection, candidate text creation, queue insertion, approval, commit, runtime apply, or weight mutation.

## Local verification command

```bash
cargo check -p ash_core --bin ash_word_context_promo_02_runtime_identity_evidence_bind
cargo run -p ash_core --bin ash_word_context_promo_02_runtime_identity_evidence_bind
```

## Container verification limit

`cargo` and `rustc` are unavailable in the current container, so this bake is sealed as `BAKED_STATIC_NO_CARGO`.
