# 16AI-QW-38G-R6A-WCTX-RT-06 Bake Report

## Patch

- `16AI-QW-38G-R6A-WCTX-RT-06`
- `Multi-Step Surface Chain Receipt Bind / No Candidate Text No Review Insert Seal`
- SSOT: `en_to_ko_translation_subtitle_machine`

## Baked scope

This bake adds the RT-06 surface-chain receipt bind layer. RT-06 consumes RT-05 multi-step surface-chain shadow receipts and binds chain digest, step order, step receipt keys, step digests, token surface digests, tokenizer identity, and upstream RT/MOCK receipt keys as evidence only.

RT-06 does **not** generate a new surface chain, join surfaces into text, create decoded text, create candidate text, finalize a candidate envelope, insert into review queue, commit, apply runtime state, train, run backward, or commit weights.

## Added files

- `crates/ash_core/src/word_context_rt_multi_step_surface_chain_bind.rs`
- `crates/ash_core/src/bin/ash_word_context_rt_multi_step_surface_chain_bind.rs`

## Updated files

- `crates/ash_core/src/lib.rs`

## Matrix coverage

- Positive accepted cases: `4`
- Negative blocked cases: `40`
- Total fixture cases: `44`

Positive cases:

- `rt06:two_step_surface_chain_receipt_bind`
- `rt06:four_step_surface_chain_receipt_bind`
- `rt06:eos_observed_surface_chain_receipt_bind_no_candidate`
- `rt06:hangul_surface_chain_receipt_bind`

Negative coverage includes:

- missing RT-05 / RT-04 / RT-03 / RT-02 / RT-01 / RT-00 / MOCK-20 upstream keys
- missing source / candidate envelope / provenance / review queue keys
- tokenizer identity mismatch
- surface chain too short / too long
- non-contiguous step order
- missing step receipts / step digests / token surface digests / chain digest
- chain digest mismatch
- unsafe special token
- surface bind not allowed
- new surface chain generation
- new decode / new token selection
- joined surface text present / persisted
- decoded text generated / present
- candidate text generated / present
- candidate envelope finalized
- review queue inserted
- auto accept / auto commit
- target mutation / runtime apply
- training / backward / weight commit

## Static status

- status: `BAKED_STATIC_NO_CARGO`
- cargo: `NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`
- module brace balance: `0`
- bin brace balance: `0`
- lib export present: `True`

## Local verification commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_multi_step_surface_chain_bind
cargo run -p ash_core --bin ash_word_context_rt_multi_step_surface_chain_bind
```

Expected output files after local run:

```text
workspace/word_context_probe/wctx_rt_06_multi_step_surface_chain_bind_cases.json
workspace/word_context_probe/wctx_rt_06_multi_step_surface_chain_bind_receipts.json
workspace/word_context_probe/wctx_rt_06_multi_step_surface_chain_bind_matrix.json
workspace/word_context_probe/wctx_rt_06_multi_step_surface_chain_bind_summary.json
workspace/word_context_probe/wctx_rt_06_multi_step_surface_chain_bind_sample_receipt.json
```
