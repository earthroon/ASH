# 16AI-QW-38 — Word Salad Negative Corpus / Divergence Label Seal

## Status
PASS_STATIC_BAKE_SOURCE_ONLY

## Scope
QW-38 adds a Word Salad negative-corpus and divergence-label candidate layer on top of QW-35/QW-36/QW-37.

## Added source
- `crates/lora_train/src/word_salad_negative_corpus.rs`

## Modified source
- `crates/lora_train/src/lib.rs`
- `meta.json`

## Added artifacts
- `artifacts/word_salad_negative/qw38_word_salad_negative_corpus.jsonl`
- `artifacts/word_salad_negative/qw38_word_salad_label_report.json`
- `artifacts/word_salad_negative/qw38_word_salad_corpus_receipt.json`

## Confirmed policy surface
- `affects_loss_candidate = true`
- `affects_total_loss = false`
- `affects_gradient = false`
- `affects_optimizer = false`
- `affects_lora_weights = false`
- `affects_base_model = false`

## Guarded non-mutations
- no backward execution
- no optimizer step
- no LoRA weight mutation
- no base model mutation
- no token/vocab/embedding mutation
- no runtime pointer mutation
- no sampler/backend mutation

## Corpus contents
The baked fixture corpus contains good/bad pairs for:
- repetition loop
- ending / sentence closure failure
- foreign token and symbol intrusion
- QWave curvature / phase / binding divergence labels
- Hangul geometry divergence labels

## Acceptance criteria covered statically
- QW-35/QW-36/QW-37 receipt references are represented in the QW-38 receipt.
- `sample_id`, `pair_id`, `failure_tags`, `primary_failure_tag`, hashes, and `word_salad_score` fields are present in JSONL samples.
- `word_salad_score` is finite and constrained to the 0.0..1.0 range in baked fixtures.
- Corpus report and receipt are emitted.

## Native execution note
`cargo`/`rustc` is unavailable in the current container, so no native Rust compile, unit test, or runtime training execution was performed. This is a static source bake with explicit non-execution metadata.
