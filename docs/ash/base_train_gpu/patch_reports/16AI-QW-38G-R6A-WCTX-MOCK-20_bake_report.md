# 16AI-QW-38G-R6A-WCTX-MOCK-20 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-20`  
`Real Runtime Receipt Shape Draft / No Forward No Decode Seal`

## SSOT

- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Base artifact: `ash_pass3_WCTX-MOCK-19_handoff_preflight_baked.zip`
- State owner: `crates/ash_core/src/word_context_mock_real_runtime_receipt_shape.rs`

## Implemented

- Added real runtime receipt shape draft module.
- Added CLI entrypoint for deterministic JSON emission.
- Added `lib.rs` module/export surface.
- Added 4 positive shape-draft cases.
- Added 25 negative boundary/leak cases.
- Added static checks and bake manifest.

## Positive cases

- `mock20:native_wgpu_receipt_shape_draft_ready`
- `mock20:cpu_reference_receipt_shape_draft_ready`
- `mock20:external_backend_receipt_shape_draft_ready`
- `mock20:lookahead_receipt_shape_draft_ready`

## Negative cases

The negative matrix covers missing upstream receipt keys, missing model/tokenizer/checkpoint/runtime-config hashes, missing output shape fields, generated candidate text leakage, forward/decode/generation/sampling/token-selection execution leaks, logits/KV-cache/final-receipt leaks, full-logits attachment, and production-safe leakage.

## Boundary

MOCK-20 only drafts future real-runtime receipt shape. It does not execute forward, decode, generation, sampling, token selection, logits computation, KV-cache allocation, runtime receipt finalization, full logits attachment, or candidate text generation.

## Static checks

```text
module_exists: True
bin_exists: True
lib_export_present: True
module_brace_balance: 0
bin_brace_balance: 0
case_push_count: 29
positive_case_count: 4
negative_case_count: 25
forward_block_present: True
decode_block_present: True
logits_block_present: True
kv_cache_block_present: True
runtime_receipt_finalized_block_present: True
candidate_text_generated_block_present: True
full_logits_block_present: True
acceptance_pass_field_present: True
output_paths_present: True
cargo_present: False
```

## Cargo status

`NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`
