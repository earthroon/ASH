# QW-TOK-00-R3 — Embedding LMHead Row Parity 48259 Probe / No Resize Seal

## 확정

QW-TOK-00-R3는 Tokenizer V5 final vocab cap 48259가 모델 체크포인트/런타임의 token embedding rows, lm_head rows, runtime vocab cap, native vocab projection cap과 일치하는지 metadata/header 기반으로 검증하는 패치다.

## 상태 귀속 위치

- 귀속: model config vocab size, embedding row count, lm_head row count, runtime vocab cap, native vocab projection cap, checkpoint/runtime spec drift receipt.
- 비귀속: tokenizer rewrite, embedding/lm_head resize, checkpoint write, model weight mutation, runtime decode binding, sampler/QW/MCTS mutation.

## SSOT 존재 여부

- Tokenizer final vocab SSOT: QW-TOK-00-R1 final manifest, vocab size 48259.
- Local artifact hash parity: QW-TOK-00-R2 report.
- Model row parity SSOT: 이번 패치에서 probe/report 구조 생성.

## 재현 가능성

```powershell
cargo check -p model_core --lib
cargo test -p model_core qw_tok00_r3 --test qw_tok00_r3_embedding_lmhead_row_parity
cargo test -p model_core qw_tok00_r3 --test qw_tok00_r3_no_resize_no_checkpoint_mutation
cargo test -p model_core qw_tok00_r3 --test qw_tok00_r3_runtime_vocab_projection_cap
```

## 금지 계약

- embedding resize 금지
- lm_head resize 금지
- checkpoint rewrite/repack 금지
- model weight mutation 금지
- vocab padding/truncation/token remap 금지
- runtime decode/sampler/QW selector/MCTS mutation 금지
- unknown row parity 상태에서 PASS 처리 금지

## Acceptance

- probe 구조 생성
- 값이 unknown이면 PENDING
- 명시 mismatch면 FAILED
- 모든 행/캡 값이 48259이고 mutation flag가 false면 PASS 가능
- trace/receipt/report 생성
