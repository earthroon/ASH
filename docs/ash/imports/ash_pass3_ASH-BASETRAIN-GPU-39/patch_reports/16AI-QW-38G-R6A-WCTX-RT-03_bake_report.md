# 16AI-QW-38G-R6A-WCTX-RT-03 Bake Report

## Patch
- `16AI-QW-38G-R6A-WCTX-RT-03`
- Controlled Decode One-Step Smoke / No Review Insert No Commit Seal

## Files Added
- `crates/ash_core/src/word_context_rt_controlled_decode_one_step_smoke.rs`
- `crates/ash_core/src/bin/ash_word_context_rt_controlled_decode_one_step_smoke.rs`

## Files Updated
- `crates/ash_core/src/lib.rs`

## Implemented Contract
- Binds RT-02 shadow selected token receipt.
- Binds RT-01 forward output shape receipt.
- Binds RT-00 forward dry probe receipt.
- Binds MOCK-20 runtime receipt shape draft.
- Allows one-step token surface decode smoke only.
- Blocks new token selection, selection commit, sequence decode, multi-token decode, decoded text, candidate text, candidate envelope finalization, review queue insert, auto accept, auto commit, target mutation, runtime apply, training, backward, and weight commit.

## Case Matrix
- Positive accepted cases: 4
- Negative blocked cases: 33
- Total cases: 37

## Build Status
- Static bake only in this container.
- `cargo` / `rustc` not available in the container, so compile/run was not executed here.
