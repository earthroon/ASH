# 16AI-QW-38G-R6A-WCTX-04 Bake Report

## SSOT

`Ash = EN-to-KO translation subtitle machine`

## Baked result

Added `word_context_edge_registry.rs` and `ash_word_context_edge_registry.rs` to convert WCTX-03 term graph split receipts into typed edge registry receipts.

## Implemented public API

```rust
pub fn default_enko_typed_edge_registry_split_receipts() -> Vec<EnKoSubtitleTermGraphSplitReceipt>

pub fn register_enko_typed_edges_shadow(
    split_receipt: &EnKoSubtitleTermGraphSplitReceipt,
) -> EnKoTypedEdgeRegistryReceipt

pub fn run_enko_typed_edge_registry_matrix(
    split_receipts: &[EnKoSubtitleTermGraphSplitReceipt],
) -> EnKoTypedEdgeRegistryMatrix

pub fn confidence_band(score: f32) -> EnKoRelationConfidenceBand
```

## Relation registry

Implemented typed relation kinds including:

- `source_target_translation_candidate`
- `negation_alignment`
- `proper_noun_preserve`
- `glossary_required`
- `preserve_required`
- `speaker_register_carry`
- `same_speaker_continuity`
- `linebreak_pressure`
- `compression_pressure`
- `timing_density_pressure`
- `reading_speed_pressure`
- `previous_cue_reference`
- `next_cue_setup`
- `timing_contains`
- `unknown`

## Guarded non-actions

The patch keeps the following sealed false:

- token mutation
- generation mutation
- source text mutation
- target text mutation
- timing mutation
- glossary auto-apply
- preserve auto-apply
- stable graph promotion
- ContextPlan creation
- candidate rerank
- runtime default apply

## Validation status

`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

The container does not include Rust toolchain binaries, so this bake provides static Rust files and precomputed static JSON receipts, not executed cargo results.
