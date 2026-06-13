# QW-TOK-00-R1 — Tokenizer V5 Append-only Vocab Cap 48259 Extension / No Existing ID Drift Seal

## SSOT
- Final manifest: `tokenizer_manifest_v5_final.json`
- Tokenizer ID: `tok_v5_20260417`
- Version: `20260417`
- Final vocab cap: `48259`
- Final ID range: `0..48258`
- Reserved IDs: `0..71`
- Byte tail: `48003..48258 = <byte:00>..<byte:FF>`

## Scope
This patch binds and validates the final manifest. It does not generate new reserved tail tokens and does not rewrite the SentencePiece model.

## Forbidden
- tokenizer retrain
- token remap
- id reorder
- vocab padding/truncation
- sentencepiece model rewrite
- embedding resize
- lm_head resize
- model weight mutation
- runtime decode bind
- sampler/QW/MCTS mutation

## Status
`PENDING_QW_TOK00_R1_BASELINE_DRIFT_NOT_VERIFIED` because final manifest validation passes but baseline drift comparison remains unavailable.

## Next
QW-TOK-00-R2 — Tokenizer V5 Local Artifact Hash Parity / Model Vocab Manifest Seal
