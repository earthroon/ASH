# QW-TOK-00-R2 — Tokenizer V5 Local Artifact Hash Parity / Model Vocab Manifest Seal

## 확정

이 패치는 R1에서 봉인한 `tokenizer_manifest_v5_final.json`을 기준으로 로컬 `tokenizer_v5.model` 및 `tokenizer_v5.vocab`의 SHA256 parity를 검증하는 read-only 패치다.

- final manifest: `artifacts/tokenizer_manifest_v5_final.json`
- local artifacts dir: `D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts`
- expected vocab size: `48259`
- mutation: forbidden

## 금지

- tokenizer model/vocab rewrite
- vocab padding/truncation
- token remap / id reorder
- sentencepiece retrain
- embedding/lm_head resize
- runtime decode/sampler/QW/MCTS mutation

## Acceptance

1. manifest hash fields are loaded.
2. local model/vocab paths are recorded.
3. local files are hashed when accessible.
4. hash unknown is PENDING, not PASS.
5. hash mismatch is FAILED.
6. no artifact mutation is performed.
