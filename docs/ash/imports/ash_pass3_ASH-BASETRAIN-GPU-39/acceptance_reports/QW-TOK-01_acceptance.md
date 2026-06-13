# QW-TOK-01 Acceptance

## Current bake status

`PENDING_QW_TOK01_TOKENIZER_LOADER_UNAVAILABLE`

## PASS criteria

- tokenizer loader available
- tokenizer loaded
- piece size 48259
- all required special tokens present and atomic
- roundtrip fixture cases pass
- byte fallback fixture passes
- no runtime bind / no inference / no mutation

## Current sealed state

This bake installs the fixture layer. Operator local tokenizer access is still required for runtime PASS.
