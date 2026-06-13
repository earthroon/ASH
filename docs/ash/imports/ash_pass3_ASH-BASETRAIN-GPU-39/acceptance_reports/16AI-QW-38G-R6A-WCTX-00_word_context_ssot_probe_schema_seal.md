# 16AI-QW-38G-R6A-WCTX-00
## Word Context SSOT / Probe Schema Seal

Status: PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE

## Scope

This patch adds a Rust-native, probe-only Word Context SSOT to `ash_core`.
It records current-turn word-like spans, conservative initial roles, risk flags,
and deterministic receipt keys without mutating tokenizer ids, generation state,
LexGraph long-term memory, runtime defaults, or QWave activation.

## Files Added

- `crates/ash_core/src/word_context.rs`
- `crates/ash_core/src/bin/ash_word_context_probe.rs`
- `workspace/word_context_probe/ash_wctx_00_probe_korean_compound.json`
- `workspace/word_context_probe/ash_wctx_00_probe_contract_anchor.json`
- `workspace/word_context_probe/ash_wctx_00_probe_negation.json`
- `workspace/word_context_probe/ash_wctx_00_probe_technical.json`
- `workspace/word_context_probe/ash_wctx_00_probe_summary.json`
- `workspace/word_context_probe/ash_wctx_00_static_validation.json`

## Files Modified

- `crates/ash_core/src/lib.rs`
  - added `pub mod word_context;`
  - added `pub use word_context::*;`

## Rust SSOT Types

- `WordRole`
- `WordContextRelation`
- `WordContextSource`
- `CharSpan`
- `WordContextLink`
- `WordContextHit`
- `WordContextProbeRisk`
- `WordContextProbeReceipt`

## Public API

```rust
pub fn probe_word_context(input: &str) -> WordContextProbeReceipt
pub fn collect_char_spans(input: &str) -> Vec<(String, CharSpan)>
pub fn classify_initial_role(surface: &str) -> WordRole
pub fn build_receipt_key(
    input: &str,
    hits: &[WordContextHit],
    risk: &WordContextProbeRisk,
) -> String
```

## Non-Mutation Contract

The following flags are fixed by the probe path:

```text
token_id_mutated = false
generation_mutated = false
byte_leak_observed = false
```

This patch does not call runtime generation, sampler, tokenizer mutation,
LexGraph write, QWave apply, or any default-apply path.

## Static Validation

Static validation summary:

- `word_context.rs` exists
- `ash_word_context_probe.rs` exists
- `lib.rs` exports and re-exports the module
- core SSOT structs/enums are present
- `probe_word_context` is present
- deterministic receipt key builder is present
- 5 unit tests are embedded in `word_context.rs`
- sample receipts are written under `workspace/word_context_probe/`

Validation receipt:

- `workspace/word_context_probe/ash_wctx_00_static_validation.json`

## Runtime Caveat

`rustc` and `cargo` are not available in the current bake container, so this bake
does not claim compile/test execution. The status is therefore static-pass only.

## Acceptance Criteria

- PASS: Rust-native WordContext SSOT schema added.
- PASS: Probe-only public API added.
- PASS: Korean char/byte span logic implemented.
- PASS: Deterministic SHA-256 receipt key implemented.
- PASS: CLI probe binary added for later runtime receipt generation.
- PASS: Sample receipts generated.
- PASS: No runtime default apply added.
- PASS: No token id mutation path added.
- PASS: No generation mutation path added.
- HOLD: cargo test execution pending external Rust toolchain.

## Next Patch

Recommended next patch:

`16AI-QW-38G-R6A-WCTX-01 — Korean Word Context Smoke Corpus / Probe Regression Matrix Seal`
