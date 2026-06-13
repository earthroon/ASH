# 16AI-QW-38G-R6A-WCTX-RT-06 Acceptance Report

## Acceptance contract

RT-06 accepts only surface-chain receipt binding as evidence. It must keep the chain below candidate text and review queue authority.

## Required static gates

- total cases >= 44: `44`
- positive cases >= 4: `4`
- negative cases >= 40: `40`
- chain digest match check present: `True`
- step digest check present: `True`
- token surface digest check present: `True`
- joined surface text block present: `True`
- decoded text block present: `True`
- candidate text block present: `True`
- candidate envelope block present: `True`
- review queue block present: `True`
- runtime apply block present: `True`
- training/backward/weight commit block present: `True` / `True` / `True`

## Verdict

`STATIC_ACCEPTANCE_READY_NO_CARGO`

The source files and CLI are baked. Runtime compilation and JSON generation require a local Rust toolchain.
